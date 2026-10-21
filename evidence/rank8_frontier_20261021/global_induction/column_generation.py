"""Exact-oracle column generation for the complete central-induction cone."""
import argparse,json,math,os,sys,time,traceback
from fractions import Fraction as Q
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import streaming as st
from exact import require
import sympy as s

_cones={}
def kinds(variant):
    require(variant in ('streaming','frame','spectral_frame','sts_frame'),'unknown induction variant')
    return (f'frontier_{variant}_induction',f'frontier_{variant}_cone_feasible',f'frontier_{variant}_induction_lift')
def variant_for(kind):
    for variant in ('streaming','frame','spectral_frame','sts_frame'):
        if kind in kinds(variant):return variant
    raise ValueError('unknown frontier induction certificate kind')
def cone(R,height,variant='streaming'):
    key=(st.digest(R),height,variant)
    if key not in _cones:
        if variant=='sts_frame':
            from sts_frame import STSFrameCone
            cls=STSFrameCone
        elif variant=='spectral_frame':
            from spectral_frame import SpectralFrameCone
            cls=SpectralFrameCone
        elif variant=='frame':
            from frame_cone import FrameCone
            cls=FrameCone
        else:cls=st.Cone
        _cones[key]=cls(R,height)
    return _cones[key]

def active_rows(C,active):
    rows=[{} for _ in range(C.nrows)]
    for local,index in enumerate(active):
        for row,value in C.column(index).items():rows[row][local]=value
    return rows

def phase_one(rows,b,nvars,seconds):
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix,eye,hstack
    m=len(b);scales=np.array([max(1,abs(bb),max(map(abs,row.values()),default=0)) for row,bb in zip(rows,b)],dtype=float)
    rr=[];cc=[];vv=[]
    for i,row in enumerate(rows):
        for j,v in row.items():rr.append(i);cc.append(j);vv.append(float(v)/scales[i])
    matrix=coo_matrix((vv,(rr,cc)),shape=(m,nvars)).tocsc();identity=eye(m,format='csc');start=time.monotonic()
    answer=linprog(np.r_[np.zeros(nvars),np.ones(2*m)],A_eq=hstack([matrix,identity,-identity],format='csc'),b_eq=np.asarray(b,dtype=float)/scales,bounds=(0,None),method='highs',options={'time_limit':seconds})
    answer.frontier_scales=scales
    return answer,{'status':int(answer.status),'message':answer.message,'objective':float(answer.fun) if answer.fun is not None else None,'seconds':round(time.monotonic()-start,3)}

def reuse_dual(rows,b,nvars,answer):
    """Propose from the already computed dual; exact checks remain mandatory."""
    ray=[-float(x)/float(scale) for x,scale in zip(answer.eqlin.marginals,answer.frontier_scales)]
    maximum=max(map(abs,ray),default=0.)
    if not maximum:return None
    ray=[x/maximum for x in ray]
    for bound in (100,1000,10000,100000,1000000,10000000):
        values=[Q(x).limit_denominator(bound) for x in ray];den=math.lcm(*(x.denominator for x in values));y=[int(x*den) for x in values];g=math.gcd(*y) or 1;y=[x//g for x in y]
        if st.old.check(rows,b,y,nvars,False):return y
    return None

def exact_feasible(C,active,b,numerical):
    # HiGHS basic solutions have a small support. All arithmetic below is exact.
    for threshold in (1e-9,1e-12,0.):
        positions=[j for j,x in enumerate(numerical) if x>threshold]
        if not positions:continue
        columns=[C.column(active[j]) for j in positions]
        matrix=s.Matrix([[col.get(i,0) for col in columns] for i in range(C.nrows)])
        try:solution,parameters,free=matrix.gauss_jordan_solve(s.Matrix(b),freevar=True)
        except ValueError:continue
        for denominator in (1000,1000000,1000000000):
            subs={parameters[k,0]:s.Rational(Q(float(numerical[positions[j]])).limit_denominator(denominator)) for k,j in enumerate(free)}
            values=list(solution.subs(subs));weights=[Q(int(x.p),int(x.q)) for x in values]
            if any(x<0 for x in weights):continue
            support=[active[j] for j,x in zip(positions,weights) if x];weights=[x for x in weights if x]
            result={'indices':support,'weights':list(map(str,weights))}
            return result
    return None

def solve_case(C,ep,active,batch,lp_seconds,progress):
    b=C.rhs_for(ep);active=set(active);iterations=[];seen=set();round_no=0
    while True:
        round_no+=1;ordered=sorted(active);rows=active_rows(C,ordered)
        answer,lp=phase_one(rows,b,len(ordered),lp_seconds)
        record={'iteration':round_no,'active_columns':len(ordered),'lp':lp}
        if not answer.success:
            record['outcome']='numerical_solver_incomplete';iterations.append(record);progress(iterations)
            return None,None,active,iterations
        feasible=exact_feasible(C,ordered,b,answer.x[:len(ordered)]) if answer.fun<1e-7 else None
        if feasible is not None:
            C.check_feasible(feasible['indices'],feasible['weights'],ep)
            record.update(outcome='exact_feasible',support=len(feasible['indices']));iterations.append(record);progress(iterations)
            return None,feasible,active,iterations
        # The published proposal helper already performs exact reconstruction
        # on this small restricted cone. Its result is then checked against
        # every column of the complete domain by the new exact oracle.
        y=reuse_dual(rows,b,len(ordered),answer)
        if y is None:y=st.old.farkas(rows,b,len(ordered),True)
        if y is None:
            record.update(outcome='exact_reconstruction_incomplete',proposal=st.old.farkas.last_status);iterations.append(record);progress(iterations)
            return None,None,active,iterations
        require(sum(x*z for x,z in zip(b,y))<0,'restricted ray has wrong sign')
        report=C.oracle(y,batch);record.update(oracle=report)
        if not report['negative_columns']:
            value=C.check_farkas(y,ep);record['outcome']='full_exact_separator';iterations.append(record);progress(iterations)
            return {'indicators':list(ep),'y':y,'bTy':value},None,active,iterations
        added=set(report['violating_columns'])-active;require(added,'exact oracle violated a restricted column')
        record.update(outcome='columns_added',added=len(added));iterations.append(record);progress(iterations)
        active.update(added)
        signature=st.digest(sorted(active));require(signature not in seen,'column generation cycle');seen.add(signature)

def initial_columns(C):
    if hasattr(C,'initial_columns'):return C.initial_columns()
    zero=next((j for j,tt in enumerate(C.types) if not any(x for v in tt for x in v)),0)
    return set(range(C.offset))|set(range(C.high_end,C.nvars))|{C.offset+i*C.nt+zero for i in range(len(C.high))}

def verify_pseudo(R,c):
    variant=variant_for(c['kind']);require(c['kind']==kinds(variant)[0],'wrong streaming certificate kind');C=cone(R,c['height'],variant);require(C.meta==c['metadata'],'streaming domain metadata differs')
    choices=list(map(list,st.old.ht.indicator_choices(R)));require([b['indicators'] for b in c['cases']]==choices,'streaming indicator coverage incomplete')
    for branch in c['cases']:require(C.check_farkas(branch['y'],branch['indicators'])==branch['bTy'],'streaming Farkas value differs')

def install():
    st.old.install();import oriented_extension as oe
    if getattr(oe,'_frontier_streaming_installed',False):return
    original=oe.pseudo_check
    def check(R,c):return verify_pseudo(R,c) if c['kind'] in [kinds(v)[0] for v in ('streaming','frame','spectral_frame','sts_frame')] else original(R,c)
    oe.pseudo_check=check;oe._frontier_streaming_installed=True

def verify(R,c):
    install();variant=variant_for(c['kind']);KIND,FEASIBLE_KIND,LIFT_KIND=kinds(variant)
    if c['kind']==LIFT_KIND:
        import advanced_criteria
        return advanced_criteria.verify(R,c['general'])
    if c['kind']==FEASIBLE_KIND:
        C=cone(R,c['height'],variant);require(C.meta==c['metadata'],'feasible domain metadata differs')
        require(c['indicators'] in list(map(list,st.old.ht.indicator_choices(R))),'ineligible feasible indicator assignment')
        return C.check_feasible(c['indices'],c['weights'],c['indicators'])
    return verify_pseudo(R,c)

def run(source,height,batch,lp_seconds,dest,variant='streaming'):
    KIND,FEASIBLE_KIND,LIFT_KIND=kinds(variant)
    start=time.monotonic();out={'id':source['id'],'tensor_sha256':source['tensor_sha256'],'status':'running','method':variant+'_global_column_generation','height':height}
    def save():
        out['seconds']=round(time.monotonic()-start,3);dest.parent.mkdir(parents=True,exist_ok=True);temp=dest.with_suffix('.tmp');temp.write_text(json.dumps(out,separators=(',',':'))+'\n');temp.replace(dest)
    try:
        install();R=source['tensor'];C=cone(R,height,variant);out['metadata']=C.meta;out['indicator_attempts']=[];save();active=initial_columns(C);cases=[]
        for ep in st.old.ht.indicator_choices(R):
            attempt={'indicators':list(ep),'iterations':[]};out['indicator_attempts'].append(attempt)
            def progress(iterations):attempt['iterations']=iterations;save();print(source['id'],'indicator',list(ep),'round',len(iterations),iterations[-1]['outcome'],iterations[-1]['active_columns'],flush=True)
            certificate,feasible,active,iterations=solve_case(C,ep,active,batch,lp_seconds,progress)
            if feasible is not None:
                c={'kind':FEASIBLE_KIND,'height':height,'metadata':C.meta,'indicators':list(ep),**feasible};verify(R,c);out.update(status='exact_feasible_relaxation',certificate=c,scope='pseudo_unitary_induction_relaxation');save();return out
            if certificate is None:out['status']='search_incomplete';save();return out
            cases.append(certificate);out['partial_pseudo_certificate']={'kind':KIND,'height':height,'metadata':C.meta,'cases':cases};save()
        pseudo=out.pop('partial_pseudo_certificate');verify_pseudo(R,pseudo);out.update(status='pseudo_certificate_verified',pseudo_certificate=pseudo);save()
        import character_induction
        general=character_induction.lift_general(R,pseudo,1200)
        if general is not None:
            c={'kind':LIFT_KIND,'general':general};verify(R,c);out.update(status='excluded',scope='general_complex_fusion_category',certificate=c)
        else:out['status']='pseudo_unitary_excluded_general_unresolved'
    except MemoryError as exc:out.update(status='resource_bound',error=repr(exc))
    except Exception as exc:out.update(status='error',error=repr(exc),traceback=traceback.format_exc())
    save();return out

def main():
    ap=argparse.ArgumentParser();group=ap.add_mutually_exclusive_group(required=True);group.add_argument('--ring');group.add_argument('--verify',type=str);ap.add_argument('--height',type=int,default=4);ap.add_argument('--batch',type=int,default=256);ap.add_argument('--lp-seconds',type=int,default=300);ap.add_argument('--q',type=int);ap.add_argument('--r',type=int);args=ap.parse_args()
    if args.q is not None:
        import general_global_convex
        require(args.r is not None,'both radicands needed');general_global_convex.install(args.q,args.r)
    if args.verify:
        row=json.loads(st.Path(args.verify).read_text());source=st.load_ring(row['id']);require(source['tensor_sha256']==row['tensor_sha256'],'replay source tensor mismatch');verify(source['tensor'],row['certificate']);print('PASS',row['id']);return
    source=st.load_ring(args.ring);out=run(source,args.height,args.batch,args.lp_seconds,st.HERE/'results'/f'{args.ring}_h{args.height}.json');print(source['id'],out['status'],out['seconds'],flush=True)
if __name__=='__main__':main()

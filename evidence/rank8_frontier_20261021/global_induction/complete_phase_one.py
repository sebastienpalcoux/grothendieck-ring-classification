"""Packed sparse full-cone phase I; exact certificates use frozen frontier cores.

Only discovery uses NumPy/SciPy. Exact replay delegates to the same full-domain
integer/rational checker as column generation; no new mathematical condition.
"""
import argparse,array,gc,json,math,time,traceback
from fractions import Fraction as Q
import column_generation as cg
from exact import require
s=cg.s;st=cg.st

def fast_column(C,index):
    # The original exact column constructor remains the verifier. This
    # discovery builder contracts already-scaled integer bilinear features
    # against one common phase denominator, avoiding repeated Fraction work.
    if index<C.offset or index>=C.high_end:return C.column(index)
    out=st.Cone.column(C,index);orbit,ti=divmod(index-C.offset,C.nt)
    if hasattr(C,'sts_products'):
        products=C.sts_products[orbit];rows=C.sts_rows;trace=C.sts_trace1[ti]
    elif hasattr(C,'extra_products'):
        products=C.extra_products[orbit];rows=C.sts_rows;trace=C.extra_traces[ti]
    else:return out
    den=math.lcm(*(x.denominator for x in trace));nums=[int(x*den) for x in trace]
    for rr,product in zip(rows,products):
        for k,row in enumerate(rr):
            numerator=sum(product[l][k]*nums[l] for l in range(C.width));require(numerator%den==0,'packed modular coefficient not integral');value=numerator//den
            if value:out[row]=value
    return out

def packed(C):
    import numpy as np
    from scipy.sparse import coo_matrix
    samples=range(C.nvars) if C.nvars<3000 else sorted({i*(C.nvars-1)//63 for i in range(64)})
    for j in samples:require(fast_column(C,j)==C.column(j),'packed discovery column differs from exact operator')
    rr=array.array('i');cc=array.array('i');vv=array.array('d');scales=np.ones(C.nrows)
    for i,x in enumerate(C.rhs_for([1]*7)):scales[i]=max(1,abs(x))
    for j in range(C.nvars):
        for i,x in fast_column(C,j).items():rr.append(i);cc.append(j);vv.append(float(x));scales[i]=max(scales[i],abs(float(x)))
    rows=np.frombuffer(rr,dtype=np.int32);cols=np.frombuffer(cc,dtype=np.int32);values=np.frombuffer(vv,dtype=np.float64)
    for start in range(0,len(values),1000000):values[start:start+1000000]/=scales[rows[start:start+1000000]]
    M=coo_matrix((values,(rows,cols)),shape=(C.nrows,C.nvars)).tocsc()
    return M,scales

def proposal(M,scales,b,seconds):
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import eye,hstack
    m=len(b);n=M.shape[1];I=eye(m,format='csc');start=time.monotonic()
    answer=linprog(np.r_[np.zeros(n),np.ones(2*m)],A_eq=hstack([M,I,-I],format='csc'),b_eq=np.asarray(b,dtype=float)/scales,bounds=(0,None),method='highs',options={'time_limit':seconds})
    return answer,{'status':int(answer.status),'message':answer.message,'objective':float(answer.fun) if answer.fun is not None else None,'seconds':round(time.monotonic()-start,3)}

def exact_ray(C,M,scales,b,answer):
    import numpy as np
    ray=-np.asarray(answer.eqlin.marginals)/scales;maximum=max(abs(ray));require(maximum>0,'zero full-cone dual');ray/=maximum
    def integer(values):
        den=math.lcm(*(x.denominator for x in values));y=[int(x*den) for x in values];g=math.gcd(*y) or 1;return [x//g for x in y]
    def okay(y):
        return sum(x*z for x,z in zip(b,y))<0 and C.oracle(y,1)['negative_columns']==0
    for bound in (100,1000,10000,100000,1000000,10000000):
        y=integer([Q(float(x)).limit_denominator(bound) for x in ray])
        if okay(y):return y,{'method':'rational_denominator','bound':bound}
    gaps=M.T@(ray*scales);support=np.flatnonzero(abs(ray)>1e-12).tolist();positions={i:j for j,i in enumerate(support)}
    for tolerance in (1e-10,1e-9,1e-8):
        active=np.flatnonzero(abs(gaps)<tolerance).tolist();basis={};equations=[]
        for j in active:
            col=C.column(j);row=[Q(col.get(i,0)) for i in support];reduced=list(row)
            for pivot,other in sorted(basis.items()):
                c=reduced[pivot]
                if c:reduced=[x-c*y for x,y in zip(reduced,other)]
            pivot=next((i for i,x in enumerate(reduced) if x),None)
            if pivot is not None:
                c=reduced[pivot];basis[pivot]=[x/c for x in reduced];equations.append(row)
            if len(equations)>=len(support)-1:break
        equations.append([b[i] for i in support]);matrix=s.Matrix(equations);target=s.zeros(matrix.rows,1);target[-1]=-1
        try:solution,parameters,free=matrix.gauss_jordan_solve(target,freevar=True)
        except ValueError:continue
        numerical=ray/(-float(np.dot(np.asarray(b,dtype=float),ray)))
        for bound in (1000,1000000,1000000000):
            substitutions={parameters[k,0]:s.Rational(Q(float(numerical[support[j]])).limit_denominator(bound)) for k,j in enumerate(free)}
            candidate=list(solution.xreplace(substitutions));values=[Q(0)]*C.nrows
            for i,x in zip(support,candidate):values[i]=Q(int(x.p),int(x.q))
            y=integer(values)
            if okay(y):return y,{'method':'exact_active_face','tolerance':tolerance,'support':len(support),'equations':len(equations),'parameters':parameters.rows,'bound':bound}
    return None,{'method':'exact_reconstruction_incomplete','numeric_bTy':float(np.dot(np.asarray(b,dtype=float),ray))}

def run(source,variant,height,seconds,dest):
    start=time.monotonic();out={'id':source['id'],'tensor_sha256':source['tensor_sha256'],'status':'constructing_complete_domain','method':'packed_complete_sparse_phase_one','variant':variant,'height':height,'indicator_attempts':[]}
    def save():
        out['seconds']=round(time.monotonic()-start,3);dest.parent.mkdir(parents=True,exist_ok=True);tmp=dest.with_suffix('.tmp');tmp.write_text(json.dumps(out,separators=(',',':'))+'\n');tmp.replace(dest)
    save()
    try:
        cg.install();R=source['tensor'];C=cg.cone(R,height,variant);out['metadata']=C.meta;save();M,scales=packed(C);out.update(status='solving_complete_sparse_cone',nonzeros=int(M.nnz));save();print(source['id'],'complete matrix',M.shape,M.nnz,flush=True)
        KIND,FEASIBLE,LIFT=cg.kinds(variant);cases=[];rays=[]
        for ep in st.old.ht.indicator_choices(R):
            b=C.rhs_for(ep);attempt={'indicators':list(ep)};out['indicator_attempts'].append(attempt)
            y=next((yy for yy in rays if sum(x*z for x,z in zip(b,yy))<0),None)
            if y is None:
                answer,lp=proposal(M,scales,b,seconds);attempt['lp']=lp;save()
                if not answer.success:out['status']='numerical_solver_incomplete';save();return out
                feasible=cg.exact_feasible(C,range(C.nvars),b,answer.x[:C.nvars]) if answer.fun<1e-7 else None
                if feasible is not None:
                    c={'kind':FEASIBLE,'height':height,'metadata':C.meta,'indicators':list(ep),**feasible};cg.verify(R,c);out.update(status='exact_feasible_relaxation',scope='pseudo_unitary_induction_relaxation',certificate=c);save();return out
                y,report=exact_ray(C,M,scales,b,answer);attempt['reconstruction']=report
                if y is None:out['status']='exact_reconstruction_incomplete';save();return out
                rays.append(y)
            else:attempt['reused_exact_ray']=True
            value=C.check_farkas(y,ep);case={'indicators':list(ep),'y':y,'bTy':value};cases.append(case);out['partial_pseudo_certificate']={'kind':KIND,'height':height,'metadata':C.meta,'cases':cases};save();print(source['id'],'full exact separator',list(ep),flush=True)
        pseudo=out.pop('partial_pseudo_certificate');cg.verify_pseudo(R,pseudo);out.update(status='pseudo_certificate_verified',pseudo_certificate=pseudo);save();del M;gc.collect()
        import character_induction
        general=character_induction.lift_general(R,pseudo,1200)
        if general is not None:
            c={'kind':LIFT,'general':general};cg.verify(R,c);out.update(status='excluded',scope='general_complex_fusion_category',certificate=c)
        else:out['status']='pseudo_unitary_excluded_general_unresolved'
    except MemoryError as exc:out.update(status='resource_bound',error=repr(exc))
    except Exception as exc:out.update(status='error',error=repr(exc),traceback=traceback.format_exc())
    save();return out

def main():
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--ring');g.add_argument('--verify');ap.add_argument('--variant',default='sts_frame');ap.add_argument('--height',type=int,default=4);ap.add_argument('--lp-seconds',type=int,default=3600);args=ap.parse_args()
    if args.variant=='atomic_real_sts':import atomic_generation
    if args.variant=='atomic_spectrum':import atomic_spectrum_generation
    if args.verify:
        import atomic_generation,atomic_spectrum_generation
        row=json.loads(st.Path(args.verify).read_text());source=st.load_ring(row['id']);require(row['tensor_sha256']==source['tensor_sha256'],'source binding mismatch');cg.verify(source['tensor'],row['certificate']);print('PASS',row['id']);return
    source=st.load_ring(args.ring);dest=st.HERE/'complete_results'/f'{args.ring}_{args.variant}_h{args.height}.json'
    # A separate worker may finish a queued target first. The process lock
    # serializes discovery for that exact target; completed exact evidence
    # is replayed and retained instead of being overwritten.
    import fcntl
    dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.with_suffix('.lock').open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        previous=json.loads(dest.read_text()) if dest.exists() else None
        if previous and previous.get('status') in ('excluded','exact_feasible_relaxation'):
            require(previous['id']==source['id'] and previous['tensor_sha256']==source['tensor_sha256'],'existing completed source binding differs')
            cg.verify(source['tensor'],previous['certificate']);out=previous;print('REUSED exact completed target',source['id'],flush=True)
        else:out=run(source,args.variant,args.height,args.lp_seconds,dest)
    print(source['id'],out['status'],out['seconds'],flush=True)
if __name__=='__main__':main()

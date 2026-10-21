"""Global convex relaxation of commutative central induction.

Search is numerical; acceptance and replay use integer Farkas certificates.
Restored after workspace loss; all result certificates must be regenerated.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse,itertools,json,math,sys,time,traceback,os
if os.environ.get('RANK8_GLOBAL_MEMORY_MB'):
    import resource
    _memory=int(os.environ['RANK8_GLOBAL_MEMORY_MB'])*1024**2
    resource.setrlimit(resource.RLIMIT_AS,(_memory,_memory))
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path[:0]=[str(ROOT/'supplements/rank8/experimental_signed'),str(ROOT/'supplements/rank8/software'),str(HERE.parent/'noncommutative')]
import sympy as s
import higher_traces as ht
from exact import require

def biquadratic_polynomial(z,mul):
    z=tuple(map(Q,z));support=[i for i in range(1,4) if z[i]]
    if not support:return [Q(1),-z[0]]
    if len(support)==1:
        i=support[0];e=[Q(0)]*4;e[i]=Q(1);q=mul(e,e)[0]
        return [Q(1),-2*z[0],z[0]*z[0]-q*z[i]*z[i]]
    powers=[z]
    for k in range(3):powers.append(mul(powers[-1],z))
    traces=[4*v[0] for v in powers];elementary=[Q(1)]
    for k in range(1,5):
        elementary.append(sum(((-1)**(i-1)*elementary[k-i]*traces[i-1] for i in range(1,k+1)),Q(0))/k)
    return [(-1)**i*x for i,x in enumerate(elementary)]

def biquadratic_high(a,bq):
    high=[];dimensions=a['dimensions'];D=a['global_dimension'];mul=bq.mul
    candidates=bq.native(a['Gram'].extract(range(1,8),range(1,8)))
    print('global high candidates',len(candidates),flush=True)
    for v in candidates:
        z=tuple(sum((Q(v[i])*dimensions[i+1][c] for i in range(7)),Q(0)) for c in range(4))
        conjugates=[(z[0],e*z[1],f*z[2],e*f*z[3]) for e,f in [(-1,1),(1,-1),(-1,-1)]]
        numerator=mul(mul(conjugates[0],conjugates[1]),conjugates[2]);norm=mul(z,numerator)
        require(not any(norm[1:]),'field norm not rational')
        if not norm[0]:continue
        quotient=tuple(x/norm[0] for x in mul(D,numerator))
        if any(x.denominator!=1 for x in biquadratic_polynomial(quotient,mul)):continue
        cp=biquadratic_polynomial(z,mul);degree=len(cp)-1
        require(all(x.denominator==1 for x in cp),'central dimension nonintegral')
        nn=abs(int(cp[-1]));require(nn>0,'zero central dimension norm')
        if any(int(c)**degree%nn**j for j,c in enumerate(cp[1:],1)):continue
        high.append((tuple(map(int,v)),z))
    return high

_data_cache={}
_system_cache={}
def ring_key(R):return tuple(x for matrix in R for row in matrix for x in row)
def setup(R):
    key=ring_key(R)
    if key not in _data_cache:_data_cache[key]=_setup(R)
    return _data_cache[key]
def build(R,a,height):
    key=(ring_key(R),height)
    if key not in _system_cache:_system_cache[key]=_build(R,a,height)
    return _system_cache[key]

def _setup(R):
    import rank8_signed_bridge
    rank8_signed_bridge.install()
    require(len(R)==8 and all(R[i][j]==R[j][i] for i in range(8) for j in range(8)),'commutative rank eight required')
    original=ht.low_matrices;ht.low_matrices=lambda *args,**kwargs:[]
    try:a=ht.quadratic_data(R)
    finally:ht.low_matrices=original
    if a is not None:
        import tensor_rotation
        a['width']=2;a['B']=a['ch'].C;a['mul']=lambda x,y:ht.mul(x,y,a['q'])
        a['traces']=lambda height:ht.trace_types(a['q'],a['primes'],height)
        a['rotations']=lambda order,rs:tensor_rotation.rotation_types(a['q'],order,rs)
        a['high']=ht.high_columns(a,s.Matrix([1]+[0]*7))[1]
        a['field']={'degree':a['factor'].degree(),'q':a['q'],'primes':a['primes']}
    else:
        import biquadratic_commutative
        bq,lift=biquadratic_commutative.install()
        old=bq.low_frames;bq.low_frames=lambda *args,**kwargs:[]
        try:a=bq.data(R)
        finally:bq.low_frames=old
        a['width']=4;a['B']=a['Gram'];a['mul']=bq.mul;a['traces']=bq.trace_types
        a['rotations']=lambda order,rs:bq.trace_types(order,s.divisors(order),rs)[0]
        a['high']=biquadratic_high(a,bq)
        a['field']={'degree':4,'radicands':[2,3],'primes':[2,3]}
    require(all(a['columns']),'empty low restriction set')
    return a

def _build(R,a,height):
    width=a['width'];dimensions=a['dimensions'];D=a['global_dimension'];mul=a['mul']
    types,bound=a['traces'](height)
    lows=[]
    for group,columns in enumerate(a['columns']):
        for c in columns:
            z=tuple(sum((Q(c[i])*dimensions[i][k] for i in range(8)),Q(0)) for k in range(width))
            lows.append((group,tuple(map(int,c)),z))
    labels=[(v,z,ti) for v,z in a['high'] for ti in range(len(types))]
    offset=len(lows);nvars=offset+len(labels);rows=[];rhs=[];indicator_rows=[]
    for group in range(len(a['columns'])):
        rows.append({j:Q(1) for j,(g,c,z) in enumerate(lows) if g==group});rhs.append(Q(1))
    for i,j in itertools.combinations_with_replacement(range(8),2):
        row={k:Q(c[i]*c[j]) for k,(g,c,z) in enumerate(lows) if c[i]*c[j]}
        if i and j:
            row.update({offset+k:Q(v[i-1]*v[j-1]) for k,(v,z,ti) in enumerate(labels) if v[i-1]*v[j-1]})
        rows.append(row);rhs.append(Q(int(a['B'][i,j])-int(i==j==0)))
    moments=[[mul(z,tt) for tt in types[ti]] for v,z,ti in labels]
    for power in (1,2):
        for i in range(1,8):
            for coord in range(width):
                row={k:c[i]*z[coord] for k,(g,c,z) in enumerate(lows) if c[i]*z[coord]}
                row.update({offset+k:v[i-1]*moments[k][power-1][coord] for k,(v,z,ti) in enumerate(labels) if v[i-1]*moments[k][power-1][coord]})
                if power==2:indicator_rows.append((len(rows),i-1,coord))
                rows.append(row);rhs.append(Q(0))
    for obj in range(1,8):
        powers=[[1]+[0]*7]
        for order in range(1,height+1):powers.append([sum(powers[-1][i]*R[i][obj][j] for i in range(8)) for j in range(8)])
        for order in range(3,height+1):
            rs=[int(r) for r in s.divisors(order) if r<order];rotation=a['rotations'](order,rs)
            start=nvars;nvars+=len(rotation)
            rows.append({start+k:Q(1) for k in range(len(rotation))});rhs.append(Q(powers[order][0]))
            for at,r in enumerate(rs):
                for coord in range(width):
                    row={}
                    for k,(g,c,z) in enumerate(lows):
                        value=-sum(powers[r][i]*c[i] for i in range(8))*z[coord]
                        if value:row[k]=value
                    for k,(v,z,ti) in enumerate(labels):
                        value=-sum(powers[r][i]*v[i-1] for i in range(1,8))*moments[k][order//r-1][coord]
                        if value:row[offset+k]=value
                    for k,tt in enumerate(rotation):
                        value=mul(D,tt[at])[coord]
                        if value:row[start+k]=value
                    rows.append(row);rhs.append(Q(powers[r][0] if coord==0 else 0))
    indicator_at={at:(obj,coord) for at,obj,coord in indicator_rows};scaled=[]
    for i,row in enumerate(rows):
        constant=Q(D[indicator_at[i][1]]) if i in indicator_at else Q(rhs[i])
        den=math.lcm(constant.denominator,*(Q(x).denominator for x in row.values()))
        integer={j:int(x*den) for j,x in row.items()};divisor=math.gcd(int(constant*den),*integer.values()) or 1
        rows[i]={j:x//divisor for j,x in integer.items()};rhs[i]=int(rhs[i]*den)//divisor
        if i in indicator_at:
            obj,coord=indicator_at[i];scaled.append((i,obj,coord,int(constant*den)//divisor))
    metadata={'field':a['field'],'low_column_counts':list(map(len,a['columns'])),'high_columns':len(a['high']),'trace_types':len(types),'order_bound':bound,'rows':len(rows),'variables':nvars}
    return rows,rhs,scaled,metadata

def integers(rows,rhs,indicator_rows,D,indicators):
    out=list(rhs)
    for at,obj,coord,value in indicator_rows:out[at]=int(indicators[obj])*value
    return rows,out

def check(A,b,y,nvars,raise_error=True):
    okay=len(y)==len(b) and all(type(x) is int for x in y)
    if okay:
        values=[0]*nvars
        for row,yi in zip(A,y):
            if yi:
                for j,x in row.items():values[j]+=x*yi
        okay=all(x>=0 for x in values) and sum(x*z for x,z in zip(b,y))<0
    if raise_error:require(okay,'global induction integer Farkas certificate fails')
    return okay

def farkas(A,b,nvars):
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix,csr_matrix,hstack,vstack
    m=len(b);scale=np.array([max(1,abs(bb),max(map(abs,row.values()),default=0)) for row,bb in zip(A,b)],dtype=float)
    rr=[];cc=[];vv=[]
    for i,row in enumerate(A):
        for j,x in row.items():rr.append(i);cc.append(j);vv.append(float(x)/scale[i])
    M=coo_matrix((vv,(rr,cc)),shape=(m,nvars)).tocsr();del rr,cc,vv
    rhs=np.array(b,dtype=float)/scale
    constraints=vstack([hstack([-M.T,M.T]),csr_matrix(np.r_[rhs,-rhs][None,:])],format='csr')
    start=time.monotonic()
    sol=linprog(np.ones(2*m),A_ub=constraints,b_ub=np.r_[np.zeros(nvars),-1.],bounds=(0,None),method='highs',options={'time_limit':90})
    farkas.last_status={'solver_status':int(sol.status),'solver_message':sol.message,'solver_seconds':round(time.monotonic()-start,3),'solver_limit_seconds':90}
    if not sol.success:return None
    ray=(sol.x[:m]-sol.x[m:])/scale;ray/=max(abs(ray))
    for maximum in (100,1000,10000,100000,1000000,10000000):
        zz=[Q(float(x)).limit_denominator(maximum) for x in ray];den=math.lcm(*(z.denominator for z in zz));out=[int(z*den) for z in zz]
        divisor=math.gcd(*out) or 1;out=[z//divisor for z in out]
        if check(A,b,out,nvars,False):return out
    support=np.flatnonzero(abs(ray)>1e-9).tolist();active=np.flatnonzero(abs(M.T@(ray*scale))<1e-6).tolist()
    columns={j:[] for j in active}
    for i in support:
        for j,x in A[i].items():
            if j in columns:columns[j].append((i,x))
    positions={i:j for j,i in enumerate(support)};basis={};equations=[]
    for j in active:
        row=[Q(0)]*len(support)
        for i,x in columns[j]:row[positions[i]]=Q(x)
        reduced=list(row)
        for pivot,other in sorted(basis.items()):
            c=reduced[pivot]
            if c:reduced=[x-c*y for x,y in zip(reduced,other)]
        pivot=next((i for i,x in enumerate(reduced) if x),None)
        if pivot is not None:
            c=reduced[pivot];basis[pivot]=[x/c for x in reduced];equations.append(row)
        if len(equations)>=len(support)-1:break
    equations.append([b[i] for i in support]);C=s.Matrix(equations);target=s.zeros(C.rows,1);target[-1]=-1
    try:solution,parameters=C.gauss_jordan_solve(target)
    except ValueError:return None
    if parameters.rows:return None
    den=math.lcm(*(int(x.q) for x in solution));out=[0]*m
    for i,x in zip(support,solution):out[i]=int(x*den)
    return out if check(A,b,out,nvars,False) else None
farkas.last_status={}

def certificate(R,height=4,progress=None,seeds=()):
    a=setup(R);rows,rhs,ir,metadata=build(R,a,height);print(metadata,flush=True);cases=[];rays=[]
    for seed in seeds:
        if seed.get('kind')!='global_convex_induction' or seed.get('height')!=height or seed.get('metadata')!=metadata:continue
        for case in seed.get('cases',[]):
            y=case['y'];A,b=integers(rows,rhs,ir,a['global_dimension'],case['indicators'])
            if y not in rays and check(A,b,y,metadata['variables'],False):rays.append(y)
    for ep in ht.indicator_choices(R):
        A,b=integers(rows,rhs,ir,a['global_dimension'],ep)
        y=next((ray for ray in rays if sum(x*z for x,z in zip(b,ray))<0),None)
        if y is None:
            y=farkas(A,b,metadata['variables'])
            if y is not None:rays.append(y)
        print('indicators',ep,'separated',y is not None,flush=True)
        if y is None:return None,dict(metadata,completed_indicator_branches=len(cases),feasible_or_unresolved_indicators=list(ep),search_status=farkas.last_status)
        check(A,b,y,metadata['variables']);cases.append({'indicators':list(ep),'y':y,'bTy':sum(x*z for x,z in zip(b,y))})
        if progress:progress({'kind':'global_convex_induction','height':height,'metadata':metadata,'cases':list(cases)})
    return {'kind':'global_convex_induction','height':height,'metadata':metadata,'cases':cases},metadata

def verify_pseudo(R,c):
    require(c['kind']=='global_convex_induction','wrong convex induction kind');a=setup(R);rows,rhs,ir,meta=build(R,a,c['height'])
    require(meta==c['metadata'],'global induction metadata mismatch');eps=ht.indicator_choices(R)
    require([case['indicators'] for case in c['cases']]==list(map(list,eps)),'incomplete indicator branches')
    for ep,case in zip(eps,c['cases']):
        A,b=integers(rows,rhs,ir,a['global_dimension'],ep);check(A,b,case['y'],meta['variables'])
        require(case['bTy']==sum(x*z for x,z in zip(b,case['y'])),'incorrect Farkas value')

def install():
    import rank8_signed_bridge
    rank8_signed_bridge.install()
    import oriented_extension as oe
    if getattr(oe,'_global_convex_installed',False):return
    original=oe.pseudo_check
    def pseudo(R,c):
        if c['kind']=='global_convex_induction':return verify_pseudo(R,c)
        return original(R,c)
    oe.pseudo_check=pseudo;oe._global_convex_installed=True

def verify(R,c):
    require(c['kind']=='global_convex_induction_lift','wrong global general certificate');install()
    import advanced_criteria
    advanced_criteria.verify(R,c['general'])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--ring',required=True);ap.add_argument('--height',type=int,default=4);ap.add_argument('--tag',default='global_convex');args=ap.parse_args()
    row=next(r for r in json.loads((HERE.parent/'pipeline/census_m3.json').read_text()) if r['id']==args.ring)
    dest=HERE/'advanced'/args.tag/(args.ring+'.json');dest.parent.mkdir(parents=True,exist_ok=True);start=time.monotonic()
    out={'id':row['id'],'tensor_sha256':row['tensor_sha256'],'mode':'global_convex','status':'no_conclusion'}
    def save():
        out['seconds']=round(time.monotonic()-start,3);tmp=dest.with_suffix('.json.tmp');tmp.write_text(json.dumps(out,separators=(',',':'))+'\n');tmp.replace(dest)
    def progress(c):out.update(status='partial_indicator_certificate',partial_certificate=c);save()
    seeds=[]
    for path in (HERE/'advanced').glob('global*/'+args.ring+'.json'):
        previous=json.loads(path.read_text())
        if previous.get('tensor_sha256')==row['tensor_sha256']:
            seeds.extend(previous[k] for k in ('pseudo_certificate','partial_certificate') if k in previous)
    try:
        install();pseudo,report=certificate(row['tensor'],args.height,progress,seeds);out['report']=report
        if pseudo:
            out.pop('partial_certificate',None);out.update(status='pseudo_certificate_pending_replay',pseudo_certificate=pseudo);save()
            import character_induction as ci
            general=ci.lift_general(row['tensor'],pseudo,120)
            if general:
                c={'kind':'global_convex_induction_lift','general':general};verify(row['tensor'],c)
                out.update(status='excluded',scope='general',certificate=c)
            else:verify_pseudo(row['tensor'],pseudo);out['status']='pseudo_unitary_only'
        else:out['status']='no_conclusion'
    except MemoryError as exc:out.update(status='resource_bound',memory_limit_mb=int(os.environ.get('RANK8_GLOBAL_MEMORY_MB','0')),error=repr(exc))
    except Exception as exc:out.update(status='error',error=repr(exc),traceback=traceback.format_exc())
    save();print(args.ring,out['status'],out['seconds'],flush=True)
if __name__=='__main__':main()

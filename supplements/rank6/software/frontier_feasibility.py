"""Exact feasible points in a finite necessary relaxation, not fusion categories."""
from balanced_traces import *
from integer_gram import frames,frame_system
from pathlib import Path
import time

def rational_feasible(A,b):
    from scipy.optimize import linprog
    AA=np.array(A,dtype=float);bb=np.array(b,dtype=float);scale=np.maximum(1,np.maximum(np.max(abs(AA),axis=1),abs(bb)))
    sol=linprog(np.ones(AA.shape[1]),A_eq=AA/scale[:,None],b_eq=bb/scale,bounds=(0,None),method='highs')
    if not sol.success:return None
    support=np.flatnonzero(sol.x>1e-8).tolist()
    for den in [1000,1000000,1000000000]:
        x=[Q(float(sol.x[j])).limit_denominator(den) for j in support]
        if all(sum(Q(A[i][j])*z for j,z in zip(support,x))==b[i] for i in range(len(b))):return [[j,z.numerator,z.denominator] for j,z in zip(support,x)]
    C=s.Matrix([[A[i][j] for j in support] for i in range(len(b))]);B=s.Matrix(b)
    try:x,params=C.gauss_jordan_solve(B)
    except ValueError:return None
    if params.rows:return None
    if any(v<0 for v in x):return None
    require(C*x==B,'rational primal solve failed')
    return [[j,int(z.p),int(z.q)] for j,z in zip(support,x) if z]

def certificate(R,height=6,frame_limit=4000):
    data=quadratic_data(R,gram_prune=True)
    if data is None:return None
    for ix,cs in enumerate(data['lows']):
        if low_failure(cs,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du):continue
        L=s.Matrix.hstack(*map(s.Matrix,cs));Qm,cols=high_columns(data,L);ff=frames(Qm,cols,15)
        print('LOW',ix,'FRAMES',len(ff),flush=True)
        if len(ff)>frame_limit:continue
        for ep in indicator_choices(R):
            A,b,meta=system(R,data,L,ep,height)
            for frame in ff:
                AA,bb=frame_system(A,b,meta,frame);x=rational_feasible(AA,bb)
                if x is not None:return {'kind':'feasible_balanced_integer_gram_relaxation','height':height,'q':data['q'],'columns':[list(c) for c in cs],'indicators':list(ep),'frame':list(frame),'primal':x,'equations':len(bb),'variables':len(AA[0]),'center_rank':len(cs)+sum(frame)}
    return None

def verify(R,c):
    require(c['kind']=='feasible_balanced_integer_gram_relaxation','wrong primal kind');data=quadratic_data(R,gram_prune=True);cs=tuple(map(tuple,c['columns']));require(cs in data['lows'],'primal low matrix outside exhaustive list');ep=c['indicators'];require(ep in list(map(list,indicator_choices(R))),'invalid primal indicators');L=s.Matrix.hstack(*map(s.Matrix,cs));Qm,cols=high_columns(data,L);frame=c['frame'];require(len(frame)==len(cols) and all(type(z) is int and z>=0 for z in frame),'bad integer Gram counts')
    require(all(sum(m*v[i]*v[j] for m,(v,z) in zip(frame,cols))==Qm[i,j] for i in range(Qm.rows) for j in range(Qm.cols)),'integer Gram identity fails');A,b,meta=system(R,data,L,ep,c['height']);AA,bb=frame_system(A,b,meta,frame);require((len(bb),len(AA[0]))==(c['equations'],c['variables']),'wrong primal system size');x=[Q(0)]*len(AA[0]);seen=set()
    for j,num,den in c['primal']:
        require(j not in seen and 0<=j<len(x) and den>0 and num>=0,'bad primal entry');seen.add(j);x[j]=Q(num,den)
    require(all(sum(Q(a)*z for a,z in zip(row,x))==rhs for row,rhs in zip(AA,bb)),'exact primal identity fails');require(c['center_rank']==len(cs)+sum(frame),'bad candidate center rank')

if __name__=='__main__':
    import argparse,json
    P=Path(__file__).resolve().parents[1]
    ap=argparse.ArgumentParser(description="Discover or exactly verify the first frontier point.")
    ap.add_argument('ring',nargs='?',default='R6_2_4')
    ap.add_argument('--verify',action='store_true',help='check the stored point without optimization or writes')
    a=ap.parse_args()
    r=next(r for r in json.load(open(P/'data/census.json')) if r['id']==a.ring)
    if a.verify:
        o=json.load(open(P/'data/frontier_feasible.json'))
        require(o['id']==a.ring and o['N']==r['N'],'stored frontier does not match the requested census tensor')
        verify(r['N'],o['certificate']);print('EXACT FRONTIER POINT VERIFIED',a.ring)
    else:
        st=time.monotonic();c=certificate(r['N'])
        if c:
            verify(r['N'],c)
            (P/'data/frontier_feasible.json').write_text(json.dumps({'id':a.ring,'N':r['N'],'certificate':c},separators=(',',':'))+'\n')
            print('EXACT FEASIBLE',a.ring,'rank',c['center_rank'],'seconds',time.monotonic()-st)
        else:print('NO FEASIBLE POINT FOUND')

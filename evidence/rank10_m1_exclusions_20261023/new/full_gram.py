import json,pathlib,math,itertools,sys,time
import numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds,linprog
from scipy.sparse import csc_matrix
from central_filter import records,P,mv
BASE=pathlib.Path(__file__).resolve().parent

def dimok(a,b):
 n=a*a-2*b*b
 if not n:return False
 aa=17408*(a*a+2*b*b)-49152*a*b
 bb=12288*(a*a+2*b*b)-34816*a*b
 return aa%(n*n)==bb%(n*n)==0

def candidates(Q,T,dims):
 inds=[i for i in range(10) if Q[i][i]]
 # most constrained first
 inds.sort(key=lambda i:(sum(bool(Q[i][j]) for j in range(10)),Q[i][i]))
 v=[0]*10;out=[]
 def rec(j,a,b):
  if j==len(inds):
   if not a or not dimok(a,b):return
   w=mv(T,v)
   if any(x<0 for x in w):
    w=[-x for x in w]
   if any(x<0 or x.denominator!=1 for x in w):return
   w=list(map(int,w))
   if any(w[i]*w[k]>Q[i][k] for i in range(10) for k in range(i+1)):return
   out.append(tuple(v));return
  i=inds[j];bound=math.isqrt(Q[i][i])
  for k in inds[:j]:
   if v[k]:bound=min(bound,Q[i][k]//v[k])
  for x in range(bound+1):
   v[i]=x;rec(j+1,a+dims[i][0]*x,b+dims[i][1]*x)
  v[i]=0
 rec(0,0,0)
 return out

def main(q):
 id=f'R10_1_{q}';a=json.load(open(BASE/f'{id}_central.json'));T=[[__import__('fractions').Fraction(x) for x in r] for r in a['T']]
 N=records[id]['fusion_tensor'];ds=records[id]['invariants']['frobenius_perron_dimensions_approx'];dims=[(1,0) if d<2 else ((2,2) if d<5 else (3,2)) for d in ds]
 prior=json.load(open(P/f'work/resolve_rank10_quadratic/{id}_reciprocal.json')); B=a['B'];seen=set();results=[]
 for no,sol in enumerate(a['solutions']):
  V=[prior['column_sets'][h][j] for h,j in enumerate(sol)];Q=[[B[i][j]-sum(v[i]*v[j] for v in V) for j in range(10)] for i in range(10)]
  key=tuple(map(tuple,Q))
  if key in seen:continue
  seen.add(key); start=time.time();C=candidates(Q,T,dims);
  import sympy as sp
  Qi=sp.Matrix(Q).pinv(); kernel=sp.Matrix(Q).nullspace();
  C=[v for v in C if all(sum(x*y for x,y in zip(v,w))==0 for w in kernel) and (sp.Matrix(v).T*Qi*sp.Matrix(v))[0]<=1]
  Cset=set(C);orbits=[];used=set();dual=records[id]['invariants']['dual_indices']
  for v in C:
   if v in used:continue
   orb={v};todo=[v]
   while todo:
    u=todo.pop();w=tuple(int(x) for x in mv(T,u));w=w if all(x>=0 for x in w) else tuple(-x for x in w)
    for z in [w,tuple(u[i] for i in dual)]:
     if z not in Cset:raise ValueError('orbit')
     if z not in orb:orb.add(z);todo.append(z)
   used.update(orb);orbits.append(sorted(orb))
  pos=[(i,j) for i in range(10) for j in range(i+1) if Q[i][j]]
  A=np.array([[sum(v[i]*v[j] for v in orb) for orb in orbits] for i,j in pos],dtype=float)
  target=np.array([Q[i][j] for i,j in pos],dtype=float)
  print(id,no,'columns',len(C),'orbits',len(orbits),'enumerated',time.time()-start,flush=True)
  lp=linprog(np.zeros(len(orbits)),A_eq=A,b_eq=target,bounds=(0,None),method='highs'); print('LP',lp.status,flush=True)
  if lp.status==0:
   res=milp(np.zeros(len(orbits)),integrality=np.ones(len(orbits)),bounds=Bounds(0,np.inf),constraints=LinearConstraint(csc_matrix(A),target,target),options={'time_limit':10})
  else: res=lp
  print('status',res.status,res.message,flush=True)
  d={'solution':no,'columns':len(C),'orbits':len(orbits),'status':int(res.status)}
  if res.x is not None:
   x=np.rint(res.x).astype(int);assert np.array_equal(A@x,target)
   d['witness']=[{'multiplicity':int(k),'orbit':o} for k,o in zip(x,orbits) if k]
  results.append(d)
  (BASE/f'{id}_fullgram.json').write_text(json.dumps(results,indent=2))
if __name__=='__main__':main(int(sys.argv[1]))

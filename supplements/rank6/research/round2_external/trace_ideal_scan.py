import json,sys,math
import sympy as s
sys.path.insert(0,'software')
from rings import Characters,dual
from new_ramified_signed import magnitude_branches
rows=json.load(open('verification/round2/campaign_manifest.json'))['inputs'];t=s.Symbol('t')
for r in rows:
 N=r['N']
 if dual(N)!=list(range(6)):continue
 C=sum((s.Matrix(M)**2 for M in N),s.zeros(6));fac=C.charpoly(t).as_poly().factor_list()[1];steps=[]
 for f,m in fac:
  if f.degree()==1:steps.append(int(-f.TC()));continue
  if f.degree()!=2:
   from sympy.polys.numberfields import round_two
   try:ZK,discK=round_two(f)
   except Exception as e: print(r['id'],'SKIP maximalorder',str(f),type(e).__name__,flush=True);continue
   M=ZK.matrix.to_Matrix();d=f.degree();H=s.zeros(d)
   for j in range(d-1):H[j+1,j]=1
   for i in range(d):H[i,d-1]=-f.nth(i)
   tt=[s.trace(H**(i+1)) for i in range(d)]
   vals=[sum(M[i,j]*tt[i] for i in range(d))/ZK.denom for j in range(d)]
   if any(v.q!=1 for v in vals):raise ValueError(vals)
   steps.append(math.gcd(*map(int,vals)));continue
  A=-int(f.all_coeffs()[1]);B=int(f.TC());disc=A*A-4*B
  q=math.prod(int(p) for p,e in s.factorint(disc).items() if e%2);b=math.isqrt(disc//q)
  step=math.gcd(A,(A+b*q)//2) if q%4==1 else math.gcd(A,b*q)
  steps.append(step)
 L=math.lcm(*steps) if steps else 1;T=int(s.trace(C));budget=T-L
 if budget<0:print(r['id'],'EXCLUDED',steps,'trace',T,'step',L,flush=True)
 elif budget<50:
  p,mag=magnitude_branches(N,{'deficit_budget':budget});print(r['id'],'BRANCHES',steps,'trace',T,'step',L,'budget',budget,'count',len(mag),flush=True)

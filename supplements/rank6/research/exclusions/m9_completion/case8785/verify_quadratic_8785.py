"""Complete necessary spectra for R8785 conditional on signed dimension field Q(sqrt5).
Only exact arithmetic. Portable tensor input; checks remain active under python -O.
"""
import hashlib,itertools,json,math,sys,time
from pathlib import Path
from fractions import Fraction
from collections import defaultdict
import sympy as s

def need(condition,message):
 if not condition:raise ValueError(message)

def run(path=None):
 st=time.monotonic();path=Path(path) if path else Path(__file__).with_name('tensor_8785.json')
 R=next(r['N'] for r in json.load(open(path)) if r['id']=='R6_9_8785')
 digest=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
 need(digest=='7897af45c48cb1d416710f37ea9c4c11226490421317d193c85e3cc5022b3da8','tensor')
 M=list(map(s.Matrix,R));C=sum((N*N for N in M),s.zeros(6));x=s.symbols('x')
 need(C.charpoly(x).as_expr().expand()==((x*x-4225*x+21125)*(x*x-50*x+125)**2).expand(),'codegrees')
 T=int(s.trace(C));need(T==4325,'trace')
 # All entries of the Frobenius map are exact modulo2.
 F=s.Matrix(6,6,lambda i,j:R[j][j][i]%2)
 need(all(v%2==0 for v in F**2-s.eye(6)),'Frobenius²')
 A=[[int(v)%2 for v in row] for row in (F-s.eye(6)).tolist()];rank=0
 for j in range(6):
  k=next((k for k in range(rank,6) if A[k][j]),None)
  if k is None:continue
  A[rank],A[k]=A[k],A[rank]
  for i in range(6):
   if i!=rank and A[i][j]:A[i]=[(u+v)%2 for u,v in zip(A[i],A[rank])]
  rank+=1
 need(rank==3,'mod2 algebra F4³')
 # Each root is represented by (a,b,n,p,q): (a+b√5)/2=p+qφ, norm n.
 universe=[]
 for a in range(2,T+1):
  for b in range(a%2,math.isqrt((a-2)**2//5)+1,2):
   n=(a*a-5*b*b)//4
   if n<=0 or a*a%n or not n%2:continue
   universe.append((a,b,n,(a-b)//2,b))
 def divides(f,d):
  a,b,n,p,q=f;A,B,N,u,v=d
  return (u*(p+q)-v*q)%n==0 and (v*p-u*q)%n==0
 D=(4225,1885,21125,1170,1885)
 # D=65√5*(29+13√5)/2; the last factor has norm−1.
 need(29*29-5*13*13==-4,'FP ideal unit')
 deltas=[d for d in universe if divides(D,d)];spectra=[]
 for d in deltas:
  if d[0]+4>T:continue
  candidates=[f for f in universe if f[0]+d[0]+2<=T and divides(f,d)]
  buckets=defaultdict(list)
  for f in candidates:buckets[Fraction(f[0],f[2])].append(f)
  target=1-Fraction(d[0],d[2])
  for f in candidates:
   for g in buckets.get(target-Fraction(f[0],f[2]),[]):
    if g<f or d[0]+f[0]+g[0]>T or (d[0]+f[0]+g[0]-T)%4:continue
    # Odd norms force each pair mod2 to be x²+x+1 or (x+1)².
    if sum(v[0]%2 for v in (d,f,g))!=1:continue
    spectra.append({'Delta':d[:3],'other_pairs':[f[:3],g[:3]],'trace':d[0]+f[0]+g[0],'deficit':T-d[0]-f[0]-g[0]})
 expected=[{'Delta':(1625,325,528125),'other_pairs':[(450,200,625),(1170,520,4225)],'trace':3245,'deficit':1080}]
 for pair,tr in [([(10,0,25),(10,0,25)],4245),([(10,0,25),(50,20,125)],4285),([(50,20,125),(50,20,125)],4325)]:
  expected.append({'Delta':D[:3],'other_pairs':pair,'trace':tr,'deficit':T-tr})
 need(spectra==expected,'complete spectrum inventory')
 need(len(universe)==3001 and len(deltas)==18,'domain inventory')
 return {'id':'R6_9_8785','tensor_sha256':digest,'scope':'general categorical necessary spectra conditional on K=Q(sqrt5)','complete':True,'universe_count':len(universe),'delta_count':len(deltas),'spectra':spectra,'seconds':time.monotonic()-st}
if __name__=='__main__':print(json.dumps(run(sys.argv[1] if len(sys.argv)>1 else None),indent=2))

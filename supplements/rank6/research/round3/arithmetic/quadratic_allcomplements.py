import sys,json,math,itertools,time
from pathlib import Path
from fractions import Fraction as F
import sympy as s
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'software'))
from round3_arithmetic import reciprocal_tuples
q=41;c=18;T=7416;out=[];start=time.monotonic();counts=[0,0,0]
def integraldiv(A,B,S,r,P):
 for rr in [r,-r]:
  a=F(A*S-q*B*rr,4*P);b=F(B*S-A*rr,4*P)
  if (a-b).denominator!=1 or (2*b).denominator!=1:return False
 return True
for y in range(1,11):
 for x in range(-math.isqrt(q*y*y-1),math.isqrt(q*y*y-1)+1):
  if (x-y)%2:continue
  n=q*y*y-x*x
  if (4*q*y*y)%n:continue
  A=c*q*y;B=c*x;N=c*c*q*n//4;content=math.gcd((A-B)//2,B)
  if content%9:continue
  target=1-F(4*y,c*n)
  if target<=0:continue
  ds=[int(d) for d in s.divisors(abs(content)) if d>1]
  pairs=[]
  for P in map(int,s.divisors(N)):
   for r in range(1,math.isqrt(max(0,((T-A-3)**2-4*P)//q))+1):
    S=math.isqrt(4*P+q*r*r)
    if S*S!=4*P+q*r*r or S<=2 or P-S+1<=0 or S*S%P:continue
    if not integraldiv(A,B,S,r,P):continue
    pairs.append((S,P,r))
  counts[0]+=1;counts[1]+=len(pairs)
  records=[]
  for fs in reciprocal_tuples(ds,4,target,T-A):records.append({'rational':fs,'quadratic':[],'trace':A+sum(fs)})
  for S,P,r in pairs:
   for fs in reciprocal_tuples(ds,2,target-F(S,P),T-A-S):records.append({'rational':fs,'quadratic':[[S,P,r]],'trace':A+sum(fs)+S})
  for (S,P,r),(S2,P2,r2) in itertools.combinations_with_replacement(pairs,2):
   if A+S+S2>T or F(S,P)+F(S2,P2)!=target:continue
   records.append({'rational':[],'quadratic':[[S,P,r],[S2,P2,r2]],'trace':A+S+S2})
  if records:
   out.append({'y':y,'x':x,'records':records});counts[2]+=len(records);print(y,x,records,flush=True)
print('counts',counts,'seconds',time.monotonic()-start,flush=True)
Path('research/round3/arithmetic/quadratic41_allcomplement_exploration.json').write_text(json.dumps({'counts':counts,'survivors':out},indent=2)+'\n')

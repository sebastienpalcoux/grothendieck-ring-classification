"""Independent rational-arithmetic verification of the rank-38 obstruction.

No SymPy, FLINT, optimizer, approximate arithmetic or assert statement is used.
Cyclotomic coefficients are reduced modulo Phi_15 in ascending order.
"""
from fractions import Fraction as F
from pathlib import Path
import json

def require(condition,message):
 if not condition:raise ValueError(message)

PHI=[1,-1,0,1,-1,1,0,-1,1]
ZERO=(F(0),)*8
ONE=(F(1),)+(F(0),)*7
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,b):
 c=[F(0)]*15
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 for i in range(14,7,-1):
  for j in range(8):c[i-8+j]-=c[i]*PHI[j]
 return tuple(c[:8])
def inv(a):
 columns=[]
 for j in range(8):columns.append(mul(a,tuple(F(i==j) for i in range(8))))
 M=[[columns[j][i] for j in range(8)]+[F(i==0)] for i in range(8)]
 for j in range(8):
  p=next((i for i in range(j,8) if M[i][j]),None);require(p is not None,'zero divisor in quotient')
  M[j],M[p]=M[p],M[j];q=M[j][j];M[j]=[x/q for x in M[j]]
  for i in range(8):
   if i!=j:
    q=M[i][j];M[i]=[x-q*y for x,y in zip(M[i],M[j])]
 ans=tuple(M[i][-1] for i in range(8));require(mul(a,ans)==ONE,'invalid inverse');return ans
def decode(v):return tuple(map(F,reversed(v)))+(F(0),)*(8-len(v))

here=Path(__file__).parent
branch=next(x for x in json.load(open(here/'modular_closure.json')) if x['rank']==38)
rows={tuple(x['indices']):[decode(v) for v in x['S_image']] for x in branch['known_class_rows']}
value=ZERO
for s0,s1,s6 in zip(rows[(0,)],rows[(1,)],rows[(6,)]):
 value=add(value,mul(mul(mul(s1,s1),s6),inv(s0)))
require(value==(F(1,3),)+(F(0),)*7,'independent coefficient differs from one third')
record={'passed':True,'rank':38,'objects':[1,1,6],'coefficient_ascending':list(map(str,value)),'arithmetic':'fractions.Fraction modulo Phi_15','optimizer_used':False}
(here/'independent_fraction.json').write_text(json.dumps(record,indent=2));print(record)

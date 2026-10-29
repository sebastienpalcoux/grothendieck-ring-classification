"""Finite arithmetic supporting MORITA_RING_RIGIDITY.md; no categorical claim by computation."""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
from math import isqrt
import hashlib,json,runpy
HERE=Path(__file__).resolve().parent
PRIOR=HERE.parents[1]/'prior'

def require(c,msg):
 if not c:raise ValueError(msg)
def mm(A,B):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*B)]for row in A]
def tr(A):return [list(x)for x in zip(*A)]
def lin(cs,Ms):return [[sum(c*M[i][j] for c,M in zip(cs,Ms))for j in range(6)]for i in range(6)]
def mat(a,b,c,e,u,v):return [[a,b,c,e,u,v],[b,a,e,c,u,v],[c,e,a,b,v,u],[e,c,b,a,v,u],[v,v,u,u,a+b,c+e],[u,u,v,v,c+e,a+b]]
P=[mat(*(int(i==j)for i in range(6)))for j in range(4)]
Q=mat(0,0,0,0,1,0);Qt=tr(Q)
X=mat(1,1,1,1,1,2);Y=tr(X)
require(mm(Q,Qt)==lin([1,1],P[:2]),'Q Q*')
require(mm(Q,Q)==lin([1,1],P[2:]),'Q²')
require(mm(X,Y)==lin([1,1,4,4],[P[0],P[1],X,Y]),'XY')
require(mm(X,X)==lin([1,1,4,4],[P[2],P[3],X,Y]),'XX')
require(mm(P[1],X)==X and mm(P[2],X)==Y,'pointed large action')
for i in range(4):
 for j in range(4):require(mm(P[i],P[j])==P[i^j],'V4')

# Full rational commutant dimension, without assuming its displayed pattern.
eqs=[]
for A in P+[X]:
 for i in range(6):
  for j in range(6):
   r=[F(0)]*36
   for k in range(6):r[k*6+j]+=A[i][k];r[i*6+k]-=A[k][j]
   eqs.append(r)
r=0
for c in range(36):
 k=next((k for k in range(r,len(eqs))if eqs[k][c]),None)
 if k is None:continue
 eqs[k],eqs[r]=eqs[r],eqs[k]
 t=eqs[r][c];eqs[r]=[x/t for x in eqs[r]]
 for k in range(r+1,len(eqs)):
  if eqs[k][c]:
   t=eqs[k][c];eqs[k]=[x-t*y for x,y in zip(eqs[k],eqs[r])]
 r+=1
require(r==30,'commutant dimension six')
for B in P+[Q,Qt]:
 for A in P+[X]:require(mm(A,B)==mm(B,A),'six spanning matrices commute')
# Each generator has its own entry among row zero, so they are independent,
# and nonnegativity of any commutant matrix forces all six parameters >=0.
require([B[0]for B in P+[Q,Qt]]==[[int(i==j)for i in range(6)]for j in range(6)],'parameter extraction')

# Algebraic integer Gram tests, enumerating all residual multisets where used.
def gram_multisets(q,dot,divisor):
 pairs=[(a,b) for a in range(isqrt(q)+1)for b in range(isqrt(q)+1)
        if a+b and (a+b)%divisor==0 and a*b<=dot]
 out=[]
 def rec(start,aa,bb,ab,parts):
  if aa==bb==ab==0:out.append(parts);return
  for i in range(start,len(pairs)):
   a,b=pairs[i]
   if a*a<=aa and b*b<=bb and a*b<=ab:rec(i,aa-a*a,bb-b*b,ab-a*b,parts+[(a,b)])
 rec(0,q,q,dot,[]);return out
require(gram_multisets(8,6,7)==[],'B1,B3 integrality excludes')
require(gram_multisets(10,8,3)==[[(1,2),(1,2),(2,1),(2,1)]],'B2 residual module list')
require(gram_multisets(2,0,1)==[[(0,1),(0,1),(1,0),(1,0)]],'B4 residual module list')
require(gram_multisets(1,0,1)==[[(0,1),(1,0)]],'A2 residual list')

# Exact arithmetic in Q(sqrt2).
def add(x,y):return(x[0]+y[0],x[1]+y[1])
def mul(x,y):return(x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def div(x,y):
 n=y[0]*y[0]-2*y[1]*y[1];z=mul(x,(y[0],-y[1]));return(F(z[0],n),F(z[1],n))
d=(4,3);d2=mul(d,d);require(d2==(34,24),'dimension square')
require(div(d2,(10,6))==(F(13,7),F(9,7)),'B1 internal end')
require(div(d2,(26,18))==(F(5,7),F(3,7)),'B3 internal end')
require(div(d2,(18,12))==(1,F(2,3)),'B2 internal end')
require(div(d2,(34,24))==(1,0),'B4 internal end')
require(div(d2,(17,12))==(2,0),'A2 internal end')
v=[(1,0)]*4+[(0,1)]*2
for i in range(6):
 for j in range(6):
  actual=add((sum(M[i][j]for M in P),0),mul(d,(X[i][j]+Y[i][j],0)))
  expected=mul((9,6),mul(v[i],v[j]))
  require(actual==expected,'regular-object matrix')
require((36-4)*18==24**2,'Cauchy equality')
require((24,18)==(6*4,6*3),'Cauchy ratio4:3')
require([u for u in range(4)if u*(3-u)==2]==[1,2],'only viable dual coefficients')

# Bind to published source tensor and check the resulting rules up to labels.
T=runpy.run_path(str(PRIOR/'data/current_remaining_cases.py'))['TENSORS']['R6_4_155']
sha=hashlib.sha256(json.dumps(T,separators=(',',':')).encode()).hexdigest()
require(sha=='012ef716d19b96a2a800d7bcbb33f3ae5e99e3c6a223f6e14bcd20144d4072a3','source tensor hash')
N=[[[0]*6 for _ in range(6)]for _ in range(6)]
for i in range(4):
 for j in range(4):N[i][j][i^j]=1
 for j in (4,5):N[i][j][j^int(i>=2)]=1;N[j][i][j^int(i>=2)]=1
for i in (4,5):
 for j in (4,5):
  inv=(0,1)if i!=j else(2,3)
  for k in inv:N[i][j][k]=1
  N[i][j][4]=N[i][j][5]=4
iso=None
for tail in permutations(range(1,6)):
 p=(0,)+tail
 if all(N[i][j][k]==T[p[i]][p[j]][p[k]]for i in range(6)for j in range(6)for k in range(6)):
  iso=list(p);break
require(iso is not None,'dual fusion ring identifies with source')
receipt={'source_sha256':sha,'commutant_dimension':6,'surviving_connected_algebra_parameters':{'A_k':[0,1,2],'B_k':[0,2,4]},'A1_dual_simple_dimensions':{'invertible':4,'4+3sqrt2':2},'dual_tensor_to_census_permutation':iso,'scope':'Finite arithmetic supporting a conditional Morita based-ring rigidity theorem. No model or exclusion.'}
(HERE/'morita_ring_rigidity_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: complete algebra Gram reduction, commutant, Cauchy identity and exact R155 dual tensor')

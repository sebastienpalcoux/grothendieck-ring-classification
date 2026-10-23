"""Independent standard-library replay in the 11^3-dimensional tensor algebra.
No NumPy/SciPy/matrix products, numerical eigenvalues, or producer imports.
"""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction
import sys,json,itertools,time
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent));from common import read,sha,require

def rank_solve(A,b):
 A=[[Fraction(x)for x in row]+[Fraction(y)]for row,y in zip(A,b)];n=len(A)
 for i in range(n):
  p=next(j for j in range(i,n)if A[j][i]);A[i],A[p]=A[p],A[i];t=A[i][i];A[i]=[x/t for x in A[i]]
  for j in range(n):
   if j!=i:
    t=A[j][i];A[j]=[a-t*b for a,b in zip(A[j],A[i])]
 return [row[-1]for row in A]

def verify(rid):
 R=read()[rid];n=len(R);du=[next(j for j in range(n)if R[i][j][0])for i in range(n)]
 d=[1 if sum(R[i][du[i]])==1 else 2 for i in range(n)]
 require(all(sum(R[i][j][k]*d[k]for k in range(n))==d[i]*d[j]for i,j in itertools.product(range(n),repeat=2)),'positive dimensions')
 require(sum(a*a for a in d)==32,'global dimension')
 require(all(R[du[i]][j][k]==R[i][k][j]for i,j,k in itertools.product(range(n),repeat=3)),'regular star transpose')
 require(all(d[du[i]]==d[i]and 2%d[i]==0 for i in range(n)),'selfadjoint q coefficients')
 prod=[[[(k,a)for k,a in enumerate(R[i][j])if a]for j in range(n)]for i in range(n)]
 q={(i,i,i):2//d[i]for i in range(n)}
 def multiply_by_q(v):
  w=defaultdict(int)
  for (a,b,c),v0 in v.items():
   for i in range(n):
    w0=v0*(2//d[i])
    for (j,r),(k,s),(l,t)in itertools.product(prod[a][i],prod[b][i],prod[c][i]):w[j,k,l]+=w0*r*s*t
  return {k:v for k,v in w.items()if v}
 # Polynomial is evaluated directly inside R tensor R tensor R.
 value=q.copy();steps=[]
 for root in (8,16,64):
  nxt=defaultdict(int,multiply_by_q(value))
  for k,v in value.items():nxt[k]-=root*v
  value={k:v for k,v in nxt.items()if v};steps.append(len(value))
 require(not value,'q(q-8)(q-16)(q-64)=0 in exact tensor algebra')
 # Independent exact multiplicities from three regular traces and dimension.
 tr=[sum(R[i][j][j]for j in range(n))for i in range(n)]
 traces=[n**3];power=q
 for k in range(1,4):
  traces.append(sum(v*tr[a]*tr[b]*tr[c]for(a,b,c),v in power.items()))
  if k<3:power=multiply_by_q(power)
 roots=[0,8,16,64];mults=rank_solve([[a**k for a in roots]for k in range(4)],traces)
 require(all(a.denominator==1 and a>=0 for a in mults),'nonnegative integral multiplicities')
 return {'id':rid,'tensor_sha256':sha(R),'passed':True,'dimensions':d,'polynomial_roots':roots,'successive_tensor_support_sizes':steps,'regular_traces':traces,'spectrum':[{'eigenvalue':a,'multiplicity':int(b)}for a,b in zip(roots,mults)],'conclusions':['full primary-3 positive semidefinite','all primary-n criteria pass by HLPW Theorem3.9','Schur-product criterion passes by HLPW Proposition3.13'],'categorification_claim':False}
if __name__=='__main__':
 t=time.monotonic();rows=[verify(rid)for rid in ['R11_1_104','R11_1_153']];(HERE/'primary3_independent.json').write_text(json.dumps({'records':rows,'seconds':time.monotonic()-t},indent=2)+'\n');print('PASS: exact tensor-algebra annihilators and primary/Schur positivity for both inputs')

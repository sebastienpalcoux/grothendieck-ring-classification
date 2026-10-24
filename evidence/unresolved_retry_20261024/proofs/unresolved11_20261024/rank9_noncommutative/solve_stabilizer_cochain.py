from cohomology_probe import G,e,mul,omega
from itertools import product
import numpy as np,json,time
from pathlib import Path
P=Path(__file__).resolve().parent
L=list(product(G,range(2)));I={a:i for i,a in enumerate(L)};N=len(L)
def lm(a,b):return mul(a[0],b[0],1),a[1]^b[1]
def p2(a):g,k=a;return (g[0]^k,g[1]^k,g[2])
W=[[[ (omega(a[0],b[0],c[0],0)-omega(p2(a),p2(b),p2(c),0))%4 for c in L]for b in L]for a in L]
V=list(product(range(1,N),repeat=2));J={x:i for i,x in enumerate(V)}
rows=[];rhs=[]
for i,j,k in product(range(1,N),repeat=3):
 r=[0]*len(V)
 for pair,coef in [((j,k),1),((I[lm(L[i],L[j])],k),-1),((i,I[lm(L[j],L[k])]),1),((i,j),-1)]:
  if pair in J:r[J[pair]]+=coef
 rows.append(r);rhs.append(W[i][j][k])
A0=np.array(rows,dtype=np.int64);b0=np.array(rhs,dtype=np.int64)
def solve(A,b,mod):
 A=A.copy()%mod;b=b.copy()%mod;m,n=A.shape;piv=[];r=0
 while r<min(m,n):
  candidates=np.argwhere(A[r:,:]%2)
  if len(candidates)==0:break
  rr,c=map(int,candidates[0]);rr+=r
  A[[r,rr]]=A[[rr,r]];b[[r,rr]]=b[[rr,r]]
  inv=pow(int(A[r,c]),-1,mod);A[r]=A[r]*inv%mod;b[r]=b[r]*inv%mod
  coeff=A[:,c].copy();coeff[r]=0
  A=(A-coeff[:,None]*A[r])%mod;b=(b-coeff*b[r])%mod
  piv.append(c);r+=1
 free=[i for i in range(n)if i not in piv]
 x=np.zeros(n,dtype=np.int64)
 if r<m:
  if any(b[r:]%2):return None
  if mod>2 and free:
   tail=solve(A[r:,free]//2,b[r:]//2,mod//2)
   if tail is None:return None
   x[free]=tail
  elif any(b[r:]%mod):return None
 for i,c in reversed(list(enumerate(piv))):x[c]=(b[i]-sum(A[i,j]*x[j]for j in free))%mod
 return x
for mod in (4,8,16,64):
 t=time.time();b=b0*(mod//4);x=solve(A0,b,mod);print('mod',mod,'satisfiable',x is not None,'seconds',time.time()-t,flush=True)
 if x is not None:
  assert np.all((A0@x-b)%mod==0)
  vals=[[int(x[J[i,j]])if(i,j)in J else 0 for j in range(N)]for i in range(N)]
  (P/'full_stabilizer_cochain.json').write_text(json.dumps({'modulus':mod,'group':L,'cochain':vals,'w':W,'scope':'Full identity-quotient D8 bimodule stabilizer obstruction vanishes for explicit Kac-Paljutkin associator; this supplies no fusion-category model.'},indent=2)+'\n');break

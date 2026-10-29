"""Exact generalized cubic rotations in all 26^3 blocks of B.
Cyclotomic coefficients are ascending; common matrix denominator is24.
"""
from pathlib import Path
from fractions import Fraction
import json,time,hashlib
import numpy as np
P=Path(__file__).resolve().parents[2]
src=P/'prior/supplements/rank6/research/frontier/new_research/r155_modular/reconstruction.json'
J=json.load(open(src));N=np.array(J['fusion_rules'],dtype=np.int64);r=26
t=np.array([12,0,0,12,21,0,12,21,4,16,8,20,5,5,13,13,6,6,18,18,9,9,12,0,18,0])
dual=J['duality'];S=np.zeros((8,r,r),dtype=np.int64)
for i,row in enumerate(J['normalized_S']):
 for j,v in enumerate(row):
  for k,q in enumerate(reversed(v)):
   q=24*Fraction(q);assert q.denominator==1;S[k,i,j]=int(q)
def roots(L,degree):
 out=[]
 for e in range(L):
  a=[0]*(e+degree+1);a[e]=1
  for k in range(len(a)-1,degree-1,-1):
   v=a[k];a[k-degree//2]+=v;a[k-degree]-=v;a[k]=0
  out.append(a[:degree])
 return np.array(out,dtype=np.int64)
R24=roots(24,8);R72=roots(72,24)
def shift_cols(A,ee):
 out=np.zeros_like(A)
 for a in range(r):
  for k in range(8):out[:,:,a]+=R24[(k+int(ee[a]))%24,:,None]*A[k,:,a][None,:]
 return out
def trace(m):
 L=shift_cols(S,m*t);R=shift_cols(S[:,dual,:],-m*t)
 out=np.zeros((r,r,r,8),dtype=np.int64)
 for p in range(8):
  for q in range(8):
   val=np.einsum('ia,abk,jb->kij',L[p],N,R[q],optimize=True)
   out+=val[:,:,:,None]*R24[(p+q)%24]
 return out
start=time.time();G=trace(1)
for k in range(r):
 for i in range(r):
  for j in range(r):assert np.array_equal(G[k,i,j],576*N[i,j,k]*R24[(int(t[j])-int(t[i]))%24])
G=trace(3);fail=[];norm=[]
for k in range(r):
 power=np.einsum('x,xr->r',N[k,k],N[:,k,:]);H=np.einsum('ijx,x->ij',N,power)
 for i in range(r):
  for j in range(r):
   tr=np.zeros(24,dtype=np.int64)
   for p in range(8):tr+=G[k,i,j,p]*R72[(3*p+int(t[i])-int(t[j]))%72]
   ok=all(v==0 for p,v in enumerate(tr) if p not in (0,12))
   a=int(tr[0]+tr[12]);b=int(tr[12]);h=int(H[i,j])
   # a,b are still over denominator576.
   mult=[576*h+2*a-b,576*h-a+2*b,576*h-a-b]
   ok=ok and all(m>=0 and m%(576*3)==0 for m in mult)
   if not ok:fail.append({'base':k,'target':[i,j],'hom_dim':h,'trace_coefficients_over576':tr.tolist(),'scaled_multiplicities':mult})
   else:norm.append([k,i,j,h]+[m//1728 for m in mult])
receipt={'scope':'necessary generalized cubic rotation spectra for all26 simples and676 central targets','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'blocks':len(norm)+len(fail),'degree1_checks':26**3,'failures':fail,'elapsed_seconds':time.time()-start,'rows':norm}
(Path(__file__).parent/'r155_cubic_receipt.json').write_text(json.dumps(receipt,separators=(',',':'))+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='rows'},indent=2))

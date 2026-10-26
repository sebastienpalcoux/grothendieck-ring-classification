"""Short exact completion of the small mod-four sign kernels."""
from signed_mod4 import *
import numpy as np

def gauge_solution(R,orbits,x):
 n=len(R);du=common.dual(R);piv={};seen=set()
 for i in range(1,n):
  if i in seen:continue
  J={i,du[i]};seen.update(J);row=0
  for v,orb in enumerate(orbits):
   if sum(j in J for j in orb[0])%2:row|=1<<v
  eps=sum(1<<j for j in J)
  while row:
   j=row.bit_length()-1
   if j in piv:row^=piv[j][0];eps^=piv[j][1]
   else:piv[j]=(row,eps);break
 eps=0
 while x:
  j=x.bit_length()-1
  if j not in piv:return None
  x^=piv[j][0];eps^=piv[j][1]
 return [-1 if eps>>j&1 else 1 for j in range(n)]

def enumerate_kernel(R,normalize=True):
 q,(orbits,mapping,eqs,piv,basis)=system(R,normalize);n=len(R);rows=[];rejected=0
 common.require(len(basis)<=12,'short-kernel bound')
 for values in itertools.product((0,1),repeat=len(basis)):
  x=0
  for v,b in zip(values,basis):
   if v:x^=b
  T=np.array(R,dtype=np.int64)
  for (i,j,k),v in mapping.items():
   if x>>v&1:T[i,j,k]=-T[i,j,k]
  bad=None
  for i,j in itertools.product(range(n),repeat=2):
   if not np.array_equal(T[i]@T[j],np.tensordot(T[j,i,:],T,axes=1)):
    bad=[i,j];break
  if bad:rejected+=1;continue
  gauge=gauge_solution(R,orbits,x)
  if gauge is not None:
   common.require(all(int(T[i,j,k])==R[i][j][k]*gauge[i]*gauge[j]*gauge[k]for i,j,k in itertools.product(range(n),repeat=3)),'full gauge equality')
  rows.append(dict(sign_vector=hex(x),basis_gauge=gauge,tensor=T.tolist()))
 return dict(summary=q,linear_boxes=2**len(basis),associativity_rejections=rejected,associative_count=len(rows),all_gauge_original=all(r['basis_gauge']is not None for r in rows),tables=rows)

if __name__=='__main__':
 data=json.loads((BASE/'tensors.json').read_text());out=[]
 for i in (63,64,215,365,332,350,561,623,628):
  start=time.monotonic();r=enumerate_kernel(data[f'R12_1_{i}']);r.update(id=f'R12_1_{i}',seconds=time.monotonic()-start);out.append(r);print({k:v for k,v in r.items()if k not in ('summary','tables')},flush=True)
 (Path(__file__).resolve().parent/'signed_enumeration.json').write_text(json.dumps(out,indent=2)+'\n')

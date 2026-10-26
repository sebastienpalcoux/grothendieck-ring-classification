"""Additional short localized primary-five/six tests; no negative => unknown."""
from pathlib import Path
from fractions import Fraction as Q
import itertools,json,math,time
import numpy as np
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[2]/'rank12-m1-offline-20261025'

def main():
 start=time.monotonic();D=json.loads((BASE/'tensors.json').read_text());fam=json.loads((BASE/'unresolved_families.json').read_text())['records'];P={r['id']:r for r in json.loads((BASE/'profile.json').read_text())['records']};rows=[]
 for rid in [r['id']for r in fam if r['family']=='D32']:
  N=np.array(D[rid],dtype=np.int64);sq=P[rid]['squared_dimensions'];cert=None;minimum=0.;checks=0
  for degree,size in [(5,2),(6,2)]:
   for U in itertools.combinations(range(12),size):
    A=N[:,U,:][:,:,U];K=A.copy();dim=size
    for _ in range(degree-1):K=np.einsum('iab,icd->iacbd',K,A).reshape(12,dim*size,dim*size);dim*=size
    B=np.einsum('iab,i->ab',K,np.array(sq,dtype=float)**(-(degree-2)/2));w,V=np.linalg.eigh(B);checks+=1;minimum=min(minimum,float(w[0]))
    if w[0]>=-1e-7:continue
    v=np.rint(V[:,0]*10000).astype(np.int64);cs=[int(v@a@v)for a in K]
    if degree%2==0:value=sum(Q(c,q**((degree-2)//2))for c,q in zip(cs,sq))
    else:
     value=Q(0);scale=10**9
     for c,q in zip(cs,sq):
      a=math.isqrt(q*scale*scale);b=a if a*a==q*scale*scale else a+1
      value+=Q(c*(b if c>=0 else a),scale*q**((degree-1)//2))
    if value<0:cert=dict(degree=degree,subset=list(U),vector=v.tolist(),coefficients=cs,exact_quadratic_upper_bound=str(value),squared_dimensions=sq);break
   if cert:break
  rows.append(dict(id=rid,certificate=cert,subsets_checked=checks,minimum_numerical_eigenvalue=minimum));print(rid,'EXCLUDED'if cert else'no witness',minimum,flush=True)
 (HERE/'higher_primary.json').write_text(json.dumps(dict(records=rows,seconds=time.monotonic()-start),indent=2)+'\n')
if __name__=='__main__':main()

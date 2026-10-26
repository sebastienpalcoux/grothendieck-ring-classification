"""Short localized primary-four scan. Only exact negative forms assign status."""
from pathlib import Path
from fractions import Fraction
import itertools,json,time
import numpy as np
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[2]/'rank12-m1-offline-20261025'

def main():
 start=time.monotonic();data=json.loads((BASE/'tensors.json').read_text());fam=json.loads((BASE/'unresolved_families.json').read_text())['records'];P={r['id']:r for r in json.loads((BASE/'profile.json').read_text())['records']}
 ids=[r['id']for r in fam if r['family']=='D32']+['R12_1_28','R12_1_183','R12_1_405','R12_1_522'];out=[]
 for rid in ids:
  N=np.array(data[rid],dtype=np.int64);sq=P[rid]['squared_dimensions'];cert=None;smallest=0.;tested=0
  for size in [2,3]:
   for U in itertools.combinations(range(12),size):
    A=N[:,U,:][:,:,U];B=np.einsum('iab,icd,ief,igh,i->acegbdfh',A,A,A,A,1/np.array(sq)).reshape(size**4,size**4)
    w,V=np.linalg.eigh(B);tested+=1;smallest=min(smallest,float(w[0]))
    if w[0]>=-1e-7:continue
    v=np.rint(V[:,0]*10000).astype(np.int64)
    cs=[int(v@np.kron(np.kron(np.kron(a,a),a),a)@v)for a in A]
    exact=sum(Fraction(c,q)for c,q in zip(cs,sq))
    if exact<0:
     cert=dict(kind='localized_primary4',subset=list(U),vector=v.tolist(),coefficients=cs,squared_dimensions=sq,exact_quadratic_value=str(exact),gate='global dimension32 implies weakly group-theoretical hence unitarizable');break
   if cert:break
  out.append(dict(id=rid,certificate=cert,tested_subsets=tested,smallest_numerical_eigenvalue=smallest));print(rid,'EXCLUDED'if cert else'no witness',smallest,flush=True)
 (HERE/'primary4.json').write_text(json.dumps(dict(records=out,seconds=time.monotonic()-start,theorem='Huang-Liu-Palcoux-Wu2210.00792 Theorems3.12 and4.1'),indent=2)+'\n')
if __name__=='__main__':main()

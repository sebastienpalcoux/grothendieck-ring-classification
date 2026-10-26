"""Finite discovery only: exact negative witnesses, otherwise no conclusion."""
from pathlib import Path
from fractions import Fraction
import itertools,json,time,math
import numpy as np
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'rank12-m1-offline-20261025'
PREV=HERE.parents[1]/'rank12-m1-round2-20261025'

def main():
    start=time.monotonic()
    data=json.loads((PREV/'unresolved_tensors.json').read_text())
    profiles={x['id']:x for x in json.loads((BASE/'profile.json').read_text())['records']}
    rows=[]
    for row in data:
        family=row['exact_dimension_character']['family']
        if family not in ['D48','D144']:continue
        rid=row['id'];N=np.array(row['tensor'],dtype=np.int64)
        sq=profiles[rid]['squared_dimensions']
        dims=np.sqrt(sq)
        certificate=None;minimum=0.;checks=0
        for degree,size in [(4,3),(5,2),(6,2)]:
            for U in itertools.combinations(range(12),size):
                A=N[:,U,:][:,:,U];K=A.copy();dim=size
                for _ in range(degree-1):
                    K=np.einsum('iab,icd->iacbd',K,A).reshape(12,dim*size,dim*size);dim*=size
                B=np.einsum('iab,i->ab',K,np.array(dims,dtype=float)**(2-degree))
                w,V=np.linalg.eigh(B);checks+=1;minimum=min(minimum,float(w[0]))
                if w[0]>=-1e-7:continue
                v=np.rint(V[:,0]*10000).astype(np.int64)
                cs=[int(v@a@v)for a in K]
                if degree%2==0:
                    value=sum(Fraction(c,q**((degree-2)//2))for c,q in zip(cs,sq))
                else:
                    value=Fraction(0);scale=10**9
                    for c,q in zip(cs,sq):
                        a=math.isqrt(q*scale*scale);b=a if a*a==q*scale*scale else a+1
                        value+=Fraction(c*(b if c>=0 else a),scale*q**((degree-1)//2))
                if value<0:
                    certificate=dict(degree=degree,subset=list(U),vector=v.tolist(),coefficients=cs,squared_dimensions=sq,upper_bound=str(value),scope='general complex',gate='ENO two-prime solvability and GHR unitarizability');break
            if certificate:break
        rows.append(dict(id=rid,family=family,tensor_sha256=row['tensor_sha256'],certificate=certificate,tests=checks,minimum_numerical_eigenvalue=minimum))
        print(rid,'negative witness'if certificate else'no negative witness',minimum,flush=True)
    (HERE/'higher_primary_results.json').write_text(json.dumps(dict(records=rows,seconds=time.monotonic()-start,scope='No witness is not a positivity certificate'),indent=2)+'\n')
if __name__=='__main__':main()

"""Short sparse full primary-3 search; exact integer/radical negative witnesses."""
from pathlib import Path
import json,time
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh,ArpackNoConvergence
from primary import upper_bound
from state import current
ROOT=Path(__file__).resolve().parent
def main():
    start=time.monotonic();data=json.loads((ROOT/'tensors.json').read_text());ex,mo=current();rows=[]
    elig={r['id']:r for r in json.loads((ROOT/'primary.json').read_text())['records']}
    for profile in json.loads((ROOT/'profile.json').read_text())['records']:
        rid=profile['id']
        if rid in ex or rid in mo or rid not in elig:continue
        sq=profile['squared_dimensions'];N=data[rid]
        AA=[sp.kron(sp.kron(sp.csr_matrix(A,dtype=np.int64),sp.csr_matrix(A,dtype=np.int64)),sp.csr_matrix(A,dtype=np.int64),format='csr')for A in N]
        B=sum((A*(1/d)for A,d in zip(AA,np.sqrt(sq))),sp.csr_matrix((1728,1728)))
        c=None;completed=True
        try:
            w,V=eigsh(B,k=1,which='SA',tol=1e-7,maxiter=80,v0=np.linspace(1,2,1728))
            if w[0]<-1e-6:
                v=np.rint(V[:,0]*10000).astype(np.int64);cs=[int(v@(A@v))for A in AA];upper=upper_bound(cs,sq)
                if upper<0:c=dict(kind='full_primary3_with_solvable_unitarity_gate',vector=v.tolist(),coefficients=cs,squared_dimensions=sq,global_dimension=sum(sq),rigorous_quadratic_upper_bound=str(upper),scope='general_complex_fusion_category')
        except ArpackNoConvergence:completed=False
        rows.append(dict(id=rid,tensor_sha256=profile['tensor_sha256'],certificate=c,numerical_discovery_completed=completed))
    (ROOT/'primary_full.json').write_text(json.dumps(dict(records=rows,elapsed_seconds=time.monotonic()-start,scope='Only exact negative witnesses assign status; numerical nonnegativity is not an exact pass'),indent=2)+'\n')
    print('tested',len(rows),'negative certificates',sum(bool(r['certificate'])for r in rows),'seconds',time.monotonic()-start)
if __name__=='__main__':main()

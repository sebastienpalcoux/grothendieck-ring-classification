"""Conditional discovery: use only after the cyclic-stabilizer GT proof audit."""
from pathlib import Path
import json,time,itertools
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh,ArpackNoConvergence
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1]/'rank12-m1-offline-20261025';PREV=HERE.parents[1]/'rank12-m1-round2-20261025'
def main():
 start=time.monotonic();data=json.loads((PREV/'unresolved_tensors.json').read_text());P={r['id']:r for r in json.loads((BASE/'profile.json').read_text())['records']};out=[]
 for row in data:
  if row['exact_dimension_character']['family']!='D120':continue
  N=np.array(row['tensor'],dtype=np.int64);sq=P[row['id']]['squared_dimensions'];dims=[round(q**.5)for q in sq]
  if any(d*d!=q or 10%d for d,q in zip(dims,sq)):raise ValueError('dimension binding')
  weights=[10//d for d in dims];cert=None;minimum=0;completed=True
  AA=[sp.kron(sp.kron(sp.csr_matrix(A),sp.csr_matrix(A)),sp.csr_matrix(A),format='csr')for A in N]
  B=sum((w*A for w,A in zip(weights,AA)),sp.csr_matrix((1728,1728),dtype=np.int64))
  try:
   w,V=eigsh(B.astype(float),k=1,which='SA',tol=1e-8,maxiter=160,v0=np.linspace(1,2,1728));minimum=float(w[0])
   if minimum < -1e-6:
    v=np.rint(V[:,0]*10000).astype(np.int64);value=int(v@(B@v))
    if value<0:cert=dict(vector=v.tolist(),weights=weights,exact_scaled_value=value,scaling=10,scope='unitary; general once forced-GT lemma audited')
  except ArpackNoConvergence:completed=False
  out.append(dict(id=row['id'],tensor_sha256=row['tensor_sha256'],certificate=cert,minimum_numerical_eigenvalue=minimum,completed=completed));print(row['id'],minimum,'NEGATIVE'if cert else'no witness',flush=True)
 (HERE/'d120_primary_results.json').write_text(json.dumps(dict(records=out,seconds=time.monotonic()-start),indent=2)+'\n')
if __name__=='__main__':main()

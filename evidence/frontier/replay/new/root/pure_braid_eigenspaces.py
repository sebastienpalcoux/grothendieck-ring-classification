"""Necessary spectral intersections for three-strand pure braids; integer only."""
from pathlib import Path
import json,hashlib,time
import numpy as np
P=Path(__file__).resolve().parents[2]
source=P/'prior/supplements/rank6/research/frontier/new_research/r155_modular/reconstruction.json'
J=json.loads(source.read_text()); N=np.array(J['fusion_rules'],dtype=np.int64)
t=np.array([12,0,0,12,21,0,12,21,4,16,8,20,5,5,13,13,6,6,18,18,9,9,12,0,18,0])
r=len(N); counts=0; violations=[]; tight=0; start=time.time()
# M[a,b,c,d,e] counts the ab-channel twist e in Hom(d, a*b*c).
M=np.zeros((r,r,r,r,24),dtype=np.int64)
for e in range(24):
    xs=np.flatnonzero(t==e)
    M[:,:,:,:,e]=np.einsum('abx,xcd->abcd',N[:,:,xs],N[xs,:,:])
for a in range(r):
 for b in range(r):
  for c in range(r):
   A=M[a,b,c]; B=M[b,c,a]; C=M[a,c,b]
   n=A.sum(axis=1)
   assert np.array_equal(n,B.sum(axis=1)) and np.array_equal(n,C.sum(axis=1))
   for e in np.flatnonzero(A.sum(axis=0)):
    for f in np.flatnonzero(B.sum(axis=0)):
     g=(t+t[a]+t[b]+t[c]-e-f)%24
     rhs=n+C[np.arange(r),g]
     gap=rhs-A[:,e]-B[:,f]
     active=(A[:,e]>0)&(B[:,f]>0)
     counts+=int(active.sum());tight+=int(((gap==0)&active).sum())
     for d in np.flatnonzero((gap<0)&active): violations.append([a,b,c,int(d),int(e),int(f),int(g[d]),int(gap[d])])
out={'criterion':'pairwise eigenvector intersection for pure-braid monodromy triple',
     'scope':'necessary complex ribbon consistency, not categorification',
     'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
     'twist_exponents_mod24':t.tolist(),'ordered_nonzero_tests':counts,
     'equalities':tight,'violations':violations,'elapsed_seconds':time.time()-start}
(Path(__file__).parent/'pure_braid_eigenspaces_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

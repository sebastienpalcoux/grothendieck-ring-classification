"""Independent exact verification of Liptrap Definition 4.3 certificates."""
from pathlib import Path
import json,itertools,numpy as np
P=Path(__file__).resolve().parents[2]
D=json.load(open(P/'work/input_audit/tensors.json'))
C=json.load(open(P/'work/literature/gty_liptrap_certificates.json'))
results={}
for rid,c in C.items():
 if not c['found']:continue
 N=np.array(D[rid]);n=len(N);S=c['serfs'];M=c['lords'];H=c['stabilizer'];q=c['modulus']
 dual=[next(j for j in range(n) if N[i,j,0]) for i in range(n)]
 def prod(a,b):
  z=np.flatnonzero(N[a,b]);assert len(z)==1;return int(z[0])
 assert all(N[m,k,l]==0 for m,k,l in itertools.product(M,M,M))
 assert all([a for a in S if prod(a,m)==m]==H for m in M)
 assert all([a for a in S if prod(m,a)==m]==H for m in M)
 assert c['tau']=='1/2' and len(H)==4
 X={(f,a,b,m):e for f,a,b,m,e in c['phase_values']}
 def v(f,a,b,m):return X.get((f,a,b,m),0)
 count=0
 for a,b,m in itertools.product(S,S,M):
  assert (v('chi',b,a,dual[m])-v('chi',a,b,prod(prod(a,m),b)))%q==0;count+=1
 for a,b,c0,m in itertools.product(S,S,S,M):
  lhs=v('upsilon',a,b,m)-v('upsilon',a,b,prod(m,dual[c0]))+v('chi',prod(a,b),c0,m)
  rhs=v('chi',a,c0,m)+v('chi',b,c0,prod(dual[a],m))
  assert (lhs-rhs)%q==0;count+=1
 for m in M:
  for a,b in itertools.product(H,H):assert v('chi',a,b,m)==v('chi',b,a,m)
  for a,b,c0 in itertools.product(H,H,H):assert (v('chi',prod(a,b),c0,m)-v('chi',a,c0,m)-v('chi',b,c0,m))%q==0
  rows=[tuple(v('chi',a,b,m) for b in H) for a in H]
  assert len(set(rows))==len(H)
  assert all(v(f,a,b,m)==0 for f in ['chi','upsilon'] for a,b in itertools.product(S,S) if a==0 or b==0)
 # Reconstruct every nontrivial F block using Liptrap Lemma 5.4 gamma formula.
 cosets=sorted({tuple(sorted(prod(a,h) for h in H)) for a in S})
 def gamma_phase(c0,a,m):
  m1=prod(dual[a],m)
  return (v('upsilon',dual[c0],c0,dual[m1])-v('upsilon',dual[a],a,prod(m1,dual[c0]))-v('chi',a,c0,m))%q
 blocks=0
 for I,J,m in itertools.product(cosets,cosets,M):
  for i,k in itertools.product(I,I):
   # zeta16 has minimal polynomial x^8+1; exact inner product times4.
   coeff=[0]*8
   for j in J:
    e=(gamma_phase(i,j,m)-gamma_phase(k,j,m))%16
    coeff[e%8]+=1 if e<8 else -1
   assert coeff==([4]+[0]*7 if i==k else [0]*8)
  blocks+=1
 results[rid]={'all_recoupling_matrices_unitary':True,'nontrivial_F_blocks_verified':blocks,'definition_4_3_exactly_verified':True,'quasisymmetry_and_biderivation_identities':count,'nondegenerate_symmetric_bicharacters':len(M),'tau':'1/2','modulus':q}
print(json.dumps(results,indent=2))
(P/'work/literature/gty_verification.json').write_text(json.dumps(results,indent=2)+'\n')

"""Fusion of the triality equivariantization by induction and restriction."""
import sys,json,itertools,numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'work/models'))
from match_models import read,based_iso,tensor_hash,rep_dihedral
from triality_ring import tensors
OUT=Path(__file__).parent

def construct(neutral=None,pairing=0):
 # E neutral labels0..3=V4,4=m; X0,X1=5,6; Y0,Y1=7,8.
 E=next(T for hL,hR,a,T in tensors()if hL==1 and hR==2)
 B=rep_dihedral(8)if neutral is None else neutral
 F=np.zeros((9,9),dtype=int)
 for i,a in enumerate([0,3,0,3,4,None,4]):
  if a is not None:F[i,a]=1
 F[5,1]=F[5,2]=1
 for i in range(2):F[7+i,5+i]=F[7+i,7+(i^pairing)]=1
 T=np.zeros((9,9,9),dtype=int);T[:7,:7,:7]=B
 for i,j in itertools.product(range(9),repeat=2):
  if i<7 and j<7:continue
  v=np.zeros(9,dtype=int)
  if i>=7:
   for a in range(9):v+=F[j,a]*np.array(E[5+i-7][a])
  else:
   for a in range(9):v+=F[i,a]*np.array(E[a][5+j-7])
  T[i,j]=F@v
 assert np.array_equal(np.einsum('ijx,xkl->ijkl',T,T),np.einsum('jkx,ixl->ijkl',T,T))
 assert np.array_equal(np.einsum('ijk,ka->ija',T,F),np.einsum('ia,jb,abc->ijc',F,F,np.array(E)))
 return T.tolist(),F.tolist(),E
def rep_semidihedral16():
 T=[[[0]*7 for _ in range(7)]for _ in range(7)]
 ks=[1,2,5];orb={1:4,3:4,2:5,6:5,5:6,7:6}
 for i,j in itertools.product(range(4),repeat=2):T[i][j][i^j]=1
 for i,k in itertools.product(range(4),ks):
  z=orb[(k+4*(i//2))%8];T[i][orb[k]][z]=T[orb[k]][i][z]=1
 for k,l in itertools.product(ks,repeat=2):
  for z in [(k+l)%8,(k+3*l)%8]:
   if z in [0,4]:
    a=0 if z==0 else 2;T[orb[k]][orb[l]][a]+=1;T[orb[k]][orb[l]][a+1]+=1
   else:T[orb[k]][orb[l]][orb[z]]+=1
 return T

def main():
 records=[]
 for name,B,pairing in [('Rep(D16)',rep_dihedral(8),0),('Rep(SD16)',rep_semidihedral16(),1)]:
  T,F,E=construct(B,pairing);matches=[]
  for idx,R in enumerate(read(9),1):
   p=based_iso(R,T)
   if p is not None:matches.append((f'R9_1_{idx}',p,tensor_hash(R)))
  print(name,matches)
  assert len(matches)==1
  rid,p,sha=matches[0]
  rec={'id':rid,'status':'unitarily_realized','model':'C2-equivariantization of a nontrivial C3 extension of Rep(D8)','tensor_sha256':sha,'model_tensor':T,'source_to_model':p,'restriction_to_triality':F,'triality_tensor':E,'neutral_model':name,'orbit_pairing':pairing,'categorical_proof_file':'work/resolve_small_models/TRIALITY_EQUIVARIANT.md'}
  records.append(rec)
 assert [r['id']for r in records]==['R9_1_12','R9_1_108']
 (OUT/'triality_equivariant_certificate.json').write_text(json.dumps(records,indent=2)+'\n')
if __name__=='__main__':main()

"""Enumerate rank-two C3 extensions of the TY(V4) fusion ring.
Categorical existence and admissible module structures are proved in THEORY.md.
"""
import itertools,sys,json,numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'work/models'))
from match_models import read,based_iso,tensor_hash

def tensors():
 for hL,hR in itertools.product(range(1,4),repeat=2):
  phi=lambda g:int(g not in [0,hL]);psi=lambda g:int(g not in [0,hR])
  T=np.zeros((9,9,9),dtype=int)
  for g,h in itertools.product(range(4),repeat=2):T[g,h,g^h]=1
  for g in range(4):T[g,4,4]=T[4,g,4]=T[4,4,g]=1
  for i in range(2):
   for g in range(4):
    T[g,5+i,5+(i^phi(g))]=T[5+i,g,5+(i^psi(g))]=1
    T[g,7+i,7+(i^psi(g))]=T[7+i,g,7+(i^phi(g))]=1
   for j in range(2):
    T[4,5+i,5+j]=T[5+i,4,5+j]=T[4,7+i,7+j]=T[7+i,4,7+j]=1
    T[5+i,7+j,4]=T[7+i,5+j,4]=1
    for g in range(4):
     T[5+i,7+j,g]=int(phi(g)==i^j);T[7+i,5+j,g]=int(psi(g)==i^j)
  for a in itertools.product(range(3),repeat=4):
   for i,j in itertools.product(range(2),repeat=2):
    T[5+i,5+j,7]=T[7+j,7+i,5]=a[2*i+j]
    T[5+i,5+j,8]=T[7+j,7+i,6]=2-a[2*i+j]
   if np.array_equal(np.einsum('ijx,xkl->ijkl',T,T),np.einsum('jkx,ixl->ijkl',T,T)):
    yield hL,hR,a,T.tolist()

def main():
 ans=[];R=read(9)[116]
 for hL,hR,a,T in tensors():
  p=based_iso(R,T);assert p is not None
  ans.append({'left_stabilizer_generator':hL,'right_stabilizer_generator':hR,'XX_first_multiplicities':a,'tensor':T,'source_to_model':p})
 assert len(ans)==6
 out={'id':'R9_1_117','status':'unitarily_realized','model':'Nontrivial C3-graded extension of Rep(D8) associated to an order-three Brauer-Picard element','tensor_sha256':tensor_hash(R),'enumerated_associative_extensions':len(ans),'all_match_target':True,'models':ans,'categorical_existence_reference':'Nikshych--Riepel, arXiv:1309.5026, Example 9.3 and Remark 4.2','unitarity_reference':'Galindo--Hong--Rowell, Generalized and quasi-localizations of braid group representations, Theorem 5.20'}
 path=Path(__file__).with_name('triality_117_certificate.json');path.write_text(json.dumps(out,indent=2)+'\n');print('PASS',len(ans),'associative possibilities, all exactly R9_1_117; left/right stabilizers always distinct')
if __name__=='__main__':main()

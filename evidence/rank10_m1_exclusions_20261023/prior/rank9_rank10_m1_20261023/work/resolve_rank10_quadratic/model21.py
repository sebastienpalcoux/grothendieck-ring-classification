"""Independent tensor of the bosonic permutation quotient of PSU(2)_6^2.
Canonical basis: 1,s,g,sg,a,ga,b,sb,gb,sgb (V4 coordinates).
The construction and fixed-point resolution are in model21.tex.
"""
import json,itertools
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]

def construct():
 n=10;N=np.zeros((n,n,n),dtype=int)
 def act(q,z):
  if z<4:return q^z
  if z<6:return 4+((z-4)^((q>>1)&1))
  return 6+((z-6)^q)
 def shifted(v,q):
  ans=np.zeros(n,dtype=int)
  for z,c in enumerate(v):ans[act(q,z)]+=int(c)
  return ans
 base={('a','a'):[1,1,0,0,1,1,1,1,0,0],('a','b'):[0,0,0,0,1,0,1,1,1,1],('b','b'):[1,0,0,0,1,1,1,1,1,1]}
 for i,j in itertools.product(range(n),repeat=2):
  if i<4:N[i,j,act(i,j)]=1;continue
  if j<4:N[i,j,act(j,i)]=1;continue
  ki,qi=('a',2*(i-4))if i<6 else('b',i-6)
  kj,qj=('a',2*(j-4))if j<6 else('b',j-6)
  N[i,j]=shifted(base[tuple(sorted((ki,kj)))],qi^qj)
 return N

def main():
 N=construct();n=len(N)
 if not np.array_equal(N,N.swapaxes(0,1)):raise ValueError('commutativity')
 if not np.array_equal(np.einsum('ijx,xkl->ijkl',N,N),np.einsum('jkx,ixl->ijkl',N,N)):raise ValueError('associativity')
 if not np.array_equal(N[:,:,0],np.eye(n,dtype=int)):raise ValueError('duality')
 T=json.load(open(ROOT/'work/input_audit/tensors.json'))
 matches=[]
 # Dimension strata fix the three nontrivial invertibles, the a pair and the b quartet.
 for gid in [21,114,115,152,153,179]:
  R=np.array(T[f'R10_1_{gid}'])
  inv=[i for i in range(1,n) if sum(R[i,i])==1 and R[i,i,0]==1]
  # Match all basis permutations via multiplication-invariant local signatures.
  sig=lambda X,i:tuple(sorted([tuple(sorted(X[i,j]))for j in range(n)]))
  candidates=[[j for j in range(n)if sig(N,i)==sig(R,j)]for i in range(n)]
  p=[-1]*n;p[0]=0
  def search(i,used):
   if i==n:
    if np.array_equal(N,R[np.ix_(p,p,p)]):return p[:]
    return None
   for j in candidates[i]:
    if j in used:continue
    p[i]=j
    if all(N[a,b,c]==R[p[a],p[b],p[c]]for a,b,c in itertools.product(range(i+1),repeat=3)):
     out=search(i+1,used|{j})
     if out is not None:return out
   p[i]=-1
  pmap=search(1,{0})
  if pmap is not None:matches.append({'id':f'R10_1_{gid}','basis_map':pmap,'basis_map_direction':'model_to_input','input_to_model_basis_map':[pmap.index(i)for i in range(n)]})
 if len(matches)!=1 or matches[0]['id']!='R10_1_21':raise ValueError(matches)
 out={'status':'actual_unitary_model','construction':'((PSU(2)_6 Deligne PSU(2)_6)^C2)_(1+(f,f)_minus)','basis':['1','s','g','sg','a','ga','b','sb','gb','sgb'],'tensor':N.tolist(),'matches':matches,'associativity_equations':n**4,'checked_coefficients':n**3,'proof':'work/resolve_rank10_quadratic/model21.tex','independent_verifier':'work/audit_new_models/verify_model21.py','independent_receipt':'work/audit_new_models/model21_audit.json'}
 (HERE/'model21.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items()if k!='tensor'},indent=2))
if __name__=='__main__':main()

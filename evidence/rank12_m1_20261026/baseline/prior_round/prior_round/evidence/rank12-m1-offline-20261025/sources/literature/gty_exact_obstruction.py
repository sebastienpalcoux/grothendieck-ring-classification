"""Exact monomial-relation contradictions; valid over C*, no finite-order assumption."""
from pathlib import Path
import json,itertools,sys,numpy as np
sys.path.insert(0,str(Path(__file__).parent))
import gty_liptrap as G
P=Path(__file__).resolve().parents[2]
D=json.load(open(P/'work/input_audit/tensors.json'))
cap={}
def capture(A,B,q):cap.update(A=A,B=B);return []
G.solve_mod_batch=capture

def rowsparseadd(a,b,k):
 z=a.copy()
 for i,c in b.items():
  z[i]=z.get(i,0)+k*c
  if not z[i]:del z[i]
 return z

def eliminate(A,B):
 # Only integral elementary row operations and column swaps: every zero row
 # with a nonintegral right side is an exact multiplicative contradiction.
 A=A.astype(object);B=B.astype(object);m,n=A.shape;E=[{i:1} for i in range(m)];r=0
 while r<min(m,n):
  W=A[r:,r:];ij=np.argwhere(W!=0)
  if not len(ij):break
  i,j=map(int,min(ij,key=lambda p:abs(W[tuple(p)]))+np.array([r,r]))
  if i!=r:A[[r,i]]=A[[i,r]];B[[r,i]]=B[[i,r]];E[r],E[i]=E[i],E[r]
  if j!=r:A[:,[r,j]]=A[:,[j,r]]
  while True:
   if A[r,r]<0:A[r]=-A[r];B[r]=-B[r];E[r]={k:-v for k,v in E[r].items()}
   ids=np.flatnonzero(A[r+1:,r])+r+1
   if not len(ids):break
   for i in ids:
    k=-int(A[i,r]//A[r,r]);A[i]+=k*A[r];B[i]+=k*B[r];E[i]=rowsparseadd(E[i],E[r],k)
    if A[i,r]:
     A[[r,i]]=A[[i,r]];B[[r,i]]=B[[i,r]];E[r],E[i]=E[i],E[r];break
  r+=1
 z=np.flatnonzero(np.all(A==0,axis=1));cert=[]
 for col in range(B.shape[1]):
  witnesses=[int(i) for i in z if B[i,col]%4]
  if not witnesses:cert.append(None);continue
  i=min(witnesses,key=lambda i:len(E[i]));c=E[i]
  assert all(sum(v*int(cap['A'][k,j]) for k,v in c.items())==0 for j in range(n))
  rhs=sum(v*int(cap['B'][k,col]) for k,v in c.items())
  assert rhs%4
  cert.append({'form_pair_index':col,'row_combination':sorted(c.items()),'right_side_mod4':int(rhs%4)})
 print('integer row rank',r,'residual rank rows',sum(any(v for v in row) for row in A[r:]),'contradicted',sum(c is not None for c in cert),'/',len(cert),flush=True)
 return cert

out={}
for k in [118,122,180]:
 rid='R10_1_'+str(k);result=G.construct(np.array(D[rid]),q=4)
 cert=eliminate(cap['A'],cap['B'])
 out[rid]={'all_complex_solutions_excluded':all(c is not None for c in cert),'form_count':result['forms'],'form_pairs':cert,'equation_matrix':cap['A'].tolist(),'rhs_mod4':cap['B'].tolist()}
(P/'work/literature/gty_exact_obstructions.json').write_text(json.dumps(out,indent=2)+'\n')

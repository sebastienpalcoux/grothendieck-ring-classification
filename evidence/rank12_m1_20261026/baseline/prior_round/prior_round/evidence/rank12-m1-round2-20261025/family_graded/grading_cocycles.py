"""Small exact H3 cocycle representative generator; positive construction only."""
import itertools,numpy as np
from h4_bimodules import need

def reduce4(A,track=False):
 A=np.array(A,dtype=np.int64)%4;m,n=A.shape;T=np.eye(n,dtype=np.int64);U=np.eye(m,dtype=np.int64)if track else None;r=0
 while r<min(m,n):
  nz=np.argwhere(A[r:,r:])
  if not len(nz):break
  pos=min(nz,key=lambda ij:0 if int(A[r+ij[0],r+ij[1]])%2 else 1);i,j=map(int,pos+np.array([r,r]));d=1 if A[i,j]%2 else 2
  A[[r,i]]=A[[i,r]]
  if track:U[[r,i]]=U[[i,r]]
  A[:,[r,j]]=A[:,[j,r]];T[:,[r,j]]=T[:,[j,r]];u=pow(int(A[r,r])//d,-1,4);A[r]=A[r]*u%4
  if track:U[r]=U[r]*u%4
  for i in np.flatnonzero(A[r+1:,r])+r+1:
   v=int(A[i,r])//d;A[i]=(A[i]-v*A[r])%4
   if track:U[i]=(U[i]-v*U[r])%4
  for j in np.flatnonzero(A[r,r+1:])+r+1:
   v=int(A[r,j])//d;A[:,j]=(A[:,j]-v*A[:,r])%4;T[:,j]=(T[:,j]-v*T[:,r])%4
  r+=1
 return A,T,U,r

def representatives(G,c):
 n=len(G);keys=list(itertools.product(range(1,n),repeat=3));ix={k:i for i,k in enumerate(keys)};A=[]
 def row(terms):
  out=[0]*len(keys)
  for v,k in terms:
   if k in ix:out[ix[k]]+=v
  return out
 for a,b,d,e in itertools.product(range(1,n),repeat=4):A.append(row([(1,(b,d,e)),(1,(a,G[b][d],e)),(1,(a,b,d)),(-1,(G[a][b],d,e)),(-1,(a,b,G[d][e]))]))
 A.append(row([(1,(c,c,c))]));orig=np.array(A,dtype=np.int64);diag,T,_,r=reduce4(A);gens=[]
 for i in range(len(keys)):
  if i<r and diag[i,i]==1:continue
  g=T[:,i]*(2 if i<r else 1)%4;need(np.all(orig@g%4==0),'normalized 3cocycle generator');gens.append(g)
 pairs=list(itertools.product(range(1,n),repeat=2));pi={k:i for i,k in enumerate(pairs)};B=[]
 for a,b,d in keys:
  row0=[0]*len(pairs)
  for v,k in [(1,(b,d)),(1,(a,G[b][d])),(-1,(G[a][b],d)),(-1,(a,b))]:
   if k in pi:row0[pi[k]]+=v
  B.append(row0)
 B=np.array(B,dtype=np.int64);A0,T0,U0,r0=reduce4(B,True)
 def key(v):
  w=U0@v%4
  return tuple([int(w[i]%A0[i,i])for i in range(r0)if A0[i,i]!=1]+list(map(int,w[r0:])))
 selected=[];Ab,_,Ub,rb=reduce4(B,True)
 def inside(v):
  w=Ub@v%4
  return not np.any(w[rb:])and all(int(w[i])%int(Ab[i,i])==0 for i in range(rb))
 for g in gens:
  if inside(g):continue
  selected.append(g);Ab,_,Ub,rb=reduce4(np.column_stack([B,*selected]),True)
 need(len(selected)<=5,'small cohomology quotient representative budget');seen=set();reps=[]
 for coeff in itertools.product(range(4),repeat=len(selected)):
  v=sum((a*g for a,g in zip(coeff,selected)),np.zeros(len(keys),dtype=np.int64))%4;k=key(v)
  if k in seen:continue
  seen.add(k);omega=[[[0]*n for _ in range(n)]for _ in range(n)]
  for abc,i in ix.items():a,b,d=abc;omega[a][b][d]=int(v[i])
  need(omega[c][c][c]==0 and all((omega[b][d][e]+omega[a][G[b][d]][e]+omega[a][b][d]-omega[G[a][b]][d][e]-omega[a][b][G[d][e]])%4==0 for a,b,d,e in itertools.product(range(n),repeat=4)),'all 3cocycle identities')
  reps.append(omega)
 return reps,dict(phase_modulus=4,normalized_variables=len(keys),kernel_generators=len(gens),cohomology_generators=len(selected),representative_count=len(reps))

"""Actual graded A-bimodules and balanced quotients; phases modulo four."""
from pathlib import Path
import itertools,json,sys,collections,numpy as np
BASE=Path(__file__).resolve().parents[2]/'rank12-m1-offline-20261025'
sys.path.insert(0,str(BASE));from group_models import common
need=common.require

def linear_solutions(A,b,q=4,limit=4096):
 A=np.array(A,dtype=np.int64)%q;b=np.array(b,dtype=np.int64)%q;m,n=A.shape;T=np.eye(n,dtype=np.int64);r=0
 while r<min(m,n):
  nz=np.argwhere(A[r:,r:])
  if not len(nz):break
  pos=min(nz,key=lambda ij:0 if int(A[r+ij[0],r+ij[1]])%2 else 1);i,j=map(int,pos+np.array([r,r]));d=1 if A[i,j]%2 else 2
  A[[r,i]]=A[[i,r]];b[[r,i]]=b[[i,r]];A[:,[r,j]]=A[:,[j,r]];T[:,[r,j]]=T[:,[j,r]]
  u=pow(int(A[r,r])//d,-1,q);A[r]=A[r]*u%q;b[r]=b[r]*u%q
  for i in np.flatnonzero(A[r+1:,r])+r+1:
   v=int(A[i,r])//d;A[i]=(A[i]-v*A[r])%q;b[i]=(b[i]-v*b[r])%q
  for j in np.flatnonzero(A[r,r+1:])+r+1:
   v=int(A[r,j])//d;A[:,j]=(A[:,j]-v*A[:,r])%q;T[:,j]=(T[:,j]-v*T[:,r])%q
  r+=1
 if np.any(b[r:])or any(int(b[i])%int(A[i,i])for i in range(r)):return []
 choices=[[(int(b[i])//int(A[i,i])+k*(q//int(A[i,i])))%q for k in range(int(A[i,i]))]for i in range(r)]+[list(range(q))for i in range(r,n)]
 count=np.prod([len(v)for v in choices]);need(count<=limit,'short linear solution limit')
 return[(T@np.array(v,dtype=np.int64))%q for v in itertools.product(*choices)]

def construct(G,H,w,psi,expected_rank=12):
 n=len(G);inv=[next(j for j in range(n)if G[i][j]==0)for i in range(n)];H=sorted(H);hs=set(H)
 need(all((psi(a,b)+psi(G[a][b],c)-w(a,b,c)-psi(b,c)-psi(a,G[b][c]))%4==0 for a,b,c in itertools.product(H,repeat=3)),'algebra associativity')
 objs=[];seen=set()
 for z in range(n):
  if z in seen:continue
  D=sorted({G[G[a][z]][b]for a,b in itertools.product(H,repeat=2)});seen.update(D);L={};leftcosets=[];done=set()
  for x0 in D:
   if x0 in done:continue
   leftcosets.append(x0)
   for h in H:done.add(G[h][x0])
   for a,h in itertools.product(H,repeat=2):L[a,G[h][x0]]=(psi(a,h)-w(a,h,x0))%4
  keys=[(b,x)for b in H if b for x in D];ki={k:i for i,k in enumerate(keys)};A=[];rhs=[]
  def add(terms,v):
   row=[0]*len(keys)
   for c,key in terms:
    if key in ki:row[ki[key]]+=c
   A.append(row);rhs.append(v)
  for a,b,x in itertools.product(H,H,D):add([(1,(a,x)),(1,(b,G[x][a])),(-1,(G[a][b],x))],w(x,a,b)+psi(a,b))
  for a,b,x in itertools.product(H,H,D):add([(1,(b,G[a][x])),(-1,(b,x))],w(a,x,b)+L[a,G[x][b]]-L[a,x])
  # Gauge on left H-cosets: normalize a spanning right-action tree.
  visited={leftcosets[0]};queue=[leftcosets[0]]
  cosetof={G[a][x0]:x0 for x0 in leftcosets for a in H}
  for x0 in queue:
   for b in H:
    y0=cosetof[G[x0][b]]
    if y0 not in visited:add([(1,(b,x0))],0);visited.add(y0);queue.append(y0)
  solutions=linear_solutions(A,rhs)
  K=[a for a in H if G[G[inv[z]][a]][z]in hs]
  need(len(solutions)==len(K),'complete one-dimensional projective stabilizer characters')
  for v in solutions:
   R={(b,x):(0 if b==0 else int(v[ki[b,x]]))for b,x in itertools.product(H,D)}
   for a,b,x in itertools.product(H,H,D):
    need((L[b,x]+L[a,G[b][x]]-psi(a,b)-L[G[a][b],x]+w(a,b,x))%4==0,'left module')
    need((R[a,x]+R[b,G[x][a]]-w(x,a,b)-psi(a,b)-R[G[a][b],x])%4==0,'right module')
    need((L[a,x]+R[b,G[a][x]]-w(a,x,b)-R[b,x]-L[a,G[x][b]])%4==0,'bimodule compatibility')
   objs.append(dict(z=z,D=D,K=K,L=L,R=R))
 rank=len(objs)
 if rank!=expected_rank:return None,dict(rank=rank)
 N=[[[0]*rank for _ in range(rank)]for _ in range(rank)]
 for i,U in enumerate(objs):
  for j,V in enumerate(objs):
   pairs=list(itertools.product(U['D'],V['D']));maps={};reps=[]
   for P in pairs:
    if P in maps:continue
    rep=P;reps.append(rep);maps[P]=(rep,0);queue=[P]
    for x,y in queue:
     for h in H:
      Q=(G[x][h],G[inv[h]][y]);delta=(w(G[x][h],inv[h],y)+V['L'][inv[h],y]-U['R'][inv[h],G[x][h]])%4
      phase=(maps[x,y][1]-delta)%4
      if Q in maps:need(maps[Q]==(rep,phase),'balanced consistency')
      else:maps[Q]=(rep,phase);queue.append(Q)
   need(len(reps)*len(H)==len(pairs),'balanced quotient dimension')
   left={};right={}
   for a in H:
    for P in reps:
     x,y=P;Q,b=maps[G[a][x],y];left[a,P]=(Q,(U['L'][a,x]-w(a,x,y)+b)%4)
     Q,b=maps[x,G[y][a]];right[a,P]=(Q,(w(x,y,a)+V['R'][a,y]+b)%4)
   for P in pairs:
    x,y=P;rep,a=maps[P]
    for h in H:
     for target,phase,ops in [((G[h][x],y),U['L'][h,x]-w(h,x,y),left),((x,G[y][h]),w(x,y,h)+V['R'][h,y],right)]:
      Q,b=maps[target];Q0,c=ops[h,rep];need(Q==Q0 and(phase+b-a-c)%4==0,'balanced action descent')
   for k,W in enumerate(objs):
    z=W['z'];basis=[P for P in reps if G[P[0]][P[1]]==z];co=[0]*4
    for a in W['K']:
     b=G[G[inv[z]][inv[a]]][z];chi=(W['R'][b,z]+W['L'][a,G[z][b]])%4
     for P in basis:
      Q,c=right[b,P];T,d=left[a,Q]
      if T==P:co[(c+d-chi)%4]+=1
    need(co[1]==co[3]and(co[0]-co[2])%len(W['K'])==0,'integral stabilizer projection');N[i][j][k]=(co[0]-co[2])//len(W['K']);need(N[i][j][k]>=0,'nonnegative multiplicity')
 units=[i for i in range(rank)if all(N[i][j][k]==N[j][i][k]==int(j==k)for j,k in itertools.product(range(rank),repeat=2))]
 need(len(units)==1,'unique simple tensor unit');u=units[0]
 order=[u]+[i for i in range(rank)if i!=u]
 N=[[[N[i][j][k]for k in order]for j in order]for i in order];objs=[objs[i]for i in order]
 common.validate(N)
 return N,dict(rank=rank,simple_dimensions=[len(U['D'])//len(H)for U in objs],objects=[dict(z=U['z'],D=U['D'],K=U['K'],L=[[a,x,v]for(a,x),v in U['L'].items()],R=[[a,x,v]for(a,x),v in U['R'].items()])for U in objs])

if __name__=='__main__':
 from group_models import group_product,fusion
 from extra_models import a4_table
 G=group_product(a4_table(),[[0,1],[1,0]]);H=[0,6,17,23];T,info=construct(G,H,lambda a,b,c:0,lambda a,b:0)
 S,inf=fusion(G,H);need(common.based_iso(T,S)is not None,'independent untwisted convolution control');print('PASS untwisted control')

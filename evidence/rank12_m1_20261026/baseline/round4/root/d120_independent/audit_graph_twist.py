"""Independent monomial Hom-space audit: no character trace projection."""
from pathlib import Path
from itertools import product
import json,time,hashlib,sys
import numpy as np
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parents[1];MOD=20

def require(c,m):
 if not c:raise ValueError(m)

def audit(row,w,modulus=20):
 MOD=modulus
 G=row['group_table'];H=row['subgroup'];n=len(G);inv=[next(j for j in range(n)if G[i][j]==0)for i in range(n)]
 require(all(G[0][a]==G[a][0]==a for a in range(n)),'group identity')
 require(all(sorted(G[a])==list(range(n))and sorted(G[b][a]for b in range(n))==list(range(n))for a in range(n)),'Latin group table')
 require(all(G[G[a][b]][c]==G[a][G[b][c]]for a,b,c in product(range(n),repeat=3)),'group associativity')
 require(0 in H and len(H)==len(set(H))and all(G[a][b]in H for a,b in product(H,repeat=2)),'actual subgroup')
 def load(z):
  dim=z['fiber_dimension'];S=list(product(z['support'],range(dim)));lp={(h,x):e for h,x,e in z['left_phases']};rp={tuple(a[:-1]):a[-1]for a in z['right_phases']};P=z.get('right_permutation')
  L={h:{(x,t):((G[h][x],t),lp[h,x])for x,t in S}for h in H}
  R={h:{(x,t):((G[x][h],(t+P[str(h)])%2 if P else 0),rp[x,h,t]if P else rp[x,h])for x,t in S}for h in H}
  return dict(S=S,L=L,R=R,grade=lambda x:x[0],dim=dim)
 O=[load(o)for o in row['info']['objects']]
 # Check all source associativity, including matrix fibers and every grade.
 for A in O:
  for h,k,x in product(H,H,A['S']):
   y,e=A['L'][k][x];z,f=A['L'][h][y];z0,g=A['L'][G[h][k]][x]
   require(z==z0 and(e+f+w(h,k,x[0])-g)%MOD==0,'left source axiom')
   y,e=A['R'][h][x];z,f=A['R'][k][y];z0,g=A['R'][G[h][k]][x]
   require(z==z0 and(e+f-w(x[0],h,k)-g)%MOD==0,'right source axiom')
   y,e=A['L'][h][x];z,f=A['R'][k][y];y0,g=A['R'][k][x];z0,u=A['L'][h][y0]
   require(z==z0 and(e+f-g-u-w(h,x[0],k))%MOD==0,'mixed source axiom')
 # Linear intertwining equations on each grade; every connected component
 # gives one scalar unless a cycle forces that scalar to vanish.
 def hom(A,B):
  states={(a,b)for a,b in product(A['S'],B['S'])if A['grade'](a)==B['grade'](b)};remaining=set(states);dim=0
  while remaining:
   start=min(remaining);phase={start:0};queue=[start];consistent=True
   for a,b in queue:
    ph=phase[a,b]
    for typ,h in product(['L','R'],H):
     x,e=A[typ][h][a];y,f=B[typ][h][b];v=(ph+f-e)%MOD
     require((x,y)in states,'intertwiner grade')
     if(x,y)in phase:
      if phase[x,y]!=v:consistent=False
     else:phase[x,y]=v;queue.append((x,y))
   remaining-=set(queue);dim+=int(consistent)
  return dim
 for i,A in enumerate(O):
  for j,B in enumerate(O):require(hom(A,B)==int(i==j),'simple pairwise inequivalent source objects')
 require(sum((len(A['S'])//len(H))**2 for A in O)==n,'global dimension exhausts simple bimodules')
 R=[[[0]*len(O)for B in O]for A in O];balanced=0
 for i,A in enumerate(O):
  for j,B in enumerate(O):
   raw=set(product(A['S'],B['S']));remaining=set(raw);reduction={}
   while remaining:
    root=min(remaining);reduction[root]=(root,0);queue=[root]
    for a,b in queue:
     root0,ph=reduction[a,b]
     for h in H:
      x,e=A['R'][h][a];q=G[inv[h]][b[0]];bpre=(q,b[1]);y,f=B['L'][h][bpre]
      require(y==b,'left action has trivial fiber permutation')
      nxt=(x,bpre);value=(ph+w(a[0],h,q)+f-e)%MOD
      if nxt in reduction:require(reduction[nxt]==(root0,value),'balanced relation holonomy')
      else:reduction[nxt]=(root0,value);queue.append(nxt)
    require(len(queue)==len(H),'free balancing orbits');remaining-=set(queue)
   S=sorted({r for r,e in reduction.values()});balanced+=len(S);L={};RR={}
   for h in H:
    L[h]={};RR[h]={}
    for a,b in S:
     x,e=A['L'][h][a];root,f=reduction[x,b];L[h][a,b]=(root,(e-w(h,a[0],b[0])+f)%MOD)
     x,e=B['R'][h][b];root,f=reduction[a,x];RR[h][a,b]=(root,(e+w(a[0],b[0],h)+f)%MOD)
   P=dict(S=S,L=L,R=RR,grade=lambda x:G[x[0][0]][x[1][0]])
   for k,C in enumerate(O):R[i][j][k]=hom(C,P)
 require(R==row['model_tensor'],'all independent Hom dimensions match all fusion coefficients')
 tensors=json.loads((ROOT/'frozen/target_tensors.json').read_text())
 for hit in row['matches']:
  T=tensors[hit['id']];p=hit['basis_map_source_to_model']
  require(sorted(p)==list(range(12)),'bijective based identification')
  require(all(T[a][b][c]==R[p[a]][p[b]][p[c]]for a,b,c in product(range(12),repeat=3)),'all1728 supplied coefficients')
 return dict(status='PASS',matches=[h['id']for h in row['matches']],source_module_axioms='all',independent_hom_coefficients=len(O)**3,balanced_basis_states=balanced,simple_modules=len(O))

def main():
 t=time.monotonic();rows=json.loads((ROOT/'frozen/all_graph_twists.json').read_text());out=[]
 require(len(rows)==4,'four classes complete')
 for row in rows:
  lam=row['schur_cocycle'];G=row['group_table'];H=row['subgroup'];parity,cup=row['parameters'];Q=np.array([[G[2*a][2*b]//2 for b in range(60)]for a in range(60)],dtype=int);W=np.array(row['transfer_cocycle'],dtype=int)
  require(all(G[a][b]==2*int(Q[a//2,b//2])+((a+b)%2)for a,b in product(range(120),repeat=2)),'G direct product')
  require(all((lam[b][c]+lam[a][Q[b,c]]-lam[Q[a,b]][c]-lam[a][b])%2==0 for a,b,c in product(range(60),repeat=3)),'actual2cocycle')
  for a in range(60):
   b=np.arange(60)[:,None,None];c=np.arange(60)[None,:,None];d=np.arange(60)[None,None,:]
   delta=W[b,c,d]-W[Q[a,b],c,d]+W[a,Q[b,c],d]-W[a,b,Q[c,d]]+W[a,b,c]
   require(not np.any(delta%2),'all12960000 3cocycle equations')
  require(not np.any(W[0])and not np.any(W[:,0])and not np.any(W[:,:,0]),'normalized3cocycle')
  w=lambda x,y,z:10*((parity*(int(W[x//2,y//2,z//2])+(x%2)*(y%2)*(z%2))+cup*(lam[x//2][y//2]+(x%2)*(y%2))*(z%2))%2)
  require(all(w(a,b,c)==0 for a,b,c in product(H,repeat=3)),'subgroup algebra strict')
  r=audit(row,w);r['parameters']=row['parameters'];out.append(r);print(r,flush=True)
 (ROOT/'all_graph_twists_independent.json').write_text(json.dumps(dict(status='PASS',records=out,seconds=time.monotonic()-t),indent=2)+'\n')
if __name__=='__main__':main()


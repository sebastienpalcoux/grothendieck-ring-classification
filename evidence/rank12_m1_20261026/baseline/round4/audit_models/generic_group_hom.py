"""Independent monomial bimodule Hom audit with nontrivial subgroup cochain."""
from itertools import product
from audit_liptrap import need as require
def audit(row,w,modulus=20,psi=None,coefficient=None,check_tensor=True):
 MOD=modulus
 G=row['group_table'];H=row['subgroup'];n=len(G);hi={a:i for i,a in enumerate(H)};psi=psi or [[0]*len(H) for _ in H];ps=lambda a,b:psi[hi[a]][hi[b]];inv=[next(j for j in range(n)if G[i][j]==0)for i in range(n)]
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
   require(z==z0 and(e+f+w(h,k,x[0])-g-ps(h,k))%MOD==0,'left source axiom')
   y,e=A['R'][h][x];z,f=A['R'][k][y];z0,g=A['R'][G[h][k]][x]
   require(z==z0 and(e+f-w(x[0],h,k)-g-ps(h,k))%MOD==0,'right source axiom')
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
 require(all(len(A['S'])%len(H)==0 for A in O),'integer categorical dimensions')
 require(sum((len(A['S'])//len(H))**2 for A in O)==n,'global dimension exhausts simple bimodules')
 if not check_tensor and coefficient is None:return dict(status='PASS',simple_modules=len(O),source_module_axioms='all',independent_hom_coefficients=0)
 R=[[[0]*len(O)for B in O]for A in O];balanced=0
 for i,A in enumerate(O):
  for j,B in enumerate(O):
   if coefficient is not None and (i,j)!=tuple(coefficient[:2]):continue
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
   for k,C in enumerate(O):
    if coefficient is None or k==coefficient[2]:R[i][j][k]=hom(C,P)
 if coefficient is not None:
  i,j,k,m=coefficient;require(R[i][j][k]==m and m>1,'independent nonmultiplicityfree witness')
 else:
  require(R==row['model_tensor'],'all independent Hom dimensions')
  T=row['matched_source'];p=row['source_to_model']
  require(p[0]==0 and sorted(p)==list(range(12)),'unital bijective based identification')
  require(all(T[a][b][c]==R[p[a]][p[b]][p[c]] for a,b,c in product(range(12),repeat=3)),'all1728supplied coefficients')
 return dict(status='PASS',source_module_axioms='all',independent_hom_coefficients=1 if coefficient else len(O)**3,balanced_basis_states=balanced,simple_modules=len(O))

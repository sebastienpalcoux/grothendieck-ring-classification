import itertools,collections,json
from match_models import *
def metaplectic(N):
 # odd SO(N)_2, labels1,Z,X+,X-,Y1,...
 assert N%2==1
 n=(N+7)//2;q=(N-1)//2
 R=[[[0]*n for _ in range(n)]for _ in range(n)]
 for i in range(n):R[0][i][i]=R[i][0][i]=1
 R[1][1][0]=1
 for i in [2,3]:R[1][i][5-i]=R[i][1][5-i]=1
 for i in range(4,n):R[1][i][i]=R[i][1][i]=1
 for a,b in itertools.product([2,3],repeat=2):
  R[a][b][0 if a==b else 1]=1
  for i in range(4,n):R[a][b][i]=1
 for a in [2,3]:
  for i in range(4,n):R[a][i][2]=R[a][i][3]=R[i][a][2]=R[i][a][3]=1
 for a,b in itertools.product(range(1,q+1),repeat=2):
  for c in [a+b,a-b]:
   c%=N;c=min(c,N-c)
   if c==0:R[3+a][3+b][0]+=1;R[3+a][3+b][1]+=1
   else:R[3+a][3+b][3+c]+=1
 return R

def permutation_equivariant(R):
 r=len(R);labs=[([(i,i)],s)for i in range(r)for s in [1,-1]]+[(list({(i,j),(j,i)}),0)for i in range(r)for j in range(i+1,r)]
 n=len(labs);T=[[[0]*n for _ in range(n)]for _ in range(n)]
 for i,(A,s) in enumerate(labs):
  for j,(B,t) in enumerate(labs):
   for k,(C,u) in enumerate(labs):
    c,d=C[0];dim=sum(R[a][b][c]*R[x][y][d]for a,x in A for b,y in B)
    trace=s*t*R[A[0][0]][B[0][0]][c] if s and t and u else 0
    if u:assert (dim+u*trace)%2==0;T[i][j][k]=(dim+u*trace)//2
    else:T[i][j][k]=dim
 return T

def abelian_table(orders):
 R=group(orders);return [[row.index(1)for row in M]for M in R]
def dihedral_table(m):return [[row.index(1)for row in M]for M in pointed_dihedral(m)]
def dicyclic_table(m):
 # a order2m, x^2=a^m, xa=a^-1x; elements a^i x^e.
 els=list(itertools.product(range(2),range(2*m)));ix={x:i for i,x in enumerate(els)}
 return [[ix[((e+f)%2,(i+(-1)**e*j+(m if e*f else 0))%(2*m))]for f,j in els]for e,i in els]
def a4_table():
 els=[p for p in itertools.permutations(range(4)) if sum(p[i]>p[j]for i in range(4)for j in range(i+1,4))%2==0];ix={p:i for i,p in enumerate(els)}
 return [[ix[tuple(a[b[i]]for i in range(4))]for b in els]for a in els]
def element_order(G,x):
 p=x;k=1
 while p!=0:p=G[p][x];k+=1
 return k

def auts(G):
 n=len(G);closure={0};gens=[]
 for a in range(1,n):
  if a in closure:continue
  gens.append(a)
  while True:
   new=closure|{G[x][g]for x in closure for g in gens}
   if new==closure:break
   closure=new
 orders=[element_order(G,x)for x in range(n)]
 for images in itertools.product(*[[x for x in range(n)if orders[x]==orders[g]]for g in gens]):
  mp={0:0};queue=[0];good=True
  for x in queue:
   for a,b in zip(gens,images):
    y,z=G[x][a],G[mp[x]][b]
    if y in mp:
     if mp[y]!=z:good=False;break
    elif z in mp.values():good=False;break
    else:mp[y]=z;queue.append(y)
   if not good:break
  if not good or len(mp)!=n:continue
  p=[mp[i]for i in range(n)]
  assert all(p[G[a][b]]==G[p[a]][p[b]]for a,b in itertools.product(range(n),repeat=2))
  yield p

def pointed_equivariant(G,sigma):
 n=len(G);seen=set();labs=[]
 for a in range(n):
  if a in seen:continue
  A=sorted({a,sigma[a]});seen.update(A)
  for s in ([1,-1]if len(A)==1 else [0]):labs.append((A,s))
 r=len(labs);T=[[[0]*r for _ in range(r)]for _ in range(r)]
 for i,(A,s) in enumerate(labs):
  for j,(B,t) in enumerate(labs):
   for k,(C,u) in enumerate(labs):
    c=C[0];dim=sum(G[a][b]==c for a in A for b in B)
    if u:
     trace=sum(s*t*(G[a][b]==c)for a in A for b in B if sigma[a]==a and sigma[b]==b)
     assert (dim+u*trace)%2==0
     T[i][j][k]=(dim+u*trace)//2
    else:T[i][j][k]=dim
 return T

def crossed(R,sigma):
 r=len(R);n=2*r
 return [[[R[i%r][sigma[j%r]if i//r else j%r][k%r]*int(k//r==(i//r+j//r)%2)for k in range(n)]for j in range(n)]for i in range(n)]

def more_models():
 yield 'SO(11)_2',metaplectic(11),'odd_metaplectic',{'N':11},'Unitary SO(11) level2 category; standard odd metaplectic fusion rules'
 for a,R in [('Vec(C3)',group((3,))),('Ising',ty((2,))),('Rep(S3)',rep_dihedral(3)),('PSU(2)_5',su2(5,True))]:
  T=permutation_equivariant(R)
  if max(v for M in T for row in M for v in row)==1:yield '(('+a+') x ('+a+'))^C2_swap',T,'permutation_equivariant',{'base_name':a,'base_tensor':R},'Canonical swap C2-equivariantization of a Deligne square; unitary; Rep(S3) case equals Rep(S3 wr C2)'
 gs=[('C8',abelian_table((8,))),('C4xC2',abelian_table((4,2))),('C2^3',abelian_table((2,2,2))),('D8',dihedral_table(4)),('Q8',dicyclic_table(2)),('C3^2',abelian_table((3,3))),('C12',abelian_table((12,))),('C6xC2',abelian_table((6,2))),('D12',dihedral_table(6)),('Dic3',dicyclic_table(3)),('A4',a4_table()),('C14',abelian_table((14,))),('D14',dihedral_table(7)),('C15',abelian_table((15,))),('C17',abelian_table((17,)))]
 for name,G in gs:
  for sigma in auts(G):
   if not all(sigma[sigma[i]]==i for i in range(len(G))):continue
   f=sum(sigma[i]==i for i in range(len(G)));r=(len(G)+3*f)//2
   if r not in [9,10]:continue
   T=pointed_equivariant(G,sigma)
   if max(v for M in T for row in M for v in row)>1:continue
   yield f'Vec({name})^C2[{sigma}]',T,'pointed_equivariant',{'group_name':name,'group_table':G,'automorphism':sigma},'Canonical strict action by the displayed group automorphism on Vec(G); unitary C2-equivariantization'
 # Orthogonal involutions of TY(A,chi,tau) for A of order4.
 for orders in [(4,),(2,2)]:
  A=abelian_table(orders);R=ty(orders)
  for p in auts(A):
   if not all(p[p[i]]==i for i in range(4)):continue
   # C4 chi(a,b)=exp(2pi i ab/4); for V4 search nonsingular symmetric bilinear forms.
   if orders==(4,):chis=[[[i*j%4 for j in range(4)]for i in range(4)]];mod=4
   else:
    mod=2;chis=[]
    for a,b,c in itertools.product(range(2),repeat=3):
     if (a*c-b*b)%2!=1:continue
     chi=[[((i//2)*(j//2)*a+((i//2)*(j%2)+(i%2)*(j//2))*b+(i%2)*(j%2)*c)%2 for j in range(4)]for i in range(4)]
     chis.append(chi)
   for chi in chis:
    if not all(chi[p[i]][p[j]]==chi[i][j]for i,j in itertools.product(range(4),repeat=2)):continue
    T=crossed(R,p+[4]);name='x'.join('C'+str(x)for x in orders)
    yield f'TY({name}) crossed C2[{p}]',T,'ty_crossed',{'orders':orders,'automorphism':p,'bicharacter_exponents':chi,'modulus':mod},'An involutive automorphism preserving chi acts strictly on the standard TY skeleton; unitary crossed product'
    break

def run_extra():
 known=json.load(open(OUT/'known_models.json'));lookup={x['id']:x for x in known};by=collections.defaultdict(list)
 for n in [9,10]:
  for i,R in enumerate(read(n),1):by[(n,coarse(R))].append((f'R{n}_1_{i}',R))
 seen=set();extras=[]
 for name,M,kind,pars,ref in more_models():
  # Dedup constructed labeled tensors only to limit exact comparisons.
  h=tensor_hash(M)
  if h in seen:continue
  seen.add(h)
  for rid,R in by[(len(M),coarse(M))]:
   p=based_iso(R,M)
   if p is None:continue
   rec={'model':name,'constructor':kind,'parameters':pars,'reference':ref,'basis_map_source_to_model':p,'model_tensor':M}
   if rid not in lookup:lookup[rid]={'id':rid,'tensor_sha256':tensor_hash(R),'status':'unitarily_realized','models':[]};extras.append(rid)
   # Keep compact constructors per named family
   if not any(c['constructor']==kind and c['parameters'].get('group_name')==pars.get('group_name') for c in lookup[rid]['models']):lookup[rid]['models'].append(rec)
   print(rid,name,flush=True)
 known=sorted(lookup.values(),key=lambda x:tuple(map(int,x['id'].replace('R','').split('_'))))
 (OUT/'known_models_extended.json').write_text(json.dumps(known,indent=2)+'\n')
 print('NEW',extras,'TOTAL',collections.Counter(x['id'].split('_')[0]for x in known))
if __name__=='__main__':run_extra()

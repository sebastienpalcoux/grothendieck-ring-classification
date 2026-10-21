"""Independent constructions recovered and freshly reverified after workspace loss.

All tensors are constructed from categorical formulas or the preexisting
positive-model catalog, never copied from a new census tensor.
"""
from pathlib import Path
import itertools,json,math
from functools import lru_cache
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def require(v,m):
 if not v:raise ValueError(m)
def blank(n=8):return [[[0]*n for _ in range(n)]for _ in range(n)]
def product(A,B):
 a,b=len(A),len(B);R=blank(a*b)
 for i,j,k in itertools.product(range(a*b),repeat=3):R[i][j][k]=A[i//b][j//b][k//b]*B[i%b][j%b][k%b]
 return R

def e8_graph_ring():
 edges=[(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(4,7)];A=s.zeros(8)
 for i,j in edges:A[i,j]=A[j,i]=1
 powers=[s.eye(8)]
 for _ in range(7):powers.append(powers[-1]*A)
 K=s.Matrix.hstack(*(P[:,0]for P in powers));require(K.det()!=0,'E8 unit is cyclic')
 R=blank()
 for i in range(8):
  coeff=K.inv()[:,i];N=sum((coeff[j]*powers[j]for j in range(8)),s.zeros(8))
  require(N[:,0]==s.eye(8)[:,i],'E8 cyclic polynomial')
  require(all(v.is_Integer and v>=0 for v in N),'E8 fusion coefficients')
  R[i]=[[int(N[k,j])for k in range(8)]for j in range(8)]
 return R

def frobenius13():
 H={pow(4,i,13)for i in range(6)};O=[sorted(H),sorted(set(range(1,13))-H)];R=blank()
 for a,b in itertools.product(range(6),repeat=2):R[a][b][(a+b)%6]=1
 for a in range(6):
  for i in range(2):R[a][6+i][6+i]=R[6+i][a][6+i]=1
 for i,j in itertools.product(range(2),repeat=2):
  counts=[sum((a+b)%13==c for a in O[i]for b in O[j])for c in range(13)]
  require(counts[0]%6==0,'Frobenius zero orbit')
  for a in range(6):R[6+i][6+j][a]=counts[0]//6
  for k in range(2):
   require(len({counts[c]for c in O[k]})==1,'Frobenius orbit constant')
   R[6+i][6+j][6+k]=counts[O[k][0]]
 return R

def izumi_equivariant(epsilon):
 R=blank()
 for g,e,h,f in itertools.product(range(3),range(2),range(3),range(2)):R[2*g+e][2*h+f][2*((g+h)%3)+(e+f)%2]=1
 for g,e,f in itertools.product(range(3),range(2),range(2)):R[2*g+e][6+f][6+(e+f)%2]=R[6+f][2*g+e][6+(e+f)%2]=1
 for e,f in itertools.product(range(2),repeat=2):
  for g in range(3):R[6+e][6+f][2*g+(e+f+epsilon)%2]=1
  R[6+e][6+f][6]=R[6+e][6+f][7]=3
 return R

def izumi_xu():
 # Basis 1,g,g²,X,M,V,gV,g²V; CMS Appendix A.6.1.
 R=blank()
 for a,b in itertools.product(range(3),repeat=2):R[a][b][(a+b)%3]=1
 for a in range(3):
  for x in [3,4]:R[a][x][x]=R[x][a][x]=1
  for b in range(3):R[a][5+b][5+(a+b)%3]=1;R[5+b][a][5+(b-a)%3]=1
 for a in range(3):R[3][3][a]=R[4][4][a]=1
 R[3][3][3]=3
 for a in range(3):R[3][4][5+a]=R[4][3][5+a]=1
 for a in range(3):
  R[3][5+a][4]=R[5+a][3][4]=1
  for b in range(3):R[3][5+a][5+b]=R[5+a][3][5+b]=1
  R[4][5+a][3]=R[5+a][4][3]=1
 for a,b in itertools.product(range(3),repeat=2):R[5+a][5+b][(a-b)%3]=R[5+a][5+b][3]=1
 return R

def fibonacci_cyclic():
 bit=list(itertools.product(range(2),repeat=3));orbit1=[b for b in bit if sum(b)==1];orbit2=[b for b in bit if sum(b)==2]
 labels=[([(0,0,0)],e)for e in range(3)]+[([(1,1,1)],e)for e in range(3)]+[(orbit1,None),(orbit2,None)]
 F=[[[1,0],[0,1]],[[0,1],[1,1]]];R=blank()
 for i,(A,e) in enumerate(labels):
  for j,(B,f) in enumerate(labels):
   for k,(C,h) in enumerate(labels):
    c=C[0];n=sum(math.prod(F[a[t]][b[t]][c[t]]for t in range(3))for a in A for b in B)
    if len(C)>1:R[i][j][k]=n
    elif len(A)==len(B)==1:R[i][j][k]=n*int((e+f)%3==h)
    else:require(n%3==0,'C3 orbit character projection');R[i][j][k]=n//3
 return R

def tt3_morita():
 words=[(),(0,),(1,),(0,1),(1,0),(0,1,0)];index={w:i for i,w in enumerate(words)}
 @lru_cache(None)
 def reduce(w):
  if w in index:return tuple(int(i==index[w])for i in range(6))
  for j in range(len(w)-1):
   if w[j]==w[j+1]:
    a=reduce(w[:j]+w[j+2:]);b=reduce(w[:j]+w[j+1:]);return tuple(x+y for x,y in zip(a,b))
  if w==(1,0,1):return reduce((0,1,0))
  require(len(w)>=4,'TT3 word reduction')
  a=reduce(w[1:3]+w[4:]);b=reduce((0,1,0)+w[4:]);return tuple(x+y for x,y in zip(a,b))
 R=blank()
 for i,j in itertools.product(range(6),repeat=2):R[i][j][:6]=reduce(words[i]+words[j])
 F=s.Matrix([[0,1],[1,1]]);actions=[s.eye(2),F,F,F**2,F**2,F**3]
 for a,i,j in itertools.product(range(6),range(2),range(2)):
  v=int(actions[a][i,j]);R[a][6+i][6+j]=R[6+i][a][6+j]=R[6+i][6+j][a]=v
 return R

def tt3_gram():
 catalog=json.loads((ROOT/'supplements/rank8/data/model_catalog.json').read_text());row=next(r for r in catalog if r['id']=='R8_2_37');E=row['constructors'][0]['tensor'];odd=[1,3,5,7];A=[0,4]
 G=[[sum(E[a][w][t]*E[t][b][z]for a in A for b in A for t in range(8))for w in odd]for z in odd]
 require(G==[[1,1,3,3],[1,1,3,3],[3,3,13,13],[3,3,13,13]],'TT3 free-bimodule Gram matrix')
 partitions=sorted({tuple(v)for length in range(1,5)for v in itertools.combinations_with_replacement([1,2],length)if sum(x*x for x in v)==4})
 require(partitions==[(1,1,1,1),(2,)],'complete square-norm4 factorization')
 return dict(source='R8_2_37',source_model_basis='1,a,a²,a³,r,ar,a²r,a³r',algebra_basis=A,odd_basis=odd,free_bimodule_Gram=G,residual_square_norm=4,all_partitions_of_residual_norm=[[2],[1,1,1,1]],surviving_odd_dimensions=['2phi','2phi²'])

def g2_candidate(coeff):
 R=blank()
 for a,b in itertools.product(range(3),repeat=2):R[a][b][(a+b)%3]=1
 for a in range(3):
  for x in [3,4]:R[a][x][x]=R[x][a][x]=1
  for b in range(3):R[a][5+b][5+(a+b)%3]=1;R[5+b][a][5+(b-a)%3]=1
 for x in [3,4]:
  for a in range(3):R[x][x][a]=1
  R[x][x][x]=3
 for a in range(3):R[3][4][5+a]=R[4][3][5+a]=1
 for x in [3,4]:
  for a in range(3):
   R[x][5+a][7-x]=R[5+a][x][7-x]=1
   for b in range(3):R[x][5+a][5+b]=R[5+a][x][5+b]=1
 for a,b in itertools.product(range(3),repeat=2):
  R[5+a][5+b][(a-b)%3]=1;R[5+a][5+b][3]=R[5+a][5+b][4]=1
  for c in range(3):R[5+a][5+b][5+c]=coeff[(c-a+b)%3]
 return R

def g2_morita():
 candidates=[]
 for coeff in itertools.product(range(4),repeat=3):
  if sum(coeff)!=3:continue
  R=g2_candidate(coeff)
  if all(sum(R[i][j][a]*R[a][k][b]for a in range(8))==sum(R[j][k][a]*R[i][a][b]for a in range(8))for i,j,k,b in itertools.product(range(8),repeat=4)):candidates.append((coeff,R))
 require(len(candidates)==1 and candidates[0][0]==(1,1,1),'G2 exhaustive10-case associativity completion')
 return candidates[0][1]

def all_models():
 lower={r['name']:r for r in json.loads((ROOT/'supplements/rank8/data/lower_rank_positive_models.json').read_text())}
 fib=[[[1,0],[0,1]],[[0,1],[1,1]]];c2=[[[1,0],[0,1]],[[0,1],[1,0]]]
 E=e8_graph_ring();even=[[[E[i][j][k]for k in [0,2,4,6]]for j in [0,2,4,6]]for i in [0,2,4,6]]
 for ident,name,rank4,rank2 in [(331,'NG(C3,3) x Vec(C2)',lower['C3+3']['tensor'],c2),(471,'NG(C3,3) x Fibonacci',lower['C3+3']['tensor'],fib),(1456,'Ad(E8) x Vec(C2)',even,c2),(3314,'Ad(E8) x Fibonacci',even,fib)]:
  yield ident,name,product(rank4,rank2),'Existing unitary near-group or E8 model and Deligne product.',dict(kind='Deligne product',rank4_tensor=rank4,rank2_tensor=rank2)
 for ident,name,R,ref,extra in [
  (342,'Rep(C13 semidirect C6)',frobenius13(),'Faithful finite Frobenius group; exact orbit convolution.',{}),
  (3278,'E8 fusion category',E,'Kirillov–Ostrik arXiv:math/0101219v3; E8 module category; cyclic adjacency reconstruction.',{}),
  (274,'Phase-rotation C2 equivariantization of NG(C3,6)',izumi_equivariant(1),'Izumi arXiv:1512.04288v2, Lemma13.1, Example13.10 and paragraph before Lemma13.2.',{'epsilon':1,'omega':'i','u':'rotation pi/2'}),
  (334,'Reflection C2 equivariantization of NG(C3,6)',izumi_equivariant(0),'Izumi arXiv:1512.04288v2, Lemma13.1, Example13.10 and paragraph before Lemma13.2.',{'epsilon':0,'omega':'1','u':'diag(1,-1)'}),
  (448,'Unitary Izumi–Xu Z2 extension (2221)',izumi_xu(),'CMS Appendix A.6.1; Morrison–Penneys arXiv:1208.3637v2 §5.1 and Theorem5.5; GJS arXiv:1211.6414v2 Theorem4.9 and Remarks4.10–4.11.',{'proof':'IZUMI_XU_UNITARY_SCOPE.md'}),
  (475,'Cyclic permutation equivariantization of Fibonacci cubed',fibonacci_cyclic(),'Canonical strict C3 factor permutation and multiplicity-space averaging.',{'proof':'FIBONACCI_CYCLIC_PROOF.md'}),
  (715,'Morita dual of the nonsplit unitary 2D2 extension',tt3_morita(),'Grossman arXiv:1612.07185 Lemma4.1 and §4.1; Edie-Michell arXiv:1904.08909 Definition2.5.',{'free_bimodule_certificate':tt3_gram(),'proof':'TT3_MORITA_PROOF.md'}),
  (458,'Bimodules over the conformal G2_3 to E6_1 algebra',g2_morita(),'CMS Appendix A.4; DMNO arXiv:1009.2117v2 §3.3; Gui arXiv:1908.03484v3 Theorems2.21,2.28 and Corollary3.32.',{'proof':'G2_MORITA_PROOF.md'})]:yield ident,name,R,ref,extra

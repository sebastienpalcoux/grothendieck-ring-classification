"""Exact C3 level 4 conformal-module checks; numerical data only proposes N.
Every source fusion coefficient is independently certified by exact Weyl
character diagonalization over Q[z]/(z^16+1), z=exp(2*pi*i/32).
"""
from pathlib import Path
import json,itertools,hashlib,time
from flint import fmpq_poly,fmpq
P=Path(__file__).parent
x=fmpq_poly([0,1]);mod=x**16+1
def red(a):return a%mod
def mul(a,b):return red(a*b)
def pw(e):
 e%=32
 return x**e if e<16 else -(x**(e-16))
def inv(a):return a.xgcd(mod)[1]%mod
def div(a,b):return mul(a,inv(b))
def enc(a):return list(map(str,a.coeffs()))
def det3(a):return red(a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))
start=time.time();r=json.load(open(P/'probe_data.json'));weights=list(map(tuple,r['weights']));N=r['N'];rho=(3,2,1)
shifted=[tuple(sum(a[j:])+rho[j] for j in range(3)) for a in weights]
A=[[det3([[pw(2*a*b)-pw(-2*a*b) for b in t] for a in s]) for t in shifted] for s in shifted]
Ai=[inv(a) for a in A[0]];characters=[[mul(a,Ai[j]) for j,a in enumerate(row)] for row in A]
for i in range(35):
 for j in range(35):
  for c in range(35):
   if sum((characters[k][c]*N[i][j][k] for k in range(35) if N[i][j][k]),fmpq_poly([]))!=mul(characters[i][c],characters[j][c]):
    raise ValueError(('character equation',i,j,c))
d=[row[0] for row in characters]
# Enumerate all abelian upper ideals in C3 positive roots.
eye=[(1,0,0),(0,1,0),(0,0,1)]
add=lambda a,b:tuple(x+y for x,y in zip(a,b))
roots=set(tuple(2*t for t in e) for e in eye)
for i in range(3):
 for j in range(i+1,3):
  roots.add(add(eye[i],eye[j]));roots.add(add(eye[i],tuple(-t for t in eye[j])))
roots=sorted(roots);R=set(roots);ideals=[]
for mask in range(1<<9):
 I={a for i,a in enumerate(roots) if mask>>i&1}
 if any(add(a,b) in R-I for a in I for b in R):continue
 if any(add(a,b) in R for a in I for b in I):continue
 w=tuple(sum(a[i] for a in I) for i in range(3));dyn=(w[0]-w[1],w[1]-w[2],w[2]);ideals.append(dict(size=len(I),weight=dyn,roots=sorted(I)))
if len(ideals)!=8:raise ValueError('abelian ideals')
branch=[[0]*35 for a in range(3)]
for I in ideals:branch[I['size']%2][weights.index(I['weight'])]+=1
branch[2][weights.index((1,1,1))]=2
if [weights[i] for i,n in enumerate(branch[0]) if n] != [(0,0,0),(2,1,0),(0,0,4),(1,2,1)]:raise ValueError('vacuum branch')
even=[i for i,a in enumerate(weights) if (a[0]+a[2])%2==0];G=[[sum(branch[0][a]*N[i][a][j] for a in range(35)) for j in even] for i in even]
# Reconstruct restriction rows by Gram peeling. Distinguish local sigma using spinor branch.
col0=G[0];it=even.index(weights.index((0,1,0)));colt=G[it]
ip=even.index(weights.index((2,0,0)));colp=[G[ip][j]-colt[j] for j in range(19)]
ix=even.index(weights.index((0,0,2)));colx=[]
for j in range(19):
 if G[ix][j]%2:raise ValueError('fixed point multiplicity')
 colx.append(G[ix][j]//2)
# sigma coefficients = <lambda, underlying sigma> by adjunction.
cols=[col0,colx,colx,[branch[2][i] for i in even],colp,colt]
B=[list(v) for v in zip(*cols)]
if any(sum(B[i][a]*B[j][a] for a in range(6))!=G[i][j] for i in range(19) for j in range(19)):raise ValueError('Gram factor')
# Check known target makes induction a ring map on all even weights.
target=json.load(open(P/'target_R91.json'))
for i,a in enumerate(even):
 for j,b in enumerate(even):
  for c in range(6):
   left=sum(N[a][b][k]*B[l][c] for l,k in enumerate(even));right=sum(B[i][u]*B[j][v]*target[u][v][c] for u in range(6) for v in range(6))
   if left!=right:raise ValueError('tensor map')
# Ng--Schauenburg indicator formula for center C3_4 x Ising_21^rev.
theta=[pw(sum(a*a-b*b for a,b in zip(w,rho))) for w in shifted]
ds=[fmpq_poly([1]),fmpq_poly([1]),pw(4)+pw(-4)];tw=[fmpq_poly([1]),fmpq_poly([-1]),pw(42)]
DimA=sum((d[i]*branch[0][i] for i in range(35)),fmpq_poly([]));DimD=DimA*4
nu=[]
for mu in [0,weights.index((0,1,0)),weights.index((2,0,0)),weights.index((0,0,2)),weights.index((1,1,1))]:
 total=fmpq_poly([])
 for l in range(35):
  for a in range(3):
   m=sum(branch[a][v]*N[v][l][mu] for v in range(35))
   total+=mul(mul(mul(theta[l],theta[l]),inv(mul(tw[a],tw[a]))),mul(d[l],ds[a]))*m
 value=div(total,DimD);nu.append({'weight':weights[mu],'indicator':enc(value)})
expected=[[1],[1],[2],[],[]]
if [q['indicator'] for q in nu]!=[[str(v) for v in row] for row in expected]:raise ValueError(nu)
record={'field':'Q[z]/(z^16+1); z=exp(2*pi*i/32); coefficients ascending','source':'C3 level4','exact_character_equations':35**3,'abelian_ideals':ideals,'branching':branch,'even_weights':[weights[i] for i in even],'free_induction_matrix':B,'neutral_Gram':G,'algebra_dimension':enc(DimA),'neutral_dimension':enc(DimA*2),'full_module_dimension':enc(DimD),'free_second_indicators':nu,'R91_induction_homomorphism':True,'elapsed_seconds':time.time()-start,'source_data_sha256':hashlib.sha256((P/'probe_data.json').read_bytes()).hexdigest()}
json.dump(record,open(P/'exact_certificate.json','w'),indent=2);print({k:v for k,v in record.items() if k in ['exact_character_equations','free_second_indicators','elapsed_seconds','R91_induction_homomorphism']})
# Known rank-14 modularization E of the adjoint subcategory by J=004.
def J(w):
 j=weights.index((0,0,4));row=N[j][weights.index(w)]
 if sum(row)!=1:raise ValueError('J is not a simple current')
 return weights[row.index(1)]
seen=set();edims=[];orbits=[]
for i in even:
 w=weights[i]
 if w in seen:continue
 v=J(w);seen|={w,v};di=d[i]
 if v==w:edims.extend([di/2,di/2])
 else:edims.append(di)
 orbits.append({'weights':sorted([list(t) for t in {w,v}]),'split':v==w,'qdim':enc(di)})
if len(edims)!=14:raise ValueError('modularization rank')
centerdims=[mul(t,e) for t in ds for e in edims];D0=DimA*2
fplus=fmpq_poly([8])+ds[2]*4;fminus=fmpq_poly([8])-ds[2]*4
ratios=[div(D0,f) for f in [fplus,fminus]]
if any(u==v for u in ratios for v in centerdims):raise ValueError('unexpected formal codegree dimension')
if sum((mul(e,e) for e in edims),fmpq_poly([]))*4!=mul(D0,D0):raise ValueError('center global dimension')
record.update(modularization_orbits=orbits,modularization_rank=14,actual_center_rank=42,forbidden_selfdual_formal_codegrees=[enc(fplus),enc(fminus)],forbidden_induction_dimensions=[enc(u) for u in ratios],selfdual_outer_candidates_excluded_by_center_dimension=True)
# Exact witnesses used in the rank-six Gram argument.
if colp != [branch[1][i] for i in even]:raise ValueError('local fermion column')
if any(G[i][j]-sum(cols[a][i]*cols[a][j] for a in [0,3,4,5])!=2*colx[i]*colx[j] for i in range(19) for j in range(19)):raise ValueError('residual rank one')
record.update(Gram_rank_six_peeling={'known_local_columns':[0,3,4],'simple_free_column':5,'residual':'2 v v^t','v':colx,'distinguished_row':[0,0,2],'v_at_distinguished_row':colx[ix]})
json.dump(record,open(P/'exact_certificate.json','w'),indent=2)
print('Known center excludes outer selfdual candidates exactly')

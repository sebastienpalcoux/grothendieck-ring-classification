
if not __debug__:
    raise RuntimeError('Proof verification requires assertions enabled; run without -O.')
from pathlib import Path
import sys,json,itertools,time,math
import sympy as s
PACKAGE=Path(__file__).resolve().parents[1];ROOT=PACKAGE.parents[1];OUT=PACKAGE/'domain'
sys.path.insert(0,str(ROOT/'evidence/rank8_frontier_20261021/quadratic'))
from sextic_character_table import SexticTable,simple_data
R=json.load(open(ROOT/'site/dist/downloads/fusion-tensors/R8_3_3472.txt'))
if isinstance(R,dict): R=R['tensor']
T=SexticTable(R,simple_data(3472));K=T.K
Es=[i for i,b in enumerate(T.beta)if b==K(100)+K(70)*(T.ds[3]-K(7))/K(5)]
print('Es',Es,flush=True)
# Derive the induction Gram matrix directly from the source fusion tensor.
N=list(map(s.Matrix,R));B=sum((x*x.T for x in N),s.zeros(8))
u=s.Matrix([1]+[0]*7);p=s.Matrix([1]+[2]*7);Q=B-u*u.T-p*p.T
assert all(Q[:j,:j].det()>0 for j in range(1,9))
# All possible beta restrictions have v0=1, total nonunit multiplicity14,
# and rational part99. For group totals A (dimensions6+5r), C (8+5r),
# these equations give C=A+1 and v3=13-2A; A=0,...,6.
def comp3(n):
 return [(a,b,n-a-b)for a in range(n+1)for b in range(n-a+1)]
allV=[]
for a in range(7):
 for x in comp3(a):
  for y in comp3(a+1):allV.append((1,x[0],x[1],13-2*a,x[2],*y))
assert len(set(allV))==2142
adj=Q.adjugate();det=Q.det()
V=sorted(v for v in allV if (s.Matrix(v).T*adj*s.Matrix(v))[0]<=det);n=len(V)
assert n==96
# Preserve compatibility of existing index-based receipt after sorted generation.
assert V==[tuple(v)for v in json.load(open(OUT/'low_beta_fixed_pi_psd.json'))]
print('Source-derived dimensions and fixed-pi Gram retain',n,'of',len(allV),'vectors',flush=True)

A=Q.adjugate();d=int(Q.det());G=s.Matrix(V)*A*s.Matrix(V).T;G=[[int(z)for z in row]for row in G.tolist()]
vals=[[T.coordinates(sum((K(v[i])*T.characters[E][i]for i in range(8)),K.zero))for v in V]for E in Es]
compat={}
for E,F in itertools.combinations(range(6),2):
 C=[]
 for vi,v in enumerate(V):
  mask=0
  for wi,w in enumerate(V):
   if vals[F][vi]!=vals[E][wi]:continue
   if (d-G[vi][vi])*(d-G[wi][wi])<G[vi][wi]**2:continue
   if any(v[i]*v[j]+w[i]*w[j]>Q[i,j]for i in range(8)for j in range(i,8)):continue
   mask|=1<<wi
  C.append(mask)
 compat[E,F]=C
print('paircounts',{str(k):sum(m.bit_count()for m in v)for k,v in compat.items()},flush=True)
target=tuple(Q[0,:]);mins=[min(v[i]for v in V)for i in range(8)];maxs=[max(v[i]for v in V)for i in range(8)];sol=[];visits=[0]*7
allmask=(1<<n)-1
# Fixed variable order. Compatibility pair pruning and sum residual suffices before exact final PSD.
def walk(chosen,masks,total):
 E=len(chosen);visits[E]+=1
 if E==6:
  if total==target:sol.append(chosen)
  return
 mask=masks[E]
 while mask:
  bit=mask&-mask;mask-=bit;vi=bit.bit_length()-1;v=V[vi];newtotal=tuple(a+b for a,b in zip(total,v));left=5-E
  if any(not(newtotal[i]+left*mins[i]<=target[i]<=newtotal[i]+left*maxs[i])for i in range(8)):continue
  newmasks=masks[:];okay=True
  for F in range(E+1,6):
   newmasks[F]&=compat[E,F][vi]
   if not newmasks[F]:okay=False;break
  if okay:walk(chosen+[vi],newmasks,newtotal)
walk([],[allmask]*6,(0,)*8)
print('visits',visits,'sum+symmetry solutions',len(sol),flush=True)
PSD=[]
for ids in sol:
 W=s.Matrix([V[j]for j in ids]);res=Q-W.T*W
 if res.is_positive_semidefinite:PSD.append(ids)
print('PSD solutions',len(PSD),flush=True)
actual={'characters':Es,'vectors':V,'sum_symmetry_solutions':sol,'psd_solutions':PSD,'visits':visits}
assert json.loads(json.dumps(actual))==json.loads((OUT/'low_beta_assignments.json').read_text())
print('PASS complete 372 low frames')

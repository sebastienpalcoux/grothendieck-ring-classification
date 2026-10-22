"""Complete first relative-trace domain over Q(sqrt2,zeta7+).

Every root of unity whose order is supported on {2,5,7} has normalized
relative trace either zero or one of these 32 nonzero values. Orders with
v2>3, v5>1 or v7>1 have zero trace by cyclotomic tower transitivity.
Otherwise its order divides 280. We independently calculate all 280
averages in Q(zeta280), and identify their values in SexticTable's field.
"""

if not __debug__:
    raise RuntimeError('Proof verification requires assertions enabled; run without -O.')
import json,sys,math,hashlib
from pathlib import Path
from fractions import Fraction as Q
import sympy as sp
PACKAGE=Path(__file__).resolve().parents[1];ROOT=PACKAGE.parents[1];OUT=PACKAGE/'frames'
sys.path.insert(0,str(ROOT/'evidence/rank8_frontier_20261021/quadratic'))
from sextic_character_table import SexticTable,simple_data
R=json.loads((ROOT/'site/dist/downloads/fusion-tensors/R8_3_3472.txt').read_text());T=SexticTable(R,simple_data(3472));K=T.K
rad=(T.ds[1]-K(6))/K(5);u=K([1,0]);th=u-rad
# Direct 33 values in the sextic field, matching its maximal real embedding.
cosines=[K.one,th/K(2),(th*th-K(2))/K(2),(th**3-K(3)*th)/K(2)]
products={tuple(T.coordinates(K.zero)):K.zero}
for a in (K.one,-K.one,rad/K(2),-rad/K(2)):
 for b in cosines:
  for c in (K.one,-K.one/K(4)):
   z=a*b*c;products[tuple(T.coordinates(z))]=z
assert len(products)==33
# Independent exact computation in Q(zeta280), represented modulo Phi280.
N=280;x=sp.Symbol('x');poly=sp.Poly(sp.cyclotomic_poly(N,x),x);deg=poly.degree();assert deg==96
mod=[Q(int(poly.nth(i))) for i in range(deg)]
def reduce(v):
 v=list(v)
 for j in range(len(v)-1,deg-1,-1):
  if v[j]:
   q=v[j]
   for i,a in enumerate(mod):v[j-deg+i]-=q*a
 return tuple(v[:deg]+[Q(0)]*max(0,deg-len(v)))
zero=(Q(0),)*deg
powers=[reduce([Q(0)]*j+[Q(1)]) for j in range(N)]
def add(a,b):return tuple(q+r for q,r in zip(a,b))
def scale(a,q):return tuple(q*r for r in a)
def mul(a,b):
 out=[Q(0)]*(2*deg-1)
 for i,q in enumerate(a):
  if q:
   for j,r in enumerate(b):
    if r:out[i+j]+=q*r
 return reduce(out)
rc=add(powers[35],powers[-35]);tc=add(powers[40],powers[-40]);uc=add(rc,tc)
up=[powers[0]]
for j in range(1,6):up.append(mul(up[-1],uc))
def embed(z):
 out=zero
 for q,b in zip(T.coordinates(z),up):out=add(out,scale(b,q))
 return out
assert mul(rc,rc)==scale(powers[0],2)
assert embed(rad)==rc and embed(th)==tc
H=[a for a in range(N) if math.gcd(a,N)==1 and a%8 in (1,7) and a%7 in (1,6)]
assert len(H)==16
lookup={embed(z):coords for coords,z in products.items()}
assert len(lookup)==33
trace_to_exp={};exp_to_trace=[]
for j in range(N):
 out=zero
 for a in H:out=add(out,powers[(a*j)%N])
 out=scale(out,Q(1,len(H)))
 assert out in lookup,(j,out)
 cs=lookup[out];exp_to_trace.append(cs);trace_to_exp.setdefault(cs,[]).append(j)
assert set(trace_to_exp)==set(products)
# Every conjugate is a real average of roots, hence within [-1,1].
# Check all six real embeddings using the direct product description as well.
for a in [-1.0,1.0,-math.sqrt(2)/2,math.sqrt(2)/2]:
 for b in [1.0]+[math.cos(2*math.pi*j/7) for j in (1,2,3)]:
  for c in [1.0,-0.25]:assert abs(a*b*c)<=1+1e-15
atoms=sorted(products)
out={'field_polynomial':T.metadata['field_polynomial'],'primitive_generator':'u=sqrt(2)+2cos(2pi/7)',
 'basis':'1,u,u^2,u^3,u^4,u^5','sqrt2_coordinates':list(map(str,T.coordinates(rad))),
 'theta_coordinates':list(map(str,T.coordinates(th))),'trace_order_bound':280,
 'cyclotomic_degree':96,'fixed_subgroup':H,'subgroup_order':16,'atom_count':33,
 'atoms':[{'coordinates':list(map(str,cs)),'root_exponents':trace_to_exp[cs],
           'multiplicity_in_mu280':len(trace_to_exp[cs])} for cs in atoms],
 'complete_coverage':'For orders 2^a5^b7^c: trace zero if a>3 or b>1 or c>1; otherwise order divides280. This is a trace-compression bound, not a twist-order bound.',
 'universal_convex_coverage':'For an arbitrary root of unity of order 2^a7^c*m with gcd(m,14)=1, its normalized relative trace to this field vanishes if a>3 or c>1. Otherwise it is a*b*mu(m)/phi(m), where a is 0,+/-1,+/-sqrt2/2 and b is 1 or one of cos(2pi/7),cos(4pi/7),cos(6pi/7). Since mu(m)/phi(m) lies in [-1,1], this trace is a convex combination of two opposite base atoms among these33. Consequently the nonnegative real phase-mass LP is a necessary relaxation for arbitrary twist orders, without a Cauchy prime restriction.',
 'verification':'All280 normalized relative traces calculated exactly moduloPhi280 and matched to sextic-field elements;33 distinct values.',
 'tensor_sha256':hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()}
assert out==json.loads((OUT/'first_trace_atoms.json').read_text())
print('PASS:33exactatoms; all280roots; subgroup16; degree96; sexticembeddingmatched')

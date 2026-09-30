from pathlib import Path
import json,sympy as s,hashlib,collections
P=Path(__file__).parent
def require(value,message):
 if not value:raise ValueError(message)
x=s.symbols('x');phi=s.Poly(s.cyclotomic_poly(60,x),x,domain=s.QQ)
def red(f):return s.rem(s.Poly(f,x,domain=s.QQ),phi).as_expr()
def mul(a,b):return red(a*b)
def inv(a):return s.invert(a,phi.as_expr(),x)
def power(n):return red(x**(n%60))
def qs(n):return red(power(n)-power(-n))
den=mul(mul(qs(1),qs(2)),mul(qs(3),qs(4)));di=inv(den)
def qdim(a,b):return mul(mul(mul(qs(2*a+2),qs(b+1)),mul(qs(2*a+b+3),qs(2*a+2*b+4))),di)
def enc(f):return [str(z) for z in s.Poly(f,x).all_coeffs()]
def eval15(seq):return red(sum(s.Rational(v)*power(4*(len(seq)-i-1)) for i,v in enumerate(seq)))
embedding_weights=[(0,0,1),(0,6,1),(1,8,1),(3,2,1),(3,8,1),(4,4,2),(6,6,1),(7,2,1),(12,0,1)]
D=red(sum(m*qdim(a,b) for a,b,m in embedding_weights)/2)
weights=[(a,b) for b in range(0,13,2) for a in range(13-b)]
seen=set();dims=[];orbits=[]
for a,b in weights:
 if (a,b) in seen:continue
 twin=(12-a-b,b);seen|={(a,b),twin};d=qdim(a,b)
 if twin==(a,b):ds=[red(d/2)]*2
 else:ds=[d]
 dims+=ds;orbits.append(dict(weight=[a,b],orbit=sorted([list(t) for t in {(a,b),twin}]),dimension=enc(d),local_dimensions=[enc(v) for v in ds]))
require(len(dims)==35,'Wrong center rank')
require(red(sum(mul(d,d) for d in dims)-mul(D,D))==0,'Center global dimension mismatch')
require(all(red(d-D/3)!=0 and red(d-D/15)!=0 for d in dims),'Forbidden codegree dimensions appear')
invertibles=[(a,b) for b in range(13) for a in range(13-b) if qdim(a,b)==1]
require(invertibles==[(0,0),(12,0)],'Unexpected invertible objects')
record=dict(check='Known B2 level12 adjoint modularization dimension spectrum',field='Q[x]/Phi_60(x); x=exp(pi i/30)',rank=35,neutral_weights=49,simple_current=[12,0],orbit_map='(a,b)->(12-a-b,b)',fixed_points=7,ordinary_orbits=21,original_ring_dimension=enc(D),known_center_global_dimension_equals_D_squared=True,formal_codegree3_impossible=True,formal_codegree15_impossible=True,orbits=orbits)
json.dump(record,open(P/'center_dimension_certificate.json','w'),indent=2)
print({k:v for k,v in record.items() if k!='orbits'})

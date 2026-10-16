def _require(condition, message):
    if not condition:
        raise RuntimeError(message)

from itertools import product, permutations
import json
from pathlib import Path
import sympy as s

a,b,c,d,e,f,g,h,i,j=s.symbols('a b c d e f g h i j')
N=[[[s.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
for p,q in product(range(4),repeat=2):
    N[0][p][q]=N[p][0][q]=s.Integer(p==q)
    N[p][q][0]=s.Integer(p==q)
for triple,v in zip([(1,1,1),(1,1,2),(1,1,3),(1,2,2),(1,2,3),(1,3,3),(2,2,2),(2,2,3),(2,3,3),(3,3,3)],(a,b,c,d,e,f,g,h,i,j)):
    for p,q,r in set(permutations(triple)): N[p][q][r]=v
A=[]
for p,q,r,t in product(range(4),repeat=4):
    v=s.expand(sum(N[p][q][k]*N[k][r][t]-N[q][r][k]*N[p][k][t] for k in range(4)))
    if v and v not in A and -v not in A: A.append(v)
# In the exceptional absolute-rigidity branch, simultaneous e/-e associativity
# is equivalent (over the e != 0 locus) to exactly the seven stated relations.
rels=[a-d-f,g-b-i,j-c-h,b*h+c*i-b*c,d*h-c*d-f*h,b*f+d*i-f*i,e**2-1-d*f-b*i-c*h]
G=s.groebner(rels,a,g,j,b,c,d,e,f,h,i)
_require(all(G.reduce(v)[1]==0 and G.reduce(v.subs(e,-e))[1]==0 for v in A), 'structural_algebra.py exact check at source line 21')
# Conversely the three linear relations follow from e-odd parts; after their
# substitution the e-even parts generate the four stated residual relations.
odd=[s.expand((v-v.subs(e,-e))/(2*e)) for v in A]
Godd=s.groebner([x for x in odd if x],a,g,j,b,c,d,f,h,i)
_require(all(Godd.reduce(v)[1]==0 for v in rels[:3]), 'structural_algebra.py exact check at source line 26')
sub={a:d+f,g:b+i,j:c+h}
remaining=[s.expand(v.subs(sub)) for v in A]
Gr=s.groebner(remaining,b,c,d,e,f,h,i)
_require(all(Gr.reduce(v)[1]==0 for v in rels[3:]), 'structural_algebra.py exact check at source line 30')
# Fourier-array inequality is an identity for arbitrary additive arrays.
AA=s.symbols('A0:8'); BB=s.symbols('B0:5')
r=lambda p,q: AA[p]+BB[q]
lhs=sum(r(p,q) for p,q in product(range(8),range(5)))-5*r(0,0)-3*r(4,0)
rhs=s.Rational(1,2)*sum(r(4,q) for q in range(1,5))+s.Rational(5,4)*sum(r(p,q) for p in range(8) if p not in (0,4) for q in range(1,5))
_require(s.expand(lhs-rhs)==0, 'structural_algebra.py exact check at source line 36')
# Mixed rational-row fixed-invertible formulas, including integrality obstruction.
u=s.symbols('u')
red=lambda x:s.rem(s.expand(x),u*u-(2*b-1)*u-2*b-2,u)
E=2+u*u+(u+2)**2
Ep=E.subs(u,2*b-1-u)
_require(red(E-(4*b+10+(4*b+2)*u))==0, 'structural_algebra.py exact check at source line 42')
_require(red(E*Ep-8*(4*b*b+4*b+9))==0, 'structural_algebra.py exact check at source line 43')
# Near-group and h=3 norm formulas are exact, including constant-codegree cases.
m,v=s.symbols('m v')
for n in (3,6):
    Ev=n+v*v
    Evp=Ev.subs(v,m-v)
    rr=lambda x:s.rem(s.expand(x),v*v-m*v-n,v)
    _require(rr(Ev+Evp-(m*m+4*n))==0, 'structural_algebra.py exact check at source line 50')
    _require(rr(Ev*Evp-n*(m*m+4*n))==0, 'structural_algebra.py exact check at source line 51')
# Finite trace/discriminant subchart in the fixed-invertible proof.
rows=[]
for k in (1,2,3):
    for T in range(k+2,8):
        disc=T*T-4*k; n=disc; v3=0
        while n%3==0: n//=3; v3+=1
        if v3%2: rows.append((k,T))
_require(rows==[(1,4),(1,5),(3,6)], 'structural_algebra.py exact check at source line 59')
# Non-self-dual repeated-codegree reductions.
for gg,expected in ((3,{(-1,0),(1,0)}),(4,{(0,-1),(0,1)}),(5,set())):
    actual={(aa,tt) for aa in range(-3,4) for tt in range(-3,4) if 2+aa*aa+2*tt*tt==gg and (1+aa*aa+tt*tt)%2==0}
    _require(actual==expected, 'structural_algebra.py exact check at source line 63')
result={'status':'PASS','independent_associativity_polynomials':len(A),'absolute_rigidity_exceptional_relations':True,'fortieth_root_additive_array_identity':True,'fixed_invertible_mixed_row_norm':True,'near_group_and_fixed_row_norms':True,'fixed_invertible_discriminant_chart':rows,'nonselfdual_small_codegree_rows':True,'scope':'Algebraic identities only; categorical steps reviewed in structural.md.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

"""Independent exact arithmetic checks for rank-four §§9–10.

These checks supplement, and do not replace, the categorical and inequality
audit in cubic_pivotal.md. No input census or supplied checker is imported.
"""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sympy as s
from paths import repository_root
ROOT=repository_root()

checks = []
def need(condition, name):
    if not condition:
        raise RuntimeError(name)
    checks.append(name)

z, n, t, a, c, p, j = s.symbols('z n t a c p j')
need(s.factor(s.discriminant(z**3-(n+1)*z**2+2*n*z-n,z)) == n*(n-4),
     'Schur boundary cubic discriminant')
need(s.factor(s.discriminant(z**3-n*z**2+2*n*z-n,z)) == n*n*(4*n-27),
     'conductor-nine cubic discriminant')
N = [[[s.Integer(0) for k in range(4)] for jj in range(4)] for i in range(4)]
for i in range(4):
    N[0][i][i] = N[i][0][i] = 1
for i in range(1,4):
    N[i][i][0] = 1
from itertools import permutations
for ijk, value in [((1,1,1),a),((1,1,2),a),((1,1,3),c),
                  ((1,2,2),a+1),((1,2,3),c),((1,3,3),p),
                  ((2,2,2),a+1),((2,2,3),c),((2,3,3),p+1),
                  ((3,3,3),j)]:
    for i,jj,k in set(permutations(ijk)):
        N[i][jj][k] = value
casimir_trace = s.expand(sum(N[i][jj][k]**2 for i in range(4)
                             for jj in range(4) for k in range(4)))
need(s.expand(casimir_trace-(17+8*a*(a+1)+6*p*(p+1)+12*c*c+j*j)) == 0,
     'cubic normal-form Casimir trace')
assoc = s.expand(sum(N[3][3][q]*N[1][q][1]-N[1][3][q]*N[q][3][1]
                     for q in range(4)))
need(s.expand(assoc-(1+a*(2*p+1)+c*j-2*c*c-p*p)) == 0,
     'cubic normal-form associativity equation')
sol = [(aa,cc,pp,jj) for aa in range(3) for cc in range(3)
       for pp in range(3) for jj in range(5)
       if 17+8*aa*(aa+1)+6*pp*(pp+1)+12*cc*cc+jj*jj == 30]
need(sol == [(0,0,1,1),(0,1,0,1)], 'Casimir-trace-30 nonnegative solutions')
need([int((z**3+z*z-2*z-1).subs(z,k)) % 3 for k in range(3)] == [2,2,1],
     'conductor-seven defining polynomial inert modulo three')
need(Q(43008)*Q(187,1344)/3 > 1900,
     'trace-gap threshold implies largest codegree exceeds 1900')
need(Q(1,1008)-Q(1,1140)>0, 'conductor-seven reciprocal-root interval')
need(Q(9,400)-Q(1,336)-Q(9,500)>0, 'conductor-seven sharper reciprocal interval')
need(Q(7910,47)<169, 'conductor-seven s at most twelve')
need(Q(47*49,21)<110<Q(9*49,4) and 110 % 4 != 3,
     'conductor-seven final integer contradiction')

D=t*t
alpha=2-4/t
w=1/D**2+(1-1/D)**2/3
L0=t*t-Q(91,3)+64/t-Q(40,3)/t**2-64/t**3+Q(128,3)/t**4
need(s.expand(2*(alpha+1)**2*(D*w-1)-(1+alpha**2)*(D-1)-L0)==0,
     'centered lower-bound L0 identity')
need(Q(471,100)**2*2<Q(20,3)**2,
     'g(B) square-root coefficient bound')
need(Q(2007,1000)>2+Q(602,100)/1000,
     'g(B) quartic coefficient bound')
need(Q(71,100)*Q(1003,1000)<Q(18,25),
     'g(B) B^(3/2) coefficient bound')

# Independent rational endpoint lower bounds, with non-assert failure semantics.
T=Q(158,5); rtlo=Q(28,5); rthi=Q(45,8); b=Q(301,100)
rows=[(Q(18,5),Q(0),Q(0),Q(2683,1000),Q(671,250),Q(6831,1000),Q(1,2),Q(19,10)),
      (Q(10,3),Q(1,1000),Q(4,25),Q(2581,1000),Q(1291,500),Q(3043,500),Q(5,2),Q(5,2)),
      (Q(5,2),Q(1,250),Q(8,25),Q(559,250),Q(2237,1000),Q(3953,1000),Q(12),Q(4))]
receipts=[]
for e,v,jj,rlo,rhi,hhi,valfloor,derfloor in rows:
    need(rlo*rlo < 2*e < rhi*rhi and hhi*hhi>e**3,
         f'endpoint radicals at e={e}')
    A=2*e-4; Caux=(Q(471,100)+jj)*rhi
    C0=11-Q(91,3)-b+2*e-Q(3,2)*e*e+32*v
    C1=8*rlo-(Q(71213,100000)+Q(1003,1000)*jj)*hhi
    C2=64+(2*b-3)*e-(e if v==0 else 0)
    C3=Q(40,3)+Q(1,2)+Q(3,2)*b*e*e
    C4=-64+b*e; C5=Q(128,3)-b/2
    value=18*v*T*T+(A-48*v)*T-Caux*rthi+C0+C1/rthi+C2/T-C3/T**2+C4/T**3+C5/T**4
    derivative=36*v*T+A-48*v-Caux/(2*rtlo)-C1/(2*T*rtlo)-C2/T**2-4*C5/T**5
    need(value>valfloor and derivative>derfloor, f'concentration endpoint e={e}')
    receipts.append(dict(e=str(e), value_lower=str(value), derivative_lower=str(derivative)))

m=Q(333,1000)
for V,c0,P0,p0,H0 in [(Q(1,1000),Q(41,200),Q(1,6),Q(147,4000),Q(327,250)),
                       (Q(1,250),Q(27,100),Q(7,40),Q(181,5000),Q(53,50))]:
    R=54*P0-c0*(9-5*c0*c0)
    need(R>0 and R*R>2*(3-c0*c0)**3, f'cubic-product radical bound V={V}')
    need(H0*P0*P0/p0<1, f'determinant exact bound V={V}')
need(Q(12,25)/(27*Q(17,500))==Q(80,153)<1,
     'third variance determinant bound')
need(Q(1,32)-Q(4,576)==Q(7,288)>Q(1,48),
     'exceptional pivotal-character contradiction at D=576')
sources=['manuscripts/rank4/papers/companion_sections/09_cubic.tex',
         'manuscripts/rank4/papers/companion_sections/10_pivotal_bound.tex']
result={'status':'PASS','source_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in sources},
        'checks':checks,'rational_endpoints':receipts,
        'scope':'Exact arithmetic supplements a mathematical audit; no formal categorical verification.'}
out=Path(__file__).with_suffix('.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'checks':len(checks),'receipt':str(out)}))

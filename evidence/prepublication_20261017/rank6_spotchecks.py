#!/usr/bin/env python3
"""Fresh small arithmetic checks, independent of the publication replayers."""
import json
from fractions import Fraction as F
from pathlib import Path
import sympy as s
root=Path(__file__).resolve().parents[2]
q2,q3=s.sqrt(2),s.sqrt(3)
d=3+2*q2+2*q3+s.sqrt(6)
dims=[1,1,d,d,q2,s.expand(q2*d)]
D=s.expand(sum(a*a for a in dims))
Di=(6-2*q3-s.sqrt(6))/48
assert s.simplify(D*Di)==1
weights3=[];weights6=[]
for a in dims:
    x=s.expand(a*Di)
    weights3.append(int(s.expand(x).coeff(q3)*24))
    weights6.append(int(s.expand(x).coeff(s.sqrt(6))*48))
assert weights3==[-1,-1,1,1,-1,-1]
assert weights6==[-1,-1,-1,-1,-2,2]
a,u,z=s.symbols('a u z')
restriction=s.expand((u+a*q2)*d+z*q2)
x=s.expand(restriction*Di)
assert s.solve([x.coeff(q3),x.coeff(s.sqrt(6))],[a,u])=={a:3*z,u:4*z}
N=next(r['N'] for r in json.loads((root/'supplements/rank6/data/unresolved_tensors.json').read_text()) if r['id']=='R6_8_1660')
def unit_in_power(i,n):
    v=[1,0,0,0,0,0]
    for _ in range(n):
        v=[sum(v[j]*N[i][j][k] for j in range(6)) for k in range(6)]
    return v[0]
homs={n:[unit_in_power(i,n) for i in [2,5]] for n in [3,5,7]}
assert homs=={3:[3,8],5:[402,2272],7:[55401,626784]}
# Represent a+b*omega+c*omega**2 by (a-c,b-c), using omega**2=-1-omega.
possible={(a-c,b-c) for a in range(4) for b in range(4-a) for c in [3-a-b]}
assert (2,1) in possible and (1,-1) in possible
assert (3,3) not in possible and (0,-3) not in possible
p=[F(1,12),F(1,24),F(1,6),F(1,12),F(1,12),F(1,24),F(1,6),F(1,12),F(1,12),F(1,24),F(1,12),F(1,24)]
q=[15,3,-1,-1,-1,-1,-1,-1,15,3,-1,-1]
assert sum(p)==1 and sum(x*y for x,y in zip(p,q))==2
coefficient=(sum(x*y for x,y in zip(p,q))-1)/2
assert coefficient==F(1,2)
# The R'(m) norm-ratio argument uses these exact polynomial norm identities.
r,m=s.symbols('r m')
assert s.expand((8+r*r)**2-r*r*(r*r+8))==8*(r*r+8)
assert s.expand((8+4*m*m)**2-4*m*m*(4*m*m+8))==8*(4*m*m+8)
out={'dimension':str(D),'weights3':weights3,'weights6':weights6,'twist_one_restriction_constraints':'a=3z, b+c=4z','invariant_dimensions_X_T':homs,'third_rotation_spectrum_choices':len(possible),'Verlinde_probabilities_sum':str(sum(p)),'Verlinde_visible_expectation':str(sum(x*y for x,y in zip(p,q))),'Verlinde_diagonal_coefficient':str(coefficient),'scope':'Independent arithmetic checks only; categorical premises reviewed separately; no categorification claimed.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

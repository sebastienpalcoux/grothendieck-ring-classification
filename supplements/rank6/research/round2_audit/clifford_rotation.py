"""Exact universal Cl_3 algebra identities for the stabilizer criterion.

Generators e0,e1,e2 square to 1 and anticommute. Monomials are encoded
by increasing-index bitmasks. All coefficients are rational.
"""
from fractions import Fraction as Q
import json
from pathlib import Path

def plus(*xs):
    out={}
    for x in xs:
        for k,v in x.items():out[k]=out.get(k,Q(0))+v
    return {k:v for k,v in out.items() if v}

def scale(x,c):return {k:v*c for k,v in x.items() if v*c}

def mul(x,y):
    terms=[]
    for a,va in x.items():
        for b,vb in y.items():
            inversions=sum(1 for i in range(3) for j in range(3)
                           if (a>>i)&1 and (b>>j)&1 and i>j)
            terms.append({a^b:va*vb*((-1)**inversions)})
    return plus(*terms)

def need(ok,msg):
    if not ok:raise ArithmeticError(msg)

one={0:Q(1)}; e=[{1<<i:Q(1)} for i in range(3)]
U=scale(plus(scale(one,-1),mul(e[0],e[1]),mul(e[1],e[2]),mul(e[2],e[0])),Q(1,2))
need(mul(mul(U,U),U)==one,'U cube is not one')
for i in range(3):
    need(mul(U,e[i])==mul(e[(i+1)%3],U),'wrong cycle intertwiner')
need(U.get(0)==Q(-1,2),'wrong scalar coefficient and 2D-simple trace')

out={'clifford_generators':3,'generator_squares':1,
     'U_in_increasing_monomial_basis':{str(k):str(v) for k,v in U.items()},
     'U_cubed_is_one':True,'U_cycles_generators':True,
     'trace_on_each_two_dimensional_simple':-1,
     'rational_third_indicator_values':{
         str(n):[-n//2+3*b for b in range(n//4+1)] for n in range(2,17,2)},
     'scope':'requires anticommuting order-two stabilizer; rationality additionally requires 3 coprime to FS exponent'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

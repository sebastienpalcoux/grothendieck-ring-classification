#!/usr/bin/env python3
"""Exact arithmetic checks supporting MORITA_REDUCTION.md; not an exclusion."""
from fractions import Fraction as Q
from pathlib import Path
import json

triples=[(a,b,c) for a in range(5) for b in range(3) for c in range(3) if a+2*b+2*c==4]
canonical=sorted({(a,max(b,c),min(b,c)) for a,b,c in triples})
assert canonical==[(0,1,1),(0,2,0),(2,1,0),(4,0,0)]
assert [tau for tau in range(1,5) if tau*tau%5==1]==[1,4]
assert all((i+2)%5!=i for i in range(5))

# Q(sqrt5), represented as pairs.  Norm the quadratic in y.
def mul(a,b):return (a[0]*b[0]+5*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def norm_quadratic(t):
 u=mul(t,t);u=(u[0]+4,u[1])
 p=[(1,0),(-u[0],-u[1]),u]
 out=[(Q(0),Q(0)) for _ in range(5)]
 for i,a in enumerate(p):
  for j,b in enumerate(p):
   v=mul(a,(b[0],-b[1]));s=out[i+j];out[i+j]=(s[0]+v[0],s[1]+v[1])
 assert all(b==0 and a.denominator==1 for a,b in out)
 return [int(a) for a,b in out]
records=[]
for triple,t,expected in [((2,1,0),(Q(3,2),Q(1,2)),[1,-15,60,-90,45]),((0,2,0),(Q(-1),Q(1)),[1,-20,100,-160,80])]:
 coeff=norm_quadratic(t)
 assert coeff==expected
 assert coeff[0]%5 and all(a%5==0 for a in coeff[1:]) and coeff[-1]%25
 records.append({'triple':triple,'formal_codegree_divided_by_5_minimal_polynomial':coeff,'Eisenstein_prime':5,'degree':4})
receipt={'id':'R10_1_189','status':'verified arithmetic for necessary Morita based-ring self-duality; categorifiability unresolved','all_normalized_triples':triples,'four_isomorphism_types':canonical,'quartic_exclusions':records}
Path(__file__).with_name('morita_reduction_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: four candidate rings, two quartic formal-codegree polynomials, Eisenstein5. No classification decision.')

"""Rank-six commutative descent for signed sphericalization quotients.

The returned witness rules out C^2 + M_2(C) as the signed algebra;
see Theorem 3.2 of the manuscript. It is not itself a nonexistence result.
"""
from rings import *
import math
def certificate(R):
    n=len(R)
    if n<=5:return {'kind':'rank_at_most_five'}
    require(n==6,'rank-six descent only')
    if dual(R)==list(range(n)):return {'kind':'self_dual'}
    if sum(i==j for i,j in enumerate(dual(R)))==2:return {'kind':'duality_trace','fixed_basis_elements':2}
    for f,m in codegree_factors(R):
        if f.degree()>2:return {'kind':'codegree_field_degree','factor':pc(f)}
    p=codegree_poly(R);mu=next((j for j,a in enumerate(reversed(p.all_coeffs())) if int(a)%2),n)
    if mu<4:return {'kind':'mod_two_casimir','zero_multiplicity':mu,'polynomial':pc(p)}
    # A noncommutative signed quotient has dimension character field of degree
    # at most two. Two different quadratic subfields cannot both lie in it.
    quadratic=[]
    for f,m in codegree_factors(R):
        if f.degree()!=2:continue
        disc=int(s.discriminant(f));sf=math.prod(int(p) for p,e in s.factorint(disc).items() if e%2)
        quadratic.append((sf,pc(f)))
    for a in quadratic:
        for b in quadratic:
            if a[0]!=b[0]:return {'kind':'distinct_quadratic_fields','factors':[a[1],b[1]]}
    return None

def verify(R,c):require(certificate(R)==c,'invalid commutative descent witness')

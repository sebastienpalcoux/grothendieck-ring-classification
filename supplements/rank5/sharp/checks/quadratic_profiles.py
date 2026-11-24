"""Exact quadratic profile test for perfect rank-five rings when all d_i>2.

There is no input cutoff on dimension or on fusion coefficients.
A pair (a,b) represents (a+b sqrt(c))/2.
"""

if not __debug__:
    raise RuntimeError("Run this verifier with Python assertions enabled")

from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations_with_replacement
from math import gcd, isqrt, lcm


def at_most_radical(x, y):
    """Compare x <= sqrt(y), with rational x and nonnegative rational y."""
    return x <= 0 or x*x <= y


def fundamental(c):
    if c % 4 == 1:
        r = c
    elif c % 4 == 0 and c//4 % 4 in (2, 3):
        r = c//4
    else:
        return False
    return r >= 2 and all(r % (p*p) for p in range(2, isqrt(r)+1))


def rational_profiles():
    for c in range(5,38):  # (4c/21-1)^2 <= c if 4c/21 >= 1
        k = Q(1,c)
        if not fundamental(c) or not at_most_radical(Q(4,21)-k, k):
            continue
        for f in range(3,10):
            if not at_most_radical(1-Q(5,f), k):
                break
            for g in range(f,19):
                if not at_most_radical(1-Q(1,f)-Q(4,g), k):
                    break
                base = 1-Q(1,f)-Q(1,g)
                if at_most_radical(base, k):
                    assert (c,f,g) in ((5,3,3), (5,3,4), (8,3,3))
                    continue  # inert prime three, as proved in the text
                h = g
                while at_most_radical(base-Q(3,h), k):
                    mass = base-Q(1,h)
                    if mass >= Q(4,21):
                        yield c, (f,g,h), None, mass, mass*mass-k
                    h += 1


def mixed_profiles():
    for c in (5,8,12,13):
        for n in range(1,3778):  # sqrt(n) <= 30+sqrt(990)
            for h in range(2*c,n,c):
                if h*h % n:
                    continue
                disc = h*h-4*n
                if disc <= 0 or disc % c:
                    continue
                b = isqrt(disc//c)
                if c*b*b != disc or (h-2)**2 <= disc:
                    continue
                w = Q(h,n)
                radius = Q(1,c)-Q(disc,n*n)
                if radius < 0:
                    continue
                assert not at_most_radical(1-w, radius)
                g = 3
                while at_most_radical(1-w-Q(3,g), radius):
                    v = 1-w-Q(1,g)
                    if v > 0 and (c,g) != (5,3):
                        yield c, (g,), (h,b,n), v, v*v-radius
                    g += 1


def plus_positive(a,b,c):
    if b < 0:
        return a > 0 and a*a > c*b*b
    return a > 0 or (b > 0 and a*a < c*b*b)


def records(profile):
    c, gs, H, mass, delta = profile
    a, d = mass.as_integer_ratio()
    modulus = lcm(lcm(*gs)**2, c*d//gcd(a,c*d), H[2] if H else 1)
    for N in range(modulus, int(4/delta)+1, modulus):
        A = N*a//d
        if A < 4*c or A*A % N:
            continue
        disc = A*A-4*N
        if disc <= 0 or disc % c:
            continue
        B = isqrt(disc//c)
        if c*B*B != disc or (A-2)**2 <= disc or not plus_positive(A-34,B,c):
            continue
        if any(A%g or B%g or ((A//g)**2-c*(B//g)**2)%4 for g in gs):
            continue
        if H:
            h,b,n = H
            if (A*h+c*B*b)%(2*n) or (A*h-c*B*b)%(2*n):
                continue
        yield c,(A,B,N),gs,H


def dimension_vectors(c,D):
    A,B,N = D
    acap, bcap = isqrt(A-4), isqrt(A//c)
    coords = [(a,b) for a in range(-acap,acap+1)
              for b in range(-bcap,bcap+1) if b and (a*a-c*b*b)%4==0
              and plus_positive(a-4,b,c)]
    parts = defaultdict(list)
    for u,v in combinations_with_replacement(coords,2):
        a,b = u
        e,f = v
        x,y,z = a*a+e*e, b*b+f*f, a*b+e*f
        if x <= A-4 and y <= A//c-2:
            parts[x,y,z].append((u,v))
    for (x,y,z), left in parts.items():
        right = parts.get((A-4-x,A//c-y,B-z), ())
        for u,v in left:
            for w,t in right:
                if v <= w:
                    yield u,v,w,t


def excluded_by_rows(c,gs):
    if gs.count(4) >= 2:
        return True
    if gs[:2] == (3,3):
        h = gs[2]
        return h % 3 != 0 or not any(3+3*u*u+v*v==h
            for u in range(1,isqrt(h//3)+1) for v in range(1,isqrt(h)+1))
    return c == 8 and gs == (3,4,16)


def verify():
    profiles = [*rational_profiles(),*mixed_profiles()]
    sizes = Counter((bool(H),delta<=0) for c,gs,H,v,delta in profiles)
    assert sizes == {(False,False):1299,(False,True):162,(True,False):614,(True,True):6}
    active = [p for p in profiles if p[-1] > 0]
    possible = [r for p in active for r in records(p)]
    assert len(possible)==16 and all(H is None for c,D,gs,H in possible)
    finite = [(c,D,gs) for c,D,gs,H in possible if not excluded_by_rows(c,gs)]
    assert len(finite)==5 and all(not list(dimension_vectors(c,D)) for c,D,gs in finite)
    limit = [(c,gs,H) for c,gs,H,v,delta in profiles if delta<=0]
    assert [(c,gs,H) for c,gs,H in limit if H] == [
        *((5,(g,),(10,2,20)) for g in range(4,9)), (5,(4,),(15,3,45))]
    assert [(c,gs) for c,gs,H in limit if not H and
            any(g>=7 and gs.count(g)>=2 for g in gs)] == [
        (5,(3,7,7)),(5,(3,8,8)),(5,(3,9,9))]
    candidates = [(k, isqrt(k*(125*k-48))) for k in range(1,65)
                  if isqrt(k*(125*k-48))**2 == k*(125*k-48)]
    assert candidates == [(12,132)]
    ds = list(dimension_vectors(5,(300,132,720)))
    assert ds == [((4,2),(6,2),(10,4),(12,6))]
    # D/4 has coordinates (75,33), while every lattice generator has even coordinates.
    assert all(a%2==b%2==0 for a,b in ((2,0),*ds[0]))
    print('Finite profiles: 1299 rational, 614 mixed. Limiting profiles: 162 rational, 6 mixed.')
    print('All finite norm survivors:', [(c,gs) for c,D,gs,H in possible])
    print('The five cases requiring a dimension-vector check:', finite)
    print('Unrestricted mixed moment check:', candidates,ds,'D/4 has coordinates (75,33).')


if __name__ == '__main__':
    verify()

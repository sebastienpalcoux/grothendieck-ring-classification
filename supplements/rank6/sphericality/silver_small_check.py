"""Exact finite comparisons in the three-orbit theorem over Q(sqrt(2))."""
from fractions import Fraction
from itertools import combinations_with_replacement, product
from math import lcm

F = Fraction


def trace(family, exponent):
    left, right = ((2, 6), (2, 10))[family]
    for _ in range(exponent):
        left, right = right, 6*right-left
    return left


def mass(orbit):
    family, exponent, scalar = orbit
    return F(trace(family, exponent), scalar)


def gap(orbit):
    family, exponent, scalar = orbit
    return (trace(family, exponent)**2 - F(4, 2**family)) / scalar**2


def greater_ratio(physical, ordinary, exponent_shift, a):
    # Evaluate v^(ordinary-physical) u^shift > a in Q(sqrt(2)).
    A, B = {(0, 1): (2, 1), (1, 0): (1, F(-1,2))}.get((physical, ordinary), (1, 0))
    for _ in range(exponent_shift):
        A, B = 3*A+4*B, 2*A+3*B
    A -= a
    if A*B >= 0:
        return (A or B) > 0
    return A*(A*A-2*B*B) > 0


def orbit_candidates():
    for family, exponent in ((1, 0), (0, 1), (1, 1)):
        for n in range(2, 50, 2 if family else 4):
            # Start the unit-family enumeration at four.
            scalar = n if family else n+2
            H = family, exponent, scalar
            w = mass(H)
            if F(1,5) < w < 1 and gap(H)+F(16,19)*(1-w)**2 <= F(1,2):
                yield H


def small_pairs():
    rows = set()
    for H in orbit_candidates():
        for f in (0, 1):
            for n in range(2 if f else 4, 100, 2 if f else 4):
                G = f, 1, n
                t = 1 - mass(H) - mass(G)
                if 0 < t <= F(1,4) and gap(H)+gap(G)+16*t*t <= F(1,2):
                    rows.add(tuple(sorted((H, G))))
    return sorted(rows)


def admissible(H, G, E, f, r, a, t):
    e, k, m = E
    ell = k+r
    if m % a or (f > e and a % 2):
        return
    M = m//a
    if M % (2 if f else 4):
        return
    if any(m % n or (i > e and m//n % 2) for i,j,n in (H,G)):
        return
    if not greater_ratio(e, f, r, a) or 2*ell+f < max(2*o[1]+o[0] for o in (H,G)):
        return
    D = f, ell, M
    s = mass(D)
    if (lcm(H[2], G[2])*s).denominator != 1:
        return
    if gap(E)+gap(H)+gap(G)+2*gap(D) > F(1,2):
        return
    # Both complementary numerator traces are strictly positive even integers.
    for c in range(2, H[2], 2):
        other = G[2]*(1-s-F(c, H[2]))
        if other.denominator == 1 and 0 < other < G[2] and other % 2 == 0:
            return D, s


def small_survivors(rows):
    out = []
    for H,G in rows:
        t = 1-mass(H)-mass(G)
        e = (1-H[0]-G[0]) % 2
        for k,f,r,a in product(range(7), range(2), range(3), range(1,9)):
            scalar = F(trace(e,k), t)
            if scalar.denominator != 1:
                continue
            E = e, k, int(scalar)
            value = admissible(H, G, E, f, r, a, t)
            if value is not None:
                D, s = value
                out.append(((H,G), E, D, s))
    return out


def polynomial_minimum(a, b, c):
    return c-F(b*b, 4*a)


def check_unbounded_second_exponent():
    c = F(288,289)
    large = [H for H in orbit_candidates() if
             gap(H)+F(57600,60401)*(1-mass(H))**2 <= F(1,2)]
    assert large == [(1,0,4),(1,0,6),(0,1,12),(0,1,16),
                     (1,1,18),(1,1,20),(1,1,22),(1,1,24)]
    for H in large[1:]:
        z = 1-mass(H)
        a, b, d = c*F(209,100), -c*F(3,5)*z, gap(H)+c*z*z
        assert polynomial_minimum(a+1, b-1, d+F(1,4)) > F(29,50)
        sample = F(21,100) if H in [(1,0,6),(0,1,12)] else F(1,6)
        assert a*sample**2+b*sample+d > F(1,2) and 2*a*sample+b > 0
        if H == (0,1,16):
            assert a*F(1,64) + b*F(1,8) + d > F(1,2)
    assert F(49,200)+c*(F(19,40)**2+F(2,64)) > F(1,2)
    lookup = [p for p in combinations_with_replacement(range(4,25,2),4)
              if F(79,100) < sum(F(1,d) for d in p) < 1]
    assert all(p[:3] == (4,4,4) or p in [(4,4,6,6),(4,4,6,8)] for p in lookup)


if __name__ == "__main__":
    rows = small_pairs()
    assert len(rows) == 8 and min(1-mass(H)-mass(G) for H,G in rows) == F(1,36)
    assert max(lcm(H[2],G[2]) for H,G in rows) == 220
    sols = small_survivors(rows)
    assert len(sols) == 4
    expected = {(0,1,132):((1,1,66), F(5,33)), (0,0,16):((0,1,16), F(3,8)),
                (1,0,44):((1,1,44), F(5,22)), (1,1,220):((0,2,220), F(17,110))}
    for (H,G), E, D, s in sols:
        assert expected[E] == (D,s)
        if D not in (H,G):
            budget = F(1,2) - gap(E)-gap(H)-gap(G)-2*gap(D)
            assert budget < (F(1,2)-s)**2
    check_unbounded_second_exponent()
    print("Eight short pairs and four dimension cases checked.")
    print("The only residual orbit is 8 +/- 4*sqrt(2).")

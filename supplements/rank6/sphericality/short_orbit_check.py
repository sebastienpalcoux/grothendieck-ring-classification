#!/usr/bin/env python3
"""Exact finite substitution for the conductor-five short-orbit reduction.

The height bound and local idempotent argument are proved in the manuscript.
All comparisons here use integers or fractions. No numerical search bound
is substituted for a proved bound.
"""
from fractions import Fraction as F
from math import isqrt

# Coordinates a+b*phi, where phi^2=phi+1.
def mul(x, y):
    a, b = x; c, d = y
    return (a*c+b*d, a*d+b*c+b*d)
def norm(x):
    a, b = x
    return a*a+a*b-b*b
def trace(x):
    return 2*x[0]+x[1]
def scale(x, m):
    return (m*x[0], m*x[1])
def divides(y, x):
    a, b = y
    z = mul(x, (a+b, -b))
    return all(v % norm(y) == 0 for v in z)
def mass(x):
    return F(trace(x), norm(x))
def gap(x):
    return F(5*x[1]*x[1], norm(x)**2)
def below_80(x):
    a, b = x
    r = 160-2*a-b
    return r > 0 and 5*b*b < r*r

u, v = (1, 1), (2, 1)
powers = [(1, 0)]
for _ in range(5):
    powers.append(mul(powers[-1], u))
assert [trace(x) for x in powers] == [2, 3, 7, 18, 47, 123]
assert [mass(mul(v, x)) for x in powers] == [1, 2, 5, 13, 34, 89]
assert F(5, 14)*F(29, 40)**2+F(1, 80)-F(1, 5) == F(1, 4480)
assert not below_80(scale(powers[3], 5))
assert not below_80(scale(mul(v, powers[2]), 6))

primitives = [('U', k, p) for k, p in enumerate(powers[:5])]
primitives += [('V', k, mul(v, p)) for k, p in enumerate(powers[:5])]
e_values = []
for family, k, p in primitives:
    for m in range(1, 80):
        E = scale(p, m)
        if below_80(E) and trace(E) % 5 == 0 and mass(E) < 1:
            e_values.append((family, k, m, E))
assert len(e_values) == 49
assert max(e[2] for e in e_values) == 75

actual = set()
for family, k, m, E in e_values:
    complements = []
    for f, j, q in primitives:
        if f == 'U' and j == 0:
            continue
        for n in range(1, m+1):
            if m % n:
                continue
            H = scale(q, n)
            if mass(H) < 1 and trace(H) % 5 == 0 and divides(H, E):
                complements.append((f, j, n, H))
    for i, h in enumerate(complements):
        for j in complements[i+1:]:
            H, J = h[3], j[3]
            if mass(E)+mass(H)+mass(J) != 1:
                continue
            if gap(E)+gap(H)+gap(J) > F(1, 5):
                continue
            discr = F(norm(E)*norm(H)*norm(J), 125)
            if discr.denominator != 1 or isqrt(discr.numerator)**2 != discr.numerator:
                continue
            pair = tuple(sorted((h[:3], j[:3])))
            actual.add(((family, k, m), pair))

raw = [
    (('U', 0, 10), ('V', 0, 2), ('U', 1, 10)),
    (('V', 0, 4), ('V', 0, 2), ('V', 0, 4)),
    (('V', 0, 6), ('V', 0, 2), ('V', 0, 3)),
    (('V', 0, 6), ('V', 0, 2), ('V', 1, 6)),
    (('V', 0, 10), ('V', 0, 2), ('V', 1, 5)),
    (('U', 1, 20), ('V', 0, 2), ('U', 2, 20)),
    (('V', 1, 6), ('V', 0, 2), ('V', 0, 6)),
    (('V', 1, 6), ('V', 0, 3), ('V', 1, 6)),
    (('V', 1, 8), ('V', 0, 2), ('V', 0, 4)),
    (('V', 1, 8), ('V', 0, 2), ('V', 1, 8)),
]
expected = {(e, tuple(sorted((h, j)))) for e, h, j in raw}
assert actual == expected, (actual-expected, expected-actual)
assert all(('V', 0, 2) in pair or ('V', 0, 3) in pair for _, pair in actual)

# Exact constants in the exclusion of the 3v orbit.
assert gap(mul(v, u))/mass(mul(v, u))**2 == F(4, 5)
assert F(4, 5)*F(2, 9)+F(1, 45) == F(1, 5)
assert gap(scale(mul(v, powers[2]), 6)) == F(121, 180) > F(1, 5)
# (8-2*sqrt(6))/15 > 1/5 is equivalent to 5 > 2*sqrt(6).
assert 25 > 24
print('Conductor five: all 49 bounded E-values checked exactly.')
print('Exactly 10 signed profiles remain; each contains 2v or 3v.')
print('The height margin and constants excluding the 3v orbit are verified.')
print('The unbounded local-order exclusion is treated in the paper.')

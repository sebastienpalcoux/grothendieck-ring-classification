#!/usr/bin/env python3
"""Exact Fourier certificates reducing the 15 K7 ratios to two unit orbits.

Every root interval is verified by rational sign changes.  Positive
definiteness uses interval determinants and Sylvester's criterion.
No floating point, numerical optimization, or external package is used.
"""
from fractions import Fraction as F
from itertools import permutations
from cubic_ratio_bound import enumerate_ratios


class Interval:
    def __init__(self, lo, hi=None):
        self.lo = F(lo)
        self.hi = F(lo if hi is None else hi)
        assert self.lo <= self.hi

    @staticmethod
    def cast(x):
        return x if isinstance(x, Interval) else Interval(x)

    def __add__(self, other):
        other = self.cast(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-self.cast(other))

    def __rsub__(self, other):
        return self.cast(other) - self

    def __mul__(self, other):
        other = self.cast(other)
        values = [x*y for x in (self.lo, self.hi)
                  for y in (other.lo, other.hi)]
        return Interval(min(values), max(values))

    __rmul__ = __mul__


ROOTS = {
    (5, 6, 1): ((198062262, 198062267), (1554958129, 1554958135), (3246979601, 3246979607)),
    (6, 5, 1): ((307978526, 307978531), (643104130, 643104135), (5048917337, 5048917343)),
    (7, 14, 7): ((753020394, 753020399), (2445041865, 2445041870), (3801937733, 3801937738)),
    (10, 17, 1): ((60998922, 60998927), (2088145998, 2088146003), (7850855073, 7850855078)),
    (10, 24, 8): ((396124526, 396124531), (3109916262, 3109916267), (6493959205, 6493959210)),
    (12, 20, 8): ((615957054, 615957059), (1286208262, 1286208267), (10097834677, 10097834682)),
    (13, 26, 1): ((39228658, 39228663), (2417894790, 2417894795), (10542876544, 10542876549)),
    (14, 21, 7): ((484270526, 484270531), (1170915186, 1170915191), (12344814280, 12344814285)),
    (14, 49, 7): ((149144922, 149144927), (5911853997, 5911854002), (7939001073, 7939001078)),
    (15, 54, 27): ((594186790, 594186795), (4664874394, 4664874399), (9740938809, 9740938814)),
    (17, 10, 1): ((127374658, 127374663), (478893715, 478893720), (16393731620, 16393731625)),
    (18, 45, 27): ((923935583, 923935588), (1929312394, 1929312399), (15146752016, 15146752021)),
    (19, 83, 1): ((12081583, 12081588), (6780167469, 6780167474), (12207750941, 12207750946)),
    (20, 68, 8): ((121997847, 121997852), (4176291998, 4176292003), (15701710148, 15701710153)),
    (20, 96, 64): ((792249054, 792249059), (6219832526, 6219832531), (12987918412, 12987918417)),
}

# (ordinary Fourier weight, 1000*lambda, 1000*kappa,
#  reciprocal-mass weight, 1000*mu).
# The last term is mu*(q0-q2).
CERTIFICATES = {
    (10, 17, 1): (1, 5929, 4844, 0, 1508),
    (10, 24, 8): (0, 17047, 16329, 1, 3049),
    (12, 20, 8): (1, 6805, 0, 0, 3904),
    (13, 26, 1): (0, 17862, 11703, 1, 5252),
    (14, 21, 7): (1, 11529, 0, 0, 6289),
    (15, 54, 27): (0, 25571, 24493, 1, 4573),
    (17, 10, 1): (1, 25283, 0, 0, 13000),
    (18, 45, 27): (0, 20979, 7891, 1, 7111),
    (20, 68, 8): (0, 28688, 20681, 1, 7790),
}
MIDDLE_ROOT_EXCLUSIONS = {(14, 49, 7), (19, 83, 1), (20, 96, 64)}
SEVEN_CERTIFICATES = [
    # 1000*lambda, [(1000*weight, linear form), ...]
    (5282, [(481, (7, -3, 5))]),
    (5935, [(239, (17, -5, 7)), (9, (4, 0, -1))]),
    (4967, [(403, (9, 0, -1))]),
]

# If q0<=1/bound, C2+lambda*C1+mu*(q0-1/bound)<=0.
# These augmented matrices are positive definite, giving strict height bounds.
HEIGHT_CERTIFICATES = {
    (5, 6, 1): (2000, 6034, 4158),
    (6, 5, 1): (44, 8842, 5466),
}


def root_intervals(poly):
    a, b, c = poly
    intervals = [Interval(F(lo, 10**9), F(hi, 10**9))
                 for lo, hi in ROOTS[poly]]
    value = lambda x: x**3 - a*x*x + b*x - c
    assert all(value(r.lo)*value(r.hi) < 0 for r in intervals)
    assert 0 < intervals[0].lo
    assert all(intervals[i].hi < intervals[i+1].lo for i in (0, 1))
    # Three disjoint sign-changing intervals for a cubic isolate all roots.
    return intervals


def determinant(matrix):
    n = len(matrix)
    total = Interval(0)
    for perm in permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n)
                         for j in range(i+1, n))
        term = Interval(-1 if inversions % 2 else 1)
        for i, j in enumerate(perm):
            term = term * matrix[i][j]
        total = total + term
    return total


def matrix(alpha, ordinary, lam, kap, mass, linear):
    p = [[F(1) if i == j else F(-1, 2) for j in range(3)]
         for i in range(3)]
    q = [[ordinary*alpha[i]*alpha[j]*p[i][j]
          + lam*(p[i][j] + F(1, 4))
          + kap*(F(1, 4) - p[i][j])
          for j in range(3)] for i in range(3)]
    ell = [-lam/2 + mass*alpha[i] + linear[i] for i in range(3)]
    constant = -F(ordinary, 7) + 3*lam/28 - mass
    return [q[i] + [ell[i]*F(1, 2)] for i in range(3)] + [
        [ell[i]*F(1, 2) for i in range(3)] + [Interval(constant)]]


def verify_positive_definite(m):
    for k in range(1, 5):
        minor = determinant([row[:k] for row in m[:k]])
        assert minor.lo > 0, (k, minor.lo, minor.hi)


def main():
    candidates = {row[:3] for row in enumerate_ratios()}
    for poly, weights in CERTIFICATES.items():
        alpha = root_intervals(poly)
        ordinary, l, k, mass, mu = weights
        verify_positive_definite(matrix(
            alpha, ordinary, F(l, 1000), F(k, 1000), mass,
            [F(mu, 1000), F(0), F(-mu, 1000)]))
    for poly in MIDDLE_ROOT_EXCLUSIONS:
        assert root_intervals(poly)[1].lo > 5

    alpha = root_intervals((7, 14, 7))
    for l, terms in SEVEN_CERTIFICATES:
        linear = [sum(F(weight, 1000)*form[i]
                      for weight, form in terms) for i in range(3)]
        verify_positive_definite(matrix(
            alpha, 1, F(l, 1000), F(0), 0, linear))

    eliminated = set(CERTIFICATES) | MIDDLE_ROOT_EXCLUSIONS | {(7, 14, 7)}
    assert candidates - eliminated == {(5, 6, 1), (6, 5, 1)}
    for poly, (bound, lam, mu) in HEIGHT_CERTIFICATES.items():
        m = matrix(root_intervals(poly), 1, F(lam, 1000), F(0), 0,
                   [F(mu, 1000), F(0), F(0)])
        m[3][3] = m[3][3] - F(mu, 1000*bound)
        verify_positive_definite(m)
    print("PASS: 9 global positive-definite certificates.")
    print("PASS: 3 middle-root exclusions.")
    print("PASS: 3 positive-definite certificates cover the norm-7 ratio.")
    print("Remaining ratio polynomials: x^3-5x^2+6x-1 and x^3-6x^2+5x-1.")
    print("PASS: the remaining ratios force E<2000 and E<44, respectively.")


if __name__ == "__main__":
    main()

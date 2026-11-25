#!/usr/bin/env python3
"""Exact finite polynomial checks for the cubic codegree arguments.

These are proved finite ranges for algebraic integers, not a bounded census
of fusion rings.  No floating-point calculation occurs in this program.
The accompanying proof normalizes an invariant principal ideal in the
conductor-seven/nine field to norm 1,p,p^2.
"""

from fractions import Fraction
from math import isqrt


def discriminant(a, b, c):
    return a*a*b*b - 4*b*b*b - 4*a*a*a*c - 27*c*c + 18*a*b*c


def d_number(a, b, c):
    return a**3 % c == 0 and b**3 % (c*c) == 0


def check_nine_gap():
    """If nu<1/4, discriminant positivity forces a<32c."""
    totals = []
    for c in (1, 3, 9):
        checked = 0
        survivors = []
        for a in range(1, 32*c):
            for b in range(a*a//4 + 1, a*a//3 + 1):
                if not d_number(a, b, c):
                    continue
                checked += 1
                if discriminant(a, b, c) > 0:
                    survivors.append((a, b, c))
        assert not survivors, survivors
        totals.append((c, 32*c-1, checked))
    return totals


def check_seven_gap():
    """If nu<1/7, positivity forces 2a^3<343c."""
    totals = []
    for c in (1, 7, 49):
        bound = 0
        while 2*(bound+1)**3 < 343*c:
            bound += 1
        checked = 0
        survivors = []
        for a in range(1, bound+1):
            for b in range(2*a*a//7 + 1, a*a//3 + 1):
                if not d_number(a, b, c):
                    continue
                checked += 1
                if discriminant(a, b, c) > 0:
                    survivors.append((a, b, c))
        assert not survivors, survivors
        totals.append((c, bound, checked))
    return totals


def check_seven_second_gap():
    """Classify nu<1/4 in K7; sharper integral gaps bound the trace."""
    totals = []
    survivors = []
    for c, bound in ((1, 10), (7, 31), (49, 10)):
        checked = 0
        for a in range(1, bound+1):
            for b in range(a*a//4+1, a*a//3+1):
                if not d_number(a, b, c):
                    continue
                checked += 1
                delta = discriminant(a, b, c)
                if delta > 0:
                    survivors.append((a, b, c, delta))
        totals.append((c, bound, checked))
    assert survivors == [(7, 14, 7, 49)], survivors
    return totals, survivors


def check_nine_alpha():
    """All degree-three alpha with Tr(alpha)<=6 and Norm(alpha)|3^6."""
    survivors = []
    for a in (3, 6):  # Trace(O_{Q(zeta_9)^+})=3 Z.
        for c in (1, 3):  # Positive norm <=(6/3)^3=8, dividing 3^6.
            for b in range(1, a*a//3+1):
                if not d_number(a, b, c):
                    continue
                delta = discriminant(a, b, c)
                if delta <= 0 or isqrt(delta)**2 != delta:
                    continue
                if isqrt(delta) % 9:
                    continue
                if any(z**3-a*z*z+b*z-c == 0
                       for z in range(1, c+1) if c % z == 0):
                    continue
                survivors.append((a, b, c, delta))
    assert survivors == [(6, 9, 1, 81), (6, 9, 3, 81)], survivors
    return survivors


def check_nine_complement():
    """Recover H from E=9, reciprocal mass 2/3, and variance 1/4."""
    survivors = []
    for k in range(7):
        c = 3**k
        if c % 9:
            continue
        a, b = c//9, 2*c//3
        if a*a <= 3*b:
            continue
        # disc(T)=9^3 Norm(H), disc(O_K^2)=81^2.
        index_squared = Fraction(9**3*c, 81**2)
        if index_squared.denominator != 1:
            continue
        index_squared = int(index_squared)
        if isqrt(index_squared)**2 != index_squared:
            continue
        delta = discriminant(a, b, c)
        assert delta > 0 and isqrt(delta)**2 == delta
        survivors.append((a, b, c, delta))
    assert survivors == [(81, 486, 729, 3**16)], survivors
    return survivors


if __name__ == "__main__":
    print("Conductor 9 strict-gap ranges (norm, trace bound, checks):",
          check_nine_gap())
    print("Conductor 7 strict-gap ranges (norm, trace bound, checks):",
          check_seven_gap())
    print("Conductor 7 second gap:", check_seven_second_gap())
    print("Conductor 9 possible ratios:", check_nine_alpha())
    print("Conductor 9 complementary polynomial:", check_nine_complement())
    print("PASS: all exact cubic polynomial checks.")

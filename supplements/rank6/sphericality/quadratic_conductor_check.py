#!/usr/bin/env python3
"""Check the conductor bounds for quadratic fields with two rational codegrees.

The manuscript derives the search ranges from the Fourier inequalities."""
from fractions import Fraction as F
from math import gcd, isqrt


def least_unit_trace(c):
    b = 1
    while True:
        a = isqrt(c * b * b + 4)
        if a * a - c * b * b == 4:
            return a, b
        b += 1


def main():
    conductors = [
        5, 8, 12, 13, 17, 21, 24, 28, 29, 33,
        40, 44, 56, 60, 76, 88, 92, 104,
    ]
    survivors = []
    for c in conductors:
        a, b = least_unit_trace(c)
        gap = F(a - 2, a + 2)
        bound = F(gcd(c, 4), c)
        irrational = gap / 18 <= bound
        rational_mass = F(1, 3) - F(2 if c % 2 else 4, c)
        rational = rational_mass <= 0 or gap * rational_mass**2 <= bound
        if irrational or rational:
            survivors.append(c)
    assert survivors == [5, 8, 12, 13, 17, 21, 24, 28, 40, 44, 56, 60]

    for c in (17, 44, 56):
        a, _ = least_unit_trace(c)
        gap = F(a - 2, a + 2)
        bound = F(gcd(c, 4), c)
        assert gap / 8 > bound
        mass = F(1, 2) - F(2 if c % 2 else 4, c)
        assert gap * mass**2 > bound

    final = [c for c in survivors if c not in (17, 44, 56)]
    assert final == [5, 8, 12, 13, 21, 24, 28, 40, 60]
    print("Exact least-unit sieve:", survivors)
    print("After the inert-three argument:", final)
    print("PASS: all bounded-field comparisons.")


if __name__ == "__main__":
    main()

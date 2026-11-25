#!/usr/bin/env python3
"""Enumerate the fifteen cubic ratios at conductor seven within the proved trace bound."""
from itertools import product
from cubic_seven_lattice_check import mul, trace


def norm(a):
    basis = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    columns = [mul(a, b) for b in basis]
    m = [[columns[j][i] for j in range(3)] for i in range(3)]
    value = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
             - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
             + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    assert value.denominator == 1
    return int(value)


def sigma(a):
    # sigma(theta)=2-theta^2.
    x, y, z = a
    return (x + 2*y + 3*z, z, -y-z)


def enumerate_ratios():
    out = []
    for a in product(range(-20, 21), range(-10, 11), range(-10, 11)):
        if a[1:] == (0, 0):
            continue
        big_a = trace(a)
        if not 0 < big_a <= 20:
            continue
        tr2 = trace(mul(a, a))
        if tr2 > big_a**2:
            continue
        big_b = (big_a**2 - tr2) / 2
        assert big_b.denominator == 1
        big_b, big_c = int(big_b), norm(a)
        if big_b <= 0 or big_c <= 0:
            continue
        if big_a**3 % big_c or big_b**3 % (big_c**2):
            continue
        # Reject alpha-1 totally positive; irreducibility excludes a root 1.
        if (big_a > 3 and big_b - 2*big_a + 3 > 0
                and big_c - big_b + big_a - 1 > 0):
            continue
        if a != min(a, sigma(a), sigma(sigma(a))):
            continue
        out.append((int(big_a), big_b, big_c, a))
    out.sort()
    expected = [
        (5, 6, 1), (6, 5, 1), (7, 14, 7), (10, 17, 1),
        (10, 24, 8), (12, 20, 8), (13, 26, 1), (14, 21, 7),
        (14, 49, 7), (15, 54, 27), (17, 10, 1), (18, 45, 27),
        (19, 83, 1), (20, 68, 8), (20, 96, 64)]
    assert [row[:3] for row in out] == expected, out
    return out


if __name__ == "__main__":
    for a, b, c, vector in enumerate_ratios():
        print((a, b, c), vector)
    print("PASS: exactly 15 nontrivial ratio orbits in the proved range.")

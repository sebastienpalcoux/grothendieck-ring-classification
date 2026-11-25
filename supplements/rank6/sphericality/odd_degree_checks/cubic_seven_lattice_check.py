#!/usr/bin/env python3
"""Verify the trace form and the integral frames of norms two and three at conductor seven."""
from fractions import Fraction
from itertools import product


def mul(a, b):
    out = [Fraction(0) for _ in range(5)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    # theta^3 = theta^2 + 2 theta - 1.
    for k in (4, 3):
        x = out[k]
        out[k - 3] -= x
        out[k - 2] += 2 * x
        out[k - 1] += x
        out[k] = 0
    return tuple(out[:3])


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(n, a):
    return tuple(n * x for x in a)


def trace(a):
    return 3 * a[0] + a[1] + 5 * a[2]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def check_field():
    unit = (1, 0, 0)
    basis = (unit, (0, 1, 0), (-1, 0, 1))
    f = (1, 1, 2)
    f_inv = (Fraction(4, 7), 0, Fraction(-1, 7))
    assert mul(f, f_inv) == unit
    f2 = mul(f, f)
    f3 = mul(f2, f)
    assert add(add(f3, scale(-14, f2)),
               add(scale(49, f), scale(-49, unit))) == (0, 0, 0)
    gram = tuple(tuple(trace(mul(mul(a, b), f_inv)) for b in basis)
                 for a in basis)
    assert gram == ((1, 0, 0), (0, 1, 0), (0, 0, 1)), gram
    return gram


def check_frames(n):
    first = (1,) * n + (0,) * (6 - n)
    rows = [(0,) + x for x in product((-1, 0, 1), repeat=5)
            if dot(x, x) == n and dot(first, (0,) + x) == 0]
    frames = [(a, b) for a in rows for b in rows if dot(a, b) == 0]
    if n == 3:
        assert not frames, frames
    elif n == 2:
        # The second column is the first row's unique extra entry.
        assert all(a[1] == b[1] == 0 for a, b in frames)
        assert frames
    return len(rows), len(frames)


if __name__ == "__main__":
    print("Integral trace Gram matrix:", check_field())
    print("n=2 admissible rows and ordered frames:", check_frames(2))
    print("n=3 admissible rows and ordered frames:", check_frames(3))
    print("PASS: conductor-seven lattice identities and frame assertions.")

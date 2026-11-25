#!/usr/bin/env python3
"""Exact reciprocal-mass and trace-recurrence checks at quadratic conductor 24."""
from fractions import Fraction as F


def cycle(first, second, modulus):
    """Trace values over one period, from an invertible recurrence."""
    start = first % modulus, second % modulus
    a, b = start
    values = []
    while True:
        values.append(a)
        a, b = b, (10 * b - a) % modulus
        if (a, b) == start:
            return values


def main():
    cutoff = F(207, 1000)
    ld, lh = F(24, 25), F(242, 243)
    # The right side decreases with t <= s/5 < 1/3 in the w term.
    lower = lh * (F(1, 3) - cutoff / 5) ** 2 + 2 * ld * cutoff ** 2
    slope = 4 * ld * cutoff - 2 * lh * (F(1, 3) - cutoff / 5) / 5
    assert slope > 0 and lower > F(1, 6)
    assert F(48, 25)*F(7, 22)**2 > F(1, 6)
    assert F(1, 3) - cutoff / 5 > F(7, 24)
    assert lh*F(7, 24)**2 + F(16, 183) > F(1, 6)
    assert 4 < 2/(F(1, 3) - cutoff) < 16

    assert F(5, 24) - cutoff == F(1, 750)
    survivors = []
    for h in range(2, 14):
        s = F(5, 24) - F(1, 4*h*h)
        if s.denominator % 9 == 0:
            continue
        period = cycle(2, 10, s.numerator)
        zeros = [r for r, value in enumerate(period) if value == 0]
        if zeros:
            survivors.append((h, s, len(period), zeros))
    assert survivors == [(2, F(7, 48), 8, [2, 6])]

    assert cycle(2,10,32) == [2,10]
    assert cycle(1,5,8) == [1,5]
    assert cycle(1,9,8) == [1]
    print("Quadratic conductor 24: reciprocal bounds and all twelve denominator checks passed.")
    print("Only the pair (8,16) remains before Pell divisibility.")


if __name__ == "__main__":
    main()

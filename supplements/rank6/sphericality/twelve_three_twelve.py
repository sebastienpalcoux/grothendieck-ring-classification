"""Exclude the conductor-twelve profile with rational rows of codegrees 3,12."""
from fractions import Fraction
from itertools import product

from folded_twelve_check import B, ONE, add, coeff, divisors, mul, positive, power, scale


def square(x):
    return mul(x, x)


def admissible_indices():
    for d, r, c in product(range(2), range(1, 5), range(1, 33)):
        if d and c % 6:
            continue
        comparison = mul(coeff(d, False), power(r))
        if not positive(add(comparison, (-c, 0))):
            continue
        wronskian = 2 * B(d, r + 1) - 4 * B(d, r)
        assert 0 < abs(wronskian) <= 672
        for h in divisors(2 * c * abs(wronskian)):
            for z in range(-11, 5):
                if 2 * z > 2 * r + d or (h - (-1)**(z % 2)) % 3:
                    continue
                if (d, r, c) != (0, z, h):  # D=H already gives a spherical section
                    yield d, r, c, h, z


def passes_small(k, d, r, c, h, z):
    if k + z < 3:
        return False
    b, g, o = B(0, k), B(0, k + z), B(d, k + r)
    m, remainder = divmod(12 * (b + h * g), 7)
    if remainder or m % 12 or m % (6 * h) or m % ((2 if d else 6) * c):
        return False
    if (2 * b) % h or (2 * c * o) % h:
        return False
    n = 6**d
    gap = n * (b*b - 4 + h*h*(g*g - 4)) + 2*c*c*(n*o*o - 4)
    return 3 * gap <= n * m*m


def passes_large(d, r, c, h, z):
    eta = Fraction(999, 1000)
    x = scale(power(z), h)
    y = scale(mul(coeff(d, True), power(r)), c)
    lower = scale(add(add(ONE, square(x)), scale(square(y), 2)), 147*eta*eta)
    upper = scale(square(add(ONE, x)), 144)
    return not positive(add(lower, scale(upper, -1)))


def main():
    # eta <= (u^6-1)/(u^6+1) for u=2+sqrt(3).
    assert positive(add(power(6), (-1999, 0)))
    small = []
    large = []
    for parameters in admissible_indices():
        for k in range(3):
            if passes_small(k, *parameters):
                small.append((k, *parameters))
        if passes_large(*parameters):
            large.append(parameters)
    assert small == []
    assert large == [(0, 1, 1, 8, 1)]
    assert (B(0, 8) % 7, B(0, 9) % 7) == (2, 4)
    assert all((B(0, k) + 8*B(0, k+1)) % 7 for k in range(8))
    print("No small index; one limiting tuple, excluded modulo seven.")


if __name__ == "__main__":
    main()

"""Check the quadratic unit, trace and projection bounds in the rank-six proof.

All comparisons use integers or rational arithmetic. Run with python3.
"""
from fractions import Fraction
from math import gcd, isqrt


# Columns are the field discriminant c, Tr(U), b, d, and h, with
# U=(Tr(U)+b sqrt(c))/2, V=(1+U)/d and Tr(O_K/V)=hZ.
QUADRATIC_UNITS = (
    (5, 3, 1, 1, 1), (8, 6, 2, 2, 2), (12, 4, 1, 1, 1),
    (13, 11, 3, 1, 1), (21, 5, 1, 1, 1), (24, 10, 2, 2, 2),
    (28, 16, 3, 3, 1), (40, 38, 6, 2, 2), (60, 8, 1, 1, 1),
)


def verify_quadratic_units():
    """Verify the minimal norm-one unit, primitivity of V and its trace ideal."""
    for c, trace, b, d, h in QUADRATIC_UNITS:
        assert trace**2 - c*b**2 == 4
        for smaller in range(1, b):
            candidate = c*smaller**2 + 4
            assert isqrt(candidate)**2 != candidate

        # The integral basis is (1, omega), where omega=(e+sqrt(c))/2.
        e = c % 2
        constant = Fraction(trace + 2 - b*e, 2*d)
        coefficient = Fraction(b, d)
        assert constant.denominator == coefficient.denominator == 1
        assert gcd(int(constant), int(coefficient)) == 1

        # Tr(1/V)=d, while 1/V=d(1+U')/(trace+2).
        trace_omega_over_v = Fraction(d*e, 2) - Fraction(c*b*d, 2*(trace+2))
        assert trace_omega_over_v.denominator == 1
        assert gcd(d, int(trace_omega_over_v)) == h


def verify_projection_bounds():
    """Check the squared bounds for s,w,t and the comparison t+w <= 1/3."""
    bounds = {
        13: (Fraction(11, 39)**2, Fraction(11, 39)**2, Fraction(2, 39)**2),
        21: (Fraction(5, 21)**2, Fraction(5, 21)**2, Fraction(2, 21)**2),
        40: (Fraction(19, 60)**2 / 2, Fraction(19, 60)**2, Fraction(1, 60)**2 / 2),
        60: (Fraction(4, 15)**2 / 2, Fraction(4, 15)**2, Fraction(1, 15)**2 / 2),
    }
    for c, trace, _, d, _ in QUADRATIC_UNITS:
        if c not in bounds:
            continue
        gap = 1 - Fraction(4, trace**2)
        s_squared = Fraction(gcd(c, 2), c) / gap
        w_squared = Fraction(gcd(c, 4), c) / gap
        t_squared = s_squared * Fraction(max(d, 2), trace)**2
        assert (s_squared, w_squared, t_squared) == bounds[c]

        # Squaring removes the one remaining square root, 2*w*t.
        margin = Fraction(1, 9) - w_squared - t_squared
        assert margin > 0
        product = 4*w_squared*t_squared
        if c in (13, 21):
            assert margin**2 == product
        else:
            assert margin**2 > product


def verify_repeated_pair_bounds():
    """Compare the long and short reciprocal gaps used at conductor eight."""
    long_gap = Fraction(49, 50)
    assert Fraction(1, 4) - long_gap * Fraction(12, 25)**2 < Fraction(1, 18)
    assert 2 * long_gap * (Fraction(1, 5)**2 + Fraction(12, 25)**2) > Fraction(1, 2)


def verify_norm_one_obstructions():
    """Check the prime divisors excluding the real complementary rows at 24."""
    masses = {h: Fraction(5, 24) - Fraction(1, 4*h**2) for h in range(2, 14)}
    possible = [h for h, mass in masses.items() if mass.denominator % 9]
    assert possible == [2, 4, 5, 7, 8, 10, 11, 13]
    numerators = [masses[h].numerator for h in possible]
    assert numerators == [7, 37, 119, 239, 157, 247, 599, 839]
    for numerator, prime in zip(numerators[1:], (37, 17, 239, 157, 13, 599, 839)):
        assert all(prime % trial for trial in range(2, isqrt(prime) + 1))
        assert numerator % prime == 0
        symbol = pow(6, (prime - 1) // 2, prime)
        assert symbol in (1, prime - 1)
        group_order = prime - (1 if symbol == 1 else -1)
        assert group_order % 4 == 2


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Use unoptimized Python to run the assertions.")
    verify_quadratic_units()
    verify_projection_bounds()
    verify_repeated_pair_bounds()
    verify_norm_one_obstructions()
    print("Quadratic units, trace ideals, projection bounds and residue obstructions verified.")

"""Independent conductor-list and cyclic-field audit for the split profile.

The finite certificate is replayed separately by its production verifier.
This file tests the mathematical field-list transitions with different code.
"""
import itertools
import json
import math
from pathlib import Path
import sympy as s


def need(v, message):
    if not v:
        raise RuntimeError(message)


products = sorted({math.prod(c) for n in range(4)
                   for c in itertools.combinations([3, 5, 7], n)})
twists = [m for m in products if m % 4 == 1 and math.lcm(738, m) <= 7416]
biquadratic = [m for m in twists if m > 1 and m % 8 == 1]
quartic = [m for m in twists if m % 8 == 5]
need(biquadratic == [], "unexpected biquadratic field")
need(quartic == [5, 21], "unexpected cyclic quartic twist")

generator = next(g for g in range(2, 41)
                 if pow(g, 20, 41) != 1 and pow(g, 8, 41) != 1)
log_two = next(k for k in range(40) if pow(generator, k, 41) == 2)
need(log_two % 4 == 2, "quartic character at two is not minus one")

# Generators 3 modulo 7 and 2 modulo 9 identify the cubic characters.
need(pow(3, 2, 7) == 2, "wrong cubic logarithm modulo seven")
cubic = []
for a, b in itertools.product(range(3), repeat=2):
    if (a, b) == (0, 0) or (2 * a + b) % 3:
        continue
    cubic.append({"character_exponents": [a, b],
                  "conductor": (7 if a else 1) * (9 if b else 1)})
need(len(cubic) == 2 and all(c["conductor"] == 63 for c in cubic),
     "unexpected split cubic character")

x = s.symbols("x")
field_checks = []
for m in quartic:
    f = s.Poly(x**4 - 41*m*x*x + 164*m*m, x, domain=s.QQ)
    need(f.is_irreducible, "quartic polynomial reducible")
    red = lambda v: s.rem(v, f.as_expr(), x)
    beta = (x**3 - 33*m*x) / (10*m)
    sigma = lambda v: red(v.subs(x, beta))
    r = (2*x*x/m - 41) / 5
    need(red(r*r) == 41, "wrong quadratic subfield")
    need(red(x*beta - 2*m*r) == 0, "wrong radical product")
    need(sigma(r) == -r, "automorphism does not conjugate the quadratic field")
    need(sigma(beta) == -x, "automorphism does not have order four")
    need(sigma(sigma(sigma(sigma(x)))) == x, "fourth automorphism power failed")
    field_checks.append({"twist": m, "polynomial": str(f.as_expr()),
                         "irreducible": True, "cyclic_order_four_verified": True})

report = {
    "passed": True,
    "optimized": not __debug__,
    "positive_odd_discriminants_with_trace_budget": twists,
    "biquadratic_candidates": biquadratic,
    "quartic_twists": quartic,
    "quartic_character_at_two": -1,
    "split_cubic_characters": cubic,
    "quartic_fields": field_checks,
    "sextic_norm_contradiction": {"lower_bound": 49,
                                  "AMGM_upper_bound": "343/27",
                                  "strict": 49*27 > 343},
}
Path(__file__).with_suffix(".json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))

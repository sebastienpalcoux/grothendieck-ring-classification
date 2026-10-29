"""Exact arithmetic for the additional quartic-family model screens.

Run with Python 3. No optional packages or floating-point decisions.
This verifies dimensions/index inequalities, not categorical existence claims.
"""
from fractions import Fraction as Q
import json


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def mul(a, b):
    # Basis 1, sqrt(2), sqrt(3), sqrt(6); bit 0 represents sqrt(2).
    ans = [Q(0)] * 4
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            overlap = i & j
            factor = (2 if overlap & 1 else 1) * (3 if overlap & 2 else 1)
            ans[i ^ j] += factor * x * y
    return tuple(ans)


def interval(a):
    # Rational enclosures, independently checked by squaring.
    roots = [(Q(1), Q(1)), (Q(1414213, 10**6), Q(1414214, 10**6)),
             (Q(1732050, 10**6), Q(1732051, 10**6)),
             (Q(2449489, 10**6), Q(2449490, 10**6))]
    for n, (lo, hi) in zip([1, 2, 3, 6], roots):
        assert lo * lo <= n <= hi * hi
    lo = hi = Q(0)
    for c, (x, y) in zip(a, roots):
        lo += c * (x if c >= 0 else y)
        hi += c * (y if c >= 0 else x)
    return lo, hi


D = (144, 96, 80, 56)
E = (432, 0, 240, 0)
ratio = (24, -15, 12, -9)
assert mul(D, ratio) == E
ratio_lo, ratio_hi = interval(ratio)
assert 1 < ratio_lo < ratio_hi < 2

F4_dims = [(1, 0, 0, 0)] + [(2, 0, 0, 1)] * 2 + \
    [(3, 0, 0, 1)] * 2 + [(4, 0, 0, 2)] * 2 + \
    [(5, 0, 0, 2), (6, 0, 0, 2)]
F4_dimension = (0, 0, 0, 0)
for d in F4_dims:
    F4_dimension = add(F4_dimension, mul(d, d))
assert F4_dimension == (240, 0, 0, 96)
assert interval(F4_dimension)[1] < interval(D)[0]

# Vieta for the four roots of t^4-576t^3+11520t^2-73728t+147456.
sum_reciprocal = Q(73728, 147456)
sum_pairwise_reciprocal = Q(11520, 147456)
formal_codegree_inverse_square_sum = sum_reciprocal**2 - \
    2 * sum_pairwise_reciprocal + Q(1, 16)
assert formal_codegree_inverse_square_sum == Q(5, 32)
assert formal_codegree_inverse_square_sum < Q(1, 2)

print(json.dumps({
    'su4_8_exceptional_ratio_exact': list(ratio),
    'su4_8_ratio_rational_interval': [str(ratio_lo), str(ratio_hi)],
    'su4_8_proper_subcategory_index_screen': 'excluded: index strictly below 2',
    'f4_3_g2_4_global_dimension_exact': [int(x) for x in F4_dimension],
    'f4_3_g2_4_direct_subcategory_screen': 'excluded: source dimension below target',
    'formal_codegree_inverse_square_sum': str(formal_codegree_inverse_square_sum),
    'formal_codegree_inequality': 'passes',
    'categorification_status_change': False,
}, indent=2))

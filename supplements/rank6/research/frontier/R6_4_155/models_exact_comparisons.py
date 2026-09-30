#!/usr/bin/env python3
"""Tiny exact arithmetic checks for R155 literature comparisons.

This does not construct S, fusion coefficients, or a fusion category.
All Q(sqrt(2)) arithmetic uses rational pairs and the standard library.
"""
from fractions import Fraction as F
import json
from pathlib import Path


def q(a, b=0):
    return F(a), F(b)


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def mul(x, y):
    return x[0] * y[0] + 2 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def scale(a, x):
    return a * x[0], a * x[1]


def norm(x):
    return x[0] ** 2 - 2 * x[1] ** 2


def inv(x):
    return x[0] / norm(x), -x[1] / norm(x)


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


d, D = q(4, 3), q(72, 48)
b = add(q(2), scale(4, d))
check(mul(d, d) == add(q(2), scale(8, d)), "R155 dimension equation")
check(D == add(q(4), scale(2, mul(d, d))), "R155 global dimension")
check(b == scale(F(1, 4), D), "b = D/4")

dimensions = {
    "1": q(1), "d": d, "2d": scale(2, d), "3d": scale(3, d),
    "1+2d": add(q(1), scale(2, d)),
    "1+4d": add(q(1), scale(4, d)), "b": b,
}
norms = {name: int(norm(x)) for name, x in dimensions.items()}
check(norms == {"1": 1, "d": -2, "2d": -8, "3d": -18,
                "1+2d": 9, "1+4d": 1, "b": 36}, "norm list")

# The B dimension multiplicities in the forced spectrum.
multiplicities = {"1": 2, "d": 6, "2d": 8, "3d": 2,
                  "1+2d": 4, "1+4d": 2, "b": 2}
total = q(0)
for name, count in multiplicities.items():
    total = add(total, scale(count, mul(dimensions[name], dimensions[name])))
check(sum(multiplicities.values()) == 26, "rank B")
check(total == scale(F(1, 2), mul(D, D)), "dimension B")

# Grossman-Izumi S_00 = (1/sqrt(m) - 1/sqrt(n))/2.
center_difference = q(F(1, 4), -F(1, 6))  # m=16, n=18
B_difference = q(-F(1, 3), F(1, 4))       # m=8, n=9
check(center_difference == scale(2, inv(D)), "GI full center vacuum")
check(B_difference == mul(q(0, 2), inv(D)), "GI B vacuum")
GI_section4_rank = 2 + 2 + (16 - 2) // 2 + 2 + (18 - 2) // 2
GI_section6_rank = 2 + 6 + (8 - 4) // 2 + (9 - 1) // 2
check(GI_section4_rank == 21, "GI section 4 rank")
check(GI_section6_rank == 14, "GI section 6 rank")

# Section 6's dimension list at group orders (8,9).
sec6_mult = {"1": 1, "1+4d": 1, "1+2d": 6, "b": 2, "4d": 4}
sec6_dims = dict(dimensions, **{"4d": scale(4, d)})
sec6_total = q(0)
for name, count in sec6_mult.items():
    sec6_total = add(sec6_total, scale(count, mul(sec6_dims[name], sec6_dims[name])))
check(sec6_total == total, "GI section6 global dimension but wrong rank and dims")

# Merely an arithmetic near-group lead, not an existence assertion.
rho = scale(4, d)
check(mul(rho, rho) == add(q(32), scale(32, rho)), "near-group (32,32)")
check(add(q(32), mul(rho, rho)) == scale(8, D), "near-group dimension = 8D")

# All odd-N Haagerup-Izumi fields differ from Q(sqrt(2)).
check({(n*n+4) % 8 for n in (1, 3, 5, 7)} == {5}, "odd HI residues")
check({2*n*n % 8 for n in range(8)} == {0, 2}, "twice-square residues")

# Rational dimension-scale invariant J(z)=Tr(z)/sqrt(Norm(z)) at z=D².
# For a GH center it is N²+2; for a near-group center it is m²/n+2.
J_target = 2 * mul(D, D)[0] / norm(D)
check(J_target == 34, "target rational-scale invariant")
check(5**2 < J_target - 2 < 6**2, "no generalized Haagerup order")
# Schopieray Prop. 3.3 imposes n|m. Substituting n=2k², m=8k
# gives k|4. These are all positive divisors of 4, not a cutoff search.
near_group_locus = [(2*k*k, 8*k) for k in (1, 2, 4)]
for n, m in near_group_locus:
    check(m*m == 32*n and m % n == 0, "near-group locus and divisibility")

receipt = {
    "status": "PASS; invariant comparisons only, no categorification claimed",
    "B_rank": 26,
    "B_global_dimension_pair": [str(x) for x in total],
    "dimension_norms": norms,
    "GI_full_center_group_orders": [16, 18],
    "GI_section4_rank": GI_section4_rank,
    "GI_B_group_orders": [8, 9],
    "GI_section6_rank": GI_section6_rank,
    "GI_section6_dimension_multiplicities": sec6_mult,
    "near_group_32_32_dimension_ratio_to_R155": 8,
    "odd_HI_field_exclusion_mod8": True,
    "center_rational_dimension_scale_invariant": str(J_target),
    "near_group_types_after_Prop_3_3": near_group_locus,
    "near_group_types_after_rank3_exclusion": [[8, 16], [32, 32]],
}
path = Path(__file__).with_suffix(".json")
path.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))

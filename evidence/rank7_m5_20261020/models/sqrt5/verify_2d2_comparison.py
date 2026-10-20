#!/usr/bin/env python3
"""Exclude a specific Morita-model route, not general categorification.

Source for the center profile: Grossman--Izumi, arXiv:1501.07679v2,
Section 6, Figure 6 and Example 6.9. Its m=1 parameters are a'=1/2,
b'=1/sqrt(5), and S00=(a'-b')/2.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def mul(u, v):
    return (u[0]*v[0]+5*u[1]*v[1], u[0]*v[1]+u[1]*v[0])


def main():
    census = json.loads((ROOT / "supplements/rank7/output/m5/census.json").read_text())
    # Pair (r,s) denotes r+s*sqrt(5).
    unit, a, b, e = (1, 0), (5, 2), (8, 4), (9, 4)
    center_profile = [unit, e] + [a]*6 + [b]*2
    D = (720, 320)
    square_sum = tuple(sum(mul(d, d)[j] for d in center_profile) for j in range(2))
    require(square_sum == D, "Wrong 2D2-center global dimension")
    require(mul((20, 8), (20, 8)) == D, "Wrong 2D2 global dimension square")
    # Check the dimensions extracted from the first row of Figure 6.
    sqrt5 = sp.sqrt(5)
    ap, bp = sp.Rational(1, 2), 1/sqrt5
    s00 = (ap-bp)/2
    require(sp.simplify((ap+bp)/(2*s00)) == 9+4*sqrt5, "Wrong pi dimension")
    require(sp.simplify(ap/(2*s00)) == 5+2*sqrt5, "Wrong phi/psi dimension")
    require(sp.simplify(bp/s00) == 8+4*sqrt5, "Wrong mu dimension")
    product_profile = Counter(mul(u, v) for u in center_profile for v in center_profile)
    require(sum(product_profile.values()) == 100, "Wrong center-product rank")
    x = sp.Symbol("x")
    cases = []
    for ring_id, obstructing_codegree, expected in [
        ("R7_5_3895", 4, (x-16)**2*(x-5)**2*(x-4)*(x*x-1440*x+6400)),
        ("R7_5_5039", 8, (x-8)**3*(x-5)**2*(x*x-1440*x+6400)),
    ]:
        matches = [r for r in census if r["id"] == ring_id]
        require(len(matches) == 1, "Wrong census row count")
        tensor = matches[0]["tensor"]
        require(all(tensor[i][j] == tensor[j][i] for i in range(7) for j in range(7)),
                "Induced-unit computation expects commutative ring")
        matrices = [sp.Matrix(m) for m in tensor]
        casimir = sum((m*m.T for m in matrices), sp.zeros(7))
        require(casimir.charpoly(x).as_expr().expand() == expected.expand(),
                "Casimir polynomial mismatch")
        target = tuple(z // obstructing_codegree for z in D)
        require(tuple(z*obstructing_codegree for z in target) == D, "Nonintegral target pair")
        require(target not in product_profile, "Proposed Morita model not ruled out")
        cases.append({
            "ring_id": ring_id,
            "tensor_sha256": hashlib.sha256(json.dumps(tensor, separators=(",", ":")).encode()).hexdigest(),
            "obstructing_formal_codegree": obstructing_codegree,
            "required_induced_unit_simple_dimension": list(target),
            "present_in_proposed_center": False,
        })
    result = {
        "coefficient_convention": "[r,s] means r+s*sqrt(5)",
        "source": "Grossman-Izumi arXiv:1501.07679v2, Section 6, Figure 6 and Example 6.9",
        "two_d_two_global_dimension": [20, 8],
        "two_d_two_center_profile": [list(p) for p in center_profile],
        "proposed_center_product_profile": [
            {"dimension": list(p), "multiplicity": m}
            for p, m in sorted(product_profile.items())
        ],
        "cases": cases,
        "excluded_model_route": "Morita equivalence to 2D2 boxtimes 2D2^op or to Z(2D2)",
        "general_categorification_excluded": False,
        "arithmetic_verification": "PASS",
    }
    (HERE / "two_d_two_comparison_result.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact exploratory structure for R7_5_4530 and R7_5_4531.

No model and no general fusion-category exclusion are claimed. The
compression consequence is restricted to spherical categorifications.
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dihedral_tensor(elementary):
    representatives = [(1, 0), (0, 1), (1, 1), (1, 2)] if elementary else [1, 2, 3, 4]
    zero = (0, 0) if elementary else 0
    def add(a, b):
        return tuple((x+y) % 3 for x, y in zip(a, b)) if elementary else (a+b) % 9
    def neg(a):
        return tuple(-x % 3 for x in a) if elementary else -a % 9
    tensor = [[[0]*6 for _ in range(6)] for _ in range(6)]
    for i in range(6):
        tensor[0][i][i] = tensor[i][0][i] = 1
    tensor[1][1][0] = 1
    for i in range(2, 6):
        tensor[1][i][i] = tensor[i][1][i] = 1
    for i, a in enumerate(representatives, 2):
        for j, b in enumerate(representatives, 2):
            for c in [add(a, b), add(a, neg(b))]:
                if c == zero:
                    tensor[i][j][0] += 1
                    tensor[i][j][1] += 1
                else:
                    k = next(k for k, r in enumerate(representatives, 2) if c in (r, neg(r)))
                    tensor[i][j][k] += 1
    return tensor


def main():
    census = json.loads((ROOT / "supplements/rank7/output/m5/census.json").read_text())
    x = sp.Symbol("x")
    field_polynomial = x**3 - 3*x - 1
    def red(v):
        return sp.rem(v, field_polynomial, x).expand()
    a = 3*x*x + 3*x
    d = 3*x*x + 6*x + 2
    dimensions = [sp.Integer(1), a, d-1, d, d, d, d]
    D = red(sum(v*v for v in dimensions))
    P = 3*(x*x+x+1)
    require(red(D-P*P*(1+x)**2) == 0, "Quantum-group dimension comparison failed")
    reports = []
    for ring_id, elementary, embedding in [
        ("R7_5_4530", False, [0, 2, 3, 6, 4, 5]),
        ("R7_5_4531", True, [0, 2, 3, 4, 5, 6]),
    ]:
        matches = [r for r in census if r["id"] == ring_id]
        require(len(matches) == 1, "Wrong census row count")
        tensor = matches[0]["tensor"]
        base = dihedral_tensor(elementary)
        expected = [[[0]*7 for _ in range(7)] for _ in range(7)]
        for i in range(7):
            expected[0][i][i] = expected[i][0][i] = 1
        for i in range(1, 6):
            for j in range(1, 6):
                expected[embedding[i]][embedding[j]][1] = 3
                for k in range(6):
                    expected[embedding[i]][embedding[j]][embedding[k]] = base[i][j][k] + (4 if k else 0)
        expected[1][1] = [1, 3, 1, 2, 2, 2, 2]
        for i in range(2, 7):
            expected[1][i] = expected[i][1] = [0, 1 if i == 2 else 2, 3, 3, 3, 3, 3]
        require(expected == tensor, "Generalized dihedral structural identity failed")
        for i in range(7):
            for j in range(7):
                require(red(dimensions[i]*dimensions[j]-sum(tensor[i][j][k]*dimensions[k] for k in range(7))) == 0,
                        "Dimension homomorphism failed")
        matrices = [sp.Matrix(m) for m in tensor]
        casimir = sum((m*m.T for m in matrices), sp.zeros(7))
        f = x**3-3078*x*x+32805*x-59049
        require(casimir.charpoly(x).as_expr().expand() == ((x-9)**4*f).expand(),
                "Casimir polynomial failed")
        reports.append({
            "ring_id": ring_id,
            "tensor_sha256": hashlib.sha256(json.dumps(tensor, separators=(",", ":")).encode()).hexdigest(),
            "dihedral_group": "(C3 x C3) semidirect C2, inversion action" if elementary else "C9 semidirect C2, inversion action",
            "dihedral_basis_to_census": embedding,
            "tensor_coefficients_checked": 343,
        })
    # The three reciprocal algebraic codegrees have elementary symmetric
    # sums s1=5/9 and s2=38/729. For a nontrivial C3 character their
    # Fourier modulus squared is s1^2-3*s2, regardless of root ordering.
    variance = Fraction(5, 9)**2 - 3*Fraction(38, 729)
    lhs = 3*variance
    upper_bound = Fraction(3, 9)
    require(variance == Fraction(37, 243), "Wrong cubic Fourier magnitude")
    require(lhs > upper_bound and lhs/4 < upper_bound, "Wrong scope distinction")
    square_root_poly = x**3-54*x*x-81*x+243
    require(sp.expand(square_root_poly*(-square_root_poly.subs(x, -x))) == x**6-3078*x**4+32805*x*x-59049,
            "Square root polynomial identity failed")
    # Its unique negative root lies in (-3,-2); hence neither square root
    # of D is totally positive. A global FP dimension must be totally positive.
    require(square_root_poly.subs(x, -3) < 0 and square_root_poly.subs(x, -2) > 0,
            "Negative conjugate interval failed")
    require(sp.Poly(square_root_poly, x).is_irreducible, "Unexpected reducible square root polynomial")
    receipt = {
        "rings": reports,
        "field": "z^3-3*z-1=0, z=2*cos(pi/9)",
        "dimension_vector": [str(v) for v in dimensions],
        "global_FP_dimension": str(D),
        "casimir_polynomial": "(x-9)^4*(x^3-3078*x^2+32805*x-59049)",
        "nontrivial_C3_Fourier_magnitude_squared": str(variance),
        "spherical_compression_left_side": str(lhs),
        "spherical_compression_upper_bound": str(upper_bound),
        "spherical_categorification_excluded_by_full_induced_unit_theorem": True,
        "general_categorification_excluded": False,
        "known_model_identified": False,
        "center_model_excluded_by_total_positivity": True,
        "arithmetic_verification": "PASS",
    }
    (HERE / "structure_result.json").write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()

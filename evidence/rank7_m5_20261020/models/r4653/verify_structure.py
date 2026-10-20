#!/usr/bin/env python3
"""Exact structural and compression arithmetic for R7_5_4653.

The dihedral deformation is a based-ring identity, not a categorical
construction. The exclusion uses the independently stated full-I(1)
compression theorem in manuscripts/rank7/papers/full_I1_compression.tex.
"""

import hashlib
import json
from fractions import Fraction
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
RING_ID = "R7_5_4653"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dihedral_tensor():
    """Rep(D22): 1, sign, and the five two-dimensional characters."""
    tensor = [[[0] * 7 for _ in range(7)] for _ in range(7)]
    for i in range(7):
        tensor[0][i][i] = tensor[i][0][i] = 1
    tensor[1][1][0] = 1
    for i in range(2, 7):
        tensor[1][i][i] = tensor[i][1][i] = 1
    for i in range(1, 6):
        for j in range(1, 6):
            for z in [i + j, i - j]:
                k = min(z % 11, (-z) % 11)
                if k == 0:
                    tensor[i + 1][j + 1][0] += 1
                    tensor[i + 1][j + 1][1] += 1
                else:
                    tensor[i + 1][j + 1][k + 1] += 1
    return tensor


def main():
    census = json.loads((ROOT / "supplements/rank7/output/m5/census.json").read_text())
    rows = [row for row in census if row["id"] == RING_ID]
    require(len(rows) == 1, "Expected one census row")
    tensor = rows[0]["tensor"]
    require(len(tensor) == 7 and all(len(x) == 7 for x in tensor), "Wrong rank")
    require(all(len(x) == 7 for matrix in tensor for x in matrix), "Wrong shape")
    require(all(type(n) is int and 0 <= n <= 5 for a in tensor for b in a for n in b),
            "Wrong coefficient range")
    permutation = [0, 1, 2, 6, 3, 5, 4]
    dihedral = dihedral_tensor()
    for i in range(7):
        for j in range(7):
            for k in range(7):
                deformation = 4 if i and j and k else 0
                require(tensor[permutation[i]][permutation[j]][permutation[k]]
                        == dihedral[i][j][k] + deformation,
                        "Dihedral deformation identity failed")

    matrices = [sp.Matrix(a) for a in tensor]
    casimir = sum((a * a.T for a in matrices), sp.zeros(7))
    x = sp.Symbol("x")
    expected = (x - 11) ** 5 * (x ** 2 - 3960 * x + 7260)
    require(casimir.charpoly(x).as_expr().expand() == expected.expand(),
            "Casimir characteristic polynomial mismatch")
    q = 165
    require(sp.factorint(q) == {3: 1, 5: 1, 11: 1} and q % 4 == 1,
            "Expected fundamental discriminant")
    require(3960 ** 2 - 4 * 7260 == 308 ** 2 * q, "Wrong quadratic field")
    compression = Fraction(q * (3960 ** 2 - 4 * 7260), 7260 ** 2)
    require(compression == 49 and compression > 4, "Compression arithmetic failed")
    d = 13 + sp.sqrt(165)
    dimensions = [1, d - 1] + [d] * 5
    for i in range(7):
        for j in range(7):
            require(sp.expand(dimensions[i] * dimensions[j] - sum(
                tensor[i][j][k] * dimensions[k] for k in range(7))) == 0,
                "FP dimension equation failed")
    require(sp.expand(sum(t*t for t in dimensions)) == 1980 + 154*sp.sqrt(165),
            "Global dimension mismatch")

    result = {
        "ring_id": RING_ID,
        "tensor_sha256": hashlib.sha256(json.dumps(tensor, separators=(",", ":")).encode()).hexdigest(),
        "dihedral_model": "Rep(D22), D22 the dihedral group of order 22",
        "dihedral_deformation_parameter": 4,
        "model_to_census_permutation": permutation,
        "deformation_rule": "Add 4 to every coefficient with all three indices nonzero",
        "tensor_coefficients_checked": 343,
        "categorical_model_claimed": False,
        "casimir_characteristic_polynomial": "(x-11)^5*(x^2-3960*x+7260)",
        "quadratic_fundamental_discriminant": q,
        "full_induced_unit_compression_Q": str(compression),
        "general_categorification_upper_bound": 4,
        "sphericalization_contribution_Q_over_4": str(compression / 4),
        "arithmetic_verification": "PASS",
        "theorem_reference": "manuscripts/rank7/papers/full_I1_compression.tex, Boundary constraint for an arbitrary categorification",
    }
    (HERE / "structure_result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

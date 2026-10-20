#!/usr/bin/env python3
"""Reconstruct the complete normalized Galois transport over Q(sqrt(5)).

All calculations are rational and exact.  This certifies a necessary Galois
transport, not a categorification or exclusion by itself.  Import verify_all()
to obtain the checked matrices; run the file to check its committed receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "supplements/rank7/software"))
from rings import Characters, validate  # noqa: E402
from exact import t  # noqa: E402

CASES = {
    "R7_5_3895": {
        "sha256": "590b613093643a1c3047e866213050ba7fd87c211a42906de823d0c613d11ad0",
        "dimension_a": [1, 5, 5, 10, 8, 8, 9],
        "dimension_b": [0, 2, 2, 4, 4, 4, 4],
        "D_a": 720, "D_b": 320, "radicand": 5,
        "rational_codegrees": [4, 16, 16, 5, 5],
        "swap": [4, 5],
    },
    "R7_5_5039": {
        "sha256": "8606c63a2f02ea028185db755a4b055382073b94736d5040ee92f3eec07f450c",
        "dimension_a": [1, 5, 5, 8, 8, 10, 9],
        "dimension_b": [0, 2, 2, 4, 4, 4, 4],
        "D_a": 720, "D_b": 320, "radicand": 5,
        "rational_codegrees": [8, 8, 8, 5, 5],
        "swap": [3, 4],
    },
}
CONTROL = {
    "sha256": "2fac7e9b2ba6ee55e35443af3ac36221f20b56b60a6224e0137813bc2365fa8c",
    "dimension_a": [1, 1, 4, 5, 5, 4, 6],
    "dimension_b": [0, 0, 1, 1, 1, 1, 2],
    "D_a": 240, "D_b": 60, "radicand": 15,
    "rational_codegrees": [12, 6, 6, 5, 4],
    "swap": None,
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def evaluate_matrix(coefficients, matrix):
    """Evaluate ascending rational coefficients by Horner's rule."""
    out = s.zeros(matrix.rows)
    for coefficient in reversed(coefficients):
        out = out * matrix + coefficient * s.eye(matrix.rows)
    return out


def reconstruct_transport(tensor, radicand):
    """Return T and its CRT proof, without roots or numerical approximations."""
    algebra = Characters(tensor)
    q = s.Poly(0, t, domain=s.QQ)
    component_records = []
    for factor, multiplicity in algebra.components:
        require(multiplicity == 1, "separating polynomial is not squarefree")
        discriminant = s.discriminant(factor)
        conjugated = (factor.degree() == 2 and discriminant > 0
                      and s.sqrt(discriminant / radicand).is_Rational is True)
        require(factor.degree() in (1, 2), "unexpected character field degree")
        residue = s.Poly(-factor.nth(1) - t if conjugated else t,
                         t, domain=s.QQ)
        complementary = algebra.p.exquo(factor)
        q = (q + residue * complementary * s.invert(complementary, factor)).rem(algebra.p)
        component_records.append({
            "factor_descending": [str(x) for x in factor.all_coeffs()],
            "discriminant": str(discriminant),
            "conjugated": bool(conjugated),
            "residue_descending": [str(x) for x in residue.all_coeffs()],
        })
    for record, (factor, _) in zip(component_records, algebra.components):
        residue = s.Poly.from_list(list(map(s.Rational, record["residue_descending"])), t)
        require((q - residue).rem(factor).is_zero, "CRT residue mismatch")
    require(s.Poly(q.as_expr().subs(t, q.as_expr()) - t, t).rem(algebra.p).is_zero,
            "CRT automorphism is not involutive")
    h_conjugate = evaluate_matrix(list(reversed(q.all_coeffs())), algebra.H)
    conjugates = [evaluate_matrix(coefficients, h_conjugate)
                  for coefficients in algebra.coeff]
    n = len(tensor)
    for i in range(n):
        for j in range(n):
            require(conjugates[i] * conjugates[j]
                    == sum((tensor[i][j][k] * conjugates[k] for k in range(n)), s.zeros(n)),
                    "transported fusion matrices do not define an algebra homomorphism")
    conjugate_casimir = sum((conjugates[i] * conjugates[algebra.du[i]]
                            for i in range(n)), s.zeros(n))
    weight = algebra.C * conjugate_casimir.inv()
    transport = s.Matrix.hstack(*[(weight * matrix)[0, :].T for matrix in conjugates])
    require(transport * transport == s.eye(n), "normalized transport is not involutive")
    return transport, {
        "separating_k": int(algebra.k),
        "separating_polynomial_descending": [str(x) for x in algebra.p.all_coeffs()],
        "components": component_records,
        "crt_polynomial_descending": [str(x) for x in q.all_coeffs()],
    }


def check_case(ring_id, tensor, case):
    digest = hashlib.sha256(json.dumps(tensor, separators=(",", ":")).encode()).hexdigest()
    require(digest == case["sha256"], f"source tensor checksum mismatch: {ring_id}")
    validate(tensor)
    aa, bb = s.Matrix(case["dimension_a"]), s.Matrix(case["dimension_b"])
    radicand = case["radicand"]
    # Check the positive dimension character in its exact quadratic basis.
    require(aa[0] == 1 and bb[0] == 0 and all(x >= 0 for x in aa)
            and all(x >= 0 for x in bb), "dimension positivity or normalization")
    for i in range(7):
        for j in range(7):
            require(aa[i] * aa[j] + radicand * bb[i] * bb[j]
                    == sum(tensor[i][j][k] * aa[k] for k in range(7)), "rational dimension part")
            require(aa[i] * bb[j] + bb[i] * aa[j]
                    == sum(tensor[i][j][k] * bb[k] for k in range(7)), "irrational dimension part")
    require(sum(aa[i] ** 2 + radicand * bb[i] ** 2 for i in range(7)) == case["D_a"]
            and sum(2 * aa[i] * bb[i] for i in range(7)) == case["D_b"], "global dimension")
    transport, proof = reconstruct_transport(tensor, radicand)
    algebra = Characters(tensor)
    expected_cp = (t ** 2 - 2 * case["D_a"] * t
                   + case["D_a"] ** 2 - radicand * case["D_b"] ** 2)
    for degree in case["rational_codegrees"]:
        expected_cp *= t - degree
    require(algebra.C.charpoly(t).as_poly() == s.Poly(expected_cp, t), "formal codegree polynomial")
    permutation = s.eye(7)
    if case["swap"]:
        first, second = case["swap"]
        permutation.row_swap(first, second)
    compact = permutation + bb * (aa - s.Rational(case["D_a"], case["D_b"]) * bb).T
    require(transport == compact, "compact full-character transport formula")
    require(transport[:, 0] == s.eye(7)[:, 0] + bb, "forced Galois unit row")
    return {**case, "T": transport, "forced_unit": transport[:, 0], "proof": proof}


def verify_all():
    """Return dict[id] with checked SymPy T, forced_unit, dimensions and proof."""
    census = json.loads((ROOT / "supplements/rank7/output/m5/census.json").read_text())
    by_id = {entry["id"]: entry["tensor"] for entry in census}
    require(len(by_id) == len(census), "duplicate source IDs")
    check_case("R7_5_443", by_id["R7_5_443"], CONTROL)
    return {ring_id: check_case(ring_id, by_id[ring_id], case)
            for ring_id, case in CASES.items()}


def receipt(results):
    return {
        "schema": "rank7-quadratic-galois-row-transport-v1",
        "scope": "Exact normalized character transport; no exclusion by itself.",
        "convention": "T is row-major and acts on column multiplicity vectors.",
        "control": "R7_5_443: T=I+b*(a-4*b)^transpose, checked exactly.",
        "rings": {ring_id: {
            **{key: value for key, value in result.items() if key not in ("T", "forced_unit")},
            "T": [[str(x) for x in row] for row in result["T"].tolist()],
            "forced_unit": [str(x) for x in result["forced_unit"]],
        } for ring_id, result in results.items()},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-receipt", action="store_true")
    args = parser.parse_args()
    result = receipt(verify_all())
    path = HERE / "transport_certificate.json"
    if args.write_receipt:
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        require(json.loads(path.read_text()) == result, "stored transport receipt differs")
    print("PASS: pinned tensors, complete CRT transport, codegrees, involutions and R443 control")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Conditional strict-HI obstruction; does NOT certify general categorification exclusion.

Default replay is read-only; --write explicitly regenerates the deterministic receipt.
"""
import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
CENSUS = HERE.parents[2] / "rank8_m3_20261021/pipeline/census_m3.json"
EXPECTED_SHA = "358b5323c54c66e80684b34dbe39d7bff44c5fe227bb8fb188794a0a9a722d88"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def build():
    records = json.loads(CENSUS.read_text())
    source = next(r for r in records if r["id"] == "R8_3_455")
    tensor = source["tensor"]
    sha = hashlib.sha256(json.dumps(tensor, separators=(",", ":")).encode()).hexdigest()
    require(sha == source["tensor_sha256"] == EXPECTED_SHA, "source tensor hash")
    neutral, odd, pointed, y = [0, 1, 2, 3, 6, 7], [4, 5], [0, 1, 2], 4
    degree = [int(i in odd) for i in range(8)]
    for i in range(8):
        for j in range(8):
            for k in range(8):
                require(not tensor[i][j][k] or degree[k] == (degree[i] + degree[j]) % 2,
                        "faithful C2 grading")
    require(tensor[y][y] == [int(k in pointed) for k in range(8)], "Y squared")
    for g in pointed:
        require(tensor[g][y] == tensor[y][g] == [int(k == y) for k in range(8)], "pointed fixed Y")
    for g in pointed:
        for h in pointed:
            require(tensor[g][h] == [int(k == (g+h) % 3) for k in range(8)], "pointed C3")

    c, a, b, f, g, z, u = sp.symbols("c a b f g z u")
    variables = (c, a, b, f, g)
    matrix = sp.Matrix([[c, a, b], [a, b, f], [b, g, a]])
    fixed = sp.Matrix([[3*b+g, b, b], [b, b, g], [b, g, b]])
    transform = sp.Matrix(3, 3, lambda i, j: sp.expand(sum(
        matrix[x, yy] * z**((i*yy-j*x) % 3) for x in range(3) for yy in range(3)) / 3))
    linear_results = []
    for automorphism in (1, -1):
        equations = []
        for i in range(3):
            for j in range(3):
                p = sp.rem(transform[i, j] - matrix[(automorphism*i) % 3, (automorphism*j) % 3],
                           z*z+z+1, z)
                equations.extend(sp.Poly(p, z).all_coeffs())
        coefficients, constant = sp.linear_eq_to_matrix(equations, variables)
        require(constant == sp.zeros(len(equations), 1), "homogeneous Fourier equations")
        require(coefficients.rank() == 3, "Fourier kernel dimension")
        substitution = {c: 3*b+g, a: b, f: g}
        require(all(sp.expand(p.subs(substitution)) == 0 for p in equations), "Fourier kernel parametrization")
        linear_results.append({"automorphism": automorphism, "rank": 3, "kernel_dimension": 2})

    # E2 and the E3 equations (h,k)=(0,1),(1,0),(1,1), after Fourier fixedness.
    e2 = sum(fixed[h, 0] for h in range(3)) + u
    def e3(h, k):
        return sp.expand(sum(fixed[(h+x) % 3, k]*fixed[k, x] for x in range(3))
                         - int(h == 0) + u*int(k == 0))
    polys = [sp.expand(e2), e3(0, 1), e3(1, 0), e3(1, 1)]
    expected = [5*b+g+u, 2*b*b+g*g-1, 7*b*b+2*b*g+u, b*(b+2*g)]
    require(all(sp.expand(p-q) == 0 for p, q in zip(polys, expected)), "HI equation transcription")
    basis = sp.groebner(polys, g, b, u, domain=sp.QQ)
    require(list(basis) == [1], "inconsistent strict Fourier-fixed HI equations")
    # Elementary branch certificate, independent of the Groebner algorithm.
    # b=0 gives u=0 from E3(1,0), g=0 from E2, then E3(0,1)=-1.
    require(polys[1].subs({b: 0, g: 0, u: 0}) == -1, "zero branch contradiction")
    # b!=0 gives g=-b/2, u=-9b/2; E3(1,0)=b(12b-9)/2.
    require(sp.expand(polys[2].subs({g: -b/2, u: -9*b/2}) - b*(12*b-9)/2) == 0,
            "nonzero branch factor")
    require(polys[1].subs({b: sp.Rational(3,4), g: -sp.Rational(3,8)}) == sp.Rational(17,64),
            "nonzero branch contradiction")
    return {
        "id": source["id"], "source_tensor_sha256": sha,
        "status": "conditional_strict_HI_presentation_obstruction",
        "general_complex_exclusion": False,
        "remaining_gap": "No converse from arbitrary abstract untwisted complex HI(C3) categorifications to the strict Evans-Gannon matrix presentation is proved here.",
        "neutral_basis": neutral, "odd_basis": odd, "pointed_basis": pointed, "fixed_simple": y,
        "grading_coefficient_checks": 512,
        "Fourier_linear_systems": linear_results,
        "Fourier_fixed_matrix": [["3*b+g", "b", "b"], ["b", "b", "g"], ["b", "g", "b"]],
        "necessary_polynomials": [str(p) for p in polys],
        "Groebner_basis": ["1"],
        "elementary_branch_residuals": ["-1", "17/64"],
        "scope": "No R455 categorification whose neutral category is an Evans-Gannon strict HI(C3) matrix category; in particular the known Haagerup categories and their Galois conjugates are ruled out as neutral categories."
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = build()
    path = HERE / "conditional_fourier.json"
    if args.write:
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        require(json.loads(path.read_text()) == result, "saved receipt differs")
    print("PASS: R455 conditional strict-HI obstruction; general complex exclusion NOT established")


if __name__ == "__main__":
    main()

"""Small exact checks supporting the R3472 simple-center application.

This checks ring data, not categorical existence or the signed-quotient
sphericalization theorem. The latter is an explicitly cited prior input.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / "site/dist/downloads/fusion-tensors/R8_3_3472.txt"
EXPECTED = "33984d45e69ff778e70847def8349abda79ed6c0eaea242a73b533649f9b153a"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def run():
    R = json.loads(SOURCE.read_text())
    digest = hashlib.sha256(json.dumps(R, separators=(",", ":")).encode()).hexdigest()
    require(digest == EXPECTED, "canonical tensor differs")
    n = len(R)
    require(n == 8, "rank differs")
    N = [sp.Matrix([[R[i][j][k] for j in range(n)] for k in range(n)]) for i in range(n)]
    require(N[0] == sp.eye(n), "unit differs")
    require(all(N[i] == N[i].T for i in range(n)), "self-duality differs")
    require(all(N[i]*N[j] == sum((R[i][j][k]*N[k] for k in range(n)), sp.zeros(n))
                for i in range(n) for j in range(n)), "fusion multiplication fails")
    subrings = []
    for mask in range(1 << (n-1)):
        subset = [0] + [i for i in range(1, n) if mask & (1 << (i-1))]
        if all(not R[i][j][k] or k in subset for i in subset for j in subset for k in range(n)):
            subrings.append(subset)
    require(subrings == [[0], list(range(n))], "based ring is not simple")
    r = sp.sqrt(2)
    dims = [1, 6+5*r, 6+5*r, 7+5*r, 6+5*r, 8+5*r, 8+5*r, 8+5*r]
    require(all(sp.expand(dims[i]*dims[j]-sum(R[i][j][k]*dims[k] for k in range(n))) == 0
                for i in range(n) for j in range(n)), "dimension character fails")
    require(all(d > 0 for d in dims), "not positive dimensions")
    D = sp.expand(sum(d*d for d in dims))
    require(D == 700+490*r, "global dimension differs")
    casimir = sum((M*M for M in N), sp.zeros(n))
    x = sp.Symbol("x")
    p = casimir.charpoly(x).as_expr()
    require(sp.expand(p-(x-7)**6*(x*x-1400*x+9800)) == 0, "codegrees differ")
    min_square = [int(min(N[i]**2)) for i in range(1, n)]
    require(min(min_square) > 0, "a nonunit fusion square is not positive")
    # A quadratic algebraic integer x with x^2-12x-14=0 is not a
    # d-number, since its norm -14 does not divide trace(x)^2=144.
    require(144 % 14 != 0, "d-number witness fails")
    return {
        "kind": "exact_R3472_simple_center_inputs",
        "tensor_sha256": digest,
        "based_fusion_subrings": subrings,
        "FP_dimensions": [[1,0],[6,5],[6,5],[7,5],[6,5],[8,5],[8,5],[8,5]],
        "FP_global_dimension": [700,490],
        "formal_codegrees": {"rational_7_multiplicity": 6, "quadratic_polynomial": [1,-1400,9800]},
        "distinguished_center_dimensions": {"unit": [1,0], "dimension_conjugate": [99,70], "six_others": [100,70]},
        "minimum_entry_of_nonunit_fusion_squares": min_square,
        "nonbraided_d_number_witness": {"polynomial": [1,-12,-14], "norm": -14, "squared_trace": 144},
        "categorical_input": "The previously certified general sphericalization and pseudo-unitary Galois-conjugacy theorem is required.",
        "categorical_conclusion": "Conditional on a complex categorification, its Drinfeld center is simple, by Liu-Palcoux-Ren Theorem 5.1.",
        "classification_status": "unresolved"
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = run()
    receipt = HERE / "structure.json"
    if args.write:
        receipt.write_text(json.dumps(result, indent=2)+"\n")
    else:
        require(json.loads(receipt.read_text()) == result, "receipt differs")
    print("PASS R3472 simple-center inputs; categorification remains unresolved")

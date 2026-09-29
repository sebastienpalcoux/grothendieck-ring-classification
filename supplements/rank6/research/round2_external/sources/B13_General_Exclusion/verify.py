#!/usr/bin/env python3
"""Exact finite certificate for the exclusion of B_13.

Python standard library only. All arithmetic is rational or integral. The
categorical theorems and the proofs of the finite bounds are in proof.pdf.
Explicit checks remain active under python -O. No census or network is used.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import itertools
import json
import math
from fractions import Fraction as F
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def tensor() -> list[list[list[int]]]:
    n = 6
    out = [[[0] * n for _ in range(n)] for _ in range(n)]
    for i in range(n):
        out[0][i][i] = out[i][0][i] = 1
    # Corrections to 12(a+b+c+d+e), in basis (1,a,b,c,d,e).
    corrections = {
        (1, 1): (1, 1, -2, -1, 0, 1),
        (1, 2): (0, -2, 1, 1, 1, -1),
        (1, 3): (0, -1, 1, -1, 0, 0),
        (1, 4): (0, 0, 1, 0, 0, 0),
        (1, 5): (0, 1, -1, 0, 0, 1),
        (2, 2): (1, 1, -3, 1, 1, 1),
        (2, 3): (0, 1, 1, -2, -1, 1),
        (2, 4): (0, 1, 1, -1, 0, 1),
        (2, 5): (0, -1, 1, 1, 1, 0),
        (3, 3): (1, -1, -2, 1, 1, 0),
        (3, 4): (0, 0, -1, 1, 1, 0),
        (3, 5): (0, 0, 1, 0, 0, 0),
        (4, 4): (1, 0, 0, 1, 1, 1),
        (4, 5): (0, 0, 1, 0, 1, 1),
        (5, 5): (1, 1, 0, 0, 1, 1),
    }
    for (i, j), row in corrections.items():
        values = [value + (12 if k else 0) for k, value in enumerate(row)]
        out[i][j] = values.copy()
        out[j][i] = values.copy()
    return out


# Exact arithmetic in Q(sqrt(5), sqrt(149)). Bit-mask basis: 1,s,r,sr.
def q(a=0, b=0, c=0, d=0):
    return tuple(map(F, (a, b, c, d)))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(n, a):
    return tuple(F(n) * x for x in a)


def mul(a, b):
    out = [F(0)] * 4
    for i in range(4):
        for j in range(4):
            common = i & j
            factor = (5 if common & 1 else 1) * (149 if common & 2 else 1)
            out[i ^ j] += a[i] * b[j] * factor
    return tuple(out)


def total(values):
    result = q()
    for value in values:
        result = add(result, value)
    return result


def dot(a, b):
    return total(mul(x, y) for x, y in zip(a, b))


def determinant_integer(matrix: list[list[int]]) -> int:
    """Bareiss elimination; exact integer determinant, with row pivoting."""
    a = [row.copy() for row in matrix]
    n, sign, previous = len(a), 1, 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot = next((i for i in range(k + 1, n) if a[i][k]), None)
            if pivot is None:
                return 0
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = pivot * a[i][j] - a[i][k] * a[k][j]
                require(numerator % previous == 0, "Nonexact Bareiss division")
                a[i][j] = numerator // previous
        for i in range(k + 1, n):
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]


def norm_numerator(x: int, y: int, m: int, w: int) -> int:
    """Independent norm of x+y*s+m*r+w*s*r via its 4x4 matrix."""
    coefficients = (x, y, m, w)
    matrix = [[0] * 4 for _ in range(4)]
    for i, value in enumerate(coefficients):
        for j in range(4):
            common = i & j
            factor = (5 if common & 1 else 1) * (149 if common & 2 else 1)
            matrix[i ^ j][j] += value * factor
    return determinant_integer(matrix)


def check_ring(N):
    indices = range(6)
    require(all(type(x) is int and x >= 0 for mat in N for row in mat for x in row),
            "Nonintegral or negative coefficient")
    for i, j, k in itertools.product(indices, repeat=3):
        require(N[0][i][j] == int(i == j), "Unit failure")
        require(N[i][j][0] == int(i == j), "Self-duality failure")
        require(N[i][j][k] == N[j][i][k] == N[i][k][j], "Reciprocity failure")
    for i, j, k, ell in itertools.product(indices, repeat=4):
        left = sum(N[i][j][h] * N[h][k][ell] for h in indices)
        right = sum(N[j][k][h] * N[i][h][ell] for h in indices)
        require(left == right, "Associativity failure")
    require(max(x for mat in N for row in mat for x in row) == 13, "Multiplicity mismatch")
    require(all(all(N[i][i][j] > 0 for j in indices) for i in range(1, 6)),
            "Square-support simplicity test failed")
    trace = sum(x * x for mat in N for row in mat for x in row)
    require(trace == 18725, "Casimir trace mismatch")
    return trace


def check_characters(N):
    rows = []
    for sign in (1, -1):
        u = q(F(61, 2), 0, F(5 * sign, 2))
        rows.append([q(1), add(u, q(-1)), u, add(u, q(-1)),
                     add(u, q(1)), add(u, q(1))])
    for sign in (1, -1):
        p = q(-2, sign)
        h = q(F(-1, 2), F(sign, 2))
        k = q(F(3, 2), F(-sign, 2))
        rows.extend([[q(1), scale(-1, p), p, h, q(-1), k],
                     [q(1), h, p, scale(-1, p), k, q(-1)]])
    for row in rows:
        for i, j in itertools.product(range(6), repeat=2):
            rhs = total(scale(N[i][j][k], row[k]) for k in range(6))
            require(mul(row[i], row[j]) == rhs, "Character equation failed")
    for i, j in itertools.combinations(range(6), 2):
        require(dot(rows[i], rows[j]) == q(), "Character orthogonality failed")
    codes = [dot(row, row) for row in rows]
    expected = [q(F(18625, 2), 0, F(1525, 2)),
                q(F(18625, 2), 0, F(-1525, 2)),
                q(25, -10), q(25, -10), q(25, 10), q(25, 10)]
    require(codes == expected, "Formal codegree mismatch")
    u = q(F(61, 2), 0, F(5, 2))
    require(mul(u, add(u, q(-61))) == q(1), "Unit identity failed")
    require(mul(q(0, 0, 25), u) == codes[0], "D=25*r*u identity failed")
    require(mul(codes[0], codes[1]) == q(93125), "Norm(D) mismatch")
    return [[str(x) for x in f] for f in codes]


def check_integral_basis():
    # The product basis has discriminant 5^2*149^2. Only these primes can
    # divide its index in the maximal order. The other quadratic polynomial
    # splits simply at each such prime, giving the local maximal orders.
    phi, eta = q(F(1, 2), F(1, 2)), q(F(1, 2), 0, F(1, 2))
    basis = [q(1), phi, eta, mul(phi, eta)]
    gram = [[4 * mul(a, b)[0] for b in basis] for a in basis]
    require(all(x.denominator == 1 for row in gram for x in row), "Nonintegral basis trace")
    discriminant = determinant_integer([[int(x) for x in row] for row in gram])
    require(discriminant == 5**2 * 149**2, "Integral basis discriminant mismatch")
    roots_5 = [t for t in range(5) if (t*t-t-37) % 5 == 0]
    roots_149 = [t for t in range(149) if (t*t-t-1) % 149 == 0]
    require(roots_5 == [2, 4], "Splitting at 5 failed")
    require(roots_149 == [41, 109], "Splitting at 149 failed")
    for prime, roots in ((5, roots_5), (149, roots_149)):
        require(all((2*t-1) % prime for t in roots), "Nonsimple residue root")
    # Exact outward integer bounds used by the search.
    require(25 * 149 < 62**2 and 5 * 149 < 28**2, "Search bounds failed")
    return {"product_basis_discriminant": discriminant,
            "eta_roots_mod_5": roots_5, "phi_roots_mod_149": roots_149}


def check_global_dimensions(csv_path: Path | None):
    counts = {m: 0 for m in range(1, 6)}
    kept_counts = {m: 0 for m in range(1, 6)}
    survivors, records = [], []
    for m in range(1, 6):
        for w, x, y in itertools.product(range(-2, 3), range(-61, 62), range(-27, 28)):
            if 5*w*w >= m*m:
                continue
            if (y-w) % 2 or (m-w) % 2 or (x-y-m+w) % 4:
                continue
            A = 149*(m*m + 5*w*w) - x*x - 5*y*y
            B = 298*m*w - 2*x*y
            # Together with m>|w|sqrt(5), this is exactly total positivity
            # of Delta=(25/4)(149m+149w*s+x*r+y*s*r).
            if A <= 0 or A*A <= 5*B*B:
                continue
            counts[m] += 1
            numerator = A*A - 5*B*B
            require(numerator == norm_numerator(x, y, m, w),
                    "Norm formula / determinant disagreement")
            require(numerator % 256 == 0, "Nonintegral norm of an integer")
            norm_theta = numerator // 256
            keep = (149**2 * m**4) % norm_theta == 0
            records.append((m, w, x, y, norm_theta, int(keep)))
            if keep:
                kept_counts[m] += 1
                survivors.append((m, w, x, y, norm_theta))
    require(counts == {1: 0, 2: 66, 3: 132, 4: 267, 5: 664},
            "Positive-candidate counts changed")
    require(survivors == [(4, 0, 0, 0, 22201)], "Unexpected global dimension")
    if csv_path is not None:
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(("m", "w", "x", "y", "norm_theta", "norm_divides_trace_power"))
            writer.writerows(records)
    return {"positive_counts": counts, "norm_survivor_counts": kept_counts,
            "total_positive_candidates": len(records),
            "independent_norm_determinants_checked": len(records),
            "survivors_m_w_x_y_norm": survivors,
            "only_possible_global_dimension": 3725}


def check_residual_codegrees(trace: int):
    delta = 3725
    require(math.gcd(delta, delta - 4) == 1, "Unexpected common divisor")
    # S must be a positive multiple of delta-4, and 4*delta+S <= trace.
    possibilities = list(range(delta - 4, trace - 4*delta + 1, delta - 4))
    require(possibilities == [3721], "Residual trace is not forced")
    S = possibilities[0]
    require(delta*S % (delta-4) == 0, "Residual norm not integral")
    P = delta*S // (delta-4)
    require(P == 3725, "Residual norm mismatch")
    discriminant = S*S - 4*P
    root = math.isqrt(discriminant)
    require(root*root < discriminant < (root+1)**2, "Polynomial is reducible")
    remainder = S*S % P
    require(remainder == 16, "Expected quadratic d-number violation missing")
    return {"residual_codegree_polynomial": [1, -S, P],
            "discriminant": discriminant,
            "bounding_squares": [root*root, (root+1)**2],
            "trace_squared_mod_norm": remainder,
            "d_number_condition": "FAIL: 3725 does not divide 3721^2"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("verification.json"))
    parser.add_argument("--candidates", type=Path, help="Write the 1129 positive candidates as CSV")
    args = parser.parse_args()
    N = tensor()
    tensor_path = Path(__file__).resolve().with_name("tensor.json")
    if tensor_path.exists():
        require(json.loads(tensor_path.read_text()) == N, "Supplied tensor differs from multiplication table")
    canonical = json.dumps(N, separators=(",", ":")).encode()
    trace = check_ring(N)
    report = {
        "status": "PASS",
        "scope": "Exact finite checks; categorical inputs and exhaustive bounds are in the proof.",
        "ring": "B_13 (local label)",
        "rank": 6, "multiplicity": 13, "casimir_trace": trace,
        "tensor_sha256_canonical_json": hashlib.sha256(canonical).hexdigest(),
        "ring_checks": {"associativity_equations": 6**4, "unit_duality_reciprocity": "PASS",
                        "simplicity_by_square_support": "PASS"},
        "codegrees_in_basis_1_sqrt5_sqrt149_sqrt745": check_characters(N),
        "integral_basis_checks": check_integral_basis(),
        "dimension_check": check_global_dimensions(args.candidates),
        "final_contradiction": check_residual_codegrees(trace),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("PASS: B_13 exclusion arithmetic verified exactly.")
    print("1129 totally positive candidates; unique norm survivor Delta=3725.")
    print("Residual polynomial x^2-3721x+3725 is irreducible and fails the d-number test.")


if __name__ == "__main__":
    main()

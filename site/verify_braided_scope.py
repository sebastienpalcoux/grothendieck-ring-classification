#!/usr/bin/env python3
"""Fast exact arithmetic for the rank-eight braided-scope corollaries.

This checks canonical tensors and numerical hypotheses, not the categorical
theorems cited in BRAIDED_CATEGORIFICATION.md.  In particular it does not
replay the large R982 center certificates, or reprove the prior pivotal /
spherical / Galois-pseudo-unitary reduction.

R1795: Lacabanne, arXiv:1807.00766v3, Lemma 3.1 and Proposition 3.3,
give quotient formal codegrees (dim(C)/2)/d_i^2 in the self-dual spherical
case with dim(g)=1.  A codegree 5 has no corresponding simple dimension.
R1768/R3472: the squared FP dimensions below fail Ostrik's quadratic
d-number criterion (arXiv:0810.3242, Theorem 1.8 and Lemma 2.7).
"""

import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "evidence/rank8_m3_20261021/pipeline/census_m3.json"
HASHES = {
    "R8_3_982": "f4a9fb77b3a78e9dcd8370ca9fa822ea331f1b71e3fad7990efdd386445fcd1c",
    "R8_3_1768": "240509807c67da437c86f2a51efeb831364734feb93ed18a1d2f32087ebc1af0",
    "R8_3_1795": "feddd2934d44be4872c82ed6c5650bf9d8aac2bc87b72778d88b375726f4cd1f",
    "R8_3_3472": "33984d45e69ff778e70847def8349abda79ed6c0eaea242a73b533649f9b153a",
}
ZERO, ONE = (F(0), F(0)), (F(1), F(0))


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def scale(n, x):
    return n * x[0], n * x[1]


def mul(x, y, q):
    return x[0] * y[0] + q * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def total(values):
    answer = ZERO
    for value in values:
        answer = add(answer, value)
    return answer


def encode(value):
    return [str(coefficient) for coefficient in value]


def character(tensor, values, q):
    need(values[0] == ONE, "non-unital character")
    n = len(tensor)
    for i in range(n):
        for j in range(n):
            need(mul(values[i], values[j], q) == total(
                scale(tensor[i][j][k], values[k]) for k in range(n)),
                "character multiplication identity failed")


def structural(tensor):
    n = len(tensor)
    need(all(tensor[i][j] == tensor[j][i] for i in range(n) for j in range(n)),
         "ring is not commutative")
    dual = [next(j for j in range(n) if tensor[i][j][0]) for i in range(n)]

    def closed(indices):
        return all(dual[i] in indices and all(
            k in indices for j in indices for k, value in enumerate(tensor[i][j])
            if value) for i in indices)

    subrings = []
    for mask in range(1 << (n - 1)):
        indices = {0} | {i for i in range(1, n) if mask & (1 << (i - 1))}
        if closed(indices):
            subrings.append(sorted(indices))
    adjoint = {k for i in range(n) for k, value in enumerate(tensor[i][dual[i]]) if value}
    while not closed(adjoint):
        current = set(adjoint)
        adjoint |= {dual[i] for i in current}
        adjoint |= {k for i in current for j in current
                    for k, value in enumerate(tensor[i][j]) if value}
    need(adjoint == set(range(n)), "adjoint subring is not full")
    return {"duality": dual, "based_subrings": subrings, "full_adjoint": True}


def main():
    census = {row["id"]: row for row in json.loads(CENSUS.read_text())}
    tensors, results = {}, {}
    for ring_id, expected_hash in HASHES.items():
        source = census[ring_id]
        tensor = source["tensor"]
        digest = hashlib.sha256(json.dumps(tensor, separators=(",", ":")).encode()).hexdigest()
        need(digest == source["tensor_sha256"] == expected_hash, ring_id + " tensor mismatch")
        tensors[ring_id] = tensor
        results[ring_id] = {"tensor_sha256": digest, **structural(tensor)}

    specifications = {
        "R8_3_1768": (37, [(1, 0), (1, 0), (5, 1), (6, 1), (7, 1), (7, 1), (6, 1), (5, 1)]),
        "R8_3_1795": (5, [(1, 0), (1, 0), (6, 3), (7, 3), (7, 3), (7, 3), (7, 3), (6, 3)]),
        "R8_3_3472": (2, [(1, 0), (6, 5), (6, 5), (7, 5), (6, 5), (8, 5), (8, 5), (8, 5)]),
    }
    for ring_id, (q, coefficients) in specifications.items():
        values = [tuple(map(F, value)) for value in coefficients]
        # Every constant is strictly positive and every radical coefficient
        # nonnegative: positivity needs no numerical root approximation.
        need(all(a > 0 and b >= 0 for a, b in values), "FP positivity fails")
        character(tensors[ring_id], values, q)
        need(results[ring_id]["duality"] == list(range(8)), "not self-dual")
        results[ring_id]["FP_radicand"] = q
        results[ring_id]["FP_dimensions"] = [encode(value) for value in values]
        if ring_id != "R8_3_1795":
            value = values[2] if ring_id == "R8_3_1768" else values[1]
            squared = mul(value, value, q)
            trace = 2 * squared[0]
            norm = squared[0] ** 2 - q * squared[1] ** 2
            need(squared[1] != 0 and trace.denominator == norm.denominator == 1,
                 "not an integral quadratic squared dimension")
            need(trace * trace % norm != 0, "squared FP dimension passed d-number test")
            results[ring_id]["squared_FP_dimension_not_d_number"] = {
                "squared_dimension": encode(squared), "minimal_polynomial": [1, -int(trace), int(norm)],
                "trace_squared_mod_norm": int(trace * trace % norm),
            }

    ring_id = "R8_3_1795"
    tensor = tensors[ring_id]
    q, coefficients = specifications[ring_id]
    need(results[ring_id]["based_subrings"] == [[0], [0, 1], list(range(8))],
         "R1795 based-subring inventory changed")
    action = []
    for i in range(8):
        product = tensor[1][i]
        need(sum(product) == 1, "g is not invertible")
        action.append(product.index(1))
    need(all(action[i] != i and action[action[i]] == i for i in range(8)),
         "g action is not a free involution")
    representatives = [i for i in range(8) if i < action[i]]
    quotient = [[[tensor[i][j][k] + tensor[i][j][action[k]] for k in representatives]
                 for j in representatives] for i in representatives]
    table_path = ROOT / ("evidence/rank8_frontier_20261021/global_induction/"
                        "complete_results/R8_3_1795_atomic_real_sts_h4.json")
    saved = json.loads(table_path.read_text())
    need(saved["tensor_sha256"] == HASHES[ring_id], "character-table tensor mismatch")
    table = saved["metadata"]["character_table"]
    need(list(map(F, table["field_polynomial"])) == [1, -1636, -45296],
         "unexpected character field")
    # The saved descending-power encoding has u = 818 + 378 sqrt(5).
    u = (F(818), F(378))

    def decode(encoded):
        result = ZERO
        for coefficient in encoded:
            result = add(mul(result, u, q), (F(coefficient), F(0)))
        return result

    need(add(add(mul(u, u, q), scale(-1636, u)), (F(-45296), F(0))) == ZERO,
         "field generator does not satisfy its polynomial")
    rows = [tuple(decode(value) for value in row) for row in table["characters"]]
    need(len(rows) == len(set(rows)) == 8, "incomplete character table")
    for row, saved_degree in zip(rows, table["codegrees"]):
        character(tensor, row, q)
        need(total(mul(value, value, q) for value in row) == decode(saved_degree),
             "saved formal codegree differs")
    positive_rows = [row for row in rows if row[1] == ONE]
    need(len(positive_rows) == 4, "wrong number of g-positive characters")
    quotient_codegrees = []
    for row in positive_rows:
        restricted = [row[i] for i in representatives]
        character(quotient, restricted, q)
        quotient_codegrees.append(total(mul(value, value, q) for value in restricted))
    need(sorted(quotient_codegrees) == sorted([(F(270), F(120)), (F(270), F(-120)),
                                              (F(5), F(0)), (F(5), F(0))]),
         "unexpected quotient formal codegrees")
    fp = [tuple(map(F, value)) for value in coefficients]
    dimension = total(mul(value, value, q) for value in fp)
    need(dimension == (F(540), F(240)), "wrong FP dimension")
    required_square = scale(F(1, 10), dimension)
    actual_squares = sorted(set(mul(value, value, q) for value in fp))
    need(required_square not in actual_squares, "slightly-degenerate contradiction failed")
    results[ring_id].update({
        "g_action": action, "quotient_representatives": representatives,
        "quotient_formal_codegrees": [encode(value) for value in sorted(quotient_codegrees)],
        "required_square_for_quotient_codegree_5": encode(required_square),
        "actual_FP_dimension_squares": [encode(value) for value in actual_squares],
        "missing_required_square": True,
        "Tannakian_rank_four_quotient_dimension": encode(scale(F(1, 2), dimension)),
    })
    print(json.dumps({"status": "PASS", "scope": "exact_tensor_and_arithmetic_checks_only",
                      "not_replayed": ["categorical_theorems", "pivotal_to_Galois_PU_reduction",
                                       "R982_center_certificates"],
                      "rings": results}, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()

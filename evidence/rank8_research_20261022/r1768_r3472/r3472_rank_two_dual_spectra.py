#!/usr/bin/env python3
"""Exact necessary FP-dimension spectra for one rank-two R3472 module dual.

This enumerates dimensions, not fusion rings or module associators.  See
R3472_RANK_TWO_DUAL_SPECTRA.md for the conditional categorical statement.
Only the Python standard library is required.
"""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
INPUT = ROOT / "evidence/rank8_next_20261021/quadratic/action_classes.json"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def enumerate_spectra(g):
    # d_Y = (7*t+k) + 5*t*sqrt(2), with t>0 for nonintegral simples.
    # The complete bounds t<=2 and |k|<=2 follow from the square sums.
    types = [(t, k) for t in (1, 2) for k in range(-2, 3)]
    answers = []

    def visit(index, sum_t2, sum_k2, sum_tk, multiset):
        if sum_t2 > 7 or sum_k2 > 7 - g:
            return
        if index == len(types):
            if (sum_t2, sum_k2, sum_tk) == (7, 7 - g, 0):
                answers.append(multiset)
            return
        t, k = types[index]
        max_count = (7 - sum_t2) // (t * t)
        if k:
            max_count = min(max_count, (7 - g - sum_k2) // (k * k))
        for n in range(max_count + 1):
            extra = [(t, k, n)] if n else []
            visit(index + 1, sum_t2 + n * t * t,
                  sum_k2 + n * k * k, sum_tk + n * t * k,
                  multiset + extra)

    visit(0, 0, 0, 0, [])
    return answers


def matrix(s, t):
    return [[s + t, 7 * t], [7 * t, s - t]]


def main(write=False):
    raw = INPUT.read_bytes()
    actions = json.loads(raw)["R8_3_3472"]["complete_action_classes"]
    rank_two = [a["actions"] for a in actions if a["module_rank"] == 2]
    generators = [a[1] for a in rank_two]
    need(sorted(generators) == sorted([[[1, 5], [5, 11]], [[5, 7], [7, 7]]]), "exact spectrum verification failed")
    # Reverse the two module simples to match the convenient positive bases.
    normalized = [[[a[1][1], a[1][0]], [a[0][1], a[0][0]]] for a in generators]
    need(sorted(normalized) == sorted([[[11, 5], [5, 1]], [[7, 7], [7, 5]]]), "exact spectrum verification failed")

    # D/h is an algebraic integer iff its quadratic trace and norm are integers.
    # h<=7 follows from the norm identity in the proof.
    possible_h = [h for h in range(1, 8) if 1400 % h == 0 and 9800 % (h*h) == 0]
    need(possible_h == [1, 2, 5, 7], "exact spectrum verification failed")
    result = []
    for g in possible_h:
        for spectrum in enumerate_spectra(g):
            rows = []
            sum_s2, sum_t2, sum_st = g, 0, 0
            for t, k, n in spectrum:
                s = 7 * t + k
                need(min(sum(matrix(s, t), [])) >= 0, "exact spectrum verification failed")
                sum_s2 += n*s*s
                sum_t2 += n*t*t
                sum_st += n*s*t
                rows.append({"t": t, "k": k, "dimension": [s, 5*t], "multiplicity": n})
            need((sum_s2, sum_t2, sum_st) == (350, 7, 49), "exact spectrum verification failed")
            # When g=7, k=0 throughout and every noninvertible dimension is t*d.
            # For any d-dimensional simple X, the constant coefficient of
            # FPdim(X X*)=d^2=1+14d forces |Stab_G(X)|=1.  Thus the number of
            # d-dimensional simples must be divisible by seven.
            obstruction = None
            if g == 7:
                count_d = sum(n for t, k, n in spectrum if t == 1 and k == 0)
                if count_d % 7:
                    obstruction = "C7 must act freely on d-dimensional simples, but their count is not divisible by 7"
            result.append({"invertible_count": g, "rank": g + sum(n for _, _, n in spectrum),
                           "nonintegral_dimensions": rows, "excluded_by_orbit_test": bool(obstruction),
                           "orbit_obstruction": obstruction})
    need(len(result) == 11, "exact spectrum verification failed")
    need(Counter(x["invertible_count"] for x in result) == {1: 5, 2: 2, 5: 2, 7: 2}, "exact spectrum verification failed")
    need(sum(x["excluded_by_orbit_test"] for x in result) == 1, "exact spectrum verification failed")
    output = {"case_id": "R8_3_3472", "scope": "conditional necessary dimensions of the Morita dual of the rank-two action with source basis-1 matrix [[5,7],[7,7]] only",
              "source": str(INPUT.relative_to(ROOT)), "source_sha256": sha256(raw).hexdigest(),
              "covered_module_generator": [[5,7],[7,7]], "not_covered_module_generator": [[1,5],[5,11]], "global_fp_dimension": [700, 490],
              "quadratic_field": "Q(sqrt(2))", "dimensions_encoding": "[a,b] means a+b*sqrt(2)",
              "spectrum_count_before_orbit_test": 11, "spectrum_count_after_orbit_test": 10,
              "spectra": result}
    target = HERE / "r3472_rank_two_dual_spectra.json"
    if write:
        target.write_text(json.dumps(output, indent=2) + "\n")
    else:
        need(json.loads(target.read_text()) == output, "saved spectrum receipt differs")
    print(json.dumps({"recorded_rank_two_actions": len(rank_two), "covered_rank_two_actions": 1, "dimension_spectra": 11,
                      "orbit_excluded_spectra": 1, "remaining_necessary_spectra": 10}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="explicitly regenerate the receipt")
    main(parser.parse_args().write)

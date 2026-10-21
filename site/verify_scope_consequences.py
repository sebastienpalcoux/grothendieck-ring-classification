#!/usr/bin/env python3
"""Replay four small scope corollaries without a classification search.

Theory: Bruguières--Virelizier, arXiv:1203.4180v2, Section 4.3:
the left/right dimension ratio is a monoidal natural automorphism of Id,
and the pivotal category is spherical exactly when this slope is trivial.
The two products below force every slope to be one.  The complete exact
character table then shows that every spherical dimension character is in
the Frobenius--Perron orbit.  Galois transport gives a pseudo-unitary
categorification with the same fusion ring, not necessarily the same category.

The three additional self-dual rings have spherical pivotal structures.
Their non-FP characters are excluded by a zero simple dimension, or (R1795)
by Ostrik, arXiv:1309.4822, Theorem 2.13: dim(C)/f is an algebraic integer
for every formal codegree f of a spherical fusion category.  The rational
norms 1/9 and 1/36 below prove the latter failure.

Consequences for each of R982,R1768,R1795,R3472: every pivotal
categorification is spherical; pivotal, spherical and pseudo-unitary
EXISTENCE are equivalent. No implication from general categorifiability,
no unitarity, and no existence are proved.

Sources are the canonical census tensor and the previously saved complete
cyclotomic character table, whose multiplication identities were also
checked by evidence/rank8_next_20261021/r982/joint_galois_check.py.
"""

import hashlib
import json
from pathlib import Path

import sympy as s


ROOT = Path(__file__).resolve().parents[1]
CENSUS = "evidence/rank8_m3_20261021/pipeline/census_m3.json"
TABLE = ("evidence/rank8_frontier_20261021/global_induction/"
         "complete_results/R8_3_982_sts_frame_h4.json")
EXPECTED_HASH = "f4a9fb77b3a78e9dcd8370ca9fa822ea331f1b71e3fad7990efdd386445fcd1c"


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def verify_quadratic(ring_id, table_path, q, coefficients, expected_hash):
    """Check the complete stored tables, not just numerical approximations."""
    source = next(r for r in json.loads((ROOT / CENSUS).read_text())
                  if r["id"] == ring_id)
    tensor = source["tensor"]
    digest = hashlib.sha256(json.dumps(tensor, separators=(",", ":"))
                            .encode()).hexdigest()
    saved = json.loads((ROOT / table_path).read_text())
    need(digest == source["tensor_sha256"] == saved["tensor_sha256"]
         == expected_hash, ring_id + " tensor mismatch")
    need(all(tensor[i][j][0] == int(i == j)
             for i in range(8) for j in range(8)), "not self-dual")
    table = saved["metadata"]["character_table"]
    x = s.Symbol("x")
    poly = s.Poly.from_list(list(map(s.Rational, table["field_polynomial"])), x)
    need(poly.is_irreducible, "table quotient is not a field")
    field = s.QQ.alg_field_from_poly(poly, alias="u")
    u = field([1, 0])
    if q == 37:
        radical = (u - field(716)) / field(126)
    elif q == 5:
        radical = (u - field(818)) / field(378)
    else:
        # This metadata vector uses ascending powers; characters use descending.
        radical = field(list(reversed(list(map(
            s.Rational, table["radical_power_coordinates"])))))
    need(radical * radical == field(q), "incorrect radical")
    chars = [tuple(field(list(map(s.Rational, value))) for value in row)
             for row in table["characters"]]
    need(len(chars) == len(set(chars)) == 8, "not eight distinct characters")
    for row in chars:
        need(row[0] == field.one, "character is not unital")
        for i in range(8):
            for j in range(8):
                need(row[i] * row[j] == sum(
                    (field(tensor[i][j][k]) * row[k] for k in range(8)),
                    field.zero), "character multiplication fails")
    # These exact radicals certify positivity independently of the saved FP flag.
    need(all(s.Integer(a) + b * s.sqrt(q) > 0 for a, b in coefficients),
         "FP positivity fails")
    fp = tuple(field(a) + field(b) * radical for a, b in coefficients)
    conjugate = tuple(field(a) - field(b) * radical for a, b in coefficients)
    fp_index, conjugate_index = chars.index(fp), chars.index(conjugate)
    need(fp_index != conjugate_index, "quadratic FP orbit collapsed")
    # Both embeddings of Q(sqrt(q)) extend to algebraic-closure automorphisms.
    orbit = {fp_index, conjugate_index}
    codegrees = [sum((v * v for v in row), field.zero) for row in chars]
    stored = [field(list(map(s.Rational, value))) for value in table["codegrees"]]
    need(codegrees == stored, "stored formal codegrees fail exact verification")
    f, f_conjugate = codegrees[fp_index], codegrees[conjugate_index]
    exclusions = []
    for index, row in enumerate(chars):
        if index in orbit:
            continue
        zero_indices = [i for i, value in enumerate(row) if not value]
        if zero_indices:
            exclusions.append({"character": index, "zero_simple_indices": zero_indices})
            continue
        need(ring_id == "R8_3_1795", "unexpected nonzero residual character")
        dimension = codegrees[index]
        need(dimension in (field(10), field(20)), "unexpected candidate dimension")
        need(f * f_conjugate == field(3600), "incorrect FP codegree norm")
        norm = dimension * dimension / (f * f_conjugate)
        expected = s.Rational(1, 36) if dimension == field(10) else s.Rational(1, 9)
        need(norm == field(expected) and expected.q != 1,
             "algebraic-integrality norm obstruction failed")
        exclusions.append({"character": index, "candidate_dimension": int(dimension.to_list()[0]),
                           "norm_of_dimension_over_FP_codegree": str(expected)})
    need(len(exclusions) == 6, "not all non-FP characters excluded")
    return {"id": ring_id, "tensor_sha256": digest,
            "pivotal_implies_spherical": "all simple objects self-dual",
            "complete_characters": 8, "FP_character": fp_index,
            "FP_positivity": "exact positive radical expressions",
            "FP_Galois_orbit": sorted(orbit), "excluded_dimension_characters": exclusions,
            "existence_equivalence": ["pivotal", "spherical", "pseudo_unitary"],
            "not_proved": ["general_implies_pivotal", "same_category_pseudo_unitarity",
                           "unitarity", "categorification_existence"]}


def main():
    source = next(r for r in json.loads((ROOT / CENSUS).read_text())
                  if r["id"] == "R8_3_982")
    tensor = source["tensor"]
    digest = hashlib.sha256(json.dumps(tensor, separators=(",", ":"))
                            .encode()).hexdigest()
    need(digest == source["tensor_sha256"] == EXPECTED_HASH,
         "canonical tensor hash changed")
    dual = [next(j for j in range(8) if tensor[i][j][0])
            for i in range(8)]
    need(dual == [0, 2, 1, 4, 3, 5, 6, 7], "unexpected duality")
    need(tensor[1][2] == [1, 1, 1, 2, 2, 2, 0, 0],
         "first slope-forcing product changed")
    need(tensor[1][1] == [0, 1, 1, 2, 2, 0, 1, 2],
         "second slope-forcing product changed")
    # X1 X1* forces slopes 0..5 to one; X1^2 then forces 6,7.
    first = {k for k, n in enumerate(tensor[1][2]) if n}
    need(first == set(range(6)) and 1 in first, "first slope support")
    need(first | {k for k, n in enumerate(tensor[1][1]) if n}
         == set(range(8)), "slope support does not exhaust the basis")

    saved = json.loads((ROOT / TABLE).read_text())
    need(saved["tensor_sha256"] == digest, "table tensor mismatch")
    table = saved["metadata"]["character_table"]
    x = s.Symbol("x")
    polynomial = s.Poly.from_list(
        list(map(s.Rational, table["cyclotomic_polynomial"])), x)
    need(polynomial == s.Poly(s.cyclotomic_poly(24, x), x), "not Phi24")
    field = s.QQ.alg_field_from_poly(polynomial, alias="zeta")
    zeta = field([1, 0])
    chars = [tuple(field(list(map(s.Rational, value))) for value in row)
             for row in table["characters"]]
    need(len(chars) == len(set(chars)) == 8, "not eight distinct characters")
    for row in chars:
        need(row[0] == field.one, "character is not unital")
        for i in range(8):
            for j in range(8):
                need(row[i] * row[j]
                     == sum((field(tensor[i][j][k]) * row[k]
                             for k in range(8)), field.zero),
                     "character multiplication identity fails")
    # Eight distinct homomorphisms from this eight-dimensional algebra
    # exhaust its one-dimensional characters; no omitted dimension character.
    compatible = [j for j, row in enumerate(chars)
                  if all(row[i] == row[dual[i]] for i in range(8))]
    need(compatible == [0, 1, 6, 7], "unexpected dual-compatible characters")

    def evaluate(value, at):
        result = field.zero
        for coefficient in value.to_list():
            result = result * at + field(coefficient)
        return result

    automorphisms = [1, 5, 7, 11, 13, 17, 19, 23]
    conjugates = [chars.index(tuple(evaluate(value, zeta ** power)
                                   for value in chars[0]))
                  for power in automorphisms]
    need(conjugates == [0, 1, 7, 6, 6, 7, 1, 0], "unexpected Galois action")
    need(set(conjugates) == set(compatible), "FP orbit does not exhaust candidates")

    # Exact positivity at zeta_24=exp(pi*i/12), independent of any saved FP flag.
    r2, r3, r6 = s.sqrt(2), s.sqrt(3), s.sqrt(6)
    embedding = (r6 + r2 + s.I * (r6 - r2)) / 4
    a = 2 + r3 + r6 + 2 * r2
    b = 3 + 2 * r3 + r6 + 2 * r2
    c = 2 + r2 + r3 + r6
    positive = [s.Integer(1), a, a, b, b, c, s.Integer(1), c]
    need(all(value.is_positive is True for value in positive),
         "positive radical expressions not verified")
    for encoded, expected in zip(table["characters"][0], positive):
        value = 0
        for coefficient in encoded:
            value = value * embedding + s.Rational(coefficient)
        need(s.simplify(s.expand(value - expected)) == 0,
             "character zero is not the positive character")
    # A positive unital fusion-ring character is the unique FP character.
    print(json.dumps({
        "id": "R8_3_982", "tensor_sha256": digest,
        "pivotal_implies_spherical": "two exact slope-forcing products",
        "complete_characters": 8, "dual_compatible_characters": compatible,
        "FP_character": 0, "FP_positivity": "exact positive radical expressions",
        "Galois_powers": automorphisms, "FP_Galois_character_indices": conjugates,
        "existence_equivalence": ["pivotal", "spherical", "pseudo_unitary"],
        "not_proved": ["general_implies_pivotal", "same_category_pseudo_unitarity",
                       "unitarity", "categorification_existence"],
    }, separators=(",", ":")))
    prefix = "evidence/rank8_frontier_20261021/global_induction/"
    for receipt in [
        verify_quadratic("R8_3_1768", prefix + "complete_results/R8_3_1768_atomic_real_sts_h4.json",
                         37, [(1, 0), (1, 0), (5, 1), (6, 1), (7, 1), (7, 1), (6, 1), (5, 1)],
                         "240509807c67da437c86f2a51efeb831364734feb93ed18a1d2f32087ebc1af0"),
        verify_quadratic("R8_3_1795", prefix + "complete_results/R8_3_1795_atomic_real_sts_h4.json",
                         5, [(1, 0), (1, 0), (6, 3), (7, 3), (7, 3), (7, 3), (7, 3), (6, 3)],
                         "feddd2934d44be4872c82ed6c5650bf9d8aac2bc87b72778d88b375726f4cd1f"),
        verify_quadratic("R8_3_3472", prefix + "atomic_spectrum_results/R8_3_3472_h4.json",
                         2, [(1, 0), (6, 5), (6, 5), (7, 5), (6, 5), (8, 5), (8, 5), (8, 5)],
                         "33984d45e69ff778e70847def8349abda79ed6c0eaea242a73b533649f9b153a"),
    ]:
        print(json.dumps(receipt, separators=(",", ":")))


if __name__ == "__main__":
    main()

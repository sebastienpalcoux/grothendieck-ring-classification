#!/usr/bin/env python3
"""Exact full-I(1) conductor-five saturation and conductor-eight frame cut.

This verifies the algebraic input to the phase refinement. It does not by
itself exclude both rings. No optimizer is used and -O preserves every check.
"""
import argparse
import json
from pathlib import Path
import sys

import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))
from verify_transport import verify_all, require
sys.path.insert(0, str(ROOT / "evidence/rank7_m5_20261020/criteria"))
import q5_center_trace as q
from exact_quadratic_characters import ExactQuadraticCharacterTable


def encode_matrix(matrix):
    return [[str(s.simplify(value)) for value in row] for row in matrix.tolist()]


def conductor_five_model():
    """Check the equality representations on the 24 nonzero vectors over F5."""
    points = [(p, z) for p in range(5) for z in range(5) if (p, z) != (0, 0)]
    index = {point: i for i, point in enumerate(points)}
    def chi(value):
        return 0 if value % 5 == 0 else (1 if value % 5 in (1, 4) else -1)
    unipotent, weyl = s.zeros(24), s.zeros(24)
    for i, (p, z) in enumerate(points):
        unipotent[i, index[((p-z) % 5, z)]] = 1
        weyl[i, index[(z, -p % 5)]] = 1
    big = s.Matrix([chi(z) for p, z in points])
    small = s.Matrix([chi(-p) if z == 0 else 0 for p, z in points])
    projector = sum((unipotent ** j for j in range(5)), s.zeros(24)) / 5
    require(projector * weyl * big == small, "big-to-small equality vector")
    require(projector * weyl * small == big / 5, "small-to-big equality vector")
    require((weyl * unipotent) ** 3 == weyl ** 2, "SL2(F5) presentation")
    result = {}
    x = s.Symbol("x")
    for delta in (-1, 1):
        vector = big + delta * s.sqrt(5) * small
        require(s.simplify(projector * weyl * vector - delta * vector / s.sqrt(5)) == s.zeros(24, 1),
                "conductor-five compression eigenvalue")
        span = s.Matrix.hstack(*[unipotent ** j * weyl * vector for j in range(5)])
        basis = span[:, list(span.rref()[1])]
        require(basis.cols == 3, "equality representation dimension")
        action = basis.gauss_jordan_solve(unipotent * basis)[0]
        expected = (x - 1) * (x*x + (1-delta*s.sqrt(5))*x/2 + 1)
        require(s.simplify(action.charpoly(x).as_expr() - expected) == 0,
                "primitive fifth-root sign")
        # The Weyl operator must preserve this span, not merely the unipotent.
        basis.gauss_jordan_solve(weyl * basis)
        result[str(delta)] = {
            "dimension": 3,
            "twist_polynomial": str(s.expand(expected)),
            "allowed_nontrivial_relative_phase_scaled_by_8": [-2, 2*delta, -2, -2*delta],
        }
    return result


def verify():
    transports = verify_all()
    census = {row["id"]: row["tensor"] for row in json.loads(
        (ROOT / "supplements/rank7/output/m5/census.json").read_text())}
    result = {"scope": "Necessary low-block compression and saturation refinement, not a complete exclusion.",
              "rings": {}, "level_five_equality_models": conductor_five_model()}
    for ring_id in transports:
        tensor = census[ring_id]
        dimensions, total, gram, low_dimensions, transport, signs = q.source_data(tensor, ring_id)
        lows, nodes, forced = q.enumerate_low(gram, dimensions, low_dimensions, transport)
        table = ExactQuadraticCharacterTable(tensor, dimensions, 5)
        field = table.K
        characters = [[s.expand(field.to_sympy(value)) for value in row] for row in table.rows]
        sigma5 = [characters.index([value.xreplace({s.sqrt(5): -s.sqrt(5)}) for value in row])
                  for row in characters]
        pairs = [(i, j) for i, j in enumerate(sigma5) if i < j]
        require(len(pairs) == 2, "two conductor-five differences")
        require(all(table.codegrees[i] == field(5) for i in pairs[1]), "second pair has codegree five")
        conjugate = [characters.index([s.conjugate(value) for value in row]) for row in characters]
        imaginary_pairs = [(i, j) for i, j in enumerate(conjugate) if i < j]
        require(len(imaginary_pairs) == int(ring_id == "R7_5_5039"), "imaginary character orbit")
        frames = []
        for frame_index, low in enumerate(lows):
            rows = [(1, 0, 0, 0, 0, 0, 0)] + low
            labels = table.assignments(rows)
            if not labels:
                continue
            assignments = []
            for label in labels:
                assigned = {character: vector for character, vector in zip(label, rows)}
                low_s = s.Matrix([[s.expand(field.to_sympy(sum(
                    (field(assigned[j][k]) * table.rows[i][k] for k in range(7)), field.zero)
                    / table.codegrees[i])) for j in range(7)] for i in range(7)])
                require(s.simplify(low_s - low_s.T) == s.zeros(7), "normalized character reciprocity")
                block = s.Matrix([[s.simplify((low_s[i, k] - low_s[i, ell]
                    - low_s[j, k] + low_s[j, ell]) / 2)
                    for k, ell in pairs] for i, j in pairs])
                delta = s.simplify(s.sqrt(5) * block[1, 1])
                require(delta in (-1, 1), "conductor-five equality sign")
                require(block == s.diag(-s.sqrt(5)/10, delta*s.sqrt(5)/5),
                        "complete conductor-five block")
                difference_basis = s.Matrix.hstack(*[
                    (s.eye(7)[:, i] - s.eye(7)[:, j])/s.sqrt(2) for i, j in pairs])
                require(s.simplify(low_s * difference_basis - difference_basis * block) == s.zeros(7, 2),
                        "full low block preserves conductor-five isotypic subspace")
                require(s.simplify(s.eye(2)/5 - block.conjugate().T * block)
                        == s.diag(s.Rational(3, 20), 0), "exact compression slack")
                odd_block, excluded = None, False
                if imaginary_pairs:
                    i, j = imaginary_pairs[0]
                    require(table.codegrees[i] == table.codegrees[j] == field(8), "imaginary codegree")
                    odd_block = s.simplify((low_s[i, i] - low_s[i, j] - low_s[j, i] + low_s[j, j])/2)
                    square = s.simplify(s.conjugate(odd_block)*odd_block)
                    require(square in (0, s.Rational(1, 2)), "observed conductor-eight block")
                    excluded = bool(square > s.Rational(1, 8))
                assignments.append({
                    "labelling": list(label), "chi5_block": encode_matrix(block), "delta": int(delta),
                    "chi5_slack": [["3/20", "0"], ["0", "0"]],
                    "chi_minus8_block": None if odd_block is None else str(odd_block),
                    "excluded_by_conductor8": excluded,
                    "unequal_phi_high_row_phase_scaled_by_8": [-2, 2*int(delta), -2, -2*int(delta)],
                })
            frames.append({"frame_index": frame_index, "low_rows": low, "assignments": assignments})
        require([frame["frame_index"] for frame in frames]
                == ([6, 8] if ring_id == "R7_5_3895" else [1, 3]), "complete labelled frame inventory")
        result["rings"][ring_id] = {
            "source_sha256": transports[ring_id]["sha256"], "low_frame_count": len(lows),
            "characters": [[str(x) for x in row] for row in characters],
            "chi5_pairs": pairs, "chi_minus8_pairs": imaginary_pairs,
            "phi_indices": [4, 5] if ring_id == "R7_5_3895" else [3, 4], "frames": frames,
        }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-receipt", action="store_true")
    args = parser.parse_args()
    result = json.loads(json.dumps(verify()))
    path = HERE / "low_compression_certificate.json"
    if args.write_receipt:
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        require(json.loads(path.read_text()) == result, "compression receipt mismatch")
    print("PASS: full conductor-five saturation, conductor-eight frame cut, exact level-five equality models")


if __name__ == "__main__":
    main()

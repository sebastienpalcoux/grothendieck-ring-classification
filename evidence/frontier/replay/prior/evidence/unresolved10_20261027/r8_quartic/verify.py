#!/usr/bin/env python3
"""Short exact input checks for the quartic integral-center lemma.

This does NOT verify categorical existence, center lifts, or prior scope gates.
No third-party library and no search beyond closure of eight-element supports.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INPUT = ROOT / "evidence/unresolved_retry_20261024/proofs/unresolved11_20261024/inputs"
ONE = (1, 0, 0, 0)
A = (2, 1, 1, 1)
B = (2, 2, 1, 1)
C = (3, 2, 2, 1)
ZERO = (0, 0, 0, 0)


def check(p, message):
    if not p:
        raise ValueError(message)


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def scale(c, x):
    return tuple(c * a for a in x)


def mul(x, y):
    # Basis masks 0,1,2,3 represent 1,sqrt(2),sqrt(3),sqrt(6).
    z = [0] * 4
    for i, a in enumerate(x):
        for j, b in enumerate(y):
            common = i & j
            factor = (2 if common & 1 else 1) * (3 if common & 2 else 1)
            z[i ^ j] += factor * a * b
    return tuple(z)


def closure(N, dual, seed):
    current = set(seed)
    while True:
        nxt = current | {dual[i] for i in current}
        nxt |= {k for i in current for j in current for k in range(8) if N[i][j][k]}
        if nxt == current:
            return sorted(current)
        current = nxt


def main():
    receipt = {"source_revision": "6a426acf6465dd674351be92dcca41b72f371521", "cases": []}
    for case, dimensions, g, digest in [
        ("R8_3_928", [ONE, A, A, B, B, C, C, ONE], 7,
         "94dfb90235dbb3ba95864a1be23437943ea3b1316ec82ca44baf419262890614"),
        ("R8_3_941", [ONE, B, B, ONE, A, A, C, C], 3,
         "8ae4007492dee167ab8b3f4f16310ee368482da03696e20ed7cceea34bec64e6"),
    ]:
        record = json.loads((INPUT / f"{case}.json").read_text())
        N = record["fusion_tensor"]
        dual = record["invariants"]["dual_indices"]
        actual = hashlib.sha256(json.dumps(N, separators=(",", ":")).encode()).hexdigest()
        check(actual == digest, f"{case}: tensor hash")
        for i in range(8):
            for j in range(8):
                rhs = ZERO
                for k in range(8):
                    rhs = add(rhs, scale(N[i][j][k], dimensions[k]))
                check(mul(dimensions[i], dimensions[j]) == rhs, f"{case}: character {i},{j}")
        # Each coordinate is nonnegative, so the character is strictly positive.
        # Uniqueness of the positive normalized fusion-ring character identifies FPdim.
        check(all(all(a >= 0 for a in d) and d[0] > 0 for d in dimensions), "positive character")
        check(all(all(a > 0 for a in dimensions[i][1:]) for i in range(8) if i not in (0, g)),
              "strict positive irrational support")
        action = []
        for i in range(8):
            check(sum(N[g][i]) == 1 and N[g][i] == N[i][g], "central invertible action")
            image = N[g][i].index(1)
            check(image != i, "free invertible action")
            action.append(image)
        ad_seed = {k for i in range(8) for k in range(8) if N[i][dual[i]][k]}
        ad = closure(N, dual, ad_seed)
        check(ad == list(range(8)), "full adjoint closure")
        generated = {str(i): closure(N, dual, {0, i}) for i in range(8)}
        check(all(generated[str(i)] == list(range(8)) for i in range(8) if i not in (0, g)),
              "every nonpointed object generates")
        global_dimension = ZERO
        for d in dimensions:
            global_dimension = add(global_dimension, mul(d, d))
        check(global_dimension == (144, 96, 80, 56), "global dimension")
        receipt["cases"].append({
            "id": case, "tensor_sha256": actual, "dimension_basis": ["1", "sqrt(2)", "sqrt(3)", "sqrt(6)"],
            "exact_dimensions": dimensions, "global_dimension": global_dimension,
            "invertible_action": action, "full_adjoint_closure": ad, "single_generated_subrings": generated,
            "categorical_lift_input": "inherited semion" if g == 7 else "inherited fermion",
            "categorification_decision": "unresolved",
        })
    receipt["outcome"] = "PASS: exact source hypotheses only; no categorical decision"
    target = Path(__file__).with_name("verification.json")
    target.write_text(json.dumps(receipt, indent=2) + "\n")
    print(receipt["outcome"])


if __name__ == "__main__":
    main()

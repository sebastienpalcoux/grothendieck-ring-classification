#!/usr/bin/env python3
"""Check the captured R416 first-system coordinate diagnosis with integers only.

This checks the diagnostic matrices and ray transport, not the full certificate
or the categorical necessity of the matrix equations.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", type=Path, default=Path(__file__).resolve().parent / "r416_diagnostic")
    args = ap.parse_args()
    proof = json.loads((args.data / "r416_row_permutation_proof.json").read_text())
    systems = {}
    for name, expected in proof["systems"].items():
        path = args.data / (name + ".system.json.gz")
        require(hashlib.sha256(path.read_bytes()).hexdigest() == expected, "system digest mismatch: " + name)
        systems[name] = json.loads(gzip.decompress(path.read_bytes()))
    py, f8, f9 = (systems[name] for name in ("python-r416", "flint08-r416", "flint09-r416"))
    require(all(f8[k] == f9[k] for k in ("A", "b", "y")), "Flint versions produced different systems")
    require(py["y"] == f9["y"], "saved rays differ")
    p = proof["python_to_flint_row_permutation"]
    require(sorted(p) == list(range(len(py["b"]))), "not a row bijection")
    require(len(p) == len(f9["b"]), "row counts differ")
    for i, j in enumerate(p):
        require(py["A"][i] == f9["A"][j] and py["b"][i] == f9["b"][j], "augmented row mismatch")
    transported = [0] * len(p)
    for i, j in enumerate(p):
        transported[j] = py["y"][i]
    def dual(system, ray):
        return [sum(row[j] * y for row, y in zip(system["A"], ray)) for j in range(len(system["A"][0]))]
    python_dual = dual(py, py["y"])
    flint_dual = dual(f9, transported)
    original_flint_dual = dual(f9, f9["y"])
    python_value = sum(x * y for x, y in zip(py["b"], py["y"]))
    flint_value = sum(x * y for x, y in zip(f9["b"], transported))
    require(python_dual == flint_dual, "transport changed the dual vector")
    require(min(python_dual) >= 0, "transported ray is not nonnegative on all columns")
    require(python_value == flint_value < 0, "transport changed or lost the contradiction")
    require(sum(x < 0 for x in original_flint_dual) == 23, "original failure was not reproduced")
    print(json.dumps({"passed": True, "rows": len(p), "columns": len(python_dual),
                      "changed_row_positions": sum(i != j for i, j in enumerate(p)),
                      "original_flint_negative_coefficients": 23,
                      "transported_minimum_dual_coefficient": min(flint_dual),
                      "transported_rhs_value": flint_value,
                      "scope": "R416 first captured Farkas system only"}, indent=2))


if __name__ == "__main__":
    main()

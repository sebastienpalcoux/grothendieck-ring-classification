#!/usr/bin/env python3
"""Portable exact replay of the archived K(C4,8) terminal obstruction.

The original five-module import closure is preserved byte-for-byte. No
optimizer is called: each separating vector is checked over the integers.
"""
import hashlib
import itertools
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    provenance = json.loads((ROOT / "provenance.json").read_text())
    for relative, expected in provenance["source_members_sha256"].items():
        require(digest(ROOT / relative) == expected, "Changed archived source: " + relative)
    require(digest(ROOT / "case.json") == provenance["extracted_case_sha256"], "Changed extracted case")
    case = json.loads((ROOT / "case.json").read_text())
    tensor = case["source_record"]["N"]
    actual_hash = hashlib.sha256(json.dumps(tensor, separators=(",", ":")).encode()).hexdigest()
    require(actual_hash == case["tensor_sha256"], "Source tensor hash mismatch")

    # Construct K(C4,8) independently of the source's numbering.
    standard = [[[0 for _ in range(5)] for _ in range(5)] for _ in range(5)]
    for i, j in itertools.product(range(5), repeat=2):
        if i == j == 4:
            standard[i][j] = [1, 1, 1, 1, 8]
        elif i == 4 or j == 4:
            standard[i][j][4] = 1
        else:
            standard[i][j][(i + j) % 4] = 1
    maps = []
    for tail in itertools.permutations(range(1, 5)):
        p = (0,) + tail
        if all(standard[i][j][k] == tensor[p[i]][p[j]][p[k]]
               for i, j, k in itertools.product(range(5), repeat=3)):
            maps.append(list(p))
    require(bool(maps), "Source is not the complete K(C4,8) tensor")

    sys.path.insert(0, str(ROOT / "software"))
    import cyclic_four
    from rings import validate
    validate(tensor)
    certificate = case["certificate"]
    require(certificate["parameter"] == 2 and certificate["height"] == 6, "Wrong specialization")
    cyclic_four.verify(tensor, certificate)
    outcomes = []
    for branch in certificate["branches"]:
        entry = {key: branch[key] for key in ("u", "h", "epsilon")}
        obstruction = branch["obstruction"]
        entry["kind"] = obstruction["kind"]
        if obstruction["kind"] == "central_trace":
            A, b, meta = cyclic_four.system(2, branch, 6)
            y = obstruction["y"]
            aty = [sum(row[j] * yi for row, yi in zip(A, y)) for j in range(len(A[0]))]
            entry.update(meta=meta, minimum_ATy=min(aty), bTy=sum(bi * yi for bi, yi in zip(b, y)))
        else:
            entry.update(forced_fusion_coefficient="1/2", integral=False)
        outcomes.append(entry)
    return {"result": "PASS", "scope": "K(C4,8) has no complex fusion categorification",
            "tensor_sha256": actual_hash, "standard_to_source_basis_maps": maps,
            "source_archive": provenance["source_archive"],
            "branches": outcomes, "optimizer_called": False,
            "archived_sources_hash_checked": len(provenance["source_members_sha256"])}


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))

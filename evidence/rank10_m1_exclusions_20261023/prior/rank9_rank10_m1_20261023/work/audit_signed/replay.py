"""Replay the entire sphericalization bridge without changing discovery files.

Run normally (not with python -O): the older self-dual verifiers use assertions.
Only this audit directory receives output. All ring tensors are read directly
from the uploaded gzipped multiplication tables, not from cached audit tensors.
"""
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

if not __debug__:
    raise RuntimeError("Run this verifier without -O; legacy verifiers use assert")

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
ROOT = WORK.parent
sys.path.insert(0, str(WORK / "general_signed"))
from oriented import read
from verify import verify_record
from verify_characters import verify_original, verify_signed
from branches import signed_tensor

sys.path.insert(0, str(WORK / "rank9_bridge"))
from verify_certificate import verify as verify_special
from verify_saturation import verify as verify_selfdual
from verify_extra_signed import check as verify_extra


def load(name):
    return json.loads((WORK / name).read_text())


def must_fail(operation, name):
    try:
        operation()
    except (AssertionError, ValueError, RuntimeError):
        return {"check": name, "tampering_rejected": True}
    raise RuntimeError("Verifier accepted tampering: " + name)


def main():
    source = {r["id"]: r for r in read()}
    rows = {i: r["tensor"] for i, r in source.items()}
    receipts = load("general_signed/ledger.json")
    original = load("general_signed/original_characters.json")
    selfdual = load("rank9_bridge/saturation_scan.json")
    extra = load("rank9_bridge/extra_signed.json")
    summary = load("general_signed/summary.json")
    alternate_count = 0
    signed_ids = []
    for rec in receipts:
        rid = rec["id"]
        if source[rid]["tensor_sha256"] != rec["tensor_sha256"]:
            raise RuntimeError("Oriented source mismatch: " + rid)
        verify_record(rows[rid], rec)
        signed_ids.append(rid)
        R = rows[rid]
        dual = [next(j for j in range(len(R)) if R[i][j][0]) for i in range(len(R))]
        mapping = {}
        for index, orbit in enumerate(rec["oriented_orbits"]):
            for i, j, k in orbit:
                mapping[i, j, dual[k]] = index
        for b in rec["branches"]:
            if b["outcome"] == "excluded_dimension_characters":
                T = signed_tensor(R, {"mapping": mapping}, b["sign_assignment"])
                verify_signed(R, T, b["dimension_test"])
                alternate_count += 1
    print("PASS oriented", len(receipts), "alternate signed inventories", alternate_count, flush=True)
    for rec in original:
        rid = rec["id"]
        if source[rid]["tensor_sha256"] != rec["tensor_sha256"]:
            raise RuntimeError("Character source mismatch: " + rid)
        verify_original(rows[rid], rec)
    print("PASS original character inventories", len(original), flush=True)
    special = verify_special(rows["R9_1_41"], load("rank9_bridge/signed_bridge_certificate.json"))
    selfdual_results = [verify_selfdual(rows[rid], rec) for rid, rec in selfdual.items()]
    extra_results = [verify_extra(rows[rid], rec) for rid, rec in extra.items()]
    spherical_ids = set(signed_ids) | {
        r["id"] for r in selfdual_results if r["sphericality_proved"]
    } | {r["id"] for r in extra_results}
    if not all(rec["id"] in spherical_ids for rec in original):
        raise RuntimeError("An original character inventory lacks a sphericality bridge")
    excluded = [
        rec["id"] for rec in original
        if all(b["obstruction"] for b in rec["branches"])
    ]
    expected = set(summary["general_exclusions_with_this_bridge"]) | set(
        summary["spherical_exclusions_requiring_selfdual_bridge"]
    )
    if set(excluded) != expected:
        raise RuntimeError("Summary exclusion list does not match audited inventories")
    bad_sign = copy.deepcopy(receipts[0])
    bad_sign["normalized_variable_exponents"][0] ^= 1
    bad_character = copy.deepcopy(original[0])
    bad_character["branches"][0]["dimensions"][0] = ["2"]
    mutations = [
        must_fail(lambda: verify_record(rows[receipts[0]["id"]], bad_sign), "altered sign exponent"),
        must_fail(lambda: verify_original(rows[original[0]["id"]], bad_character), "altered unit dimension"),
    ]
    files = [
        "general_signed/ledger.json", "general_signed/original_characters.json",
        "rank9_bridge/saturation_scan.json", "rank9_bridge/extra_signed.json",
        "rank9_bridge/signed_bridge_certificate.json",
    ]
    result = {
        "status": "PASS",
        "audit_scope": "sphericalization and scalar-character bridge only",
        "oriented_receipts": len(receipts),
        "alternate_signed_character_inventories": alternate_count,
        "original_character_inventories": len(original),
        "selfdual_receipts": len(selfdual_results),
        "extra_selfdual_receipts": len(extra_results),
        "sphericality_certified_ids": sorted(spherical_ids),
        "general_exclusion_ids": excluded,
        "case_ids_requiring_status_downgrade": [],
        "mutation_checks": mutations,
        "receipt_sha256": {p: hashlib.sha256((WORK / p).read_bytes()).hexdigest() for p in files},
        "input_sha256": {
            f"rank{rank}": hashlib.sha256((ROOT / "inputs" / f"rank{rank}_M1_verified" /
                "FusionRingMultiplicationTables.txt.gz").read_bytes()).hexdigest()
            for rank in (9, 10)
        },
    }
    (HERE / "audit_result.json").write_text(json.dumps(result, indent=2) + "\n")
    print("PASS", len(spherical_ids), "sphericality bridges;", len(excluded), "general exclusions", flush=True)
    return result


if __name__ == "__main__":
    main()

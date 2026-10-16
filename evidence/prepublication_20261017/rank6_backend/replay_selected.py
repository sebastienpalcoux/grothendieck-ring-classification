#!/usr/bin/env python3
"""Replay selected frozen rank-six exclusions with their saved row convention.

This is an environment adapter, not a replacement mathematical checker. It calls
the unchanged supplements/rank6/verify.py worker. It does not replay positive
models, scoped structure obstructions, frontier reductions, or census import.
"""
import os

# Must precede every SymPy import. ANP string ordering enters frozen row assembly.
os.environ["SYMPY_GROUND_TYPES"] = "python"
for _name in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_name] = "1"

import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
from pathlib import Path
import platform
import sys
import time


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def object_digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def source_manifest(rank6):
    paths = [rank6 / "verify.py"]
    paths += sorted(p for p in (rank6 / "software").rglob("*") if p.suffix in (".py", ".cpp") and p.is_file())
    return {str(p.relative_to(rank6)): digest(p) for p in paths}


def native_manifest(rank6):
    # The frozen checker may compile adjacent executables. Record their actual
    # bytes without changing an executable that another replay could be using.
    paths = sorted(p.with_suffix("") for p in (rank6 / "software").rglob("*.cpp"))
    return {str(p.relative_to(rank6)): digest(p) for p in paths if p.is_file()}


def package_version(name):
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, required=True, help="repository root")
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--ids", nargs="+", help="one or more excluded census IDs")
    group.add_argument("--failed-receipts", type=Path, help="select every explicit passed:false record from a JSONL replay")
    ap.add_argument("--out", type=Path, help="new JSONL output; adjacent .summary.json is also written")
    ap.add_argument("--list", action="store_true", help="validate and list selection without running certificates")
    args = ap.parse_args()
    rank6 = args.repo.resolve() / "supplements" / "rank6"
    census_path, ledger_path = rank6 / "data/census.json", rank6 / "data/decisions.json"
    rows, ledger = json.loads(census_path.read_text()), json.loads(ledger_path.read_text())
    index, decisions = {r["id"]: r for r in rows}, {r["id"]: r for r in ledger}
    if len(index) != len(rows) or len(decisions) != len(ledger):
        raise ValueError("duplicate census or ledger IDs")
    if [r["id"] for r in rows] != [r["id"] for r in ledger]:
        raise ValueError("ledger does not exactly cover census in order")
    selection_source = None
    if args.ids is not None:
        selected = args.ids
    else:
        selection_source = {"path": str(args.failed_receipts.resolve()), "sha256": digest(args.failed_receipts)}
        records = [json.loads(line) for line in args.failed_receipts.read_text().splitlines() if line.strip()]
        selected = [r["id"] for r in records if r.get("passed") is False]
    if not selected or len(set(selected)) != len(selected):
        raise ValueError("selection must be nonempty with no duplicate IDs")
    for rid in selected:
        if rid not in decisions:
            raise ValueError("unknown census ID: " + rid)
        if decisions[rid]["status"] != "excluded":
            raise ValueError("selected record is not a general exclusion: " + rid)
        if "certificate" not in decisions[rid]:
            raise ValueError("selected exclusion has no certificate: " + rid)
    if args.list:
        print(json.dumps({"selected_ids": selected, "executed": False}, indent=2))
        return 0
    if args.out is None:
        ap.error("--out is required unless --list is used")
    out = args.out.resolve()
    summary_path = out.with_suffix(".summary.json")
    if out == summary_path or out.exists() or summary_path.exists():
        raise FileExistsError("refusing to overwrite replay output or summary")

    from sympy.external.gmpy import GROUND_TYPES
    if GROUND_TYPES != "python":
        raise RuntimeError("the frozen certificates require the Python ground-type row convention")
    before = source_manifest(rank6)
    initial_native = native_manifest(rank6)
    census_sha, ledger_sha = digest(census_path), digest(ledger_path)
    spec = importlib.util.spec_from_file_location("rank6_frozen_verify", rank6 / "verify.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    started = time.monotonic()
    results = []
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x", encoding="utf-8") as stream:
        for rid in selected:
            result = module.worker((index[rid], decisions[rid]["certificate"]))
            result["certificate_canonical_json_sha256"] = object_digest(decisions[rid]["certificate"])
            result["tensor_canonical_json_sha256"] = object_digest(index[rid]["N"])
            result["ground_types"] = GROUND_TYPES
            result["complete_selected_certificate"] = result["passed"] is True
            stream.write(json.dumps(result, separators=(",", ":")) + "\n")
            stream.flush()
            results.append(result)
            print(json.dumps(result, separators=(",", ":")), flush=True)
    unchanged = before == source_manifest(rank6) and census_sha == digest(census_path) and ledger_sha == digest(ledger_path)
    passed = unchanged and len(results) == len(selected) and all(r["passed"] is True for r in results)
    summary = {
        "passed": passed,
        "scope": "Complete selected general-exclusion certificates only; not a full rank-six release replay or independent mathematical proof.",
        "selected_ids": selected,
        "completed": len(results),
        "failed_ids": [r["id"] for r in results if not r["passed"]],
        "seconds": time.monotonic() - started,
        "environment": {"python": platform.python_version(), "optimized_python": not __debug__, "sympy_ground_types": GROUND_TYPES,
                        **{name: package_version(name) for name in ("sympy", "numpy", "scipy", "python-flint")}},
        "checker": "unchanged supplements/rank6/verify.py:worker (disables scipy.optimize.linprog and milp)",
        "adapter_sha256": digest(Path(__file__)),
        "census_sha256": census_sha,
        "ledger_sha256": ledger_sha,
        "source_sha256": before,
        "source_and_inputs_unchanged": unchanged,
        "native_executables_before": initial_native,
        "native_executables_after": native_manifest(rank6),
        "selection_source": selection_source,
        "receipt_sha256": digest(out),
    }
    with summary_path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"passed": passed, "summary": str(summary_path), "completed": len(results)}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate complete negative-certificate coverage across documented replays.

Does not turn an unsuccessful full run into a successful single run. The input
index links each fresh complete replay to its unchanged raw receipt and inputs.
This script checks evidence coverage and hashes, not the certificates themselves.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def objsha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load_json(path):
    return json.loads(path.read_text())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--initial", type=Path, required=True, help="unchanged original complete JSONL stream, including failures")
    ap.add_argument("--initial-log", type=Path, required=True, help="unchanged combined log of the original full process")
    ap.add_argument("--replay-index", type=Path, required=True)
    ap.add_argument("--baseline", type=Path, required=True)
    ap.add_argument("--postloop", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True, help="new output JSON summary")
    args = ap.parse_args()
    coverage_path = args.out.with_suffix(".coverage.jsonl.gz")
    require(not args.out.exists() and not coverage_path.exists(), "refusing to overwrite output or coverage")
    repo = args.repo.resolve()
    baseline = load_json(args.baseline)
    require(baseline["passed"] is True, "baseline identity check did not pass")
    require(not baseline["missing_files"] and not baseline["mismatches"], "baseline identity is incomplete")
    for rec in baseline["tracked_files"] + baseline["restored_inputs"]:
        require(rec["matches_preexisting_baseline"] is True, "unbound baseline input")
        require(sha(repo / rec["path"]) == rec["sha256"], "source/input changed: " + rec["path"])
    rows = load_json(repo / "supplements/rank6/data/census.json")
    ledger = load_json(repo / "supplements/rank6/data/decisions.json")
    row_index = {r["id"]: r for r in rows}
    require(len(row_index) == len(rows), "duplicate census ID")
    require([r["id"] for r in rows] == [r["id"] for r in ledger], "census/ledger coverage differs")
    excluded = [r for r in ledger if r["status"] == "excluded"]
    require(len(excluded) == 25362, "unexpected frozen exclusion count")
    by_id = {r["id"]: r for r in excluded}
    initial = [json.loads(line) for line in args.initial.read_text().splitlines() if line.strip()]
    require(len(initial) == len(excluded), "initial stream is incomplete or oversized")
    require([r["id"] for r in initial] == [r["id"] for r in excluded], "initial ordered IDs do not exactly cover the frozen exclusions")
    for rec in initial:
        require(type(rec.get("passed")) is bool, "initial receipt lacks Boolean outcome")
        require(rec["kind"] == by_id[rec["id"]]["certificate"]["kind"], "certificate kind mismatch")
    failed = [r["id"] for r in initial if r["passed"] is False]
    initial_log = args.initial_log.read_text()
    require("TRUSTED SOURCE IMPORT AND CONSTRUCTED MODELS VERIFIED" in initial_log,
            "original full-model/import completion marker missing")
    if failed:
        require(initial_log.rstrip().endswith(f"exact.VerificationError: {len(failed)} negative certificates failed"),
                "original full process did not reach its expected final negative-certificate failure gate")
    replay_index = load_json(args.replay_index)
    replays = replay_index["records"]
    require(len({r["id"] for r in replays}) == len(replays), "duplicate selected replay")
    require({r["id"] for r in replays} == set(failed), "fresh complete replays must cover exactly every initial failure")
    selected = {}
    for rec in replays:
        rid = rec["id"]
        require(rec["complete"] is True and rec["passed"] is True, "selected replay is not a full PASS")
        require(rec["ground_types"] == "python", "selected replay used the wrong backend")
        require(rec["certificate_canonical_json_sha256"] == objsha(by_id[rid]["certificate"]), "selected certificate mismatch")
        require(rec["census_record_canonical_json_sha256"] == objsha(row_index[rid]), "selected census record mismatch")
        receipt_path = args.replay_index.parent / rec["receipt"]
        require(sha(receipt_path) == rec["receipt_sha256"], "raw selected receipt changed")
        raw = load_json(receipt_path)
        require(raw.get("passed") is True or raw.get("status") == "PASS", "raw selected receipt is not PASS")
        if "id" in raw:
            require(raw["id"] == rid, "raw selected receipt ID mismatch")
        elif "case" in raw:
            require(raw["case"] == rid, "raw selected receipt case mismatch")
        for commitment in rec["supporting_commitments"]:
            require(sha(args.replay_index.parent / commitment["path"]) == commitment["sha256"], "selected replay commitment changed")
        for path, expected in rec["checked_source_sha256"].items():
            require(sha(repo / path) == expected, "selected replay source changed: " + path)
        selected[rid] = rec
    postloop = load_json(args.postloop)
    require(postloop["passed"] is True, "separate original post-loop checks did not pass")
    require(postloop["multiplicity_one"]["passed"] is True and postloop["positive_registry"]["equal"] is True,
            "missing original post-loop count or registry check")
    require(postloop["all_sources_and_inputs_unchanged"] is True, "post-loop inputs changed during checking")
    require(postloop["other_skipped_checks"] == [], "other original post-loop checks were not covered")
    for path, commitment in postloop["sources_and_inputs"].items():
        if path.startswith("supplements/rank6/"):
            require(sha(repo / path) == commitment["sha256"], "post-loop source/input mismatch: " + path)
    coverage = []
    for rec in initial:
        rid = rec["id"]
        coverage.append({"id": rid, "kind": rec["kind"], "passed": True,
                         "evidence": "initial full run" if rec["passed"] else "fresh complete Python-backend replay",
                         "certificate_canonical_json_sha256": objsha(by_id[rid]["certificate"]),
                         "census_record_canonical_json_sha256": objsha(row_index[rid])})
    result = {
        "passed": True,
        "scope": "Coverage audit of all frozen general-exclusion certificates, plus separately replayed original post-loop count/registry checks. Not an independent mathematical proof or a successful single full run.",
        "initial_run_passed": not failed,
        "initial_failed_ids": failed,
        "initial_passed_count": len(initial) - len(failed),
        "fresh_complete_selected_pass_count": len(replays),
        "covered_negative_certificates": len(coverage),
        "unique_covered_ids": len({r["id"] for r in coverage}),
        "original_failures_preserved": True,
        "postloop_checks_passed": True,
        "original_full_model_and_import_marker_present": True,
        "original_pre_negative_pipeline_completed": True,
        "baseline_commit": baseline["baseline_commit"],
        "census_sha256": sha(repo / "supplements/rank6/data/census.json"),
        "ledger_sha256": sha(repo / "supplements/rank6/data/decisions.json"),
        "evidence_sha256": {"initial_stream": sha(args.initial), "initial_log": sha(args.initial_log), "replay_index": sha(args.replay_index),
                            "baseline": sha(args.baseline), "postloop": sha(args.postloop)},
        "coverage_canonical_json_sha256": objsha(coverage),
        "coverage_file": coverage_path.name,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with coverage_path.open("xb") as binary:
        with gzip.GzipFile(filename="", mode="wb", fileobj=binary, mtime=0) as stream:
            for rec in coverage:
                stream.write((json.dumps(rec, separators=(",", ":")) + "\n").encode())
    result["coverage_file_sha256"] = sha(coverage_path)
    with args.out.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

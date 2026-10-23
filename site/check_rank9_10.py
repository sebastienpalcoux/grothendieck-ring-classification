#!/usr/bin/env python3
"""Verify the additive release and preservation of the historical site data."""
import ast
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from check_cases import check_tensor, check_browser_integers, implication_closure

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "site/dist"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(source=None):
    data = json.loads((DIST / "data/rank9_rank10_m1.json").read_text())
    receipt = json.loads((DIST / "data/rank9_rank10_m1_build.json").read_text())
    rows = data["cases"]
    source = source or ROOT / data["summary"]["release"]
    require(source.is_dir(), "Research package is not staged: " + str(source))
    require(hashlib.sha256((source / "deliverable/ledger.json").read_bytes()).hexdigest() == data["summary"]["ledger_sha256"], "Published ledger is stale")
    require(receipt["ledger_sha256"] == data["summary"]["ledger_sha256"], "Build receipt and payload bind different ledgers")
    check_browser_integers(data, "rank9_rank10_m1")
    expected = {f"R{rank}_1_{i}" for rank, count in ((9, 142), (10, 194)) for i in range(1, count + 1)}
    require(len(rows) == 336 and {r["id"] for r in rows} == expected, "Incomplete new case inventory")
    require({row["id"] for row in rows if row["investigation_deferred"]} == {f"R10_1_{i}" for i in (114, 115, 152, 153, 179, 189)}, "The six deferred investigations must remain explicit")
    for path, digest in receipt["legacy_sha256"].items():
        require(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, "Historical data changed: " + path)
    old = []
    for file, key in (("realized_rings.json", "records"), ("unresolved_cases.json", "cases"), ("resolved_cases.json", "cases")):
        old += json.loads((DIST / "data" / file).read_text())[key]
    require(not ({r["id"] for r in old} & expected), "New IDs collide with historical IDs")
    for row in rows:
        check_tensor(row, DIST, require_character_presentation=False)
        tensor = ast.literal_eval((DIST / "downloads/fusion-tensors" / (row["id"] + ".txt")).read_text())
        require(tensor == row["fusion_tensor"], "Tensor download differs: " + row["id"])
        digest = hashlib.sha256(json.dumps(tensor, separators=(",", ":")).encode()).hexdigest()
        require(digest == row["tensor_sha256"], "Tensor hash differs: " + row["id"])
        require(row["research"] and row["evidence"] and row["summary"], "Missing case provenance")
        ledger_path = data["summary"]["release"] + "/deliverable/ledger.json"
        ledger_evidence = [item for item in row["evidence"] if item["path"] == ledger_path]
        ledger_reports = [item for item in row["research"] if item["source"] == ledger_path]
        require(len(ledger_evidence) == 1 and ledger_reports and all(item["sha256"] == data["summary"]["ledger_sha256"] for item in ledger_evidence) and all(item["source_sha256"] == data["summary"]["ledger_sha256"] for item in ledger_reports), "Case binds a different ledger: " + row["id"])
        require(not row["investigation_deferred"] or row["status"] == "unresolved", "Deferred case was promoted to a decision")
        if row["investigation_deferred"]:
            scope = row["categorification_scope"]
            same = implication_closure(scope["same_category_implications"])
            existence = implication_closure(scope["same_category_implications"] + scope["existence_implications"])
            require(("general", "spherical") in same and ("general", "pseudo_unitary") not in same,
                    "Sphericality was confused with pseudo-unitarity of the same category")
            require(("general", "pseudo_unitary") in existence and ("general", "unitary") not in existence,
                    "Wrong Galois-existence reduction")
    for rank in (9, 10):
        actual = Counter(r["status"] for r in rows if r["rank"] == rank)
        require(dict(actual) == data["summary"]["counts"][str(rank)], "Status totals differ")
    require(set(data["summary"]["remaining_ids"]) == {r["id"] for r in rows if r["status"] == "unresolved"}, "Current open inventory differs")
    report = DIST / "papers/rank9-rank10-m1.pdf"
    require(report.is_file() and report.read_bytes().startswith(b"%PDF-"), "Missing report PDF")
    require(report.read_bytes() == (source / "deliverable/report.pdf").read_bytes(), "Website report differs from the research package")
    evidence = {item["path"]: item for row in rows for item in row["evidence"]}
    for path, item in evidence.items():
        relative = Path(path).relative_to(data["summary"]["release"])
        local = source / relative
        require(local.is_file() and hashlib.sha256(local.read_bytes()).hexdigest() == item["sha256"], "Missing or stale evidence: " + path)
    for name in ("index.html", "case.html", "unresolved.html", "records.html"):
        require('src="./catalogue.js' in (DIST / name).read_text(), "Missing release integration: " + name)
    print(f"Rank-nine/ten release checked: 336 records and tensor downloads; {len(old)} historical profiles preserved.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, help="External source package used for a staging check")
    args = parser.parse_args()
    check(args.source.resolve() if args.source else None)

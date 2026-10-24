#!/usr/bin/env python3
"""Verify the additive release and preservation of the historical site data."""
import ast
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from publication_identity import matches as publication_matches
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
    continuation = data["summary"].get("continuation_release")
    require(source.is_dir(), "Research package is not staged: " + str(source))
    baseline_digest = hashlib.sha256((source / "deliverable/ledger.json").read_bytes()).hexdigest()
    require(baseline_digest == data["summary"].get("baseline_ledger_sha256", data["summary"]["ledger_sha256"]), "Published baseline ledger is stale")
    if continuation:
        current_ledger = ROOT / data["summary"]["ledger_path"]
        require(hashlib.sha256(current_ledger.read_bytes()).hexdigest() == data["summary"]["ledger_sha256"], "Current accepted ledger is stale")
        current = json.loads(current_ledger.read_text())
        accepted = {r["id"]: r for r in current["records"]}
        retry=bool(data['summary'].get('theoretical_retry'))
        require({r['id']for r in rows if r['status']=='unresolved'}==(set()if retry else {'R10_1_189'}),'Rank-ten open frontier differs')
        require(Counter(data['summary']['counts']['10'])==Counter(excluded=136,unitarily_realized=58)if retry else data['summary']['counts']['10']=={'excluded':136,'unitarily_realized':57,'unresolved':1},'Rank-ten continuation totals differ')
        for row in rows:
            require(row["status"] == accepted[row["id"]]["status"] and row["tensor_sha256"] == accepted[row["id"]]["tensor_sha256_compact_json"], "Case differs from current accepted ledger: " + row["id"])
    require(receipt["ledger_sha256"] == data["summary"]["ledger_sha256"], "Build receipt and payload bind different ledgers")
    check_browser_integers(data, "rank9_rank10_m1")
    expected = {f"R{rank}_1_{i}" for rank, count in ((9, 142), (10, 194)) for i in range(1, count + 1)}
    require(len(rows) == 336 and {r["id"] for r in rows} == expected, "Incomplete new case inventory")
    require({row["id"] for row in rows if row["investigation_deferred"]} == (set() if continuation else {f"R10_1_{i}" for i in (114, 115, 152, 153, 179, 189)}), "Deferred investigation inventory differs")
    for path, digest in receipt["legacy_sha256"].items():
        require(publication_matches(path,digest), "Historical data changed: " + path)
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
        ledger_path = row["source_file"]
        expected_digest = hashlib.sha256((ROOT/ledger_path).read_bytes()).hexdigest()
        ledger_evidence = [item for item in row["evidence"] if item["path"] == ledger_path]
        ledger_reports = [item for item in row["research"] if item["source"] == ledger_path]
        require(len(ledger_evidence) == 1 and ledger_reports and all(item["sha256"] == expected_digest for item in ledger_evidence) and all(item["source_sha256"] == expected_digest for item in ledger_reports), "Case binds a different ledger: " + row["id"])
        require(not row["investigation_deferred"] or row["status"] == "unresolved", "Deferred case was promoted to a decision")
        if row["investigation_deferred"] or (continuation and row["id"] == "R10_1_189" and row['status']=='unresolved'):
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
    report_source = ROOT / "publications/rank9-rank10/paper/rank9-rank10.pdf" if continuation else source / "deliverable/report.pdf"
    require(report.read_bytes() == report_source.read_bytes(), "Website report differs from the current manuscript")
    evidence = {item["path"]: item for row in rows for item in row["evidence"]}
    for path, item in evidence.items():
        if path.startswith(data["summary"]["release"] + "/"):
            local = source / Path(path).relative_to(data["summary"]["release"])
        else:
            require(bool(continuation) and any(path.startswith(x+'/')for x in (continuation,data['summary'].get('theoretical_retry','__none__'))), 'Unexpected evidence root: '+path)
            local = ROOT / path
        require(local.is_file() and hashlib.sha256(local.read_bytes()).hexdigest() == item["sha256"], "Missing or stale evidence: " + path)
    for name in ("index.html", "case.html", "unresolved.html", "records.html"):
        require('src="./catalogue.js' in (DIST / name).read_text(), "Missing release integration: " + name)
    print(f"Rank-nine/ten release checked: 336 records and tensor downloads; {len(old)} historical profiles preserved.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, help="External source package used for a staging check")
    args = parser.parse_args()
    check(args.source.resolve() if args.source else None)

#!/usr/bin/env python3
"""Check a repository-derived atlas snapshot before publication."""
import csv
import json
from pathlib import Path

root = Path(__file__).resolve().parent / "dist"
payload = json.loads((root / "data/atlas.json").read_text())
status_payload=json.loads((root / "data/classification_status.json").read_text())
rows = payload["rows"]
assert rows, "No census rows"
assert len(rows) == len({(r["rank"], r["multiplicity"]) for r in rows}), "Duplicate cells"
assert all(isinstance(r["rings"], int) and r["rings"] >= 0 for r in rows), "Invalid counts"
assert all(r["source"] for r in rows), "Missing provenance"
index = {(r["rank"], r["multiplicity"]):r["rings"] for r in rows}
positive = {(r["rank"],r["multiplicity"]):r["rings"] for r in payload["grothendieck_rows"]}
positive_flags={(r["rank"],r["multiplicity"]):r["is_lower_bound"] for r in payload["grothendieck_rows"]}
assert all(n>0 for n in positive.values()), "Zero-only Grothendieck rows are not displayed"
models=json.loads((root/"data/realized_rings.json").read_text())["records"]
from collections import Counter
model_counts=Counter((r["rank"],r["multiplicity"]) for r in models)
assert model_counts==positive, "Displayed Grothendieck counts do not match explicit model records"
assert len(models)==len({r["id"] for r in models}), "Duplicate model identifier"
assert all(r["model_reference"] and r["source_file"] and r["fusion_tensor"] for r in models)
for record in status_payload["rows"]:
    key = record["rank"], record["multiplicity"]
    assert index.get(key)==record["rings"], f"Status count mismatch at {key}"
    statuses = ("excluded_general","realized_unitary","realized_other_or_unspecified",
                "realized_spherical_nonpseudounitary","unresolved_general","unassessed")
    assert sum(record[status] for status in statuses)==record["rings"], f"Status partition mismatch at {key}"
    assert positive.get(key,0)==sum(record[field] for field in ("realized_unitary","realized_other_or_unspecified","realized_spherical_nonpseudounitary")), f"Positive model mismatch at {key}"
    if key in positive_flags:
        assert positive_flags[key]==(record["classification_coverage"]!="complete_classification"),f"Incomplete band shown as exact at {key}"
rank5={r["multiplicity"]:r for r in status_payload["rows"] if r["rank"]==5}
if 20 in rank5:
    assert all(m in rank5 and rank5[m]["classification_coverage"]=="complete_classification"
               and rank5[m]["unresolved_general"]==0 for m in range(1,21)), \
        "Rank-five complete-through-20 manuscript cannot accompany a stale open-status ledger"
with (root / "data/counts.csv").open(newline="") as stream:
    csv_rows = list(csv.DictReader(stream))
assert len(csv_rows) == len(rows), "CSV / JSON mismatch"
assert (root / "index.html").exists() and (root / "styles.css").exists() and (root / "app.js").exists()
print(f"Atlas checked: {len(rows)} analyzed cells, {len(models)} explicit Grothendieck rings, {len({r['rank'] for r in rows})} ranks")

rank6 = {r["multiplicity"]: r for r in status_payload["rows"] if r["rank"] == 6}
release = payload["rank6_release"]
summary=json.loads((root / release["summary_path"]).read_text())
summary_counts={r["multiplicity"]:r for r in summary["counts"]}
expected_bands=sorted(summary_counts)
assert expected_bands and len(summary_counts)==len(summary["counts"])
assert expected_bands==list(range(1,expected_bands[-1]+1)), "Rank-six summary has a coverage gap"
assert sorted(rank6)==expected_bands, "Rank-six site and release summary cover different multiplicities"
assert all(rank6[m]["unresolved_general"]==summary_counts[m]["unresolved"] for m in expected_bands)
assert all(rank6[m]["rings"]==summary_counts[m]["classes"] for m in expected_bands)
assert sum(r["excluded_general"] for r in rank6.values()) == summary["excluded"]
assert all(rank6[m]["classification_coverage"] == "complete_classification" for m in release["complete_multiplicity_bands"])
assert release["complete_multiplicity_bands"] == [r["multiplicity"] for r in summary["counts"] if r["unresolved"] == 0]
scope6=next(r for r in payload["scope"] if r["rank"] == 6)
assert scope6["analyzed_through"]==expected_bands[-1]
assert release.get("analyzed_through",scope6["analyzed_through"])==expected_bands[-1]
assert (scope6["through"],scope6["positive"],scope6["unresolved"]) == (release["complete_through"],summary["positive"],summary["unresolved"])
assert release["date"] == payload["snapshot"]
coverage=json.loads((root / release["research_coverage_path"]).read_text())
assert release["research_cases"] == [{key: case[key] for key in ("id", "categorical_status", "public_summary")} for case in coverage["cases"]]
assert {r["id"] for r in release["research_cases"]} == set(summary["unresolved_ids"])
assert all(r["categorical_status"] == "unresolved" and r["public_summary"] for r in release["research_cases"])
import hashlib
archive=root / release["archive"]["path"]
assert hashlib.sha256(archive.read_bytes()).hexdigest() == release["archive"]["sha256"]
assert archive.stat().st_size == release["archive"]["bytes"]
for name,expected in release["documents"].items():
    assert hashlib.sha256((root / "papers" / name).read_bytes()).hexdigest() == expected
frontier=json.loads((root / release["frontier_path"]).read_text())
assert len(frontier) == summary["unresolved"]
assert [r["id"] for r in frontier] == summary["unresolved_ids"]
assert not any(r["m"] in release["complete_multiplicity_bands"] for r in frontier)
print(f"Rank-six release verified through multiplicity {expected_bands[-1]}: complete bands {release['complete_multiplicity_bands']}; {len(frontier)} residuals; exact archive and PDF hashes.")

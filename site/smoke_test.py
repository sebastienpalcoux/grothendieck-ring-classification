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
expected_open = [0, 0, 0, 7, 2, 3, 2, 8]
assert [rank6[m]["unresolved_general"] for m in range(1, 9)] == expected_open
assert sum(r["excluded_general"] for r in rank6.values()) == 16536
assert all(rank6[m]["classification_coverage"] == "complete_classification" for m in range(1, 4))
scope6 = next(r for r in payload["scope"] if r["rank"] == 6)
assert (scope6["through"], scope6["positive"], scope6["unresolved"]) == (3, 54, 22)
import hashlib
release = payload["rank6_release"]
archive = root / release["archive"]["path"]
assert hashlib.sha256(archive.read_bytes()).hexdigest() == release["archive"]["sha256"] == "c9508a49228f199e8f4bf476edddb72a0eddcce45b6e249a11b9f49105de2467"
assert archive.stat().st_size == release["archive"]["bytes"] == 9398369
assert hashlib.sha256((root / "papers/rank6.pdf").read_bytes()).hexdigest() == "e50d39340aca45e92b78f5334049f29f63f457494f5bbfaca4ec0f7c59e6fa1a"
assert hashlib.sha256((root / "papers/rank6_guide.pdf").read_bytes()).hexdigest() == "349fb90e3c3c5562d8bb6033dca7443527b45c739c08e68cb8323545c161ed6f"
frontier = json.loads((root / release["frontier_path"]).read_text())
assert len(frontier) == 22 and not any(r["id"] == "R6_3_215" for r in frontier)
print("Rank-six release verified: complete through 3, 22 residuals, exact archive and PDF hashes.")

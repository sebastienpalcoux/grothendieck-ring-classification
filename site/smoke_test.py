#!/usr/bin/env python3
"""Check a repository-derived atlas snapshot before publication."""
import csv
import json
from pathlib import Path

root = Path(__file__).resolve().parent / "dist"
payload = json.loads((root / "data/atlas.json").read_text())
rows = payload["rows"]
assert rows, "No census rows"
assert len(rows) == len({(r["rank"], r["multiplicity"]) for r in rows}), "Duplicate cells"
assert all(isinstance(r["rings"], int) and r["rings"] >= 0 for r in rows), "Invalid counts"
assert all(r["source"] for r in rows), "Missing provenance"
index = {(r["rank"], r["multiplicity"]):r["rings"] for r in rows}
for record in payload["classification_rows"]:
    key = record["rank"], record["multiplicity"]
    assert index.get(key)==record["rings"], f"Status count mismatch at {key}"
    statuses = ("excluded_general","realized_unitary","realized_other_or_unspecified",
                "realized_spherical_nonpseudounitary","unresolved_general","unassessed")
    assert sum(record[status] for status in statuses)==record["rings"], f"Status partition mismatch at {key}"
with (root / "data/counts.csv").open(newline="") as stream:
    csv_rows = list(csv.DictReader(stream))
assert len(csv_rows) == len(rows), "CSV / JSON mismatch"
assert (root / "index.html").exists() and (root / "styles.css").exists() and (root / "app.js").exists()
print(f"Atlas checked: {len(rows)} distinct cells, {len({r['rank'] for r in rows})} ranks")

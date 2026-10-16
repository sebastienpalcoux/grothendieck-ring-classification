#!/usr/bin/env python3
"""Check a repository-derived atlas snapshot before publication."""
import csv
import hashlib
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
assert release["date"] <= payload["snapshot"]
coverage=json.loads((root / release["research_coverage_path"]).read_text())
assert payload["snapshot"] == max(release["date"], coverage["date"], payload.get("theoretical_update", {}).get("date", ""))
assert release["research_cases"] == [{key: case[key] for key in ("id", "categorical_status", "public_summary")} for case in coverage["cases"]]
assert {r["id"] for r in release["research_cases"]} == set(summary["unresolved_ids"])
assert all(r["categorical_status"] == "unresolved" and r["public_summary"] for r in release["research_cases"])
chain = release["research_coverage_chain"]
assert chain, "Missing rank-six research provenance chain"
previous = None
for entry in chain:
    source = root / entry["path"]
    assert hashlib.sha256(source.read_bytes()).hexdigest() == entry["sha256"]
    record = json.loads(source.read_text())
    assert record["date"] == entry["date"]
    assert record["classification_counts"] == coverage["classification_counts"]
    if previous:
        assert record["previous_coverage"] == previous["source"]
        assert record["previous_coverage_sha256"] == previous["sha256"]
    previous = entry
assert chain[-1]["source"] == release["research_coverage_source"]
assert hashlib.sha256((root / release["research_coverage_path"]).read_bytes()).hexdigest() == chain[-1]["sha256"]
assert coverage["classification_counts"] == {
    "total": sum(r["classes"] for r in summary["counts"]),
    "excluded": summary["excluded"], "realized": summary["positive"], "unresolved": summary["unresolved"]
}
if "research_addendum" in release:
    addendum=release["research_addendum"]
    assert hashlib.sha256((root / addendum["path"]).read_bytes()).hexdigest() == addendum["sha256"]
archive=root / release["archive"]["path"]
assert hashlib.sha256(archive.read_bytes()).hexdigest() == release["archive"]["sha256"]
assert archive.stat().st_size == release["archive"]["bytes"]
for name,expected in release["documents"].items():
    assert hashlib.sha256((root / "papers" / name).read_bytes()).hexdigest() == expected
frontier=json.loads((root / release["frontier_path"]).read_text())
assert len(frontier) == summary["unresolved"]
assert [r["id"] for r in frontier] == summary["unresolved_ids"]
assert not any(r["m"] in release["complete_multiplicity_bands"] for r in frontier)
identity = json.loads((root / release["identity_path"]).read_text())
canonical_identity = root.parent.parent / "data/rank6_release_identity.json"
if canonical_identity.is_file():
    assert canonical_identity.read_bytes() == (root / release["identity_path"]).read_bytes()
assert chain[0]["source"] == "supplements/rank6/data/frontier_research_progress.json"
assert chain[0]["sha256"] == identity["research_files_sha256"]["data/frontier_research_progress.json"]
assert chain[0]["date"] == identity["date"]
totals = tuple(identity["summary"][key] for key in ("excluded", "positive", "unresolved"))
assert tuple(summary[key] for key in ("excluded", "positive", "unresolved")) == totals
assert tuple(release[key] for key in ("excluded", "realized", "unresolved")) == totals
bands = [[summary_counts[m][key] for key in ("classes", "excluded", "unitarily_realized",
          "spherically_realized_nonpseudounitary", "unresolved")] for m in expected_bands]
assert bands == identity["counts"], "Site rank-six bands differ from the frozen release identity"
assert release["date"] == identity["date"]
assert summary["ledger_sha256"] == identity["ledger_sha256"]
assert release["archive"]["path"] == "downloads/" + identity["archive"]["name"]
assert release["archive"]["sha256"] == identity["archive"]["sha256"]
assert release["archive"]["bytes"] == identity["archive"]["bytes"]
revision = None
if "document_revision" in release:
    revision_entry = release["document_revision"]
    revision_path = root / revision_entry["path"]
    assert hashlib.sha256(revision_path.read_bytes()).hexdigest() == revision_entry["sha256"]
    revision = json.loads(revision_path.read_text())
    canonical_revision = root.parent.parent / revision_entry.get("source", "evidence/rank6_theoretical_20261011/document_revision.json")
    if canonical_revision.is_file():
        assert canonical_revision.read_bytes() == revision_path.read_bytes()
    assert revision["date"] == revision_entry["date"] == coverage["date"]
    assert revision["research_progress"] == release["research_coverage_source"]
    assert revision["research_progress_sha256"] == chain[-1]["sha256"]
    assert all(name.startswith("manuscripts/rank6/papers/") and Path(name).suffix in (".tex", ".pdf")
               and len(record["sha256"]) == 64 and record["bytes"] > 0
               for name, record in revision["documents"].items())
for source, target in (("manuscript.pdf", "rank6.pdf"), ("verification_guide.pdf", "rank6_guide.pdf")):
    expected = (revision["documents"]["manuscripts/rank6/papers/" + source]
                if revision else identity["documents"][source])
    assert release["documents"][target] == expected["sha256"], "Site PDF differs from its current revision: " + target
    assert (root / "papers" / target).stat().st_size == expected["bytes"]
print(f"Rank-six release verified through multiplicity {expected_bands[-1]}: complete bands {release['complete_multiplicity_bands']}; {len(frontier)} residuals; frozen archive and current document revision hashes.")

for rank in (7, 8):
    release = payload["upper_rank_releases"][str(rank)]
    for document in (release["manuscript"], release["archive"]):
        path = root / document["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == document["sha256"]
        if "bytes" in document:
            assert path.stat().st_size == document["bytes"]
    expected = next(b["sha256"] for b in status_payload["bundles"]
                    if b["name"] == Path(release["archive"]["path"]).name)
    assert release["archive"]["sha256"] == expected
print("Upper-rank manuscripts and portable supplements match their publication hashes.")

update = payload.get("theoretical_update")
if update:
    assert update["date"] == "2026-10-16" and update["source"] in ("evidence/theoretical_20261016", "evidence/unified_20261016")
    decisions = update["decisions"]
    assert len(decisions) == len({record["id"] for record in decisions})
    assert update["new_general_exclusions"] == sum(d["status"] == "excluded" for d in decisions)
    assert update.get("new_unitary_models", 0) == sum(d["status"] == "unitarily_realized" for d in decisions)
    assert all(record["status"] in ("excluded", "unitarily_realized") and record["scope"] == "general_complex" and record["rank"] in (7,8)
               for record in decisions), "A scoped obstruction entered the general-exclusion notice"
    for key, entry in update["files"].items():
        assert hashlib.sha256((root / entry["path"]).read_bytes()).hexdigest() == entry["sha256"]
    assert json.loads((root / update["files"]["decisions"]["path"]).read_text()) == decisions
    remaining = json.loads((root / update["files"]["remaining_ids"]["path"]).read_text())
    totals = json.loads((root / update["files"]["expected_totals"]["path"]).read_text())
    assert update["remaining"] == {rank: len(ids) for rank, ids in remaining.items()}
    for rank in (7,8):
        assert update["by_rank"][str(rank)] == sum(record["rank"] == rank for record in decisions)
        scope = next(record for record in payload["scope"] if record["rank"] == rank)
        assert scope["unresolved"] == len(remaining[str(rank)]) == totals[str(rank)]["unresolved"]
        assert scope["positive"] == totals[str(rank)]["unitarily_realized"]
        assert scope["rings"] - scope["positive"] - scope["unresolved"] == totals[str(rank)]["excluded"]
    archive = root / update["archive"]["path"]
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == update["archive"]["sha256"]
    assert archive.stat().st_size == update["archive"]["bytes"]
    import zipfile
    with zipfile.ZipFile(archive) as bundle:
        matches = [name for name in bundle.namelist()
                   if name == "decisions.json" or name.endswith(update["source"].split("/")[-1] + "/decisions.json")]
        assert len(matches) == 1 and json.loads(bundle.read(matches[0])) == decisions, "Stale update bundle"
    assert set(remaining["6"]) == {record["id"] for record in frontier}
    print(f"Theoretical update checked: {len(decisions)} proved decisions; counts, proof records, residual inventory and download hashes agree.")

from html.parser import HTMLParser
class LocalLinkCheck(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("href", "src") and value and value.startswith("./"):
                assert (root / value[2:].split("#",1)[0]).is_file(), "Missing local page asset: " + value
LocalLinkCheck().feed((root / "index.html").read_text())

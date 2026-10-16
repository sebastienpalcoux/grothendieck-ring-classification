#!/usr/bin/env python3
"""Check a repository-derived atlas snapshot before publication."""
import csv
import argparse
import tempfile
import urllib.request
import ast
import hashlib
import json
from pathlib import Path

TRUSTED_PROOF_BUNDLE_URL = "https://sebastienpalcoux.github.io/grothendieck-ring-classification/downloads/review-update-2026-10-17.zip"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--proof-bundle", type=Path, help="Verify this local copy of the externally hosted proof ZIP")
args = parser.parse_args()
proof_temporary_directory = None

root = Path(__file__).resolve().parent / "dist"
payload = json.loads((root / "data/atlas.json").read_text())
status_payload=json.loads((root / "data/classification_status.json").read_text())
scope4 = next(r for r in payload['scope'] if r['rank'] == 4)
assert scope4['kind'] == 'unrestricted' and scope4['through'] is None
assert scope4['positive'] == 15 and scope4['unresolved'] == 0
assert status_payload['inputs']['rank4']['classification_scope'] == 'unrestricted'
assert 'https://arxiv.org/abs/2609.33272' in (root / 'app.js').read_text()
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
assert payload["snapshot"] == max(release["date"], coverage["date"], payload.get("theoretical_update", {}).get("date", ""), payload["current_documents"]["date"])
assert [(case["id"], case["categorical_status"]) for case in release["research_cases"]] == [(case["id"], case["categorical_status"]) for case in coverage["cases"]]
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
    assert revision["date"] == revision_entry["date"]
    assert revision["schema"] == "current-document-revision/v1"
    assert all(Path(name).suffix in (".tex", ".pdf") and len(record["sha256"]) == 64 and record["bytes"] > 0
               for name, record in revision["documents"].items())
for source, target in (("manuscript.pdf", "rank6.pdf"), ("verification_guide.pdf", "rank6_guide.pdf")):
    expected = (revision["documents"]["manuscripts/rank6/papers/" + source]
                if revision else identity["documents"][source])
    assert release["documents"][target] == expected["sha256"], "Site PDF differs from its current revision: " + target
    assert (root / "papers" / target).stat().st_size == expected["bytes"]
print(f"Rank-six release verified through multiplicity {expected_bands[-1]}: complete bands {release['complete_multiplicity_bands']}; {len(frontier)} residuals; dataset and current document manifest hashes.")

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

current_entry = payload["current_documents"]
current_manifest_path = root / current_entry["path"]
assert hashlib.sha256(current_manifest_path.read_bytes()).hexdigest() == current_entry["sha256"]
current_manifest = json.loads(current_manifest_path.read_text())
assert current_manifest["schema"] == "current-document-revision/v1"
assert current_manifest["date"] == current_entry["date"]
assert {f"papers/rank{rank}.pdf" for rank in range(2,9)} <= set(current_manifest["web_copies"])
for local, canonical in current_manifest["web_copies"].items():
    expected = current_manifest["documents"][canonical]
    document = root / local
    assert document.read_bytes().startswith(b"%PDF-")
    assert document.stat().st_size == expected["bytes"]
    assert hashlib.sha256(document.read_bytes()).hexdigest() == expected["sha256"], "Stale website manuscript: " + local
print("All current website manuscripts match the publication manifest.")

reader = payload["reader_resources"]
assert set(reader["files"]) == {"remaining_cases.py", "manuscript_page_counts.json"}
for name, record in reader["files"].items():
    raw = (root / record["path"]).read_bytes()
    assert record["path"] == "downloads/" + name
    assert hashlib.sha256(raw).hexdigest() == record["sha256"], "Reader resource hash: " + name
    canonical = root.parent.parent / "data" / name
    if canonical.is_file():
        assert canonical.read_bytes() == raw, "Reader resource differs from repository: " + name
pages = json.loads((root / reader["files"]["manuscript_page_counts.json"]["path"]).read_text())
assert pages["document_counts"] == {"mathematical_manuscripts": 8, "verification_guides": 3, "research_status_reports": 1}
assert len(pages["documents"]) == len({r["path"] for r in pages["documents"]}) == 12
for record in pages["documents"]:
    assert {key: record[key] for key in ("bytes", "sha256")} == current_manifest["documents"][record["path"]]
    assert type(record["pages"]) is int and record["pages"] > 0
sums = {kind: sum(r["pages"] for r in pages["documents"] if r["kind"] == kind)
        for kind in ("mathematical_manuscript", "verification_guide", "research_status_report")}
sums["mathematical_manuscripts_and_guides"] = sums["mathematical_manuscript"] + sums["verification_guide"]
sums["all_distinct_documents"] = sum(r["pages"] for r in pages["documents"])
assert sums == pages["totals"] == reader["page_totals"]
page_summary = (f"Eight mathematical manuscripts: {sums['mathematical_manuscript']} pages; "
                f"with the three verification guides: {sums['mathematical_manuscripts_and_guides']}; "
                f"with the research-status report: {sums['all_distinct_documents']}. "
                "Each distinct document is counted once.")
assert '<span id="manuscript-page-summary">' + page_summary + '</span>' in (root / "index.html").read_text()
tree = ast.parse((root / reader["files"]["remaining_cases.py"]["path"]).read_text())
constants = {node.targets[0].id: ast.literal_eval(node.value) for node in tree.body
             if isinstance(node, ast.Assign) and node.targets[0].id != "TENSORS"}
assert set(constants["METADATA"]) == set(constants["DUALS"]) == {"R6_4_155", "R6_8_1660"}
for name, metadata in constants["METADATA"].items():
    assert isinstance(constants[name], list) and len(constants[name]) == metadata["rank"]
    assert metadata["status"] == "unresolved" and metadata["unit_index"] == 0
    assert hashlib.sha256(json.dumps(constants[name], separators=(",", ":")).encode()).hexdigest() == metadata["tensor_sha256"]
print("Reader downloads checked: two exact tensor constants and twelve distinct PDF page counts.")

update = payload.get("theoretical_update")
if update:
    stage_dates = {"evidence/theoretical_20261016": "2026-10-16",
                   "evidence/unified_20261016": "2026-10-16",
                   "evidence/review_20261017": "2026-10-17",
                   "evidence/rigidity_20261017": "2026-10-17"}
    assert update["source"] in stage_dates and update["date"] == stage_dates[update["source"]]
    is_review = update["source"] == "evidence/review_20261017"
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
    if is_review:
        assert "reading_edition" not in payload["upper_rank_releases"]["8"]
        assert payload["upper_rank_releases"]["8"]["manuscript"]["path"] == "papers/rank8.pdf"
        assert update["proofs_source"] == "evidence/unified_20261016"
        assert len(decisions) == 35 and update["original_case_count"] == 38
        assert (update["new_general_exclusions"], update["new_unitary_models"]) == (28, 7)
        assert "R8_2_24" not in {record["id"] for record in decisions}
        assert remaining == {"6": ["R6_4_155", "R6_8_1660"], "7": [], "8": ["R8_2_24"]}
        assert totals["8"] == {"excluded": 895, "unitarily_realized": 77, "unresolved": 1}
        scope8 = next(record for record in payload["scope"] if record["rank"] == 8)
        assert (scope8["through"], scope8["analyzed_through"], scope8["kind"]) == (1, 2, "partial")
        assert positive_flags[(8, 2)] and positive[(8, 2)] == 29
        band8 = next(record for record in status_payload["rows"] if (record["rank"], record["multiplicity"]) == (8, 2))
        assert (band8["rings"], band8["excluded_general"], band8["unresolved_general"], band8["classification_coverage"]) == (877, 847, 1, "partial_classification")
    if update["source"] == "evidence/rigidity_20261017":
        assert len(decisions) == 36 and update["original_case_count"] == 38
        assert (update["new_general_exclusions"], update["new_unitary_models"]) == (29, 7)
        assert remaining == {"6": ["R6_4_155", "R6_8_1660"], "7": [], "8": []}
        assert totals["8"] == {"excluded": 896, "unitarily_realized": 77, "unresolved": 0}
        r24 = next(record for record in decisions if record["id"] == "R8_2_24")
        assert r24["status"] == "excluded" and r24["proof_source"] == update["source"]
        scope8 = next(record for record in payload["scope"] if record["rank"] == 8)
        assert (scope8["through"], scope8["analyzed_through"], scope8["kind"]) == (2, 2, "complete")
        assert not positive_flags[(8, 2)] and positive[(8, 2)] == 29
        band8 = next(record for record in status_payload["rows"] if (record["rank"], record["multiplicity"]) == (8, 2))
        assert (band8["rings"], band8["excluded_general"], band8["unresolved_general"], band8["classification_coverage"]) == (877, 848, 0, "complete_classification")
    for rank in (7,8):
        assert update["by_rank"][str(rank)] == sum(record["rank"] == rank for record in decisions)
        scope = next(record for record in payload["scope"] if record["rank"] == rank)
        assert scope["unresolved"] == len(remaining[str(rank)]) == totals[str(rank)]["unresolved"]
        assert scope["positive"] == totals[str(rank)]["unitarily_realized"]
        assert scope["rings"] - scope["positive"] - scope["unresolved"] == totals[str(rank)]["excluded"]
    archive_metadata = update["archive"]
    external_url = archive_metadata.get("url")
    if external_url:
        assert external_url == TRUSTED_PROOF_BUNDLE_URL, "Untrusted external proof-bundle URL"
        assert archive_metadata["path"] == "downloads/review-update-2026-10-17.zip"
        if args.proof_bundle:
            archive = args.proof_bundle.resolve()
        else:
            proof_temporary_directory = tempfile.TemporaryDirectory(prefix="atlas-proof-check-")
            archive = Path(proof_temporary_directory.name) / "proof-bundle.zip"
            with urllib.request.urlopen(TRUSTED_PROOF_BUNDLE_URL, timeout=60) as response:
                assert response.geturl() == TRUSTED_PROOF_BUNDLE_URL, "Unexpected proof-bundle redirect"
                raw = response.read(archive_metadata["bytes"] + 1)
            assert len(raw) == archive_metadata["bytes"], "External proof-bundle size mismatch"
            archive.write_bytes(raw)
    else:
        assert args.proof_bundle is None, "--proof-bundle requires an external archive URL in the snapshot"
        archive = root / archive_metadata["path"]
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == update["archive"]["sha256"]
    assert archive.stat().st_size == update["archive"]["bytes"]
    import zipfile
    with zipfile.ZipFile(archive) as bundle:
        matches = [name for name in bundle.namelist()
                   if name == "decisions.json" or name.endswith(update["source"].split("/")[-1] + "/decisions.json")]
        assert len(matches) == 1 and json.loads(bundle.read(matches[0])) == decisions, "Stale update bundle"
        if is_review:
            for relative in set(revision["web_copies"].values()) | {"data/current_document_revision.json"}:
                documents = [name for name in bundle.namelist()
                             if name == relative or name.endswith("/" + relative)]
                canonical = root.parent.parent / relative
                assert len(documents) == 1, "Missing current document in archive: " + relative
                if canonical.is_file():
                    assert bundle.read(documents[0]) == canonical.read_bytes(), "Stale current document in archive: " + relative
            for decision in decisions:
                proof_path = update["proofs_source"] + "/" + decision["proof"]
                assert any(name == proof_path or name.endswith("/" + proof_path) for name in bundle.namelist()), "Missing inherited proof: " + proof_path
    assert set(remaining["6"]) == {record["id"] for record in frontier}
    print(f"Current update checked: {len(decisions)} accepted decision records; counts, source records, residual inventory and download hashes agree.")

from html.parser import HTMLParser
class LocalLinkCheck(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("href", "src") and value and value.startswith("./"):
                relative = value[2:].split("#",1)[0]
                assert not relative or (root / relative).is_file(), "Missing local page asset: " + value
for filename in ("index.html", "review.html"):
    LocalLinkCheck().feed((root / filename).read_text())
reader_sources = "\n".join((root / filename).read_text() for filename in ("index.html", "review.html", "app.js"))
for stale in ("rank8-reviewed.pdf", "Historical PDF", "Read reviewed edition", "Printable manuscript errata", "has been reopened", "Read with dated corrections"):
    assert stale not in reader_sources, "Obsolete publication wording or link: " + stale
assert "AI-generated research" in (root / "index.html").read_text()
assert all(case in (root / "review.html").read_text() for case in ("R6_4_155", "R6_8_1660", "R8_2_24"))

assert "docs/CASE_INVENTORY.md" in (root / "app.js").read_text(), "Missing current case-inventory route"
assert "ALL38_COVERAGE.md" not in reader_sources, "Reader route points to an immutable stage guide"
assert "tree/main/evidence/review_20261017" not in reader_sources, "Reader route points to an immutable stage overview"

if proof_temporary_directory is not None:
    proof_temporary_directory.cleanup()

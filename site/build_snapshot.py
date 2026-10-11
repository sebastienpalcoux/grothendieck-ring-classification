#!/usr/bin/env python3
"""Build the site snapshot from the exact, curated classification repository.

Run this in the site checkout with --classification PATH. The repository's
data/counts.json is the source of truth; no count is scraped from a PDF.
"""
import argparse
import csv
import json
import hashlib
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read_counts(path: Path):
    payload = json.loads(path.read_text())
    if isinstance(payload, list):
        return {"rows": payload}
    for key in ("rows", "counts", "data"):
        if isinstance(payload.get(key), list):
            payload["rows"] = payload[key]
            return payload
    raise ValueError(f"No count rows in {path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--classification", type=Path, required=True)
    parser.add_argument("--classification-commit", help="Full immutable commit containing this verified research release")
    args = parser.parse_args()
    if args.classification_commit and (len(args.classification_commit) != 40 or any(c not in "0123456789abcdef" for c in args.classification_commit)):
        parser.error("--classification-commit requires a full 40-character commit SHA")
    repo = args.classification.resolve()
    counts = read_counts(repo / "data" / "counts.json")
    rows = []
    for row in counts["rows"]:
        rank = int(row["rank"])
        multiplicity = int(row["multiplicity"])
        rings = int(row["rings"])
        if min(rank, multiplicity, rings) < 0:
            raise ValueError(f"Negative coordinate/count: {row}")
        if "source" not in row:
            raise ValueError(f"Missing source: {row}")
        rows.append({
            "rank": rank,
            "multiplicity": multiplicity,
            "rings": rings,
            "source": row["source"],
            "verification": row.get("verification", ""),
        })
    keys = [(r["rank"], r["multiplicity"]) for r in rows]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate rank/multiplicity")
    rows.sort(key=lambda r: (r["rank"], r["multiplicity"]))
    for summary in counts.get("rank_summary", []):
        band = [r for r in rows if r["rank"] == summary["rank"]]
        expected = list(range(1,summary["recorded_through"]+1))
        if [r["multiplicity"] for r in band] != expected:
            raise ValueError(f"Incomplete census coverage for rank {summary['rank']}")
        if sum(r["rings"] for r in band) != summary["classes_at_recorded_bound"]:
            raise ValueError(f"Cumulative census mismatch for rank {summary['rank']}")
    status_file = repo / "data" / "classification_status.json"
    status = json.loads(status_file.read_text())
    if not isinstance(status.get("rows"), list):
        raise ValueError("Classification status file has no rows")
    census_index = {(r["rank"], r["multiplicity"]):r["rings"] for r in rows}
    classifications = status["rows"]
    for record in classifications:
        key=(record["rank"],record["multiplicity"])
        if census_index.get(key) != record["rings"]:
            raise ValueError(f"Census/ledger mismatch for {key}")
        fields = ("excluded_general","realized_unitary","realized_other_or_unspecified",
                  "realized_spherical_nonpseudounitary","unresolved_general","unassessed")
        if sum(record[k] for k in fields) != record["rings"]:
            raise ValueError(f"Status sum mismatch for {key}")
    # Publish ranks with a manuscript and a genuine categorification ledger.
    # A census-only rank is never represented as classified research.
    classifications = [r for r in classifications if 2 <= r["rank"] <= 8 and
                       r["classification_coverage"]!="census_only"]
    covered = {(r["rank"],r["multiplicity"]) for r in classifications}
    rows = [r for r in rows if (r["rank"],r["multiplicity"]) in covered]
    def positive(record):
        return sum(record[field] for field in (
            "realized_unitary", "realized_other_or_unspecified",
            "realized_spherical_nonpseudounitary"))
    positive_rows = [{"rank":r["rank"],"multiplicity":r["multiplicity"],"rings":positive(r),
                      "is_lower_bound":r["classification_coverage"]!="complete_classification"}
                     for r in classifications if positive(r)>0]
    def scope_record(rank):
        band=sorted((r for r in classifications if r["rank"]==rank),key=lambda r:r["multiplicity"])
        through=0
        for r in band:
            if r["multiplicity"]!=through+1 or r["classification_coverage"]!="complete_classification":break
            through+=1
        unresolved=sum(r["unresolved_general"] for r in band)
        return {"rank":rank,"through":through,"analyzed_through":max(r["multiplicity"] for r in band),
                "kind":"complete" if len(band)==through else "partial",
                "rings":sum(r["rings"] for r in band),"positive":sum(positive(r) for r in band),
                "unresolved":unresolved,
                "paper":f"Rank-{rank} classification manuscript",
                "note":("General existence remains open for the stated residuals." if unresolved else
                        "All analyzed bands are classified by a model or exclusion.")}
    scoped_ranks=sorted({r["rank"] for r in classifications})
    scope=[{"rank":rank,"through":None,"analyzed_through":None,"kind":"unrestricted",
            "rings":None,"positive":sum(positive(r) for r in classifications if r["rank"]==rank),
            "unresolved":0,"paper":f"Rank-{rank} classification manuscript",
            "note":"Unrestricted complex classification."}
           if rank in (2,3) else scope_record(rank) for rank in scoped_ranks]
    data = {
        "snapshot": None,
        "classification_commit": args.classification_commit,
        "source_repository": counts.get("census_repository", "https://github.com/sebastienpalcoux/fusion-ring-census"),
        "census_commit": counts.get("census_commit", ""),
        "classification_repository": "https://github.com/sebastienpalcoux/grothendieck-ring-classification",
        "rows": rows,
        "grothendieck_rows":positive_rows,
        "scope":scope,
    }
    release = json.loads((repo / "supplements/rank6/verification/release_summary.json").read_text())
    archive_name = status["inputs"]["rank6"]["current_bundle"]
    identity = json.loads((repo / "data/rank6_release_identity.json").read_text())
    coverage_relative = "data/frontier_research_progress.json"
    if not (repo / "supplements/rank6" / coverage_relative).is_file():
        coverage_relative = "data/frontier_summary.json"
    coverage_source = repo / "supplements/rank6" / coverage_relative
    coverage = json.loads(coverage_source.read_text())
    if hashlib.sha256(coverage_source.read_bytes()).hexdigest() != identity["research_files_sha256"][coverage_relative]:
        raise ValueError("Frozen rank-six research source differs from the release identity")
    coverage_chain = [(coverage_source, coverage)]
    october2_update = repo / "evidence/residual_20261002/rank6/research_progress.json"
    theoretical_update = repo / "evidence/rank6_theoretical_20261011/research_progress.json"
    for research_update in (october2_update, theoretical_update):
        if not research_update.is_file():
            continue
        update = json.loads(research_update.read_text())
        previous = repo / update["previous_coverage"]
        if (previous.resolve() != coverage_source.resolve() or
                hashlib.sha256(previous.read_bytes()).hexdigest() != update["previous_coverage_sha256"]):
            raise ValueError("Rank-six research update does not match its previous source")
        if update["classification_counts"] != coverage["classification_counts"]:
            raise ValueError("Research overlay cannot change categorification counts")
        coverage = update
        coverage_source = research_update
        coverage_chain.append((coverage_source, coverage))
    revision_source = repo / "evidence/rank6_theoretical_20261011/document_revision.json"
    revision = None
    if theoretical_update.is_file() != revision_source.is_file():
        raise ValueError("The theoretical research overlay and document revision must be published together")
    if revision_source.is_file():
        revision = json.loads(revision_source.read_text())
        if (revision["date"] != coverage["date"] or
                revision["research_progress"] != coverage_source.relative_to(repo).as_posix() or
                revision["research_progress_sha256"] != hashlib.sha256(coverage_source.read_bytes()).hexdigest()):
            raise ValueError("Current document revision does not match the current research overlay")
        current_documents = {path.relative_to(repo).as_posix()
                             for path in (repo / "manuscripts/rank6/papers").rglob("*")
                             if path.is_file() and path.suffix in (".tex", ".pdf")}
        if set(revision["documents"]) != current_documents:
            raise ValueError("Current document revision must inventory every rank-six paper TEX/PDF")
        for source, expected in revision["documents"].items():
            document = repo / source
            if (hashlib.sha256(document.read_bytes()).hexdigest() != expected["sha256"] or
                    document.stat().st_size != expected["bytes"]):
                raise ValueError(f"Rank-six document differs from its current revision: {source}")
    release_counts = {record["multiplicity"]: record for record in release["counts"]}
    release_bands = sorted(release_counts)
    if not release_bands or len(release_counts) != len(release["counts"]) or release_bands != list(range(1, release_bands[-1] + 1)):
        raise ValueError("Rank-six release summary must contain each analyzed multiplicity exactly once")
    rank6_status = {record["multiplicity"]: record for record in classifications if record["rank"] == 6}
    if sorted(rank6_status) != release_bands:
        raise ValueError("Rank-six site coverage differs from the release summary")
    for multiplicity, record in release_counts.items():
        published = rank6_status[multiplicity]
        if (published["rings"], published["excluded_general"], positive(published), published["unresolved_general"]) != (
            record["classes"], record["excluded"], record["unitarily_realized"] + record["spherically_realized_nonpseudounitary"], record["unresolved"]
        ):
            raise ValueError(f"Rank-six release/status mismatch at multiplicity {multiplicity}")
    if any(identity["summary"][field] != release[field] for field in ("excluded", "positive", "unresolved")):
        raise ValueError("Rank-six identity totals differ from the verified release")
    if identity["ledger_sha256"] != release["ledger_sha256"]:
        raise ValueError("Rank-six identity and release refer to different ledgers")
    if [[release_counts[m][key] for key in ("classes", "excluded", "unitarily_realized",
          "spherically_realized_nonpseudounitary", "unresolved")] for m in release_bands] != identity["counts"]:
        raise ValueError("Rank-six bands differ from the frozen release identity")
    if coverage["classification_counts"] != {
        "total": sum(record["classes"] for record in release["counts"]),
        "excluded": release["excluded"], "realized": release["positive"], "unresolved": release["unresolved"]
    }:
        raise ValueError("Rank-six research totals differ from the frozen release")
    if {case["id"] for case in coverage["cases"]} != set(release["unresolved_ids"]):
        raise ValueError("Rank-six research coverage does not match the unresolved frontier")
    data["snapshot"] = max(identity["date"], coverage["date"])
    if identity["archive"]["name"] != archive_name:
        raise ValueError("Rank-six archive identity differs from the classification source")
    if Path(archive_name).name != archive_name or not archive_name.endswith(".zip"):
        raise ValueError("Rank-six archive must be a ZIP filename")
    archive_source = repo / "site/dist/downloads" / archive_name
    if not archive_source.is_file():
        raise FileNotFoundError("Run python3 tools/restore_data.py in the classification repository first.")
    data["rank6_release"] = {
        "date": identity["date"], "excluded": release["excluded"],
        "realized": release["positive"], "unresolved": release["unresolved"],
        "analyzed_through": release_bands[-1],
        "complete_through": next(record["through"] for record in scope if record["rank"] == 6),
        "research_summary": coverage.get("research_summary", identity["research_summary"]),
        "research_cases": [{key: case[key] for key in ("id", "categorical_status", "public_summary")}
                           for case in coverage["cases"]],
        "research_coverage_path": "data/rank6_research_coverage.json",
        "research_coverage_source": coverage_source.relative_to(repo).as_posix(),
        "research_coverage_chain": [{
            "source": source.relative_to(repo).as_posix(),
            "path": f"data/rank6_research_coverage_{record['date'].replace('-', '')}.json",
            "sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "date": record["date"],
        } for source, record in coverage_chain],
        "identity_path": "data/rank6_release_identity.json",
        "complete_multiplicity_bands": [r["multiplicity"] for r in release["counts"] if r["unresolved"] == 0],
        "documents": {
            target: hashlib.sha256((repo / "manuscripts/rank6/papers" / source).read_bytes()).hexdigest()
            for source, target in (("manuscript.pdf", "rank6.pdf"), ("verification_guide.pdf", "rank6_guide.pdf"))
        },
        "archive": {"path": "downloads/" + archive_name,
                    "bytes": archive_source.stat().st_size,
                    "sha256": hashlib.sha256(archive_source.read_bytes()).hexdigest()},
        "frontier_path": "data/rank6_unresolved_tensors.json",
        "summary_path": "data/rank6_release_summary.json",
    }
    if data["rank6_release"]["archive"]["sha256"] != identity["archive"]["sha256"]:
        raise ValueError("Rank-six archive bytes differ from the verified release")
    if data["rank6_release"]["archive"]["bytes"] != identity["archive"]["bytes"]:
        raise ValueError("Rank-six archive size differs from the verified release")
    for source, target in (("manuscript.pdf", "rank6.pdf"), ("verification_guide.pdf", "rank6_guide.pdf")):
        expected = (revision["documents"]["manuscripts/rank6/papers/" + source]
                    if revision else identity["documents"][source])
        if data["rank6_release"]["documents"][target] != expected["sha256"]:
            raise ValueError(f"Rank-six document differs from its verified revision: {source}")
    downloads = HERE / "dist/downloads"
    downloads.mkdir(parents=True, exist_ok=True)
    archive_target = downloads / archive_name
    if archive_source.resolve() != archive_target.resolve():
        shutil.copy2(archive_source, archive_target)
    for obsolete in downloads.glob("Rank6_Categorification_M*.zip"):
        if obsolete.name != archive_name:
            obsolete.unlink()
    (HERE / "dist/data").mkdir(parents=True, exist_ok=True)
    for source_name, target_name in (("data/unresolved_tensors.json", "rank6_unresolved_tensors.json"),
                                     ("verification/release_summary.json", "rank6_release_summary.json")):
        shutil.copy2(repo / "supplements/rank6" / source_name, HERE / "dist/data" / target_name)
    shutil.copy2(repo / "data/rank6_release_identity.json", HERE / "dist/data/rank6_release_identity.json")
    shutil.copy2(coverage_source, HERE / "dist/data/rank6_research_coverage.json")
    for (source, _), record in zip(coverage_chain, data["rank6_release"]["research_coverage_chain"]):
        shutil.copy2(source, HERE / "dist" / record["path"])
    if revision:
        shutil.copy2(revision_source, HERE / "dist/data/rank6_document_revision.json")
        data["rank6_release"]["document_revision"] = {
            "path": "data/rank6_document_revision.json", "date": revision["date"],
            "sha256": hashlib.sha256(revision_source.read_bytes()).hexdigest(),
        }
    for name, target in (("manuscript.pdf", "rank6.pdf"), ("verification_guide.pdf", "rank6_guide.pdf")):
        shutil.copy2(repo / "manuscripts/rank6/papers" / name, HERE / "dist/papers" / target)
    addendum = repo / "evidence/residual_20261002/rank6/research_addendum.pdf"
    if october2_update.is_file():
        shutil.copy2(addendum, HERE / "dist/papers/rank6_addendum_20261002.pdf")
        data["rank6_release"]["research_addendum"] = {
            "path": "papers/rank6_addendum_20261002.pdf",
            "sha256": hashlib.sha256(addendum.read_bytes()).hexdigest(),
        }
    output = HERE / "dist" / "data" / "atlas.json"
    data["upper_rank_releases"] = {}
    bundles = {entry["name"]: entry["sha256"] for entry in status["bundles"]}
    for rank, pdf_path, archive_path in (
        (7, "manuscripts/rank7/papers/manuscript.pdf", "supplements/rank7/release/rank7-certified-through-m4.zip"),
        (8, "manuscripts/rank8/paper/rank8.pdf", "supplements/rank8/rank8-verified-supplement.zip"),
    ):
        pdf_source, archive_source = repo / pdf_path, repo / archive_path
        archive_hash = hashlib.sha256(archive_source.read_bytes()).hexdigest()
        if archive_hash != bundles[archive_source.name]:
            raise ValueError(f"Rank-{rank} archive differs from the publication ledger")
        pdf_target = HERE / "dist/papers" / f"rank{rank}.pdf"
        archive_target = downloads / archive_source.name
        shutil.copy2(pdf_source, pdf_target)
        shutil.copy2(archive_source, archive_target)
        data["upper_rank_releases"][str(rank)] = {
            "manuscript": {"path": f"papers/rank{rank}.pdf", "sha256": hashlib.sha256(pdf_source.read_bytes()).hexdigest()},
            "archive": {"path": "downloads/" + archive_source.name, "sha256": archive_hash, "bytes": archive_source.stat().st_size},
        }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n")
    status["rows"] = classifications
    status["site_filter"] = "Ranks 2–8 with complete or partial categorification analysis; unassessed census-only bands omitted."
    (output.parent / "classification_status.json").write_text(json.dumps(status,ensure_ascii=False,indent=2)+"\n")
    with (output.parent / "counts.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=("rank", "multiplicity", "rings", "source", "verification"))
        writer.writeheader()
        writer.writerows(rows)
    with (output.parent / "grothendieck_counts.csv").open("w", newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=("rank","multiplicity","rings","is_lower_bound"))
        writer.writeheader();writer.writerows(positive_rows)
    print(f"Wrote {len(rows)} count rows to {output}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the site snapshot from the exact, curated classification repository.

Run this in the site checkout with --classification PATH. The repository's
data/counts.json is the source of truth; no count is scraped from a PDF.
"""
import argparse
import csv
import json
import hashlib
import re
import shutil
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def version_app_script():
    """Keep cached JavaScript in sync with each published HTML snapshot."""
    version = hashlib.sha256((HERE / "dist/app.js").read_bytes()).hexdigest()[:12]
    path = HERE / "dist/index.html"
    html, count = re.subn(r'(<script src="\./app\.js)(?:\?v=[^"]*)?(" defer></script>)',
                          lambda match: f'{match[1]}?v={version}{match[2]}', path.read_text())
    if count != 1:
        raise ValueError("Expected one atlas application script")
    path.write_text(html)


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
    sys.path.insert(0,str(repo/'tools'))
    from frontier import active as current_frontier_active
    if current_frontier_active(repo):
        from sync_frontier import profiles,documents
        profiles();documents()
        if args.classification_commit:
            p=HERE/'dist/data/atlas.json';payload=json.loads(p.read_text());payload['classification_commit']=args.classification_commit;p.write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':'))+'\n');(repo/'data/atlas.json').write_bytes(p.read_bytes())
        from current_presentation import apply
        from version_catalogue import main as version_catalogue
        from version_assets import version_assets
        apply(HERE);version_catalogue();version_assets()
        print('Built the current source-bound frontier; frozen historical generators are not reapplied.')
        return
    sys.path.insert(0, str(repo / "tools"))
    from rank6_publication import RESEARCH_UPDATES
    from rank8_publication import extension as rank8_extension_info, archive_path as rank8_archive, ledger_path as rank8_ledger
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
            "note":("Unrestricted complex classification; every categorification is spherical. Multiplicity is at most six." if rank == 4 else "Unrestricted complex classification.")}
           if rank in (2,3,4) else scope_record(rank) for rank in scoped_ranks]
    data = {
        "snapshot": None,
        "classification_commit": args.classification_commit,
        "source_repository": counts.get("census_repository", "https://github.com/sebastienpalcoux/fusion-ring-census"),
        "census_commit": counts.get("census_commit", ""),
        "census_extensions": counts.get("census_extensions", {}),
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
    for research_update in (repo / path for path in RESEARCH_UPDATES):
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
    revision_source = repo / "data/current_document_revision.json"
    if not revision_source.is_file():
        raise FileNotFoundError("Build the current document manifest before the website snapshot")
    revision = json.loads(revision_source.read_text())
    if revision.get("schema") != "current-document-revision/v1":
        raise ValueError("Unexpected current document manifest schema")
    for source, expected in revision["documents"].items():
        document = repo / source
        if (hashlib.sha256(document.read_bytes()).hexdigest() != expected["sha256"] or
                document.stat().st_size != expected["bytes"]):
            raise ValueError("Document differs from its current manifest: " + source)
    for target, source in revision["web_copies"].items():
        if target.startswith("/") or ".." in Path(target).parts or not target.startswith("papers/"):
            raise ValueError("Invalid website manuscript path: " + target)
        if source not in revision["documents"]:
            raise ValueError("Website manuscript is missing from the document manifest: " + source)
        document = repo / source
        if not document.read_bytes().startswith(b"%PDF-"):
            raise ValueError("Website manuscript is not a PDF: " + source)
        destination = HERE / "dist" / target
        destination.parent.mkdir(parents=True, exist_ok=True)
        if document.resolve() != destination.resolve():
            shutil.copy2(document, destination)
    required_papers = {f"papers/rank{rank}.pdf" for rank in range(2, 9)}
    if not required_papers <= set(revision["web_copies"]):
        raise ValueError("Current document manifest must include every rank manuscript")
    (HERE / "dist/data").mkdir(parents=True, exist_ok=True)
    shutil.copy2(revision_source, HERE / "dist/data/current_document_revision.json")
    data["current_documents"] = {
        "path": "data/current_document_revision.json", "source": "data/current_document_revision.json",
        "date": revision["date"], "sha256": hashlib.sha256(revision_source.read_bytes()).hexdigest(),
    }
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
    data["snapshot"] = max(identity["date"], coverage["date"], revision["date"])
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
        "research_summary": coverage.get("research_summary", coverage.get("scope", "")),
        "research_cases": [{key: case[key] for key in ("id", "categorical_status", "public_summary")}
                           for case in coverage["cases"]],
        "research_coverage_path": "data/rank6_research_coverage.json",
        "research_coverage_source": coverage_source.relative_to(repo).as_posix(),
        "research_coverage_chain": [{
            "source": source.relative_to(repo).as_posix(),
            "path": (f"data/rank6_research_coverage_{record['date'].replace('-', '')}"
                     + ("_unified" if "unified_20261016" in source.parts else "_rigidity" if "rigidity_20261017" in source.parts else "") + ".json"),
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
    from reader_resources import RESOURCE_NAMES, validate_reader_resources
    reader_check = validate_reader_resources(repo)
    page_inventory = json.loads((repo / "data/manuscript_page_counts.json").read_text())
    data["reader_resources"] = {
        "files": {name: {"path": "downloads/" + name, "sha256": reader_check["resource_sha256"][name]}
                  for name in RESOURCE_NAMES},
        "page_totals": page_inventory["totals"],
    }
    for name in RESOURCE_NAMES:
        shutil.copy2(repo / "data" / name, downloads / name)
    sums = page_inventory["totals"]
    summary = (f"Eight mathematical manuscripts: {sums['mathematical_manuscript']} pages; "
               f"with the three verification guides: {sums['mathematical_manuscripts_and_guides']}; "
               f"with the research-status report: {sums['all_distinct_documents']}. "
               "Each distinct document is counted once.")
    index_path = HERE / "dist/index.html"
    html, replacements = re.subn(r'(<span id="manuscript-page-summary">).*?(</span>)',
                                 lambda match: match[1] + summary + match[2], index_path.read_text())
    if replacements != 1:
        raise ValueError("Missing unique manuscript-page summary")
    index_path.write_text(html)
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
            "source": revision_source.relative_to(repo).as_posix(),
            "sha256": hashlib.sha256(revision_source.read_bytes()).hexdigest(),
        }
    for name, target in (("manuscript.pdf", "rank6.pdf"), ("verification_guide.pdf", "rank6_guide.pdf")):
        shutil.copy2(repo / "manuscripts/rank6/papers" / name, HERE / "dist/papers" / target)
    output = HERE / "dist" / "data" / "atlas.json"
    data["upper_rank_releases"] = {}
    bundles = {entry["name"]: entry["sha256"] for entry in status["bundles"]}
    for rank, pdf_path, archive_path in (
        (7, "manuscripts/rank7/papers/manuscript.pdf", "supplements/rank7/release/rank7-certified-through-m5.zip"),
        (8, "manuscripts/rank8/paper/rank8.pdf", rank8_archive(repo)),
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
    stage_path = next(("evidence/" + name for name in
                       ("rigidity_20261017", "review_20261017", "unified_20261016", "theoretical_20261016")
                       if (repo / "evidence" / name / "decisions.json").is_file()),
                      "evidence/theoretical_20261016")
    stage_name = stage_path.split("/")[-1]
    stage = repo / stage_path
    if (stage / "decisions.json").is_file():
        decisions = json.loads((stage / "decisions.json").read_text())
        remaining = json.loads((stage / "remaining_ids.json").read_text())
        expected_totals = json.loads((stage / "expected_totals.json").read_text())
        is_review = stage_name == "review_20261017"
        is_rigidity = stage_name == "rigidity_20261017"
        is_current = is_review or is_rigidity
        stage_date = "2026-10-17" if is_current else "2026-10-16"
        proofs_source = "evidence/unified_20261016" if is_current else stage_path
        if is_review:
            if len(decisions) != 35 or any(record["id"] == "R8_2_24" for record in decisions):
                raise ValueError("The current continuation requires 35 decisions and an open R8_2_24")
            if remaining != {"6": ["R6_4_155", "R6_8_1660"], "7": [], "8": ["R8_2_24"]}:
                raise ValueError("The current record must retain exactly the three open cases")
        if is_rigidity:
            if len(decisions) != 36 or remaining != {"6": ["R6_4_155", "R6_8_1660"], "7": [], "8": []}:
                raise ValueError("The rigidity stage requires 36 decisions and exactly two open rank-six cases")
        if not decisions or len({record["id"] for record in decisions}) != len(decisions):
            raise ValueError("The theoretical update must have distinct decisions")
        if any(record["status"] not in ("excluded", "unitarily_realized") or record["scope"] != "general_complex" or record["rank"] not in (7,8) for record in decisions):
            raise ValueError("Only proved general exclusions or unitary constructions may enter the update")
        by_rank = {str(rank): sum(record["rank"] == rank for record in decisions) for rank in (7, 8)}
        for rank, ledger_path in ((7, "supplements/rank7/output/rank7_ledger.json"),
                                  (8, rank8_ledger(repo))):
            ledger = json.loads((repo / ledger_path).read_text())
            current = {record["id"]: record for record in ledger}
            for decision in (record for record in decisions if record["rank"] == rank):
                if current[decision["id"]]["status"] != decision["status"]:
                    raise ValueError("Theoretical-update decision missing from ledger: " + decision["id"])
                if not (repo / decision.get("proof_source", proofs_source) / decision["proof"]).is_file():
                    raise ValueError("Missing theoretical proof: " + decision["proof"])
            historical_ledger = [record for record in ledger if record["multiplicity"] <= (4 if rank == 7 else 2)]
            actual = {key: sum(record["status"] == key for record in historical_ledger)
                      for key in ("excluded", "unitarily_realized", "unresolved")}
            if actual != expected_totals[str(rank)]:
                raise ValueError(f"Rank-{rank} update totals differ from the current ledger")
            scope_row = next(record for record in scope if record["rank"] == rank)
            aggregate = {key: sum(record["status"] == key for record in ledger) for key in ("excluded", "unitarily_realized", "unresolved")}
            if (scope_row["positive"], scope_row["unresolved"]) != (aggregate["unitarily_realized"], aggregate["unresolved"]):
                raise ValueError(f"Refresh classification_status.json for rank {rank} before building the site")
            if remaining[str(rank)] != [record["id"] for record in historical_ledger if record["status"] == "unresolved"]:
                raise ValueError(f"Rank-{rank} remaining cases differ from the current ledger")
        if remaining["6"] != release["unresolved_ids"]:
            raise ValueError("Theoretical update changes the rank-six unresolved inventory")
        archive_name = ("review" if is_current else "unified" if stage_name.startswith("unified") else "theoretical") + "-update-" + stage_date + ".zip"
        archive_source = repo / "site/dist/downloads" / archive_name
        if not archive_source.is_file():
            raise FileNotFoundError("Missing current theoretical update archive: " + str(archive_source))
        with zipfile.ZipFile(archive_source) as bundle:
            matches = [name for name in bundle.namelist()
                       if name == "decisions.json" or name.endswith(stage_name + "/decisions.json")]
            if len(matches) != 1 or json.loads(bundle.read(matches[0])) != decisions:
                raise ValueError("Theoretical update archive contains stale or missing decision records")
            if is_current:
                for relative in set(revision["web_copies"].values()) | {"data/current_document_revision.json"}:
                    source = repo / relative
                    document = archive_source.stem + "/" + relative
                    if bundle.namelist().count(document) != 1 or bundle.read(document) != source.read_bytes():
                        raise ValueError("Proof bundle contains a stale or missing current document: " + relative)
        archive_target = downloads / archive_name
        if archive_source.resolve() != archive_target.resolve():
            shutil.copy2(archive_source, archive_target)
        local_files = {}
        for filename in ("decisions.json", "remaining_ids.json", "expected_totals.json"):
            source = stage / filename
            target = HERE / "dist/data" / (stage_name + "_" + filename)
            shutil.copy2(source, target)
            local_files[filename.removesuffix(".json")] = {
                "path": "data/" + target.name,
                "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            }
        data["theoretical_update"] = {
            "date": stage_date, "source": stage_path, "proofs_source": proofs_source,
            "new_general_exclusions": sum(d["status"] == "excluded" for d in decisions),
            "new_unitary_models": sum(d["status"] == "unitarily_realized" for d in decisions),
            "by_rank": by_rank,
            "remaining": {rank: len(ids) for rank, ids in remaining.items()},
            "decisions": decisions, "files": local_files,
            "archive": {"path": "downloads/" + archive_name,
                        "bytes": archive_source.stat().st_size,
                        "sha256": hashlib.sha256(archive_source.read_bytes()).hexdigest()},
        }
        if is_current:
            data["theoretical_update"]["original_case_count"] = 38
        data["snapshot"] = max(data["snapshot"], data["theoretical_update"]["date"])
    from rank7_publication import extension, remaining_ids
    rank7_extension = extension(repo)
    if rank7_extension:
        data["rank7_m5_update"] = rank7_extension
        data["remaining_ids"] = remaining_ids(repo)
        remaining_path = HERE / "dist/data/current_remaining_ids.json"
        remaining_path.write_text(json.dumps(data["remaining_ids"], indent=2) + "\n")
        data["remaining_ids_file"] = {"path": "data/current_remaining_ids.json", "sha256": hashlib.sha256(remaining_path.read_bytes()).hexdigest()}
        data["snapshot"] = max(data["snapshot"], rank7_extension["date"])
        extension_path = HERE / "dist/data/rank7_m5_update.json"
        extension_path.write_text(json.dumps(rank7_extension, indent=2) + "\n")
        rank7_extension["metadata_path"] = "data/rank7_m5_update.json"
        rank7_extension["metadata_sha256"] = hashlib.sha256(extension_path.read_bytes()).hexdigest()
    rank8_extension = rank8_extension_info(repo)
    if rank8_extension:
        data["rank8_m3_update"] = rank8_extension
        data["remaining_ids"] = remaining_ids(repo)
        remaining_path = HERE / "dist/data/current_remaining_ids.json"
        remaining_path.write_text(json.dumps(data["remaining_ids"], indent=2) + "\n")
        data["remaining_ids_file"] = {"path": "data/current_remaining_ids.json", "sha256": hashlib.sha256(remaining_path.read_bytes()).hexdigest()}
        data["snapshot"] = max(data["snapshot"], rank8_extension["date"])
        attempts_source = repo / rank8_extension["attempts_source"]
        attempts = json.loads(attempts_source.read_text())
        attempt_rows = attempts.get("rows", attempts.get("cases", attempts.get("records", []))) if isinstance(attempts, dict) else attempts
        if rank8_extension.get("frontier"):
            expected = set(rank8_extension["remaining_ids"])
            if {row["id"] for row in attempt_rows if row["general_status"] == "unresolved"} != expected:
                raise ValueError("Research audit status differs from accepted frontier")
            attempt_rows = [row for row in attempt_rows if row["id"] in expected]
            attempts = {**attempts, "rows": attempt_rows, "display_scope": "Current unresolved cases; complete baseline-34 research audit is retained in the proof package"}
        if [row["id"] for row in attempt_rows] != rank8_extension["remaining_ids"]:
            raise ValueError("Residual attempt inventory differs from the accepted M3 frontier")
        attempts_path = HERE / "dist/data/rank8_m3_attempts.json"
        attempts_path.write_text(json.dumps(attempts, ensure_ascii=False, separators=(",", ":")) + "\n")
        rank8_extension["attempts"] = {"path": "data/rank8_m3_attempts.json", "sha256": hashlib.sha256(attempts_path.read_bytes()).hexdigest(), "cases": len(attempt_rows)}
        extension_path = HERE / "dist/data/rank8_m3_update.json"
        extension_path.write_text(json.dumps(rank8_extension, indent=2) + "\n")
        rank8_extension["metadata_path"] = "data/rank8_m3_update.json"
        rank8_extension["metadata_sha256"] = hashlib.sha256(extension_path.read_bytes()).hexdigest()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n")
    status["rows"] = classifications
    status["site_filter"] = "Ranks 2–8 with complete or partial categorification analysis; unassessed census-only bands omitted."
    (output.parent / "classification_status.json").write_text(json.dumps(status,ensure_ascii=False,indent=2)+"\n")
    with (output.parent / "counts.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=("rank", "multiplicity", "rings", "source", "verification"),lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    with (output.parent / "grothendieck_counts.csv").open("w", newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=("rank","multiplicity","rings","is_lower_bound"),lineterminator="\n")
        writer.writeheader();writer.writerows(positive_rows)
    # Keep the repository's reader-facing aliases on the same exact snapshot.
    aliases = {"data/atlas.json", "data/rank6_research_coverage.json",
               "data/rank6_document_revision.json"}
    aliases.update(entry["path"] for entry in data["rank6_release"]["research_coverage_chain"])
    aliases.update(entry["path"] for entry in data.get("theoretical_update", {}).get("files", {}).values())
    for relative in sorted(aliases):
        source = HERE / "dist" / relative
        target = repo / relative
        if source.resolve() != target.resolve():
            shutil.copy2(source, target)
    from current_presentation import apply as consolidate_presentation
    consolidate_presentation(HERE)
    version_app_script()
    print(f"Wrote {len(rows)} count rows to {output}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Refresh current rank-ten publication views from its accepted evidence."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
RELEASE = "evidence/rank10_m1_exclusions_20261023"
sys.path.insert(0, str(ROOT / "site"))
from rank10_exclusions import apply, digest, write
from high_rank_publication import extend_document, extend_front


def info(path):
    return {"sha256": digest(path), "bytes": path.stat().st_size}


def main():
    source = ROOT / RELEASE
    ledger = json.loads((source / "accepted_ledger.json").read_text())
    if ledger["counts"]["10"] != {"excluded": 136, "unitarily_realized": 57, "unresolved": 1}:
        raise ValueError("Unexpected accepted rank-ten counts")
    paper = ROOT / "publications/rank9-rank10/paper"
    raw = (paper / "rank9-rank10.pdf").read_bytes()
    if not raw.startswith(b"%PDF-") or b"%%EOF" not in raw[-100:]:
        raise ValueError("Current manuscript PDF is incomplete")
    portable = source / "paper"
    portable.mkdir(exist_ok=True)
    for path in paper.glob("*.tex"):
        content = path.read_text().replace("../../../evidence/rank9_rank10_m1_20261023/work/", "../prior/rank9_rank10_m1_20261023/work/")
        (portable / path.name).write_text(content)
    shutil.copyfile(paper / "rank9-rank10.pdf", portable / "rank9-rank10.pdf")
    # Every shipped source has a current binding; exploratory records remain identified as such.
    included = sorted(p for p in source.rglob("*") if p.is_file() and "__pycache__" not in p.parts
                      and p.suffix not in {".pyc", ".log"} and p.name != "manifest_new_research.json")
    (source / "manifest_new_research.json").write_text(json.dumps({"format": "sha256", "files": {p.relative_to(source).as_posix(): digest(p) for p in included}}, indent=2) + "\n")
    archive = ROOT / "site/dist/downloads/Rank10_M1_Exclusions_20261023.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in included + [source / "manifest_new_research.json"]:
            entry = zipfile.ZipInfo("rank10_m1_exclusions_20261023/" + p.relative_to(source).as_posix(), (2026, 10, 23, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            z.writestr(entry, p.read_bytes())
    apply(ROOT)

    revision_path = ROOT / "data/current_publication_revision.json"
    revision = json.loads(revision_path.read_text())
    revision["remaining_ids"] = [r for r in revision["remaining_ids"] if r not in {f"R10_1_{i}" for i in (114, 115, 152, 153, 179)}]
    if "R10_1_189" not in revision["remaining_ids"]:
        revision["remaining_ids"].append("R10_1_189")
    revision["current_unresolved_total"] = len(revision["remaining_ids"])
    revision["rank9_rank10_m1"] = {"input_count": 336, "excluded": 238, "unitarily_realized": 97,
                                     "unresolved": 1, "ledger": RELEASE + "/accepted_ledger.json",
                                     **info(source / "accepted_ledger.json")}
    revision["rank10_m1_continuation"] = {"evidence": RELEASE, "excluded_ids": [f"R10_1_{i}" for i in (114, 115, 152, 153, 179)],
                                            "unresolved_ids": ["R10_1_189"], "delta": info(source / "classification_updates.json")}
    for p in paper.iterdir():
        if p.suffix in {".tex", ".pdf"}:
            revision["documents"][p.relative_to(ROOT).as_posix()] = info(p)
    revision_path.write_text(json.dumps(revision, ensure_ascii=False, indent=2) + "\n")
    shutil.copyfile(revision_path, ROOT / "site/dist/data/current_publication_revision.json")
    # The frozen lower-rank document manifest remains untouched.
    pages_path = ROOT / "data/current_manuscript_page_counts.json"
    pages = json.loads(pages_path.read_text())
    for doc in pages["documents"]:
        if doc["path"] == "publications/rank9-rank10/paper/rank9-rank10.pdf":
            count = re.search(r"^Pages:\s*(\d+)", subprocess.check_output(["pdfinfo", str(paper / "rank9-rank10.pdf")], text=True), re.M)
            doc.update(pages=int(count[1]), **info(paper / "rank9-rank10.pdf"))
    for kind in ("mathematical_manuscript", "verification_guide", "research_status_report"):
        pages["totals"][kind] = sum(d["pages"] for d in pages["documents"] if d["kind"] == kind)
    pages["totals"]["mathematical_manuscripts_and_guides"] = pages["totals"]["mathematical_manuscript"] + pages["totals"]["verification_guide"]
    pages["totals"]["all_distinct_documents"] = sum(d["pages"] for d in pages["documents"])
    pages_path.write_text(json.dumps(pages, ensure_ascii=False, indent=2) + "\n")
    rank11_path = ROOT / "site/dist/data/rank11_m1.json"
    rank11 = json.loads(rank11_path.read_text())
    rank11["summary"]["current_documents"].update(sha256=digest(revision_path))
    write(rank11_path, rank11)
    readme = ROOT / "README.md"
    readme.write_text(extend_front(readme.read_text(), ROOT))
    for name in ("VERIFY", "RESEARCH_STATUS", "PROVENANCE", "PREPUBLICATION_REVIEW", "PROJECT_GUIDE"):
        p = ROOT / f"docs/{name}.md"
        p.write_text(extend_document(p.read_text()))
    p = ROOT / "manuscripts/README.md"
    text = p.read_text().replace("131 exclusions, 57 unitary models and 6 unresolved", "136 exclusions, 57 unitary models and 1 unresolved")
    text = text.replace("594 pages", str(pages["totals"]["mathematical_manuscript"]) + " pages")
    text = text.replace("613 pages", str(pages["totals"]["mathematical_manuscripts_and_guides"]) + " pages")
    text = text.replace("621 pages", str(pages["totals"]["all_distinct_documents"]) + " pages")
    text = text.replace("| 24 |", "| 30 |")
    text = text.replace("[Ranks 9–10 proofs and replay](../evidence/rank9_rank10_m1_20261023/README.md)",
                        "[Ranks 9–10 proofs and replay](../evidence/rank10_m1_exclusions_20261023/README.md)")
    p.write_text(text)
    print("Current publication synchronized: seven unresolved project cases;", pages["totals"]["mathematical_manuscript"], "manuscript pages.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Add the rank-nine/ten multiplicity-one release without rewriting older data.

Run after build_snapshot.py, build_realized.py and build_cases.py. The package
root preserves its original relative evidence paths and is independently usable.
"""
import argparse
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil

import numpy as np
import sympy as sp
from build_realized import tensor_checks

HERE = Path(__file__).resolve().parent
REPO_URL = "https://github.com/sebastienpalcoux/grothendieck-ring-classification"
CONVENTION = "N[i][j][k] is the coefficient of X_k in X_i * X_j. Indices are zero-based; X_0 is the unit. The supplied source basis is preserved."
DEFERRED_SCOPE_AUDIT = {f"R10_1_{i}" for i in (114, 115, 152, 153, 179, 189)}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")


def build(repo, release, source=None, ref="main"):
    source = source or repo / release
    ledger_path = source / "deliverable/ledger.json"
    ledger_bytes = ledger_path.read_bytes()
    ledger_digest = hashlib.sha256(ledger_bytes).hexdigest()
    ledger = json.loads(ledger_bytes)
    tensor_bytes = (source / "work/input_audit/tensors.json").read_bytes()
    tensors = json.loads(tensor_bytes)
    input_hashes = {"deliverable/ledger.json": ledger_digest, "work/input_audit/tensors.json": hashlib.sha256(tensor_bytes).hexdigest()}
    records = ledger["records"]
    expected = {f"R{rank}_1_{i}" for rank, count in ((9, 142), (10, 194)) for i in range(1, count + 1)}
    if len(records) != 336 or {r["id"] for r in records} != expected or set(tensors) != expected:
        raise ValueError("Expected exactly the supplied 142 rank-nine and 194 rank-ten tensors")
    if any(r["status"] not in {"excluded", "unitarily_realized", "unresolved"} for r in records):
        raise ValueError("Unknown decision status")
    counts = {str(rank): dict(Counter(r["status"] for r in records if r["rank"] == rank)) for rank in (9, 10)}
    for rank in counts:
        if any(counts[rank].get(k, 0) != ledger["counts"][rank].get(k, 0) for k in set(counts[rank]) | set(ledger["counts"][rank])):
            raise ValueError("Ledger totals disagree with its individual records")
    notes_path = source / "deliverable/case_notes.json"
    if notes_path.exists():
        notes_bytes = notes_path.read_bytes()
        notes = json.loads(notes_bytes)
        input_hashes["deliverable/case_notes.json"] = hashlib.sha256(notes_bytes).hexdigest()
    else:
        notes = {}
    if not isinstance(notes, dict) or set(notes) - expected:
        raise ValueError("Case notes must map known case identifiers to notes")
    for rid, note in notes.items():
        if not isinstance(note, dict) or not isinstance(note.get("summary", ""), str) or not isinstance(note.get("research", []), list) or not isinstance(note.get("deferred", False), bool):
            raise ValueError("Malformed case notes: " + rid)
    dist = repo / "site/dist"
    folder = dist / "downloads/fusion-tensors"
    folder.mkdir(parents=True, exist_ok=True)
    legacy_paths = [dist / "data" / name for name in ("atlas.json", "classification_status.json", "realized_rings.json", "unresolved_cases.json", "resolved_cases.json")]
    legacy_hashes = {str(p.relative_to(repo)): sha(p) for p in legacy_paths if p.exists()}
    source_index = {}

    def evidence(relative):
        relative = str(relative)
        local = (source / relative).resolve()
        if not local.is_relative_to(source.resolve()) or not local.is_file():
            raise ValueError("Missing or unsafe release evidence: " + relative)
        if relative not in source_index:
            path = f"{release}/{relative}"
            digest = sha(local)
            if relative in input_hashes and digest != input_hashes[relative]:
                raise ValueError("Source changed during build; use a frozen package: " + relative)
            source_index[relative] = {"label": relative, "path": path, "url": f"{REPO_URL}/blob/{ref}/{path}", "sha256": digest}
        return source_index[relative]

    def receipt_paths(receipt):
        for key in ("proof", "certificate"):
            value = receipt.get(key)
            if not isinstance(value, str):
                continue
            path = value.split(":", 1)[0]
            if path == "report.pdf":
                path = "deliverable/report.pdf"
            if (source / path).is_file():
                yield path
            elif not value.startswith(("http://", "https://")):
                raise ValueError("Missing receipt source: " + value)
        for path in re.findall(r"(?:work|inputs|deliverable)/[\w./+-]+\.py", receipt.get("verifier", "")):
            yield path

    profiles = []
    for row in records:
        rid = row["id"]; tensor = tensors[rid]; rank = row["rank"]
        canonical = json.dumps(tensor, separators=(",", ":")).encode()
        if hashlib.sha256(canonical).hexdigest() != row["tensor_sha256_compact_json"]:
            raise ValueError("Tensor identity mismatch: " + rid)
        a, dual = tensor_checks(tensor)
        if len(a) != rank or dual != row["dual"] or int(a.max()) != 1:
            raise ValueError("Tensor rank, duality or multiplicity mismatch: " + rid)
        if bool(np.array_equal(a, a.transpose(1, 0, 2))) != row["commutative"]:
            raise ValueError("Commutativity mismatch: " + rid)
        text = json.dumps(tensor, indent=2) + "\n"
        if ast.literal_eval(text) != tensor:
            raise ValueError("Tensor literal round trip failed")
        (folder / f"{rid}.txt").write_text(text)
        omega = sum((sp.Matrix(a[i].tolist()) * sp.Matrix(a[dual[i]].tolist()) for i in range(rank)), sp.zeros(rank))
        poly = str(sp.factor(omega.charpoly(sp.Symbol("t")).as_expr()))
        inv = {"dual_indices": dual, "invertible_indices": [i for i in range(rank) if int(sum(a[i, dual[i]])) == 1],
               "commutative": row["commutative"], "frobenius_perron_dimensions_approx": row["fp_dimensions_approx"],
               "global_fp_dimension_approx": row["fp_dimension_approx"], "central_casimir_polynomial": poly,
               "dimensions_method": "Numerical Frobenius–Perron dimensions from the audited input tensor; approximate values.",
               "character_method": "Exact character calculations and certificates are retained in the linked research package."}
        if row["commutative"]:
            inv["formal_codegree_polynomial"] = poly
        note = notes.get(rid, {})
        if note.get("deferred") and row["status"] != "unresolved":
            raise ValueError("A deferred investigation must remain unresolved: " + rid)
        model = row["models"][0] if row["models"] else None
        if row["status"] == "unitarily_realized":
            if model is None or row["exclusions"]:
                raise ValueError("Inconsistent model decision: " + rid)
            summary = "A unitary categorification is identified: " + model["model"] + ". The source records specify the construction and exact tensor identification."
        elif row["status"] == "excluded":
            if not row["exclusions"] or model:
                raise ValueError("Inconsistent exclusion decision: " + rid)
            summary = "General fusion categorification over the complex numbers is excluded by the cited proof and exact certificates."
        else:
            if model or row["exclusions"]:
                raise ValueError("Unresolved entry has an accepted decision: " + rid)
            summary = "General categorification remains unresolved. No accepted construction or nonexistence proof is recorded in this release."
        if note.get("deferred"):
            summary += " Further investigation was deferred; this does not change its unresolved status."
        summary = note.get("summary", summary)
        paths = {"deliverable/ledger.json", "work/input_audit/tensors.json"}
        for default in ("README.md", "manifest.json", "verify.py", "verification_report.json", "deliverable/report.pdf", "deliverable/case_notes.json"):
            if (source / default).is_file(): paths.add(default)
        paths.update(path for receipt in row["models"] + row["exclusions"] for path in receipt_paths(receipt))
        for path in note.get("evidence", []): paths.add(path)
        audited_deferred = rid in DEFERRED_SCOPE_AUDIT and note.get("deferred")
        if audited_deferred:
            paths.update(("work/audit_signed/AUDIT.md", "work/audit_signed/replay.py", "work/general_signed/THEORY.md", "work/general_signed/verify_characters.py", "work/general_signed/original_characters.json", f"work/resolve_rank10_quadratic/{rid}_reciprocal.json"))
        evidence_rows = [evidence(path) for path in sorted(paths)]
        ledger_source = evidence("deliverable/ledger.json")
        reports = [{"title": "Current accepted case decision", "source": ledger_source["path"], "url": ledger_source["url"], "source_sha256": ledger_source["sha256"], "data": row}]
        paragraphs = [item for item in note.get("research", []) if isinstance(item, str)]
        if paragraphs:
            src = evidence("deliverable/case_notes.json")
            reports.append({"title": "Completed research and remaining scope", "source": src["path"], "url": src["url"], "source_sha256": src["sha256"], "data": {"findings": paragraphs}})
        for item in note.get("research", []):
            if isinstance(item, str): continue
            src = evidence(item["source"])
            reports.append({"title": item["title"], "source": src["path"], "url": src["url"], "source_sha256": src["sha256"], "data": item.get("data", {})})
        scope = note.get("categorification_scope")
        if scope is None and audited_deferred:
            def source_link(path, label):
                src = evidence(path)
                return {"path": src["path"], "url": src["url"], "sha256": src["sha256"], "label": label}
            signed_sources = [source_link("work/audit_signed/AUDIT.md", "Independent sphericalization audit"), source_link("work/audit_signed/replay.py", "Exact signed audit replay")]
            dimension_sources = [source_link("work/general_signed/THEORY.md", "Dimension-character and Galois reduction"), source_link("work/general_signed/verify_characters.py", "Exact dimension-character verifier"), source_link("work/general_signed/original_characters.json", "Complete character audit receipts")]
            scope = {"general_status": "unresolved", "level_status": {key: "unresolved" for key in ("general", "pivotal", "spherical", "pseudo_unitary", "unitary")}, "strongest_excluded": None,
                     "same_category_implications": [{"from": "general", "to": "spherical", "label": "Every hypothetical categorification admits a spherical structure", "explanation": "The exact signed-sphericalization audit supplies a spherical structure on the same hypothetical category.", "sources": signed_sources}],
                     "existence_implications": [{"from": "spherical", "to": "pseudo_unitary", "mechanism": "Galois conjugation and a tensor-sign change of spherical structure", "explanation": "The complete dimension-character audit gives a pseudo-unitary Galois conjugate of any hypothetical spherical categorification. It does not assert that the original category is pseudo-unitary.", "sources": dimension_sources}],
                     "notes": ["Existence remains unresolved. Further investigation of this case is deferred."], "audit_sources": signed_sources + dimension_sources}
        if scope is None and row["status"] != "unresolved":
            level = "excluded" if row["status"] == "excluded" else "realized"
            scope = {"general_status": level, "level_status": {key: level for key in ("general", "pivotal", "spherical", "pseudo_unitary", "unitary")},
                     "strongest_excluded": "general" if level == "excluded" else None,
                     "same_category_implications": [], "existence_implications": [], "notes": [summary],
                     "audit_sources": [{"label": "Accepted case proof and certificate record", "path": ledger_source["path"], "url": ledger_source["url"], "sha256": ledger_source["sha256"]}]}
            if level == "excluded":
                scope["braided"] = {"status": "excluded", "explanation": "The general nonexistence result also excludes a braided categorification.", "sources": scope["audit_sources"]}
        profiles.append({"id": rid, "rank": rank, "multiplicity": 1, "status": row["status"], "summary": summary,
                         "name": model["model"] if model else rid, "existence": "unitary" if model else row["status"],
                         "model_reference": model.get("scope", "") if model else "", "model_reference_url": ledger_source["url"],
                         "source_file": ledger_source["path"], "source_url": ledger_source["url"], "source_location": rid,
                         "report_url": "./papers/rank9-rank10-m1.pdf", "case_url": f"./case.html?id={rid}",
                         "fusion_tensor": tensor, "tensor_sha256": row["tensor_sha256_compact_json"],
                         "basis": [f"X{i}" for i in range(rank)], "unit_index": 0, "tensor_convention": CONVENTION,
                         "hash_convention": "SHA-256 of UTF-8 compact JSON, without a trailing newline.",
                         "invariants": inv, "research": reports, "evidence": evidence_rows, "categorification_scope": scope,
                         "download_url": f"./downloads/fusion-tensors/{rid}.txt", "investigation_deferred": bool(note.get("deferred"))})
    profiles.sort(key=lambda r: (r["rank"], int(r["id"].rsplit("_", 1)[1])))
    totals = dict(Counter(r["status"] for r in records))
    summary = {"date": "2026-10-23", "release": str(release), "counts": counts, "totals": totals, "input_count": 336,
               "ledger_sha256": ledger_digest, "ledger_url": f"{REPO_URL}/blob/{ref}/{release}/deliverable/ledger.json",
               "source_url": f"{REPO_URL}/tree/{ref}/{release}", "report_url": "./papers/rank9-rank10-m1.pdf",
               "remaining_ids": [r["id"] for r in records if r["status"] == "unresolved"]}
    archive = dist / "downloads/Rank9_Rank10_Multiplicity1_2026-10-23.zip"
    if archive.is_file():
        summary["archive"] = {"url": "./downloads/" + archive.name, "sha256": sha(archive), "bytes": archive.stat().st_size}
    for relative, item in source_index.items():
        if sha(source / relative) != item["sha256"]:
            raise ValueError("Source changed during build; use a frozen package: " + relative)
    if sha(ledger_path) != ledger_digest:
        raise ValueError("Ledger changed during build; use a frozen package")
    write_json(dist / "data/rank9_rank10_m1.json", {"schema": "ring-atlas/rank9-rank10-m1/v1", "summary": summary, "cases": profiles})
    report = source / "deliverable/report.pdf"
    if report.is_file():
        (dist / "papers").mkdir(exist_ok=True)
        shutil.copyfile(report, dist / "papers/rank9-rank10-m1.pdf")
    for path, digest in legacy_hashes.items():
        if sha(repo / path) != digest:
            raise ValueError("Legacy publication record was modified: " + path)
    write_json(dist / "data/rank9_rank10_m1_build.json", {"records": len(profiles), "counts": counts, "legacy_sha256": legacy_hashes, "source": str(release), "ledger_sha256": ledger_digest, "tensor_downloads": 336})
    readme = repo / "README.md"
    if readme.is_file():
        text = readme.read_text()
        # These rows use rank in the first column, unlike later multiplicity tables.
        text = re.sub(r"^\| (?:9|10) \| Multiplicity 1 \|.*\n", "", text, flags=re.M)
        table_rows = []
        for rank in (9, 10):
            c = counts[str(rank)]
            unresolved = f"[{c['unresolved']} unresolved](https://sebastienpalcoux.github.io/grothendieck-ring-classification/records.html?rank={rank}&status=unresolved)" if c.get("unresolved") else "0 unresolved"
            table_rows.append(f"| {rank} | Multiplicity 1 | **{'Partial' if c.get('unresolved') else 'Complete'} at multiplicity 1** | {c.get('excluded', 0)} excluded, {c.get('unitarily_realized', 0)} realized, {unresolved}. |")
        text, found = re.subn(r"(^\| 8 \|[^\n]*\n)", lambda match: match[1] + "\n".join(table_rows) + "\n", text, count=1, flags=re.M)
        if found != 1: raise ValueError("Could not locate the current README classification table")
        historical_open = len(json.loads((dist / "data/unresolved_cases.json").read_text())["cases"])
        text = re.sub(r"\*\*\d+ open cases\.\*\*", f"**{historical_open + totals.get('unresolved', 0)} open cases.**", text, count=1)
        start, end = "<!-- rank9-rank10-release -->", "<!-- /rank9-rank10-release -->"
        block = (start + "\n\n**23 October: ranks nine and ten, multiplicity one.** "
                 + f"{totals.get('excluded', 0)} general exclusions, {totals.get('unitarily_realized', 0)} unitary models and [{totals.get('unresolved', 0)} unresolved rings](https://sebastienpalcoux.github.io/grothendieck-ring-classification/records.html?status=unresolved) among all 336 supplied tensors. "
                 + f"[Browse every case](https://sebastienpalcoux.github.io/grothendieck-ring-classification/records.html) · [Report]({release}/deliverable/report.pdf) · [Proofs and verification]({release}/README.md).\n\n" + end)
        if start in text:
            text = re.sub(re.escape(start) + r".*?" + re.escape(end), lambda _: block, text, flags=re.S)
        else:
            text = text.replace('<a id="classification--what-is-decided"></a>', block + '\n\n<a id="classification--what-is-decided"></a>')
        # Extend the detailed current matrix after the preserved legacy builder.
        matrix = re.search(r"\| Multiplicity \| Rank 2[^\n]*\n(?:\|[^\n]*\n)+", text)
        if matrix:
            lines = []
            for index, line in enumerate(matrix[0].rstrip().splitlines()):
                cells = [cell.strip() for cell in line.strip().strip('|').split('|')][:8]
                if index == 0:
                    cells += ['Rank 9', 'Rank 10']
                elif index == 1:
                    cells += ['---:', '---:']
                elif cells[0] == '1':
                    cells += [('≥' if counts[str(rank)].get('unresolved') else '') + str(counts[str(rank)].get('unitarily_realized', 0)) for rank in (9, 10)]
                else:
                    cells += ['—', '—']
                lines.append('| ' + ' | '.join(cells) + ' |')
            text = text[:matrix.start()] + '\n'.join(lines) + '\n' + text[matrix.end():]
        text = text.replace('[Full count data](data/grothendieck_counts.csv)', '[Ranks 2–8 count data](data/grothendieck_counts.csv) · [Ranks 9–10 ledger](' + release + '/deliverable/ledger.csv)', 1)
        readme.write_text(text)
    for html in dist.glob("*.html"):
        text = html.read_text()
        for asset in ("app.js", "cases.js", "catalogue.js", "redirect.js", "styles.css", "cases.css"):
            digest = sha(dist / asset)[:12]
            text = re.sub(r'(\b(?:src|href)="\./' + re.escape(asset) + r')(?:\?v=[^\"]*)?(\")', lambda match: match[1] + "?v=" + digest + match[2], text)
        if text != html.read_text(): html.write_text(text)
    print(f"Published {len(profiles)} additive rank-nine/ten profiles and tensor downloads; preserved {len(legacy_hashes)} legacy data files.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--classification", type=Path, default=HERE.parent)
    parser.add_argument("--release", default="evidence/rank9_rank10_m1_20261023")
    parser.add_argument("--source", type=Path, help="Local staging package; links still use --release")
    parser.add_argument("--ref", default="main", help="GitHub source ref; preferably the immutable release commit")
    args = parser.parse_args()
    build(args.classification.resolve(), args.release, args.source.resolve() if args.source else None, args.ref)
    if (args.classification / "evidence/rank10_m1_exclusions_20261023/accepted_ledger.json").is_file():
        import subprocess, sys
        subprocess.run([sys.executable, str(args.classification.resolve() / "tools/sync_rank10_m1_publication.py")], check=True)

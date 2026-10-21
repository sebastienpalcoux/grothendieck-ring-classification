#!/usr/bin/env python3
"""Build unresolved case dossiers and literal Python tensor downloads.

The dossiers aggregate the existing published research, retaining the scope of
all tests. Algebraic ring invariants are recomputed from the exact source tensor;
no search result is promoted to a categorical construction or exclusion.
"""
import argparse
import ast
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
import runpy

import sympy as sp

from build_realized import invariants, sha_tensor

HERE = Path(__file__).resolve().parent
GITHUB = "https://github.com/sebastienpalcoux/grothendieck-ring-classification"
CONVENTION = "N[i][j][k] is the coefficient of X_k in X_i * X_j. Indices are zero-based; X_0 is the unit. The supplied source basis is preserved."
HASH_CONVENTION = "SHA-256 of UTF-8 JSON with separators=(',', ':') and no trailing newline. The formatted .txt file has the same tensor, not the same byte hash."
NUMERIC_ENCODING_NOTE = "Exact integers outside the JavaScript safe-integer range (absolute value greater than 9007199254740991) are encoded as decimal strings to preserve every digit in browser display and JSON downloads. Fusion-tensor coefficients remain integers."
NEXT = "evidence/rank8_next_20261021"
POST = "evidence/rank8_postpublication_20261021/r1154_galois_review"
RESEARCH = "evidence/rank8_research_20261022"

SUMMARIES = {
    "R8_3_65": "General complex categorification is excluded. The new pointed-induction Fourier criterion gives six exact separators covering all four pointed C4 associator classes; the two-dimension Galois reduction makes the exclusion general. This case left the unresolved inventory on 22 October 2026.",
    "R8_3_928": "The recorded Galois pseudo-unitary reduction and central-semion constraints leave ten allocations. All ten have exact charged fourth-moment and pair-product completions. These necessary data do not construct a center or category.",
    "R8_3_941": "The recorded Galois pseudo-unitary reduction and central-fermion constraints leave fourteen allocations. All fourteen admit the exact pair-product sector completion; full center and associator coherence remain unresolved.",
    "R8_3_982": "Every general categorification is spherical and has a pseudo-unitary Galois conjugate. The forced semionic branch restricts every indecomposable module category to rank eight and three necessary based-module types. The 31 algebra-object candidates reduce to eight; every nonregular Morita route requires an algebra on 1+X5. No such algebra or categorification is constructed.",
    "R8_3_1154": "Three necessary center patterns and 25 pair histograms remain. All pass the new simultaneous Galois covariance constraints. The final center dimensions rule out Morita equivalence with R8_3_1795. A nontrivial pointed C2 associator is forced; general categorification remains unresolved.",
    "R8_3_1768": "A complete signed-sphericalization analysis proves that every categorification admits a spherical structure and has a pseudo-unitary Galois conjugate. The d-number obstruction now excludes every braiding, and the tensor-image criterion excludes every braided Morita representative. The pointed C2 associator must be nontrivial, so the subgroup algebra 1+g is impossible. General unbraided categorification remains unresolved.",
    "R8_3_1795": "General complex categorification is excluded. The C2 Fourier-packing criterion gives exact separators for all sixteen indicator branches, covering both pointed associators. The signed-sphericalization and Galois reduction makes the exclusion general. This case left the unresolved inventory on 22 October 2026.",
    "R8_3_3472": "Positive second-indicator normalization in sphericalization leaves only the original signed tensor. Every general categorification is therefore spherical and has a pseudo-unitary Galois conjugate. All braided Morita representatives are excluded. General unbraided categorification remains unresolved.",
}


def exact_json_integers(value):
    """Preserve arbitrary-precision research integers through browser JSON.parse."""
    if type(value) is int and abs(value) > 9007199254740991:
        return str(value)
    if isinstance(value, list):
        return [exact_json_integers(item) for item in value]
    if isinstance(value, dict):
        return {key: exact_json_integers(item) for key, item in value.items()}
    return value


def read_json(repo, path):
    return json.loads((repo / path).read_text())


def source_url(path, is_dir=False):
    return f"{GITHUB}/{'tree' if is_dir else 'blob'}/main/{path}"


@lru_cache(maxsize=None)
def packaged_sources(repo):
    manifest = repo / "data/large_files_manifest.json"
    if not manifest.exists():
        return {}
    return {entry["path"]: entry for entry in json.loads(manifest.read_text())["files"]}


def source_location(repo, path, is_dir=False):
    """Link restored sources to their checked-in payload, preserving provenance."""
    package = packaged_sources(repo).get(path)
    if package is None:
        return {"url": source_url(path, is_dir)}
    parts = package["parts"]
    directories = {str(Path(part["path"]).parent) for part in parts}
    if len(directories) != 1 or any(not (repo / part["path"]).is_file() for part in parts):
        raise ValueError(f"Missing or inconsistent packaged source: {path}")
    if digest(repo / path) != package["sha256"]:
        raise ValueError(f"Packaged source hash differs from restored file: {path}")
    payload_directory = directories.pop()
    return {
        "url": source_url(payload_directory, is_dir=True),
        "packaged": True,
        "payload_directory": payload_directory,
        "restoration_note": "This source is stored in packaged payloads. After cloning the repository, run python3 tools/restore_data.py to restore the original path and verify its SHA-256.",
        "restoration_command": "python3 tools/restore_data.py",
        "restoration_url": source_url("tools/restore_data.py"),
        "manifest_url": source_url("data/large_files_manifest.json"),
    }


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def select_record(payload, ring_id):
    """Select an explicitly labelled source record without guessing by numbers."""
    if isinstance(payload, dict):
        if ring_id in payload:
            return payload[ring_id]
        if payload.get("id") == ring_id:
            return payload
        for name in ("records", "rows", "cases"):
            if isinstance(payload.get(name), list):
                matches = [v for v in payload[name] if isinstance(v, dict) and v.get("id") == ring_id]
                if len(matches) == 1:
                    return {**{k: v for k, v in payload.items() if k not in (name, "source_sha256")}, "record": matches[0]}
    raise ValueError(f"No unique labelled record for {ring_id}")


def research_record(repo, title, path, data=None):
    return {"title": title, "source": path, **source_location(repo, path),
            "source_sha256": digest(repo / path),
            "data": read_json(repo, path) if data is None else data}


def collect_source_paths(repo, value, found):
    """Collect explicit repository paths, leaving prose and external URLs intact."""
    if isinstance(value, dict):
        for k, v in value.items():
            collect_source_paths(repo, k, found)
            collect_source_paths(repo, v, found)
    elif isinstance(value, list):
        for v in value:
            collect_source_paths(repo, v, found)
    elif isinstance(value, str) and value.startswith(("evidence/", "manuscripts/", "supplements/", "data/", "verification/", "site/", "tools/")):
        if "\n" not in value and len(value) < 350 and (repo / value).exists():
            found.add(value)


def largest_root_description(expression, symbol):
    """Exact minimal polynomial and rational interval for the largest real root."""
    roots = []
    for factor, _ in sp.factor_list(expression, symbol)[1]:
        for (lower, upper), _ in sp.Poly(factor, symbol).intervals(eps=sp.Rational(1, 10**12)):
            roots.append((lower, upper, factor))
    if not roots:
        raise ValueError("A nonnegative fusion matrix must have a real Perron root")
    roots.sort(key=lambda item: item[0])
    lower, upper, factor = roots[-1]
    if len(roots) > 1 and roots[-2][1] >= lower:
        raise ValueError("Perron root isolating intervals overlap")
    return {"minimal_polynomial": str(factor), "largest_real_root_interval": [str(lower), str(upper)]}


def additional_invariants(tensor, inv):
    n = len(tensor)
    dual = inv["dual_indices"]
    t = sp.Symbol("t")
    matrices = [sp.Matrix(a) for a in tensor]
    polynomials = [matrix.charpoly(t).as_expr() for matrix in matrices]
    exact_dimensions = [largest_root_description(p, t) for p in polynomials]
    for description, approx in zip(exact_dimensions, inv["frobenius_perron_dimensions_approx"]):
        lo, hi = map(sp.Rational, description["largest_real_root_interval"])
        if not float(lo) - 1e-7 <= approx <= float(hi) + 1e-7:
            raise ValueError("Exact and numerical dimension records disagree")
    support = [[{k for k, v in enumerate(tensor[i][j]) if v} for j in range(n)] for i in range(n)]

    def closure(indices):
        result = {0, *indices}
        while True:
            enlarged = result | {dual[i] for i in result}
            for i in result:
                for j in result:
                    enlarged.update(support[i][j])
            if enlarged == result:
                return sorted(result)
            result = enlarged

    subrings = []
    for mask in range(1 << (n - 1)):
        indices = [0] + [i for i in range(1, n) if mask & (1 << (i - 1))]
        if closure(indices) == indices:
            subrings.append(indices)
    subrings.sort(key=lambda v: (len(v), v))
    adjoint = closure({k for i in range(n) for k in support[i][dual[i]]})
    invertibles = inv["invertible_indices"]
    product = [[next(iter(support[i][j])) for j in invertibles] for i in invertibles]
    if any(len(support[i][j]) != 1 or sum(tensor[i][j]) != 1 for i in invertibles for j in invertibles):
        raise ValueError("Malformed invertible multiplication")
    return {
        "frobenius_perron_dimensions_exact": exact_dimensions,
        "global_fp_dimension_exact": largest_root_description(sp.sympify(inv["central_casimir_polynomial"]), t),
        "exact_dimension_method": "Each FP dimension is the largest real root of its displayed irreducible polynomial, isolated by the rational interval. Factors and intervals are computed exactly from the integral fusion-matrix characteristic polynomial. The global dimension uses the central Casimir matrix.",
        "fusion_matrix_convention": "N_i[j][k] = N[i][j][k]; rows are the right input basis index, columns are the output basis index.",
        "fusion_matrix_characteristic_polynomials": [str(sp.factor(p)) for p in polynomials],
        "fusion_matrix_traces": [int(m.trace()) for m in matrices],
        "fusion_matrix_determinants": [int(m.det()) for m in matrices],
        "all_closed_based_subrings": subrings,
        "closed_based_subrings_method": "Exhaustive subsets containing the unit, closed under duality and every nonzero fusion-product coefficient. Includes the unit subring and the whole ring.",
        "adjoint_subring_indices": adjoint,
        "invertible_multiplication_table": product,
        "invertible_table_labels": invertibles,
        "self_dual_indices": [i for i in range(n) if dual[i] == i],
    }


def rank6_research(repo, ring_id):
    research = []
    path = "evidence/rigidity_20261017/rank6/research_progress.json"
    seen = set()
    while path:
        if path in seen:
            raise ValueError("Cycle in the rank-six research history")
        seen.add(path)
        payload = read_json(repo, path)
        row = next(c for c in payload["cases"] if c["id"] == ring_id)
        research.append(research_record(repo, f"Rank-six research update · {payload.get('date', 'earlier stage')}", path,
                                        {"date": payload.get("date"), "scope": payload.get("scope"), **row}))
        path = payload.get("previous_coverage")
    if ring_id == "R6_8_1660":
        for name, title in [("all_indicators.json", "All indicator sequences"), ("phase_masses.json", "Central phase masses"), ("continuation_audit_phase640.json", "Phase-profile continuation audit")]:
            research.append(research_record(repo, title, f"evidence/rigidity_20261017/rank6/r1660/{name}"))
    return research


def rank8_research(repo, ring_id, audit):
    # Newest stage first, with older source fields retained and explicitly labelled.
    research = [research_record(repo, "Published per-ring research audit (including latest completed work)",
                                f"{RESEARCH}/per_ring_research_audit.json", audit)]
    specs = []
    if ring_id == "R8_3_65":
        specs.append(("General exclusion: all pointed associator classes", f"{RESEARCH}/r65/verification.json", False))
    if ring_id in ("R8_3_982", "R8_3_1768", "R8_3_1795", "R8_3_3472"):
        gates = read_json(repo, f"{RESEARCH}/pivotality/general_spherical_gates.json")
        research.insert(0, research_record(repo, "General sphericality and pseudo-unitary Galois reduction", f"{RESEARCH}/pivotality/general_spherical_gates.json", next(r for r in gates if r['id']==ring_id)))
    morita = read_json(repo, f"{RESEARCH}/braided_morita/verification.json")
    research.insert(0, research_record(repo, "Uniform obstruction to braided Morita representatives", f"{RESEARCH}/braided_morita/verification.json", next(r for r in morita if r['id']==ring_id)))
    if ring_id in ("R8_3_1154", "R8_3_1795"):
        specs.append(("R1154 and R1795 cannot be Morita equivalent", f"{RESEARCH}/r1154_r1795/morita_obstruction.json", False))
    if ring_id == "R8_3_982":
        specs.append(("Complete module-rank and based-module restrictions", f"{RESEARCH}/r982/module_types.json", False))
    if ring_id in ("R8_3_1768", "R8_3_1795"):
        specs.append(("Complete C2 Fourier-packing branch audit", f"{RESEARCH}/pointed_followup/verification_{ring_id}.json", False))
    if ring_id == "R8_3_1795":
        specs.append(("Completed intermediate subgroup-algebra Morita analysis", f"{RESEARCH}/pointed_followup/r1795_morita/covers.json", False))
    if ring_id == "R8_3_1768":
        specs.append(("Free pointed action and partial module-factor refinement", f"{RESEARCH}/pointed_followup/r1768_modules/verification.json", False))
    if ring_id != "R8_3_65":
        block = read_json(repo, f"{RESEARCH}/pointed_followup/dimension_block/verification.json")
        research.append(research_record(repo, "Dimension-block bounds and twist-one restrictions", f"{RESEARCH}/pointed_followup/dimension_block/verification.json", next(row for row in block['records'] if row['id']==ring_id)))
    if ring_id in ("R8_3_65", "R8_3_1768", "R8_3_1795", "R8_3_3472"):
        specs += [("Connected-algebra and Morita profile closure", f"{NEXT}/quadratic/profile_closure.json", True),
                  ("Complete forced based-module actions", f"{NEXT}/quadratic/action_classes.json", True)]
        if ring_id != "R8_3_65":
            specs.append(("Trace and character closure", f"{NEXT}/quadratic/trace_closure.json", True))
        else:
            specs.append(("Pointed associator and subgroup Morita constraints", f"{NEXT}/quadratic/pointed_dual.json", False))
    if ring_id in ("R8_3_928", "R8_3_941"):
        specs += [("Exact pair-completion verification", f"{NEXT}/semion_fermion/verification.json", True),
                  ("Exact integer pair-product completions", f"{NEXT}/semion_fermion/integer_pair_completion.json", True)]
    if ring_id == "R8_3_982":
        specs.append(("Latest exact frame, indicator and phase results", f"{NEXT}/r982/FINAL_SUMMARY.json", False))
    if ring_id == "R8_3_1154":
        specs += [("Latest Galois refinement: 25 surviving pair histograms", f"{POST}/verification.json", False),
                  ("Complete 36-histogram Galois transport review", f"{POST}/review.json", False)]
    for title, path, selected in specs:
        payload = read_json(repo, path)
        research.append(research_record(repo, title, path, select_record(payload, ring_id) if selected else payload))
    return research


def validate_tensor(tensor, rank, expected_sha):
    if type(tensor) is not list or len(tensor) != rank:
        raise ValueError("Tensor rank mismatch")
    if any(type(matrix) is not list or len(matrix) != rank for matrix in tensor):
        raise ValueError("Tensor matrix shape mismatch")
    if any(type(row) is not list or len(row) != rank or any(type(x) is not int or x < 0 for x in row)
           for matrix in tensor for row in matrix):
        raise ValueError("Tensor must be a list of lists of lists of nonnegative integers")
    if sha_tensor(tensor) != expected_sha:
        raise ValueError("Tensor SHA-256 mismatch")


def write_literal(folder, ring_id, tensor, rank, expected_sha):
    if not re.fullmatch(r"(?:R\d+_\d+_\d+|F_\{\d+,\d+\})", ring_id):
        raise ValueError("Unsafe case identifier")
    validate_tensor(tensor, rank, expected_sha)
    # JSON containing only integer arrays is also a plain Python list literal.
    target = folder / f"{ring_id}.txt"
    target.write_text(json.dumps(tensor, indent=2) + "\n")
    if ast.literal_eval(target.read_text()) != tensor:
        raise ValueError("Python literal round trip failed")
    return f"./downloads/fusion-tensors/{ring_id}.txt"


def build(repo):
    packaged_sources.cache_clear()
    dist = repo / "site/dist"
    folder = dist / "downloads/fusion-tensors"
    folder.mkdir(parents=True, exist_ok=True)
    remaining = runpy.run_path(str(repo / "data/remaining_cases.py"))
    scope_payload = read_json(repo, "site/categorification_scope.json")
    scopes = scope_payload["cases"]
    if set(scopes) != set(remaining["TENSORS"]):
        raise ValueError("Categorification-scope audit differs from current remaining cases")
    realized = read_json(repo, "site/dist/data/realized_rings.json")["records"]
    closed_scopes = scope_payload.get("closed_cases", {})
    census = {r['id']: r for r in read_json(repo, 'evidence/rank8_m3_20261021/pipeline/census_m3.json')}
    closed = {rid: census[rid]['tensor'] for rid in closed_scopes}
    all_ids = [r["id"] for r in realized] + list(remaining["TENSORS"]) + list(closed)
    if len(set(all_ids)) != len(all_ids):
        raise ValueError("Duplicate realized/unresolved case identifiers")
    for record in realized:
        write_literal(folder, record["id"], record["fusion_tensor"], record["rank"], record["tensor_sha256"])
    audit_rows = {r["id"]: r for r in read_json(repo, f"{RESEARCH}/per_ring_research_audit.json")["rows"]}
    rank6_rows = {r["id"]: r for r in read_json(repo, "site/dist/data/rank6_unresolved_tensors.json")}
    cases = []
    for ring_id, tensor in {**remaining["TENSORS"], **closed}.items():
        is_closed = ring_id in closed
        metadata = remaining["METADATA"].get(ring_id)
        if is_closed:
            source = 'evidence/rank8_m3_20261021/pipeline/census_m3.json'
            metadata = {k:v for k,v in census[ring_id].items() if k!='tensor'}
            metadata.update(source=source, source_sha256=digest(repo/source))
        rank = metadata["rank"]
        if digest(repo / metadata["source"]) != metadata["source_sha256"]:
            raise ValueError(f"Source file hash mismatch: {ring_id}")
        download = write_literal(folder, ring_id, tensor, rank, metadata["tensor_sha256"])
        if max(x for matrix in tensor for row in matrix for x in row) != metadata["multiplicity"]:
            raise ValueError(f"Multiplicity mismatch: {ring_id}")
        inv = invariants(tensor)
        if not is_closed and inv["dual_indices"] != remaining["DUALS"][ring_id]:
            raise ValueError(f"Duality mismatch: {ring_id}")
        inv.update(additional_invariants(tensor, inv))
        research = rank6_research(repo, ring_id) if rank == 6 else rank8_research(repo, ring_id, audit_rows[ring_id])
        evidence_paths = {"data/remaining_cases.py", metadata["source"], "site/categorification_scope.json"}
        collect_source_paths(repo, research, evidence_paths)
        scope = closed_scopes[ring_id] if is_closed else scopes[ring_id]
        collect_source_paths(repo, scope, evidence_paths)
        if rank == 6:
            evidence_paths.add("supplements/rank6/verification/classification/attempts.jsonl")
            summary = research[0]["data"]["public_summary"]
        else:
            evidence_paths.add(f"{NEXT}/README.md")
            summary = SUMMARIES[ring_id]
        if ring_id == "R8_3_1154":
            evidence_paths.update(f"{POST}/{name}" for name in ("README.md", "PROOF.md", "INDEPENDENT_REVIEW.md", "galois_pair_probe.json"))
        evidence = []
        for path in sorted(evidence_paths):
            local = repo / path
            if not local.exists():
                raise ValueError(f"Missing evidence: {path}")
            evidence.append({"label": path, "path": path, **source_location(repo, path, local.is_dir()),
                             **({"sha256": digest(local)} if local.is_file() else {})})
        cases.append({
            "id": ring_id, "rank": rank, "multiplicity": metadata["multiplicity"],
            "status": "excluded" if is_closed else "unresolved", "summary": summary,
            "categorification_scope": scope,
            "existence": {"general":"excluded", "unitary":"excluded"} if is_closed else rank6_rows[ring_id]["existence"] if rank == 6 else {"general": "unknown", "unitary": "unknown"},
            "fusion_tensor": tensor, "tensor_sha256": metadata["tensor_sha256"],
            "basis": [f"X{i}" for i in range(rank)], "unit_index": 0,
            "source": metadata, "tensor_convention": CONVENTION,
            "hash_convention": HASH_CONVENTION,
            "numeric_encoding_note": NUMERIC_ENCODING_NOTE,
            "invariants": inv, "research": research, "evidence": evidence,
            "download_url": download,
        })
        print(f"Built {ring_id}: {len(research)} research records, {len(evidence)} source links", flush=True)
    current = read_json(repo, "site/dist/data/current_remaining_ids.json")
    # This file is an explicit current inventory rather than a historical ledger.
    ids = current if isinstance(current, list) else current.get("ids", current.get("remaining_ids", current.get("current_remaining_ids")))
    if ids is None:
        raise ValueError("Unrecognized current remaining-ID schema")
    closed_records = [r for r in cases if r['status']=='excluded']
    cases = [r for r in cases if r['status']=='unresolved']
    if sorted(ids) != sorted(r["id"] for r in cases):
        raise ValueError("Dossier inventory differs from current remaining cases")
    payload = {"schema_version": "ring-atlas/unresolved-cases/v1", "tensor_convention": CONVENTION,
               "hash_convention": HASH_CONVENTION,
               "numeric_encoding_note": NUMERIC_ENCODING_NOTE,
               "scope": "Current unresolved cases and their recorded data. Necessary conditions, finite search outcomes and scoped construction exclusions do not prove categorifiability or novelty.",
               "source_basis_note": "Research records retain the basis conventions of their source files; the displayed fusion tensor and derived invariants use the exact zero-based source basis identified in each case's metadata.",
               "cases": cases}
    (dist / "data/unresolved_cases.json").write_text(json.dumps(exact_json_integers(payload), indent=2, ensure_ascii=False) + "\n")
    (dist / "data/resolved_cases.json").write_text(json.dumps(exact_json_integers({"schema_version":"ring-atlas/resolved-cases/v1", "scope":"Formerly unresolved case pages retained with their accepted exclusion and fusion data.", "cases":closed_records}), indent=2, ensure_ascii=False)+"\n")
    for old in folder.glob("*.txt"):
        if old.stem not in all_ids:
            old.unlink()
    print(f"Published {len(cases)} unresolved dossiers, {len(closed_records)} resolved dossiers and {len(all_ids)} checked Python tensor literals.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--classification", type=Path, default=HERE.parent)
    args = parser.parse_args()
    build(args.classification.resolve())


if __name__ == "__main__":
    main()

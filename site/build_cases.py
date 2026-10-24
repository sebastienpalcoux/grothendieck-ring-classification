#!/usr/bin/env python3
"""Build current and retained case dossiers and literal Python tensor downloads.

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
CREATIVE = "evidence/rank8_creative_20261022"
FOCUS = "evidence/r3472_focus_20261022"
EXCLUSION = "evidence/r3472_exclusion_20261022"

SUMMARIES = {'R8_3_436': 'General complex categorification remains unresolved after the source-scope audit. The prescribed near-group scalar equations pass, but completeness of that scalar table for every spherical category has not been established. The unitary categorification obstruction is retained.', 'R8_3_65': 'General complex categorification is excluded. The new pointed-induction Fourier criterion gives six exact separators covering all four pointed C4 associator classes; the two-dimension Galois reduction makes the exclusion general. This case left the unresolved inventory on 22 October 2026.', 'R8_3_928': 'An exact integer-phase refinement reduces the complete ten-pattern rational domain to four survivors: 40, 49, 186 and 191. Six patterns are excluded by complete branching certificates with 49 exact Farkas leaves. Each survivor has nonnegative integer phase counts and a rational auxiliary witness. The all-order linked trace argument covers moments through height six; 288 is a trace representative box, not a bound on categorical twist orders. This narrows necessary center data and does not construct a modular category or exclude the ring. General unbraided categorification remains unresolved.', 'R8_3_941': 'Fourteen center allocations survive the new saturated-conductor and spectral-fibre constraints. A zero-residual Gram criterion forces additional nonnegative integral fusion products in every allocation. These partial products do not complete a center or categorification; general unbraided existence remains unresolved.', 'R8_3_982': 'A unitary categorification is identified: the eight-object triality-zero component of the E21 exceptional fusion category from the conformal embedding SU(3)_21 into E7_1. All 512 fusion coefficients match the census tensor. The algebra 1+X5 and both nonregular based-module types are realized. Braided categorification and braided Morita representatives remain excluded. Every Morita partner has the same based fusion ring, without a rank or multiplicity cutoff.', 'R8_3_1154': 'All three center patterns and 25 pair histograms survive. A new semionic-packet theorem uniquely reconstructs four entire S columns and fusion matrices; each packet object and its dual generate the full center in two tensor steps. One exact quartic Gram witness survives. A positive field-coordinate criterion excludes the specific index-five SU(3)_7 tensor Fibonacci construction. No full category or general exclusion is obtained.', 'R8_3_1768': 'Saturated conductor support and Galois-fibre constraints exclude 39 of 40 indicator/Gram branches. The remaining V=4 branch has an exact rational witness and a unique Galois-unit restriction. Outside the two distinguished objects, the sector with irrational d/D has either 18 objects of dimension 72+12sqrt(37) or 72 objects of dimension 36+6sqrt(37), all with primitive-37 twists. These are sector counts, not total center ranks or counts of all primitive-37 twists. In the 18-object branch, an explicit 19-dimensional modular block forces all products of the 18 objects; every forced coefficient is a nonnegative integer. General unbraided categorification remains unresolved; every braided Morita representative is excluded.', 'R8_3_1795': 'General complex categorification is excluded. The C2 Fourier-packing criterion gives exact separators for all sixteen indicator branches, covering both pointed associators. The signed-sphericalization and Galois reduction makes the exclusion general. This case left the unresolved inventory on 22 October 2026.', 'R8_3_3472': 'General complex categorification is excluded. The complete center induction domain has 372 assignments. Exact STS obstructions remove all but one symmetry orbit; the remaining orbit admits no Galois-compatible twist multiplicities satisfying the required rotation indicators. An exact verifier checks 1,648 integer-bound deductions and a final rational separating inequality, with a separate independent replay. The sphericalization and Galois reduction makes the exclusion general. Earlier necessary-condition witnesses are retained as historical stages, not categorical constructions. This case left the unresolved inventory on 22 October 2026.'}

CREATIVE_RECORDS = {'R8_3_928': [('Exact integer-phase certificates: ten rational patterns reduced to four', 'r928_r941/integer_followup/verification.json'), ('Saturated conductor and signed spectral-fibre masks', 'r928_r941/R928_spectral_mask.json'), ('Earlier rational refinement: oriented complex-semion constraints on all ten allocations', 'r928_r941/R928_complex_semion.json')], 'R8_3_941': [('Saturated conductor and signed spectral-fibre masks', 'r928_r941/R941_spectral_mask.json'), ('Forced fusion products from zero Gram residuals', 'r928_r941/R941_packet_closure.json')], 'R8_3_982': [('Unitary E21 neutral-component model: exact tensor identification', 'r982/e21_model.json'), ('Every Morita partner has the same based fusion ring', 'r982/morita_ring.json'), ('Complete rank and commutativity restrictions on Morita partners', 'r982/morita_object.json')], 'R8_3_1154': [('Forced four-object semionic packet on all 25 histograms', 'r1154/semionic_packet.json'), ('Full packet tensor support and remaining joint eigenspaces', 'r1154/packet_closure.json'), ('One exact surviving quartic Gram witness', 'r1154/quartic_witness_replay.json'), ('Obstruction to the direct index-five SU(3)_7 tensor Fibonacci construction', 'r1154/quantum_subgroup_route.json')], 'R8_3_1768': [('Forced 19-dimensional modular block and fusion products in the 18-object irrational-ratio branch', 'unified/r1768_weil_verification.json'), ('Complete forty-branch saturated Galois-fibre audit', 'r1768/verification.json'), ('Exact arithmetic and irrational-ratio sector counts', 'r1768/arithmetic_verification.json'), ('Unique Galois-unit restriction and surviving rational witness', 'r1768/unit_orbit_cone.json')], 'R8_3_3472': [('Complete arithmetic domains and exact Morita spectrum exclusions', 'r3472/verification.json'), ('Precisely scoped generalized-Haagerup construction attempts', 'r3472/construction_routes.json')]}

CREATIVE_PROOFS = {'R8_3_928': ['r928_r941/integer_followup/PROOF.md', 'r928_r941/integer_followup/README.md', 'r928_r941/integer_followup/branches.json', 'r928_r941/integer_followup/search.json', 'r928_r941/integer_followup/verify.py', 'r928_r941/PROOF.md', 'unified/SATURATED_CONDUCTOR.md', 'unified/COMPOSITE_SIGNED_SUPPORT.md'], 'R8_3_941': ['r928_r941/PROOF.md', 'unified/SATURATED_CONDUCTOR.md', 'unified/COMPOSITE_SIGNED_SUPPORT.md'], 'R8_3_982': ['r982/E21_MODEL.md', 'r982/MORITA_OBJECT.md', 'r982/MORITA_RING.md', 'unified/E21_MODEL_AUDIT.md'], 'R8_3_1154': ['r1154/PROOF.md', 'r1154/PACKET_CLOSURE.md', 'r1154/QUANTUM_SUBGROUP_ROUTE.md', 'unified/audits/R1154_PACKET_REVIEW.md'], 'R8_3_1768': ['unified/R1768_WEIL_BLOCK.md', 'r1768/WEIL_AUDIT.md', 'r1768/GALOIS_FIBRES.md', 'unified/SATURATED_CONDUCTOR.md'], 'R8_3_3472': ['r3472/PROOF.md', 'r3472/CONSTRUCTION_ROUTES.md']}


FOCUS_RECORDS = {
    "R8_3_3472": [
        ("All-Morita dimension field and pointed order-one-or-seven theorem", "morita/verification.json"),
        ("Two possible rank-fourteen based rings and scoped Radchenko–Wheeler obstruction", "constructions/verification.json"),
        ("Simple-center structure and exact formal codegrees", "center/structure.json"),
        ("Stronger center equations: exact integer witness, no twist-phase or categorical claim", "center/integer_witness.json"),
        ("Earlier exact rational witness for the same stronger center equations", "center/rational_witness.json"),
        ("Forced pseudo-unitary third indicators and surviving earlier phase witness", "independent/third_indicators_receipt.json"),
        ("Integer center point with compatible fourth-order indicator and rotation moments", "independent/phase_receipt.json"),
        ("Independent all-Morita arithmetic and proof audit", "review/independent_morita_verification.json"),
        ("Historical second-branch helper repair and unchanged-verifier replay", "reproducibility/repair_verification.json"),
    ],
}

FOCUS_PROOFS = {
    "R8_3_3472": [
        "README.md", "manuscript.tex", "morita/README.md", "morita/manuscript.tex",
        "constructions/CONSTRUCTIONS.md", "constructions/constructions.tex",
        "constructions/C7_m2_identity_tensor.json", "constructions/C7_m2_inversion_tensor.json",
        "center/README.md", "center/center.tex", "independent/THIRD_INDICATORS.md", "independent/PHASE_EXTENSION.md",
        "independent/phase_certificate.json", "independent/verify_phase_extension.py",
        "independent/third_indicators.tex", "review/ALL_MORITA_AUDIT.md",
        "review/constructions_review.md", "reproducibility/README.md",
    ],
}



EXCLUSION_RECORDS = {
    "R8_3_3472": [
        ("General exclusion: complete center domain and exact rotation-indicator contradiction", "verification.json"),
    ],
}

EXCLUSION_PROOFS = {
    "R8_3_3472": [
        "README.md", "manuscript.tex", "replay.py", "verification.json",
        "domain/replay.py", "domain/enumerate_low.py", "frames/replay.py",
        "model/check.py", "terminal/check.py", "terminal/models.json",
        "terminal/final_field_farkas.json", "independent/verify.py", "independent/certificate.json",
    ],
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
                    return {**{k: v for k, v in payload.items() if k not in (name, "source_sha256", "artifact_sha256", "historical_publication_artifact_sha256")}, "record": matches[0]}
    raise ValueError(f"No unique labelled record for {ring_id}")


def research_record(repo, title, path, data=None):
    return {"title": title, "source": path, **source_location(repo, path),
            "source_sha256": digest(repo / path),
            "data": read_json(repo, path) if data is None else data}


def collect_source_paths(repo, value, found):
    """Collect explicit repository paths, leaving prose and external URLs intact."""
    if isinstance(value, dict):
        for k, v in value.items():
            if k in {"source_sha256", "artifact_sha256", "historical_publication_artifact_sha256"} and isinstance(v,dict):
                continue  # The complete hash map remains accessible through its bound research-source link.
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


def rank8_research(repo, ring_id, audit, audit_source):
    if ring_id == "R8_3_436":
        return [research_record(repo, "Current source-scope correction · general existence unresolved", "evidence/audit_20261024/README.md", {"general_status":"unresolved", "unitary_status":"excluded", "scope":"The scalar replay does not establish completeness for arbitrary spherical categories."}), research_record(repo, "Preserved unitary inversion obstruction", "evidence/rank8_m3_20261021/models/r436_inversion_attempt.json")]
    # Newest stage first, with older source fields retained and explicitly labelled.
    previous = select_record(read_json(repo, f"{RESEARCH}/per_ring_research_audit.json"), ring_id)
    research = [research_record(repo, "Earlier published per-ring audit · previous research stage",
                                f"{RESEARCH}/per_ring_research_audit.json", previous)]
    if audit_source != f"{CREATIVE}/per_ring_research_audit.json":
        creative = select_record(read_json(repo, f"{CREATIVE}/per_ring_research_audit.json"), ring_id)
        research.insert(0, research_record(repo, "Historical creative-stage per-ring audit",
                                          f"{CREATIVE}/per_ring_research_audit.json", creative))
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
    latest = [research_record(repo, title, f"{EXCLUSION}/{path}")
              for title, path in EXCLUSION_RECORDS.get(ring_id, [])]
    latest += [research_record(repo, "Current per-ring audit · latest accepted results",
                              audit_source, audit)]
    latest += [research_record(repo, "Historical necessary-condition stage · " + title, f"{FOCUS}/{path}")
               for title, path in FOCUS_RECORDS.get(ring_id, [])]
    latest += [research_record(repo, ("Historical scoped result · " + title) if ring_id in EXCLUSION_RECORDS else title,
                               f"{CREATIVE}/{path}")
               for title, path in CREATIVE_RECORDS.get(ring_id, [])]
    return latest + research


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
    realized_by_id = {r["id"]: r for r in realized}
    closed_scopes = scope_payload.get("closed_cases", {})
    realized_scopes = scope_payload.get("realized_cases", {})
    if not set(realized_scopes) <= set(realized_by_id):
        raise ValueError("A retained realized dossier has no realized-catalogue model")
    census = {r['id']: r for r in read_json(repo, 'evidence/rank8_m3_20261021/pipeline/census_m3.json')}
    closed = {rid: census[rid]['tensor'] for rid in closed_scopes}
    retained_realized = {rid: realized_by_id[rid]['fusion_tensor'] for rid in realized_scopes}
    all_ids = [r["id"] for r in realized] + list(remaining["TENSORS"]) + list(closed)
    if len(set(all_ids)) != len(all_ids):
        raise ValueError("Duplicate realized/unresolved case identifiers")
    for record in realized:
        write_literal(folder, record["id"], record["fusion_tensor"], record["rank"], record["tensor_sha256"])
    extension = read_json(repo, "site/dist/data/rank8_m3_update.json")
    audit_source = extension["attempts_source"]
    audit_rows = {r["id"]: r for r in read_json(repo, audit_source)["rows"]}
    rank6_rows = {r["id"]: r for r in read_json(repo, "site/dist/data/rank6_unresolved_tensors.json")}
    cases = []
    for ring_id, tensor in {**remaining["TENSORS"], **closed, **retained_realized}.items():
        is_closed = ring_id in closed
        is_realized = ring_id in retained_realized
        metadata = remaining["METADATA"].get(ring_id)
        if is_closed or is_realized:
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
        if not is_closed and not is_realized and inv["dual_indices"] != remaining["DUALS"][ring_id]:
            raise ValueError(f"Duality mismatch: {ring_id}")
        inv.update(additional_invariants(tensor, inv))
        research = rank6_research(repo, ring_id) if rank == 6 else rank8_research(repo, ring_id, audit_rows[ring_id], audit_source)
        evidence_paths = {"data/remaining_cases.py", metadata["source"], "site/categorification_scope.json"}
        collect_source_paths(repo, research, evidence_paths)
        scope = closed_scopes[ring_id] if is_closed else realized_scopes[ring_id] if is_realized else scopes[ring_id]
        collect_source_paths(repo, scope, evidence_paths)
        if rank == 6:
            evidence_paths.add("supplements/rank6/verification/classification/attempts.jsonl")
            summary = research[0]["data"]["public_summary"]
        else:
            evidence_paths.add(f"{NEXT}/README.md")
            evidence_paths.update(f"{CREATIVE}/{path}" for path in CREATIVE_PROOFS.get(ring_id, []))
            evidence_paths.update(f"{FOCUS}/{path}" for path in FOCUS_PROOFS.get(ring_id, []))
            evidence_paths.update(f"{EXCLUSION}/{path}" for path in EXCLUSION_PROOFS.get(ring_id, []))
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
            **(realized_by_id[ring_id] if is_realized else {}),
            "id": ring_id, "rank": rank, "multiplicity": metadata["multiplicity"],
            "status": "excluded" if is_closed else "unitarily_realized" if is_realized else "unresolved", "summary": summary,
            "categorification_scope": scope,
            "existence": {"general":"excluded", "unitary":"excluded"} if is_closed else {"general":"realized", "unitary":"realized"} if is_realized else rank6_rows[ring_id]["existence"] if rank == 6 else {"general": "unknown", "unitary": "excluded" if ring_id == "R8_3_436" else "unknown"},
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
    closed_records = [r for r in cases if r['status']!='unresolved']
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
    (dist / "data/resolved_cases.json").write_text(json.dumps(exact_json_integers({"schema_version":"ring-atlas/resolved-cases/v1", "scope":"Formerly unresolved case pages retained with their accepted exclusion or realization, full research history, and fusion data.", "cases":closed_records}), indent=2, ensure_ascii=False)+"\n")
    for old in folder.glob("*.txt"):
        match=re.match(r"R(\d+)_",old.stem)
        if match and int(match.group(1))>=9:
            continue  # Higher-rank builders own their existing tensor downloads.
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

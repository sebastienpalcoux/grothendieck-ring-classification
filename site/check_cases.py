#!/usr/bin/env python3
"""Check published case navigation, recorded invariants and Python tensor downloads.

This checks the website's publication contract, not categorifiability or the
mathematical arguments in its linked research reports. It needs only Python's
standard library, so the same checks run in the Pages publication workflow.
"""
from collections import Counter
import ast
import hashlib
from html.parser import HTMLParser
import json
import math
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit


HERE = Path(__file__).resolve().parent
STRUCTURE_LEVELS = ("general", "pivotal", "spherical", "pseudo_unitary", "unitary")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def check_browser_integers(value, location="unresolved_cases"):
    """Exact integers outside JavaScript's safe range must be decimal strings."""
    if type(value) is int:
        require(abs(value) <= 2**53 - 1, f"Exact integer would be rounded by the browser: {location}")
    elif isinstance(value, dict):
        for key, item in value.items():
            check_browser_integers(item, f"{location}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            check_browser_integers(item, f"{location}[{index}]")


def implication_closure(implications):
    """Closure on existence implications; this does not establish their proofs."""
    reach = {(level, level) for level in STRUCTURE_LEVELS}
    reach.update(zip(STRUCTURE_LEVELS[1:], STRUCTURE_LEVELS[:-1]))
    reach.update((entry["from"], entry["to"]) for entry in implications)
    while True:
        enlarged = reach | {(a, d) for a, b in reach for c, d in reach if b == c}
        if enlarged == reach:
            return reach
        reach = enlarged


def check_braided_scope(record, braided):
    """Validate a separate braiding audit, without changing structure statuses."""
    identifier = record["id"]
    require(isinstance(braided, dict) and braided.get("status") in {"excluded", "unresolved"},
            f"Missing or unsupported braided categorification audit: {identifier}")
    require(bool(braided.get("explanation")), f"Unexplained braided categorification status: {identifier}")
    sources = braided.get("sources")
    require(isinstance(sources, list) and bool(sources) and
            any(source.get("path") and source.get("sha256") for source in sources),
            f"Braided categorification status lacks a hash-bound audit: {identifier}")
    sources = list(sources)
    conditional = braided.get("conditional_exclusions", [])
    require(isinstance(conditional, list) and (not conditional or braided["status"] == "unresolved"),
            f"Conditional braided restrictions require an unresolved general braided status: {identifier}")
    for entry in conditional:
        require(entry.get("assumption") in STRUCTURE_LEVELS[1:] and bool(entry.get("explanation")),
                f"Missing or invalid assumption for a conditional braided obstruction: {identifier}")
        references = entry.get("sources")
        require(isinstance(references, list) and bool(references) and
                any(source.get("path") and source.get("sha256") for source in references),
                f"Conditional braided obstruction lacks a hash-bound audit: {identifier}")
        sources.extend(references)
    evidence = {source["path"]: source for source in record["evidence"]}
    for source in sources:
        if source.get("path"):
            require(source["path"] in evidence and
                    source.get("sha256") == evidence[source["path"]].get("sha256"),
                    f"Braided audit is not bound to the published case evidence: {identifier}: {source['path']}")
    obstruction = braided.get("obstruction")
    witness = braided.get("noncommutativity_witness")
    require(obstruction in {None, "noncommutative"}, f"Unsupported braided obstruction: {identifier}")
    if obstruction == "noncommutative":
        require(braided["status"] == "excluded" and record["invariants"]["commutative"] is False,
                f"Noncommutativity does not support the recorded braided status: {identifier}")
        keys = {"i", "j", "k", "N_ij_k", "N_ji_k"}
        require(isinstance(witness, dict) and set(witness) == keys and
                all(type(witness[key]) is int for key in keys) and
                all(0 <= witness[key] < record["rank"] for key in ("i", "j", "k")),
                f"Malformed noncommutativity witness: {identifier}")
        i, j, k = (witness[key] for key in ("i", "j", "k"))
        tensor = record["fusion_tensor"]
        require(witness["N_ij_k"] == tensor[i][j][k] and
                witness["N_ji_k"] == tensor[j][i][k] and
                witness["N_ij_k"] != witness["N_ji_k"],
                f"Noncommutativity witness disagrees with the fusion tensor: {identifier}")
    else:
        require(witness is None, f"Noncommutativity witness has no matching obstruction: {identifier}")
    return sources


def check_scope(record, expected, repository):
    identifier = record["id"]
    scope = record.get("categorification_scope")
    require(isinstance(scope, dict) and scope == expected,
            f"Website categorification scope differs from its audited source: {identifier}")
    general_status = "realized" if record["status"] == "unitarily_realized" else record["status"]
    require(scope.get("general_status") == general_status, f"Wrong general scope: {identifier}")
    statuses = scope.get("level_status", {})
    require(set(statuses) == set(STRUCTURE_LEVELS) and
            all(status in {"unresolved", "excluded", "realized"} for status in statuses.values()),
            f"Incomplete or unsupported categorification status: {identifier}")
    require(statuses["general"] == general_status, f"General status differs from case status: {identifier}")
    if record["status"] == "unitarily_realized":
        require(all(status == "realized" for status in statuses.values()), f"Unitary model must establish every level: {identifier}")
        require(record.get("existence") == {"general":"realized", "unitary":"realized"}, f"Inconsistent realized existence: {identifier}")
        require(bool(scope.get("model_sources")) and any(item.get("path") and item.get("sha256") for item in scope["model_sources"]), f"Unbound unitary construction: {identifier}")
    excluded = [level for level in STRUCTURE_LEVELS if statuses[level] == "excluded"]
    require(scope.get("strongest_excluded") == (excluded[0] if excluded else None),
            f"The highlighted exclusion is not the strongest established one: {identifier}")
    require(bool(scope.get("record_scope_note")) and bool(scope.get("audit_sources")),
            f"Missing categorification scope or audit provenance: {identifier}")
    same = scope.get("same_category_implications")
    existence = scope.get("existence_implications")
    require(isinstance(same, list) and isinstance(existence, list),
            f"Missing distinction between category structures and existence reductions: {identifier}")
    sources = list(scope["audit_sources"])
    sources.extend(scope.get("model_sources", []))
    sources.extend(check_braided_scope(record, scope.get("braided")))
    morita = scope.get('braided', {}).get('morita')
    if morita:
        require(morita.get('status')=='excluded' and scope['braided']['status']=='excluded' and bool(morita.get('explanation')) and bool(morita.get('sources')), 'Invalid braided Morita restriction: '+identifier)
        sources.extend(morita['sources'])
    for kind, entries in (("same_category", same), ("existence", existence)):
        for entry in entries:
            require(entry.get("from") in STRUCTURE_LEVELS and entry.get("to") in STRUCTURE_LEVELS
                    and entry["from"] != entry["to"],
                    f"Invalid categorification implication: {identifier}: {entry}")
            require(bool(entry.get("explanation")) and bool(entry.get("sources")),
                    f"Unexplained or unsourced implication: {identifier}")
            if kind == "existence":
                require(bool(entry.get("mechanism")), f"Existence reduction lacks its mechanism: {identifier}")
            else:
                require("galois" not in entry.get("mechanism", "").lower(),
                        f"Galois transport is incorrectly labelled a structure on the same category: {identifier}")
            sources.extend(entry["sources"])
    # Both kinds imply existence. An exclusion must propagate against every
    # certified implication, including a reduction through a Galois conjugate.
    for source, target in implication_closure(same + existence):
        require(statuses[target] != "excluded" or statuses[source] == "excluded",
                f"Exclusion does not respect the recorded implication {source} => {target}: {identifier}")
        require(statuses[source] != "realized" or statuses[target] == "realized", f"Realization violates implication {source} => {target}: {identifier}")
    for source in sources:
        require(bool(source.get("label")) and bool(source.get("url")),
                f"Unlabelled categorification evidence: {identifier}")
        url = urlsplit(source["url"])
        require(url.scheme == "https" and bool(url.netloc), f"Invalid categorification evidence URL: {identifier}")
        path = source.get("path")
        if path:
            require(not Path(path).is_absolute() and ".." not in Path(path).parts,
                    f"Unsafe categorification evidence path: {identifier}: {path}")
            local = repository / path
            require(local.is_file() and bool(source.get("sha256")) and
                    hashlib.sha256(local.read_bytes()).hexdigest() == source["sha256"],
                    f"Categorification evidence hash mismatch: {identifier}: {path}")
            require(unquote(url.path).endswith("/" + path),
                    f"Categorification evidence link disagrees with its bound source: {identifier}: {path}")


def check_tensor(record, root, require_character_presentation=True):
    identifier = record["id"]
    rank = record["rank"]
    tensor = record["fusion_tensor"]
    require(type(rank) is int and rank > 0, f"Invalid rank: {identifier}")
    require(type(tensor) is list and len(tensor) == rank,
            f"Invalid tensor outer dimension: {identifier}")
    require(all(type(matrix) is list and len(matrix) == rank and
                all(type(row) is list and len(row) == rank and
                    all(type(value) is int and value >= 0 for value in row)
                    for row in matrix) for matrix in tensor),
            f"Tensor must be a nonnegative integer cube: {identifier}")
    require(max(value for matrix in tensor for row in matrix for value in row)
            == record["multiplicity"], f"Wrong exact multiplicity: {identifier}")
    require(all(tensor[0][i][j] == tensor[i][0][j] == int(i == j)
                for i in range(rank) for j in range(rank)),
            f"The tensor unit is not X0: {identifier}")
    require(len(record["basis"]) == rank and len(set(record["basis"])) == rank,
            f"Wrong displayed basis: {identifier}")
    require(record.get("unit_index", 0) == 0, f"Wrong unit metadata: {identifier}")
    canonical = json.dumps(tensor, separators=(",", ":")).encode()
    require(hashlib.sha256(canonical).hexdigest() == record["tensor_sha256"],
            f"Tensor hash mismatch: {identifier}")

    relative = f"downloads/fusion-tensors/{identifier}.txt"
    require(record.get("download_url", "./" + relative) == "./" + relative,
            f"Unexpected tensor download route: {identifier}")
    downloaded = ast.literal_eval((root / relative).read_text(encoding="utf-8"))
    require(type(downloaded) is list and downloaded == tensor,
            f"Download differs from the recorded Python tensor: {identifier}")
    # Reject Python booleans/floats that compare equal to integer coefficients.
    require(all(type(matrix) is list and all(type(row) is list and
                all(type(value) is int for value in row) for row in matrix)
                for matrix in downloaded),
            f"Download is not a list of lists of lists of integers: {identifier}")

    inv = record["invariants"]
    dual = inv["dual_indices"]
    require(len(dual) == rank and all(type(j) is int and 0 <= j < rank for j in dual),
            f"Malformed dual permutation: {identifier}")
    require(all(dual[dual[i]] == i and tensor[i][j][0] == int(j == dual[i])
                for i in range(rank) for j in range(rank)),
            f"Recorded duality differs from the tensor: {identifier}")
    require(inv["invertible_indices"] ==
            [i for i in range(rank) if sum(tensor[i][dual[i]]) == 1],
            f"Recorded invertibles differ from the tensor: {identifier}")
    require(inv["commutative"] ==
            all(tensor[i][j] == tensor[j][i] for i in range(rank) for j in range(rank)),
            f"Recorded commutativity differs from the tensor: {identifier}")

    dimensions = inv["frobenius_perron_dimensions_approx"]
    require(len(dimensions) == rank and all(type(d) in (int, float) and
            math.isfinite(d) and d > 0 for d in dimensions),
            f"Invalid approximate FP dimensions: {identifier}")
    require(math.isclose(dimensions[0], 1, abs_tol=1e-8) and
            all(math.isclose(sum(tensor[i][j][k] * dimensions[k] for k in range(rank)),
                             dimensions[i] * dimensions[j], rel_tol=1e-7, abs_tol=1e-7)
                for i in range(rank) for j in range(rank)),
            f"Approximate dimensions do not satisfy the fusion rules: {identifier}")
    require(math.isclose(sum(d * d for d in dimensions),
                         inv["global_fp_dimension_approx"], rel_tol=1e-7, abs_tol=1e-7),
            f"Global dimension differs from the dimension vector: {identifier}")
    require("approximate" in inv["dimensions_method"].lower(),
            f"Numerical dimensions lack a precision statement: {identifier}")
    require(bool(inv.get("central_casimir_polynomial")),
            f"Missing exact Casimir polynomial: {identifier}")
    if inv["commutative"]:
        require(inv.get("formal_codegree_polynomial") == inv["central_casimir_polynomial"],
                f"Commutative codegree and Casimir polynomials differ: {identifier}")
        if require_character_presentation:
            exact = inv.get("exact_character_presentation", {})
            require(bool(exact.get("primitive_polynomial")) and len(exact.get("basis_values", [])) == rank,
                    f"Missing exact commutative character presentation: {identifier}")
    return relative


class LocalAssets(HTMLParser):
    def __init__(self, root, filename):
        super().__init__()
        self.root, self.filename = root, filename
        self.ids, self.fragments = set(), []
        self.scripts = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get("id"):
            require(attrs["id"] not in self.ids, f"Duplicate ID in {self.filename}: {attrs['id']}")
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            value = attrs.get(key, "")
            if value.startswith("#"):
                self.fragments.append(value[1:])
            if not value or value.startswith(("#", "data:", "mailto:")):
                continue
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc:
                continue
            relative = Path(unquote(parsed.path))
            require(not relative.is_absolute() and ".." not in relative.parts,
                    f"Page link escapes site: {self.filename}: {value}")
            target = self.root / relative
            require(target.is_file(), f"Missing page asset: {self.filename}: {value}")
        if tag == "script" and attrs.get("src"):
            self.scripts.append(urlsplit(attrs["src"]).path)


def check_site(root=None, repository=None):
    root = (root or HERE / "dist").resolve()
    repository = (repository or HERE.parent).resolve()
    atlas = read_json(root / "data/atlas.json")
    statuses = read_json(root / "data/classification_status.json")["rows"]
    unresolved_payload = read_json(root / "data/unresolved_cases.json")
    check_browser_integers(unresolved_payload)
    unresolved = unresolved_payload["cases"]
    resolved_payload = read_json(root / "data/resolved_cases.json")
    check_browser_integers(resolved_payload)
    resolved = resolved_payload["cases"]
    realized = read_json(root / "data/realized_rings.json")["records"]
    require(bool(unresolved_payload.get("tensor_convention")), "Missing fusion tensor convention")
    require(bool(unresolved_payload.get("hash_convention")), "Missing tensor hash convention")
    ids = [r["id"] for r in unresolved]
    require(len(ids) == len(set(ids)), "Duplicate unresolved identifier")
    require(set(ids) == set(atlas["remaining_ids"]) ==
            set(read_json(root / "data/current_remaining_ids.json")),
            "Case pages differ from the current unresolved inventory")
    require(not set(ids) & {r["id"] for r in realized},
            "A ring appears as both unresolved and realized")
    scope_source = read_json(repository / "site/categorification_scope.json")
    require(scope_source.get("levels") == list(STRUCTURE_LEVELS), "Categorification hierarchy is not ordered from general to unitary")
    require(set(scope_source.get("cases", {})) == set(ids), "Categorification audit does not cover precisely the current cases")
    sys.path.insert(0, str(repository / "tools"))
    from frontier_20261027 import active as frontier_active, current_scope
    for record in unresolved:
        expected = scope_source["cases"][record["id"]]
        if frontier_active(repository):
            expected = current_scope(record["id"], expected)
        check_scope(record, expected, repository)
    excluded_scopes = scope_source.get("closed_cases", {})
    realized_scopes = scope_source.get("realized_cases", {})
    require(not set(excluded_scopes) & set(realized_scopes), "Retained dossier both excluded and realized")
    require(len(resolved) == len({r['id'] for r in resolved}) and set(excluded_scopes) | set(realized_scopes) == {r['id'] for r in resolved}, "Resolved-case audit inventory mismatch")
    sys.path.insert(0, str(repository / "tools"))
    from rank8_publication import ledger_path
    current_ledger = ledger_path(repository)
    require(read_json(repository / "data/classification_status.json")["inputs"]["rank8"]["file"] == current_ledger, "Classification summary does not use current accepted rank-eight ledger")
    ledger = {r['id']:r for r in read_json(repository / current_ledger)}
    realized_by_id = {r['id']:r for r in realized}
    for record in resolved:
        identifier = record['id']
        require(identifier in ledger and record['status'] == ledger[identifier]['status'] and record['tensor_sha256'] == ledger[identifier]['tensor_sha256'], 'Resolved dossier differs from accepted ledger: '+identifier)
        require(identifier not in ids, 'Resolved case still listed as open: '+identifier)
        if identifier in excluded_scopes:
            require(record['status']=='excluded' and identifier not in realized_by_id, 'Excluded dossier appears in realized catalogue: '+identifier)
            check_scope(record, excluded_scopes[identifier], repository)
        else:
            require(record['status']=='unitarily_realized' and identifier in realized_by_id, 'Retained realized dossier has no unitary catalogue model: '+identifier)
            model=realized_by_id[identifier]
            require(model.get('existence')=='unitary' and record['fusion_tensor']==model['fusion_tensor'] and record['tensor_sha256']==model['tensor_sha256'], 'Retained realized dossier differs from catalogue: '+identifier)
            require(bool(record.get('model_reference')) and bool(record.get('model_reference_url')) and bool(record.get('construction_proof_file')), 'Retained model citation missing: '+identifier)
            check_scope(record, realized_scopes[identifier], repository)
    canonical_module = ast.parse((repository / "data/remaining_cases.py").read_text(encoding="utf-8"))
    canonical_tensors = {node.targets[0].id: ast.literal_eval(node.value)
                         for node in canonical_module.body
                         if isinstance(node, ast.Assign) and len(node.targets) == 1
                         and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ids}
    require(set(canonical_tensors) == set(ids) and
            all(canonical_tensors[record["id"]] == record["fusion_tensor"] for record in unresolved),
            "Website tensors differ from the canonical current remaining_cases.py")
    expected_counts = {(r["rank"], r["multiplicity"]): r["unresolved_general"]
                       for r in statuses if r["unresolved_general"]}
    require(Counter((r["rank"], r["multiplicity"]) for r in unresolved) == expected_counts,
            "Unresolved case counts differ from clickable classification bands")
    for scope in atlas["scope"]:
        require(sum(r["rank"] == scope["rank"] and
                    (scope.get("analyzed_through") is None or r["multiplicity"] <= scope["analyzed_through"])
                    for r in unresolved) == scope.get("unresolved", 0),
                f"Unresolved cumulative count differs at rank {scope['rank']}")
    paths = set()
    for record in unresolved + realized + resolved:
        paths.add(check_tensor(record, root))
    additive_path = root / "data/rank9_rank10_m1.json"
    if additive_path.is_file():
        additive = read_json(additive_path)["cases"]
        expected_additive = {f"R{rank}_1_{i}" for rank, count in ((9, 142), (10, 194)) for i in range(1, count + 1)}
        require(len(additive) == 336 and {record["id"] for record in additive} == expected_additive,
                "Additive tensor inventory is incomplete")
        require(not expected_additive & {record["id"] for record in unresolved + realized + resolved},
                "Additive tensor identifiers overlap the historical inventory")
        for record in additive:
            # The additive release links its character research in the portable
            # package; only the Casimir/codegree polynomial is shown inline.
            paths.add(check_tensor(record, root, require_character_presentation=False))
    rank11_path = root / "data/rank11_m1.json"
    if rank11_path.is_file():
        rank11 = read_json(rank11_path)["cases"]
        require(len(rank11) == 182 and {record["id"] for record in rank11} == {f"R11_1_{i}" for i in range(1, 183)},
                "Rank-eleven tensor inventory is incomplete")
        for record in rank11:
            paths.add(check_tensor(record, root, require_character_presentation=False))
    rank9_m2_path = root / "data/rank9_m2.json"
    if rank9_m2_path.is_file():
        rank9_m2 = read_json(rank9_m2_path)["cases"]
        require(len(rank9_m2) == 2083 and
                {record["id"] for record in rank9_m2} == {f"R9_2_{i}" for i in range(1, 2084)},
                "Rank-nine multiplicity-two tensor inventory is incomplete")
        for record in rank9_m2:
            paths.add(check_tensor(record, root, require_character_presentation=False))
    rank12_path = root / "data/rank12_m1.json"
    if rank12_path.is_file():
        rank12 = read_json(rank12_path)["cases"]
        require(len(rank12) == 632 and {record["id"] for record in rank12} == {f"R12_1_{i}" for i in range(1, 633)},
                "Rank-twelve tensor inventory is incomplete")
        for record in rank12:
            paths.add(check_tensor(record, root, require_character_presentation=False))
    require(paths == {p.relative_to(root).as_posix() for p in (root / "downloads/fusion-tensors").glob("*.txt")},
            "Tensor download directory contains a missing or unlisted record")
    for record in unresolved:
        require(record["status"] == "unresolved", f"Wrong candidate status: {record['id']}")
    for record in unresolved + resolved:
        require(bool(record.get("research")) and bool(record.get("evidence")),
                f"Missing recorded research or sources: {record['id']}")
        for evidence in record["evidence"]:
            require(bool(evidence.get("label")) and bool(evidence.get("url")),
                    f"Unlabelled or unlinked evidence: {record['id']}")
            path = evidence.get("path")
            if path:
                require(not Path(path).is_absolute() and ".." not in Path(path).parts,
                        f"Unsafe evidence path: {record['id']}: {path}")
                require((repository / path).exists(),
                        f"Missing case evidence: {record['id']}: {path}")
                if evidence.get("sha256"):
                    require((repository / path).is_file() and
                            hashlib.sha256((repository / path).read_bytes()).hexdigest() == evidence["sha256"],
                            f"Case evidence hash mismatch: {record['id']}: {path}")
    for filename in ("unresolved.html", "case.html"):
        document = (root / filename).read_text(encoding="utf-8")
        parser = LocalAssets(root, filename)
        parser.feed(document)
        require(set(parser.fragments) <= parser.ids, f"Broken internal section link: {filename}")
        require("./cases.js" in parser.scripts, f"Case page is missing its application script: {filename}")
    return {"unresolved": len(unresolved), "resolved": len(resolved), "excluded": len(excluded_scopes), "retained_realized": len(realized_scopes), "realized": len(realized), "tensor_downloads": len(paths)}


if __name__ == "__main__":
    result = check_site()
    print("Case pages checked: {unresolved} unresolved profiles, {excluded} retained excluded profiles, {retained_realized} retained realized profiles, {realized} realized catalogue rings, "
          "{tensor_downloads} exact Python tensor downloads; categorification audits and implication scopes agree.".format(**result))

"""Replay exact local-search results, rejection cuts and both proof formats.

This checks finite necessary systems. It does not certify a fusion category or
turn a necessary-model contradiction into a categorical theorem.
"""
from __future__ import annotations
import argparse
import copy
import gzip
import hashlib
import json
from pathlib import Path
import re
from fractions import Fraction as Q

import engine
import independent_check

ROOT = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read_json(path):
    path = Path(path)
    data = path.read_bytes()
    text = gzip.decompress(data) if path.suffix == ".gz" else data
    return json.loads(text)


def resolved(root, value):
    path = Path(value)
    return path if path.is_absolute() else Path(root) / path


def numeric_signature(model):
    """All mathematical rows, bounds and domains; metadata is intentionally excluded."""
    core = engine.normalize_model(model)
    return {
        "n": core["n"],
        "rows": [
            {"a": {str(j): str(v) for j, v in sorted(row["a"].items())},
             "b": str(row["b"]), "sense": row["sense"]}
            for row in core["rows"]
        ],
        "lo": list(map(str, core["lo"])),
        "up": list(map(str, core["up"])),
        "integrality": core["integrality"],
    }


def same_numeric(left, right, context):
    require(numeric_signature(left) == numeric_signature(right),
            context + ": numerical systems differ")


def model_value(task, model, name):
    return task.get(name, model.get(name, task.get("metadata", {}).get(name)))


def exact_atom(value):
    value = engine.q(value)
    return int(value) if value.denominator == 1 else str(value)


def projection_replay(task, base, root):
    """Independently substitute only fixed variables and verify every map."""
    original_path = model_value(task, base, "original_model_path")
    projection = model_value(task, base, "fixed_projection")
    if not original_path and not projection:
        return None
    require(original_path and projection, "Projection needs its original model and complete map")
    raw_path = resolved(root, original_path)
    raw = read_json(raw_path)
    require("rhs" in raw and "row_lo" not in raw and "row_up" not in raw,
            "Fixed projection expects the original equality model")
    n = int(raw["n"])
    fixed = {j: engine.q(a) for j, (a, b) in enumerate(zip(raw["lo"], raw["up"]))
             if engine.q(a) == engine.q(b)}
    free = [j for j in range(n) if j not in fixed]
    new_index = {old: new for new, old in enumerate(free)}
    rows, rhs, kept, discarded = [], [], [], []
    for i, (row, target) in enumerate(zip(raw["rows"], raw["rhs"])):
        target = engine.q(target)
        reduced = {}
        for old, coefficient in row.items():
            old, coefficient = int(old), engine.q(coefficient)
            if old in fixed:
                target -= coefficient * fixed[old]
            elif coefficient:
                j = new_index[old]
                reduced[j] = reduced.get(j, Q(0)) + coefficient
        reduced = {j: v for j, v in reduced.items() if v}
        if not reduced and target == 0:
            discarded.append(i)
        else:
            kept.append(i)
            rows.append({str(j): exact_atom(v) for j, v in reduced.items()})
            rhs.append(exact_atom(target))
    expected = {
        "n": len(free), "rows": rows, "rhs": rhs,
        "lo": [raw["lo"][j] for j in free],
        "up": [raw["up"][j] for j in free],
        "integrality": [raw.get("integrality", [1] * n)[j] for j in free],
    }
    same_numeric(base, expected, "Fixed-variable projection")
    require(list(map(int, projection["free_variable_indices"])) == free,
            "Projection free-variable indices differ")
    require({int(j): engine.q(v) for j, v in projection["fixed_assignments"].items()} == fixed,
            "Projection fixed assignments differ")
    require(list(map(int, projection["retained_source_rows"])) == kept,
            "Projection retained-row map differs")
    require(list(map(int, projection["discarded_exact_zero_rows"])) == discarded,
            "Projection discarded-row map differs")
    require(int(projection["original_variables"]) == n and
            int(projection["original_rows"]) == len(raw["rows"]),
            "Projection original dimensions differ")
    return {"raw": raw, "free": free, "fixed": fixed,
            "receipt": {
                "status": "PASS_EXACT_FIXED_SUBSTITUTION",
                "original_model_path": str(original_path),
                "original_file_sha256": hashlib.sha256(raw_path.read_bytes()).hexdigest(),
                "original_variables": n, "projected_variables": len(free),
                "retained_rows": len(kept), "discarded_exact_zero_rows": len(discarded),
            }}


def lift_witness(projection, values):
    if projection is None:
        return None
    require(len(values) == len(projection["free"]), "Projected witness length differs")
    lifted = [None] * int(projection["raw"]["n"])
    for j, value in projection["fixed"].items():
        lifted[j] = str(value)
    for old, value in zip(projection["free"], values):
        lifted[old] = value
    require(all(v is not None for v in lifted), "Incomplete lifted witness")
    engine.verify_witness(projection["raw"], lifted)
    return {"status": "PASS_EXACT_ORIGINAL_MODEL_WITNESS",
            "original_variables": len(lifted)}


def candidate_values(value):
    if isinstance(value, list):
        return value
    require(isinstance(value, dict), "Candidate must be a value list or a result object")
    if isinstance(value.get("values"), list):
        return value["values"]
    if isinstance(value.get("witness"), dict):
        return candidate_values(value["witness"])
    raise ValueError("Archived candidate has no exact value list")


def append_nogood(model, cut):
    """Preserve equality rows exactly while adding one bounded inequality."""
    result = copy.deepcopy(model)
    if "row_lo" not in result and "row_up" not in result:
        require("rhs" in result, "Cannot append a cut without row bounds or equality RHS")
        result["row_lo"] = list(result["rhs"])
        result["row_up"] = list(result["rhs"])
    else:
        result.setdefault("row_lo", [None] * len(result["rows"]))
        result.setdefault("row_up", [None] * len(result["rows"]))
    result["rows"].append(dict(cut["row"]))
    result["row_lo"].append(cut.get("row_lo"))
    result["row_up"].append(cut.get("row_up"))
    return result


def rejection_paths(out):
    found = []
    for path in Path(out).glob("candidate_rejection_*.json"):
        match = re.fullmatch(r"candidate_rejection_(\d+)\.json", path.name)
        require(match is not None, "Malformed candidate-rejection filename: " + path.name)
        found.append((int(match.group(1)), path))
    found.sort()
    require(len({i for i, _ in found}) == len(found), "Duplicate rejection attempt number")
    return [p for _, p in found]


def audit_task(task, out, root=ROOT):
    """Replay one task. Raises on any invalid artifact or missing claimed proof."""
    root, out = Path(root), Path(out)
    base_path = resolved(root, task["path"])
    compressed = base_path.read_bytes()
    require(hashlib.sha256(compressed).hexdigest() == task["sha256"],
            "Base task gzip SHA256 mismatch: " + str(task["id"]))
    base = read_json(base_path)
    require(base.get("id") == task["id"] and base.get("case") == task["case"],
            "Task identity differs from its base model")
    projection = projection_replay(task, base, root)
    current = copy.deepcopy(base)
    rejected = []
    prefix_digests = [engine.model_digest(engine.normalize_model(current))]
    rejected_values = []
    paths = rejection_paths(out)
    if paths:
        require(task["case"] == "R8_3_1154", "Unexpected nonlinear rejection cuts for another case")
        from cases import r1154
        vendor = root / "vendor"
        for path in paths:
            record = read_json(path)
            values = candidate_values(record["candidate"])
            engine.verify_witness(current, values)
            observed = r1154.check_candidate(base, values, vendor)
            require(observed == record["check"], "Candidate rejection receipt changed: " + path.name)
            require(not observed.get("valid"), "A surviving candidate was excluded: " + path.name)
            cut = r1154.candidate_nogood(base, values, vendor)
            require(cut == record["nogood"], "Archived no-good differs: " + path.name)
            checked = r1154.validate_nogood(base, values, observed, cut, vendor)
            require(checked.get("valid"), "Invalid rejection/no-good chain: " + path.name)
            rejected_values.append(values)
            current = append_nogood(current, cut)
            prefix_digests.append(engine.model_digest(engine.normalize_model(current)))
            rejected.append({"file": path.name, "status": observed["status"],
                             "cut_replay": checked["status"]})
    working_path = out / "working_model.json"
    stored_working_prefix = None
    stored_working_digest = None
    if working_path.is_file():
        stored_working = read_json(working_path)
        stored_working_digest = engine.model_digest(engine.normalize_model(stored_working))
        require(stored_working_digest in prefix_digests,
                "Stored working model differs from every valid rejection-chain prefix")
        stored_working_prefix = prefix_digests.index(stored_working_digest)
    # Durable, exactly validated rejection receipts are authoritative even
    # when interruption preceded the atomic working-model replacement.
    working = current
    working_transaction_pending = (
        (stored_working_prefix is None and (out.exists() or bool(paths))) or
        (stored_working_prefix is not None and stored_working_prefix != len(paths))
    )
    latest_path = out / "latest.json"
    latest = read_json(latest_path) if latest_path.is_file() else {}
    status = latest.get("status", "NO_LATEST_RESULT")
    require(not str(status).startswith("ERROR"), "Task latest result is an error: " + str(task["id"]))
    # A durable receipt can precede both the working-model update and latest
    # status update. Engine artifacts may therefore belong to any exactly
    # replayed chain prefix. The final certified status still requires the
    # complete current working model.
    input_path = out / "input_model.json"
    evidence_model = read_json(input_path) if input_path.is_file() else working
    evidence_digest = engine.model_digest(engine.normalize_model(evidence_model))
    require(evidence_digest in prefix_digests,
            "Engine input differs from every replayed rejection-chain prefix")
    evidence_prefix = prefix_digests.index(evidence_digest)
    final_prefix = len(paths)
    if status == "INFEASIBLE_CERTIFIED":
        require(evidence_prefix == final_prefix,
                "Certified result belongs to a stale pre-cut engine model")
    if status == "CANDIDATE_REJECTED_EXACTLY":
        require(paths, "Rejected-candidate status has no archived rejection chain")
    report = {
        "case": task["case"], "id": task["id"], "latest_status": status,
        "base_file_sha256": task["sha256"],
        "working_model_sha256": engine.model_digest(engine.normalize_model(working)),
        "stored_working_model_sha256": stored_working_digest,
        "stored_working_model_prefix_cuts": stored_working_prefix,
        "working_model_transaction_pending": working_transaction_pending,
        "engine_artifact_model_sha256": evidence_digest,
        "engine_artifact_prefix_cuts": evidence_prefix,
        "final_replayed_cut_count": final_prefix,
        "engine_artifacts_cover_final_working_model": evidence_prefix == final_prefix,
        "candidate_rejections_replayed": rejected,
        "categorical_nonexistence_certified": False,
    }
    if projection is not None:
        report["projection"] = projection["receipt"]
    primary_paths = [p for p in (out / "proof.json", out / "infeasibility_certificate.json")
                     if p.is_file()]
    independent_model_path = out / "independent_model.json"
    independent_proof_path = out / "independent_proof.json"
    independent_witness_path = out / "independent_witness.json"
    if independent_model_path.is_file():
        expected_equality, _ = engine.standardize_model(evidence_model)
        same_numeric(read_json(independent_model_path), expected_equality,
                     "Independent model for the exact engine chain prefix")
    if primary_paths or independent_proof_path.is_file() or status == "INFEASIBLE_CERTIFIED":
        require(primary_paths, "Claimed or partial exclusion has no primary proof")
        require(evidence_prefix == final_prefix,
                "Exclusion proof artifacts do not cover the final working model")
        require(independent_model_path.is_file() and independent_proof_path.is_file(),
                "Certified model exclusion needs both independent model and proof")
        primary_receipts = [
            {"file": path.name, "receipt": engine.verify_certificate(working, read_json(path))}
            for path in primary_paths
        ]
        independent_model = read_json(independent_model_path)
        expected, _ = engine.standardize_model(working)
        same_numeric(independent_model, expected, "Independent standardized equality model")
        independent_receipt = independent_check.verify_proof(
            independent_model, read_json(independent_proof_path))
        report.update(status="PASS_EXACT_MODEL_INFEASIBILITY_REPLAY",
                      primary_proofs=primary_receipts,
                      independent_proof=independent_receipt)
    values = None
    witness_path = out / "witness.json"
    if witness_path.is_file():
        witness = read_json(witness_path)
        values = candidate_values(witness)
        if "model_sha256" in witness:
            require(witness["model_sha256"] == evidence_digest,
                    "Witness model digest differs")
    elif status in ("EXACT_NECESSARY_WITNESS", "SURVIVING_NECESSARY_MATRIX"):
        values = candidate_values(latest)
    elif status == "CANDIDATE_REJECTED_EXACTLY" and evidence_prefix < final_prefix:
        values = rejected_values[evidence_prefix]
    if values is not None:
        engine.verify_witness(evidence_model, values)
        if evidence_prefix < final_prefix:
            require(list(map(engine.q, values)) ==
                    list(map(engine.q, rejected_values[evidence_prefix])),
                    "Engine witness differs from its archived rejected candidate")
        latest_values_match = True
        if isinstance(latest.get("values"), list):
            latest_values_match = (list(map(engine.q, latest["values"])) ==
                                   list(map(engine.q, values)))
            report["latest_values_match_engine_witness"] = latest_values_match
            if not latest_values_match:
                report["latest_status_may_precede_durable_engine_artifacts"] = True
        report["witness"] = {"status": "PASS_EXACT_NECESSARY_WITNESS",
                             "variables": len(values)}
        lifted = lift_witness(projection, values)
        if lifted:
            report["witness"]["lifted"] = lifted
        if task["case"] == "R8_3_1154":
            from cases import r1154
            candidate_check = r1154.check_candidate(base, values, root / "vendor")
            report["matrix_candidate"] = candidate_check
            # A matrix rejected by a later non-linear check can legitimately
            # remain in the final interrupted iteration; report it honestly.
            if (status == "SURVIVING_NECESSARY_MATRIX" and
                    evidence_prefix == final_prefix and latest_values_match):
                require(candidate_check.get("valid"),
                        "Latest claims a surviving matrix that fails exact replay")
        if independent_witness_path.is_file():
            require(independent_model_path.is_file(), "Independent witness has no model")
            independent_model = read_json(independent_model_path)
            expected, _ = engine.standardize_model(evidence_model)
            same_numeric(independent_model, expected, "Independent witness equality model")
            independent_witness = read_json(independent_witness_path)
            if "model_sha256" in independent_witness:
                require(independent_witness["model_sha256"] ==
                        independent_check.model_digest(independent_model),
                        "Independent witness digest differs")
            report["independent_witness"] = independent_check.verify_witness(
                independent_model, candidate_values(independent_witness))
        if "status" not in report:
            report["status"] = ("PASS_EXACT_WITNESS_REPLAY" if evidence_prefix == final_prefix
                                else "PASS_EXACT_PREFIX_WITNESS_REPLAY")
    require(status != "INFEASIBLE_CERTIFIED" or
            report.get("status") == "PASS_EXACT_MODEL_INFEASIBILITY_REPLAY",
            "Certified exclusion claim was not replayed")
    if "status" not in report:
        report["status"] = "PASS_PARTIAL_SEARCH_REPLAY" if out.exists() else "NOT_RUN"
    return report


def audit_alias(alias, tasks_by_id, reports_by_id, results_dir, root):
    representative = alias["representative"]
    if isinstance(representative, dict):
        representative = representative["id"]
    require(representative in tasks_by_id, "Unknown alias representative")
    task = tasks_by_id[representative]
    require(alias["case"] == task["case"], "Alias and representative cases differ")
    alias_model = read_json(resolved(root, alias["path"]))
    base = read_json(resolved(root, task["path"]))
    same_numeric(alias_model, base, "Deduplicated alias and representative")
    projection = projection_replay(alias, alias_model, root)
    require(projection is not None, "A deduplicated alias needs its original projection map")
    representative_out = Path(results_dir) / task["case"] / task["id"]
    witness_path = representative_out / "witness.json"
    lifted = None
    if witness_path.is_file():
        lifted = lift_witness(projection, candidate_values(read_json(witness_path)))
    return {
        "alias": alias["alias"], "case": alias["case"],
        "representative": representative,
        "status": "PASS_EXACT_ALIAS_IDENTITY_AND_PROJECTION",
        "projection": projection["receipt"],
        "lifted_witness": lifted,
        "representative_audit_status": reports_by_id[representative]["status"],
        "categorical_nonexistence_certified": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, default=ROOT / "models" / "index.json")
    parser.add_argument("--results-dir", type=Path, default=ROOT / "results")
    parser.add_argument("--case", action="append", dest="cases")
    parser.add_argument("--task", action="append", dest="task_ids")
    args = parser.parse_args()
    index = read_json(args.index)
    if isinstance(index, list):
        tasks, aliases = index, []
    else:
        tasks = index.get("tasks", index.get("models"))
        aliases = index.get("exact_equivalent_branches", index.get("aliases", []))
    require(isinstance(tasks, list), "Index must contain a task list")
    tasks_by_id = {task["id"]: task for task in tasks}
    require(len(tasks_by_id) == len(tasks), "Duplicate task identifiers")
    selected = [task for task in tasks if
                (not args.cases or task["case"] in args.cases) and
                (not args.task_ids or task["id"] in args.task_ids)]
    require(selected, "No selected tasks in the index")
    reports = [audit_task(task, args.results_dir / task["case"] / task["id"])
               for task in selected]
    reports_by_id = {report["id"]: report for report in reports}
    alias_reports = [
        audit_alias(alias, tasks_by_id, reports_by_id, args.results_dir, ROOT)
        for alias in aliases
        if (alias["representative"]["id"] if isinstance(alias["representative"], dict)
            else alias["representative"]) in reports_by_id
    ]
    audit = {
        "status": "PASS_EXACT_REPLAY_AUDIT",
        "scope": "Exact finite necessary-system artifacts and rejection-chain replay; mathematical domain and categorical closure require separate review.",
        "categorical_nonexistence_certified": False,
        "tasks": reports, "aliases": alias_reports,
        "task_count": len(reports), "alias_count": len(alias_reports),
    }
    args.results_dir.mkdir(parents=True, exist_ok=True)
    engine.atomic_json(args.results_dir / "exact_replay_audit.json", audit)
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()

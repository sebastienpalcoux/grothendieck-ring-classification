#!/usr/bin/env python3
"""Orchestrate an unchanged FLINT full replay and strict Python failure replays.

This new orchestration has not been run end to end on all 25,362 exclusions.
Only its read-only validation/control components have been tested. It reproduces
the audit's two-backend procedure; an all-Python full replay is not claimed.
The original failed process, raw outcomes and logs are always preserved.

Run from a fresh restored checkout with the frozen dependencies installed and
no pre-existing compiled binaries beside the rank-six C++ sources:
  python evidence/prepublication_20261017/rank6_backend/replay_complete.py \
    --repo . --output-dir rank6-two-backend-output --jobs 2

--validate-initial FILE checks identities and complete ordered receipt coverage
without executing mathematics, writing outputs, or reporting a replay PASS.
"""
import argparse
import ast
import collections
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import runpy
import shutil
import subprocess
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent
EXPECTED_EXCLUSIONS = 25362
ADDITIONAL_INPUTS = {
    "supplements/rank6/provenance/repository_source.json",
    "supplements/rank6/provenance/rank6_M9_verified/classification_transport.csv",
    "supplements/rank6/systems/integral_frontier_215.json",
    "supplements/rank6/research/structural_models/data/model_input_tensors.json",
    "supplements/rank6/research/structural_models/quartic/b2_7_graph_extraction.json",
    "supplements/rank6/research/structural_models/r629/graph_extraction.json",
    "supplements/rank6/research/structural_models/c3_model/probe_data.json",
    "supplements/rank6/research/structural_models/c3_model/target_R91.json",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1048576), b""):
            h.update(chunk)
    return h.hexdigest()


def objsha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def native_manifest(repo):
    return {str(binary.relative_to(repo)): sha(binary)
            for source in sorted((repo / "supplements/rank6").rglob("*.cpp"))
            for binary in (source.with_suffix(""), source.with_suffix(".exe")) if binary.is_file()}


def read_json(path):
    return json.loads(path.read_text())


def write_json(path, value):
    with path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(value, indent=2) + "\n")


def safe_relative(repo, name):
    relative = Path(name)
    require(not relative.is_absolute() and ".." not in relative.parts, "Unsafe baseline path: " + name)
    path = (repo / relative).resolve()
    require(path.is_relative_to(repo), "Baseline path escapes repository: " + name)
    return path


def check_baseline(repo, baseline_path):
    baseline = read_json(baseline_path)
    require(baseline.get("passed") is True and not baseline.get("missing_files")
            and not baseline.get("mismatches"), "Baseline identity is incomplete or failed")
    require({"supplements/rank6/" + path for path in baseline.get("extra_declared_model_and_frontier_inputs", [])}
            == ADDITIONAL_INPUTS,
            "Baseline lacks the frozen provenance/frontier/conformal model inputs")
    commitments = baseline["tracked_files"] + baseline["restored_inputs"]
    paths = [item["path"] for item in commitments]
    require(len(paths) == len(set(paths)), "Duplicate baseline paths")
    rank6 = repo / "supplements/rank6"
    observed = {
        str(path.relative_to(repo)) for path in rank6.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
        and (path.suffix in (".py", ".cpp")
             or path.is_relative_to(rank6 / "data")
             or path.is_relative_to(rank6 / "certificates"))
    }
    require(observed | ADDITIONAL_INPUTS == set(paths), "Frozen source/input file inventory changed")
    result = {}
    for item in commitments:
        require(item.get("matches_preexisting_baseline") is True, "Unbound baseline commitment")
        path = safe_relative(repo, item["path"])
        actual = sha(path)
        require(actual == item["sha256"] and path.stat().st_size == item["bytes"],
                "Frozen source/input changed: " + item["path"])
        if "baseline_git_blob_sha1" in item:
            data = path.read_bytes()
            git_sha = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            require(git_sha == item["baseline_git_blob_sha1"], "Baseline Git blob mismatch: " + item["path"])
        else:
            require(actual == item["baseline_manifest_sha256"], "Restored manifest commitment mismatch")
        result[item["path"]] = actual
    for required in ("verify.py", "software/exact.py", "software/existence.py",
                     "data/census.json", "data/decisions.json"):
        require("supplements/rank6/" + required in result, "Missing essential baseline commitment")
    return baseline, result


def load_context(repo):
    rows = read_json(repo / "supplements/rank6/data/census.json")
    ledger = read_json(repo / "supplements/rank6/data/decisions.json")
    require(len({row["id"] for row in rows}) == len(rows), "Duplicate census IDs")
    require([row["id"] for row in rows] == [row["id"] for row in ledger], "Census/ledger coverage mismatch")
    excluded = [row for row in ledger if row["status"] == "excluded"]
    require(len(excluded) == EXPECTED_EXCLUSIONS, "Unexpected frozen exclusion count")
    return rows, ledger, excluded


def load_jsonl(path):
    data = path.read_bytes()
    require(data.endswith(b"\n"), "Receipt stream lacks a complete terminal line")
    lines = data.splitlines()
    require(all(line.strip() for line in lines), "Blank line in receipt stream")
    records = [json.loads(line) for line in lines]
    require(all(isinstance(record, dict) for record in records), "Receipt is not an object")
    return records


def validate_initial_records(records, excluded):
    require(len(excluded) == EXPECTED_EXCLUSIONS, "Unexpected frozen exclusion count")
    require(len(records) == len(excluded), "Initial stream is incomplete or oversized")
    require([record.get("id") for record in records] == [row["id"] for row in excluded],
            "Initial ordered IDs do not exactly cover the frozen exclusions")
    for record, decision in zip(records, excluded):
        require(type(record.get("passed")) is bool, "Initial receipt lacks a Boolean outcome")
        require(record.get("kind") == decision["certificate"]["kind"], "Initial certificate kind mismatch")
    return [record["id"] for record in records if record["passed"] is False]


def extract_postloop(verifier):
    source = verifier.read_text()
    function = next(node for node in ast.parse(source).body
                    if isinstance(node, ast.FunctionDef) and node.name == "main")
    gate = next(index for index, node in enumerate(function.body)
                if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name) and node.value.func.id == "require"
                and node.value.args and isinstance(node.value.args[0], ast.UnaryOp)
                and isinstance(node.value.args[0].op, ast.Not)
                and isinstance(node.value.args[0].operand, ast.Name)
                and node.value.args[0].operand.id == "fail")
    end = next(index for index in range(gate + 1, len(function.body))
               if isinstance(function.body[index], ast.Assign)
               and any(isinstance(target, ast.Name) and target.id == "stats"
                       for target in function.body[index].targets))
    statements = function.body[gate + 1:end]
    require(len(statements) == 4, "Unexpected original post-loop check structure")
    tail = function.body[end:]
    require(not any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id == "require" for stmt in tail for node in ast.walk(stmt)),
            "Additional original post-loop check omitted")
    return source, statements, function.body[gate].lineno


def validate_initial_exit(returncode, failed, stderr_text, stdout_text, verifier, summary_path):
    require("TRUSTED SOURCE IMPORT AND CONSTRUCTED MODELS VERIFIED" in stdout_text,
            "Initial full-model/import completion marker is missing")
    if failed:
        require(returncode == 1, "Initial process did not exit at the expected certificate gate")
        lines = [line.rstrip() for line in stderr_text.splitlines() if line.strip()]
        require(lines and lines[-1] == f"exact.VerificationError: {len(failed)} negative certificates failed",
                "Initial process failed for a reason other than the final negative-certificate gate")
        _, _, gate_line = extract_postloop(verifier)
        require(f'File "{verifier}", line {gate_line}, in main' in stderr_text,
                "Initial traceback does not identify the original final gate")
        require(not summary_path.exists(), "Failed initial process unexpectedly wrote a success summary")
    else:
        require(returncode == 0, "Initial process failed despite all negative receipts passing")
        summary = read_json(summary_path)
        require(summary.get("passed") is True and summary.get("optimized_python") is False
                and summary.get("negative_certificates") == EXPECTED_EXCLUSIONS
                and summary.get("selected_multiplicity") is None,
                "Initial successful summary is missing or not a complete normal-mode replay")


def validate_selected(records, summary, failed, excluded, rows, initial_path, selected_path, source_hashes):
    require([record.get("id") for record in records] == failed,
            "Python replays must cover every initial failure exactly once and in order")
    by_id, tensors = {row["id"]: row for row in excluded}, {row["id"]: row for row in rows}
    for record in records:
        rid = record["id"]
        require(record.get("passed") is True and record.get("complete_selected_certificate") is True,
                "A selected complete certificate did not pass: " + rid)
        require(record.get("ground_types") == "python", "Selected replay used the wrong backend")
        require(record.get("kind") == by_id[rid]["certificate"]["kind"], "Selected certificate kind mismatch")
        require(record.get("certificate_canonical_json_sha256") == objsha(by_id[rid]["certificate"]),
                "Selected certificate identity mismatch")
        require(record.get("tensor_canonical_json_sha256") == objsha(tensors[rid]["N"]),
                "Selected tensor identity mismatch")
    require(summary.get("passed") is True and summary.get("source_and_inputs_unchanged") is True,
            "Selected replay summary failed or sources changed")
    require(summary.get("selected_ids") == failed and summary.get("completed") == len(failed)
            and summary.get("failed_ids") == [], "Selected replay summary coverage mismatch")
    require(summary.get("environment", {}).get("sympy_ground_types") == "python"
            and summary["environment"].get("optimized_python") is False, "Selected environment mismatch")
    require(summary.get("receipt_sha256") == sha(selected_path), "Selected receipt hash mismatch")
    require(summary.get("selection_source", {}).get("sha256") == sha(initial_path), "Selected input stream mismatch")
    require(summary.get("ledger_sha256") == source_hashes["supplements/rank6/data/decisions.json"]
            and summary.get("census_sha256") == source_hashes["supplements/rank6/data/census.json"],
            "Selected source census/ledger mismatch")
    expected_sources = {path.removeprefix("supplements/rank6/"): value for path, value in source_hashes.items()
                        if path == "supplements/rank6/verify.py"
                        or (path.startswith("supplements/rank6/software/") and Path(path).suffix in (".py", ".cpp"))}
    require(summary.get("source_sha256") == expected_sources, "Selected checker source commitments differ")


def environment_record():
    versions = {}
    for name in ("sympy", "numpy", "scipy", "python-flint"):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = None
    compiler = shutil.which("g++")
    compiler_version = (subprocess.run([compiler, "--version"], capture_output=True, text=True, check=True).stdout
                        if compiler else None)
    return {"python": platform.python_version(), "executable": sys.executable,
            "optimized_python": not __debug__, "requested_sympy_ground_types": os.environ.get("SYMPY_GROUND_TYPES"),
            "package_versions_before_mathematical_imports": versions, "argv": sys.argv,
            "compiler": {"path": compiler, "version": compiler_version},
            "temporary_directory": os.environ.get("TMPDIR"),
            "recorded_utc": datetime.now(timezone.utc).isoformat()}


def child_main(args):
    # This process has imported only standard-library modules up to this point.
    output, repo = args.output_dir.resolve(), args.repo.resolve()
    mode = args._child
    write_json(output / f"{mode}.environment.json", environment_record())
    require(__debug__, "Optimized Python is not supported by this full wrapper")
    expected_backend = "flint" if mode == "initial" else "python"
    require(os.environ.get("SYMPY_GROUND_TYPES") == expected_backend, "Wrong requested backend")
    _, before = check_baseline(repo, HERE / "baseline_identity.json")
    from sympy.external.gmpy import GROUND_TYPES
    write_json(output / f"{mode}.backend.json", {"observed_ground_types": GROUND_TYPES})
    require(GROUND_TYPES == expected_backend, "Requested SymPy backend was not loaded")
    rank6 = repo / "supplements/rank6"
    if mode == "initial":
        sys.argv = [str(rank6 / "verify.py"), "--jobs", str(args.jobs), "--out", str(output / "initial.jsonl")]
        runpy.run_path(str(rank6 / "verify.py"), run_name="__main__")
    elif mode == "selected":
        sys.argv = [str(HERE / "replay_selected.py"), "--repo", str(repo),
                    "--failed-receipts", str(output / "initial.jsonl"), "--out", str(output / "selected.jsonl")]
        runpy.run_path(str(HERE / "replay_selected.py"), run_name="__main__")
    else:
        sys.path.insert(0, str(rank6 / "software"))
        from exact import require as original_require
        from existence import positive_registry, POSITIVE_STATUSES
        ledger = read_json(rank6 / "data/decisions.json")
        source, statements, _ = extract_postloop(rank6 / "verify.py")
        original = "\n".join(ast.get_source_segment(source, node) for node in statements) + "\n"
        with (output / "postloop.original_statements.py").open("x") as stream:
            stream.write(original)
        namespace = {"ledger": ledger, "require": original_require,
                     "positive_registry": positive_registry, "POSITIVE_STATUSES": POSITIVE_STATUSES}
        exec(compile(ast.Module(body=statements, type_ignores=[]), str(rank6 / "verify.py"), "exec"), namespace)
        _, after = check_baseline(repo, HERE / "baseline_identity.json")
        require(before == after, "Sources/inputs changed during post-loop checking")
        m1, positive = namespace["m1"], namespace["positive"]
        expected = {row["id"] for row in ledger if row["status"] in POSITIVE_STATUSES}
        write_json(output / "postloop.json", {
            "passed": True, "scope": "Only the original two post-loop checks; no full-replay summary was fabricated",
            "multiplicity_one": {"expected": {"total": 39, "excluded": 18, "unitarily_realized": 21},
                                 "observed": {"total": len(m1), "excluded": sum(d["status"] == "excluded" for d in m1),
                                              "unitarily_realized": sum(d["status"] == "unitarily_realized" for d in m1)}},
            "positive_registry": {"equal": positive == expected, "registry_count": len(positive),
                                  "ledger_count": len(expected), "registry_ids": sorted(positive), "ledger_ids": sorted(expected)},
            "all_sources_and_inputs_unchanged": True, "source_input_sha256": before,
            "other_skipped_checks": [], "original_statements_sha256": sha(output / "postloop.original_statements.py")})
    return 0


def run_child(mode, args, output, expected_native):
    command = [sys.executable, "-B", str(Path(__file__).resolve()), "--_child", mode,
               "--repo", str(args.repo.resolve()), "--output-dir", str(output), "--jobs", str(args.jobs)]
    env = os.environ.copy()
    env.pop("PYTHONOPTIMIZE", None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["SYMPY_GROUND_TYPES"] = "flint" if mode == "initial" else "python"
    temporary = output / (mode + ".tmp")
    temporary.mkdir(exist_ok=False)
    for name in ("TMPDIR", "TEMP", "TMP"):
        env[name] = str(temporary)
    for name in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
        env[name] = "1"
    write_json(output / f"{mode}.command.json", {"argv": command, "cwd": str(args.repo.resolve()),
               "environment_overrides": {key: env[key] for key in ("SYMPY_GROUND_TYPES", "PYTHONDONTWRITEBYTECODE",
                                            "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "TMPDIR", "TEMP", "TMP")}})
    native_before = native_manifest(args.repo.resolve())
    require(native_before == expected_native, "Native verification binaries changed before the next child")
    start = time.monotonic()
    with (output / f"{mode}.stdout.log").open("xb") as stdout, (output / f"{mode}.stderr.log").open("xb") as stderr:
        result = subprocess.run(command, cwd=args.repo.resolve(), env=env, stdout=stdout, stderr=stderr, check=False)
    native_after = native_manifest(args.repo.resolve())
    record = {"returncode": result.returncode, "seconds": time.monotonic() - start,
              "native_executables_before": native_before, "native_executables_after": native_after,
              "remaining_temporary_files_sha256": {str(path.relative_to(temporary)): sha(path)
                                                    for path in sorted(temporary.rglob("*")) if path.is_file()}}
    write_json(output / f"{mode}.process.json", record)
    expected = "flint" if mode == "initial" else "python"
    environment = read_json(output / f"{mode}.environment.json")
    require(environment.get("optimized_python") is False
            and environment.get("requested_sympy_ground_types") == expected, "Child environment mismatch")
    require(read_json(output / f"{mode}.backend.json").get("observed_ground_types") == expected,
            "Child did not observe the requested backend")
    return record


def orchestrate(args):
    require(__debug__ and args.jobs > 0, "Use normal Python and a positive worker count")
    repo, output = args.repo.resolve(), args.output_dir.resolve()
    require(not output.is_relative_to(repo / "supplements/rank6"),
            "Output directory must be outside the frozen rank-six supplement")
    output.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    stage = "baseline"
    try:
        baseline_path, adapter = HERE / "baseline_identity.json", HERE / "replay_selected.py"
        wrapper_files = {str(path): sha(path) for path in (baseline_path, adapter, Path(__file__).resolve())}
        baseline, source_hashes = check_baseline(repo, baseline_path)
        native_bound = native_manifest(repo)
        require(not native_bound,
                "Pre-existing native verification binaries detected; use a fresh restored checkout. "
                "This wrapper will not delete or overwrite binaries belonging to another run: " + ", ".join(native_bound))
        rows, ledger, excluded = load_context(repo)
        checked_receipts = {}
        initial_path = output / "initial.jsonl"
        write_json(output / "inputs.json", {"source_input_sha256": source_hashes,
                   "wrapper_sha256": wrapper_files, "baseline_commit": baseline["baseline_commit"],
                   "baseline_tree": baseline["baseline_tree"], "full_orchestration_previously_validated": False,
                   "validation_limit": "Only read-only validator/control components were tested before publication; no complete run of this new orchestrator or all-Python full replay is claimed."})

        def unchanged():
            require(wrapper_files == {path: sha(Path(path)) for path in wrapper_files}, "Orchestration/baseline files changed")
            require(check_baseline(repo, baseline_path)[1] == source_hashes, "Frozen source/input commitments changed")
            require(checked_receipts == {name: sha(output / name) for name in checked_receipts},
                    "An already validated replay receipt or log changed")
            observed_native = native_manifest(repo)
            require(all(observed_native.get(name) == value for name, value in native_bound.items()),
                    "A previously built native verification binary changed")

        def bind_receipts(prefix):
            checked_receipts.update({path.name: sha(path) for path in output.iterdir()
                                     if path.is_file() and path.name.startswith(prefix + ".")})

        stage = "initial full FLINT replay"
        initial_process = run_child("initial", args, output, native_bound)
        unchanged()
        native_bound.update(initial_process["native_executables_after"])
        initial = load_jsonl(initial_path)
        failed = validate_initial_records(initial, excluded)
        validate_initial_exit(initial_process["returncode"], failed,
                              (output / "initial.stderr.log").read_text(), (output / "initial.stdout.log").read_text(),
                              repo / "supplements/rank6/verify.py", output / "initial.summary.json")
        initial_sha = sha(initial_path)
        bind_receipts("initial")
        selected_process = None
        if failed:
            stage = "selected full Python certificate replays"
            selected_process = run_child("selected", args, output, native_bound)
            unchanged()
            native_bound.update(selected_process["native_executables_after"])
            require(sha(initial_path) == initial_sha, "Original failed receipt stream changed")
            require(selected_process["returncode"] == 0, "Selected Python replay failed")
            selected_path = output / "selected.jsonl"
            validate_selected(load_jsonl(selected_path), read_json(output / "selected.summary.json"),
                              failed, excluded, rows, initial_path, selected_path, source_hashes)
            bind_receipts("selected")
        stage = "original post-loop checks under Python"
        postloop_process = run_child("postloop", args, output, native_bound)
        unchanged()
        native_bound.update(postloop_process["native_executables_after"])
        require(postloop_process["returncode"] == 0, "Original post-loop checks failed")
        postloop = read_json(output / "postloop.json")
        require(postloop.get("passed") is True and postloop.get("all_sources_and_inputs_unchanged") is True
                and postloop.get("source_input_sha256") == source_hashes and postloop.get("other_skipped_checks") == [],
                "Post-loop source/coverage commitments failed")
        require(postloop["multiplicity_one"]["expected"] == postloop["multiplicity_one"]["observed"]
                and postloop["positive_registry"]["equal"] is True
                and postloop["positive_registry"]["registry_ids"] == postloop["positive_registry"]["ledger_ids"],
                "Post-loop counts/registry equality failed")
        require(sha(initial_path) == initial_sha, "Original receipt stream changed")
        bind_receipts("postloop")
        unchanged()
        tensors = {row["id"]: row for row in rows}
        coverage = output / "coverage.jsonl"
        with coverage.open("x") as stream:
            for record, decision in zip(initial, excluded):
                stream.write(json.dumps({"id": decision["id"], "kind": record["kind"], "passed": True,
                    "initial_passed": record["passed"], "evidence": "initial full FLINT run" if record["passed"] else "complete selected Python replay",
                    "certificate_canonical_json_sha256": objsha(decision["certificate"]),
                    "tensor_canonical_json_sha256": objsha(tensors[decision["id"]]["N"]),
                    "census_record_canonical_json_sha256": objsha(tensors[decision["id"]])}, separators=(",", ":")) + "\n")
        evidence_hashes = {path.name: sha(path) for path in sorted(output.iterdir()) if path.is_file()}
        summary = {"combined_replay_passed": True,
            "scope": "Unchanged full FLINT verifier through its terminal negative-certificate gate, every failed complete certificate replayed under Python, and exact original post-loop checks under Python. This is a combined campaign, not a successful single full run or independent human/Lean proof.",
            "initial_run_passed": initial_process["returncode"] == 0,
            "initial_process": initial_process, "initial_failed_ids": failed,
            "initial_passed_count": EXPECTED_EXCLUSIONS - len(failed), "selected_process": selected_process,
            "fresh_complete_selected_pass_count": len(failed), "postloop_process": postloop_process,
            "covered_negative_certificates": EXPECTED_EXCLUSIONS, "all_original_failures_preserved": True,
            "source_and_inputs_unchanged": True, "baseline_commit": baseline["baseline_commit"],
            "ledger_status_counts": dict(collections.Counter(row["status"] for row in ledger)),
            "evidence_sha256": evidence_hashes, "seconds": time.monotonic() - start,
            "all_python_full_replay_executed": False}
        write_json(output / "combined.summary.json", summary)
        print(json.dumps(summary, indent=2))
        return 0
    except Exception as error:
        write_json(output / "failure.json", {"combined_replay_passed": False, "stage": stage,
                   "error": str(error), "traceback": traceback.format_exc(), "seconds": time.monotonic() - start})
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", type=Path, default=HERE.parents[2])
    parser.add_argument("--output-dir", type=Path, help="new, nonexistent output directory")
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--validate-initial", type=Path, help="read-only complete stream validation; runs no mathematics")
    parser.add_argument("--_child", choices=("initial", "selected", "postloop"), help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args._child:
        require(args.output_dir is not None and args.validate_initial is None, "Invalid child invocation")
        return child_main(args)
    if args.validate_initial:
        require(args.output_dir is None, "Read-only validation does not accept an output directory")
        check_baseline(args.repo.resolve(), HERE / "baseline_identity.json")
        _, _, excluded = load_context(args.repo.resolve())
        failed = validate_initial_records(load_jsonl(args.validate_initial), excluded)
        print(json.dumps({"coverage_valid": True, "mathematical_replay_executed": False,
                          "mathematical_replay_pass_claimed": False, "records": EXPECTED_EXCLUSIONS,
                          "failed_ids": failed, "note": "Exit state, selected replays and post-loop checks are not validated by this read-only command."}, indent=2))
        return 0
    if args.output_dir is None:
        parser.error("--output-dir is required for a new combined replay")
    return orchestrate(args)


if __name__ == "__main__":
    raise SystemExit(main())

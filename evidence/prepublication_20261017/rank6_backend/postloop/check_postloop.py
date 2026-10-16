#!/usr/bin/env python3
"""Run only the unchanged rank-six verifier's checks after its negative-proof gate."""
import argparse
import ast
import collections
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import time


def digest(data):
    return hashlib.sha256(data).hexdigest()


def identity(path):
    data = path.read_bytes()
    return {
        "bytes": len(data),
        "sha256": digest(data),
        "git_blob_sha1": hashlib.sha1(
            b"blob " + str(len(data)).encode("ascii") + b"\0" + data
        ).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    repo = args.repo.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    rank6 = repo / "supplements/rank6"
    if not __debug__ or os.environ.get("SYMPY_GROUND_TYPES") != "python":
        raise RuntimeError("Run in normal mode with SYMPY_GROUND_TYPES=python")
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(rank6 / "software"))
    from exact import require
    from existence import POSITIVE_STATUSES, REGISTRIES, positive_registry
    import sympy
    from sympy.external.gmpy import GROUND_TYPES
    require(GROUND_TYPES == "python", "SymPy did not select the Python backend")

    inventory = {item["path"]: item for item in json.loads(args.inventory.read_text())}
    ledger_path = "supplements/rank6/data/decisions.json"
    paths = [
        "supplements/rank6/verify.py",
        "supplements/rank6/software/exact.py",
        "supplements/rank6/software/existence.py",
        ledger_path,
        *[f"supplements/rank6/data/{name}.json" for name in REGISTRIES],
        "data/large_files_manifest.json",
    ]
    manifest = json.loads((repo / "data/large_files_manifest.json").read_text())
    ledger_entry = next(item for item in manifest["files"] if item["path"] == ledger_path)
    locations = {name: repo / name for name in paths}
    before = {name: identity(path) for name, path in locations.items()}
    provenance = {}
    for name, actual in before.items():
        if name == ledger_path:
            require(actual["sha256"] == ledger_entry["sha256"], "Restored ledger SHA256 mismatch")
            require(actual["bytes"] == ledger_entry["bytes"], "Restored ledger length mismatch")
            provenance[name] = {
                **actual,
                "binding": "Restored file SHA256 equals the commitment in the remote-tracked large-file manifest",
                "manifest_sha256": ledger_entry["sha256"],
                "matches_manifest": True,
            }
            continue
        expected = inventory[name]
        require(actual["git_blob_sha1"] == expected["sha"], "Remote Git blob mismatch: " + name)
        require(actual["bytes"] == expected["size"], "Remote size mismatch: " + name)
        provenance[name] = {
            **actual,
            "local_path": str(locations[name]),
            "remote_git_blob_sha1": expected["sha"],
            "matches_remote_inventory": True,
        }

    # Extract the exact original statements; do not import or invoke verify.main.
    verifier_source = (rank6 / "verify.py").read_text()
    tree = ast.parse(verifier_source, filename=str(rank6 / "verify.py"))
    main_function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "main")
    gate_index = next(
        n for n, node in enumerate(main_function.body)
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name) and node.value.func.id == "require"
        and node.value.args and isinstance(node.value.args[0], ast.UnaryOp)
        and isinstance(node.value.args[0].op, ast.Not)
        and isinstance(node.value.args[0].operand, ast.Name)
        and node.value.args[0].operand.id == "fail"
    )
    stats_index = next(
        n for n in range(gate_index + 1, len(main_function.body))
        if isinstance(main_function.body[n], ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "stats"
                for target in main_function.body[n].targets)
    )
    statements = main_function.body[gate_index + 1:stats_index]
    require(len(statements) == 4, "Unexpected post-loop check structure")
    excerpt = "\n".join(ast.get_source_segment(verifier_source, node) for node in statements) + "\n"
    (output / "executed_original_statements.py").write_text(excerpt)
    ledger = json.loads((repo / ledger_path).read_text())
    namespace = {
        "ledger": ledger, "require": require,
        "positive_registry": positive_registry, "POSITIVE_STATUSES": POSITIVE_STATUSES,
    }
    exec(compile(ast.Module(body=statements, type_ignores=[]), str(rank6 / "verify.py"), "exec"), namespace)
    m1 = namespace["m1"]
    positive = namespace["positive"]
    ledger_positive = {record["id"] for record in ledger if record["status"] in POSITIVE_STATUSES}
    observed_m1 = {
        "total": len(m1),
        "excluded": sum(record["status"] == "excluded" for record in m1),
        "unitarily_realized": sum(record["status"] == "unitarily_realized" for record in m1),
    }
    # The remaining source statements only assemble/write the success summary.
    # Record them for inspection; do not manufacture a full-replay PASS receipt.
    tail = main_function.body[stats_index:]
    tail_excerpt = "\n".join(ast.get_source_segment(verifier_source, node) for node in tail) + "\n"
    (output / "unexecuted_summary_statements.py").write_text(tail_excerpt)
    require(not any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id == "require" for stmt in tail for node in ast.walk(stmt)),
            "An additional post-loop require was omitted")
    after = {name: identity(path) for name, path in locations.items()}
    require(before == after, "A frozen source or input changed during this run")
    receipt = {
        "schema": "rank6-isolated-postloop-check-v1",
        "passed": True,
        "scope": "Only the two checks following the original negative-certificate failure gate; no full-replay PASS is asserted",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "original_commit": "e6a36a6f247b2db05f5468ffd4be1752ff42f157",
        "original_tree": "037b0822e5086c706ca221bcb416a28dd1c760be",
        "repo": str(repo),
        "command": "SYMPY_GROUND_TYPES=python PYTHONDONTWRITEBYTECODE=1 python3 "
                   + str(Path(__file__).resolve()) + " --repo " + str(repo)
                   + " --inventory " + str(args.inventory.resolve()) + " --output-dir " + str(output),
        "environment": {"python": platform.python_version(), "sympy": sympy.__version__,
                        "optimized_python": not __debug__, "SYMPY_GROUND_TYPES": os.environ["SYMPY_GROUND_TYPES"],
                        "actual_sympy_ground_types": GROUND_TYPES},
        "multiplicity_one": {"expected": {"total": 39, "excluded": 18, "unitarily_realized": 21},
                             "observed": observed_m1, "passed": True},
        "positive_registry": {"expected": "Exact equality with ledger IDs whose status belongs to POSITIVE_STATUSES",
                              "positive_statuses": list(POSITIVE_STATUSES),
                              "registry_count": len(positive), "ledger_count": len(ledger_positive),
                              "equal": positive == ledger_positive,
                              "registry_only": sorted(positive - ledger_positive),
                              "ledger_only": sorted(ledger_positive - positive),
                              "ids": sorted(positive),
                              "ledger_status_counts": dict(collections.Counter(
                                  record["status"] for record in ledger if record["status"] in POSITIVE_STATUSES))},
        "all_ledger_status_counts": dict(collections.Counter(record["status"] for record in ledger)),
        "original_check_source_lines": sorted({node.lineno for node in statements}),
        "other_skipped_operations": "After these two checks, verify.py only assembles stats, writes the summary JSON, prints it, and returns 0. These operations were intentionally not executed.",
        "other_skipped_checks": [],
        "sources_and_inputs": provenance,
        "all_sources_and_inputs_unchanged": True,
        "ledger_matches_remote_bound_manifest": True,
        "payload_parts_reconstructed_in_this_run": False,
        "payload_note": "The materialized replay and canonical checkouts omit compressed payload parts. The restored ledger is independently hashed and matches the original Git-bound manifest commitment; no payload reconstruction is claimed by this run.",
        "remote_inventory": {"path": str(args.inventory.resolve()), **identity(args.inventory)},
        "audit_script": {"path": str(Path(__file__).resolve()), **identity(Path(__file__))},
        "seconds": time.monotonic() - started,
    }
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({key: receipt[key] for key in (
        "passed", "environment", "multiplicity_one", "positive_registry",
        "all_sources_and_inputs_unchanged", "other_skipped_checks", "seconds")}, indent=2))


if __name__ == "__main__":
    main()

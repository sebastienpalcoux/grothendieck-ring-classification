#!/usr/bin/env python3
"""Exercise the real R1154 rejection, transaction recovery, and proof pipeline.

A two-variable necessary model has exactly two one-hot assignments. One fails
a mandatory vacuum moment and the other fails the mandatory spectrum. This
control calls campaign.worker directly, without monkeypatching either solver
or candidate checker, and replays the resulting complete exclusion chain.
"""
from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path
import sys
import tempfile

SOURCE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE_ROOT))

import campaign
import engine
import verify_results


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def toy_model():
    return {
        "id": "R1154_campaign_control",
        "case": "R8_3_1154",
        "branch": "CONTROL",
        "n": 2,
        "rows": [{"0": 1, "1": 1}],
        "rhs": [1],
        "lo": [0, 0],
        "up": [1, 1],
        "integrality": [1, 1],
        "row_tags": ["one_hot"],
        "matrix_rank": 2,
        "entry_domains": [
            {"i": 0, "j": 0, "lo": 0, "up": 0, "choices": []},
            {"i": 0, "j": 1, "lo": 0, "up": 1,
             "choices": [[0, 0], [1, 1]]},
            {"i": 1, "j": 1, "lo": 0, "up": 0, "choices": []},
        ],
        "onehot_groups": [[0, 1]],
        "target_characteristic_polynomial": [1, 0, -2],
        "known_actions": {
            "N2": [[0, 0], [0, 0]],
            "K3": [[0, 0], [0, 0]],
            "K4": [[2, 2], [2, 2]],
        },
        "known_vacuum_moments": {"": 1, "1": 0, "11": 1},
        "theory_scope": "Synthetic necessary-model integration control only.",
    }


def control(root):
    root = Path(root)
    model = toy_model()
    model_path = root / "models" / "control.json.gz"
    model_path.parent.mkdir(parents=True, exist_ok=True)
    encoded = (json.dumps(model, sort_keys=True, separators=(",", ":")) + "\n").encode()
    compressed = gzip.compress(encoded, mtime=0)
    model_path.write_bytes(compressed)
    task = {
        "case": model["case"], "id": model["id"],
        "path": model_path.relative_to(root).as_posix(),
        "sha256": hashlib.sha256(compressed).hexdigest(),
        "variables": 2, "rows": 1, "integer_variables": 2,
    }
    task_path = root / "task.json"
    campaign.write_json(task_path, task)
    out = root / "results" / task["case"] / task["id"]

    # Real discovery, not replay of a hand-chosen candidate.
    campaign.worker(task_path, 5.0, 0)
    first = read(out / "latest.json")
    require(first["status"] == "CANDIDATE_REJECTED_EXACTLY",
            "First real solver candidate was not rejected exactly")
    require(len(verify_results.rejection_paths(out)) == 1,
            "First rejection receipt was not durably archived")
    # The solver artifacts still describe the predecessor model. Audit must
    # replay that prefix honestly while separately validating the new no-good.
    first_audit = verify_results.audit_task(task, out, root=root)
    require(len(first_audit["candidate_rejections_replayed"]) == 1,
            "Audit did not replay the first rejected candidate")

    # Simulate a stop after the receipt transaction and before the strengthened
    # model transaction. A subsequent worker must rebuild from exact receipts.
    (out / "working_model.json").unlink()
    campaign.worker(task_path, 5.0, 1)
    second = read(out / "latest.json")
    require(second["status"] == "CANDIDATE_REJECTED_EXACTLY",
            "Receipt recovery did not discover the other rejected assignment")
    paths = verify_results.rejection_paths(out)
    require(len(paths) == 2, "Expected exactly two rejection receipts")
    records = [read(path) for path in paths]
    candidates = [tuple(map(engine.q, record["candidate"])) for record in records]
    require(len(set(candidates)) == 2,
            "Receipt recovery rediscovered an already blocked assignment")
    statuses = {record["check"]["status"] for record in records}
    require(statuses == {"REJECTED_WRONG_VACUUM_MOMENT", "REJECTED_WRONG_SPECTRUM"},
            "Actual vacuum-moment and spectrum rejection routes were not both exercised")
    require((out / "working_model.json").is_file(),
            "Recovered working model was not persisted")
    second_audit = verify_results.audit_task(task, out, root=root)
    require(len(second_audit["candidate_rejections_replayed"]) == 2,
            "Audit did not replay the full rejection chain")

    # Both and only both original assignments are now blocked. The engine must
    # produce an exact finite-model proof, accepted by the independent checker.
    campaign.worker(task_path, 5.0, 2)
    final = read(out / "latest.json")
    require(final["status"] == "INFEASIBLE_CERTIFIED",
            "Complete synthetic rejection chain did not close exactly")
    require(final.get("independent_certificate_check") == "PASS",
            "Worker did not run the independent final certificate audit")
    report = verify_results.audit_task(task, out, root=root)
    require(report["status"] == "PASS_EXACT_MODEL_INFEASIBILITY_REPLAY",
            "Final full-chain audit did not verify the exact exclusion")
    require(len(report["candidate_rejections_replayed"]) == 2,
            "Final exclusion omitted a rejection receipt")
    require(not report["categorical_nonexistence_certified"],
            "Necessary-model control must not claim categorical nonexistence")
    for name in ("infeasibility_certificate.json", "independent_model.json",
                 "independent_proof.json"):
        require((out / name).is_file(), "Missing exact proof artifact: " + name)
    require(model_path.read_bytes() == compressed, "Base model was mutated")
    return {
        "status": "PASS",
        "control": "REAL_R1154_REJECTION_RECOVERY_AND_EXACT_CLOSURE",
        "workers": 3,
        "exact_rejections": 2,
        "recovery": "working model reconstructed from archived rejection receipt",
        "final_audit": report["status"],
        "categorical_nonexistence_certified": False,
    }


def main():
    previous_root = campaign.ROOT
    try:
        with tempfile.TemporaryDirectory(prefix="rank8-campaign-control-") as folder:
            campaign.ROOT = Path(folder)
            receipt = control(Path(folder))
    finally:
        campaign.ROOT = previous_root
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()

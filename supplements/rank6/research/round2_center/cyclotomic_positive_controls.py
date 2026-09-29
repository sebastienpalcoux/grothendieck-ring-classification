"""Replay the new cyclotomic criterion against all 54 catalog model tensors.

This is an eligibility/nonexclusion control, not a collection of feasible LP
witnesses. Unsupported inputs may raise the criterion's explicit verification
guard, which is recorded separately from a returned ``None``.
"""
import collections
import hashlib
import json
import signal
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "software"))
import cyclotomic_stabilizer_trace as C
from exact import VerificationError


def deadline(*_):
    raise TimeoutError("180-second per-model criterion budget reached")


def main():
    signal.signal(signal.SIGALRM, deadline)
    catalog = json.loads((ROOT / "data/model_catalog.json").read_text())
    census = {r["id"]: r["N"] for r in json.loads((ROOT / "data/census.json").read_text())}
    decisions = json.loads((ROOT / "data/decisions.json").read_text())
    positive_ids = {r["id"] for r in decisions if r["existence"]["general"] == "yes"}
    ids = [r["id"] for r in catalog]
    if len(ids) != 54 or len(set(ids)) != 54 or set(ids) != positive_ids:
        raise RuntimeError("catalog and positive-decision domains disagree")
    rows = []
    calls = {"trace_systems": 0, "farkas_searches": 0}
    original_system, original_farkas = C.system, C.farkas

    def counted_system(*args, **kwargs):
        calls["trace_systems"] += 1
        return original_system(*args, **kwargs)

    def counted_farkas(*args, **kwargs):
        calls["farkas_searches"] += 1
        return original_farkas(*args, **kwargs)

    C.system, C.farkas = counted_system, counted_farkas
    output = Path(__file__).with_suffix(".json")
    allowed_guards = {
        "commutativity required": "ineligible_noncommutative",
        "expected quartic FP field": "ineligible_field_degree",
        "no supported exact cyclotomic embedding": "ineligible_cyclotomic_field",
    }
    for model in catalog:
        name = model["id"]
        R = census[name]
        row = {"id": name, "model": model["latex_model"]}
        started = time.monotonic()
        commutative = all(R[i][j] == R[j][i] for i in range(len(R)) for j in range(len(R)))
        row["commutative"] = commutative
        signal.alarm(180)
        try:
            modules = C.forced_module_data(R) if commutative else None
            row["local_stabilizer_eligible"] = modules is not None
            if modules is not None:
                row["local"] = {
                    "involution": modules["involution"],
                    "objects": modules["objects"],
                    "module_branches": len(modules["representations"]),
                }
                f, K, ds, D, pD, embedding = C.Characters(R).fp()
                row["fp_field_degree"] = f.degree()
                row["global_dimension_degree"] = pD.degree()
                row["global_dimension_polynomial"] = str(pD.as_expr())
                row["prime_support"] = sorted(map(int, C.s.factorint(abs(int(pD.TC())))))
            try:
                result = C.certificate(R)
            except VerificationError as exc:
                message = str(exc)
                if message not in allowed_guards:
                    raise
                row.update(outcome=allowed_guards[message], canonical_api="explicit_eligibility_guard", reason=message)
            else:
                if result is not None:
                    row.update(outcome="FALSE_EXCLUSION", certificate=result)
                    raise RuntimeError("criterion returned a certificate for a known model")
                row["canonical_api"] = "returned_none"
                if not commutative:
                    row["outcome"] = "ineligible_noncommutative"
                    row["reason"] = "noncommutative tensor; canonical API returned None before requiring commutativity"
                elif modules is None:
                    row["outcome"] = "ineligible_for_forced_local_stabilizer"
                else:
                    data = C.data_for(R, 3)
                    row["field"] = C.field_metadata(data)
                    if 3 in data["primes"] or data["F"] % 3 == 0:
                        row["outcome"] = "ineligible_third_indicator_rationality"
                    else:
                        row["outcome"] = "eligible_no_exact_obstruction_found"
        except TimeoutError as exc:
            row.update(outcome="budget_incomplete", reason=str(exc))
        except Exception as exc:
            row.setdefault("outcome", "unexpected_error")
            row["reason"] = repr(exc)
            raise
        finally:
            signal.alarm(0)
            row["seconds"] = round(time.monotonic() - started, 6)
            rows.append(row)
            report = {
                "criterion": "software/cyclotomic_stabilizer_trace.py",
                "criterion_sha256": hashlib.sha256((ROOT / "software/cyclotomic_stabilizer_trace.py").read_bytes()).hexdigest(),
                "model_domain": "all 54 model_catalog IDs, exactly equal to all general=yes decision IDs",
                "optimized_python": not __debug__,
                "per_model_budget_seconds": 180,
                "scope": "Eligibility and canonical criterion nonexclusion; ineligible inputs are not feasible trace-LP witnesses.",
                "completed": len(rows) == 54,
                "counts": dict(collections.Counter(r["outcome"] for r in rows)),
                "criterion_calls": dict(calls),
                "rows": rows,
            }
            output.write_text(json.dumps(report, indent=2) + "\n")
            print(json.dumps({k: v for k, v in row.items() if k not in ("model", "certificate")}), flush=True)


if __name__ == "__main__":
    main()

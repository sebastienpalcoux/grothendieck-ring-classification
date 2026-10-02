"""Publication metadata for immutable stage b and its separate continuation c.

This module reads decisions; mathematical replay remains in each stage verifier.
It never changes ledgers or frozen proof files.
"""
import collections
import json

BASE = "upper_residual_20261002b"
CONTINUATION = "upper_residual_20261002c"
CONTINUATION_IDS = (
    "R7_2_160", "R7_4_1417", "R7_4_1420", "R8_2_312", "R8_2_315", "R8_2_317", "R8_2_53", "R8_2_93", "R8_2_191", "R8_2_299", "R8_2_158", "R8_2_186", "R8_2_579", "R8_2_682",
)
CURRENT_TOTALS = {
    "7": {"excluded": 4135, "unitarily_realized": 27, "unresolved": 39},
    "8": {"excluded": 857, "unitarily_realized": 72, "unresolved": 44},
}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def load_stages(repo, status=None):
    base = json.loads((repo / "evidence" / BASE / "decisions.json").read_text())
    require(len(base) == len({d["id"] for d in base}) == 43,
            "Frozen stage-b publication inventory")
    require(collections.Counter(d["status"] for d in base) ==
            {"excluded": 30, "unitarily_realized": 13},
            "Frozen stage-b publication decision counts")
    extra_path = repo / "evidence" / CONTINUATION / "decisions.json"
    extra = []
    if extra_path.is_file():
        extra = json.loads(extra_path.read_text())
        require(len(extra) == len({d["id"] for d in extra}) == len(CONTINUATION_IDS) and
                {d["id"] for d in extra} == set(CONTINUATION_IDS),
                "Stage-c exact approved-case publication inventory")
        require(all(d["status"] == "excluded" and d["scope"] == "general_complex"
                    and d["rank"] == int(d["id"].split("_")[0][1:])
                    for d in extra), "Stage-c publication scope")
        require(not ({d["id"] for d in base} & {d["id"] for d in extra}),
                "Stage-b/c publication overlap")
        report_path = extra_path.parent / "report.json"
        if report_path.is_file():
            report = json.loads(report_path.read_text())
            require(report["status"] == "PASS" and report["changed_records"] == len(CONTINUATION_IDS)
                    and report["new_general_exclusions"] == len(CONTINUATION_IDS)
                    and report["new_unitary_models"] == 0,
                    "Stage-c publication replay report")
            require(report["status_totals"] == CURRENT_TOTALS,
                    "Stage-c publication replay totals")
        if status is not None:
            require(all(status["inputs"]["rank" + rank]["status_totals"] == totals
                        for rank, totals in CURRENT_TOTALS.items()),
                    "Refresh upper-rank status for stage c before rendering")
    decisions = base + extra
    totals = collections.Counter(d["status"] for d in decisions)
    require(totals == ({"excluded": 30 + len(extra), "unitarily_realized": 13} if extra else
                       {"excluded": 30, "unitarily_realized": 13}),
            "Aggregated publication stage counts")
    latest = CONTINUATION if extra else BASE
    return {"latest": latest, "decisions": decisions, "continuation": bool(extra),
            "count": len(decisions), "exclusions": totals["excluded"],
            "models": totals["unitarily_realized"],
            "continuation_ids": list(CONTINUATION_IDS) if extra else [],
            "verifier": "tools/verify_" + latest + ".py"}

def overview(stage, prefix=""):
    base_link = prefix + "evidence/" + BASE + "/README.md"
    if stage["continuation"]:
        extra_link = prefix + "evidence/" + CONTINUATION + "/README.md"
        ids = ", ".join("`" + rid + "`" for rid in stage["continuation_ids"])
        return (f"The [43-decision residual stage]({base_link}) and its "
                f"[{len(stage["continuation_ids"])}-decision continuation]({extra_link}) resolve "
                f"{stage['count']} further rings: {stage['exclusions']} general exclusions "
                f"and {stage['models']} unitary models. The continuation generally excludes "
                f"{ids}. Stage b retains its frozen proofs and replay; stage c restores "
                "the historical ledgers when checking that replay.")
    return (f"The [latest residual stage]({base_link}) resolves {stage['count']} further "
            f"rings: {stage['exclusions']} general exclusions and {stage['models']} unitary models.")

def replay_commands(stage):
    return "\n".join("python3 " + flag + stage["verifier"] for flag in ("", "-O "))

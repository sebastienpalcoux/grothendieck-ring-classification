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
STAGE_C_TOTALS = {
    "7": {"excluded": 4135, "unitarily_realized": 27, "unresolved": 39},
    "8": {"excluded": 857, "unitarily_realized": 72, "unresolved": 44},
}
THEORETICAL = "theoretical_20261016"
UNIFIED = "unified_20261016"
REVIEW = "review_20261017"
RIGIDITY = "rigidity_20261017"

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
            require(report["status_totals"] == STAGE_C_TOTALS,
                    "Stage-c publication replay totals")
        if status is not None and not (repo / "evidence" / THEORETICAL / "decisions.json").is_file():
            require(all(status["inputs"]["rank" + rank]["status_totals"] == totals
                        for rank, totals in STAGE_C_TOTALS.items()),
                    "Refresh upper-rank status for stage c before rendering")
    decisions = base + extra
    totals = collections.Counter(d["status"] for d in decisions)
    require(totals == ({"excluded": 30 + len(extra), "unitarily_realized": 13} if extra else
                       {"excluded": 30, "unitarily_realized": 13}),
            "Aggregated publication stage counts")
    latest = CONTINUATION if extra else BASE
    advance_path = repo / "evidence" / THEORETICAL / "decisions.json"
    advance = []
    if advance_path.is_file():
        advance = json.loads(advance_path.read_text())
        require(len(advance) == len({d["id"] for d in advance}) and advance,
                "Theoretical update decision inventory")
        require(all(d["status"] == "excluded" and d["scope"] == "general_complex"
                    and d["rank"] == int(d["id"].split("_")[0][1:]) for d in advance),
                "Theoretical update scope")
        require(not {d["id"] for d in advance}.intersection(d["id"] for d in decisions),
                "Theoretical update overlaps historical stages")
        current = {r: dict(v) for r, v in STAGE_C_TOTALS.items()}
        for d in advance:
            current[str(d["rank"])]["excluded"] += 1
            current[str(d["rank"])]["unresolved"] -= 1
        if status is not None and not (repo / "evidence" / UNIFIED / "decisions.json").is_file():
            require(all(status["inputs"]["rank" + r]["status_totals"] == v
                        for r, v in current.items()), "Refresh theoretical-update status before rendering")
        decisions += advance
        totals = collections.Counter(d["status"] for d in decisions)
        latest = THEORETICAL
    unified_path = repo / "evidence" / UNIFIED / "decisions.json"
    unified = []
    if unified_path.is_file():
        unified = json.loads(unified_path.read_text())
        require(unified and len(unified) == len({d['id'] for d in unified}),
                'Unified update decision inventory')
        require(all(d['status'] in ('excluded', 'unitarily_realized') and
                    d['scope'] == 'general_complex' and d['rank'] in (7, 8)
                    for d in unified), 'Unified update general scope')
        require(not {d['id'] for d in unified}.intersection(d['id'] for d in decisions),
                'Unified update overlaps historical stages')
        expected = json.loads((unified_path.parent / 'expected_totals.json').read_text())
        if status is not None and not (repo / 'evidence' / REVIEW / 'review.json').is_file():
            require(all(status['inputs']['rank' + r]['status_totals'] == v
                        for r, v in expected.items() if r in ('7', '8')),
                    'Refresh unified-update status before rendering')
        decisions += unified
        totals = collections.Counter(d['status'] for d in decisions)
        latest = UNIFIED
    historical_unified = list(unified)
    review_path = repo / 'evidence' / REVIEW / 'review.json'
    review = None
    if review_path.is_file():
        review = json.loads(review_path.read_text())
        require(review['reopened_ids'] == ['R8_2_24'] and review['historical_stage'] == UNIFIED,
                'Exact prepublication correction inventory')
        accepted = json.loads((review_path.parent / 'decisions.json').read_text())
        require(accepted == [d for d in historical_unified if d['id'] != 'R8_2_24'] and len(accepted) == 35,
                'Correction preserves every other unified decision')
        unified = accepted
        decisions = [d for d in decisions if d['id'] != 'R8_2_24']
        totals = collections.Counter(d['status'] for d in decisions)
        expected = json.loads((review_path.parent / 'expected_totals.json').read_text())
        if status is not None and not (repo / 'evidence' / RIGIDITY / 'decisions.json').is_file():
            require(all(status['inputs']['rank' + r]['status_totals'] == v
                        for r, v in expected.items() if r in ('7', '8')),
                    'Refresh review-corrected status before rendering')
        latest = REVIEW
    rigidity_path = repo / 'evidence' / RIGIDITY / 'decisions.json'
    rigidity = False
    if rigidity_path.is_file():
        accepted = json.loads(rigidity_path.read_text())
        additions = json.loads((rigidity_path.parent / 'new_decisions.json').read_text())
        require(len(additions) == 1 and additions[0]['id'] == 'R8_2_24'
                and additions[0]['status'] == 'excluded'
                and additions[0]['scope'] == 'general_complex', 'Exact rigidity-stage decision')
        require(accepted == unified + additions and len(accepted) == 36,
                'Rigidity stage preserves the complete accepted continuation')
        require(not {d['id'] for d in additions}.intersection(d['id'] for d in decisions),
                'Rigidity decision overlaps accepted stages')
        decisions += additions
        unified = accepted
        totals = collections.Counter(d['status'] for d in decisions)
        require(totals == {'excluded': 120, 'unitarily_realized': 20},
                'Combined residual program inventory')
        expected = json.loads((rigidity_path.parent / 'expected_totals.json').read_text())
        if status is not None:
            require(all(status['inputs']['rank' + r]['status_totals'] == v
                        for r, v in expected.items() if r in ('7', '8')),
                    'Refresh rigidity-stage status before rendering')
        latest = RIGIDITY
        rigidity = True
    return {"latest": latest, "decisions": decisions, "continuation": bool(extra),
            "rigidity": rigidity,
            "review": review, "historical_unified_count": len(historical_unified),
            "theoretical": bool(advance), "theoretical_count": len(advance),
            "unified": bool(unified), "unified_count": len(unified),
            "unified_exclusions": sum(d['status'] == 'excluded' for d in unified),
            "unified_models": sum(d['status'] == 'unitarily_realized' for d in unified),
            "count": len(decisions), "exclusions": totals["excluded"],
            "models": totals["unitarily_realized"],
            "continuation_ids": list(CONTINUATION_IDS) if extra else [],
            "verifier": "tools/verify_" + latest + ".py"}

def overview(stage, prefix=""):
    """Summarize the current accepted inventory without a revision narrative."""
    if stage.get('review'):
        return (f"The [current research account]({prefix}docs/RESEARCH_STATUS.md) "
                f"records **{stage['unified_count']} decisions among 38 cases**: "
                f"{stage['unified_exclusions']} proposed general exclusions and "
                f"{stage['unified_models']} unitary constructions. " +
                ("Two general questions remain open: `R6_4_155` and `R6_8_1660`. "
                 if stage.get('rigidity') else
                 "Three general questions remain open: `R6_4_155`, `R6_8_1660` and `R8_2_24`. ") +
                f"The combined residual program records {stage['count']} decisions "
                f"({stage['exclusions']} exclusions and {stage['models']} constructions), "
                "all subject to independent mathematical verification.")
    return (f"The current residual program records {stage['count']} decisions: "
            f"{stage['exclusions']} general exclusions and {stage['models']} unitary models. "
            "Scope-specific obstructions remain separate from general categorification decisions.")


def replay_commands(stage):
    return "\n".join("python3 " + flag + stage["verifier"] for flag in ("", "-O "))

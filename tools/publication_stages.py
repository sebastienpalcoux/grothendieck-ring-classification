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
        if status is not None:
            require(all(status['inputs']['rank' + r]['status_totals'] == v
                        for r, v in expected.items() if r in ('7', '8')),
                    'Refresh review-corrected status before rendering')
        latest = REVIEW
    return {"latest": latest, "decisions": decisions, "continuation": bool(extra),
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
    base_link = prefix + "evidence/" + BASE + "/README.md"
    if stage.get('review'):
        return (f"The [17 October prepublication correction]({prefix}evidence/{REVIEW}/README.md) "
                "reopens **R8_2_24** because its categorical-to-linear bridge is unproved. "
                f"The latest 38-case continuation retains **{stage['unified_count']} accepted decisions**: "
                f"{stage['unified_exclusions']} proposed general exclusions and {stage['unified_models']} unitary constructions. "
                "Three general questions remain open: R6_4_155, R6_8_1660 and R8_2_24. "
                f"Together with earlier residual stages, {stage['count']} decisions remain accepted "
                f"({stage['exclusions']} exclusions and {stage['models']} constructions), subject to independent review. "
                f"The [frozen 36-decision snapshot]({prefix}evidence/{UNIFIED}/README.md) "
                "and manuscripts remain available with dated errata and exact historical replay; "
                "their R8_2_24 exclusion is superseded.")
    if stage.get('unified'):
        return (f"The [unified theoretical continuation]({prefix}evidence/{UNIFIED}/README.md) "
                f"adds {stage['unified_exclusions']} general exclusions and "
                f"{stage['unified_models']} unitary constructions. "
                f"Together with the earlier residual stages, these updates resolve "
                f"{stage['count']} rings: {stage['exclusions']} general exclusions "
                f"and {stage['models']} unitary models. "
                "The remaining general questions and scoped results are identified explicitly. "
                "Earlier proofs, decision records and manuscript versions retain historical replay.")
    if stage.get("theoretical"):
        return (f"The [16 October theoretical update]({prefix}evidence/{THEORETICAL}/README.md) "
                f"adds {stage['theoretical_count']} general exclusions, with no new realization. "
                f"Together with the frozen October 2 stages, these updates resolve {stage['count']} "
                f"rings: {stage['exclusions']} general exclusions and {stage['models']} unitary models. "
                "Scope-specific obstructions remain separate from general categorification decisions. "
                "The earlier proofs and ledgers retain their historical replay.")
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

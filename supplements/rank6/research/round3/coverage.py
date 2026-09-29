#!/usr/bin/env python3
"""Build a ledger-independent coverage report for the frozen third campaign.

This is a receipt aggregator, not a mathematical verifier.  Only the canonical
third-campaign JSONL allocates exclusions.  Discovery labels and bounded scans
are retained independently, even when a later complete proof resolves a row.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = "verification/round3/campaign_manifest.json"
CANONICAL = "certificates/continuation_round3.jsonl"
PREFIX = "research/round3/"
KINDS = {
    "c4_associator_stabilizer": "c4_associator",
    "inert_quadratic_pseudo_exclusion": "inert_signed_spectrum",
    "inert_quadratic_signed_spectrum": "inert_signed_spectrum",
    "split_quadratic_different_pseudo_exclusion": "split_different",
    "noncommutative_signed_exclusion": "noncommutative_signed_spectrum",
    "general_stabilizer_rotation_higher": "higher_stabilizer_rotation",
    "general_integral_morita_rotation": "integral_morita",
    "general_ambient_full_character_rotation": "ambient_character",
    "general_low_verlinde_restriction": "low_verlinde",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def ring_order(rid):
    return tuple(map(int, rid.split("_")[1:]))


def counts(rows):
    return dict(sorted(Counter(r["outcome"] for r in rows).items()))


class Sources:
    def __init__(self, root):
        self.root, self.cache, self.hashes = root, {}, {}

    def read(self, path):
        if path not in self.cache:
            raw = (self.root / path).read_bytes()
            self.hashes[path] = hashlib.sha256(raw).hexdigest()
            self.cache[path] = ([json.loads(s) for s in raw.splitlines() if s.strip()]
                                if path.endswith(".jsonl") else json.loads(raw))
        return self.cache[path]

    def research(self, path):
        return self.read(PREFIX + path)

    def unchanged(self):
        for path, digest in self.hashes.items():
            require(hashlib.sha256((self.root / path).read_bytes()).hexdigest() == digest,
                    "Source changed during report generation: " + path)


def compact(row, source, outcome=None, eligible=None):
    result = {"id": row["id"], "outcome": outcome or row.get("outcome", "not_recorded"),
              "source": PREFIX + source}
    if row.get("outcome") and result["outcome"] != row["outcome"]:
        result["raw_outcome"] = row["outcome"]
    if eligible is not None:
        result["eligible"] = eligible
    for key in ("reason", "height", "scope", "metadata", "module_runs"):
        if key in row:
            result[key] = row[key]
    return result


def build(root=ROOT, require_canonical=False):
    s = Sources(Path(root))
    manifest = s.read(MANIFEST)
    ids = manifest["input_ids"]
    require(len(ids) == manifest["input_count"] == 22 and len(set(ids)) == 22,
            "Expected the frozen 22-input campaign manifest")
    require({r["id"] for r in manifest["inputs"]} == set(ids), "Manifest tensors differ")
    models = s.read("data/model_catalog.json")
    positive = [r["id"] for r in models]
    require(len(positive) == len(set(positive)) == 54, "Expected 54 distinct positive controls")
    require(not set(ids) & set(positive), "Frontier overlaps positive models")
    domain = set(ids) | set(positive)
    prior = set()
    for path in ("certificates/classification.jsonl", "certificates/continuation_20260929.jsonl",
                 "certificates/continuation_round2.jsonl"):
        prior.update(r["id"] for r in s.read(path) if r.get("status") == "excluded")
    require(not prior & set(ids), "Frozen frontier already excluded in an inherited campaign")
    pending = []
    if (s.root / "verification/round3/proof_sources.json").exists():
        for rec in s.read("verification/round3/proof_sources.json"):
            obj = s.read(rec["path"])
            cert = obj[rec["field"]] if rec.get("field") else obj
            require(rec["id"] in ids and cert["kind"] in KINDS, "Unknown pending proof")
            pending.append({"id": rec["id"], "kind": cert["kind"], "source": rec["path"],
                            "criterion": KINDS[cert["kind"]]})
    require(len({r["id"] for r in pending}) == len(pending), "Repeated pending proof")
    allocated = []
    frozen = (s.root / CANONICAL).exists()
    require(frozen or not require_canonical, "Canonical third-campaign certificates are not frozen")
    if frozen:
        for rec in s.read(CANONICAL):
            require(rec["id"] in ids and rec.get("status") == "excluded" and
                    rec.get("exact_checked") is True, "Invalid canonical allocation")
            kind = rec["certificate"]["kind"]
            require(kind in KINDS, "Unmapped canonical certificate kind: " + kind)
            require(rec["certificate"].get("scope") in ("general", "general_complex_fusion_categories"),
                    "Non-general certificate in canonical allocation")
            if rec.get("source"):
                s.read(rec["source"])
                require(rec.get("source_sha256") == s.hashes[rec["source"]],
                        "Canonical source hash mismatch: " + rec["id"])
            allocated.append({"id": rec["id"], "kind": kind, "stage": rec["stage"],
                              "criterion": KINDS[kind], "source": rec.get("source")})
        require(len({r["id"] for r in allocated}) == len(allocated), "Duplicate canonical allocation")
        if pending:
            require({r["id"] for r in allocated} == {r["id"] for r in pending},
                    "Canonical file does not yet contain the submitted proof-source domain")
    replay = None
    if frozen and (s.root / "verification/round3/release_replay.json").exists():
        rr = s.read("verification/round3/release_replay.json")
        require(rr.get("passed") is True and rr.get("optimizer_disabled") is True,
                "Third-campaign replay receipt did not pass")
        require(rr["certificate_sha256"] == s.hashes[CANONICAL], "Stale release replay receipt")
        require(set(rr["new_ids"]) == {r["id"] for r in allocated}, "Replay allocation mismatch")
        replay = {k: rr[k] for k in ("passed", "optimized_python", "optimizer_disabled",
                                     "certificate_sha256", "new_exclusions") if k in rr}

    criteria = []

    def add(key, title, application_domain, rows, notes, **extra):
        require(len({r["id"] for r in rows}) == len(rows), "Repeated effective row in " + key)
        frontier = [r for r in rows if r["id"] in ids]
        controls = [r for r in rows if r["id"] in positive]
        c = {"id": key, "title": title, "application_domain": application_domain,
             "effective_records": rows, "frontier_count": len(frontier),
             "frontier_outcomes": counts(frontier), "positive_count": len(controls),
             "positive_outcomes": counts(controls), "notes": notes, **extra}
        c["new_allocated_ids"] = ([r["id"] for r in allocated if r["criterion"] == key]
                                  if frozen else None)
        c["pending_proof_ids"] = [r["id"] for r in pending if r["criterion"] == key]
        criteria.append(c)
        return c

    def family_rows(source, applicable, applicable_rows, universe):
        byid = {r["id"]: r for r in applicable_rows}
        return [byid[rid] if rid in applicable else compact({"id": rid}, source,
                    "ineligible_family", False) for rid in universe]

    c4 = s.research("smallest/coverage.json")
    require(c4["census_rows_checked"] == 16612 and c4["residual_rows_checked"] == 22 and
            c4["positive_rows_checked"] == 54, "Incomplete C4 coverage receipt")
    app = {r["id"] for r in c4["records"]}
    rows = [compact(r, "smallest/coverage.json", "general_proof_reported" if r["outcome"] == "general_excluded"
                    else r["outcome"], eligible=r["outcome"] != "ineligible")
            for r in c4["records"]]
    hits = {r["id"] for r in rows if r["outcome"] == "general_proof_reported"}
    add("c4_associator", "C4 associator and fourth rotation", "all 16612 census tensors; 54 controls",
        family_rows("smallest/coverage.json", app, rows, ids + positive),
        [c4["positive_control_scope"], "Family eligibility and implementation eligibility are different.",
         "General proof reports outside the frozen frontier are inherited-stage confirmations."],
        census_screened=16612, family_eligible_count=len(app), family_eligible_ids=sorted(app, key=ring_order),
        implementation_eligible_count=sum(r["outcome"] != "ineligible" for r in rows),
        family_outcomes=counts(rows), overlapping_prior_exclusion_confirmations=sorted(hits & prior, key=ring_order))

    inert = s.research("arithmetic/full_census_scan.json")
    iv = s.research("arithmetic/verification_optimized.json")
    require(inert["checked"] == 16612 and iv["positive_models_checked"] == 54 and iv["passed"],
            "Incomplete inert arithmetic coverage")
    app = {r["id"] for r in inert["applicable"]}
    proofids = {r["id"] for r in iv["general_exclusions"] if r["passed"]}
    rows = [compact(r, "arithmetic/full_census_scan.json",
                    "arithmetic_exclusion_reported" if r["arithmetic"]["excluded"] else
                    "signed_spectrum_survives", True) for r in inert["applicable"]]
    c = add("inert_signed_spectrum", "Inert quadratic signed spectra", "all 16612 census tensors; 54 controls",
        family_rows("arithmetic/full_census_scan.json", app, rows, ids + positive),
        ["The full-census receipt supersedes the earlier two-hit frontier scan, and includes R6_8_6999.",
         "A surviving signed spectrum is a necessary arithmetic possibility, not a category.",
         "Three targeted sign-saturation and induction proofs strengthen surviving arithmetic spectra."],
        census_screened=16612, family_eligible_count=len(app), family_eligible_ids=sorted(app,key=ring_order),
        family_outcomes=counts(rows), targeted_general_proof_ids=sorted(proofids,key=ring_order),
        overlapping_prior_exclusion_confirmations=sorted({r["id"] for r in rows
            if r["outcome"] == "arithmetic_exclusion_reported"} & prior, key=ring_order),
        positive_verifier_controls={"checked":54,"excluded":sum(r["excluded"] for r in iv["positive_controls"])})
    require(c["positive_verifier_controls"]["excluded"] == 0, "Inert positive control rejected")

    split = s.research("arithmetic/split_verification_optimized.json")
    require(split["passed"] and split["census_checked"] == 16612 and split["positive_models_checked"] == 54,
            "Incomplete split-different coverage")
    require(not any(r["excluded"] for r in split["positive_controls"]), "Split positive control rejected")
    app = {r["id"] for r in split["census_applicable"]}
    rows = [compact(r, "arithmetic/split_verification_optimized.json", "general_proof_reported", True)
            for r in split["census_applicable"]]
    add("split_different", "Split quadratic different and signed saturation", "all 16612 census tensors; 54 controls",
        family_rows("arithmetic/split_verification_optimized.json", app, rows, ids + positive),
        ["The census screen checks the hypotheses of this particular split-different theorem."],
        census_screened=16612,family_eligible_count=len(app),family_eligible_ids=sorted(app,key=ring_order),
        positive_verifier_controls={"checked":54,"excluded":sum(r["excluded"] for r in split["positive_controls"])},
        overlapping_prior_exclusion_confirmations=[])

    nc = s.research("noncommutative/verification_optimized.json")
    require(nc["passed"] and nc["census_tensors_screened"] == 16612 and nc["positive_controls"] == 54,
            "Incomplete noncommutative coverage")
    cases = nc["noncommutative_source_cases"]
    app = {r["id"] for r in cases if r["hypotheses"]}
    rows = [compact(r,"noncommutative/verification_optimized.json",
            "signed_spectrum_survives" if r["hypotheses"] else "ineligible_hypotheses", r["hypotheses"])
            for r in cases]
    byid = {r["id"]:r for r in rows}
    rows = [byid.get(rid,compact({"id":rid},"noncommutative/verification_optimized.json",
                               "ineligible_commutative_source",False)) for rid in ids+positive]
    add("noncommutative_signed_spectrum", "Noncommutative signed spectra and complete sector check",
        "all 16612 census tensors screened for noncommutativity; 54 full-verifier controls", rows,
        ["13 source tensors are noncommutative; 10 satisfy the arithmetic hypotheses.",
         "The three targeted general proofs also exclude every remaining signed sector.",
         "R6_7_200 and R6_8_491 include exhaustive commutative signed-sector certificates.",
         "The 54 positive controls run the complete general certificate constructor; none is rejected."],
        census_screened=16612,noncommutative_source_count=len(cases),family_eligible_count=len(app),
        family_eligible_ids=sorted(app,key=ring_order),positive_verifier_controls={"checked":54,"excluded":0},
        targeted_general_proof_ids=["R6_6_170"]+[r["id"] for r in nc["additional_general_certificates"]],
        overlapping_prior_exclusion_confirmations=[])

    def batch(key,title,source,retries=(),notes=(),budget=None):
        obj = s.research(source)
        raw = obj["records"] if isinstance(obj,dict) else obj
        require({r["id"] for r in raw} == domain and len(raw) == 76, "Incomplete 22+54 batch: "+source)
        effective = {r["id"]:compact(r,source) for r in raw}
        passes = [{"source":PREFIX+source,"records":76,"outcomes":counts(raw),
                   "per_input_seconds":obj.get("per_input_seconds",budget) if isinstance(obj,dict) else budget}]
        for retry in retries:
            retryobj = s.research(retry)
            rerecs = retryobj["records"]
            require(len({r["id"] for r in rerecs}) == len(rerecs),"Repeated retry row")
            for r in rerecs:
                require(r["id"] in effective, "Retry outside original domain")
                # A retry cannot erase a completed result or change eligibility.
                require(effective[r["id"]]["outcome"] in ("budget_incomplete","arithmetic_unavailable"),
                        "Retry unexpectedly overwrites a completed result: "+r["id"])
                effective[r["id"]] = compact(r,retry)
            passes.append({"source":PREFIX+retry,"records":len(rerecs),"outcomes":counts(rerecs),
                           "per_input_seconds":retryobj.get("per_input_seconds")})
        return add(key,title,"22 frozen frontier inputs and 54 distinct positive controls",
            [effective[rid] for rid in ids+positive],list(notes),passes=passes)

    batch("ambient_character","Ambient full-character cyclotomic moments", "m4/scan_controls.json",
          ["m4/retry_positive_controls.json"],
          ["Default-conductor height-three batch; targeted higher-height and conductor-60 work is separate.",
           "no_exact_obstruction is a search outcome, not an exact primal feasibility certificate.",
           "Targeted complete proof for R6_4_211 is allocated only through the canonical file."])
    batch("low_verlinde","Low Verlinde, restriction products, and congruences", "m4/verlinde_controls.json",
          ["m4/retry_verlinde_controls.json"],
          ["This self-dual implementation has a narrower domain than the separate quartic witness systems.",
           "Targeted R6_4_243 proof and exact quartic witnesses are recorded separately.",
           "Surviving or interrupted searches do not construct a full center fusion ring."])
    batch("integral_morita","Integral Morita multiplicity congruences", "higher/integral_scan.json", notes=
          ["The quick scan stops at the first surviving module branch; it is not an exhaustive center search.",
           "Two general proofs combine all module branches, forced stabilizers, and completed center traces."],budget=60)
    batch("scalar_third","Scalar cubic-space rotation", "smallest/scalar_third_scan.json",notes=
          ["A necessary-indicator-value screen only; it reports no categorical exclusion.",
           "Unavailable arithmetic is retained as unavailable, not as ineligibility or an exclusion."])

    raw = s.research("higher/rotation_all22.json")
    require(len(raw)==22 and {r["id"] for r in raw}==set(ids),"Incomplete tensor-rotation frontier scan")
    normalized=[]
    for r in raw:
        outcome = r["outcome"]
        if outcome == "not_excluded": outcome="no_obstruction_or_ineligible"
        elif outcome == "candidate": outcome="pseudo_unitary_candidate"
        elif outcome == "incomplete":
            outcome = "ineligible_noncommutative" if r.get("reason")=="noncommutative algebra" else "budget_incomplete"
        normalized.append(compact(r,"higher/rotation_all22.json",outcome))
    add("tensor_rotation_height6","Height-six tensor rotation", "22 frozen frontier inputs",normalized,
        ["This older quadratic tensor-rotation implementation is distinct from the higher-stabilizer engine.",
         "Raw not_excluded merges ineligibility with no discovered obstruction; feasibility is not inferred.",
         "The four pseudo-unitary candidates become general only through separately recorded signed reductions."],
        raw_outcomes=counts(raw),per_input_seconds=45)

    pc = s.research("higher/positive_controls.json")
    require(len(pc)==54 and {r["id"] for r in pc}==set(positive),"Incomplete higher-stabilizer controls")
    rows = [compact(r,"higher/positive_controls.json") for r in pc]
    selected=["m4/R6_4_155_h6.json", "higher/R6_5_638_higher_h6_resumed.json",
              "higher/R6_7_1225_higher_h6_resumed.json"]
    for fn in selected:
        r=s.research(fn);rows.append(compact(r,fn))
    add("higher_stabilizer_rotation","Higher stabilizer rotation", "54 controls and 3 selected frontier inputs", rows,
        ["This is the older local-rotation engine; its positive timeout does not affect the completed integral-Morita screen.",
         "Discovery status discovered_unverified is historical; the final general proof has separate receipts."],
        positive_per_input_seconds=120)

    audit = s.research("smallest/frontier_witness_audit.json")
    require(audit["all_four_branches_verified"] and audit["optimizer_disabled"] and audit["optimized"],
            "Strong quartic witness replay did not pass")
    witness_rows=[]
    for rid in sorted({r["id"] for r in audit["records"]},key=ring_order):
        branches=[r for r in audit["records"] if r["id"]==rid]
        require(all(r["necessary_relaxation_survives"] for r in branches),"Failed quartic witness")
        witness_rows.append({"id":rid,"outcome":"exact_necessary_relaxation_survives",
            "source":PREFIX+"smallest/frontier_witness_audit.json","branches":len(branches),
            "relaxation_ranks":sorted({r["relaxation_rank"] for r in branches}),
            "equations_per_branch":sorted({r["rows"] for r in branches}),
            "variables_per_branch":sorted({r["columns"] for r in branches})})
    add("quartic_exact_witnesses","Exact coupled-character and low-Verlinde relaxation witnesses",
        "2 selected frontier inputs; 4 complete witness replays",witness_rows,
        [audit["scope"],"These witnesses are exact rational checks with optimizers disabled, not numerical feasibility statuses."])

    targeted=[]
    for fn in ("m4/R6_4_155_coupled_h6.json","m4/R6_4_629_coupled_h6.json"):
        r=s.research(fn);targeted.append(compact(r,fn))
    add("ambient_height6_targeted","Targeted coupled ambient moments through height six",
        "2 selected frontier inputs",targeted,
        ["no_exact_obstruction records an unfinished exclusion argument, not an exact primal witness or model."])

    q22=s.research("quartic/R6_4_22_h6.json")
    q91=s.research("smallest/R6_4_91_full_probe.json")
    q1035=s.research("quartic/audit_1035_lows.json")
    qs=s.research("quartic/summary.json")
    q629=s.research("m4/probe_629_verlinde.json")
    exploratory=[
        {"id":"R6_4_22","outcome":"numerical_height6_LP_survivors","source":PREFIX+"quartic/R6_4_22_h6.json",
         "branches":len(q22),"solver_status_counts":dict(Counter(str(r["status"]) for r in q22))},
        {"id":"R6_4_91","outcome":"scalar_third_refinement_survives","source":PREFIX+"smallest/R6_4_91_full_probe.json",
         "branches":len(q91),"excluded_branches":sum(r["excluded"] for r in q91),
         "surviving_branches":sum(not r["excluded"] for r in q91)},
        {"id":"R6_6_1035","outcome":qs["quartic_frontier"]["R6_6_1035"]["status"],
         "source":PREFIX+"quartic/summary.json","ambient_conductor":60,"low_frames":len(q1035),
         "character_labelled_low_frames":sum(bool(r["labellings"]) for r in q1035)},
        compact(q629,"m4/probe_629_verlinde.json")]
    add("quartic_targeted_exploration","Selected full-character refinements and conductor-60 exploration",
        "4 selected frontier inputs",exploratory,
        ["The height-six R6_4_22 receipt records numerical LP statuses; the separate height-three witnesses are exactly replayed.",
         "R6_4_91 retains two of 32 scalar-third refinement branches; both have separate exact necessary-relaxation witnesses.",
         "R6_6_1035 has 12 audited low frames, two with character labellings; the larger center system was not completed.",
         "R6_4_629 also survives a height-three ambient-plus-low-Verlinde/restriction search; no exact primal witness is claimed."])

    modelscan=s.research("models/model_scope_scan.json")
    require(modelscan["input_residual_count"]==22 and {r["id"] for r in modelscan["residuals"]}==set(ids),
            "Model search does not cover the frozen frontier")
    add("model_matching","Model matching and weak-integrality eligibility", "22 frozen frontier inputs",
        [{"id":r["id"],"outcome":"known_model_match" if r["NRW_modular_tensor_match"] or
          r["existing_positive_tensor_match"] else "no_known_model_match","source":PREFIX+"models/model_scope_scan.json",
          "weakly_integral_scope_eligible":r["weakly_integral_scope_eligible"]} for r in modelscan["residuals"]],
        [modelscan["scope"],"A match to a published open family is not a realization."],
        comparison_domains={k:modelscan[k] for k in ("NRW_tensor_records","NRW_distinct_rings",
            "positive_constructor_records","positive_distinct_rings")},
        weakly_integral_scope_eligible_count=sum(r["weakly_integral_scope_eligible"] for r in modelscan["residuals"]),
        open_family_matches=modelscan["Meng_Yu_open_families_as_of_arxiv2608_06064v1"])

    supplemental=[]
    for fn in ("higher/family_scan.json","higher/integral_family_scan.json"):
        recs=s.research(fn);supplemental.append({"source":PREFIX+fn,"domain":"four selected related-family parameters",
            "records":recs,"outcomes":counts(recs),"classification_allocation":False})
    trace=s.research("m4/trace_formula_controls.json")
    supplemental.append({"source":PREFIX+"m4/trace_formula_controls.json","domain":"formula identities, not ring inputs",
        "passed":trace["passed"],"field_order_pairs":len(trace["pairs"]),"exact_comparisons":trace["exact_comparisons"]})
    # Audit receipts add reproducibility evidence, never allocations or ring counts.
    audit_files=["smallest/final_replay.json","smallest/controls_optimized.json","models/arithmetic_audit.json",
        "models/split_different_audit.json","models/split_different_replay.json","models/c4_associator_audit.json",
        "m4/R6_4_211_exact_replay.json","m4/R6_4_243_exact_replay.json","m4/certificate_mutation_controls.json",
        "higher/integral_audit.json","quartic/nc_comm_replay.json","quartic/summary.json"]
    for fn in audit_files:
        z=s.research(fn)
        supplemental.append({"source":PREFIX+fn,"domain":"selected proof or component audit",
                             "passed":z.get("passed",z.get("all_passed")),"classification_allocation":False})

    allocations={r["id"]:r for r in allocated}
    proofmap={r["id"]:r for r in pending}
    frontier=[]
    for rid in ids:
        evidence=[{"criterion":c["id"],**r} for c in criteria for r in c["effective_records"] if r["id"]==rid]
        frontier.append({"id":rid,"multiplicity":int(rid.split("_")[1]),
            "allocation_status":("excluded_by_third_campaign" if rid in allocations else "unresolved_after_third_campaign")
                if frozen else "allocation_not_yet_frozen",
            "canonical_allocation":allocations.get(rid),"proof_source_pending_freeze":None if frozen else proofmap.get(rid),
            "criterion_evidence":evidence})
    overlap=sorted({rid for c in criteria for rid in c.get("overlapping_prior_exclusion_confirmations",[])},key=ring_order)
    by_multiplicity=[]
    for m in range(4,9):
        selected=[r for r in frontier if r["multiplicity"]==m]
        resolved=sum(r["canonical_allocation"] is not None for r in selected)
        by_multiplicity.append({"multiplicity":m,"frozen_inputs":len(selected),
            "canonical_new_exclusions":resolved if frozen else None,
            "canonical_remaining":len(selected)-resolved if frozen else None})
    report={"schema_version":1,"report_kind":"frozen_canonical_coverage" if frozen else "pre_freeze_coverage_structure",
        "classification_authority":CANONICAL,"canonical_allocation_available":frozen,
        "canonical_replay_receipt":replay,"frozen_input_count":22,"frozen_input_ids":ids,
        "positive_control_count":54,"positive_control_ids":positive,
        "input_tensors_sha256":manifest["input_tensors_sha256"],
        "original_census_sha256":manifest["original_census_sha256"],
        "canonical_new_exclusions":len(allocated) if frozen else None,
        "canonical_remaining_count":22-len(allocated) if frozen else None,
        "canonical_new_ids":[r["id"] for r in allocated] if frozen else None,
        "pending_proof_count":None if frozen else len(pending),
        "prior_exclusion_confirmation_ids":overlap,
        "prior_exclusion_confirmations_not_new_allocations":len(overlap),
        "criteria":criteria,"frontier":frontier,"by_multiplicity":by_multiplicity,"supplemental_evidence":supplemental,
        "interpretation":["No current ledger is read or used to select the 22 inputs.",
            "Only canonical general certificates allocate exclusions; search or component receipts never do.",
            "Criterion counts overlap and must not be added to compute new exclusions.",
            "Budget gaps are criterion-specific; a complete proof in another criterion can resolve the same input.",
            "An exact necessary-relaxation witness does not supply full modular data, center fusion rules, or a category."]}
    report["source_sha256"] = dict(sorted(s.hashes.items()))
    s.unchanged()
    return report


def markdown(report):
    lines=["# Third-continuation coverage", "", "Generated by `python research/round3/coverage.py`. "
        "The input domain is the frozen 22-tensor campaign manifest; the current decision ledger is not read.", ""]
    if report["canonical_allocation_available"]:
        lines += [f"The canonical third-campaign file allocates **{report['canonical_new_exclusions']} new general exclusions**, "
            f"leaving **{report['canonical_remaining_count']}** of the 22 inputs unresolved. "
            "All allocation counts below come from that file.", ""]
    else:
        lines += ["**Pre-freeze coverage structure.** Canonical third-campaign allocations are not yet available. "
            f"There are {report['pending_proof_count']} submitted proof sources; they are not counted as current classifications here.", ""]
    if report["canonical_allocation_available"]:
        lines += ["| Multiplicity | Frozen inputs | New general exclusions | Remaining |", "| ---: | ---: | ---: | ---: |"]
        for r in report["by_multiplicity"]:
            lines.append(f"| {r['multiplicity']} | {r['frozen_inputs']} | {r['canonical_new_exclusions']} | {r['canonical_remaining']} |")
        lines.append("")
    lines += ["`coverage.json` is the final machine-readable report when the canonical file exists; "
        "`coverage_structure.json` records the pre-freeze report. Regenerate after the source receipts settle:", "",
        "```sh", "python research/round3/coverage.py --require-canonical --output research/round3/coverage.json", "```", "",
        "## Application domains", "", "Counts in different criteria overlap. A bounded search that finds no obstruction "
        "does not certify a category, and a timeout does not exclude one.", "",
        "| Criterion | Application domain | Frontier outcomes | Positive-control outcomes | New canonical allocations |",
        "| --- | --- | --- | --- | --- |"]
    def display(cs):
        return "; ".join(f"{k}: {v}" for k,v in cs.items()) or "not in this batch"
    for c in report["criteria"]:
        new=c["new_allocated_ids"]
        lines.append(f"| {c['title']} | {c['application_domain']} | {display(c['frontier_outcomes'])} | "
                     f"{display(c['positive_outcomes'])} | {'pending freeze' if new is None else len(new)} |")
    lines += ["", "## Census-wide screens", "",
        "| Criterion | Tensors screened | Theorem-family eligible | Further distinction |", "| --- | ---: | ---: | --- |"]
    for c in report["criteria"]:
        if "census_screened" not in c:continue
        detail=display(c.get("family_outcomes",{}))
        if c["id"]=="noncommutative_signed_spectrum":detail=f"{c['noncommutative_source_count']} noncommutative sources; 3 targeted complete general proofs"
        if c["id"]=="split_different":detail="one complete general proof"
        lines.append(f"| {c['title']} | {c['census_screened']} | {c['family_eligible_count']} | {detail} |")
    lines += ["", f"There are **{report['prior_exclusion_confirmations_not_new_allocations']} distinct inherited exclusions** "
        "confirmed again by the new census-wide criteria: " + ", ".join(f"`{x}`" for x in report["prior_exclusion_confirmation_ids"]) +
        ". They are not new allocations. The earlier inert-family frontier receipt listed two inputs; the completed "
        "census scan also includes `R6_8_6999`.", "", "## Frozen frontier", "",
        "The table preserves complete proofs and exact witness checks separately from search outcomes. "
        "The JSON report retains every applicable batch result, including earlier timeouts.", "",
        "| Input | Canonical allocation | Additional exact evidence or surviving search |", "| --- | --- | --- |"]
    for r in report["frontier"]:
        a=r["canonical_allocation"]
        state=a["kind"] if a else ("unresolved" if report["canonical_allocation_available"] else "pending freeze")
        evidence=[]
        for e in r["criterion_evidence"]:
            if e["criterion"]=="quartic_exact_witnesses":
                evidence.append(f"{e['branches']} exact necessary-relaxation witnesses, rank " + "/".join(map(str,e["relaxation_ranks"])))
            elif e["criterion"]=="ambient_height6_targeted":evidence.append("height-six ambient search: "+e["outcome"])
            elif e["criterion"]=="quartic_targeted_exploration" and e["id"]=="R6_6_1035":
                evidence.append("conductor 60: 12 low frames, 2 character-labelled; larger system incomplete")
            elif e["criterion"]=="quartic_targeted_exploration" and e["id"]=="R6_4_629":
                evidence.append("height-three ambient + low-Verlinde search: "+e["outcome"])
        if not evidence:evidence=["criterion-specific search and eligibility outcomes recorded in coverage.json"]
        lines.append(f"| `{r['id']}` | {state} | {'; '.join(evidence)} |")
    lines += ["", "## Scope and bounded-search gaps", ""]
    for c in report["criteria"]:
        lines += [f"**{c['title']}.** " + " ".join(c["notes"]), ""]
        for group,ids in (("frontier",set(report["frozen_input_ids"])),("positive controls",set(report["positive_control_ids"]))):
            gaps=[r["id"] for r in c["effective_records"] if r["id"] in ids and r["outcome"] in ("budget_incomplete","arithmetic_unavailable")]
            if gaps:lines += [f"Remaining batch gaps ({group}): " + ", ".join(f"`{rid}`" for rid in gaps) + ".", ""]
    lines += ["The four exact quartic witness replays cover 1,909 equations and 2,242 variables per R6_4_22 branch, "
        "and 1,885 equations and 1,815 variables per R6_4_91 branch. The latter also impose the three scalar third-indicator values. "
        "These are necessary relaxations, not full modular data or models.", "",
        "The trace-formula control checks 1,056 exact identities across 176 field/order pairs. "
        "This is formula validation, not an additional 1,056 ring inputs. Source hashes, targeted proof audits, "
        "and related-family experiments are retained in the JSON report.", ""]
    return "\n".join(lines)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root",type=Path,default=ROOT)
    ap.add_argument("--output",type=Path)
    ap.add_argument("--readme",type=Path,default=Path("research/round3/README.md"))
    ap.add_argument("--require-canonical",action="store_true")
    args=ap.parse_args();r=build(args.root,args.require_canonical)
    output=args.output or Path("research/round3/" + ("coverage.json" if r["canonical_allocation_available"] else "coverage_structure.json"))
    if not output.is_absolute():output=args.root/output
    readme=args.readme if args.readme.is_absolute() else args.root/args.readme
    output.parent.mkdir(parents=True,exist_ok=True);readme.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(r,indent=2)+"\n");readme.write_text(markdown(r))
    print(json.dumps({"report":str(output),"readme":str(readme),"canonical":r["canonical_allocation_available"],
                      "new_exclusions":r["canonical_new_exclusions"],"remaining":r["canonical_remaining_count"],
                      "criteria":len(r["criteria"]),"source_receipts":len(r["source_sha256"])},indent=2))


if __name__=="__main__":main()

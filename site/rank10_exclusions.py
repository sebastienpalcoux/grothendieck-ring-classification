"""Apply the source-bound rank-ten continuation to the common catalogue."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil

RELEASE = "evidence/rank10_m1_exclusions_20261023"
EXCLUDED = {f"R10_1_{n}" for n in (114, 115, 152, 153, 179)}
OPEN = "R10_1_189"
REPO_URL = "https://github.com/sebastienpalcoux/grothendieck-ring-classification"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n")


def apply(repo, ref="main"):
    repo = Path(repo)
    source = repo / RELEASE
    if not (source / "accepted_ledger.json").is_file():
        return
    path = repo / "site/dist/data/rank9_rank10_m1.json"
    payload = json.loads(path.read_text())
    ledger_path = source / "accepted_ledger.json"
    ledger = json.loads(ledger_path.read_text())
    rows = {r["id"]: r for r in ledger["records"]}
    changes = json.loads((source / "classification_updates.json").read_text())["cases"]
    if {r["id"] for r in changes} != EXCLUDED | {OPEN}:
        raise ValueError("Unexpected continuation inventory")

    def evidence(relative, label=None):
        local = source / relative
        if not local.is_file() or not local.resolve().is_relative_to(source.resolve()):
            raise ValueError("Missing continuation evidence: " + relative)
        name = RELEASE + "/" + relative
        return {"label": label or relative, "path": name,
                "url": f"{REPO_URL}/blob/{ref}/{name}", "sha256": digest(local)}

    for ring in payload["cases"]:
        change = next((r for r in changes if r["id"] == ring["id"]), None)
        if change is None:
            continue
        rid = ring["id"]
        if ring["tensor_sha256"] != change["tensor_sha256_compact_json"]:
            raise ValueError("Continuation tensor differs: " + rid)
        row = rows[rid]
        status = "excluded" if rid in EXCLUDED else "unresolved"
        if row["status"] != status:
            raise ValueError("Continuation decision differs: " + rid)
        ring.update(status=status, existence=status, investigation_deferred=False)
        proof = change["proof"]
        paths = ["README.md", "accepted_ledger.json", "classification_updates.json",
                 "verification_summary.json", proof]
        if rid in EXCLUDED:
            paths += ["new/quadratic_obstructions/MORITA_REDUCTION.md",
                      "new/quadratic_obstructions/REDUCTION_AUDIT.md",
                      "new/rank16_dual/RELATIVE_FACTORIZATION.md",
                      f"new/quadratic_obstructions/{rid}_dual_tensor.json",
                      "new/quadratic_obstructions/commutant_completeness_receipt.json",
                      "new/rank16_dual/verify_subcategories.py",
                      "new/rank16_dual/subcategories_receipt.json"]
            ordinary = rid in {"R10_1_114", "R10_1_115"}
            paths.append("new/rank16_dual/ORDINARY_DESCENT_AUDIT.md" if ordinary
                         else "new/pseudo_psu_central_fermion_audit.md")
            ring["summary"] = (
                "No complex fusion categorification exists. The forced Morita dual and relative factorization reduce the problem to "
                + ("two ordinary-factor swap descents: one has fusion multiplicity two, and the other has invertible group C2×C2, incompatible with this ring's C4."
                   if ordinary else
                   "a central fermion in a pseudo-PSU(2)6 factor. Its odd-evaluation rank-two superfusion quotient is excluded by the published finite superpentagon calculation.")
            )
            scope = {"general_status": "excluded",
                     "level_status": {k: "excluded" for k in ("general", "pivotal", "spherical", "pseudo_unitary", "unitary")},
                     "strongest_excluded": "general", "same_category_implications": [],
                     "existence_implications": [], "notes": [ring["summary"]],
                     "audit_sources": [evidence(proof, "General complex exclusion proof")],
                     "braided": {"status": "excluded", "explanation": "General complex nonexistence also excludes braided categorifications.",
                                 "sources": [evidence(proof)]}}
            findings = [ring["summary"], "The categorical proof and the exact finite reconstruction have independent agent audits; independent human verification remains pending."]
            if not ordinary:
                findings.append("The final finite superpentagon exclusion is imported from Chang–Chen–Xu, Section 3; their unrestricted rank-two classification conjecture is not used, and their calculation was not independently rerun here.")
        else:
            paths += ["new/case189/POINTED_ASSOCIATOR.md", "new/case189/MORITA_REDUCTION.md",
                      "new/case189/verify_structure.py", "new/case189/verify_pointed_associator.py",
                      "new/case189/verify_morita_reduction.py", "new/case189/pointed_associator_receipt.json",
                      "new/case189/morita_reduction_receipt.json", "new/case189_pointed_associator_independent_audit.md",
                      "new/case189_morita_independent_audit.md"]
            ring["summary"] = "General complex categorifiability remains unresolved. The pointed subcategory must be untwisted Vec(C5), the regular-algebra Morita dual must have the same fusion ring, and no braided categorification exists. These restrictions provide neither a model nor a general exclusion."
            scope = ring["categorification_scope"]
            scope["notes"] = [ring["summary"], "A pseudo-unitary Galois conjugate exists conditionally on categorifiability; this does not assert pseudo-unitarity of the original category."]
            scope["braided"] = {"status": "excluded", "explanation": "Schopieray's irrational braided generalized-near-group classification excludes the noninvertible dimension 2+√5.",
                                "sources": [evidence(proof), {"label": "Schopieray, Theorem 3.6", "url": "https://doi.org/10.4153/S0008439523000334"}]}
            findings = [ring["summary"], "The pointed-associator theorem rules out every nonzero H³(C5,C×) class.",
                        "Based-ring equality of the Morita dual does not imply a tensor equivalence or a central lift.",
                        "The necessary twist orders divide 1600. Surviving integer Gram data are not categorical models."]
        ring["categorification_scope"] = scope
        active = evidence("accepted_ledger.json")
        ring.update(source_file=active["path"], source_url=active["url"], model_reference_url=active["url"])
        ring["research"] = [
            {"title": "Current accepted case decision", "source": active["path"], "url": active["url"],
             "source_sha256": active["sha256"], "data": row},
            {"title": "Proof and remaining scope", "source": RELEASE + "/" + proof,
             "url": evidence(proof)["url"], "source_sha256": evidence(proof)["sha256"],
             "data": {"findings": findings}},
        ]
        # Keep the original tensor and sphericalization provenance; show current proofs first.
        previous = [r for r in ring["evidence"] if "/work/input_audit/" in r["path"] or "/work/general_signed/" in r["path"] or "/work/audit_signed/" in r["path"]]
        ring["evidence"] = [evidence(p) for p in dict.fromkeys(paths)] + previous
    summary = payload["summary"]
    summary["baseline_ledger_sha256"] = ledger["baseline_ledger"]["sha256"]
    summary.update(continuation_release=RELEASE, ledger_path=RELEASE + "/accepted_ledger.json",
                   ledger_sha256=digest(ledger_path), ledger_url=evidence("accepted_ledger.json")["url"],
                   source_url=f"{REPO_URL}/tree/{ref}/{RELEASE}")
    summary["counts"] = {str(rank): dict(Counter(r["status"] for r in payload["cases"] if r["rank"] == rank)) for rank in (9, 10)}
    summary["totals"] = dict(Counter(r["status"] for r in payload["cases"]))
    summary["remaining_ids"] = [r["id"] for r in payload["cases"] if r["status"] == "unresolved"]
    archive = repo / "site/dist/downloads/Rank10_M1_Exclusions_20261023.zip"
    if archive.is_file():
        if "baseline_archive" not in summary:
            summary["baseline_archive"] = summary.get("archive")
        summary["archive"] = {"url": "./downloads/" + archive.name, "sha256": digest(archive), "bytes": archive.stat().st_size}
    write(path, payload)
    receipt_path = repo / "site/dist/data/rank9_rank10_m1_build.json"
    receipt = json.loads(receipt_path.read_text())
    receipt.update(counts=summary["counts"], ledger_sha256=summary["ledger_sha256"], continuation_release=RELEASE,
                   baseline_ledger_sha256=summary["baseline_ledger_sha256"])
    write(receipt_path, receipt)
    current = repo / "publications/rank9-rank10/paper/rank9-rank10.pdf"
    shutil.copyfile(current, repo / "site/dist/papers/rank9-rank10-m1.pdf")
    print("Rank-ten continuation: 136 exclusions, 57 unitary models, one unresolved.")

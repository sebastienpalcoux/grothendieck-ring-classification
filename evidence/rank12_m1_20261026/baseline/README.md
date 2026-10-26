# Rank 12, multiplicity 1: audited fourth continuation

Final accepted totals: **478 excluded, 151 unitarily realized, 3 unresolved**, among 632 supplied based fusion rings. No online revision was made.

The preceding 438 exclusions and 148 models were retained after a fresh audit of categorical premises, source data, criterion implementations, and exact tensor identifications. Of the preceding 46 unresolved rings, this continuation excludes 40 and realizes 3. It does not claim to resolve the remaining three.

New models: **R12_1_320, R12_1_419, R12_1_530**.
Unresolved: **R12_1_561, R12_1_623, R12_1_628**.

“New” means a newly recorded explicit realization in this project. It is not a claim of novelty up to tensor equivalence or of exoticness. Independent assistant-team proof reviews and separately implemented exact checks passed; independent human verification remains pending.

## Read first

- `report.pdf` and `report.tex`: the checked nine-page report, with proof explanations and precise limitations.
- `summary.json`, `ledger.json`, `ledger.csv`: authoritative current counts and all 632 decisions.
- `new_decisions.json`: every new decision, proof route, replay, independent audit, and all three complete model tensors with explicit basis maps.
- `unresolved_tensors.json`: exactly the three unresolved original tensors and their hashes.
- `round4/`: complete new proof notes, exact verifiers, certificates, and independent audit records.
- `prior_round/`: frozen previous continuation, including the earlier evidence and verifiers. Its historical counts are not the current ledger.

## Proof map

| Subject | Main proof | Independent audit |
|---|---|---|
| All baseline models | `round4/audit_models/findings.md` | `round4/audit_models/results.json` |
| Baseline exclusions | `round4/audit_exclusions/findings.md`, `round4/root/exclusion_scope_review.md` | associated exact receipts |
| D32: 16 exclusions, 2 models | `round4/d32/theory.md` | `round4/audit_models/d32_exhaustion_audit.md` |
| D48: 20 exclusions | `round4/d48/general_complex_exclusion.md` | `round4/audit_exclusions/audit_quotient_reconstructions.md` |
| Integral-Lagrangian criterion | `round4/root/integral_lagrangian_lemma.md` | `round4/audit_exclusions/audit_integral_lagrangians.md` |
| D144: 3 exclusions, 1 model | `round4/d144/new_morita_reduction.md`, `round4/d32/d144_assist/theory.md` | `round4/audit_models/d144_local_and_tensor_independent.json` |
| R332 exclusion | `round4/c6/R332_proof.md` | `round4/audit_exclusions/audit_R332.md` |
| Remaining quadratic cases | `round4/c6/theory.md`, `C3_central_lift.md`, `C3_regular_algebra_Morita.md`, `R623_central_semion.md` in that directory | `round4/audit_exclusions/audit_C3_central_lift.md` |

An earlier exploratory note incorrectly excluded every near-group quotient of type NG(G,2), |G|=8, without retaining the nonabelian groups. That assertion is corrected. No accepted classification relied on it. Historical exploratory scripts remain for provenance; only the final decision manifests and proofs govern the current ledger.

The D48 proof reconstructs possible quotient rings directly. It does not assume the supplied census is exhaustive. It also does not infer a C3 grading merely from a rank-nine dimension profile: the surviving quotient tables have trivial universal grading and are handled by a separate central-symmetry argument.

## Exact replay

Requirements: Python 3, NumPy, and SymPy. No internet or external repository is needed.

Run from any directory:

```bash
python /absolute/path/to/this/package/verify.py
python -O /absolute/path/to/this/package/verify.py --baseline
```

The verifier checks all current ledger decisions, all original input hashes, every coefficient of the three new model tensors, the exact unresolved list, CSV consistency, and the frozen previous package. It then replays the accepted new constructions, structural classifications, full quotient reconstructions, the independent Hom computations, and the new obstruction. The optional `--baseline` also replays the preceding continuation's complete integrated verifier.

All replay programs execute in a temporary copy, so the frozen evidence is not modified. New execution logs and receipts go into `verification/`. The checks use explicit exceptions and remain active with Python optimizations enabled. The theoretical proofs are essential: finite replay alone is not claimed to establish categorical existence or exhaustive applicability.

The copied new scripts received only relative-path adaptations, listed in `portability_adjustments.json`. The preceding package was not edited; `prior_snapshot_manifest.json` binds every file. `MANIFEST.sha256` covers the final delivered package, excluding regenerable execution logs.

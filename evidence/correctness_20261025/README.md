# Correctness revision — 25 October 2026

**The classification is unchanged: 1,433,022 general exclusions, 378 realized rings and ten unresolved cases among the 1,433,410 supplied rank‑3–11 tensors.** Rank two and the unrestricted lower-rank arguments are reviewed separately. Independent human verification and formalization remain pending.

[Current manuscripts](../../manuscripts/README.md) · [Public audit summary](../../docs/CORRECTNESS_AUDIT.md) · [Original audit evidence · ZIP](https://sebastienpalcoux.github.io/grothendieck-ring-classification/downloads/correctness-audit-2026-10-25.zip)

The audit starts from classification commit `8014c749c17ddd2ad3d1b99a4359d49a8be921c5` and census commit `a69cd7e10047a7d86f3f03a7c43cb52dbc73c2f0`. Its 11 main mathematical manuscripts totalled 657 pages. This release incorporates the corrections below; those audited page counts describe the input release, not the enlarged revised papers. Original logs, failed invocations and historical source identities are preserved. Passing finite arithmetic never supplies a missing categorical premise.

## Exact model arguments

| Ring | Identification now used |
|---|---|
| R6_2_143 | [Actual canonical module of the HI(C5) Q-system dual](rank6_r143_module_repair.md). Both duality branches are included; exact module equations force every coefficient. No numerical center recognition or multiplicity assumption. |
| R8_2_820, R8_2_869 | [Known tube blocks, every associative completion, actual third indicators and balancing](rank8-neargroup-exact-repair.md). The original numerical recognition of the unknown tube block is not used. |
| R8_3_721 | [Direct exact completion in 14 search nodes](r721-exact-completion-proof.md). Four duality branches leave one based-ring class, with no census-completeness premise. |
| R8_2_868 | [Exact full-center theorem and canonical-algebra argument](HI7_EXACT_CENTER.md). The generator matrix alone is not treated as a full tensor identification. |

The rank-seven manuscript also explains unitarizability of its three exact-associator imports through their dimensions 16, 28 and 16 and the solvability/unitarizability theorems. It does not claim the supplied gauges are orthonormal.

## Corrected code and reproducibility

- The direct cyclotomic criterion now enforces the commutativity hypothesis required by its proof. All 16 currently allocated inputs satisfy it.
- Native square-root and frame enumeration bounds are exact on their advertised domains, including endpoint handling. Current census bounds were already below the formerly faulty ranges.
- Corrected reusable native cache wrappers now check source bytes, compiler identity, flags and the executable digest, with locked atomic rebuilding. A cache's existence or timestamp alone is insufficient.
- The [corrected atomic-integer entry point](replay_atomic_integer.py) derives its terminal status and completed scopes from verified evidence. The older dated evidence copy remains frozen for existing certificates. Missing tests or a forged outcome are rejected. No current classification used the defective terminal branch.
- A corrected, separately versioned [R189 auxiliary branching table](verify_r189_pieri_branching.py) supersedes the old frozen auxiliary. The R36 verifier path, rank-eight headline and historical-stage wording are corrected. The EH1 even-half convention and specialized source references are clarified.
- The new rank-nine route supplies the two missing phase-three certificates and runs the accepted baseline and phases two–five. The earlier root dispatcher only runs phase five, with phase four added by its `--baseline` switch. Stored GAP/cohomology narrowing records are verified here; their fresh full regeneration is retained in the original audit archive.
- R920's exact completeness fallback shares the pseudo-Boolean discovery implementation. Its memory-limited independent eight-bit attempt remains incomplete and is not relabelled as a pass.

## Current commands

Restore the checksummed repository data and install the relevant requirements first. Every replay output directory below must be new.

```bash
python3 tools/restore_data.py
python3 tools/verify_audit_revision.py
python3 evidence/correctness_20261025/replay.py \
  --output-dir /tmp/exact-model-repairs
python3 -O evidence/correctness_20261025/validate_kernels.py \
  --output-dir /tmp/exact-kernel-controls
python3 -O evidence/correctness_20261025/validate_guards.py \
  --output-dir /tmp/exact-guard-controls
```

The model command runs all seven proof/auxiliary components in normal and optimized Python, independent completion controls, and both full near-group tensor transports. The guard and kernel commands are targeted exact controls, not another full census classification.

The all-phase rank-nine continuation is:

```bash
python3 evidence/correctness_20261025/replay_rank9.py \
  --output-dir /tmp/rank9-current-complete --frontier --jobs 2
```

The current-source complete rank-six exclusion campaign is:

```bash
python3 evidence/correctness_20261025/replay_rank6.py \
  --output-dir /tmp/rank6-current-complete --jobs 2
```

It checks every current exclusion certificate and both exact original post-loop checks. It retains the complete original raw stream and reruns each ordinary failed worker in a fresh reference-backend process. The eleven multiplicity-nine certificates bind immutable historical source trees: all eleven are replayed in those exact contexts, then transported by byte-identical current tensors and certificates. No historical hash check is weakened. The resulting complete composite is explicitly distinguished from a single successful invocation. It is distinct from model-constructor verification and the earlier historical campaigns. A failed first invocation is never described as a successful single run. The pre-revision audit's partly log-derived coverage and missing original raw rows remain disclosed in its original report.

## Completed correction receipts

[Source-bound revision](revision.json) · [Receipt index](validation/receipts.json) · [Complete correction replay outputs · ZIP](https://sebastienpalcoux.github.io/grothendieck-ring-classification/downloads/correctness-replay-2026-10-25.zip)

The current rank-six composite covers all 25,362 exclusion certificates: the complete original raw stream, seven full reference-backend retries and eleven exact immutable-source completion proofs. The original invocation and its retained failures remain in the archive; its separate continuation is recorded explicitly. The effective-coverage file is explicitly derived and is not presented as original raw execution. The rank-nine receipt covers the accepted baseline and phases two–five, including all 36 model transports. All seventeen model-repair runs and the targeted kernel, cache and terminal-guard controls pass. These execution statements retain the categorical dependencies and scope specified in their receipts.

## Scope of the evidence

The original audit report and detailed rank reports describe the audit before this publication revision; references there to unpublished proposals or unchanged repositories are historical statements. The ZIP preserves their exact original form. Current manuscripts and the source-bound correction manifest identify the applied revision. Corrected versions of modules also bound by historical evidence are supplied in `source_overrides/`; the original dated evidence files retain their exact bytes. Old manifests are not rewritten to accept changed code: historical proof programs retain the source contexts and data pinned by their original releases.

The audit does not regenerate the complete upstream census search, formally certify the mathematics, or independently reconstruct every associator in the cited literature. Its proof reviews, source checks, exact replays and negative controls found no current classification requiring reversal. The ten open cases remain open.

## Responsive public website

The Atlas and standalone census page adapt automatically at their existing addresses. The responsive revision passed 44 browser layout checks and seven interaction checks, including both ring views, menus, exact tables, model dialogs, orientation changes and navigation without JavaScript. [Browser receipt](validation/mobile-ui/receipt.json) · [Reproduction guide](../../site/RESPONSIVE.md). These are interface checks, separate from the mathematical replay.

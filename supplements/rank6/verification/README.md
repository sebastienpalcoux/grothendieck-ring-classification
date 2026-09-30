# Verification evidence

The authoritative status is in [`data/decisions.json`](../data/decisions.json)
and its derived [`classification_counts.json`](../data/classification_counts.json):
16,552 general exclusions, 54 realized rings and 6 unresolved rings.
The current finite-profile reductions do not add a general exclusion.

## Current exact reductions

The unified criterion factors restriction and low-word moments jointly,
then couples the resulting coefficients to twist types through ribbon
balancing. Each verifier reconstructs its stated finite domain and equations
from the source tensor. An exact profile obstruction only excludes that
profile; a surviving necessary witness is not a categorical model.

| Scope | Current evidence |
|---|---|
| Generic finite Gram domains | [Exhaustive controls](../research/round5/unification/domain_controls.json), [native/generic crosscheck](../research/round5/unification/native_1204_domain_crosscheck.json) |
| `R6_4_22`: rank-30 obstruction and complete rank-36 fusion/modular reconstruction | [Balancing certificate](../research/round5/fermion/R6_4_22_certificate.json), [full reconstruction](../research/round5/quartic_pair/R6_4_22_center_reconstruction.json), [source-bound replay](../research/round5/quartic_pair/replay_O.json) |
| `R6_4_91`: full fusion and modular reconstruction | [Certificate](../research/round5/quartic_pair/R6_4_91_center_reconstruction.json), [source-bound replay](../research/round5/quartic_pair/replay_O.json) |
| `R6_4_155`: six profiles and forced semion-centralizer low actions | [Main exact replay](../research/round5/m4_155/frontier_replay_optimized.json), [packet reconstruction](../research/round5/m4_155/packet_frontier.json) |
| `R6_4_629`: rank-30/rank-38 obstructions and unique rank-35 necessary modular datum | [Complete certificate](../research/round5/m4_629/modular_reduction_certificate.json), [source-bound replay](../research/round5/m4_629/modular_chain_replay_O.json) |
| `R6_5_1204`: complete reduction to 171 profiles | [Certificate](../research/round5/m5_1204/profile_certificate.json), [optimizer-free replay](../research/round5/m5_1204/exact_replay_optimized.json) |
| `R6_8_1660`: general reduction and complete actual-root/profile enumeration | [General replay](../research/round5/m8_1660_conductor/reduction_replay.json), [actual-root certificate](../research/round5/m8_actual48/certificate.json), [source-bound exact replay](../research/round5/m8_actual48/replay_O.json) |

The [frozen six-input manifest](round5/campaign_manifest.json) includes each
full tensor and its SHA-256. The [coverage file](../research/round5/coverage.json)
records all staged reductions, canonical commands and retained receipts.
The reusable orchestration command is:

```bash
python -O software/round5_replay.py --list
python -O software/round5_replay.py --check-receipts
python -O software/round5_replay.py --select controls
python -O software/round5_replay.py --select R6_5_1204,R6_4_629 --jobs 2
```

`--check-receipts` checks the explicitly listed file hashes, each retained
receipt's completion predicate and any hashes intrinsic to that receipt. It is
an inventory audit, not a mathematical rerun, and makes no claim about unlisted
dependencies. Pending bindings fail the audit. Ordinary replay executes the
selected verifiers under optimized Python, captures separate logs and fresh
receipts, restores retained receipt files, and requires explicit completion. Case steps are sequential, with a 15-minute per-command
deadline. A stopped command is incomplete; use `--jobs 1` for the largest case.

The [pointed-center control](../research/round5/unification/pointed_center_control.json)
checks nontrivial complex duality, and the
[`Rep(S3)` center control](../research/round5/unification/s3_center_control.json)
checks nonzero high-word coefficients and common coefficient/twist balancing.
They do not constitute a new all-model scan.

The [Fibonacci-center control](../research/round5/unification/conductor_support_control.json)
checks saturated conductor support, finite-representation moments and forbidden
root powers. The [aggregate control receipt](round5/control_replay/receipt.json)
records a fresh optimized replay of all thirteen declared shared checks.
The [subcategory projection controls](../research/round5/unification/subcategory_intertwiner_control.json)
construct the modular matrices and projection multiplicities from finite-group
character sums, including a rank-deficient projection. Full subrepresentation
subtraction requires the separate disjoint-column hypothesis.
The [saturated Bruhat control](../research/round5/unification/saturated_bruhat_control.json)
checks full induced character spaces and an actual Fibonacci center. Its
171-profile R1204 scan found no additional exact obstruction, as recorded in
the [discovery summary](../research/round5/m5_1204/exploration_summary.json).

The exact checks use explicit requirements and remain effective under
`python -O`. Stored separating rays and integral points are checked without
calling numerical optimizers. A budget stop, numerical infeasibility status,
failed eligibility hypothesis or surviving relaxation is never an exclusion.
The case directories record the actual hypotheses, bounds and replay scope.

## Accepted classification evidence

[`classification/`](classification/) contains the executed ordered sieve,
its per-ring outcomes, finite search budgets, stage counts and exact-checked
certificates. The source census is trusted at the pinned revision; byte
integrity and representative correspondence are checked here. Verification
does not independently enumerate the census.

The accepted continuation allocations in [`certificates/`](../certificates/)
are disjoint extensions of that catalogue. Their source-bound proofs, frozen
input manifests and original replay receipts are retained in
[`continuation/`](continuation/), [`round2/`](round2/), [`round3/`](round3/) and
[`round4/`](round4/). Alternative proofs and overlapping full-census criterion
scans remain evidence for their stated criteria, not additional allocations.
Historical reports keep the counts and inputs applicable when they ran.

To replay all accepted continuation certificates with numerical optimization
disabled, run from the package root:

```bash
python -O software/continuation_controls.py --jobs 3 --out verification/current/all_continuations.json
```

To replay the complete negative catalogue, use:

```bash
python -O verify.py --jobs 2 --out verification/current/full_recheck.jsonl
```

Neither complete replay is implied by a case-specific reduction check.
Use an explicit current output path to preserve historical receipts. The
[package README](../README.md) gives commands for the shared domain controls,
case reconstructions, ledger consistency and document builds.

## Consistency, documents and archive integrity

[`current/`](current/) holds regression and consistency receipts; each report
states its executed scope and inputs. Normal and optimized Python checks
cover explicit error handling, scope guards and mathematical controls.
[`release_summary.json`](release_summary.json) links the authoritative ledger
and retained classification evidence. The original summary is preserved as
[`original_release_summary.json`](original_release_summary.json).

Document compilation logs are under
[`document_build_logs/`](document_build_logs/). PDF layout and cross-reference
checks are separate from mathematical proof verification. The archive
manifest checks file integrity, not the validity of a theorem. Run
`python check_manifest.py` before generating new reports, since newly written
reports change the archive's bytes.

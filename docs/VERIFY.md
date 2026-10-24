# Reproduce the data and mathematical checks

<!-- current-audit-correction -->
**24 October audit correction.** R8_3_436 is unresolved for general complex
categorification; its unitary exclusion is retained. Rank eight through
multiplicity three now has 4,402 general exclusions, 93 models and five open
cases. With the rank-nine M2 continuation, the current project-wide total is
26 open cases. Earlier dated ledgers and replay receipts keep their historical
scope. [Correction and precise hypotheses](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/audit_20261024/README.md).
<!-- /current-audit-correction -->

## Current audit revision and structural filters

From the repository root:

```bash
python3 tools/verify_audit_revision.py
python3 tools/verify_current_publication.py --metadata-only
node site/tests/check_properties.mjs
```

The first command reconciles the single R436 correction, checks current
manuscript/download identities and all 26 open tensors, and recomputes exact
structural properties for every individual catalogue record. Metadata-only mode
checks identities and projections without repeating the exact property arithmetic.
Neither mode is a fresh replay of every categorical exclusion.

The automatic data workflow runs current publication checks and its separately
named mathematical controls. The predecessor's nested full-history run stopped
with disk exhaustion and supplies no new full-replay receipt. Historical replay
exports commit `111137a3e3ddf93be340b39c8a7c7b6ea94b844c` into a temporary
directory; it needs ample disk space and preserves the current checkout.
Inspect `python3 tools/replay_current_publication_ci.py --historical --plan`
before running it. A successful old scalar replay does not restore R436's
withdrawn general categorical premise.

The current rank-five complete replay remains the explicit command in its revised
guide. Its historical standalone verifier and bounded discovery driver have
the separately stated limitations.


<!-- current-high-rank-publication -->

**Current results · 24 October 2026.** Rank nine at exact multiplicity two has **2,033 general exclusions, 32 unitary models and 18 unresolved rings** among 2,083 inputs. The complete rank-nine census through multiplicity two contains 2,225 rings. The project now has **26 unresolved rings** across ranks six, eight, nine and ten. [Rank-nine M2 manuscript](../publications/rank9-m2/paper/rank9-m2.pdf) · [Current proofs and exact replay](../evidence/rank9_m2_20261024/README.md) · [All current manuscripts](../manuscripts/README.md) · [All open cases](https://sebastienpalcoux.github.io/grothendieck-ring-classification/unresolved.html).

<!-- /current-high-rank-publication -->

For the current audited checkout, run `python3 tools/verify_audit_revision.py`. Full historical replay uses `python3 tools/verify_current_publication.py --historical`, which exports the pinned pre-audit Git snapshot. Earlier stage-specific commands below apply inside their corresponding immutable archives, with their original hypotheses.

The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,506 general exclusions, 16 models and 5 unresolved cases. Every recorded model admits a unitary realization. The remaining rings retain unresolved status for general complex categorification; R8_3_436 retains its unitary exclusion.

The rank-seven multiplicity-five continuation addresses all 5,805 supplied exact-multiplicity-five rings: 5,804 general exclusions, 1 realization and 0 unresolved cases. The classification of the supplied census is complete through multiplicity 5. The new realization R7_5_5678 is Rep(AGL(1,7)).

> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.

The [coverage report](PREPUBLICATION_REVIEW.md) states which computations were
actually executed. Program success checks its declared algebraic conditions;
it does not establish unproved categorical reductions or coherence.

## Restore and validate

From the repository root:

```bash
python3 tools/restore_data.py
python3 tools/validate_release.py
python3 tools/render_publication_docs.py --check
python3 tools/render_readme.py --check
```

Restoration needs only Python's standard library, works offline and checks
SHA-256 for every part and reconstructed file. `--check` verifies existing
restored files. The validation commands check publication identities, data
partitions and generated pages; they do not replay all mathematical proofs.

## Unrestricted rank-four classification

The theoretical proof gives FPdim < 1000 and multiplicity at most 31 without a pivotality hypothesis. The [self-contained replay package](../supplements/rank4/unrestricted/README.md) enumerates all 1,692 rings below that dimension bound and verifies 1,677 exclusions and 15 models. From its directory, run `python3 supplementary/check.py`; `--deep` adds unpruned and independent small-box checks. Mathematical hypotheses are proved in the [unrestricted manuscript](../manuscripts/rank4/papers/companion.pdf). Exact computation does not replace independent verification of those arguments.

## Complete rank-four and rank-five checks

Rank four requires Python 3.10 or newer and a C++17 `g++` compiler:

```bash
python3 supplements/rank4/restore_certificate.py
python3 -m pip install -r supplements/rank4/requirements.txt
cd supplements/rank4
python3 verify.py --workers 4
```

Return to the repository root for the rank-five public replay. Its
[package guide](../evidence/prepublication_20261017/rank5/README.md) gives the
pinned Python dependencies and C++17 requirement.

```bash
python3 evidence/prepublication_20261017/rank5/replay.py --check-package
python3 evidence/prepublication_20261017/rank5/replay.py --jobs 2
python3 -O evidence/prepublication_20261017/rank5/replay.py --jobs 2
```

These are full checks of 889,530 rank-four classes and 40,999 rank-five classes.
The rank-five ledger is reconstructed and has its own source-bound digest.
Neither public route requires a private attachment.

## Complete rank-six route

**The portable complete-replay orchestrator has not been executed end to end.**
Its identity and rejection controls were tested. The executed campaign combines
25,355 passes in the initial full process with seven complete Python-backend
retries and two separate post-loop checks. The initial process's failed status
is preserved. This is not a single successful full run or an all-Python full
census replay. The [backend packet](../evidence/prepublication_20261017/rank6_backend/README.md)
records exact coverage, environment observations and matrix comparisons.

Use a fresh restored checkout, with no pre-existing native binaries beside
the rank-six C++ sources. In an isolated environment, from the repository root:

```bash
python3 -m pip install -r supplements/rank6/requirements.txt
python3 evidence/prepublication_20261017/rank6_backend/replay_complete.py \
  --repo . --output-dir NEW_DIR --jobs 2
```

`NEW_DIR` must be a new directory outside `supplements/rank6`. The wrapper runs
normal Python: complete FLINT verification, complete Python-backend retries
for every failure, then the original post-loop checks. It rejects incomplete
coverage, changed inputs and unexpected failures. Read the
[full replay instructions](../evidence/prepublication_20261017/FULL_REPLAY.md#rank-six-combined-replay)
for native-cache and environment details. The initial audited process did not
capture its loaded backend/version; the installed Flint version changed during
execution, so no uniform measured runtime is claimed.

## Upper-rank and continuation checks

In a GitHub clone, use the isolated-context launcher:

```bash
python3 tools/replay_current_publication_ci.py --historical
python3 -O tools/replay_current_publication_ci.py --historical
```

The launcher checks the pinned scientific archive and all accepted inputs,
then runs the unchanged publication verifier in a temporary copy. Three
SHA-pinned discovery files retained in the clone are outside the frozen
proof inventory; their original paths and bytes are preserved. Unknown
additions or changed accepted inputs still fail. Use `--metadata-only` for
source, receipt, ledger and document checks, or `--historical --plan` to
validate the context and inspect the full command without running proofs.
The frozen portable rank-eight archives retain their direct verifier
commands; they already contain the exact accepted input context.

The `--historical` option replays the complete dependency chain with each
source-bound program run in its isolated compatible input snapshot. Omitting
it does not execute all constructor dependencies. Both commands verify the
current accepted decision inventory and source identities. They do not replace
the original full base-certificate loops described in the
[full replay guide](../evidence/prepublication_20261017/FULL_REPLAY.md).
Use normal Python for any checker whose proof checks use `assert`.

The [historical 38-case continuation](../docs/RESEARCH_STATUS.md) records **36 decisions among 38 cases**: 29 proposed general exclusions and 7 unitary constructions. Within that historical 38-case study, two questions remain open: `R6_4_155` and `R6_8_1660`. The historical residual program before the rank-eight M3 extensions records 140 decisions (120 exclusions and 20 constructions), all subject to independent mathematical verification.

The [inner-square rigidity package](../evidence/rigidity_20261017/README.md)
records the general `R8_2_24` obstruction and its source-bound finite checks.
Run `python3 tools/verify_rigidity_20261017.py` from the repository root for
that package. Cited mathematical theorems and categorical coherence remain
explicit proof obligations. External Normaliz or Groebner calculations are
not claimed to have been rerun.

## Individual rank-six checks

From `supplements/rank6`, the following check the named components:

```bash
python3 -O software/conformal_models.py --verify
python3 -O software/release_consistency.py
python3 -O software/replay_m9.py --jobs 2
python3 -O software/replay_m9_structure.py
python3 software/replay_m9_completion.py --output verification/m9/completion/replay_normal.json
python3 -O software/replay_m9_completion.py --output verification/m9/completion/replay_optimized.json
python3 -O research/exclusions/R6_5_1204/verify_exclusion.py
python3 -O software/frontier_replay.py --check-receipts
python3 -O software/frontier_replay.py --select R6_4_155
python3 research/frontier/new_research/replay.py
```

A receipt audit checks source hashes and completion predicates, not the
mathematics. The multiplicity-nine completion replay checks eleven standalone
certificates; all 8,809 exact-multiplicity-nine rings have general exclusions.
Necessary frontier reductions do not settle either rank-six open case.

From the repository root, replay the exact fermion and all-exponent
Minkowski certificates with:

```bash
python3 evidence/unified_20261016/rank6/verify_fermion_crossing.py --repo .
python3 evidence/rank6_laptop_20261002/all_p_minkowski/verify.py \
  --tensors supplements/rank6/data/unresolved_tensors.json
```

The [rank-six rigidity package](../evidence/rigidity_20261017/rank6/README.md)
checks the odd cyclic Clifford constraints, all indicator sequences and
phase-mass restrictions, including the exact 640-profile domain. Run:

```bash
python3 evidence/rigidity_20261017/rank6/run_checks.py --repo .
python3 -O evidence/rigidity_20261017/rank6/run_checks.py --repo .
```

These are necessary-condition checks. Both rank-six cases remain unresolved.

No timeout constitutes an exclusion. Component checks do not replace complete
base-certificate coverage.

## Historical base census import and publication exports

```bash
git clone https://github.com/sebastienpalcoux/fusion-ring-census.git
git -C fusion-ring-census checkout 2a340871242879665fa7ba2b01fa15b8bdeaada3
python3 tools/generate_counts.py fusion-ring-census/results/census.json
```

The [tensor crosswalks](PROVENANCE.md#tensor-crosswalks) compare based-ring
isomorphism classes at rank five and exact labelled tensor lines at rank six.
Count agreement alone does not establish tensor identification.

Refresh publication indexes from the authoritative ledgers with:

```bash
python3 tools/update_upper_rank_status.py
python3 tools/export_grothendieck_counts.py
python3 tools/render_readme.py
python3 tools/render_publication_docs.py
python3 tools/validate_release.py
```

An enumerated band is not classified until every record has been addressed.
Preserve the distinction between census, partial classification and complete
classification. Do not enter incomplete-band lower bounds as exact OEIS terms.
Archive identities must be updated only after rebuilding the corresponding
bundle. Source and document integrity checks do not replace mathematical review.

The rank-seven M5 extension is pinned separately to census commit `4e81914a6772ccd5aa2a2b5fe1b6e2cd06e2d700`. Its 5,805 new exact-multiplicity-five tensors and agreement with the earlier 4,201 tensors passed independent computational checks; exhaustive enumeration completeness relies on the supplied producer completion record. The optimized enumeration itself was not independently rerun.

To reproduce the new rank-seven import, check out that census commit and run:

```bash
git -C fusion-ring-census checkout 4e81914a6772ccd5aa2a2b5fe1b6e2cd06e2d700
python3 tools/import_rank7_m5_counts.py fusion-ring-census/results/census.json --commit 4e81914a6772ccd5aa2a2b5fe1b6e2cd06e2d700
python3 supplements/rank7/software/verify_m5.py
```

## Rank-eight multiplicity-three continuation

The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,506 general exclusions, 16 models and 5 unresolved cases. Every recorded model admits a unitary realization. The remaining rings retain unresolved status for general complex categorification; R8_3_436 retains its unitary exclusion.

The complete census is producer-reported, with independent tensor and isomorphism audits. The supplied optimized source matches both producer run receipts; full enumeration was not independently rerun. The normal and optimized mathematical replay receipts, individually investigated residuals and proof dependencies are in [`evidence/rank8_m3_20261021`](../evidence/rank8_m3_20261021). A candidate has neither a general exclusion nor a constructed associator; it is not an established exotic category. New arguments remain subject to independent human review.

```bash
python3 supplements/rank8/software/verify_m3_continuation.py --output frontier-validation/baseline_normal.json
python3 -O supplements/rank8/software/verify_m3_continuation.py --output frontier-validation/baseline_optimized.json
```

Metadata-only mode checks source identity and reconciliation with both full receipts, without repeating their finite mathematical checks.

## Further rank-eight frontier investigation

The historical frontier stage recorded 25 further general exclusions among the original 34 unresolved M3 cases. Subsequent construction and research stages, followed by the 24 October source-scope correction, leave five current rank-eight questions. The original M3 ledger, proof inputs and full receipts are unchanged. The current ledger is `supplements/rank8/output/audited_20261024/ledger.json`. The preceding exclusion ledger is retained as historical evidence.

Canonical normal and optimized frontier replays each passed all 108 checks. These receipts cover the historical frontier stage. Fresh replay after extraction from the publication archive is deferred.

Replay the original M3 package using the isolated outputs above, preserving its frozen receipts, then replay the continuation separately:

```bash
python3 tools/verify_rank8_frontier.py
python3 -O tools/verify_rank8_frontier.py
```

The new receipts bind accepted decisions and exact computations. The source-bound per-ring research inventory is `evidence/audit_20261024/per_ring_research_audit.json`. Construction-family exclusions and feasible necessary-condition witnesses have explicit scopes; neither establishes an exotic category.

## Generalized Haagerup construction and further restrictions

R8_3_721 is realized by the inherited 1+rho Q-system Morita dual of the C2 de-equivariantization of GH(C8). Exact rank and coefficient bounds identify its unique dimension type in the supplied complete rank-eight multiplicity-at-most-three census. The earlier center-action analysis leaves three necessary R8_3_1154 patterns. These results are in evidence/rank8_next_20261021/; the later R8_3_65 general exclusion is in evidence/rank8_research_20261022/.

The integrated rank-eight article includes the new construction and restrictions. Categorical arguments, targeted mathematical replay receipts and independent reconstructions are in `evidence/rank8_next_20261021/`. The original frontier ledger, audit and completed replay receipts remain unchanged.

The following commands validate the accepted overlay metadata; they do not repeat the targeted mathematical checks:

```bash
python3 tools/rank8_next.py --check
python3 -O tools/rank8_next.py --check
```

A separately reviewed Galois follow-up reduces the 36 retained R8_3_1154 pair histograms to 25 across the same three center patterns. Its proof and exact replay are in `evidence/rank8_postpublication_20261021/r1154_galois_review/`; the ring remains unresolved.

## General exclusion of R8_3_3472

R8_3_3472 admits no fusion categorification over the complex numbers. The sphericalization and Galois reduction covers general complex categories; complete center-frame and twist-orbit domains reduce the remaining case to 628 exact equations in 572 integer variables. A certificate of 1648 rational bound deductions and a final strictly positive separating gap proves infeasibility, with two independent exact checkers. The proof and reproducible certificate are in evidence/r3472_exclusion_20261022/. This complete obstruction supersedes the earlier feasible necessary systems and conditional Morita restrictions for R3472. R8_3_982 remains unitarily realized by the neutral triality component of the exceptional E21 chiral fusion category, with all 512 canonical fusion coefficients identified exactly. Apart from R8_3_436, four rank-eight general categorification questions remain: R8_3_928, R8_3_941, R8_3_1154 and R8_3_1768. Every hypothetical categorification of these four rings admits a spherical structure and has a pseudo-unitary Galois conjugate; none has a braided Morita representative. The R928 phase refinement leaves four of ten necessary center patterns, all fourteen R941 allocations survive the stated refinements, and R1154 retains its forced semionic data. R1768 has 39 of 40 necessary Gram/indicator branches excluded, while its final cone survives. These necessary data do not construct categories or settle the four remaining questions.

The complete center-domain reduction and exact infeasibility certificates are in `evidence/r3472_exclusion_20261022/README.md`. This accepted decision removes R8_3_3472 from the unresolved ledger. The earlier E21 construction and its research receipts retain their historical scope.

```bash
python3 tools/verify_rank8_exclusion_20261022.py
python3 -O tools/verify_rank8_exclusion_20261022.py
```

Use `--metadata-only` to check source identities and completed replay receipts. Use `--historical` to replay the preceding rank-eight stages in their preserved contexts. That replay explicitly records the reconstructed helper missing from the creative archive and its four revised cache-state diagnostics in a separate checkpoint; it also restores the omitted canonical tensor with its original receipt hash. The current ledger and proof have separate bindings from those historical releases.

# Mathematical review and verification scope

The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,504 general exclusions, 14 models and 9 unresolved cases. Every recorded model admits a unitary realization. The remaining rings retain unresolved status for general complex categorification.

The rank-seven multiplicity-five continuation addresses all 5,805 supplied exact-multiplicity-five rings: 5,804 general exclusions, 1 realization and 0 unresolved cases. The classification of the supplied census is complete through multiplicity 5. The new realization R7_5_5678 is Rep(AGL(1,7)).

> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.

The current manuscripts give one account of the classification and its open
questions. This guide states what the supporting review and computations
establish, and where mathematical verification is still needed.

## Mathematical scope

The [historical 38-case continuation](../docs/RESEARCH_STATUS.md) records **36 decisions among 38 cases**: 29 proposed general exclusions and 7 unitary constructions. Within that historical 38-case study, two questions remain open: `R6_4_155` and `R6_8_1660`. The combined residual program records 140 decisions (120 exclusions and 20 constructions), all subject to independent mathematical verification.

### Rank-six open rings

| Open ring | Established necessary restrictions | Remaining question |
|---|---|---|
| `R6_4_155` | A unique rank-26 modular candidate and a rank-22 based module; odd cyclic Clifford constraints pass on all 1,144 tested blocks, and the all-order path divisibility condition holds. | Coherent associators and module-category structures, or a general obstruction. |
| `R6_8_1660` | In the positive spherical representative, all indicator sequences and central phase masses are determined; eight spin objects form four dual pairs, and 640 labelled restriction-data profiles remain in branches 68, 286, 286. | A categorification or an obstruction covering every possible profile. |

For `R8_2_24`, the general-complex proof passes to a pseudo-unitary Galois
conjugate, forces the neutral indicators by saturated modular compression,
and excludes the required square root of an inner tensor functor. The proof
uses a simultaneous pivotal chart, short associator weights and finiteness
of tensor functors. Its [theoretical argument and independent AI audits](../evidence/rigidity_20261017/README.md)
are separate from the source and finite-weight checks.

The review examines general versus pivotal or pseudo-unitary scope, cited
hypotheses, sphericalization and Galois reductions, Morita constructions,
indicator constraints and root-order completeness. Further expert review
should especially examine coherence of inverse-Morita constructions, the
algebraic 2D2 arguments and the conductor-equality reductions. An AI review
cannot certify that every mathematical step is correct.

## Computational coverage

| Check | Executed scope | Result and limit |
|---|---|---|
| Rank three | Bounded near-group enumeration, `b<50` | Five reduced tuples; categorical proof reviewed separately. |
| Rank four | Two complete 889,530-ring replays, each regenerating 6,470,006 signed orbits; separate unsigned recount | Passed: 15 models and 889,515 exclusions. |
| Rank five | All 40,999 classes, 17 models and 40,982 exclusion certificates in normal and optimized Python | Passed; complete reconstructed ledgers are byte-identical. |
| Rank six | Model/import pipeline and all 25,362 exclusion certificates, followed by the two post-loop checks | Combined coverage passed; the initial full process failed on seven certificates, each of which passed a separate complete Python-backend replay. |
| Rank seven base certificates through multiplicity four | 4,201 records: 4,116 exclusions, 26 models and 59 cases deferred to continuation proofs | Passed in normal Python. |
| Rank seven multiplicity-five extension | All 5,805 new records: 5,804 general-exclusion certificates, 1 `Rep(AGL(1,7))` model and 0 open cases | Exact normal and optimized aggregate replays passed for the current ledger. [Normal receipt](../supplements/rank7/output/m5/replay_normal.json), [optimized receipt](../supplements/rank7/output/m5/replay_optimized.json). Enumeration completeness remains producer-reported. |
| Rank eight base certificates | 973 records: 832 exclusions, 60 models and 81 cases deferred to continuation proofs | Passed in normal Python, including signed proof trees. |
| Continuation chain and current inventory | Source identities, accepted decisions and dependency replays in normal and optimized Python | Passed within each program's stated scope; does not prove categorical coherence. |

The [full replay guide](../evidence/prepublication_20261017/FULL_REPLAY.md),
[coverage audit](../evidence/prepublication_20261017/reviews/verification_coverage.md)
and [current inventory receipts](../evidence/prepublication_20261017/current_history/receipt.json)
identify the exact inputs and executed programs. Continuation checks supplement
the base loops; they do not rerun every base certificate. An optimized run alone
cannot check assertions removed by Python's `-O` option.

## Rank-six environment and coverage

The [complete packet](../evidence/prepublication_20261017/rank6_backend/README.md)
records **25,355 initial passes plus seven complete Python-backend passes**,
exactly covering 25,362 distinct certificates. It also records the separately
executed post-loop counts and model registry and binds 299 source/input files.
This was a **combined verification campaign, not a successful single full run**.

The affected Galois-balance systems order some algebraic tuples by their string
representations. SymPy's Python and Flint backends can reorder or reverse these
equations, invalidating a positional Farkas vector for the other ordering.
Exact matrix comparisons establish equivalence; complete retries use the
unchanged checker with `SYMPY_GROUND_TYPES=python` set before importing SymPy.
The initial failed status and receipts remain in the packet. No inequality is
relaxed and a failed check is not counted as a pass.

The initial process did not record its loaded backend/version. The installed
Flint version changed from 0.8.0 to 0.9.0 during execution; no uniform measured
runtime is claimed. The portable complete-replay orchestrator has **not itself
been executed end to end**. Its identity, coverage and rejection controls were
tested. No all-Python full-census pass is claimed.

## Public reproducibility

The [rank-four replay](../supplements/rank4/PUBLIC_REPLAY.md) uses checksummed
public certificate parts. The [rank-five package](../evidence/prepublication_20261017/rank5/README.md)
reconstructs every class from recovered proof sources and pinned tensors;
the unavailable archive's ledger is not represented as recovered. Normal and
optimized replays independently produce the recorded reconstructed digest.
No private attachment is required for either public replay.

[Verification instructions](VERIFY.md) give executable commands.
[Provenance](PROVENANCE.md) records the exact ledger and archive identities.

## Rank-eight multiplicity-three continuation

The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,504 general exclusions, 14 models and 9 unresolved cases. Every recorded model admits a unitary realization. The remaining rings retain unresolved status for general complex categorification.

The complete census is producer-reported, with independent tensor and isomorphism audits. The supplied optimized source matches both producer run receipts; full enumeration was not independently rerun. The normal and optimized mathematical replay receipts, individually investigated residuals and proof dependencies are in [`evidence/rank8_m3_20261021`](../evidence/rank8_m3_20261021). A candidate has neither a general exclusion nor a constructed associator; it is not an established exotic category. New arguments remain subject to independent human review.

```bash
python3 supplements/rank8/software/verify_m3_continuation.py --output frontier-validation/baseline_normal.json
python3 -O supplements/rank8/software/verify_m3_continuation.py --output frontier-validation/baseline_optimized.json
```

Metadata-only mode checks source identity and reconciliation with both full receipts, without repeating their finite mathematical checks.

## Further rank-eight frontier investigation

The original 34 unresolved M3 cases now have 25 further general exclusions and 9 remaining questions. The original M3 ledger, proof inputs and full receipts are unchanged. The current ledger is `supplements/rank8/output/frontier_20261021/ledger.json`.

Canonical normal and optimized frontier replays each passed all 108 checks. Fresh replay after extraction from the publication archive is deferred.

Replay the original M3 package using the isolated outputs above, preserving its frozen receipts, then replay the continuation separately:

```bash
python3 tools/verify_rank8_frontier.py
python3 -O tools/verify_rank8_frontier.py
```

The new receipts bind accepted decisions and exact computations. The source-bound per-ring research inventory is `evidence/rank8_frontier_20261021/structural_models/per_ring_research_audit.json`. Construction-family exclusions and feasible necessary-condition witnesses have explicit scopes; neither establishes an exotic category.

## Further center-pattern constraints

A separately verified fourth-moment and center-action refinement excludes 2 of the four necessary center patterns for R8_3_721, leaving 2. For R8_3_1154, exact coordinate norm and interval bounds exclude 946 of 1,238 patterns, leaving 292. The surviving action matrices and patterns are necessary data only; no complete center fusion ring, associator or categorical model is constructed. Both source rings remain unresolved.

The integrated rank-eight article includes this separately verified addendum. Its proofs, complete pattern indices, necessary action matrices and independent reconstructions are in `evidence/rank8_center_followup_20261021/`. The original frontier ledger and audit remain unchanged.

The separate center-pattern addendum passed all eight checks in canonical normal and optimized Python, including independent arithmetic reconstructions and positive controls. Fresh replay after extraction from the publication archive is deferred.

```bash
python3 evidence/rank8_center_followup_20261021/verify.py --root .
python3 -O evidence/rank8_center_followup_20261021/verify.py --root .
```

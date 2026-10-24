# Mathematical review and verification scope

<!-- current-theoretical-retry -->
**Current results · 24 October 2026.** Rank ten at multiplicity one is complete:
136 general exclusions and 58 unitary models. R10_1_189 is recognized inside
the classical SU(4)_6 conformal-embedding module category. Ten cases remain
open at ranks six, eight and nine. Their new theoretical restrictions and
the actual twisted precursor for R8_3_1768 do not claim further decisions.
[Proofs and precise scope](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/unresolved_retry_20261024/README.md).
<!-- /current-theoretical-retry -->

<!-- current-high-rank-publication -->

**Current results · 24 October 2026.** Rank nine at exact multiplicity two has **2,043 general exclusions, 36 unitary models and 4 unresolved rings** among 2,083 inputs. The complete rank-nine census through multiplicity two contains 2,225 rings. The project now has **10 unresolved rings** across ranks six, eight and nine. [Rank-nine M2 manuscript](../publications/rank9-m2/paper/rank9-m2.pdf) · [Current proofs and exact replay](../evidence/rank9_m2_20261024/README.md) · [All current manuscripts](../manuscripts/README.md) · [All open cases](https://sebastienpalcoux.github.io/grothendieck-ring-classification/unresolved.html).

<!-- /current-high-rank-publication -->

The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,507 general exclusions, 16 models and 4 unresolved cases. Every recorded model admits a unitary realization. The four remaining rings retain unresolved status for general complex categorification. R8_3_436 has an independent general exclusion.

The rank-seven multiplicity-five continuation addresses all 5,805 supplied exact-multiplicity-five rings: 5,804 general exclusions, 1 realization and 0 unresolved cases. The classification of the supplied census is complete through multiplicity 5. The new realization R7_5_5678 is Rep(AGL(1,7)).

> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.

The current manuscripts give one account of the classification and its open
questions. This guide states what the supporting review and computations
establish, and where mathematical verification is still needed.

## Mathematical scope

The [historical 38-case continuation](../docs/RESEARCH_STATUS.md) records **36 decisions among 38 cases**: 29 proposed general exclusions and 7 unitary constructions. Within that historical 38-case study, two questions remain open: `R6_4_155` and `R6_8_1660`. The historical residual program before the rank-eight M3 extensions records 140 decisions (120 exclusions and 20 constructions), all subject to independent mathematical verification.

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

The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,507 general exclusions, 16 models and 4 unresolved cases. Every recorded model admits a unitary realization. The four remaining rings retain unresolved status for general complex categorification. R8_3_436 has an independent general exclusion.

The complete census is producer-reported, with independent tensor and isomorphism audits. The supplied optimized source matches both producer run receipts; full enumeration was not independently rerun. The normal and optimized mathematical replay receipts, individually investigated residuals and proof dependencies are in [`evidence/rank8_m3_20261021`](../evidence/rank8_m3_20261021). A candidate has neither a general exclusion nor a constructed associator; it is not an established exotic category. New arguments remain subject to independent human review.

```bash
python3 supplements/rank8/software/verify_m3_continuation.py --output frontier-validation/baseline_normal.json
python3 -O supplements/rank8/software/verify_m3_continuation.py --output frontier-validation/baseline_optimized.json
```

Metadata-only mode checks source identity and reconciliation with both full receipts, without repeating their finite mathematical checks.

## Further rank-eight frontier investigation

The historical frontier stage recorded 25 further general exclusions among the original 34 unresolved M3 cases. Subsequent construction and research stages, followed by the 24 October source-scope correction, leave four current rank-eight questions. The original M3 ledger, proof inputs and full receipts are unchanged. The current ledger is `supplements/rank8/output/research_20261024/ledger.json`.

Canonical normal and optimized frontier replays each passed all 108 checks. These receipts cover the historical frontier stage. Fresh replay after extraction from the publication archive is deferred.

Replay the original M3 package using the isolated outputs above, preserving its frozen receipts, then replay the continuation separately:

```bash
python3 tools/verify_rank8_frontier.py
python3 -O tools/verify_rank8_frontier.py
```

The new receipts bind accepted decisions and exact computations. The source-bound per-ring research inventory is `evidence/research_20261024/rank8_research_audit.json`. Construction-family exclusions and feasible necessary-condition witnesses have explicit scopes; neither establishes an exotic category.

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

R8_3_3472 admits no fusion categorification over the complex numbers. The sphericalization and Galois reduction covers general complex categories; complete center-frame and twist-orbit domains reduce the remaining case to 628 exact equations in 572 integer variables. A certificate of 1648 rational bound deductions and a final strictly positive separating gap proves infeasibility, with two independent exact checkers. The proof and reproducible certificate are in evidence/r3472_exclusion_20261022/. This complete obstruction supersedes the earlier feasible necessary systems and conditional Morita restrictions for R3472. R8_3_982 remains unitarily realized by the neutral triality component of the exceptional E21 chiral fusion category, with all 512 canonical fusion coefficients identified exactly. Four rank-eight general categorification questions remain: R8_3_928, R8_3_941, R8_3_1154 and R8_3_1768. Every hypothetical categorification of these four rings admits a spherical structure and has a pseudo-unitary Galois conjugate; none has a braided Morita representative. The R928 phase refinement leaves four of ten necessary center patterns, all fourteen R941 allocations survive the stated refinements, and R1154 retains its forced semionic data. R1768 has 39 of 40 necessary Gram/indicator branches excluded, while its final cone survives. These necessary data do not construct categories or settle the four remaining questions.

The complete center-domain reduction and exact infeasibility certificates are in `evidence/r3472_exclusion_20261022/README.md`. This accepted decision removes R8_3_3472 from the unresolved ledger. The earlier E21 construction and its research receipts retain their historical scope.

```bash
python3 tools/verify_rank8_exclusion_20261022.py
python3 -O tools/verify_rank8_exclusion_20261022.py
```

Use `--metadata-only` to check source identities and completed replay receipts. Use `--historical` to replay the preceding rank-eight stages in their preserved contexts. That replay explicitly records the reconstructed helper missing from the creative archive and its four revised cache-state diagnostics in a separate checkpoint; it also restores the omitted canonical tensor with its original receipt hash. The current ledger and proof have separate bindings from those historical releases.

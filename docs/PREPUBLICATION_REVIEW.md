# Prepublication review and corrections

**Review date: 17 October 2026 (Asia/Shanghai).** Research snapshot:
[`e6a36a6`](https://github.com/sebastienpalcoux/grothendieck-ring-classification/tree/e6a36a6f247b2db05f5468ffd4be1752ff42f157).

> [!IMPORTANT]
> **This is an AI review of AI-generated research.** The results, proofs, code
> and data have not yet been independently verified by human experts or
> formalized in Lean. They remain provisional. Successful computations do not
> prove the categorical reductions on which they depend.

This review separates mathematical arguments, computational replay, source
integrity and publication accuracy. The corrections below accompany the frozen
manuscripts and supplements; their original bytes remain available so that
earlier certificates and publication hashes can still be reproduced.

## Current disposition

**The review reopens `R8_2_24`.** Its claimed general exclusion contains an
unjustified decorated-phase cancellation. An eight-slot replacement has been
checked algebraically, but its mixed categorical transport identities have
not been established. It remains conditional research and contributes no
classification decision.

The current accepted continuation therefore records **35 of the 38 original
cases**: **28 proposed general exclusions and 7 unitary constructions**.
Three cases remain open: `R6_4_155`, `R6_8_1660` and `R8_2_24`.
Rank eight now has **895 exclusions, 77 models and one open case** through
multiplicity two; its complete contiguous range ends at multiplicity one.
Historical October 16 records of 36 decisions and complete rank-eight
classification are superseded by this dated correction, not erased.

## Dated corrections

### Rank three: induced-unit formula

In `manuscripts/rank3.tex`, Proposition `prop:near-group`, the sentence before
equation `eq:near-I1` should read

\[
(F\circ I)(\mathbf 1)=3\mathbf 1\oplus Y\oplus mX,
\]

instead of having two copies of the unit. Indeed,
`1² + Y² + X² = 1 + 1 + (1 + Y + mX)`.
The following decomposition and restrictions already use three copies, so
this correction does not change that argument or its conclusion.

In the same proposition, replace the reference to the Ng–Schauenburg formula
“in Section 3” with the explicit equation reference `eq:moments` (Section 4).

### Rank six: correct Galois-reduction dependencies

Two current manuscript passages refer to `prop:frontier-galois-pu`, a proposition
about `R6_3_215`, when discussing the different residual rings. The intended
dependencies are:

| Passage | Correct dependency |
|---|---|
| `manuscripts/rank6/papers/chapters/frontier_tensor_functors.tex`, common-field Galois conjugation | For `R6_4_155`, Proposition `prop:nonselfdual-neargroup-spherical`. For `R6_8_1660`, the unrestricted sphericalization reduction at the beginning of `subsec:frontier-1660`, with certificate `supplements/rank6/research/round4/m8/R6_8_1660_reduction.json`. |
| `manuscripts/rank6/papers/chapters/dimension_block_20261016.tex`, proof of the full twist-one support | The same unrestricted `R6_8_1660` reduction, followed by Lemma `lem:pu-tensor-functors`. |

The unrestricted signed reduction was rerun during this review. The reference
corrections do not resolve either residual categorification question:
`R6_4_155` and `R6_8_1660` remain open.

### Rank six: portable fermion replay command

The scratch-directory command in the frozen
`evidence/unified_20261016/rank6/RESEARCH.md` is not a repository entry point.
From the repository root, use:

```bash
python evidence/unified_20261016/rank6/verify_fermion_crossing.py --repo .
```

### Current and historical reproduction instructions

The rank-seven manuscript's verifier list omits several later scripts. Use
the aggregate current-stage dispatcher with the history flag:

```bash
python tools/restore_data.py
python tools/verify_review_20261017.py --historical
python -O tools/verify_review_20261017.py --historical
```

`--historical` is required to replay earlier stages. Without it, the latest
dispatcher does not run the historical constructor replays. The current
[verification guide](VERIFY.md) has been corrected accordingly.

The frozen `supplements/rank7/README.md` and `supplements/rank8/README.md`
describe the earlier theoretical stage, including its then-open counts.
They are not current classification summaries. Their direct old-stage commands
must be run against their historical snapshots, not the expanded current
ledgers. The current ledgers record 4,172 exclusions and 29 models at rank
seven, with no open cases in its stated bound. The October 16 rank-eight
ledger recorded 896 exclusions and 77 models; the present review retracts one
of those exclusions, leaving 895 exclusions, 77 models and one open case.

The compact rank-five excerpt also retains an older verifier that does not
dispatch the later inert-parity criterion. It must not be presented as a full
verification of the through-20 release. The [new complete replay package](../evidence/prepublication_20261017/rank5/README.md)
checks all 40,999 pinned classes, 17 models and 40,982 exclusions in both
normal and optimized Python. Its reconstructed decision ledger has a new
digest; the original historical ledger bytes were not recovered, and their
old digest is explicitly retained only as a historical reference.

The default upper-rank wrapper programs delegate to historical stage checks.
Such a run is not a fresh replay of all original certificates. This review
therefore runs the original full base-release loops separately, then checks
the later transitions with the current historical dispatcher. Normal Python
is essential for original checkers that use `assert`; an optimized run alone
does not check those assertions.

## Rank-six replay environment correction

The full replay exposed a portability defect in the frozen verifier: some
Galois-balance equations are ordered using string representations of algebraic
character tuples. SymPy's Python and Flint backends print those tuples
differently. This can reorder equations or reverse their orientation while
leaving the underlying exact system equivalent, so a saved positional Farkas
vector may fail against the differently ordered matrix.

The complete audit preserves the initial run and replays each failed complete
certificate with `SYMPY_GROUND_TYPES=python` **before SymPy is imported**,
restoring its historical equation convention.
Exact matrix comparisons establish the ordering issue; the affected complete
certificates are also replayed with the original, unchanged checker. The
initial failed receipts are retained beside the successful follow-up checks.
No inequality is relaxed, no failed check is counted as a pass, and no
classification decision follows merely from changing the backend.

## Mathematical review boundary

Separate AI review passes examined ranks two through eight, including general
versus pivotal or pseudo-unitary scope, cited theorem hypotheses, Galois and
sphericalization reductions, Morita constructions, indicator constraints and
root-order completeness. No definite counterexample was found in the arguments
reviewed. This is not a claim that every proof has been independently established.

The `R8_2_24` review found a specific failure in the claimed extension of
unitary diagram identities to a common composition-dual frame. The incoming
left-bend phase has the complementary index. Thus the condition `i=k` does
not imply the claimed cancellation without an additional phase relation.
The two decorated diagonal flips and the ensuing six-slot reduction cannot
be used as written.

A proposed repair keeps all eight even `D` coefficients and obtains the
required nonzero products from three column contractions. Its arithmetic,
unit-channel normalization and distinct forward/opposite index conventions
have been checked. The four mixed `B/C` trace transports still require a
proof that respects the skew self-duality of the invertible object and the
oriented crossing. Neither reciprocal-phase intuition nor a successful
symbolic expansion proves that step. Two separate AI reviewers therefore
recommend reopening the case. The conditional calculation is preserved for
further research, explicitly with **zero classification decisions**.

Other expert priorities include categorical completeness of the algebraic
2D2 argument, coherence in the inverse-Morita constructions, and the common
conductor-equality refinement. All classification labels on the public atlas
are the project's provisional research claims.

## Fresh computational review

| Check | Fresh scope | Result |
|---|---|---|
| Rank three | Independent enumeration in the bounded near-group reduction (`b<50`), plus proof review | Passed; five reduced tuples recovered |
| Rank four, original and current release | Two complete replays of all 889,530 rings; 6,470,006 signed orbits regenerated in each; independent full unsigned census recount and regression controls | Both passed; 15 models, 889,515 exclusions, zero open |
| Rank five, reconstructed current package | All 40,999 pinned classes, 17 model matches and 40,982 general certificates; normal and optimized runs | Both passed; fresh complete ledgers are byte-identical |
| Rank six | Original model/import pipeline; all 25,362 negative certificates; separately replayed post-loop counts and positive registry | Combined coverage passed: 25,355 initial passes plus 7 complete Python-backend passes; original run failed and is retained |
| Rank seven, full pre-stage-b baseline | All 4,201 records: 4,116 exclusions, 26 models, 59 then-open cases | Passed in normal Python |
| Rank eight, full pre-stage-b baseline | All 973 records: 832 exclusions, 60 models, 81 then-open cases, including imported signed proof trees | Passed in normal Python |
| Frozen unified continuation and history | 39 historical replay entries plus the prior update chain, in normal and optimized Python | Both passed; the R24 categorical gap is outside those arithmetic checks |
| Corrected current record and integrated history | R24 retraction, exact restoration of 26 parent files, all accepted decisions and the full historical chain | Both passed in normal and optimized Python; [fresh receipts](../evidence/prepublication_20261017/current_history/receipt.json) |
| Baseline GitHub CI | Complete fresh checkout of the audited baseline, including restoration, manifests, historical replays and site checks | Passed, run 38908254167, attempt 2 |

The [full replay guide](../evidence/prepublication_20261017/FULL_REPLAY.md)
explains how the original base loops and later transitions fit together.
The [verification coverage audit](../evidence/prepublication_20261017/reviews/verification_coverage.md)
documents the precise dispatch behavior. Historical computational success
for a withdrawn proof remains a computational result; it does not restore
the withdrawn classification decision.

The [rank-four public replay guide](../supplements/rank4/PUBLIC_REPLAY.md)
provides the exact certificate stream as checksummed repository parts.
The [rank-five reconstruction report](../evidence/prepublication_20261017/reviews/rank5_reproduction.md)
distinguishes recovered inputs, preserved proof modules, regenerated
certificates and the unavailable historical archive. Neither replay needs
private attachments.

The 610-file original unified source manifest is preserved with SHA-256
`aea53af376ee1622554e969a3d178b0c42124abd8da3eadc08d62cc5ee5cd851`.
The dated correction restores the historical parent for old-stage replay,
while the current status reflects the retraction. Source identity is not
proof of mathematical correctness.

The [rank-six coverage audit](../evidence/prepublication_20261017/rank6_backend/aggregate_summary.json)
passed with exactly 25,362 distinct certificates. The original full run exited
with seven failures; each affected complete certificate then passed the
unchanged exact checker under the Python backend. The two checks skipped after
the original failure gate also passed separately. The original failed stream,
all follow-up receipts and 299 baseline source/input bindings are retained.
This is a **combined verification campaign, not a successful single full run**.
The initial process did not capture its loaded backend/version, and the installed
Flint version changed during the run; no uniform measured runtime is claimed.
The new portable orchestrator has not itself been executed end to end; its
identity, coverage and rejection controls have been tested. See the
[complete packet](../evidence/prepublication_20261017/rank6_backend/README.md)
for the precise commands, evidence and environment limitations.

See also [research status](RESEARCH_STATUS.md), [verification instructions](VERIFY.md)
and [source provenance](PROVENANCE.md).

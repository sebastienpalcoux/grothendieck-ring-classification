# Deeper exact searches on the initial fifteen unresolved rings

This directory records the computational continuation of the 19 October
rank-seven multiplicity-five release. It does not itself modify the accepted
classification. The initial fifteen full tensors are pinned in
`source_frontier.json`; their original ledger has SHA-256
`508164c3f342f27988401e7c64e6efc83a844e5013a1d68f9b35c5124088c741`.

The earlier short-budget outcomes are preserved in `initial_diagnostics.json`.
Discovery used at most three concurrent workers with independent process-group
watchdogs, normally 1,200 seconds per attempt. A timeout, cancellation, missing
certificate, or numerical solver failure supplies no nonexistence conclusion.

## Complete, independently replayed certificates

| Ring | Complete proof tree | Oriented signed quotients |
|---|---|---:|
| R7_5_1964 | Ordinary induction moments in the character-induction wrapper | 52 |
| R7_5_4530 | Spherical dimension-order obstruction and oriented lifting | 4 |
| R7_5_4531 | Spherical dimension-order obstruction and oriented lifting | 1 |
| R7_5_5343 | Ordinary induction moments in the character-induction wrapper | 12 |
| R7_5_5623 | Ordinary induction moments in the character-induction wrapper | 40 |
| R7_5_5778 | Ordinary induction moments in the character-induction wrapper | 16 |

Each of the four induction cases exhausts 5,025 low Gram frames. Their
pseudo-unitary subproofs use ordinary moment obstructions; no character-label
or higher-twist constraint is needed in those subproofs. The complete
dimension-character and oriented-sphericalization trees supply general scope.
The original 60-second cutoffs had prevented these finite computations from
completing. The certificate files end in `_h6.json`; their discovery envelopes
retain the original candidate label. All six have passed independent normal
and optimized-Python exact replay and categorical scope review. Each separate
`_normal_replay.json` and `_optimized_replay.json` receipt binds its candidate
hash. They are integrated into the parent continuation ledger.

The independent replay command is, from the repository root:

```sh
python evidence/rank7_m5_20261020/computation/deep_campaign.py \
  --replay evidence/rank7_m5_20261020/computation/R7_5_1964_character_h6.json \
  --budget 1200
```

This runs the inherited exact checker in both normal Python and `python -O`,
disables numerical optimizers, and writes separate receipts binding the
candidate hash. It increases execution deadlines without changing the exact
tests. Replays use the original enumerators; the discovery accelerations below
are not required to accept these certificates. Final acceptance and current
status are recorded by the parent continuation ledger and review evidence.

## Discovery accelerations and partial evidence

`low_frames_fast.cpp` precomputes fixed suffix bounds and directly looks up
the last column instead of repeatedly scanning the same finite lists.
`gram_vectors_fast.{py,cpp}` extends the existing exact rational-range Gram
enumerator to six coordinates. `high_columns_fast.py` retains the original
dimension and integrality filters. The controls compare 36 low-frame and
24 high-vector enumerations with the earlier exact algorithms, across all
coordinate counts from one through six; see `acceleration_controls.json`.

`deep_campaign.py` checkpoints discovery results and, in later runs, exact
Farkas rays under `exact_rays/`. A reused ray must again pass the exact
integer inequalities for its complete system. Such partial rays are not
complete categorification exclusions. Search schedules and outcomes are
recorded in `wave*_tasks.json` and `results.jsonl`.

Complete raw signed-quotient enumerations are also supplied for R7_5_3895,
R7_5_4569, and R7_5_5039. The first has two quotients, both gauges of the
original; the second has only the original quotient; the third has four
commutative quotients, two gauges and two additional signed algebras. These
enumerations support the separate theoretical reductions and do not alone
exclude any of the three rings.

## Dual-variable elimination

`dual_reduction.py` avoids constructing the large dense rows that equate a
restriction variable with its dual. Discovery merges the corresponding pair
of columns; a variable whose dual was pruned is forced to zero. An exact
separating ray is then lifted back to the complete original row vocabulary.
Replay checks this full lifted integer ray against **every original retained
column**, using the two sparse entries of each duality row. It does not trust
the merged discovery matrix or call a numerical optimizer.

Normal and optimized-Python controls compare eight complete original dense
matrices, including 44 duality rows and two quadratic Galois rows, and exercise
four asymmetric pruning cases. The receipts bind the helper and inherited
mathematical source files. `dual_campaign.py` supplies independent process
watchdogs and source-bound result envelopes. A complete exclusion from this
experimental harness still requires full replay and scope review; a feasible
linear system or failed search is only a recorded inconclusive attempt.

## Refinement of the two remaining quadratic cases

`LOW_VERLINDE_AUDIT.md` checks the normalization of the low-center fusion
coefficients. The independent witness checker recomputes all 84 symmetric
triples directly from the exact character table, without using discovery
coefficient caches. It also checks all 49 restriction Gram and 49 normalized
S-row orthogonality entries. Normal and optimized Python pass for the frozen
R7_5_5039 necessary-data witnesses of center rank 28, and for R7_5_3895 low
frame 8 witnesses of ranks 40, 38, and 32. These are necessary-data examples,
not category models.

`FINITE_INTEGER_PROOF.md` explains the exact integer refinement for the
other R7_5_3895 low frame. Its lattice tests, residual-Gram pruning witnesses,
and sixteen complete integer-split trees replay without numerical solvers.
The trees contain 775 exact Farkas leaves. This removes the recorded low
frame after the separate source/completeness audit; the whole ring remains
unresolved because another low frame has feasible necessary data.

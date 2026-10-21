# R8_3_1154: three necessary center patterns remain

**The source fusion ring remains unresolved.** The results below exclude necessary center-data patterns; they do not produce or exclude a categorification of the source ring. The center calculations have pseudo-unitary scope and use the existing, separately verified reduction to that setting.

The independently reviewed chain is:

| Constraint | Patterns left | Pair-product histograms left |
|---|---:|---:|
| Frozen fourth-moment coordinate bounds | 292 | — |
| Complete joint fourth-moment fiber | 224 | 2,904 |
| Uniquely forced A2 action | 8 | 74 |
| Single-support induction trace | 4 | 37 |
| Full cyclic negative diagonal for pattern 3994 | **3** | **36** |

The final pattern indices are **6971, 8766, 8772**, using the immutable ordering in `evidence/rank8_frontier_20261021/central_integrality/integer_gram_1154.json`.

## Reviewed proof files

- `joint_quartic_fibers.py` / `.json` solve the simultaneous exact equations `M t = 0`, `sum(t_i^2) = alpha`, with all pair-product entries nonnegative integral. Every histogram is retained modulo permutation among identical restriction-column copies. The complete result has 68 empty fibers and 2,904 histograms on 224 nonempty fibers. Independent all-seven-coordinate transfer verification: `../review/r1154_fiber_review.py` / `.json`.
- `a2_action_probe.py` / `.json` fix the entire A2 action on every one of these histograms. The span of the vacuum, four distinguished simples, ten pair words, and eight forgetful rows has rank nine and is A2-invariant. Its characteristic polynomial is `x^4 (x+1)(x-3)(x+5)(x^2-270x+225)`. The complementary spectrum consists of zeros and either zero or three copies of −1. In the latter case integrality forces the unique projector `I_4-J_4/4` on the four high-type-10 copies. Exactly 2,830 histograms and 216 whole patterns are excluded by the resulting matrix entries. Independent proof using a full 23-generator Schur complement: `../r721/r1154_a2_review.py` / `.json`.
- `single_induction_trace.py` / `.json` exclude 3993, 6970, 8765, 8771. For the nontrivial invertible source simple `g=X3`, these patterns force `I(g)=2Z` for one central simple Z. Its nonzero twist trace contradicts `Tr(theta on I(g))=Dim(C) nu_1(g)=0`.
- `group1_all_triples.json`, produced by `joint_triple_after_a2.py --limit 1 --all-solutions`, records the **unique** complete triple histogram for pattern 3994. `group1_negative_diagonal.py` / `.json` verify an invariant rank-ten full cyclic span by moments through degree eight. On its unique high-type-0 coordinate, the fixed A4 diagonal is −2. The complementary A4 spectrum is `0` six times and `−2` once, so the actual diagonal is at most −2. Independent singleton-induction and complete negative-diagonal verification: `../r721/r1154_trace_diagonal_review.py` / `.json`.

`R1154_ADVANCED_CENTER_ADDENDUM.tex` gives the scoped manuscript statement and proofs. The accepted proof sources listed above are frozen.

## Complete triple census and further searches

These additional calculations record necessary-condition attempts. They add **no further whole-pattern exclusion** to the reviewed three-pattern conclusion.

- `joint_triple_after_a2.json.gz` contains all **365,671** exact triple histograms on the four patterns before excluding 3994. The four high-type-10 copies are constrained to have identical fusion-word coordinates, as their difference subspace carries the same distinguished joint eigenvalue tuple. `joint_triple_after_a2.summary.json` gives compact counts and both compressed and decompressed SHA-256 hashes. The decompressed JSON is intentionally not retained in the repository: it is 808,175,859 bytes; the exact gzip is 7,118,315 bytes.
- `low_action_bounds.py` / `.json` derive explicit matrices K3 and K4 on the final three patterns such that `N3=N1+K3` and `N4=−N1+K4`. Thus the four-action problem reduces to one symmetric integer matrix with bounds `max(0,−K3) <= N1 <= K4`, the known low columns, forgetful intertwining, and the specified joint spectrum.
- `bounded_high0_rows.py` / `.json` completely solve the resulting necessary individual-row problems for the small high-type-0 objects. These tests keep all 36 pair histograms. Applying their coordinate restrictions to the complete triple census leaves **258,875** triple histograms on the same three patterns. `bounded_high0_triple_filter.json` stores their indices in the compressed census. These are individual-row tests; they do not solve simultaneous symmetry and spectrum completion.
- `summarize_triple_archive.py` regenerates and checks the compressed-census summary and bounded-row filter. `triple_archive_review.json` records its replay.
- `symmetric_action_norm.py` / `.json` apply the full symmetric minimum-norm extension and integer rounding inequality for N1; all 36 pair histograms pass.
- `higher_moment_probe.py` / `.json` test scalar mixed vacuum moments in degrees 5–12; all 224 incoming patterns pass. `triple_projection.py` / `.json` and `triple_coupled_lattice.py` / `.json` record stronger fifth/sixth-moment coordinate and lattice bounds that likewise make no deletion. `joint_triple_fibers.py` supplies the exact augmented Gram construction used by the reviewed A2 calculation. `atomic_phase_probe.py` / `.json` record exact STS equations for actual twist sums, without asserting a complete twist assignment.

The unresolved mathematical step is the **simultaneous** bounded symmetric N1 completion with the full joint spectrum (and ultimately full center fusion/associativity data). Passing a row test, a Gram completion, or a twist-sum relaxation is not a model.

## Reproduction

Run from the repository root. The core scripts use rational/algebraic arithmetic and direct verification, not a numerical infeasibility decision.

```sh
python evidence/rank8_next_20261021/r1154/joint_quartic_fibers.py --all-solutions --output /tmp/r1154_joint_quartic.json
python evidence/rank8_next_20261021/r1154/a2_action_probe.py > /tmp/r1154_a2.json
python evidence/rank8_next_20261021/r1154/single_induction_trace.py > /tmp/r1154_trace.json
python evidence/rank8_next_20261021/r1154/group1_negative_diagonal.py > /tmp/r1154_negative_diagonal.json
python evidence/rank8_next_20261021/r1154/summarize_triple_archive.py
```

The complete triple enumeration can be regenerated with `joint_triple_after_a2.py --all-solutions --output /tmp/r1154_all_triples.json`. It is exhaustive and takes several minutes; use the compact verified archive for routine review.

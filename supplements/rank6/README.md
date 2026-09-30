# Rank-six categorification through multiplicity eight

The census contains **16,612 rings: 16,552 general exclusions, 54 realized
rings and 6 unresolved rings**. General categorifiability is completely
classified through multiplicity three; the exact multiplicity bands
**1, 2, 3, 6 and 7** are complete. This revision strengthens the necessary
conditions and finite reductions for the six remaining rings. It does not
claim a completed classification of them.

[Revised paper](papers/manuscript.pdf) ·
[Verification guide](papers/verification_guide.pdf) ·
[Decision ledger](data/decisions.csv) ·
[Model catalogue](data/model_catalog.csv)

| Exact multiplicity | Rings | Excluded | Models | Unresolved |
|---:|---:|---:|---:|---:|
| 1 | 39 | 18 | 21 | 0 |
| 2 | 154 | 132 | 22 | 0 |
| 3 | 384 | 381 | 3 | 0 |
| 4 | 872 | 866 | 2 | 4 |
| 5 | 1,582 | 1,580 | 1 | 1 |
| 6 | 2,768 | 2,765 | 3 | 0 |
| 7 | 3,814 | 3,812 | 2 | 0 |
| 8 | 6,999 | 6,998 | 0 | 1 |
| **Total** | **16,612** | **16,552** | **54** | **6** |

The realized rings have 53 unitary models and one spherical model with no
pseudo-unitary categorification. Through multiplicity three, 531 of 577
rings are excluded and 46 have spherical models. Every exclusion in the
table applies to complex fusion categories without an assumed pivotal,
spherical or unitary structure.

## Unified necessary criteria

Restriction multiplicities and coefficients of products of low central
objects must factor one joint integral Gram matrix. Its rational image and
exact quadratic bounds give finite domains for each possible coefficient
column. A common assignment of these columns and twist types must also
satisfy induction, character, rotation and ribbon-balancing equations.
This unifies previously separate moment and twist tests. Exact support,
subcategory projection and invertible-object constraints refine the same
system where their hypotheses apply.
Central projection to a fusion subcategory must intertwine both normalized
modular matrices. Individual column capacities and verified disjoint projection
rows refine the same finite system; the
[exact subgroup controls](research/round5/unification/subcategory_intertwiner_control.json)
include a projection whose rank is smaller than its target.

Saturation of the dimension-block bound gives further exact restrictions on
actual twist orders and moments of the finite modular representation. The
[complete Fourier checks](research/round5/unification/dimension_block_bound.json)
cover all six remaining inputs; the
[Fibonacci-center control](research/round5/unification/conductor_support_control.json)
checks the equality case and its forbidden twist roots.
A [prime-indicator criterion](research/round5/unification/prime_indicator_congruences.json)
also gives exact residue-wise indicator constraints for all four cases with a
proved full twist exponent.

The remaining cases now have the following exact reductions. Surviving
profiles, fusion tensors and modular data do not establish categorification.

| Ring | Current necessary alternatives | Evidence |
|---|---|---|
| `R6_4_22` | Center rank 36 with one necessary fusion/modular datum up to relabelling and complex conjugation. | [Frontier coverage](research/round5/coverage.json) |
| `R6_4_91` | Center rank 42 with a forced Ising factor; its rank-14 centralizer has one based-ring orbit and two compatible conjugate modular data. Center rank 36 is excluded. | [Complete reconstruction](research/round5/quartic_pair/R6_4_91_center_reconstruction.json) |
| `R6_4_155` | Six induction profiles, each with one forced pair of low fusion matrices in its semion centralizer. | [Exact frontier](research/round5/m4_155/README.md) |
| `R6_4_629` | Center rank 35 with one necessary fusion/modular datum up to conjugation and identical-column relabelling; ranks 30 and 38 are excluded. | [Certificate](research/round5/m4_629/modular_reduction_certificate.json), [exact replay](research/round5/m4_629/modular_chain_replay_O.json) |
| `R6_5_1204` | Exactly 171 retained induction profiles after the complete joint Gram and twist reduction. | [Certificate](research/round5/m5_1204/profile_certificate.json), [exact replay](research/round5/m5_1204/exact_replay_optimized.json) |
| `R6_8_1660` | Actual-root induction and congruence cuts leave three branches with 168, 798 and 798 necessary profiles; the center twist exponent divides 48. | [Complete actual-root certificate](research/round5/m8_actual48/certificate.json), [source-bound replay](research/round5/m8_actual48/replay_O.json) |

[Revision notes](REVISION_NOTES.md) explain the mathematical scope.
The [six-input manifest](verification/round5/campaign_manifest.json) freezes the tensors;
[criterion coverage](research/round5/coverage.json) records each staged reduction.
The [verification evidence guide](verification/README.md) distinguishes
exact reductions, surviving necessary witnesses and discovery calculations.

## Reproduce and inspect

Use the pinned Python requirements and a C++17 compiler. Rebuilding the
papers also requires `pdflatex`. Check archive integrity before generating
new reports:

```bash
python -m pip install -r requirements.txt
python check_manifest.py
python -O software/round5_replay.py --list
python -O software/round5_replay.py --check-receipts
python -O software/round5_replay.py --select controls
python software/release_consistency.py
python -O software/release_consistency.py
python build_papers.py
```

The receipt audit checks retained completion predicates and declared hashes;
it does **not** rerun the mathematical proofs. The controls command does run
fresh finite-domain and categorical checks, including nonzero word coefficients
in the center of `Rep(S3)`. To reconstruct selected frontiers, use
`python -O software/round5_replay.py --select R6_5_1204,R6_4_629 --jobs 2`.
Omit `--select` for all six frontiers and controls. Steps within a case are
sequential, with a 15-minute deadline per command; the largest case should
be run with `--jobs 1`. A timeout is incomplete and proves no exclusion.
These commands do not replay the entire negative catalogue. For all accepted continuation certificates, use
`python -O software/continuation_controls.py --jobs 3 --out verification/current/all_continuations.json`.
For the complete negative catalogue, use
`python -O verify.py --jobs 2 --out verification/current/full_recheck.jsonl`.
Neither larger replay is implied by this revision's case-specific checks.

`data/decisions.json` is authoritative. CSV exports, paper tables, counts and
`data/unresolved_tensors.json` are derived from it. General, pivotal,
spherical, pseudo-unitary and unitary existence are recorded separately.
The accepted certificate allocations and historical proof evidence are
preserved. Their frozen reports describe their original inputs and do not
define current status. An unfinished search or a feasible necessary system
changes no classification decision.

The census is inherited from the pinned
[Fusion Ring Census](https://github.com/sebastienpalcoux/fusion-ring-census/tree/b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726).
Its source is bundled for offline replay. The [OEIS directory](oeis/README.md)
is a local counting proposal, not an online submission. No claim beyond
multiplicity eight is made.

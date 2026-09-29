# Revision notes — fourth continuation, 29 September 2026

This continuation adds **4 general exclusions**, reducing the ten-case
frontier to **6 unresolved rings**. There are **16,552 general exclusions
and 54 realized rings** among the 16,612 census tensors. General
categorifiability remains completely classified through multiplicity three;
the exact multiplicity bands **1, 2, 3, 6, 7** are complete. The census, identifiers
and positive-model identifications are unchanged.

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

## Accepted general exclusions

| Tensor | General obstruction | Exact proof source |
|---|---|---|
| `R6_6_49` | Cyclic-three associator and center projection | [`research/round4/higher/R6_6_49_general.json`](research/round4/higher/R6_6_49_general.json) |
| `R6_6_1035` | Half-E6 center projection and twist-resolved masses | [`research/round4/higher/R6_6_1035_general.json`](research/round4/higher/R6_6_1035_general.json) |
| `R6_8_311` | Ising center projection and twist-resolved masses | [`research/round4/m8/R6_8_311_certificate.json`](research/round4/m8/R6_8_311_certificate.json) |
| `R6_8_3664` | Fibonacci center projection and cyclotomic subfield traces | [`research/round4/m8/R6_8_3664_certificate.json`](research/round4/m8/R6_8_3664_certificate.json) |

The canonical disjoint allocation is `certificates/continuation_round4.jsonl`.
The three preceding continuations retain their 7, 18 and 12 exclusions.
Alternative proofs are retained without double counting.

## Mathematical progress

A central object's projection onto a fusion subcategory retains its
twist. This gives necessary restrictions on individual induction columns
and exact twist-resolved dimension masses. Fibonacci, Ising, cyclic-three
and half-E6 subcategories give distinct refinements. Exact cyclotomic
subfield traces make larger conductors accessible without dropping the
character equations. Every accepted pseudo-unitary obstruction is combined
with its verified general reduction.

At multiplicity four, exhaustive Gram and Galois enumeration reduces
`R6_4_22` to three restriction profiles per character labelling, then
to two after word-multiplicity tests, and
`R6_4_91` to six, then to two by exact twist-system congruences
(center ranks 36 and 42). The corresponding reduction for `R6_4_629`
leaves five profiles, then three (ranks 30, 35 and 38) after exact
fixed-profile twist tests. These are finite necessary alternatives, not center fusion rings
or categorical models. For `R6_4_155`, fourth spectral moments,
integer-square inequalities and central-invertible transport yield a much
stronger exact surviving integral witness. None of these surviving systems
is counted as a categorification.

The new criteria are screened on all ten frozen residuals and all 54 known
positive rings. Eligibility, exact witnesses, numerical feasibility and
unfinished searches are recorded separately in the coverage report.

The manuscript proves twist-preserving subcategory projection and the
Fourier formula for twist-resolved masses. The new chapters also justify
complex low Verlinde products with duality, fourth spectral moments,
integral square cuts, finite restriction-profile enumeration and the
odd-conductor Galois-orbit divisibility criterion. The latter uses the
squared Galois action and is not asserted at even conductors.

Known-model searches remain separate from existence claims. All 61
constructors for the 54 known rings and 293 relative-center dimension
comparisons have been checked. Three tempting ADE or quantum-group Morita
models are ruled out by exact central-dimension mismatch. A mismatch with
these specific models is not a general nonexistence theorem.

## Verification and complete revision

`verification/round4/release_replay.json` records exact reconstruction of
every accepted new proof with optimized Python and numerical optimizers
disabled. The criterion directories retain independent audits, exact
surviving witnesses and controls. `research/round4/coverage.json` states the
actual scan domains and unfinished searches; they remove no rings.

The authoritative ledger, CSV exports, residual tensors, counts, paper
tables, manuscript, verification guide and current documentation are
regenerated. `software/release_consistency.py` checks their agreement in
normal and optimized Python modes. PDF compilation and visual checks are
separate from mathematical verification. The archive manifest covers every
file except itself, and every ZIP member is checked against it.

Earlier negative campaigns and their exact evidence remain unchanged; this
release does not claim to repeat the entire inherited catalogue. Earlier
revision notes are preserved in `provenance/`, including
`REVISION_NOTES_third_continuation.md`. Use the current ledger for status.

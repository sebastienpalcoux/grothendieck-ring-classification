# Rank-six categorification through multiplicity eight

This continuation adds **4 general exclusions**, reducing the ten-case
frontier to **6 unresolved rings**. There are **16,552 general exclusions
and 54 realized rings** among the 16,612 census tensors. General
categorifiability remains completely classified through multiplicity three;
the exact multiplicity bands **1, 2, 3, 6, 7** are complete. The census, identifiers
and positive-model identifications are unchanged.

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

The 54 realized rings have 53 unitary models and one spherical model with no
pseudo-unitary categorification. Through multiplicity three, 531 of 577
rings are excluded and 46 have spherical models, including 45 unitary models.
All exclusions in the table apply to complex fusion categories without an
assumed pivotal, spherical or unitary structure.

## Fourth continuation

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

[Revision notes](REVISION_NOTES.md) list the accepted proofs and their scope.
The input tensors are frozen in
[`verification/round4/campaign_manifest.json`](verification/round4/campaign_manifest.json).
See the [criterion coverage](research/round4/coverage.json) and
[research guide](research/round4/README.md) for the remaining cases.

## Reproduce and inspect

Use the pinned Python requirements and a C++17 compiler. Rebuilding the
papers also requires `pdflatex`. Check integrity before generating reports:

```bash
python -m pip install -r requirements.txt
python check_manifest.py
python -O software/round4_release.py --jobs 3
python software/model_catalog.py
python software/build_paper_tables.py
python software/round4_documents.py
python research/round4/coverage.py --require-canonical --output research/round4/coverage.json
python software/release_consistency.py
python -O software/release_consistency.py
python build_papers.py
```

The fourth-continuation checker disables numerical optimizers and
reconstructs each new accepted proof. Earlier source-bound evidence is
retained. To replay every continuation, run
`python -O software/continuation_controls.py --jobs 3 --out verification/current/all_continuations.json`.
To replay the complete negative catalogue, run
`python -O verify.py --jobs 2 --out verification/current/full_recheck.jsonl`.
These larger optional replays are not claimed to have been repeated here.

`data/decisions.json` is authoritative. CSV files, paper tables, counts and
`data/unresolved_tensors.json` are derived from it. General, pivotal,
spherical, pseudo-unitary and unitary existence are recorded separately.
The new allocation is `certificates/continuation_round4.jsonl`; all earlier
accepted certificate files remain unchanged. Historical reports retain
their original inputs and do not define current classification status.

The census is inherited from the pinned
[Fusion Ring Census](https://github.com/sebastienpalcoux/fusion-ring-census/tree/b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726).
Its source is bundled for offline replay. The [OEIS directory](oeis/README.md)
is a local counting proposal, not an online submission. No claim beyond
multiplicity eight is made.

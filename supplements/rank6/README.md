# Rank-six categorification through multiplicity eight

**12 further general exclusions reduce the unresolved frontier from 22 to 10.**
General categorifiability remains completely classified through multiplicity
three. The exact multiplicity bands now fully classified are **1, 2, 3, 7**.
The 16,612 census tensors, identifiers and 54 positive-model identifications
are unchanged.

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
| 6 | 2,768 | 2,763 | 3 | 2 |
| 7 | 3,814 | 3,812 | 2 | 0 |
| 8 | 6,999 | 6,996 | 0 | 3 |
| **Total** | **16,612** | **16,548** | **54** | **10** |

All exclusions counted here apply to complex fusion categories without an
assumed pivotal, spherical or unitary structure. The 54 realized rings have
53 unitary models and one spherical model with no pseudo-unitary
categorification. Through multiplicity three, 531 of 577 rings are excluded
and 46 have spherical models, including 45 with unitary models.

## The new continuation

The smallest previous multiplicity-four case, `R6_4_6`, is excluded by a
forced nontrivial cyclic associator and fourth-indicator support, combined
with Clifford stabilizer rotation. This also completes the uniform cyclic
order-four family throughout the census.

Further multiplicity-four exclusions use full-character cyclotomic traces,
Galois compatibility, and low Verlinde and restriction-product constraints.
An integer congruence refinement of the Morita equations strengthens the
higher stabilizer argument. Local dimension-field isolation and signed
Casimir saturation settle dense multiplicity-eight cases. A complete split
between commutative and noncommutative signed sectors resolves the remaining
noncommutative frontier. Each pseudo-unitary obstruction is used for a
general conclusion only after its signed Galois reduction has been proved.

[Revision notes](REVISION_NOTES.md) list each accepted proof and its scope.
The complete input domain is frozen in
[`verification/round3/campaign_manifest.json`](verification/round3/campaign_manifest.json).
The [coverage report](research/round3/coverage.json) distinguishes full-census
scans, tests of the 22 residuals, model controls, surviving relaxations and
unfinished searches. A necessary-system witness is not a categorical model.

## Reproduce and inspect

Use Python with the pinned requirements and a C++17 compiler. Rebuilding the
PDFs also requires `pdflatex`. Check integrity before generating reports:

```bash
python -m pip install -r requirements.txt
python check_manifest.py
python -O software/round3_release.py --jobs 3
python software/model_catalog.py
python software/build_paper_tables.py
python software/round3_documents.py
python research/round3/coverage.py --require-canonical --output research/round3/coverage.json
python software/release_consistency.py
python -O software/release_consistency.py
python build_papers.py
```

The third-continuation release checker disables numerical optimizers and
reconstructs every accepted new proof. It retains the unchanged earlier
campaigns and their exact evidence. To replay every continuation, run
`python -O software/continuation_controls.py --jobs 3 --out verification/current/all_continuations.json`.
To replay the full inherited and extended negative catalogue, run
`python -O verify.py --jobs 2 --out verification/current/full_recheck.jsonl`.
Neither larger optional replay is represented as having been repeated for
this continuation.

`data/decisions.json` is authoritative. CSV files, paper tables and
`data/unresolved_tensors.json` are derived from it. General, pivotal,
spherical, pseudo-unitary and unitary existence are recorded separately.
The original campaign and earlier continuation certificate files remain
unchanged; the new allocation is `certificates/continuation_round3.jsonl`.
Historical reports retain their original inputs and dates and do not define
current classification status.

The census is inherited from the pinned
[Fusion Ring Census](https://github.com/sebastienpalcoux/fusion-ring-census/tree/b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726).
Its source is bundled for offline replay. The [OEIS directory](oeis/README.md)
is a local counting proposal, not an online submission. No claim beyond
multiplicity eight is made.

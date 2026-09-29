# Rank-six categorification through multiplicity eight

**General categorifiability is completely classified through multiplicity three.**
The last residual, `R6_3_215`, has no complex fusion categorification.
Among the 577 rings through multiplicity three, 531 are excluded and 46 have
spherical models; 45 have unitary models. The exception is Schopieray's
`R6_2_124`, which has a spherical model and no pseudo-unitary categorification.

[Read the revised paper](papers/manuscript.pdf) ·
[Verification guide](papers/verification_guide.pdf) ·
[Decision ledger](data/decisions.csv) ·
[Model catalogue](data/model_catalog.csv)

| Exact multiplicity | Rings | Excluded | Models | Unresolved |
|---:|---:|---:|---:|---:|
| 1 | 39 | 18 | 21 | 0 |
| 2 | 154 | 132 | 22 | 0 |
| 3 | 384 | 381 | 3 | 0 |
| 4 | 872 | 863 | 2 | 7 |
| 5 | 1,582 | 1,579 | 1 | 2 |
| 6 | 2,768 | 2,762 | 3 | 3 |
| 7 | 3,814 | 3,810 | 2 | 2 |
| 8 | 6,999 | 6,991 | 0 | 8 |
| **Total** | **16,612** | **16,536** | **54** | **22** |

This second continuation gives **18 new general exclusions** relative to
the preceding 40-residual release, leaving **22 unresolved tensors**.
The census contains 16,612 rings; its enumeration is inherited from the pinned
[Fusion Ring Census](https://github.com/sebastienpalcoux/fusion-ring-census/tree/b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726).
All exclusion claims counted above are general, without an assumed pivotal,
spherical, or unitary structure. The 54 models comprise 53 unitary realizations
and one spherical realization with no pseudo-unitary categorification.

## The completed multiplicity-three proof

The signed sphericalization calculation reduces every categorification of
`R6_3_215` to a pseudo-unitary Galois conjugate. The complete two-sided
involution-module calculation leaves two possible branches, both forcing
anticommuting left and right stabilizers on two simple objects. The new
Clifford-algebra rotation theorem then forces both third indicators to be -1.
The exhaustive central-induction calculation rejects every branch with 200
exact integral separating vectors. No identification of an unknown center
with a known category is assumed.

The general certificate is
[`certificates/stabilizer_rotation_215.json`](certificates/stabilizer_rotation_215.json).
Its proof and higher-dimensional extension are in Section 5 of the paper.
The historical rank-22 modular witness is retained as a feasible control for
the older necessary tests; it does not supply a categorification.

## New criteria at multiplicities four through eight

The same tensor-based criteria are applied throughout the frozen input domain:
40 inherited residuals, including every one of the 39 higher-multiplicity
residuals. The new arguments comprise stabilizer rotation in arbitrary even
cubic dimension, ambient cyclotomic traces for quartic fields, ramification and
signed Casimir bounds, biquadratic field/norm constraints, formal-codegree trace
ideals, and an all-orders quadratic Gauss bound. Full-census arithmetic scans
and all 54 established positive controls are retained with their precise scope.

[Revision notes](REVISION_NOTES.md) identify every new exclusion, proof source,
coverage report, and verification limit. Survival of a necessary relaxation,
ineligibility, or a stopped search is not counted as a model or an exclusion.
The next unresolved multiplicity is four.

## Reproduce and inspect

Use Python with the pinned requirements and a C++17 compiler for the finite
search helpers; rebuilding the PDFs also requires `pdflatex`. Run the integrity
check before generating new reports:

```bash
python -m pip install -r requirements.txt
python check_manifest.py
python -O software/continuation_controls.py --jobs 3
python software/release_consistency.py
```

The continuation checker replays both continuation files with numerical
optimization disabled. To replay the entire inherited and extended negative
catalogue, use `python -O verify.py --jobs 2 --out verification/current/recheck_O.jsonl`.
This larger optional command is not represented as having been rerun in the
present continuation.

To regenerate the second-continuation ledger from its exact proof sources:

```bash
python -O software/round2_release.py
python software/model_catalog.py
python software/build_paper_tables.py
python build_papers.py
```

`data/decisions.json` is authoritative. CSV files, paper tables and
`data/unresolved_tensors.json` are derived from it. General, pivotal, spherical,
pseudo-unitary and unitary existence are recorded separately. All tensor
identifiers and positive-model identifications are preserved.

The original campaign remains in `verification/classification/`; the first
continuation has its frozen 47-input domain in `verification/continuation/`.
The second continuation is frozen independently in `verification/round2/`.
The new accepted proofs are in `certificates/continuation_round2.jsonl`, separate
from the unchanged original and first-continuation certificate files.
Historical research reports describe the state when they were produced and
are superseded for current status by the decision ledger.

All classification data can be read and replayed offline from the bundled
census source. Discovery can be much more expensive than exact checking.
The [OEIS directory](oeis/README.md) is a local counting proposal, not an online
submission. No claim about multiplicities beyond eight is made.

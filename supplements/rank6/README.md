# Rank-six fusion rings

## Categorification criteria and models through multiplicity eight

A unified study of **16,612 fusion rings**, using the complete rank-six data from
[Fusion Ring Census](https://github.com/sebastienpalcoux/fusion-ring-census).
The paper combines general necessary criteria, exact exclusion certificates,
and full-tensor identification of categorical models. The source census is
trusted as the counting input; this package does not repeat its enumeration.

[**Read the paper**](papers/manuscript.pdf) ·
[Verification guide](papers/verification_guide.pdf) ·
[Decision ledger](data/decisions.csv) ·
[Model catalogue](data/model_catalog.csv)

| Exact multiplicity | Fusion rings | Excluded | Models | Unresolved |
|---:|---:|---:|---:|---:|
| 1 | 39 | 18 | 21 | 0 |
| 2 | 154 | 132 | 22 | 0 |
| 3 | 384 | 380 | 3 | 1 |
| 4 | 872 | 855 | 2 | 15 |
| 5 | 1,582 | 1,577 | 1 | 4 |
| 6 | 2,768 | 2,762 | 3 | 3 |
| 7 | 3,814 | 3,807 | 2 | 5 |
| 8 | 6,999 | 6,980 | 0 | 19 |
| **Total** | **16,612** | **16,511** | **54** | **47** |

The model column contains 53 unitary realizations and one spherical realization
with no pseudo-unitary categorification. All exclusion claims are general.
The closed-subring criterion cites the revised complete rank-five general
classification through multiplicity twenty. Since every rank-six tensor
here has multiplicity at most eight, this citation update does not alter the
rank-six decision ledger.

General categorifiability is completely classified through multiplicity two:
43 of the 193 rings admit spherical models, and 42 admit unitary models.
Schopieray's `R6_2_124` has no pseudo-unitary categorification. Higher
classification is partial. The paper's sequential exclusion table records the
additional effect of each stage and exposes the smallest unresolved
multiplicity. An unfinished search or a feasible necessary relaxation never
counts as a proof of nonexistence or a categorical model.
The dimension-order and character-induction stages first contribute new
top-level exclusions at multiplicity eight (one and four rings respectively).
The latest first contribution among these top-level stages is therefore at
eight. Nested certificates can use the same criteria earlier, and the data
do not determine whether new criteria will be needed beyond this range.

## The first unresolved ring

The general existence of `R6_3_215` remains undecided. The paper proves a
joint fourth-order product-Gram necessary condition and checks it automatically:
the formal rank-22 center witness survives. A Dong–Schopieray catalogue bound
excludes **braided spherical** categorification of this ring, whose
Frobenius–Perron dimension exceeds 168; it does not settle general existence.
The complete census is also compared with the Ng–Rowell–Wen rank-six ancillary
modular data, yielding no new model.

```bash
python research/m8_frontier/low_product_gram.py --check
python research/m8_frontier/premodular_bound.py
python research/m8_frontier/nrw_rank6_scan.py
```

The scripts reconstruct the numerical conclusions from tensors and exact
source data. Their certificates and reports distinguish a surviving necessary
system, a structure-specific exclusion and an actual categorical model.

## How the argument is organized

The seven sections cover results, census input, reductions, central induction,
module and Morita criteria, positive models, and certificate verification.
The same theoretical statements apply to full tensors at every multiplicity;
there are no ring-label exceptions in the obstruction functions.

`data/decisions.json` is the authoritative classification ledger. The CSV,
paper tables and `data/unresolved_tensors.json` are derived exports. General,
pivotal, spherical, pseudo-unitary and unitary existence are recorded separately.
The complete model catalogue includes source references and basis permutations.

## Reproduce the classification

```bash
python -m pip install -r requirements.txt
python check_manifest.py
python verify.py --jobs 2 --out verification/current/recheck.jsonl
python -O verify.py --jobs 2 --out verification/current/recheck_O.jsonl
python software/current_regressions.py
```

The verifier and discovery driver select SymPy's pure-Python polynomial
backend before importing SymPy. The archived exact Farkas vectors refer to
its canonical equation-row ordering; this selection also makes checks
reproducible when the optional python-flint package is installed globally.

To repeat the ordered classification discovery from the frozen source:

```bash
python software/import_repository.py
python software/classify.py --jobs 4
```

The machine-readable stage counts and actual outcomes are in
`verification/classification/stages.json` and `summary.json` in that directory.
`attempts.jsonl` records stopped searches and errors as diagnostics, never as
exclusions. The discovery command can be more expensive than checking stored
certificates.

Run the manifest check before writing new reports. Certificate checking uses
exact arithmetic and rejects missing branches, invalid witnesses and conflicting
statuses. Numerical optimization may propose a certificate during discovery;
it is disabled during negative-certificate checking. The verification guide
states the scope of the saved reports and the remaining research limitations.

To regenerate the derived tables and PDFs:

```bash
python software/release.py
python software/model_catalog.py
python software/build_paper_tables.py
python build_papers.py
```

## Source and scope

All import and classification commands run offline from the bundled
`data/rank6_tables.txt.gz` and pinned source record.

The census source is revision
[`b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726`](https://github.com/sebastienpalcoux/fusion-ring-census/tree/b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726).
It includes every duality type and noncommutative case and applies no
categorifiability filter. The compressed rank-six tensor SHA-256 is
`0138c6228dbb06b0861ad38b8dfe67fcd1fc829add80d441c34c09a1afb78675`.
The paper's existing tensor identifiers are preserved; the multiplicity-eight
stratum uses the same row-major ordering convention.

The [OEIS files](oeis/README.md) contain counting data and a local proposal;
no online submission is implied. Conclusions about all multiplicities above
eight are outside this finite dataset.

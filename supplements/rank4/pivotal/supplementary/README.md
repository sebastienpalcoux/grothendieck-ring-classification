# Verification guide

This supplement contains the bounded census, exact exclusion certificates,
and programs used in *Classifying Grothendieck rings of pivotal fusion
categories of rank four*. The mathematical arguments are in the unified
`manuscript.tex`; the computations implement its finite search and exclusion
criteria. Published existence results supply the categorifications of the
fifteen surviving fusion rings.

## Running the checks

Run commands from the package root, alongside `manuscript.tex` and
`supplementary/`:

```sh
python3 -m pip install -r supplementary/classification/requirements.txt
python3 supplementary/check.py --workers 4
```

This regenerates the census and certificates, replays them normally and under
Python `-O`, runs the regression tests and separate audits, reproduces the
successive exclusion stages, and checks the numerical data in the manuscript.
Python 3.10 or later and SymPy are required. Regeneration also requires a C++17
compiler. The optional `python-flint` package accelerates exact arithmetic.

To replay the supplied data without regenerating them, use:

```sh
python3 supplementary/check.py --verify-only --workers 4
```

Replay refreshes reports and logs but leaves the census and certificate ledger
unchanged. It requires no compiler. Add `--deep` to either command for the
unpruned census comparison, exhaustive small parameter boxes, and strict
dimension-boundary checks; these additional checks require a compiler.

The runner records commands, exit statuses and timings in `validation/` and
`verification_report.json`. It marks the report `running` before starting and
`passed` only after every requested check succeeds. Timings depend on the
machine. Every accepted equality, sign and integer floor is checked exactly;
rounded dimensions in the model table are only for display.

## Census and model data

`census/data/rings.jsonl` contains one record for each of the 8,977 fusion rings
in the dimension window. Its zero-based `id` is stable. The field
`tensor[i][j][k]` means the fusion coefficient `N_ij^k`, with unit index 0.
Tag `S` denotes self-duality; tag `N` denotes duality `(0)(1)(23)`.
Each record also contains parameters, multiplicity, an isomorphism fingerprint,
the Casimir characteristic polynomial, and a strict-dimension certificate.

For `B = sum_i N_i N_i^T`, the largest eigenvalue is `FPdim(R)`.
The four leading principal minors of `3600 I - B` must be strictly positive,
which is equivalent to `FPdim(R) < 3600` by Sylvester's criterion. Equality
at the dimension bound is rejected. The full census contains 8,883 self-dual
rings and 94 rings with a nontrivial dual pair.

`parameters.txt`, `counts.csv` and `rings.jsonl.gz` are derived views of the
same data. The verifier checks their agreement, including all 59 multiplicity
rows of the CSV. The uncompressed JSON hash is the portable data invariant;
compressed bytes can depend on the compression library.

The enumeration uses the two complete presentations in Section 5. Its generic
exact row reduction, early dimension rejection and exhaustive free-coordinate
loops are explained in `census/README.md`. `census/data/manifest.json` records
source and data hashes. The census has no external data dependency.

`classification/models.json` supplies the fifteen reference fusion rings.
`independent/independent_models.py` reconstructs them from separate rules and
checks explicit unit-preserving fusion-ring isomorphisms with the survivors.
The manuscript cites the constructions of the corresponding unitary fusion
categories; the finite comparison checks their fusion rules.
The stable machine identifiers `Rep_D10`, `Ad_SU2_6` and `Ad_SU2_7` correspond
to the displayed names `Rep(D_5)`, `PSU(2)_6` and `PSU(2)_7`; here `D_5`
has order ten and `PSU(2)_n` denotes the adjoint subcategory of `SU(2)_n`.

## Successive exclusion stages

The revised order puts spherical-character arithmetic before the published
rank-four family classifications. Each row counts rings excluded for the
first time at that stage.

| Stage | Excluded | Remaining |
| --- | ---: | ---: |
| Complete bounded census | --- | 8,977 |
| Rank-two fusion subrings | 1,676 | 7,301 |
| Formal-codegree d-number condition | 6,541 | 760 |
| Spherical-character arithmetic | 595 | 165 |
| Published rank-four families | 90 | 75 |
| Central induction | 60 | 15 |

All 8,962 exclusions have exact certificates. To reproduce a prefix of this
calculation, run the relevant command:

```sh
python3 supplementary/stages.py rank-two
python3 supplementary/stages.py d-number
python3 supplementary/stages.py spherical
python3 supplementary/stages.py families
python3 supplementary/stages.py central
python3 supplementary/stages.py models
```

Each command starts from the census, recomputes the selected stage and every
preceding stage, verifies the new certificates, and compares stage memberships
with the release ledger. It validates the fusion data and rejects duplicate or
missing records. Reports and remaining IDs are saved in
`validation/stages/<stage>.json`. No preceding report is required or trusted.
The `models` command also replays all fifteen model certificates;
`--all` runs the same full sequence. `--workers N` controls parallelism.

The published-family filter matches complete multiplication rules. It uses
the classifications cited in Section 2, together with the stated reduction
to pseudo-unitarity where needed. These categorical results are mathematical
inputs to the calculation.

The ledger `classification/results/certificates.jsonl` has one record per
census ID. `summary.json` and `survivors.json` are derived outputs. Replay
checks the supplied witness, coverage, stage memberships and model identities;
it need not rediscover the producer's first possible witness. The producer's
ordering only makes its output reproducible. The classification schema is 5.

## Spherical-character certificates

For each ring, the arithmetic stage examines every rational character orbit.
A certificate contains a separating generator, its irreducible factors and
one obstruction for every orbit. The tests are nonvanishing on simple basis
elements, equality on duals, integral norms of the required dimension ratios,
Ostrik's spherical inequality, and cyclotomicity of formal codegrees.
The witness kinds are `zero`, `duality`, `norm`, `spherical_first_moment`, and
`nonabelian_codegrees`.

The last test is equivalent to requiring all fields generated by the ratios
`D/f_j` to be abelian, where `D` is the candidate spherical global dimension.
Indeed, `sum_j 1/f_j = 1` implies `D = sum_j D/f_j`. Thus all these ratios
lie in an abelian extension if and only if all formal codegrees do, since `D`
is itself a formal codegree. Kronecker--Weber then identifies this with
containment in a cyclotomic field.

Production factors the Casimir characteristic polynomial and computes the
exact Galois group of each irreducible factor of degree three or four; lower
degrees are automatically abelian. A `nonabelian_codegrees` certificate stores
the offending factor as descending rational coefficients. Replay confirms
that it is an actual irreducible factor and that its Galois group is
nonabelian. The independent checker instead tests whether the factor splits
in the field generated by one root: in irreducible degree three or four,
normality of this root field is equivalent to abelianity of the splitting
field. The revised pipeline does not use the earlier formal-codegree
field-containment or degree-one prime-ideal tests.

For a character orbit that passes the arithmetic tests, a
`galois_global_dimension` branch checks that its global dimension and the
Frobenius--Perron global dimension have the same minimal polynomial. The
Galois-reduction lemma then permits the pseudo-unitary induction tests. All
other candidate spherical character orbits must be excluded separately.
The executable checks these arithmetic hypotheses and the finite induction
choices; the Galois and categorical theorems remain mathematical inputs.

## Central induction

The convention is `M[a,i] = [F(Z_a):X_i]`: center simples index rows, and
category simples index columns. The low part `L` consists of the rows meeting
`I(1)`. In the commutative rank-four case, their first entries are one. With
`d` the vector of simple Frobenius--Perron dimensions, the formulas are
`M.T*M = B`, `G = L.T*L`, `Q = B-G`, and `W = G*d`.

Each stored candidate vector is one low induction row. For compatibility,
the ledger keys `columns` and `column_counts` retain their names: they contain
the rows of `L` and the numbers of candidate rows for each formal codegree.
Permutations of rows with equal formal codegrees are identified. Every
remaining low-part choice requires a verified obstruction.

The local witnesses are `polynomial_row`, `third_indicator_row`,
`fourth_indicator_row`, and `involution_moment`, corresponding to the
second-, third- and fourth-indicator corollaries and the involution proposition
in Section 3. A fourth-indicator witness records the integer floor and the
strict positive gap. Replay checks both inequalities defining that floor
by exact signs at the Frobenius--Perron embedding. Boolean or noninteger floors
are rejected. A missing or null obstruction is never accepted.

The Gram identity supplies row bounds and the involution test. Residual Gram
entry or minor rejection and the global moment estimates used for the
theoretical dimension bound are not additional finite-stage filters.

S(2) is excluded using the non-self-dual second-indicator inequality; the
corresponding example in Section 3 gives the short calculation. R2 is excluded
by the fourth-indicator corollary. Its four recorded low-part witnesses have
floor 16 and positive gaps 108, 76, 44 and 44. The hand calculation in Section 3
uses the uniform lower bound `W_X >= 7+30*delta` and gives the contradiction
`44 <= 0`. The independent fourth audit also retains symbolic consistency
checks for a related family; the individual finite certificates suffice for
their actual census exclusions.

## Separate checks and their scope

The generator and replay share routines. The following additional checks use
different implementations where indicated:

| Program | Checks | Shared or mathematical inputs |
| --- | --- | --- |
| `census/verify_census.py` | Fusion axioms, distinct isomorphism classes, dimension certificates, hashes and derived data | Presentation and canonicalization utilities; coverage follows the exhaustive search in Section 5. |
| `independent/independent_central_audit.py` | Arithmetic and induction certificates using spectral adjugates, resultant norms, full integer boxes and all low-row products before symmetry quotienting; separate root-field splitting check for cyclotomicity | SymPy and the mathematical criteria; no production imports. |
| `independent/independent_fourth_audit.py` | Fourth-indicator polynomials and integer combination; R2 formal codegrees, low-weight bound, floor and every recorded fourth witness | Indicator and central-induction theorems; no production imports. |
| `independent/independent_models.py` | Model-rule reconstruction and explicit fusion-ring isomorphisms | Published existence of the categorical models. |
| `independent/unpruned_census_audit.py` (`--deep`) | Remove both dimension rejections, enumerate 95,842 classes and recover the same 8,977 by direct determinant expansion | Generic row reduction is reused. |
| `census/audit_small.py` (`--deep`) | Exhaust all 59,778 parameter assignments through multiplicity two and recover the same 27 classes | Presentations and canonicalization are shared; matrix products replace elimination. |
| `census/audit_boundaries.py` (`--deep`) | Strict integer dimension bounds from 5 through 12, including equality rejection | Presentations and canonicalization are shared; matrix commutation and direct determinant expansion replace elimination. |

These checks have complementary coverage; agreement of totals is not a proof
of completeness. They do not formalize the categorical arguments or construct
external associators. The regression tests in `tests/` check valid certificates
and deliberate corruptions, including omitted branches, false signs, false
floors and invalid model or stage identifications. Their reports record the
actual test counts and rejection messages.

## Manuscript data and builds

`model_table.json` records the displayed model names, references,
multiplicities and exact dimensions. `check_manuscript.py` compares these data
with the independent model report, checks census and filter totals, and checks
the sharp-bound polynomial arithmetic. It validates only the designated
numerical interfaces, not arbitrary mathematical prose.

```sh
python3 supplementary/check_manuscript.py --write
pdflatex -interaction=nonstopmode -halt-on-error manuscript.tex
pdflatex -interaction=nonstopmode -halt-on-error manuscript.tex
```

The principal command performs the data check automatically. Detailed logs
are in `validation/`; `verification_report.json` gives the complete result.

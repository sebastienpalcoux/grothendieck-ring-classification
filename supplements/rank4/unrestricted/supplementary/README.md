# Supplementary census and general-case classification

All computation needed by the general manuscript is contained here. The pivotal
package is neither imported nor needed. The mathematical proof of the uniform
bound and of every categorical criterion remains in the main manuscript; the
optional theoretical family supplement is not required.

## Reproduce everything

From the package root:

```sh
python3 -m pip install -r supplementary/classification/requirements.txt
python3 supplementary/check.py
```

A C++17 compiler (`g++`) with OpenMP is required. The tested environment is Python
3.13.5 and SymPy 1.14.0. No network access is used after dependencies are installed.
The optional `python-flint` module accelerates the same exact polynomial tests;
it is not required, and the recorded runs use the SymPy fallback.

The driver displays each stage and stores detailed logs in `validation/`. It
regenerates the ordinary census and its per-ring certificates, reconstructs the
classification ledger, freshly enumerates the signed cover, replays every
witness, reconstructs the model tensors, checks their positive dimension
characters, and regenerates the manuscript tables. It accepts no external
classification flag as a mathematical exclusion.

```sh
python3 supplementary/check.py --deep
python3 supplementary/check.py --engine python
```

The deep run also disables both ordinary-census dimension prunings, compares the
exact retained set using direct determinant expansion, tests all 59,778 parameter
assignments at multiplicity two, and executes the inherited signed-reference and
scalar-algebra regressions. The Python engine changes the **local** signed search;
the complete global signed enumeration still uses C++.

## The two scopes must not be confused

The complete **ordinary fusion-ring census** has D < 1000 and multiplicity at most
31: 1,692 rings, of which 1,642 are self-dual and 50 have a dual pair. Its
classification ledger records 1,677 exclusions and 15 models. The distribution
by exact multiplicity is `census/data/counts.csv`; these counts have a dimension
restriction and are **not** the unrestricted multiplicity census or OEIS counts.

The internal **signed-table cover** has absolute coefficient bound 31, without
imposing D < 1000 on the positive orbit. It enumerates 92,795 signed orbits,
rejects 90,510 by d-numbers and 68 by cyclotomicity, and retains 2,217. Exactly
1,182 retained signed orbits have a nonnegative representative; all 1,182
certificates are checked (1,173 exclusions and nine self-dual models). This broader bank supplies every needed compatible signed quotient. These are not the input counts for Table 2.

## Files and conventions

`census/` contains the standalone ordinary generator, tensor checker, complete
uncompressed and compressed tensors, parameter tuples, counts, and manifest.
`classification/` contains the general signed proof, full-census ledger, ordered
classification driver, exact checker, and reports. `model_table.json` is the
single source for the compact model table; `models/` retains the corresponding
parameter tuples and positive dimension vectors. `check_manuscript.py` checks
all counts and exact dimensions before writing `source/models.tex`,
`source/generated_filters.tex`, and `source/generated_census.tex`.

Every full-census record is assigned exactly one stage. The first three tests
are run directly on the input. The non-self-dual stage checks hypotheses of the
manuscript's unconditional reduction to seven pseudo-unitary candidates and the
S(2) obstruction. Later self-dual stages replay the supplied exact witness bank
under an explicit based isomorphism. Their order is fixed in `classification/classify.py`.
The stage counts describe that implemented pipeline, not a claim that all
possible earlier obstructions have been found for every later record.

## Verification limitations and provenance

Every mathematical inference still relies on the proved necessity of its
criterion. Computational checks do not formalize the categorical proofs or
construct associators. Independent model reconstruction checks the published
fusion rules and basis identifications, not the underlying existence papers.

The ordinary census algorithm is adapted from the user-supplied pivotal package
with its bounds changed to the general theorem's range and its data regenerated
locally. Its complete branch proof is included as Appendix A of the general
paper. The classification criteria and signed-cover code remain those of the
general manuscript. See `provenance.json` for input archive hashes. The original
source license and notice are preserved.

Cached or ledger-only modes are explicitly conditional and never selected by
`check.py`. Reproduction writes new timing reports; the delivered release hash
manifest should be checked **before** regenerating files.

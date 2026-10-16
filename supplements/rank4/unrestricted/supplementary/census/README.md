# Complete ordinary rank-four census below D < 1000

Appendix A proves completeness, including every zero-coefficient branch and the
basis-isomorphism reduction. No precomputed ring list is an input. The executable
supports 1 <= M <= 31 and 5 <= D <= 1000; its fixed-width integer arithmetic is
restricted to that range. The Python verifier uses arbitrary-precision integers.

From the package root:

```sh
python3 supplementary/census/generate.py
python3 supplementary/census/verify_census.py --regenerate
```

At the default M=31 and D=1000 the strict dimension test retains 1,692 rings:
1,642 self-dual and 50 with a dual pair. `data/rings.jsonl` contains every full
4-by-4-by-4 multiplication tensor, in the convention R[i][j][k] = N_ij^k.
Its compressed form is a derived copy, not a substitute for the full data.
`data/parameters.txt` gives the ten- or six-parameter representations.
`data/counts.csv` gives the distribution by exact multiplicity with the duality
split. Its numbers are D-restricted, not unrestricted counts by multiplicity.

The canonical SHA-256 fingerprints use all unit-fixing basis permutations.
A record contains the exact leading principal minors of 1000I minus the Casimir
matrix and the Casimir characteristic polynomial. Its largest real root is D;
no floating approximation decides the strict inequality. `verify_census.py`
checks every tensor identity and representative distinction, and `--regenerate`
compares the regenerated parameter and tensor files exactly.

`audit_small.py` compares the optimized generator with direct matrix-commutator
checks on all 3^10+3^6=59,778 parameter assignments at M=2. The separate
`../independent/unpruned_census_audit.py` disables both dimension prunings, obtains
16,065 unrestricted multiplicity-31 classes, and uses direct determinant
expansion to recover the same 1,692 D-restricted classes. Shared components and
the limits of independence are stated in the manuscript and main guide.

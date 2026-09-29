# Spectral involution-module continuation

The general module obstruction from the manuscript is extended from fixed-point
sets of size at most two to size four by exact spectral pruning. It excludes
`R6_8_2945` and `R6_8_3071`, the only unresolved records with fixed-point sets
larger than two.

The new ingredient is exclusion of the full irreducible rational factor
containing the Perron eigenvalue: the anti-invariant action is entrywise bounded
by a proper principal submatrix of an irreducible regular fusion matrix.
Diagonal involution signs, parity of the characteristic polynomial, exact traces,
and exact squared norms then leave respectively four and zero generator matrices.

Run from the package root:

```sh
python software/new_module_spectral.py --verify research/module_continuation/spectral_module_exclusions.json
python -O software/new_module_spectral.py --verify research/module_continuation/spectral_module_exclusions.json
```

Discovery (the default restricts to previously untreated fixed sets of size at
least three):

```sh
python software/new_module_spectral.py --out research/module_continuation/spectral_module_exclusions.json
```

`spectral_module.tex` contains the general proposition, its proof, and compact
independent contradictions for both tensors. All computations use exact SymPy
integer/rational arithmetic and root-isolating rational intervals. There are no
assert statements or floating-point exclusion decisions.

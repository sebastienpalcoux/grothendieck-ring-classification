# Exact model data

`../model_table.json` controls the compact manuscript table, including the unitary
realization, multiplicity, exact global dimension, and construction reference.
`../classification/data/models.json` contains all fifteen full multiplication
tensors. `parameters.json` records the ten- or six-parameter tuple in that same
basis, its duality, and the displayed name. `dimension_vectors.json` records the
positive dimension vector in precisely that basis, not a sorted dimension list.

Run `python3 supplementary/check_manuscript.py` from the package root to recompute
all sixteen character identities for every model, verify positivity and the table's
exact global dimensions, and compare the generated TeX. Decimal fields are display
only. `independent/independent_models.py` separately reconstructs the fusion rules
and exhibits tensor isomorphisms. These checks do not construct or re-verify
associators; categorical existence is supplied by the cited literature.

Machine identifiers are stable internal names: `PSU2_6` and `PSU2_7` correspond to
the adjoint SU(2) models, and `pseudo_PSU2_6` to the principal even part of S'.
They do not denote additional rings. Old `F_{m,j}` labels in the model tensor bank
are historical aliases, never the IDs of the new census or exclusion criteria.

# Earliest residual: literature audit

The exact tensor of `R6_3_215` has positive dimension character
`(1,1,d,d,d-1,d+1)`, `d=4+sqrt(17)`, and global FP dimension
`136+32*sqrt(17)`. `premodular_bound.py` verifies all 36 dimension equations
using integer arithmetic in `Z[sqrt(17)]`.

Dong–Schopieray, *Near-integral fusion*,
[arXiv:2407.15955v1](https://arxiv.org/html/2407.15955v1),
Section 5.3, Figures 13–15, 17, 19, list rank-six premodular fusion rules.
Their scope includes a braiding and spherical structure. The finite list
implies the necessary bound `FPdim <= 168`; the certificate script gives
rational upper bounds for every listed family. Thus this residual has no
premodular model. This is **not** a general noncategorifiability result.
The table's caveat about counting braided equivalence classes for two
quantum-group families does not create additional fusion rules.

Ng–Rowell–Wen's current version is *Classification of modular data up to
rank 12*, [arXiv:2308.09670v2](https://arxiv.org/abs/2308.09670v2).
The ancillary `NsdGOL6.g` is pinned by SHA-256. `nrw_rank6_scan.py`
extracts 192 literal tensors in 20 Galois orbits, representing 11 based-ring
types, and compares the complete tensors under all 120 unit-fixed basis
permutations. None of the residual tensors in the current ledger matches, including
`R6_3_215`. The source's stated rank-12 completeness caveats do not concern
rank six. Matching modular data alone would still require a categorical
realization reference before recording a positive model.

Grossman–Izumi–Snyder,
[*The Asaeda–Haagerup fusion categories*](https://arxiv.org/html/1501.07324v1),
Section 3, describe the full higher Morita class. Their class has the same
global dimension as this residual, but dimension agreement supplies neither
a tensor isomorphism nor a Morita equivalence. A new argument placing the
residual in that Morita class would be required before the classification
could exclude it. The existing AH1 model in this package is a different
fusion tensor (`R6_6_1764`). No new unbraided model or general exclusion was
obtained from these sources.

To reproduce the finite audit from the supplied source bytes:

```sh
python research/m8_frontier/nrw_rank6_scan.py
python research/m8_frontier/premodular_bound.py
```

The first script uses the current residual ledger and records its coverage
automatically.
Neither script constructs a census or infers categorical existence from a
feasible relaxation.

# Model and literature audit for the third continuation

This audit began from the 22 residual tensors of the second continuation.
The exact input checksum and all per-ring results are in
`model_scope_scan.json`. No new positive model was established in this pass.
No equality of dimensions, character tables, or modular data is treated as
a categorical equivalence.

## Exact model comparison

`model_scope_scan.py` compares the complete tensors under all 120 unit-fixed
basis permutations. None of the 22 inputs matches any of the 61 registered
constructors representing 54 known positive rings. None matches any of the
192 rank-six tensors in the pinned Ng–Rowell–Wen ancillary source, which
represents 11 distinct based rings. The latter comparison is a modular
scope check, not an exclusion of arbitrary categorification.

The source is *Classification of modular data up to rank 12*,
arXiv:2308.09670v2, ancillary `NsdGOL6.g`:
https://arxiv.org/src/2308.09670v2/anc/NsdGOL6.g . Its SHA-256 is
`eeea55e0ae75982b0afcf7d8e936d7cb7d4adae7a42096e719d13b30974fab0b`.
The supplied bytes were rechecked before parsing; the GAP program is not
executed. A positive fusion-tensor match would still need a categorical
realization reference.

## Recent quadratic-family classification

Meng–Yu, *Classification of some Z/2Z × Z/2Z-quadratic fusion categories of
rank 6*, arXiv:2608.06064v1 (6 August 2026), explicitly leaves the three
rings R(2,2), R(4,4), R′(4) open in the discussion after Corollary 5.8.
Their new realization is R′(2), already present in the positive catalog as
R6_2_49. The exact tensor identifications computed here are:

| Family in that source | Census tensor |
|---|---|
| R(2,2) | R6_2_55 |
| R(4,4) | R6_4_174 |
| R′(4) | R6_4_155 |

The first two have already been excluded in this classification project;
that independent new work does not change what the source paper states.
The source's reference [16], on C4-quadratic rank-six categories, is listed
as in preparation. It is not an available classification theorem used here.
The primary PDF was retrieved from https://arxiv.org/pdf/2608.06064 and
checked in full text. The consulted PDF at https://arxiv.org/pdf/2608.06064 has SHA-256
`7c0fccd5a8ababc5bb7ec8b49c0309f1d41652626246cd43035e95435f5ebeda`.

## Scope of other recent classification results

Wang–Dong–Li, *The Grothendieck Ring of Strictly Weakly Integral Fusion
Categories of Rank 6*, arXiv:2609.23559 (20 September 2026), addresses
strictly weakly integral categories. Its primary abstract at
https://arxiv.org/abs/2609.23559 describes eight realizable rings and four
excluded candidates. All 22 input residuals in the present audit have
irrational global Frobenius–Perron dimension, as certified by the exact
minimal polynomials in the scan. Hence none satisfies that theorem's
weak-integrality hypothesis; it supplies no direct new decision here.

Dong–Schopieray, *Near-integral fusion*, arXiv:2407.15955v1,
https://arxiv.org/html/2407.15955v1 , Section 5.3, classifies rank-six
premodular categories. This is explicitly a braided spherical scope.
Its general near-integral results require a fusion subcategory of
codimension one in rank; the residuals here do not have such a subring.
Neither the premodular classification nor its finite lists is promoted to
a general categorification theorem. The earlier exact bounded
premodular and NRW controls remain applicable in their stated scopes.

## Reproduction and independent proof audits

```sh
python -O research/round3/models/model_scope_scan.py
python -O research/round3/models/c4_associator_audit.py
python -O research/round3/models/arithmetic_audit.py
```

The second script and its note independently audit the C4 pointed-associator
theorem. The third audits the new quadratic spectrum enumeration; its
companion note checks the inert local-field argument, the cubic local-factor
extension, and the noncommutative formal-codegree normalization. They are
separate from the exact exclusion-certificate replays.

# Integral rank-eight research record

This record concerns the two source tensors below. The final arguments exclude
complex fusion categorifications; neither tensor remains an exotic candidate.
The deductions and primary references are in `PROOF.md`; `manuscript.tex` is the
publication version. The old evidence directory is immutable. Historical
timeouts and unsuccessful filters are not counted as completed exclusions.

| Tensor | FP dimensions | Tensor SHA-256 | Final argument |
|---|---|---|---|
| R8_3_731 | 1,5,5,10,10,11,12,12 | ee54e287f01aec4e2079b7f66309d89a659742e38164a3e47de1fea650eec48b | Simple-center prime-power sieve, complete induction frames, exact joint rotation certificates |
| R8_3_3344 | 1,3,3,10,10,10,4,5 | af42e7282350264c21616caff6aeebd8d323b04b6c727b3c6230aad9933a7cf8 | Rep(A5) complement rigidity, Morita reduction, exhaustive relative A6/A5 twists |

## Common earlier attempts and their actual scope

The source-bound attempt history is
`evidence/rank8_m3_20261021/pipeline/residual_attempts.json`, with model records
in `models/model_search_attempts.json` in that old directory. Both tensors gave
no conclusion from the applicable rank-two, zero-spectrum, d-number,
integral-Drinfeld, cyclotomic, primitive-codegree, and central-twist-moment
tests. Some of these searches had stated bounds. Inherited character/modular
generator routines were ineligible; their absence of output is not a pass.
The old dimension-order runs timed out. The old tensor-rotation run timed out
for 731 and gave no conclusion for 3344.

Neither tensor matched the finite list of 72 explicitly constructed rank-eight
tensors. The bounded 1,505-model classical WZW dimension-ratio search produced
no lead; this was a numerical search, not an exhaustive quantum-group theorem.
Pointed and ordinary Tambara-Yamagami models are impossible by multiplicity.
The full adjoint ring and absence of nontrivial invertibles obstruct the stated
cyclic-prime extension/equivariantization Morita sources, without excluding
arbitrary fusion categories. These limited outcomes are superseded for the two
tensors by the complete arguments below.

## R8_3_731: completed exclusion

The ordinary finite-group search exhausts all 40 groups of order 660 and checks
the full fusion tensor for every degree match. Its sole rank/degree match gives
the control R8_3_724, not R8_3_731. The receipt is
`evidence/rank8_m3_20261021/performance/group_scan/per_id_attempts.json` and the
transcript auditor is `performance/group_scan/summarize_scan.py`.

The new proof uses integral hence pseudo-unitary categorification, simplicity,
and the known simple-center and prime-power theorems. A braided categorification
would either violate ENO's prime-power consequence or be an ordinary group
model. Therefore its center would be simple, and no nontrivial central simple
could have prime-power dimension. This is the induction strategy already
identified in Liu-Palcoux-Ren, Remark 5.15, now implemented completely for this
specific tensor; it is not a new claim of that underlying theorem.

The complete Gram-ellipsoid enumeration has 38,058 vectors. Its exact unit-row
and dimension filters, followed by complete row-sum/PSD enumeration, give 450
low induction frames. Duality excludes 434. The allowed high-column sets,
including the prime-power sieve, yield exact Gram Farkas certificates for 13.
The remaining three frames have exact joint rotation certificates through
order 6. Their systems have respectively 14,917, 11,207, and 17,249 variables.
The final verifier reconstructs all columns and frames and checks all integer
rays. It does not invoke an LP solver. The finite trace-pattern bound 19,800 is
not asserted to be a bound on the categorical exponent.

Canonical replay from the repository root:

```sh
python evidence/rank8_frontier_20261021/integral/verify_central_731.py
python -O evidence/rank8_frontier_20261021/integral/verify_central_731.py
```

Both lanes pass. The certificates are `central_731_sieve.json` and
`central_731_rotation_h6.json`. The separate independent audit reconstructs
the arithmetic without importing the producer; its receipts live in the
frontier `review/` directory. The earlier unitary-only exclusion is not the
basis for the new general-complex conclusion. No assumption that integrality
implies unitarity is used.

## R8_3_3344: completed exclusion and construction exhaustion

The old ordinary-group search exhausts all 162 groups of order 360, none of
which has the required rank. The earlier stable-relative-mu2 A6/A5 construction
produces the known positive control R8_3_3342. Its three dimension-10 square
diagonal coefficients are all 2, whereas those of 3344 are all 3. Originally,
this comparison excluded only that construction, not all possible twists.

The new argument first identifies the unique proper nontrivial subring with
Rep(A5). The complement is an indecomposable three-object Rep(A5)-bimodule with
both action matrices I,J,J,I+J,2J-I. Projective subgroup-module classification,
Goursat's lemma, and the Morita transform by Fun(A5) reduce all possibilities
to subgroup orders 3,12,48. The first gives a nonintegral rational FP dimension;
the last contradicts invertibility of a universal-grading component through
its nonnormal V4 stabilizer. The middle makes the Morita dual pointed. Thus
every categorification of this tensor would have to be group-theoretical.

All group-theoretical constructions are then exhausted: the center-invertible
constraint forces the ambient order-360 group to be perfect, the complete GAP
scan forces A6, and the subgroup/rank constraints force A5. The relative
cohomology calculation proves that there are exactly two admissible relative
classes, including the freedom of the subgroup cochain. It uses all 360 stable
conjugation conditions on a Sylow D8, the degree-two restriction, transfer,
and a separate 3-primary normalizer calculation. The trivial class has rank 9;
the nontrivial class gives the exact R8_3_3342 tensor. Neither realizes 3344.
This is a finite exhaustive construction obstruction combined with a theorem
forcing every hypothetical model into that family.

Canonical replay from the repository root:

```sh
gap -q evidence/rank8_frontier_20261021/integral/perfect_groups.g
python evidence/rank8_frontier_20261021/integral/structural_certificate.py
python -O evidence/rank8_frontier_20261021/integral/structural_certificate.py
python evidence/rank8_frontier_20261021/integral/a6_relative_cohomology.py
python -O evidence/rank8_frontier_20261021/integral/a6_relative_cohomology.py
python evidence/rank8_frontier_20261021/review/verify_relative_cohomology_independent.py
```

The GAP output matches `perfect_groups.json`; the normal and optimized Python
replays pass. The independent relative-cohomology verifier uses a separately
implemented permutation D8 and exact boundary-span arithmetic. The proof does
not assume that arbitrary integral or two-prime fusion categories are
group-theoretical. No stronger uniqueness theorem for the positive control
R8_3_3342 is claimed here.

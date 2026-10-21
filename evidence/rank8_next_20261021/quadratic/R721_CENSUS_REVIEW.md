# Independent exhaustive R721 census dimension review

The complete accepted census comparison passes a second implementation.
`review_r721_census.py` imports none of the producer modules. It independently
binds all 4,500 unique cumulative tensors to their unique historical IDs by
exact tensor hashes and verifies that all 973 earlier tensors occur unchanged
in their original order. Every tensor is included, across multiplicities
1/2/3 (96/877/3527 tensors) and all four duality strata
(2621/1278/516/85 tensors).

The constructed rank-eight dimension multiset is

`1,a,a,a+1,a+1,2a+1,2a,2a+2`, with `a=(3+sqrt(17))/2`.

Its sum is `theta=21+5 sqrt(17)`. For each tensor the reviewer forms the matrix
of multiplication by the sum of all eight basis elements. The target vector,
if it exists, must be a `theta` eigenvector. The complete screen independently
computes exact modular determinants at the two integral reductions
`(p,sqrt(17))=(1019,400)` and `(1021,494)`.

This is a necessary filter, not a numerical test: an integer polynomial
vanishing at `theta` also vanishes under every such reduction. The determinant
of the integer matrix minus `theta I` is such a polynomial. Therefore a
nonzero modular determinant excludes only the target dimension multiset and
cannot discard a matching tensor. All 4,500 determinant records are bound by
an aggregate digest in the receipt.

Both modular tests leave exactly `R8_3_2906` and `R8_3_721`. Their characteristic
polynomials are then checked for divisibility by `x^2-42x+16`. The normalized
eigenvectors are obtained independently by a rational 18-by-17 augmented
system: writing `d=u+v sqrt(17)` gives

`(M-21I)u-85v=0`, `(M-21I)v-5u=0`, `u_0=1`, `v_0=0`.

Only `R8_3_721`, source line 3222, has the required multiset. All 64 dimension
product identities and the global dimension `136+32 sqrt(17)` are checked
exactly. Its full tensor hash is
`76e26a815651476dfda5c2aa654f0d1327bdc890e08086cb6dbfe39ef9a1cdc5`.
The two spectral survivors and the unique final match agree with the producer
crosswalk. This reconstruction uses modular determinants and a doubled
rational field system rather than the producer's initial characteristic-
polynomial screen and quadratic-field elimination.

The scope is the complete **supplied** rank-eight census through multiplicity
three. This review does not rerun the enumeration that supplied the 4,500
tensors or replace its producer-reported completeness qualification. Given
that census and a separately constructed rank-eight category with the stated
dimensions and multiplicity at most three, it proves the unique based-ring
identification. The categorical construction is a separate argument.

Normal and optimized invocations passed with byte-identical output:

```sh
python evidence/rank8_next_20261021/quadratic/review_r721_census.py
python -O evidence/rank8_next_20261021/quadratic/review_r721_census.py
```

`r721_census_review.json` binds every source and the reviewer itself. The full
outputs are `r721_census_review_normal.txt` and
`r721_census_review_optimized.txt`. Every check uses an explicit exception,
so Python optimization does not disable verification.

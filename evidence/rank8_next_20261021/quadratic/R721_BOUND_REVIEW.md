# Independent review of the R721 dual multiplicity bound

The exact inequality certificate passes independent reconstruction. This
review imports none of the producer modules and takes its source tensor,
algebra object and rank-eight forgetful rows from
`../semion_fermion/construction/r721_bimodule_rank.json`.

The row order `[0,1,2,4,5,7,3,6]` gives dual dimensions
`1,a,a,a+1,a+1,2a+1,2a,2a+2`, with `a^2=3a+2`. The reviewer derives these
dimensions by dividing the exact source dimension of each forgetful object by
`FPdim(A)`, and checks the source dimension homomorphism and the entire free
bimodule Gram matrix.

Only the two repeated dimension pairs may be exchanged by duality; the other
four dimensions occur once. Thus there are exactly four duality cases. A
union-find implementation independently constructs all reciprocity/duality
orbits on the 512 tensor coefficients. The equations are then built in a
different order from the producer, with separate overlapping unit equations:
832 equations per case, from the unit, duality, exact dimension products, and

`I(X) tensor_A I(Y) = I(X tensor A tensor Y)`.

This identity is the direct bimodule identity
`(A X A) tensor_A (A Y A)=A X A Y A`. Its coefficients use the forgetful rows by
free-bimodule adjunction. No source commutativity or dual associativity is
assumed in generating these linear constraints.

| a-pair duality | b-pair duality | Coefficient orbits | Equality rank | Free variables |
|---|---|---:|---:|---:|
| Separate self-duals | Separate self-duals | 120 | 98 | 22 |
| Separate self-duals | Exchanged | 112 | 93 | 19 |
| Exchanged | Separate self-duals | 112 | 93 | 19 |
| Exchanged | Exchanged | 104 | 88 | 16 |

All four independently computed exact reduced row-echelon matrices have the
same canonical hashes as the producer's certified systems. For every orbit,
the saved rational covector y satisfies `y A >= e_j` entrywise and
`y b <= 3`. Hence `n_j <= y A n = y b <= 3` for every nonnegative solution of
`A n=b`. Every one of the 512 coefficients is covered, and the largest saved
bound is exactly 3 in each duality case. This proof uses exact rational
arithmetic, with no acceptance of numerical optimization statuses.

The scope is precise: **given the actual algebra and the separately established
rank-eight bimodule factor**, every possible dual fusion tensor has maximum
coefficient at most three. Q-system existence, exclusion of other dual ranks,
and uniqueness of the rank-eight census match are separate inputs and are not
asserted to have been independently proved by this review.

Normal and optimized invocations pass:

```sh
python evidence/rank8_next_20261021/quadratic/review_r721_bound.py
python -O evidence/rank8_next_20261021/quadratic/review_r721_bound.py
```

The source-bound receipt is `r721_bound_review.json`; the two full outputs are
`r721_bound_review_normal.txt` and `r721_bound_review_optimized.txt`.

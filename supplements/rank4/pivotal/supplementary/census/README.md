# Exact bounded rank-four census

Section 5 of the manuscript gives the two complete presentations and the
commuting-multiplication lemma. The reference
search uses generic exact linear algebra rather than case-specific formulas.
The principal guide is `../README.md`; `data/counts.csv` retains all 59
multiplicity rows. Stable representative conventions preserve every census ID.

## Reference algorithm

For each self-dual tuple `(b,c,d,e,f)` in `[0,M]^5`, reject it early if
`2+2*b*b+2*c*c+d*d+2*e*e+f*f >= D`. Indeed the corresponding Casimir diagonal
is this expression plus `a*a`, whereas every diagonal is at most the largest
eigenvalue `FPdim`. Section 4 supplies `D=3600` and `M=59` for the pivotal
classification. The census itself includes every abstract fusion ring in
this dimension window, without assuming categorifiability.

The first five self-dual equations are linear in `(a,g,h,i,j)` for fixed
`(b,c,d,e,f)`. `linear_box.hpp` performs exact fraction-free row reduction.
Inconsistent rows are rejected; every bounded integer assignment to the
original coordinates of nonpivot columns is enumerated, and pivot coordinates
are recovered by back substitution. A nonintegral or out-of-box coordinate is
rejected. All six original equations are checked again. Zero pivots and all
rank-deficient cases use the same generic procedure.

In a linear row `sum(q[k]*x[k])=r`, current integer intervals `[lo[k],hi[k]]`
give the necessary interval

    sum(min(q[k]*lo[k],q[k]*hi[k])) <= r
        <= sum(max(q[k]*lo[k],q[k]*hi[k])).

A failed interval rejects the branch. For a selected free variable, subtract
the interval of the remaining terms and use exact signed floor/ceiling division
to narrow its range. Assigned coordinates have singleton intervals; unassigned
coordinates initially range over `[0,M]`. Each intersection retains every
possible integer solution. No modular inverses, residue progressions or
ring-specific exceptional branches are used.

For a dual pair, loop directly in order `(c,d,e,f,b,a)`, testing each original
equation as soon as its variables are known. The last equation is checked at
`f`, the third at `b`, and the other two at `a`.

The self-dual representative convention first requires `b` to be minimal
among `b,c,d,f,h,i`, and then takes the lexicographically least tuple among
relabellings preserving that condition. This only fixes the representative;
all five-parameter tuples are searched. Exchanging a non-self-dual pair leaves
its six-parameter tuple unchanged.

For every final candidate, form `B=sum_i N_i*N_i^T` and require all four leading
principal minors of `D*I-B` to be strictly positive. Sylvester's criterion
(Horn--Johnson, *Matrix Analysis*, second edition, Theorem 7.2.5(b)) makes this
exactly equivalent to `FPdim < D`. A zero determinant is rejected. Fraction-free
elimination follows Bareiss (*Math. Comp.* 22 (1968), 565--578).

## Arithmetic ranges

The implementation accepts only `1 <= M <= 59`, `5 <= D <= 3600`.
Original linear coefficients have magnitude at most 59 and right-hand sides
at most 10443. By the column form of Hadamard's inequality, every minor of
order at most five in the augmented matrix has magnitude below `10^14`.
Products before exact Bareiss division therefore have magnitude below
`2*10^28`, safely within signed 128-bit integers. Back substitution and
interval sums have magnitude below `5*59*10^14`.

For the dimension test, entries of `D*I-B` have magnitude below 60000.
The minors of order at most three have magnitude below `1.2*10^15`,
so the largest intermediate products are below `3*10^30`; the final
order-four determinant is below `2.1*10^20`. Signed 128-bit arithmetic
therefore suffices. Tensor products and displayed equation evaluations
fit 64-bit arithmetic. The Python verifier independently recomputes all
final quantities with arbitrary-precision integers.

## Commands and checks

Run from the directory containing `manuscript.tex` and `supplementary/`:

```sh
python3 supplementary/census/generate.py
python3 supplementary/census/verify_census.py
python3 supplementary/census/verify_census.py --regenerate
```

The last command regenerates temporary data and compares both complete
parameter and fusion-data files. `supplementary/check.py --deep` also checks
all small-box assignments, strict dimension boundaries, and a full search
with both dimension rejection steps disabled. This last check retains the
generic linear solver and compares a separate Python determinant expansion;
it is deliberately not an independent proof of the search algorithm.

The C++ diagnostic options `--no-early-dimension` and `--no-dimension-filter`
are used by that deep comparison. Normal generation always enables both tests.
Disabling both tests takes several minutes and is not needed for the census.
Generator and replay have no external census dependency.

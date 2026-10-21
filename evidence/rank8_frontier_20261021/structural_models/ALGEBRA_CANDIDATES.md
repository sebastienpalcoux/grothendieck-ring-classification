# Complete algebra-object filters for the structural frontier

This extends the exact connected-algebra filter proved in
`../quadratic/CONNECTED_ALGEBRA_CANDIDATES.md` to R65, R439, R455, R567,
R901 and R1463. All conclusions apply to arbitrary complex fusion
categories. The search exhausts every possible underlying object of a
connected separable algebra; it does **not** solve algebra associativity,
construct its multiplication, or certify its existence.

For a connected separable algebra A, its regular right module is simple.
Writing `A=sum a_i X_i`, module rigidity and the positive module FP vector
give `a_0=1`, `a_i=a_(i*)`, and `0<=a_i<=floor FPdim(X_i)`. An invertible
g occurring in A fixes A on either side. Free right-module adjunction
gives an integral induction Gram matrix, with the row belonging to the
regular module equal to a. Consequently its residual after removing that
row is entrywise nonnegative and positive semidefinite.

## Noncommutative convention

We explicitly use right multiplication by A:

`G_ij = sum_k a_k N_(i,k)^j - a_i a_j`.

Adjunction gives the transposed indexing `N_(j,k)^i`; the two agree after
summing because A is self-dual. For example,
`Hom_A(X_i A,X_j A)=Hom(X_i,X_j A)`. The shared enumeration engine is fed
the **opposite** source tensor so its first-index multiplication computes
this convention. Both left and right invertible stabilization are checked
independently on every surviving object. All three noncommutative cases
are included; commutativity is never assumed.

## Completed finite domains

| Ring | All bounded self-dual vectors | Stabilization survivors | Entrywise Gram survivors | PSD Gram survivors |
| --- | ---: | ---: | ---: | ---: |
| R65 | 6,912 | 1,884 | 625 | 30 |
| R439 | 784 | 126 | 88 | 28 |
| R455 | 1,536 | 816 | 177 | 21 |
| R567 | 112 | 42 | 42 | 22 |
| R901 | 432 | 324 | 191 | 18 |
| R1463 | 23,328 | 11,772 | 1,975 | 26 |

Every surviving vector is saved. Exact radical FP dimensions are checked
against all source fusion equations, and their integer floors are checked
before enumeration. The entire finite domain for **each of the six
rings** is enumerated a second time in Python, using independent rational
Schur elimination rather than the C++ fraction-free arithmetic. The two
full survivor lists agree, including the empty residual-Gram case of the
unit algebra. The four internal-end vectors of the two complete R65
rank-two based modules all survive.

In R65, the only surviving object of the form `1+X_i` has `i=7`, the
order-two invertible. No `1+rho` algebra can therefore start a construction
for this ring. Larger objects remain possible, including the subgroup
algebra objects whose associator obstruction was kept explicit in
`R65_MODULES.md`. In the two Fibonacci-containing cases, `1+Fib` survives,
as it must: it is the internal end of the Fibonacci simple. This is not
evidence of a new category; its categorical Morita construction is
available whenever the original category exists.

The shared C++ engine's signed128 safety proof is inherited from the
quadratic filter: all entries reaching the 7-by-7 PSD test are bounded by
400, and twice the square of the order-six Hadamard bound is below
`2^127`. This wrapper checks the coefficient bound and records the exact
engine-source hash. No floating-point rejection or time budget is used.

The remaining 30,28,21,22,18,26 objects are **necessary candidates only**.
Integral Gram factorization, full module action, multiplication,
associativity and separability still have to be checked before an object
can be used as a construction. In particular this finite exhaustion does
not turn an open ring into a model or a noncategorifiability result.

Read-only full replay (both invocations also repeat every domain in Python):

```sh
python evidence/rank8_frontier_20261021/structural_models/algebra_candidates.py
python -O evidence/rank8_frontier_20261021/structural_models/algebra_candidates.py
```

The categorical inputs are module adjunction, rigidity and FP dimension
theory in EGNO, *Tensor Categories*, Chapter7; see the linked general
proof for their explicit derivation without pivotal or unitary assumptions.

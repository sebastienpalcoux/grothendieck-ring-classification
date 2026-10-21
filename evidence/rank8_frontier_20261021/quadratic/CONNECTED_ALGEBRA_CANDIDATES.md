# A complete finite filter for connected separable algebra objects

For each of the six quadratic residual rings this search exhausts every
possible underlying object of a connected separable algebra and applies
necessary integral Gram conditions. This is a complete finite **filter**,
not a construction or an exhaustive associator search. The remaining
objects may fail further module or algebra equations.

## Bounds and Gram conditions in an arbitrary complex fusion category

Let `A` be a connected separable algebra and let `m=A` be its regular right
module. Connectedness gives `End_A(m)=C`, so `m` is simple in the semisimple
right-module category. Write `a_i` for the multiplicity of `X_i` in `A`.
Free-module adjunction identifies `a_i` with
`dim Hom(X_i tensor m,m)`. Rigidity identifies this vector space with
`Hom(m,X_i* tensor m)`. In a semisimple category the dimensions of
`Hom(m,Y)` and `Hom(Y,m)` agree, so **`a_i=a_(i*)`**. This argument uses
neither a module trace nor a pivotal structure.

The action matrices `M_i` on an indecomposable module category have a
common strictly positive FP eigenvector with eigenvalues `d_i=FPdim(X_i)`.
As `a_i=M_i[m,m]`, positivity gives `0<=a_i<=d_i`. Thus the complete
integral domain is

`a_0=1`, `a_i=a_(i*)`, `0<=a_i<=floor(d_i)`.

If an invertible `g` occurs in `A`, then `g tensor m` is simple and its
nonzero map to `m` is an isomorphism. Consequently `g tensor A=A` as
underlying objects. This supplies a further exact stabilization test.

Let `F(X)=X tensor A` be free induction, and let `B` be its nonnegative
integral multiplicity matrix. Adjunction gives

`(B^T B)_ij = dim Hom_A(F(X_i),F(X_j)) = (N_A)_ij`,

where `N_A=sum a_k N_k` is symmetric because `A` is self-dual. The row of
`B` indexed by the simple regular module `m=A` is exactly `a`. Therefore

**`G_A=N_A-a a^T` is a nonnegative integral Gram matrix.**

In particular it is entrywise nonnegative and positive semidefinite.
These conclusions hold for arbitrary complex fusion categories. The
implementation uses the commutative source-ring convention for `N_A`;
all six tensors satisfy that hypothesis.

## Complete enumeration

| Ring | All bounded self-dual vectors | Entrywise Gram survivors | PSD Gram survivors |
| --- | ---: | ---: | ---: |
| 1055 | 794,976 | 35,913 | 85 |
| 1768 | 9,539,712 | 249,139 | 115 |
| 1795 | 12,984,608 | 416,274 | 87 |
| 3258 | 580,608 | 32,098 | 99 |
| 3413 | 580,608 | 35,404 | 60 |
| 3472 | 168,591,360 | 4,841,427 | 70 |

Every surviving coefficient vector is stored, along with source hashes,
exact dimension bounds, stabilization counts, and independent Gram ranks.
For the especially thin case 3472, of all objects `1+X` only basis index
3 survives this necessary filter. The unit algebra remains in every ring.
All candidate internal ends from the complete rank-two based-module
search also survive. Neither fact constructs a nontrivial algebra.

The categorical inputs are standard algebra/module adjunction, rigidity,
and module FP dimension theory; see
[EGNO, *Tensor Categories*, Chapter 7](https://math.mit.edu/~etingof/egnobookfinal.pdf)
and V. Ostrik,
[*Module categories, weak Hopf algebras and modular invariants*](https://arxiv.org/abs/math/0111139).
The self-duality argument is given explicitly above to avoid importing
unitary or module-trace assumptions.

## Exact arithmetic and independent checks

`connected_algebra_candidates.cpp` enumerates the entire proved domain
with no search budget. It uses symmetric pivoting and fraction-free
Schur elimination. A negative diagonal, or a zero-diagonal residual block
with a nonzero off-diagonal entry, rejects PSD. Every exact division is
checked. No floating-point decision is used.

All entries reaching the PSD test lie in `[0,400]`. Stored minors of order
at most six have absolute value at most `6^3*400^6` by Hadamard's bound.
Each update numerator is bounded by twice its square, strictly below
`2^127`; the final order-seven minor is produced by the last such update.
This proves the signed 128-bit arithmetic safe. The Python driver checks
the input and numerical bound before calling the executable.

A separate Python rational Schur-elimination implementation verifies every
surviving vector. It also repeats the **entire 392-vector domain** of the
known control `R8_3_342=Rep(C13 semidirect C6)`, reproducing all 30 survivors.
The regular function algebra, whose coefficient vector is the FP
dimension vector, gives `G_A=0` and is retained. This tests the singular
PSD boundary as well as proper positive and negative cases.

Read-only replay, including temporary compilation:

```sh
python evidence/rank8_frontier_20261021/quadratic/connected_algebra_candidates.py
python -O evidence/rank8_frontier_20261021/quadratic/connected_algebra_candidates.py
```

The remaining work is to factor the necessary Gram matrices integrally
and solve the compatible module/algebra associativity equations. No
unresolved ring is declared noncategorifiable or exotic from this filter.

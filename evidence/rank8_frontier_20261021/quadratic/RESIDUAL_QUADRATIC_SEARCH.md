# Complete bounded module searches and an unbounded model-family sieve

After the five exclusions in the other notes, the six quadratic residuals
`1055,1768,1795,3258,3413,3472` receive the following new completed searches.
These results do not construct associators and do not settle their
categorifiability. In particular a feasible based module is not a model.

## All rank-two based modules

For an indecomposable rank-two module category, its nonnegative integral
action matrices have the FP character as a simultaneous eigencharacter.
If the FP dimension field is quadratic, rationality forces the other
character to be its Galois conjugate: these two constituents already use
the entire two-dimensional representation. Thus every action matrix is
the same rational affine expression in one irrational generator matrix
as its FP dimension is in the chosen generator's dimension.

Choose a self-dual irrational generator of trace `T` and norm `U`. Its
matrix is `[[a,b],[b,T-a]]`, with `0≤a≤T` and
`b²=a(T-a)-U`. Connectedness requires `b>0`. These are complete finite
bounds, not a search budget. Swapping the module vertices lets us impose
`a≥T-a`. Reconstruct every other matrix from the affine dimension
identities, then check nonnegative integrality, duality and all 64
multiplication relations. The complete results are:

| Ring | Reference basis index | Generator matrices, up to swapping vertices | Number of classes |
| --- | ---: | --- | ---: |
| 1055 | 4 | `[[7,6],[6,5]]` | 1 |
| 1768 | 2 | `[[6,6],[6,4]]` | 1 |
| 1795 | 2 | `[[9,6],[6,3]]`; `[[12,3],[3,0]]` | 2 |
| 3258 | 1 | `[[4,3],[3,1]]` | 1 |
| 3413 | 1 | `[[4,3],[3,1]]` | 1 |
| 3472 | 1 | `[[7,7],[7,5]]`; `[[11,5],[5,1]]` | 2 |

The evidence contains every full eight-matrix action and both candidate
internal-end objects (their coefficients are the diagonal matrix
entries). This gives explicit, finite algebra-object targets for future
module-pentagon work. It does not assert that any target admits a
separable algebra structure.

The free involution actions in 1768 and 1795 have no fixed simple, so
the pointed associator is not forced trivial by the fixed-point
argument. Their rank-two based modules send the involution to the
identity. If such a module category exists, its fixed module simples
would force that pointed associator to be trivial. The other associator
class is not silently discarded by this based-module computation.

## Complete forced split representations for 1055

The involution is index 3 and the fixed indices are `[1,2]`. The
nonselfdual generator `S_1` is normal, since `S_2=S_1^T` and the ring
is commutative. Its bounded block is `[[2,0],[2,2]]`. Enumeration of all
27 matrices satisfying these parity bounds, normality and its source
polynomial leaves only `S_1=0`, and hence `S_2=0`. The remaining system
is determined by the diagonal signs of `S_3`, the symmetric bounded
`S_4`, and the symmetric bounded `S_6`, since `S_5=S_3S_4` and
`S_7=S_3S_6`. All **1,296** possibilities are tested against every
duality, bound, parity and multiplication relation. Exactly four remain;
the JSON gives their full matrices. Each has `S_3=-I`. This is a complete
necessary-system result with feasible witnesses, not an exclusion.

## All generalized-near-group dimensions, without a parameter cutoff

Let a generalized near-group category have `G` invertibles, stabilizer
order `s`, a single noninvertible orbit of size `l=G/s`, common irrational
FP dimension `d`, and total noninvertible multiplicity `K`. Then

`d²=s+Kd`, and `D=l(s+d²)=l(2s+Kd)`.

Taking the quadratic norm and trace gives the particularly useful
identity

**`Norm(D)/Trace(D)=l s=G`.**

This provides a complete, unbounded model-family sieve. It is a direct
deduction from the generalized-near-group dimension equation; it is not
a claim that the residual rings themselves are generalized near-group
rings. Morita equivalence preserves FP dimension. Pointed products and
any finite tower of group extensions or equivariantizations multiply
it by a positive integer `k`. Therefore a residual dimension `D` can
belong to that entire construction family only when
`G_D=Norm(D)/Trace(D)` is a positive integer and `k` divides `G_D`.
For each divisor `k`, the base group order is `G_D/k`; its stabilizer
`s` divides this order, and

`K² = Trace(D)/(k l)-4s`

is then uniquely determined. Checking its being a nonnegative integer
square exhausts every parameter. No upper cutoff on a group, level,
multiplicity, rank, or tower length is used. De-equivariantization by
division is outside this stated family.

| Rings | Exact FP dimension | `Norm/Trace` | Complete family result |
| --- | --- | --- | --- |
| 1055, 1768 | `444+72√37` | 6 | Four dimension matches described below |
| 1795 | `540+240√5` | `10/3` | Entire stated construction family excluded |
| 3258, 3413 | `(315+135√5)/2` | `45/7` | Entire stated construction family excluded |
| 3472 | `700+490√2` | 7 | Two dimension matches described below |

For 1055/1768, all matches have stabilizer `s=1` and `K=12`:
`(k,G,l)=(1,6,6),(2,3,3),(3,2,2),(6,1,1)`.
For 3472, all matches have `s=1,K=14`:
`(k,G,l)=(1,7,7),(7,1,1)`.
The last entry in each list would require a rank-two fusion category
with multiplicity 12 or 14, excluded by Ostrik's rank-two classification.
The remaining entries are dimension matches only. For example the
3472 match has a rank-14 generalized near-group base with group order
7 and total multiplicity 14; existence and a Morita relation to 3472
have not been proved. Describing this match as an actual construction
would be unjustified.

Primary references for the categorical inputs are EGNO,
[*Tensor Categories*, Chapter 7 and FP dimension/Morita theory](https://math.mit.edu/~etingof/egnobookfinal.pdf);
A. Schopieray, *Categorification of integral group rings extended by one
dimension*, [arXiv:2208.07319](https://arxiv.org/abs/2208.07319), for
two-orbit rings and their dimension equations; and V. Ostrik,
*Fusion categories of rank 2*,
[arXiv:math/0203255](https://arxiv.org/abs/math/0203255).

## Exact replay

```sh
python evidence/rank8_frontier_20261021/quadratic/rank_two_and_models.py
python -O evidence/rank8_frontier_20261021/quadratic/rank_two_and_models.py
python evidence/rank8_frontier_20261021/quadratic/residual_split_1055.py
python -O evidence/rank8_frontier_20261021/quadratic/residual_split_1055.py
```

These commands are read-only. Explicit `--write` regenerates JSON
evidence. Source tensor digests, positive FP homomorphisms, every
reconstructed module multiplication and every model dimension identity
are checked exactly. The three formerly thin cases 1768,1795,3472 now
have completed new finite module searches and an unbounded family
sieve; they remain unresolved rather than being certified exotic.

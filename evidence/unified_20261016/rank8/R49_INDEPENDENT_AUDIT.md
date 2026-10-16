# Independent categorical and source audit of the R8_1_49 exclusion

## Conclusion

The Frobenius–Schur parity argument and its use to construct the involution algebra are valid without a braiding. The published two-dimension theorem supplies the required positive pivotal structure after Galois conjugation, so the resulting exclusion applies to arbitrary complex fusion-category categorifications.

The independent source replay gives tensor SHA-256

`a5cefbf544001818e1e5c6e5bde951601eaf35f3d71034a252df1b7de751ea85`.

It agrees with the source digest in `supplements/rank8/data/decisions.json`.

## 1. Pivotality is a conclusion, not an assumption

I checked the **published** primary PDF of A. Schopieray, *Categorification of integral group rings extended by one dimension*, J. London Math. Soc. 108 (2023), 1617–1641, DOI https://doi.org/10.1112/jlms.12789. Lemma 3.1, printed page 1628, states that a categorification of a fusion ring with Frobenius–Perron dimensions in `{1,d}` is Galois conjugate to a pseudo-unitary category. It does not require a pivotal structure on the initial category. The published statement correctly includes Galois conjugacy; the stronger wording in the original arXiv v1 should not be substituted for it.

R49 has dimensions 1 and `d=2+sqrt(5)`. A hypothetical categorification therefore gives a pseudo-unitary categorification of the same based ring. Equip this category with its canonical positive spherical structure. It suffices to exclude this conjugate.

## 2. The tensor-power form is valid in an unbraided category

In a strict pivotal realization let `j_X:X -> X**` denote the pivotal map and define the pivotal transpose of `f:X -> X*` by

`t(f) = f* o j_X`.

For a self-dual simple X choose an isomorphism f with `t(f)=epsilon f`, where `epsilon=nu_2(X)` is +1 or -1. Set `V=X^n` and `b=f^tensor n`. This is a nondegenerate map `V -> V*`: duality reverses the tensor word, but the word consists of identical objects. The same observation applies to the component morphisms, so monoidality of the pivotal structure gives exactly

`t(b) = (f* o j_X)^tensor n = epsilon^n b`.

There is no permutation morphism or braiding in this calculation. Reversal is harmless specifically because all factors and component morphisms are identical.

Now restrict b to the S-isotypic component for a self-dual simple S. No different simple isotypic component can pair with it, by semisimplicity and the vanishing of morphisms between distinct simples. The restricted form is therefore nondegenerate. Choosing a self-duality `f_S` of sign `nu_2(S)`, its matrix is `f_S tensor B`, and the transpose equation reads

`nu_2(S) B^T = epsilon^n B`.

If S occurs with odd multiplicity, the matrix B has odd size and cannot be invertible and skew-symmetric over C. Hence `nu_2(S)=epsilon^n`. In particular, in an odd tensor power, an odd unit multiplicity forces `epsilon=+1`, and every self-dual simple of odd multiplicity in that tensor power has indicator +1.

This argument uses neither positivity nor braiding. Positivity is used subsequently to identify the order-two invertible indicator with its pointed associator class.

## 3. Exact source check

I independently loaded the rank-eight census, selected the 49th lexicographically ordered maximum-multiplicity-one tensor, and checked its ledger digest. With zero-based labels:

- the invertibles are `{0,3,4,5}` and form the Klein group;
- the dual permutation is `[0,2,1,3,4,5,6,7]`;
- `rho=6` is self-dual;
- `rho^2` is `[1,1,1,0,0,0,1,1]`;
- `rho^3` is `[1,4,4,1,1,1,5,4]`.

Thus the unit and each of the three invertible involutions occur once in `rho^3`. The preceding lemma proves `nu_2(rho)=+1` and `nu_2(g)=+1` for every invertible g.

The raw independent source receipt is the adjacent `r49_independent_source_audit.json`.

## 4. The involution algebra and dual

In the positive spherical structure of `Vec_C2^omega`, the nontrivial object's second indicator is the sign representing the restriction class in `H^3(C2,C*)`. Therefore `nu_2(3)=+1` makes the pointed restriction to `H={0,3}` tensor equivalent to ordinary `Vec_C2`. Its regular algebra `A=1+3` exists and is separable. No grading twist, assumed automorphism, or merely formal fusion-ring algebra is used.

The independent H-by-H orbit calculation gives:

| Underlying orbit | Stabilizer order |
| --- | ---: |
| `{0,3}` | 2 |
| `{4,5}` | 2 |
| `{1,2,6,7}` | 1 |

On either pointed orbit the stabilizer is C2. Every complex projective representation of C2 can be linearized, so there are two one-dimensional simple blocks, giving four invertibles in the dual. The free noninvertible orbit gives one simple bimodule, with underlying sum of all four noninvertibles. Its dual-category dimension is `4d/FPdim(A)=2d=4+2sqrt(5)`.

Consequently the dual has exactly four invertibles and one noninvertible Z. The invertibles form C4 or V4, and the dimension equation gives

`Z^2 = sum_(g in G') g + 8Z`.

The V4 terminal is excluded by the published general-complex Schopieray Theorem 1.1. The C4 terminal is the same `k=2` near-group obstruction already independently audited and replayed for R170 in `rank5_cyclic/`. Thus the parity lemma closes the only missing algebra-existence step in the inverse-Morita proof and gives a general complex exclusion of R49.

## Boundary

For the analogous R412 source the invertible multiplicities in the cube are even. This parity argument supplies no corresponding trivialization there. The present audit changes only the R49 conclusion.

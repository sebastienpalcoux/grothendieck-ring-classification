# R455: conditional complex obstruction and the remaining gap

This frontier note does **not** change the general-complex categorifiability status of `R8_3_455`. It excludes every neutral category in the strict Evans–Gannon HI(C3) presentation, including the known Haagerup categories and their Galois conjugates. No unitarity, positive dimension, or positivity of coefficients is used in the polynomial calculation. The old evidence is unchanged.

## Categorical reduction that does not require unitarity

The source tensor has a faithful C2 grading, with neutral basis `[0,1,2,3,6,7]` of HI(C3) type and odd basis `[4,5]`. Its simple `Y=4` satisfies `gY=Yg=Y` for all three invertibles and `Y²=1+g+g²`. Therefore `CY` is a rank-one module for the pointed category: its scalar module pentagon trivializes the pointed H³(C3,C×) class. Also H²(C3,C×)=0, by rescaling a projective generator by a cube root.

The internal endomorphism algebra of Y in the neutral category D has underlying object A=1+g+g². It is the unique subgroup algebra up to isomorphism because H²(C3,C×)=0. The odd component is an invertible D-bimodule, equivalent on one side to D_A. Hence its dual category, the A-bimodule category, must be tensor equivalent to D. This necessary self-Morita-duality condition is valid without a C* structure.

## Conditional Fourier obstruction

Assume D is a strict Evans–Gannon HI matrix category. For C3 its scalar phase is 1. Cyclic symmetry puts its coefficient matrix in the form

```
A = [[c,a,b], [a,b,f], [b,g,a]].
```

The full subgroup Morita dual is represented by
`B[i,j]=(1/3) sum_(x,y) A[x,y] zeta^(i*y-j*x)`.
Tensor equivalence of the strict presentations requires either `B[i,j]=A[i,j]` or `B[i,j]=A[-i,-j]`. Both exact linear systems have the same two-dimensional solution:

```
A = [[3b+g,b,b], [b,b,g], [b,g,b]].
```

Writing u for the reciprocal categorical dimension, the linear HI relation and three quadratic HI relations now require

```
5b+g+u=0,
2b²+g²−1=0,
7b²+2bg+u=0,
b(b+2g)=0.
```

If b=0, the third and first relations give u=g=0, contradicting the second. Otherwise g=−b/2, u=−9b/2, and the third gives b=3/4. The second then equals 17/64 rather than zero. Thus no strict HI matrix category is its own full-subgroup dual. This proves the claimed conditional obstruction even before imposing the dimension polynomial, cubic, or quartic HI relations.

The verifier recomputes the source tensor hash, checks all 512 grading coefficients and the fixed-simple identities, checks both Fourier kernels exactly over Q(zeta), and verifies both the elementary contradiction and an independent Groebner-basis calculation. Default replay is read-only:

```
python evidence/rank8_frontier_20261021/structural_models/r455/verify_conditional_fourier.py
python -O evidence/rank8_frontier_20261021/structural_models/r455/verify_conditional_fourier.py
```

## Exact primary-source scope

1. [Evans–Gannon, *Non-unitary fusion categories and their doubles via endomorphisms*, Adv. Math. 310 (2017), 1–43](https://orca.cardiff.ac.uk/id/eprint/73921/8/1-s2.0-S0001870816302584-main.pdf), Theorems 1–3, Sections 4 and 7.1. Theorem 1 starts with strict algebra endomorphism identities; the discussion preceding it explicitly sets aside general cocycle actions. Theorem 2(b) gives the matrix-equivalence criterion. Theorem 3(ii) describes the four C3 categories in this presentation, including the nonunitary Galois companions. These statements alone do not classify all abstract complex categorifications of the ring.
2. [Gannon–Schopieray–Yadav, *On Haagerup–Izumi fusion categories*, arXiv:2609.25185v1](https://arxiv.org/html/2609.25185v1), Appendix E.3.4–E.3.5, Theorems E.12–E.13 and Corollary E.16, supply the full subgroup Fourier–Morita equivalence for strict HI matrices without unitarity. Equations E.14 and E.16 give the transform used here. The reconstruction is a forward matrix-to-category construction; its unitary Q-system classification is not a general-complex converse.
3. [Grossman–Snyder, *Quantum subgroups of the Haagerup fusion categories*, arXiv:1102.2631v2](https://arxiv.org/html/1102.2631v2), Theorem 1.5, independently gives trivial Brauer–Picard groups for the known Haagerup categories. Applying a field automorphism to finite algebraic category, module, and equivalence data preserves this property for Galois companions. This is a second obstruction within that known family, not an assertion that every complex categorification belongs to it.

## Remaining bridge

R455 forces the pointed associator and the cyclic projective obstruction to vanish. We have not proved that these vanishings suffice to realize every possible complex neutral category by the exact strict endomorphism presentation required in Evans–Gannon Theorem 1. Nor have we proved universal completeness of the transparent ansatz or of a low-rank F-symbol census. A proof of that strictification/deconstruction converse would upgrade the conditional calculation to a general exclusion; absent it, the general status remains unresolved.

# Three new braided exclusions, with general existence left open

These arguments exclude **braided** categorifications of `R9_2_12`,
`R9_2_959`, and `R9_2_941`. They do not exclude arbitrary fusion
categorifications and do not change the 2,033/32/18 general partition.
The noncommutative ring `R9_2_1965` was already excluded from braided
categorification.

## A general obstruction to a central Rep(S3)

**Proposition.** A complex fusion category of FP-dimension type
`(1^4,2^2,6^3)` admits no fully faithful central Tannakian embedding
`Rep(S3) -> Z(C)` whose composite with the forgetful functor is fully
faithful.

**Proof.** Such an embedding gives an actual equivariantization
`C = D^{S3}`, with `FPdim(D)=20` (EGNO Theorem 8.23.3).
The dimension formula for simples in an equivariantization is

`FPdim(X_{Y,pi}) = [S3:S_Y] dim(pi) FPdim(Y)`.

Every simple of D occurs below some equivariant simple. Thus its dimension
is a rational algebraic integer, hence a positive integer. All subgroups
of S3 have trivial Schur multiplier over C, so the projective character
degrees of a stabilizer equal its ordinary character degrees. This is
clear for cyclic subgroups; for S3 it is the standard vanishing
`H^2(S3,C^*)=0`.

Each S3-fixed invertible of D contributes simples of dimensions `(1,1,2)`
to C. Conversely, an invertible of C lies over an S3-fixed invertible of D.
Therefore D has exactly two S3-fixed invertibles, already accounting for
all four dimension-one and both dimension-two objects of C. The remaining
objects of C, of dimension six, can arise only in these packets:

| Stabilizer | Orbit size | Dimension in D | Dimensions contributed to C |
|---|---:|---:|---|
| trivial | 6 | 1 | 6 |
| C2 | 3 | 2 | 6,6 |
| C3 | 2 | 3 | 6,6,6 |

No additional fixed orbit is possible, since it contributes `d,d,2d`.
Partitioning the three six-dimensional objects gives exactly three
possible types for D:

1. `(1^20)`, with two fixed elements and three free S3-orbits of size six;
2. `(1^8,2^3)`;
3. `(1^2,3^2)`.

The second is impossible because a pointed subcategory of dimension eight
would lie in a category of dimension twenty. The FP-dimension of a fusion
subcategory divides that of the ambient category in the ring of algebraic
integers, whereas `20/8` is not an integer.

The third is impossible because fusion categories of dimension `2^2*5`
are solvable (ENO Theorem 1.6), hence have the strong Frobenius property
(ENO Theorem 1.5), whereas `20/3` is not an integer.

In the first case D is `Vec_K^omega` for a group K of order twenty. The
S3 action induces an action by group automorphisms on K. Its unique
Sylow-five subgroup P is characteristic. The subgroup C3 of S3 acts
trivially on P because `Aut(C5)=C4`. Consequently C3 fixes at least five
elements of K. But the stipulated S3-orbit pattern has exactly two
C3-fixed elements: every free six-element orbit restricts to two free
three-element C3-orbits. This is a contradiction. QED.

No assumption that C itself is braided, unitary, group-theoretical, or
solvable occurs in this proposition. The central Rep(S3) premise is
essential and is not inferred merely from the presence of its based ring.

## A braided criterion applying to R9_2_12 and R9_2_959

**Theorem.** Suppose an integral fusion ring R of type `(1^4,2^2,6^3)`
has the following two properties:

* every nonpointed fusion subring contains a subring with the ordinary
  representation ring of S3;
* every invertible fixes at least one of the three dimension-six basis
  elements.

Then R has no braided complex fusion categorification.

**Proof.** A hypothetical categorification C is pseudo-unitary by weak
integrality. Equip it with the canonical positive spherical structure and
the resulting ribbon structure. Write E for its Müger center.

If E is nonpointed, the first hypothesis gives a rank-three symmetric
subcategory with fusion rules `Rep(S3)`. By Deligne's classification of
symmetric fusion categories, it is `Rep(H,z)` for a finite group H and a
central involution z. Its dimension is six and it is nonpointed, so H is
S3. Since the center of S3 is trivial, z=1, and this subcategory is
Tannakian. Its embedding in the Müger center gives the prohibited central
Rep(S3) of the proposition.

Suppose E is pointed. For each simple g of E, choose a dimension-six
simple X fixed by g. Since g is transparent, the balancing equation gives
`theta_{gX}=theta_g theta_X`; hence `theta_g=1`. All twists in E are
therefore trivial, so E is Tannakian: `E=Rep(H)` for an abelian group H
of order `e` dividing four. (This includes `e=1`.)

De-equivariantization by the full Müger center gives a nondegenerate
braided fusion category B, with `FPdim(B)=120/e`, and `C=B^H`.
It is integral by the same rational-dimension argument as above. If a
dimension-six simple of C lies over Y in B, then

`6 = [H:H_Y] dim(pi) FPdim(Y)`.

Here H has order at most four. All subgroup indices and all projective
irreducible degrees are powers of two (for these groups the degrees are
one or two). Thus `FPdim(Y)` is an integer divisible by three.
But B is integral and nondegenerate, hence modular with its positive
spherical structure. Modular square-divisibility says
`FPdim(Y)^2 | FPdim(B)` in the integers. The left side is divisible by
nine, whereas `120/e` has 3-adic valuation one. Contradiction. QED.

This proof handles the potentially super-Tannakian center explicitly;
it does not assume that every symmetric subcategory is Tannakian.

**Exact application.** With zero-based source labels, the S3 subring is
`[0,6,7]` for R9_2_12 and `[0,7,8]` for R9_2_959. Every nonpointed fusion
subring contains this subring, including the whole ring. Each of the four
invertibles fixes a dimension-six object. The verifier regenerates every
fusion subring from the original compressed source tensor, checks all
dimension equations and fixed points, and exhaustively checks the small
S3-orbit bookkeeping. No floating-point arithmetic is used.

## R9_2_941: simple, nonbraided, and not weakly group-theoretical

The exact original tensor has no proper nontrivial fusion subring, has
dimensions `(1,7,8,7,7,7,9,9,9)`, and global dimension 504. Its full tensor
is isomorphic to the exotic dimension-504 ring in Alekseyev--Bruns--Dong--
Palcoux, arXiv:2507.07023v2, Sections 1.5 and 7.5. The exact based
isomorphism is rechecked by the verifier using the copied published tensor.
The source states that it is exotic, i.e. it is not the representation
ring of a finite group. It explicitly leaves categorification open.

A hypothetical braided categorification is simple. Its Müger center is
therefore either Vec or the entire category. In the first case it is
modular, impossible because a dimension-seven simple would require
`49 | 504`. In the second case it is symmetric; Deligne's classification
makes its underlying fusion ring a finite-group representation ring,
contradicting the exotic property. Thus it cannot be braided.

ENO Proposition 9.11 also says that a nonpointed simple weakly
group-theoretical category is equivalent to Rep(G) for a nonabelian
finite simple group. Consequently R9_2_941 admits no weakly
group-theoretical categorification. General and unitary existence remain
open. This obstruction must not be represented as a general exclusion.

## Primary references and proof dependencies

* Etingof--Gelaki--Nikshych--Ostrik, *Tensor Categories*, author's final
  version: <https://math.mit.edu/~etingof/egnobookfinal.pdf>.
  Proposition 4.15.9 (equivariant simple dimensions); Theorem 8.23.3
  (central embedding and actual equivariantization); Proposition 8.23.8
  (braided descent); Proposition 8.14.6 (modular square-divisibility);
  Sections 9.9 and 9.11 (symmetric/Tannakian categories), and Section 8.20
  (Müger center and nondegeneracy).
* Etingof--Nikshych--Ostrik, *Weakly group-theoretical and solvable fusion
  categories*, <https://arxiv.org/pdf/0809.3031>, Theorems 1.5 and 1.6,
  Proposition 9.11.
* Liu--Palcoux--Ren, *Interpolated family of non group-like simple
  integral fusion rings of Lie type*, <https://arxiv.org/pdf/2102.01663>,
  Section 5, especially the symmetric/modular dichotomy for simple
  weakly integral braided categories.
* Alekseyev--Bruns--Dong--Palcoux, *Classifying integral Grothendieck
  rings up to rank 5 and beyond*, <https://arxiv.org/pdf/2507.07023v2>,
  Sections 1.5 and 7.5, Question 1.14 (the exact open ring).

`verify_scope_refinements.py` and `scope_refinements.json` record the
finite ring hypotheses. They do not computationally certify the cited
categorical theorems or turn the missing general hypotheses into facts.

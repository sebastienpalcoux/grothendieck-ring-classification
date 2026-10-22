# Categorical existence audit of the neutral E21 model

## Verdict and separation of responsibilities

The triality-zero component of the E21 quantum subgroup of SU(3) is an
**existing unitary fusion category**. It is obtained from the conformal
embedding `SU(3)_21 subset (E7)_1` by taking all right modules over its
connected commutative algebra, then taking the neutral component of the
induced faithful Z/3 grading. This is not merely a candidate graph algebra.

Its global FP dimension is exactly

    144 + 96 sqrt(2) + 80 sqrt(3) + 56 sqrt(6).

The separate graph/tensor workstream reconstructs the 24-vertex E21 graph,
its eight neutral vertices, and all 512 neutral fusion coefficients, and
reports a based-ring isomorphism with R8_3_982. This audit establishes the
categorical, unitary and grading prerequisites of that identification;
it does not substitute a dimension match for the required tensor match.

The reviewer is a separate automated mathematical agent, not an independent
human reviewer.

## 1. Actual fusion category and unitary structure

Put V=L(sl3,21), U=L(E7,1), C=Rep(V), and let A be U restricted to V.
The conformal embedding is explicitly recorded by Evans--Pugh [EP, §2,
equation (18)] and Schopieray [S, §4.1]. The vacuum branching object is

    (0,0) + (4,4) + (6,6) + (10,10) + (21,0) + (0,21)
    + (13,4) + (4,13) + (10,1) + (1,10) + (9,6) + (6,9).

The finite conformal extension makes A a connected étale algebra in C.
DMNO [D, §6.1] proves this extension/algebra correspondence and identifies
`C_A^0 = Rep(U)`. Their §3.3 proves that **all right A-modules** C_A form
a fusion category under the relative tensor product; one should not
replace this category by the rank-two subcategory of local modules.

Unitarity has two complementary primary-source justifications. The local
conformal inclusion is realized in the loop-group/type-III-factor setting:
Evans--Pugh [EP, §2, printed pp.4--5] identify its chiral fusion systems
with the E^(24) nimrep because the inclusion is local. Their chiral objects
are finite-index endomorphisms and inherit the operator-algebraic C-star
tensor structure; this does not assert a braiding on the full chiral
category. This also explicitly connects
the conformal embedding to the graph, rather than only to its invariant.

Alternatively, Gui [G, Theorem 2.21] turns a unitary conformal VOA extension
of the completely unitary affine VOA V into a standard Q-system A.
Theorem 2.27 makes every finite right A-module and A-bimodule unitarizable.
Section 3.2 constructs unitary relative tensor products, with unitary
associativity in Corollary 3.10 and the pentagon in Proposition 3.11;
Theorem 3.18 supplies rigidity. The usual embedding of right modules into
bimodules, using the unitary braiding to define the left action, is a full
tensor embedding, so C_A inherits this unitary structure. Completeness of
the unitary affine VOA hypotheses is recorded in [G, Corollary 3.32].

Thus E=C_A is a unitary fusion category, and every full fusion subcategory
of E, in particular its neutral component below, is unitary.

## 2. Faithful triality grading: proof

The SU(3) category has its standard Z/3 grading

    degree(a,b) = a-b mod 3,

with a,b nonnegative and a+b at most 21. Every displayed summand of A has
degree zero. There is also an intrinsic check: its twist is one, and the
conformal weight is

    h(a,b) = (a^2+b^2+ab+3a+3b)/72.

An integral h forces `(a-b)^2 = 0 mod 3`, hence degree zero. This also
shows that any twist-trivial algebra in C lies in its neutral component.

For an A-module M, split its underlying object as `M=M_0+M_1+M_2`.
Since A has degree zero, each M_t is stable under the right A action.
Consequently a simple A-module is homogeneous. Relative tensor products
are quotients of ordinary tensor products, so their degrees add. The
unit A has degree zero and duals negate degrees. This gives a Z/3 grading
of the genuine tensor category E. It is faithful: for a nonzero simple X
in each degree of C, the free module `X tensor A` is nonzero, lies in that
degree, and has a simple summand.

The neutral component D=E_0 is therefore a unitary fusion subcategory.
The graph grading is the same one: free induction of the fundamental
(1,0) advances the degree by one; the unit vertex is in degree zero.
For a connected directed fundamental graph, this condition determines
the colors uniquely after fixing the unit vertex. Thus the graph's eight
neutral vertices are the simples of D once the E21 graph identification
and coloring are checked in the tensor workstream.

## 3. Exact global dimension

The Weyl denominator gives

    FPdim(C) = 3*24^2 / (64 sin(pi/24)^4 sin(pi/12)^2).

Schopieray [S, §4.1] identifies `Rep(E7_1)` as the pointed category of
order two whose nontrivial twist is -i. In particular `FPdim(C_A^0)=2`.
The formulas [D, Lemma 3.11 and Corollary 3.32] imply

    FPdim(A)^2 = FPdim(C)/2,
    FPdim(E) = sqrt(2 FPdim(C)).

All components of a faithful finite-group grading have equal FP dimension,
so

    FPdim(D) = sqrt(2 FPdim(C))/3
             = sqrt(6)/(sin(pi/24)^2 sin(pi/12)).

For an elementary radical check,

    sin(pi/24)^2 sin(pi/12) = (sqrt(6)-sqrt(2)-1)/8,
    1/(sqrt(6)-sqrt(2)-1) = 7+5sqrt(2)+4sqrt(3)+3sqrt(6).

Multiplication proves the displayed quartic expression exactly.

## 4. Central semion consistency check

The nontrivial local module j has dimension one, order two, and twist -i.
Its degree in Z/3 must be zero because `2 degree(j)=0`. Local modules
embed centrally in E with reversed braiding [D, Theorem 3.20 and
Corollary 3.30]. Restricting this half-braiding to D gives a central
semionic lift of j in Z(D), with twist +i for that reversed convention.
This is consistent with R982's already retained semionic center branch.

An early suggestion in team discussion that R982 had no such central
invertible was incorrect: the frozen R982 research already includes
`rank8_next_20261021/r982/semion_action_control.py`. The semion test does
**not** distinguish R928 from R982. The exact based tensor comparison is
the decisive identifier.

## Primary references

* [EP] D. E. Evans and M. Pugh, *SU(3)-Goodman--de la Harpe--Jones
  subfactors and the realisation of SU(3) modular invariants*,
  Rev. Math. Phys. 21 (2009), 877--928,
  <https://arxiv.org/abs/0906.4252>. See §2, equation (18), the conformal
  embedding list, and the paragraph on local inclusions and chiral graphs.
* [D] A. Davydov, M. Müger, D. Nikshych and V. Ostrik,
  *The Witt group of non-degenerate braided fusion categories*,
  J. reine angew. Math. 677 (2013), 135--177,
  <https://arxiv.org/abs/1009.2117>. See §3.3, Lemma 3.11,
  Theorem 3.20, Corollaries 3.30--3.32, and §6.1.
* [G] B. Gui, *Q-systems and extensions of completely unitary vertex
  operator algebras*, <https://arxiv.org/abs/1908.03484>.
  See Theorems 2.21, 2.27 and 3.18, §3.2, and Corollary 3.32.
* [S] A. Schopieray, *Classification of sl3 relations in the Witt group
  of nondegenerate braided fusion categories*,
  <https://arxiv.org/abs/1608.03155>, §4.1.
* [CIS] R. Coquereaux, E. Isasi and G. Schieber,
  *Notes on TQFT wire models and coherence equations for SU(3) triangular
  cells*, SIGMA 6 (2010), 099, <https://arxiv.org/abs/1007.0721>.
  Figure 43 is the graph used by the separate tensor workstream.

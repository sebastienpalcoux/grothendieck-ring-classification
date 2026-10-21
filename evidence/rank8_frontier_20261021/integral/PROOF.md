# Integral frontier: a Rep(A5) complement obstruction

Status: exact computations and independent categorical review pass.
No claim that arbitrary integral fusion categories are unitary is used.

## The structural theorem

**Theorem.** Let C be a complex fusion category of dimension360 with a
fusion subcategory D tensor equivalent to Rep(A5). Suppose that the
complement has exactly three simples, all of dimension10, and that the
left and right D action matrices, in the dimension order1,3,3,4,5, are

    I, J, J, I+J, 2J-I,

where J is the three by three all-ones matrix. Then C is group-theoretical.

**Proof.** Write G=A5 and M for the full additive complement. The displayed
matrices preserve M, and J proves indecomposability as a left module, hence
as a bimodule. Use the symmetric structure on Rep(G) solely to identify
D-bimodules with modules over Rep(G x G); no braiding on C is needed.
Ostrik's classification (Theorem2 in [O]) identifies M with Rep_alpha(K)
for a subgroup K of G x G and a projective multiplier alpha. The positive
vector of ordinary vector-space dimensions of its three projective
irreducibles is an eigenvector of J with eigenvalue3, so it is (q,q,q),
with q a positive integer. The dimension of the twisted group algebra
therefore gives |K|=3q².

Let H1,H2 be the projections of K. Neither is G. Indeed Goursat's lemma
and simplicity of G show that a subgroup projecting onto G either is a
graph of an automorphism of G (if both kernels are trivial) or is a direct
product G x H (with possible interchange of factors). Every projective
multiplier sector of A5 has at least four irreducibles: the ordinary
sector has degrees1,3,3,4,5, and the unique nontrivial Schur-multiplier
sector has degrees2,2,4,6. For a direct product the multiplier splits,
since H¹(A5,C×)=0, and projective irreducibles are exterior products.
Thus both alternatives have rank at least4, contrary to rank(M)=3.

Multiplication by an ordinary character on projective characters is
diagonalized by evaluation on alpha-regular conjugacy classes. The
spectrum of the degree3 left action is3,0,0. The A5 character of degree3
vanishes exactly on its order3 elements. Hence H1 contains an element
of order3, and the same argument applies to H2. The proper subgroups of
A5 with such an element are C3,S3,A4. Their orders are3,6,12. Since |K|
divides |H1||H2|, the only possibilities compatible with |K|=3q² are

| Case | Order of K | q | Rank of the transformed complement | FP dimension there |
|---:|---:|---:|---:|---:|
| Case1 | 3 | 1 | 1200 | 1/2 |
| Case2 | 12 | 2 | 300 | 1 |
| Case3 | 48 | 4 | 75 | 2 |

Here is the asserted transformation and dimension calculation. Take the
connected separable algebra A=Fun(G) in D and let E={}_A C_A be its Morita
dual. Its diagonal subcategory {}_A D_A is canonically Vec(G), of dimension60.
The complementary category N={}_A M_A is obtained by taking modules over
Fun(G x G) in Rep_alpha(K). The action of K on G x G is free, so such
modules are projective equivariant vector bundles on a free K-set and
there is one simple for each orbit: rank(N)=3600/|K|. The Vec(G)-bimodule
actions are the two translations on this transitive G x G-set. All
simples of N consequently have the same FP dimension d. Morita
invariance gives dim(E)=360; subtracting the diagonal dimension60 gives
rank(N)d²=300, and therefore d=q/2. This proves the table.

The first row is impossible, since a simple in a fusion category has FP
dimension at least1. The second row makes all simples of E invertible,
so C is group-theoretical. In the last row both projection orders must
be12. Goursat's lemma forces K=A4 x_{C3} A4, with kernels V4 on both
sides, since the only normal subgroup of A4 of order4 is V4. Thus the
left G-stabilizer of any simple X in N is a conjugate of V4. As d(X)=2,
Frobenius reciprocity shows that XX* is exactly the sum of these four
invertibles. Products YY* for diagonal simples Y are the unit. Therefore
E_ad is pointed. It contains V4 and all its G-conjugates, so it contains
their normal closure G and is exactly Vec(G).

The universal grading expresses E as an extension of Vec(G). Each
homogeneous component is an invertible Vec(G)-bimodule by [ENOHT,
Theorem6.1]. A component containing X is, as a left Vec(G)-module, the
transitive module with stabilizer V4 and some multiplier psi; its dual
category is C(G,1,V4,psi). This dual cannot be pointed: choose g with
V4 intersect gV4g^-1=1 (distinct Sylow2 subgroups of A5 have trivial
intersection). The simple-object formula of [GN, Theorem5.1] then gives
a simple of dimension [V4:1]=4, independent of psi. But invertibility
requires this dual category to be Vec(G). This contradiction excludes
the third row and proves the theorem.

## Application to R8_3_3344

The source-bound verifier checks the unique proper subring on indices
[0,1,2,6,7], including all125 coefficients against the exact Rep(A5)
character tensor. It is simple and has dimension60. Thus any complex
categorification of it is tensor equivalent to Rep(A5), by [ENO,
Theorem9.12]. It checks all five left and right action matrices on
[3,4,5], the exact dimension character, and all closed based subrings.
The structural theorem therefore forces every categorification of
R8_3_3344 to be group-theoretical.

## Exhaustion of the group-theoretical presentations

A group-theoretical categorification has form C(L,omega,H,psi), with
|L|=360. The source tensor has only one invertible and its adjoint ring
is the entire ring. Thus its center has no nontrivial invertible: an
invertible central object must forget to1, and its half-braiding is a
tensor automorphism of the identity, hence a character of the universal
grading group. The centers of Morita-equivalent categories agree. Since
Z(Vec_L^omega) contains Hom(L,C×) as invertibles supported at1, L is
perfect. The complete SmallGroups catalogue at order360 has162 groups,
and exactly one is perfect: SmallGroup(360,118)=A6. This is independently
replayed in perfect_groups.g.

The identity double-coset sector of C(L,omega,H,psi) is Rep(H); hence H
is perfect as well. The perfect-group catalogue on all divisors of360
leaves proper possibilities of orders60 and120 only. The order120
possibility is excluded by the index3 action of the simple group A6.
Thus H=1,A5,A6. For H=1 the category is pointed; for H=A6, omega is
cohomologically trivial and the category has the Rep(A6) tensor, of
rank7. For any index6 subgroup H=A5, the coset action embeds A6 into S6
with image the unique index2 subgroup A6. Consequently an automorphism
of A6 carries H to the usual point stabilizer. This also treats both
conjugacy classes of A5 subgroups.

It remains to exhaust omega and psi for that point stabilizer. Equivalence
classes of pairs (omega,psi), under simultaneous cochain gauge, fit in

    H²(A6,C×) -> H²(A5,C×) -> H³(A6,A5;C×)
       -> H³(A6,C×) -> H³(A5,C×).

The first arrow is onto. To verify this without a table of A6 cohomology,
a6_relative_cohomology.py enumerates normalized mod2 bar cohomology on a
Sylow D8, and checks every cohomology class against all360 conjugations
for the Cartan–Eilenberg stable-elements condition. It then restricts to
the point-fixing V4, which is Sylow in A5. Its results are:

| Degree | H^degree(A6,F2) size | Kernel of restriction to V4 |
|---:|---:|---:|
| 2 | 2 | 1 |
| 3 | 4 | 2 |

The Schur multiplier of A5 is C2. This may also be seen for the needed
bound by restriction: odd Sylow subgroups are cyclic, and H²(V4,C×)=C2.
The nonzero mod2 degree2 class restricts nontrivially; since A5 and A6
are perfect, H²(-,F2) maps isomorphically to H²(-,C×)[2]. Thus it provides
an order2 class of H²(A6,C×) mapping onto H²(A5,C×), proving surjectivity.

Let B be the kernel of H³(A6,C×)->H³(A5,C×). Restriction followed by
transfer is multiplication by6, so B is annihilated by6. Its3-primary
part vanishes. In fact restriction to the Sylow P=C3 x C3 embeds that
part in H³(P,C×)=H⁴(P,Z), the three-dimensional F3 space with basis
x²,xy,y². The explicit even normalizer permutation saved in the verifier
rotates the two generators, so stable classes lie in the line spanned
by x²+y². Restriction to the coordinate C3 lying in A5 is injective on
that line. This proves B[3]=0.

For the2-primary part use the coefficient exact sequence
1->mu2->C×->[square]C×->1. It gives, naturally in the group,

    0 -> H²(-,C×)/2 -> H³(-,F2) -> H³(-,C×)[2] -> 0.

The map between the left terms for A6 and A5 is onto. Hence every
relative order2 class lifts to a mod2 class restricting to zero on A5,
and the table bounds the number of relative classes by2. The known
mu2 cocycle from the old R8_3_3342 certificate is a nonzero class in B:
its induced A4 stabilizer multiplier has commutator -1 on a commuting
pair of involutions. A trivial relative class would have trivial
multiplier. Thus B has exactly2 elements, and since H² restriction is
onto, the relative pairs have exactly2 gauge classes.

The zero class gives the untwisted double-coset construction, with five
Rep(A5) simples and four Rep(A4) simples, hence rank9. The nonzero class
is precisely the already constructed R8_3_3342 model. That construction
checks all512 tensor coefficients. It has
N(X_i,X_i;X_i)=2 for all three dimension10 simples, whereas R8_3_3344 has
N(X_i,X_i;X_i)=3 for all three. No permutation can identify them.
Therefore no group-theoretical presentation realizes R8_3_3344.
Together with the structural theorem this excludes every complex fusion
categorification of R8_3_3344.

## R8_3_731: complete simple-center induction obstruction

R8_3_731 is also excluded over C, by a different argument. Its source
hash is ee54e287f01aec4e2079b7f66309d89a659742e38164a3e47de1fea650eec48b.
The verifier checks integrality, dimensions [1,5,5,10,10,11,12,12],
dimension660, and absence of proper nontrivial fusion subrings.

### General scope and the prime-power filter

Any categorification C is integral, hence pseudo-unitary and spherical;
unitarity is not assumed. It is simple and nonpointed. If it were braided,
its Mueger center would be either Vec or C. The former would make C
nondegenerate, but its simple of prime dimension5 forces a nontrivial
symmetric subcategory by [ENO, Corollary7.2], contradicting simplicity.
The latter makes C symmetric, hence its underlying fusion category is
Rep(L). The complete ordinary-representation scan in
`evidence/rank8_m3_20261021/performance/group_scan/` treats all40 groups
of order660. Exactly one has the required rank and degree multiset; all
512 coefficients are compared up to based isomorphism, and it matches
the control R8_3_724 but not R8_3_731. The verifier binds the R731 receipt
to the source hash. Thus C cannot be braided.

By Liu--Palcoux--Ren, *Interpolated family of non group-like simple
integral fusion rings of Lie type*, arXiv:2102.01663, Theorem5.1,
Z(C) is simple. Its dimensions are integers, since the forgetful functor
preserves FP dimension and every simple of C has integer dimension.
It is nondegenerate. Therefore no nontrivial simple of Z(C) can have
prime-power dimension, again by [ENO, Corollary7.2]. This induction-matrix
strategy is explicitly described in Remark5.15 of the cited paper;
the new result here is its complete exact application with duality,
Gram completion, and joint tensor-rotation constraints to R731.

### Complete low-frame enumeration

Write B for the induction Gram matrix, so B=M M^t for the matrix of the
forgetful functor from Z(C) to C. The commutative ring has eight scalar
irreducible characters. Their formal codegrees are

    660, 4, 5, 5, 11, 11, 12, 12.

The eight distinguished columns in I(1) have unit multiplicity1; their
central dimensions are therefore

    1, 165, 132, 132, 60, 60, 55, 55.

The column for the center unit is fixed. For each remaining column v,
we require v_0=1, the exact dimension equation d.v=660/f, and
B-vv^t positive semidefinite. The native exact Gram ellipsoid enumerator
returns38058 candidate vectors in total; the seven dimension slices have
sizes65,61,61,31,31,37,37. The exact meet-in-the-middle row-sum enumerator
retains all frames satisfying the unit-row identity and
B-L L^t entrywise nonnegative and positive semidefinite, modulo only
permutations of identical-dimension distinguished columns. It returns
exactly450 frames. All450 are saved and fully re-enumerated by the
read-only verifier.

Because I(1) is self-dual, its restriction-column multiset must be
preserved by the source duality permutation [0,2,1,4,3,5,6,7]. Exactly434
frames fail this necessary condition. For each of the16 remaining
frames, put Q=(B-L L^t) restricted to the seven nonunit rows. Every
remaining central simple has zero unit multiplicity and yields a
nonzero vector v with Q-vv^t positive semidefinite. The exact enumerator
lists all such nonnegative integral vectors. Its central dimension is
d.v. The modular divisibility theorem implies that this integer divides
660, and the simple-center result excludes all prime powers. Thus every
actual high column occurs in the finite filtered list.

### Gram and joint rotation contradictions

For13 of the16 frames, the equations

    sum_v n_v v_i v_j = Q_ij,   n_v >= 0

already have a saved exact integer Farkas certificate after the
prime-power filter. The only remaining frame indices are293,301,303.
All second indicators are forced, in source nonunit order, to
(0,0,0,0,1,1,1): nonselfdual objects give zero, and the exact odd
multiplicity test forces +1 for each selfdual object.

For these three frames the verifier constructs the full joint Gram,
first/second central twist-moment, and tensor-rotation systems through
order6 using the existing exact rotation equations. The prime divisors
of the exponent are among2,3,5,11. All normalized rational trace vectors
(theta^k) for1<=k<=6 are exhausted by53 patterns obtained from divisors
of19800 together with the all-zero pattern. Here19800 is a trace-pattern
enumeration bound, not an asserted bound on the exponent. Higher prime
powers have zero traces at all six tested powers.

| Low frame | Admissible high columns | Trace patterns | Equations | Variables |
|---:|---:|---:|---:|---:|
| 293 | 280 | 53 | 182 | 14917 |
| 301 | 210 | 53 | 182 | 11207 |
| 303 | 324 | 53 | 182 | 17249 |

Every system A x=b, x>=0 has a saved integer vector y with
A^t y>=0 and b^t y<0. These inequalities are checked exactly, without
an LP solver, by `verify_central_731.py`. Each system is also bound to
a SHA256 recomputed from its entire integer matrix and right side.
Consequently all450 possible low frames are excluded:434 by duality,
13 by Gram completion, and3 by joint rotation. This proves that
R8_3_731 has no complex fusion categorification. The earlier unitary-only
obstruction is now supplemented by this independent general obstruction.
The printed F660 of [LPR] remains a different ring, R8_3_722.

## Reproduction and dependency boundary

    gap -q evidence/rank8_frontier_20261021/integral/perfect_groups.g
    python evidence/rank8_frontier_20261021/integral/structural_certificate.py
    python -O evidence/rank8_frontier_20261021/integral/structural_certificate.py
    python evidence/rank8_frontier_20261021/integral/a6_relative_cohomology.py
    python -O evidence/rank8_frontier_20261021/integral/a6_relative_cohomology.py
    python evidence/rank8_frontier_20261021/integral/verify_central_731.py
    python -O evidence/rank8_frontier_20261021/integral/verify_central_731.py

The Python verifiers recompute all tensor and local cohomology checks;
normal and optimized modes retain every validation. They bind the old
construction verifier by SHA256 and do not modify its evidence. The GAP
receipt relies explicitly on the complete SmallGroups and perfect-group
catalogues. The representation-category, Morita, stable-elements,
transfer, and coefficient exact-sequence results are mathematical inputs;
the scripts do not purport to formalize category theory.

## Primary references

[ENO] P. Etingof, D. Nikshych, V. Ostrik, *Weakly group-theoretical and
solvable fusion categories*, arXiv:0809.3031v2, Proposition9.11 and
Theorem9.12. https://arxiv.org/html/0809.3031v2

[O] V. Ostrik, *Module categories, weak Hopf algebras and modular
invariants*, arXiv:math/0111139, Section3.4, Theorem2.
https://arxiv.org/pdf/math/0111139

[ENOHT] P. Etingof, D. Nikshych, V. Ostrik, *Fusion categories and
homotopy theory*, arXiv:0909.3140, Theorem6.1 (invertibility of graded
components), and Section11.3 (central invertibles of pointed categories).
https://arxiv.org/pdf/0909.3140

[GN] S. Gelaki, D. Naidu, *Some properties of group-theoretical
categories*, arXiv:0709.4326, Section2.1 and Theorem5.1.
https://arxiv.org/pdf/0709.4326

[CE] H. Cartan, S. Eilenberg, *Homological Algebra*, ChapterXII,
Section10 (stable elements); also A. Adem, *On the geometry and
cohomology of finite simple groups*, Theorem1.3.
https://personal.math.ubc.ca/~adem/simple.pdf

[LPR] Z. Liu, S. Palcoux, Y. Ren, G. Vercleyen, *Triangular prism equations and
categorification*, arXiv:2203.06522; identification of the printed F660
is in the old source-bound f660_match.json.

GAP SmallGroups reference: https://docs.gap-system.org/pkg/smallgrp/doc/manual.pdf

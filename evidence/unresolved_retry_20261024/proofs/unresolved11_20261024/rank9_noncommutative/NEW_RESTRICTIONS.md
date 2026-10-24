# R9_2_1975: Morita and TY-sign restrictions

**The source ring remains unresolved.** The previously surviving three
rank-twelve Morita possibilities reduce to two, and the integral TY
subcategory must have negative tau. The excluded extreme
branch is ruled out by a tensor-autoequivalence obstruction, not by
claiming that its rank-six subcategory is excluded. A second argument
shows that any categorification of the source has no nontrivial
invertible object in its Drinfeld center. Neither statement supplies a
model or excludes the two uniform possibilities with negative tau.

## 1. Central twists obstruct invertible normalizers

Let C be a spherical fusion category with a unique pivotal structure.
Suppose its invertibles have unique lifts to Z(C), whose twists are
pairwise distinct. Every complex-linear tensor autoequivalence of C
fixes its invertibles individually: the autoequivalence preserves the
unique pivotal structure, its induced equivalence of centers preserves
twists, and the distinct twists distinguish the invertibles.

Consequently, if C is a fusion subcategory of D and an invertible r of D
normalizes C, then r centralizes Inv(C). Indeed, conjugation by r is a
tensor autoequivalence of C. No braiding on C or D is assumed.

The project's published center calculation for R6_4_155 gives precisely
these hypotheses. In basis 1,h,u,hu,X,Y, its rules include

    hX=X, uX=Y, X*=Y,
    XY=1+h+4X+4Y, X²=Y²=u+hu+4X+4Y.

Its tensor automorphism group of the identity is trivial, directly from
these products. The four central lifts have twists 1,-1,i,-i in a
positive spherical representative. The published general-to-spherical
and Galois reduction transports existence, uniqueness, and distinctness
back to every complex categorification. The detailed scope argument is
in the sibling `rank6_pair/POINTED_AUTOMORPHISM_OBSTRUCTION.md`.

The underlying published dependencies are
`manuscripts/rank6/papers/chapters/frontier_155.tex` and
`frontier_155_categorical.tex`, in particular the subsection “The
canonical intermediate condensation adds no new near-group category”,
at classification commit 323c4227ffb796a72eef506f1eb289437fbc95db.
This observation already occurs there for equivariantizations; the
normalizer application below is the new consequence.

## 2. The extreme rank-twelve branch is impossible

The prior complete Morita calculation for A=1+b5 gives three surviving
necessary tensors, labelled (alpha,a)=(2,0),(2,2),(3,2). Their pointed
group is D8 of order eight, and their other four simples have dimension
d=4+3sqrt(2). This calculation is recorded in
`rank9_m2_research/phase4/quadratic_noncomm/REPORT.md` and its exact
completion files, with the forced pointed associator examined in phase5.

In the extreme tensor (2,0), the basis

    (0,1,4,5,9,11)

is a dual-closed fusion subring, identified with R6_4_155 by the map

    (0,1,4,5,9,11) -> (0,3,4,5,1,2).

Conjugation by the invertible numbered 2 restricts to the permutation

    (0,1,4,5,9,11) -> (0,1,5,4,9,11).

Thus an actual categorification of this rank-twelve tensor would contain
a fusion subcategory C with ring R6_4_155, normalized by an invertible
whose conjugation exchanges two invertible classes of C. Section 1
forbids this. This rules out the extreme Morita branch, including its
previously recorded relabeling a=4.

Only the two uniform possibilities remain:

| alpha | a | duality shift in D8/Z(D8) |
|---:|---:|---|
| 2 | 2 | reflection coset |
| 3 | 2 | rotation coset |

For each, writing H=Z(D8) and Q=D8/H, their necessary fusion rules are

    gX_q = X_(q+gH) = X_qg,
    X_pX_q = sum_(gH=p+q+alpha) g + 2 sum_(t in Q) X_t.

The actual category would still need a coherent associator satisfying
the forced pointed restriction. These two tensors are not models.

## 3. The free isotropic involution has no half-braiding

In R9_2_1975, the based-central invertibles are exactly 1 and b5. The
adjoint subring is the whole ring. Hence a central lift of an invertible
is unique when it exists: two lifts differ by a tensor automorphism of
the identity, and this group is trivial.

Suppose b5 had a lift. Its square would be the central unit, by this
uniqueness. The integral TY subcategory has the nonalternating
bicharacter forced by the prior perpendicular-stabilizer argument, and
b5 is its isotropic involution. The standard formula for invertible
central objects of TY gives self-braiding chi(b5,b5)=1. Thus its lift
generates Rep(C2), and de-equivariantization gives a fusion category E
with the original category equivalent to E^{C2}.

The free orbits of b5 are {1,b5}, {b6,b7}, {b1,b3}, {b2,b4}; b8 is
fixed and splits into two simple objects under de-equivariantization.
Thus E has dimensions (1,1,1,1,d,d). In basis 1,h,u,hu,X,Y the quotient
functor has the following values:

| source objects | image |
|---|---|
| b0,b5 | 1 |
| b6,b7 | h |
| b8 | u+hu |
| b1,b3 | X |
| b2,b4 | Y |

Here h²=1, hX=X, uX=Y, X*=Y, and

    XY=1+h+4X+4Y, X²=Y²=u+hu+4X+4Y.

The pointed group is either V4 or C4. The two complete tensor bindings
are respectively

* V4: R6_4_155, via (0,3,4,5,1,2);
* C4: R6_4_1, via (0,5,1,2,3,4).

R6_4_1 already has a general-complex exclusion in the project. Its
complete source decision and provenance are bundled here in
`R6_4_1_dependency.json`, copied from
`rank9_m2_research/phase4/quadratic_noncomm/lower_tensors.json`. The
certificate kind is `oriented_pseudo_gate -> finite_indicator_traces`;
the exclusion uses the oriented pseudo-unitary gate and the exact higher
indicator obstruction, not any unitary classification premise.

For R6_4_155, every tensor autoequivalence fixes all four invertibles by
Section 1. In a C2-equivariantization each fixed invertible admits two
equivariant structures, since H²(C2,C*)=0. Thus E^{C2} would have eight
invertibles, contradicting the source's four. Both possibilities for E
are impossible. Therefore b5 has no central lift, and

    Inv Z(C) = {1}

for every hypothetical complex categorification C of R9_2_1975. This
does not imply C is nonexistent; centers with no nontrivial invertibles
occur for other fusion categories.

In fact, Z(C) has no nontrivial Tannakian subcategory. Its FP dimension
is (144+96sqrt(2))², and the quadratic norm of 144+96sqrt(2) is 2304.
If Rep(K) were a fusion subcategory, FP-dimension divisibility would
force every prime dividing |K| to be 2 or 3. Burnside's theorem makes K
solvable. Every nontrivial finite solvable group has a nontrivial
one-dimensional character, producing a forbidden nontrivial invertible
in Z(C). Since centers are invariant under categorical Morita
equivalence, no category in this Morita class has a nontrivial faithful
grading: such a grading would supply Rep(K) in its center. This is a
restriction on extension constructions throughout the Morita class.

A strengthening, supplied independently by the commutative rank-nine
investigation and checked against the primary theorem hypotheses, is

    Z(C)_int = Vec.

Indeed every central simple has FP dimension a+b d with a,b nonnegative
integers, by forgetting to C. Thus the integer-dimensional central
simples form a fusion subcategory E: a product of integer-dimensional
objects cannot contain a summand with positive coefficient b. The
integer FP dimension of E divides FPdim Z(C) in the algebraic-integer
sense, so has only prime factors 2 and 3. E is solvable, hence weakly
group-theoretical, by Etingof–Nikshych–Ostrik, *Weakly group-theoretical
and solvable fusion categories*, arXiv:0809.3031, Theorem 1.6. It has no
nontrivial Tannakian subcategory by the preceding paragraph, so its
core is E itself. Natale, *The core of a weakly group-theoretical
braided fusion category*, arXiv:1704.03523, Theorems 1.1 and 4.1, says
the core of an integral weakly group-theoretical braided category is
pointed. These statements do not require the braided category E to be
nondegenerate. Since Inv Z(C) is trivial, E=Vec follows.

For the categorical tools, see Gelaki–Naidu–Nikshych, *Centers of graded
fusion categories*, arXiv:0905.3117, the description of invertible
objects of TY centers; and Drinfeld–Gelaki–Nikshych–Ostrik, *On braided
fusion categories I*, arXiv:0906.0620, the equivariantization and
de-equivariantization correspondence. Neither requires unitarity.

## 4. The full stabilizer test admits a cochain

The remaining quotient action is the identity. The full stabilizer of
one noninvertible as a pointed left-right bimodule is

    L = D8 ×_Q D8 ≅ D8 × C2,

with projections p1(g,e)=g and p2(g,e)=gz^e, z the central involution.
An associativity obstruction is the difference p1*[omega]-p2*[omega].
The vanishing of this difference must not be mistaken for descent of
[omega] from Q. In particular, the following explicit cochain shows
that all the already forced cyclic restrictions are compatible with a
vanishing full stabilizer obstruction.

Use right semidirect coordinates g=(x,y,n) in F2³, with multiplication

    (a,n)(b,m)=(swap^m(a)+b,n+m),

so z=(1,1,0). Put omega=i^w, where, if (x',y')=swap^m(x,y),

    w((x,y,n),(u,v,m),(a,b,l))
      = l[3m(x xor y)+x'u+y'v+2y'u] mod 4.

This is an independently verified normalized cocycle. It is trivial on
the even V4, has class 2 on the rotation C4, and is trivial on the odd
reflection C2's. Multiplying by (-1)^{nml} flips the odd reflection
restrictions without changing the even or rotation restrictions, giving
the other allowed sign. These data are motivated by the explicit
Kac–Paljutkin pointed Morita cocycle in Etingof–Kinser–Walton, *Tensor
algebras in finite tensor categories*, arXiv:1906.02828, Examples 4.29
and 5.3. Our checked coordinate formula is specified explicitly here;
we do not depend on a convention-dependent transcription of that paper.

For A=(x,y,n,e), B=(u,v,m,f) in L, define beta=i^b by

    b(A,B) = 2nf+2nm+2yf+3ym+2ymf+2yu
             +yem+xm+2xmf+2xu+3xem+2xym mod 4.

Direct substitution gives

    delta b(A,B,C) = w(p1A,p1B,p1C)-w(p2A,p2B,p2C).

The same b works after the sign change, since n is unchanged by the
shear g -> gz^e. The checker verifies every cocycle and coboundary
identity for both signs with exact integers. This certificate rules
out an attempted contradiction from these stabilizer restrictions
alone. It is a pointed bimodule consistency witness, not an associator
for either full rank-twelve fusion tensor. Identifying every permissible
pointed class with this representative is unnecessary for this limited
non-exclusion statement and is not claimed here.

## 5. The positive TY sign is excluded

This additional argument uses the independently developed sibling
`rank9_commutative/TY_SPECTRUM.md`. Here Y=b8, chi is the same forced
nonalternating bicharacter on V4, and epsilon=sgn(tau). Shimizu's
general TY indicator formula gives

    nu_1(Y),...,nu_8(Y) = 0,epsilon,0,0,0,epsilon,0,2.

The defining invariant spaces and rotation operators lie in the full
TY tensor subcategory, so these indicators agree with the ambient ones
in the positive spherical representative. The existing reduction to
this representative is an existence reduction, which is enough to
exclude a sign branch. It does not claim that every original category
is unitary. More specifically, the established route Galois-conjugates
the D8 Morita category and transports back along the conjugate module
category. The TY parameters here lie in {1,-1} and tau in {1/2,-1/2},
so that field conjugation preserves this sign branch.

Writing I for induction to the center and D=FPdim(C), the center trace
formula gives

    D nu_n(Y) = sum_Z [I(Y):Z] dim(Z) theta_Z^n.

At n=8 it reaches its maximal possible absolute value 2D, so every
constituent of I(Y) has theta_Z^8=1. Fourier inversion says each of the
four primitive-eighth-root twist fibers has total weight D/4. If
epsilon=1, the theta=1 and theta=-1 fibers each have weight D/2 and
theta=±i are absent. If epsilon=-1, theta=±i each have weight D/2 and
theta=±1 are absent. The exact source tensor independently gives

    F(I(Y)) = 16Y + 16(b1+b2+b3+b4).

Impose this complete finite spectrum on every central restriction
column containing Y. At height six the two primitive-eighth-root
relative trace profiles over Q(sqrt(2)) are

    (sqrt(2)/2,0,-sqrt(2)/2,-1,-sqrt(2)/2,0)
    (-sqrt(2)/2,0,sqrt(2)/2,-1,sqrt(2)/2,0).

For epsilon=1 add the theta=±1 profiles; for epsilon=-1 add the
theta=±i profile (0,-1,0,1,0,-1). The second, fourth and sixth moments
are respectively D epsilon, zero, and D epsilon. All other center
columns retain the existing general trace-domain restrictions.

For epsilon=1 the resulting 259-by-1270 necessary system Ax=b, x≥0
has an exact integer Farkas separator y with

    b^T y = -32832,   min_j (A^T y)_j = 0.

Thus it has no nonnegative solution. Its height-four version already
has the same contradiction. Every hypothetical source category must
satisfy these center identities; hence positive tau is excluded. The
portable separator is `ty_spectrum_h6_tau1.json`, and its full exact
matrix is `ty_spectrum_h6_tau1_system.json.gz`.

For epsilon=-1 the corresponding 259-by-1251 system has both exact
rational and nonnegative integer feasible witnesses. The integer
witness has support 84. These are stored with the analogous `tau-1`
filenames and replayed exactly. Therefore the surviving source
possibilities are the two uniform Morita types with negative tau;
the finite center system does not settle them.

The source of the TY formula is Shimizu, *Frobenius–Schur indicators in
Tambara–Yamagami categories*, arXiv:1005.4500, Theorem 3.4. The center
trace identity is from Ng–Schauenburg, *Frobenius–Schur indicators and
exponents of spherical categories*, arXiv:math/0601012. The labeled
S-symmetry and central-column domain are the previously audited
phase3/noncomm1975 construction. In particular, the noncommutative
degree-two character multiplicities remain included. The new system
is generated by `ty_spectrum_center.py`; duality pairing is disabled
there, so filtering the trace types preserves a direct correspondence
between recorded variable keys and columns.

## 6. Exact replay and limits

The strengthened integral-center constraint was applied to the existing
complete labeled central-induction, modular-integrality, Galois-pairing,
S-symmetry, and height-six rotation relaxation. Seven nonunit integral
restriction columns were removed, reducing its expanded system from
1291 to 1109 variables, with 253 equations. Keeping the Galois-pairing
equations also forces away any now-forbidden dimension partners.
The earlier Z3 integer feasibility attempt timed out after 45 seconds;
a subsequent HiGHS mixed-integer proposal yielded an exact nonnegative
integer solution with support 80. Every equation was then checked with
integer arithmetic. A separate rational solution is also checked.

Consequently this strengthened necessary system still passes. This is
a completed finite test, not an unresolved solver run, and neither
witness is a fusion category. The packed matrix is
`no_integral_center_system.json.gz`; its witnesses and exact system
hash are in `no_integral_center_feasibility.json`. The main verifier
replays both witnesses without optimization software. The generator
`no_integral_center_feasibility.py` uses the prior phase3/noncomm1975
column construction to rebuild the system; its mathematical domain and
trace constraints remain prior dependencies, rather than a new proof
that all categorical data have been reconstructed.

Run `python verify_new_results.py` in this directory. It has no optional
dependencies and checks the 216-coefficient extreme subring binding,
its full conjugation permutation, both 486-coefficient quotient maps,
both 216-coefficient lower-rank bindings, the source adjoint and
based-central invertible claims, 16,384 cocycle/coboundary
identities, the finite TY indicator sums, the TY positive-sign separator,
and the strengthened center witnesses. Inputs and output are `new_results_inputs.json` and
`new_results_verification.json`.

The checker deliberately separates these exact finite checks from the
stated categorical dependencies. No online files or classification
ledger have been changed. The resulting status is still **unresolved**,
with two necessary Morita types remaining, negative TY sign, and no new model.

# R6_4_155: continuation and a conditional parent-group restriction

29 October 2026. **Status remains unresolved. No new model or general exclusion.**

This continuation rechecks the literature identification, the existing categorical
obstructions, and a possible near-group construction. It proves a new necessary
restriction on one precisely specified construction route. It does not turn that
route into a construction.

## 1. Literature identification and scope

The tensor is the non-self-dual ring R′(4), with basis 1,h,g,hg,X,Y and

\[
X^*=Y,
XY=1+h+4(X+Y),\qquad X^2=g+hg+4(X+Y).
\]

The August 2026 primary paper by Yue Meng and Zhiqiang Yu,
*Classification of some Z/2 × Z/2-quadratic fusion categories of rank 6*,
arXiv:2608.06064v1, explicitly retains this ring in Theorem 1.1 and Theorem 4.8.
Its new near-group de-equivariantization in Section 5 constructs R′(2), not R′(4).
Thus that paper supplies neither a categorification nor an exclusion here.
The paper's convention at Section 2.3 assumes spherical categories; general
complex scope must continue to use the project's separate sphericalization
argument, not silently attribute it to this paper.

Primary source: https://arxiv.org/html/2608.06064v1 .

The inherited project reduction gives d=4+3√2, D=72+48√2 and a unique necessary
rank-26 modular factor. Its complete modular data and tested cyclic spectra do
not supply associators. The prior Morita theorem excludes a search for a
different known based ring in the same Morita class. Its canonical intermediate
condensation is C ⊠ Rep(C2), so it does not provide the exchange action needed
for a new near-group category.

## 2. Conditional theorem for order-32 near-group parents

Here are the hypotheses, deliberately stated separately from any claim about
all near-group categories. Suppose a proposed parent has a modular center M
with these properties:

1. Its invertible objects form an abelian group G of order 32. Their pointed
   braided structure is described by a nondegenerate symmetric bicharacter χ
   on G, with twist q(g)=χ(g,g)^(-1).
2. Every noninvertible simple of M has FP dimension greater than 8.
3. A connected étale algebra E of dimension 8 has local modules M_E^0 braided
   equivalent, with positive ribbon structures, to the proposed R′(4) center.

These are the usual low-center-data hypotheses in the standard near-group
construction route. Their validity for an arbitrary unconstructed parent is
not asserted here. In particular this note does not infer a complete categorical
parameterization from a unitary classification or from numerical modular data.

**Theorem.** Under these hypotheses,

\[
G\cong C_4\times C_2^3.
\]

Moreover E is supported on a subgroup H≅C2³ satisfying

\[
2G\subset H\subset G[2],\quad q|_H=1,
\]

and the quotient quadratic group G/H is the four-object pointed center of
R′(4), with twists 1,-1,i,-i (up to conjugation).

**Proof.** By (2), E is a pointed algebra. A connected étale algebra in a pointed
category has one copy of each element of an isotropic subgroup H, so |H|=8.
For the quadratic form q, its associated monodromy bicharacter is

\[
b(g,h)=q(g+h)/(q(g)q(h))=\chi(g,h)^{-2}.
\]

Since χ is nondegenerate,

\[
\operatorname{rad}(b)=G[2].
\]

Every invertible object of M_E^0 has underlying M-object of dimension 8.
By (2), it is supported on G. The simple local E-modules in this pointed
subcategory are the cosets H^perp_b/H, each of module dimension one. The target
has exactly four invertibles, so |H^perp_b|/8=4 and H^perp_b=G. Therefore
H⊂rad(b)=G[2]. The quotient group is G/H≅C2², which also gives 2G⊂H.

It follows that G has exponent at most four and |G[2]|≥8. The only possibilities
are C4²×C2, C4×C2³ and C2⁵.

For C2⁵ all bicharacter values are ±1, so all quotient twists are ±1. This
cannot supply the two semion twists ±i.

For C4²×C2, H necessarily equals G[2]. Write generators e1,e2 of order four
and e3 of order two. Let A be the 2×2 symmetric exponent matrix modulo four
for χ restricted to <e1,e2>. Its reduction modulo two must be nonsingular:
a nonzero vector in its kernel would give a nontrivial radical element
2a e1+2b e2 of G. Twist-freeness on H gives χ(e3,e3)=1. Since A mod 2 is
nonsingular, there are a,b∈{0,1} such that

χ(e3,e_j)=χ(2a e1+2b e2,e_j), j=1,2.

Then e3−2a e1−2b e2 pairs trivially with e1,e2 and with e3, contradicting
nondegeneracy. This eliminates C4²×C2 and proves the theorem. □

This strengthens the previous exclusion of the three known two-generator
order-32 parents by identifying the only possible abelian group for a parent
within this larger, explicit low-center-data class. It is a route restriction,
not an exclusion of R′(4).

## 3. The surviving metric data really pass

The remaining group is not eliminated by this argument. On
G=C4×C2³, use coordinates (a,b1,b2,b3), and define

\[
\chi(x,y)=i^{aa'}(-1)^{b_1b'_1+b_2b'_2+b_3b'_3}.
\]

It is symmetric and nondegenerate. Set

\[
H=\{(a,b): a\equiv0\pmod2,
\ b_1+b_2+b_3\equiv0\pmod2\}.
\]

Then |H|=8, H⊂G[2], 2G⊂H and q|H=1. The quotient has twists
1,-1,-i,i. The restriction χ|H has a radical of order two, so the associated
alternating twisted group algebra has two two-dimensional simple modules.
Consequently the multiplicities required for splitting a noninvertible of
dimension 4d into two objects of dimension d are at least compatible with the
finite pointed calculation. This is only compatibility: existence of the
parent near-group category and of the required categorical structures remains
unproved.

The older near-group dimension comparison also leaves type (8,16). Schopieray's
classification excludes its elementary-abelian group C2³, but does not exclude
the other order-eight abelian groups by that theorem. Likewise it excludes
C2⁵+32, but does not address C4×C2³+32. It would be incorrect to extend the
elementary-abelian theorem to either mixed-exponent group.

Primary source: Andrew Schopieray, *Categorification of integral group rings
extended by one dimension*, Theorem 1.1 and Section 4,
https://doi.org/10.1112/jlms.12789 .

## 4. Exact verification and remaining gap

`verify_parent_restriction.py` verifies the original source tensor hash and
R′(4) labeling; checks every one of the 128 nondegenerate symmetric
bicharacters on C4²×C2 and finds none with twist-free G[2]; and verifies the
explicit surviving C4×C2³ example. The test uses standard Python and took
under one second. It invokes no optimizer or associator search.

The remaining issue is genuinely categorical: construct associators for R′(4),
construct an adequate parent and its algebra, or find an obstruction beyond
the inherited modular/indicator tests. Nothing in this continuation resolves
that issue. R6_4_155 must remain unresolved.

## 5. Check against the new infinite near-group construction

Radchenko–Wheeler, *Real quadratic fields and finite quantum dilogarithms I*,
arXiv:2609.21892v2, Section 5.4, Theorem 12 constructs a near-group category
from its finite-quantum-dilogarithm input. Corollary 6 proves existence for
G=Z/n×Z/m, with n,m≥1. The group C4×C2³ needs four generators, so this
existence corollary does not supply the surviving parent identified above.
Theorem 12 cannot be applied to it without constructing its additional
finite-quantum-dilogarithm input. No such input is provided by that paper's
two-generator construction. The same paper does not supply near-group
multiplicity 16 on a group of order eight, since its family has m=|G|.

Primary source checked:
https://arxiv.org/html/2609.21892v2 , Theorem 12 and Corollary 6.

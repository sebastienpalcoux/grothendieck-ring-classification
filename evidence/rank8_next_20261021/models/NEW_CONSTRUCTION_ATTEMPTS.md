# New construction reductions, 21 October 2026

R8_3_721 is now unitarily realized by the inherited-Q-system Morita construction
proved in `R721_QSYSTEM_CONSTRUCTION.md`. The other exact calculations in
`construction_reductions.py` are reductions of model-building problems. No
complete noncategorification of the other eight rings is claimed here.

## A rank-five Morita construction forced by the untwisted R1154 branch

Let a category C have ring R8_3_1154. Its nontrivial invertible is g=3.
Suppose its pointed associator class in H^3(C2,C*) is trivial. This hypothesis
is essential: g acts freely on all eight simples, so the elementary
fixed-simple argument does not force it. Under the hypothesis, the regular
algebra A=1+g is connected separable and the category of A-bimodules is a
Morita dual of C.

The left/right C2 double orbits are {0,3}, {4,5}, and {1,2,6,7}. Their
stabilizers have orders 2, 2, and 1. The stabilizer cocycles have two,
two, and one irreducible projective representations: H^2(C2,C*)=0.
Consequently the dual has exactly five simples, denoted 1,u,x,x',y, with
dimensions 1,1,a,a,2a+2, where a=6+3 sqrt(5). The character of C2 gives
u^2=1, ux=x', uy=y on both sides. The ordinary double-orbit/projective-
stabilizer description is being applied to the existing algebra A; it
does not assert that this algebra exists in the twisted branch.

Dimension comparison and Frobenius reciprocity now force

    xy=x'y=4x+4x'+9y,
    y^2=1+u+9x+9x'+19y.

If x is self-dual,

    x^2=(x')^2=1+m x+(4-m)x'+4y,
    xx'=u+(4-m)x+m x'+4y,  0<=m<=4.

Replacing x by x' interchanges m and 4-m. If x*=x', duality forces m=2,
and the occurrences of 1 and u in the last two equations are exchanged.
The verifier checks every fusion coefficient, associativity, reciprocity,
duality, and the positive dimension character for all six labelled tensors.
These are candidate rings for the mandatory dual, not constructed categories.

This construction produces a new necessary condition. The common dimension
is D=540+240 sqrt(5). All center-simple dimensions must lie in Q(sqrt(5)),
because forgetting to C expresses them as integral linear combinations of
the eight source dimensions. For the m=1,3 duals, the two formal codegrees
8+4 sqrt(2) and 8-4 sqrt(2) would force distinguished center dimensions
D/(8+4 sqrt(2)) and D/(8-4 sqrt(2)), outside this field. Thus these dual
branches are impossible.

For m=0,4 the two additional distinguished dimensions are
15+6 sqrt(5) and 255+114 sqrt(5). For m=2, including its non-self-dual
version, two distinct distinguished simples have dimension
D/4=135+60 sqrt(5). R1154 already has one such distinguished simple.
Using the complete fixed-low-frame high domain of the preceding campaign,
these alternatives require

    high[10] >= 1 OR (high[3] >= 1 AND high[14] >= 1).

In the pseudo-unitary setting the indicated additional distinguished
simples all have twist 1. The new R1154 fourth-moment campaign reports
224 remaining patterns, with high[3]=high[14]=0 throughout and high[10]
equal to 0 in 112 patterns and 4 in 112 patterns. Thus 112 patterns cannot
belong to the untwisted pointed branch. This is not an exclusion of those
patterns in the twisted branch, and it does not provide a general exclusion
of R1154. The explicit m=2 rank-five dual rings initially provided the
remaining model-building targets. A stronger check now excludes them too.

All four isomorphism types have maximum fusion multiplicity 19. Applying
the repository's exact rank-five engine directly to each entire tensor
produces a `signed_extension_positive` noncategorification certificate
in every case. These certificates include the signed/spherical branches
and the pseudo-unitary indicator obstruction when needed; they are not
merely numerical searches or an appeal to a census count. They are saved
in `rank5_dual_exclusions.json` and replayed by `verify_rank5_duals.py`.

**Consequence:** assuming the categorical double-orbit reduction above,
the entire trivial pointed-associator branch of R1154 is impossible.
Every categorification would therefore have nontrivial pointed associator;
in the pseudo-unitary normalization its invertible g must have
Frobenius--Schur indicator nu_2(g)=-1. The twisted branch remains open.

The center induction formula used here is the standard formal-codegree
formula: a one-dimensional representation with formal codegree f contributes
a distinguished center simple of dimension D/f. The argument is unconditional
for a pseudo-unitary categorification. Extension beyond that setting requires
the spherical/Galois reductions already used by the main campaign.

## Testing a common Morita construction for R1154 and R1795

Their Casimir characteristic polynomial agrees exactly:

    (t-20)(t-10)^4(t-4)(t^2-1080t+3600).

In R1154 the four-dimensional 10-eigenspace is the noncommutative 2-by-2
matrix block. In R1795 it consists of four one-dimensional characters.
Thus a common pseudo-unitary center must contain four distinct twist-one
simples of dimension D/10=54+24 sqrt(5). In the R1154 high domain these
can only be high-column 2. This is a concrete compatibility condition,
not a Morita equivalence. Among the 224 new R1154 fourth-moment survivors,
68 have four such objects and 156 have none. Only 34 simultaneously have
high[2]=4 and high[10]=4. No multiplication or commutative separable algebra
on the resulting Lagrangian-object candidate has been supplied.

The direct C2-algebra Morita construction from R1154 has rank five, so it
cannot itself produce rank-eight R1795. A larger algebra or a further
Morita step would be needed.

## The common quartic quotient and limits of zesting

The verifier independently computes the central free involution quotients
of R928, R941, and R982 and checks all 64 quotient structure constants
under a basis permutation. All three are the same rank-four based ring,
historically F_{6,19}. This extends the existing R941 observation to an
explicit three-ring correspondence. It does not imply an ordinary rank-four
category: centrality in the Grothendieck ring is not a central bosonic lift.
The earlier R928 and R941 center work forces semionic and fermionic lifts,
respectively, which demand different categorical reconstruction problems.

All nine source rings have full adjoint closure, checked directly from their
512 structure constants. Therefore none admits a nontrivial faithful group
grading. Ordinary associator twisting or tensor-product zesting along a
nontrivial faithful grading cannot produce these target rings: the grading
survives that construction. This restriction does not cover arbitrary
super/para associators or noncentral algebra Morita constructions.

No known rank-four supercategory with this quotient tensor was found.
The direct rank-two-by-rank-two supercategory route was already excluded in
the preceding campaign. Forgetting the parity of a superfusion pentagon
solution is not an ordinary fusion-category construction and is not used.

## An all-Lie-type dimension obstruction for R721 and R1768

This is a scoped exclusion of model families. Gannon--Schopieray determine
the global-dimension fields of every affine quantum-group category
C(g,k). The quadratic fields occurring are Q(sqrt(2)), Q(sqrt(3)),
Q(sqrt(5)), Q(sqrt(6)), and Q(sqrt(21)); neither Q(sqrt(17)) nor
Q(sqrt(37)) occurs.

For a Deligne product C of affine categories, its global-dimension field is
the compositum of the factor global-dimension fields. Here is a direct proof
that avoids the generally false assertion that arbitrary products generate
the compositum of their factors. Form the actual object
R=direct_sum_X X tensor X* in C. It has FP dimension D=FPdim(C).
For a factor C_j, the subobject with X in that factor and unit in the
others has FP dimension D_j. Gannon--Schopieray Lemma 1.1 applied to this
positive additive decomposition gives D_j in Q(D). The reverse containment
follows from D=product_j D_j. Pointed factors have rational global dimension.

Consequently no such product has field Q(sqrt(17)) or Q(sqrt(37)): each
factor field would have to be contained in the relevant quadratic field,
and hence would have to be rational. R721 has
D=136+32 sqrt(17), and R1768 has D=444+72 sqrt(37).

The obstruction persists under any finite sequence of operations which
multiply global dimension by a positive rational number or preserve it:
finite group extensions, equivariantizations, Tannakian de-equivariantizations,
pointed Deligne factors, and Morita equivalences. It also applies to their
centers, since squaring these two positive quadratic dimensions preserves
the field. It does not cover arbitrary noninvertible algebra condensation,
taking arbitrary fusion subcategories, or non-affine source categories.

## Fresh literature and catalogue attempt

### Exact known-center identification for R721

The new R721 modular completion is exactly the modular data in
Grossman--Izumi, arXiv:1906.07397v2, Definition 6.1 and Section 6.1.6,
with metric groups

    G=C4 x C4, q1(x,y)=zeta8^(x^2-y^2),
    Gamma=C17, q2(l)=zeta17^(3*l^2).

The independent script `r721_gi_identification.py` reconstructs the paper's
formula and matches all 484 S entries and all 22 T entries exactly, under
the permutation saved in `r721_gi_identification.json`. It passes with
Python assertions disabled. The source completion is bound by SHA256.
This is stronger than a dimension or twist-spectrum coincidence.

Section 6.1.6 and arXiv:1501.07679v2, Example 6.10, identify these data as
the center of the C2 de-equivariantization of the known Z8 generalized
Haagerup category. The ordinary Asaeda--Haagerup center instead belongs
to Section 6.1.5 and has different twists. Thus the matching center data
are known, and should not be advertised as new modular data.

The R721 restriction columns specify the possible Lagrangian object

    L = 0 + pi + g_(1,1) + g_(1,3) + 2 k_(2,2,+).

Here the labels are those in Definition 6.1. Switching the sign on the
last label preserves S and T; this fact alone does not supply a braided
autoequivalence or an algebra structure. The known de-equivariantized
generalized-Haagerup ring has four invertibles, four noninvertibles of
dimension delta=4+sqrt(17), and multiplicity two. It is not R721. Its
canonical Lagrangian object has multiplicity pattern 1,1,1,1,2 with the
double multiplicity on a dimension-34+8sqrt(17) object, whereas R721 has
double multiplicity on a dimension-17+4sqrt(17) object. Transporting its
canonical algebra by the indicated sign permutation therefore does not
establish the R721 algebra.

This construction has now been completed using the actual algebra 1+rho.
The complete free-bimodule Gram enumeration, known-center canonical-algebra
rank constraints, and an explicit Q-system conjugacy obstruction force its
Morita dual to have rank eight and the R721 dimensions. Exact rational
inequalities bound every dual fusion coefficient by three. Exhausting all
4,500 rank-eight rings of multiplicity at most three then identifies the
entire ring uniquely as R8_3_721. The detailed theorem and source-bound
certificates are in `R721_QSYSTEM_CONSTRUCTION.md` and
`r721_dual_multiplicity_bound.py`; independent reviews are recorded there.

The Anyon Atlas, arXiv:2610.25439v1 (18 October 2026), supplies numerical
modular-data searches through bosonic rank 22 and fermionic rank 26,
with exact reconstruction of retained data. Section 4 explicitly does not
claim the numerical search is complete. Section 4.2.1 also explains why
modular-data condensable-algebra candidates are insufficient without
associativity/commutativity. We use neither catalogue absence nor a modular
data match as a categorification proof.

The public catalogue was searchable but did not provide full records through
the available read-only retrieval (direct HTTP returned 403). A search
located B22-02164, with dimension 71791.5114 and objects of dimension
17+4 sqrt(17), a plausible Asaeda--Haagerup-center lead. Full S,T and
algebra data were not retrieved, so no match is claimed. The independent
R721 campaign in fact finds forced twists different from the standard
Asaeda--Haagerup center. All six known Asaeda--Haagerup Morita categories
were already excluded as exact models in the earlier campaign.

Primary references:

- S. Yamagami, *Group symmetry in tensor categories and duality for orbifolds*,
  https://doi.org/10.1016/S0022-4049(01)00028-7 , for the left/right
  invertible-object group actions and their stabilizer description.
- S. Burciu and S. Natale, *Fusion rules of equivariantizations of fusion
  categories*, Corollary 2.13,
  https://arxiv.org/abs/1206.6625 , for the orbit/projective-stabilizer
  classification. Its semisimple orbit argument applies to the H-by-H
  linear action describing A-bimodules; the dual tensor product is over A.
- T. Gannon and A. Schopieray, *Algebraic number fields generated by
  Frobenius--Perron dimensions in fusion rings*, Lemma 1.1, Figures 1--2,
  https://arxiv.org/abs/1912.12260 . The published title omits
  ``Frobenius--Perron''; the Anyon Atlas cites the 2024 version.
- J. Berean-Dutcher, C. Cordova, J. Parra-Martinez, R. Tuddenham,
  *The Anyon Atlas*, Sections 1.4 and 4.2.1,
  https://arxiv.org/abs/2610.25439 .
- P. Grossman, M. Izumi, N. Snyder, *The Asaeda--Haagerup fusion categories*,
  https://arxiv.org/abs/1501.07324 .
- D. Aasen, E. Lake, K. Walker, *Fermion condensation and super pivotal
  categories*, https://arxiv.org/abs/1709.01941 .
- C.-M. Chang et al., *Topological Defect Lines in Two-Dimensional Fermionic
  CFTs*, https://arxiv.org/abs/2208.02757 .
- J. Chen, B. Haghighat, Q.-R. Wang, *Para-fusion Category and Topological
  Defect Lines in Z_N-parafermionic CFTs*,
  https://arxiv.org/abs/2309.01914 . These generalized condensation
  frameworks do not themselves supply the missing F_{6,19} associators.

The verifier is reproducible with
`python evidence/rank8_next_20261021/models/construction_reductions.py`
and the same command under `python -O`.

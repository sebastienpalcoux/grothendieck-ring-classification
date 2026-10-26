# Further family audits

## D48 conditional group-theoretical catalogue

All 104 cases are independently checked. This sentence is conditional on
the complete group/subgroup/cohomology inventory, separately reviewed by
the D120 auditor. It does not infer that an arbitrary dimension-48 category
is group-theoretical.

For the 92 H4/H8 cases, `audit_d48_catalog.py` checks the complete source
3-cocycles, the actual algebra equation `delta(psi)+omega|H=0`, all left,
right and mixed monomial module equations, simple Hom spaces, and dimension
exhaustion. It independently reconstructs all 1,728 coefficients for each
of the 40 multiplicity-one cases and the explicit offending coefficient
for each of the 16 higher-multiplicity cases. The other 36 categories have
the certified wrong rank.

For the 12 H16 cases, `audit_h16_independent.py` does not import the discovery
fusion formula. It certifies each projective character by constructing the
corresponding central idempotent in the actual twisted group algebra.
Centrality, pairwise orthogonality, completeness, twisted-center dimension,
and regular-block traces establish that these are precisely the actual
irreducible characters, not merely orthonormal lists. The balanced tensor
character is independently recomputed by summing over all group
factorizations with a different choice of transport. Six complete rank-12
tensors match only R30/R417; the other six categories have rank18. Frozen
source inputs and checksums are in `h16_frozen`.

## D48 soft triality automorphisms

I checked the proposed lemma in `d48/triality_soft_automorphisms.md` against
Edie-Michell, *Equivalences of graded fusion categories*, arXiv:1711.00645v2,
Lemmas6.8--6.9 and Theorem8.1. The crucial distinction is handled correctly:
systems of equivalences for a fixed neutral identification form a Z1
torsor. Vanishing H1 alone would not remove arbitrary inner tensor
autoequivalences. Here the actual fixed-space decomposition
`B=B^c direct-sum V4*` says every coboundary can be produced by changing
that neutral identification by a character. This kills the entire Z1
torsor; the remaining H2(C3,C*) is zero. The six-element parabolic
normalizer then bounds the tensor autoequivalence group by S3.

For a group P of order4, positive cohomology with its C3 coefficient module
vanishes by averaging. Thus any action is equivalent either to the trivial
action or to a pullback of the actual C2 action exchanging the two
dimension-two triality objects. Its kernel acts by one fixed character
on each product, so the known multiplicity2 cannot be distributed between
the two possible equivariant lifts. The claimed multiplicity obstruction
is sound. Its application still requires the separate categorical proof
that the dimension-48 candidate is such an equivariantization.

## D144 necessary Morita structure and alternate extensions

The detailed chain in `d144/new_morita_reduction.md` is accepted through
the conclusion that the full Morita dual has type
`1^24,2^12,(sqrt2)^36`, with adjoint category genuinely `Vec(V4)`.
In particular the regular Rep(S3) algebra is actual, the intermediate
module internal-end argument retains all subgroup cochains, and the
stabilizer divisibility lemma uses the matching twisted regular algebra
determined by the fixed object. It does not assume H2 of a noncyclic
stabilizer is zero.

The corrected four-dimensional quadratic-space coordinates are coherent:
the orthogonal sum of two anisotropic planes has diagonal electric
Lagrangian; its stabilizer is explicitly diagonal S3 times factor-swap.
The two permissible index-two grading groups are S3 times S3 and
`(C3 times C3) semidirect C4`. The actual coefficient module has no fixed
vectors under its normal C3 times C3, hence all its cohomology vanishes.

The proposed alternate extension obstruction argument is valid provided
the restriction to C3 times C3 is bound to the same BrPic homomorphism as
the known triality reference. Uniqueness of that multiplication system
makes its fourth obstruction vanish on this Sylow3 subgroup. The cyclic
Sylow2 subgroup C4 has H4(C4,C*)=0, and restriction-transfer kills both
primary components. Thus the alternate extensions exist.

For this alternate grading group the 2-primary H3 is inflated from C4;
the 3-primary H3 consists of the invariant quadratic form x^2+y^2.
Restriction to the reverse diagonal S3 is onto H3(S3,C*) and has kernel
C2. Therefore there are two marked alternate twists admitting the
reverse S3 algebra. This proves existence of candidate categories, not
identification of any of the four unresolved rank-12 tensors. No D144
full-ring exclusion or realization is accepted on this basis alone.

## D144 final closure after the additional local and tensor arguments

The preceding caution describes the intermediate extension-existence
step. The additional arguments now close the whole family. I accept
R12_1_320 as modeled, and R12_1_180,R12_1_181,R12_1_321 as excluded from
general complex categorification.

The complete base-branch count is twelve marked relative H3 classes.
The actual three-fermion gaugings distinguish three first-axis C3
parameters and two first-axis defect signs. A cup-product cocycle
`(-1)^[eta(u) epsilon(v) epsilon(w)]` is trivial on the reverse S3 and
changes precisely the left bimodule tensor action on odd times odd by
its sign charge. It therefore realizes the already-audited central
zest. Distinct fusion rules make this class independent from the
defect-sign difference, exhausting the four relative 2-primary classes
for each of the three 3-primary parameters. No target of the unresolved
family lies in this base branch.

For the alternate branch, the affine Galois-origin argument is now
properly marked. A field automorphism fixing Q(zeta8) and inverting zeta3
fixes the actual BrPic data, acts by minus one on the N=C3^2 H3 torsor,
and consequently has exactly one fixed marked extension class. The
complete marked m=0 first-axis table is over Q(i,sqrt2); together with
the trivial reverse diagonal algebra this proves that its N restriction
is this fixed point. Every admissible alternate restriction is fixed
for the same diagonal reason. Comparing the integral order18 subgroup
then removes its remaining C2 twist by restriction to the reverse S3.
Thus its actual integral inverse is the known m=0 category. The source
table/marking premise was independently inspected in
`c6/audit_d144_galois_anchor.md`. This excludes R181/R321 by their distinct
integral-ring invariant.

The local C4 bridge is an existence argument, not a finite failed search.
The actual Liptrap source a10 has neutral Vec(V4), with exact neutral
coboundary f(5,5)=-1. I independently replayed all2304 defining identities,
all64 unitary Fourier blocks, and all64 neutral coboundary equations.
The six eligible order-four BrPic elements are one pointed-parabolic
conjugacy class; their natural coefficient module is the regular F2[C4]
module, so H2(C4,M)=0. Every actual alternate extension therefore has this
same local fusion tensor, up to scalar associator twists. Both possible
reverse C2 complements are conjugate by the neutral group; I checked
each directly. In either marking, sXs=X but X* differs from sX.

This local fact determines the actual global S3-bimodule supports:
two odd support orbits of size18, each with cyclic stabilizer2. Their
two projective characters produce four odd simples of dimension3sqrt2.
Duality exchanges the two support orbits, so no odd simple is self-dual;
this excludes R180. No claim that the entire pointed S4 associator is
trivial is used: only its specified S3 restriction is trivial.

For the existence claim, the actual inverse category is known to exist
and its full fusion tensor is forced as follows. The sign charge swaps
the two characters in each support pair; the standard charge acts by
I+Z. The integral m=0 rules force the three dimension-four action matrices
to coincide. The symmetric P action has row sum3, and on the Z eigenspaces
satisfies P_+^2=3I+2P_+ and P_-^2=I. Indecomposability removes the diagonal
P_+=3I possibility. The remaining plus action is [[1,2],[2,1]], and
integrality forces P_- to have independent diagonal signs. The other
even action matrices are then all-ones. Thus there are precisely four
P choices and two possible odd duality involutions, with all other
products determined by Frobenius reciprocity. This derivation imposes
no unproved multiplicity-one bound.

`audit_d144_local_and_tensor.py` independently constructs all eight
tensors. The equal-sign blocks fail associativity; the four remaining
choices all match every one of the1728 original R320 coefficients.
The receipt is `d144_local_and_tensor_independent.json`. Hence the
abstract alternate extension, with its actual reverse algebra, is a
realization of R320. This final step repairs the earlier gap between
precursor existence and identification of a specific census tensor.

## D48 final closure without a census-completeness premise

I accept all twenty retained D48 targets as excluded after the additional
quotient reconstruction and categorical arguments. This does not assume
that every intermediate ring already occurs in the rank12 census.

For the rank12 dimension24 quotient branch, the invariant orbit tensor
forces a group of eight invertibles and four two-dimensional simples.
The reconstruction enumerates all five groups of order8, every
involutive group automorphism with the required fixed points, all left
and right actions on the four remaining objects, and all commuting
dual involutions. Frobenius reciprocity determines coefficients with
an invertible output. Every remaining coefficient is at most the
corresponding nonnegative invariant orbit sum, which is at most1 in
the actual inputs. The union constraints are necessary Frobenius,
duality, involution, and invertible-associativity equations; they impose
no extra hypothesis. Every binary assignment is tested against all
dimension, orbit-sum, and associativity equations.

My fresh replay binds all twenty physical sources and all56 central
involution branches. It checks all704 valid full quotient tables against
R351/R513 before deduplication, and checks all1408 returned isomorphisms
coefficient by coefficient. The receipt is
`quotient_reconstruction_independent.json`. The new theoretical
group-theoretical converse for these quotient types and their integral
involutive extensions is in `d24_c3_pointed_extension_lemma.md`.

The rank9 branch is likewise reconstructed without presuming a grading.
There are only two possible groups of four invertibles. All five-point
actions, dualities, and required coefficient equalities are enumerated.
The invariant orbit equations and dimension equations give finite
nonnegative integer bounds for all remaining coefficients. I compared
the propagation solver to independent complete Cartesian enumeration
for every one of192 systems: there are14 distinct systems and the
largest complete integer grid has only16 entries. All12 source bindings
are checked on their entire orbit tensors. Four source rings have no
associative lift. The two surviving based rings, with respectively V4
and C4 invertibles, have trivial universal grading and exactly one
central involution, which fixes all five noninvertibles. These properties
were checked on every valid table before deduplication. Neither survivor
has the previously conjectured C3 grading, and no such grading is used.
The receipt is `rank9_quotient_reconstruction_independent.json`.

For completeness, the categorical closure of these last two survivors
is as follows. Their dimension24 categories are solvable. Trivial
universal grading forces the last prime step to be an equivariantization.
The prime3 is impossible because the invertible group has order4; hence
D=E^C2. The corresponding central involution must be the unique one in
the ring. Since it fixes all five two-dimensional simples, forgetting
equivariance splits each into two invertibles; the other source pairs
give two more invertibles. Thus E is pointed of dimension12.

The actual central lift of this involution is unique: two half-braidings
on a fixed invertible differ by a tensor automorphism of the identity,
and this group is Hom(U(D),C*)=1. The outer actual C2 action therefore
preserves the central Rep(C2). Its equivariantization is a Tannakian
Rep(P) of dimension4: forgetting to Rep(C2), and then to vector spaces,
provides a symmetric fiber functor. Iterated de-equivariantization gives
the original dimension48 category as E^P for a group P of order4.
Equivariantizations of pointed categories are group-theoretical. This
closes the branch using an actual preserved central subcategory, not
just a ring-level fixed invertible.

Together with the independently checked full group-theoretical
catalogue, the near-group branch lemma, and the separately reviewed
free-rank6/triality branch reduction, these arguments close all twenty
D48 cases. Their classification does not rely on a unitary-only table
without an appropriate categorical bridge.

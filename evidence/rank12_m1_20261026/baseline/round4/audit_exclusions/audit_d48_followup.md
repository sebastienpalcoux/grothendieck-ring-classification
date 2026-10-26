# Independent D48 follow-up audit

## Relative restrictions and frozen-category bindings

I read `../d48/restriction_certificates.py` and replayed it with Python `-O`.
It reports 432 restrictions: 386 inadmissible, 46 admissible, and exactly 92
frozen categories accounting for every subgroup Schur class.

For each negative case the saved row vector y is checked directly against the
original bar differential A: yA=0 modulo 8, but y(-omega) is nonzero. The
row/column reduction is only a way to discover this certificate; its validity
does not depend on trusting that reduction. Each positive case checks its
actual cochain against A. The parameter key, group table, subgroup, full
associator table and full relative cochain table then bind every positive
Schur refinement to the frozen fusion computation. Every frozen case is used
exactly once. The previously audited fourth-root/eighth-root exponent lemma
upgrades the negative finite-phase certificates to U(1) nontriviality.

Result: PASS for the restriction filtering and exact relative-case coverage.
This is a conditional group-theoretical coverage statement, not by itself a
proof that a hypothetical census category is group-theoretical.

## Triality soft automorphisms

I read `../d48/triality_soft_automorphisms.md` and the primary statements in
Edie-Michell, *Equivalences of Graded Fusion Categories*,
https://arxiv.org/html/1711.00645v2, Definition 2.6 and Lemmas 6.8, 6.9, 7.5.
The use of systems of equivalences as a Z1 torsor, followed by the H2 scalar
tensorator torsor, agrees with those statements. In particular the article
initially fixes the natural isomorphism on the neutral category. Removing
that restriction really does allow the character coboundaries described in
the draft; they must not be discarded merely by citing H1=0.

There is a useful independent interpretation of the same calculation.
Let A=Vec(V4), let B=Inv Z(A), and let c be the triality isometry for a
non-group-theoretical dimension-twelve category T. The exact finite linear
algebra establishes B^c -> V4 is an isomorphism. An invariant central
invertible t of A acquires a C3-equivariant structure because its sole
projective-representation obstruction lies in H2(C3,C*)=0. Relative-center
equivariantization therefore lifts it to an invertible of Z(T). Thus every
underlying neutral invertible a has a central lift in T, and every Ad_a is
tensor naturally trivial.

After the nontrivial H2(V4,C*) shear has been ruled out by noncommutation with
c, a soft autoequivalence restricts tensor-isomorphically to Id_A. The H1=0
calculation expresses its component system as a coboundary of some t in B.
Such a coboundary is the component system of conjugation by the underlying
invertible a, with the chosen neutral half-braiding t. That inner functor is
trivial by the preceding paragraph. The remaining tensorator difference is
H2(C3,C*)=0. This independently confirms the neutral-character quotient in
the draft and the vanishing of the soft automorphism group.

For the stated action of a group P of order four, the homomorphism on tensor
autoequivalence classes consequently factors through the reflection C2.
The automorphism group of the identity tensor functor is C3. Its positive
cohomology for P and for C2 vanishes, regardless of their action, since their
orders are invertible on C3. The categorical action is therefore equivalent
to the pullback of the reflection action. Its kernel acts with one fixed
character on a tensor product of two orbit objects. The two copies of each
nonneutral simple in the underlying tensor product must then enter the same
equivariant lift, giving coefficient two. The draft's exclusion of this
specific multiplicity-one equivariantization branch is valid.

This audit does not independently establish the parent's antecedent reduction
of every relevant dimension-48 category to the stated order-four action.

### Normalizer strengthening

I also read and replayed `triality_orthogonal.py`, and directly checked the
saved normalizer data for each of its four non-group-theoretical triality
elements. In every case the parabolic normalizer has six elements with
distinct induced V4 automorphisms, element orders 1,2,2,2,3,3, and grading
action -1 for each involution. The calculation enumerates all 4-by-4 binary
matrices preserving the hyperbolic quadratic form and all planes, so these
are complete finite domains. The normalizer projects bijectively to GL(V4).

Every tensor autoequivalence preserves the canonical pointed category and
grading. Edie-Michell's compatibility condition places its neutral isometry
in this normalizer. The normalizer projection and the soft-kernel result
therefore give an injection Aut_tensor(T) -> S3. Consequently every action
by a group of order four has image either trivial or the reflection C2.
For trivial image, H2(P,C3)=0 makes the categorical action equivalent to the
trivial action; T tensor Rep(P) retains rho^2=2 rhobar. For nontrivial image
the preceding reflection argument applies. Thus **every** order-four-group
equivariantization of such a non-group-theoretical T has multiplicity at
least two.

## Group-theoretical triality branch

I independently read the published Jordan--Larson statements at
https://ems.press/content/serial-article-files/30464 . Theorem 1.4 gives six
categorifications for R_(3,V4); Theorem 1.1 gives exactly three non-GT
dimension-twelve classes. Their Definition 2.8 confirms the equivalence is
ordinary tensor equivalence, not merely Morita equivalence or a fixed-grading
equivalence. Thus three pairwise tensor-inequivalent GT models with this ring
exhaust the GT part.

For H=C2 in V4 normal in A4, the proposed models
C(A4, inflation(kappa^j), H, 1), j=0,1,2, have double-coset sizes 2,2,4,4
and stabilizer orders 2,2,1,1. The invertible sector is V4/H x Hhat=V4;
the two nontrivial C3 grades each have one dimension-two simple. This forces
exactly the R_(3,V4) rules. The cocycle is identically one whenever any
argument belongs to V4, so the subgroup algebra and neutral group calculation
are valid without a hidden adaptation.

I read Schauenburg's adapted-cocycle Theorem 4.2 and the defining recursion
for pi_m at https://arxiv.org/pdf/1502.02906 . For either nonneutral
representative r, both elements of rH are 3-cycles with trivial stabilizer.
For quotient exponent a=1 or 2, the product of the three cyclic cocycle
factors has exponent a^2=1 modulo 3. Therefore both noninvertibles have
nu_3=2*zeta_3^(-j). These three invariant values are distinct. The models
are pseudo-unitary, so their unique positive spherical structures are
preserved by tensor equivalence. This establishes the required three
inequivalent GT models using the adapted theorem alone, without the
general-cocycle formula corrected in the later erratum.

Finally A4 has only two normal abelian subgroups, 1 and V4. Inflation makes
all twisting and conjugation corrections in the Naidu--Nikshych Lagrangian
classification trivial on V4. Its zero and nonzero alternating bicharacters
are both invariant under A4. Hence there are exactly three Lagrangians.
A 2-group acting on a three-element set fixes an element. The stable-
Lagrangian equivariantization criterion therefore applies to every 2-group
action, including nontrivial coherence data. The GT half of the branch
criterion in `../d48/triality_gt_branch.md` passes this audit.

## Rank-six ring prerequisite

I independently read and replayed `../d48/rank6_swap_rings.py` with `-O`.
Its domain is complete for based rings of dimension type 1^4,2^2. The
invertible group is C4 or V4; the left and right actions on the two remaining
simples are arbitrary homomorphisms to S2. Duality either fixes or exchanges
those two simples. Reciprocity fixes every invertible coefficient in their
products, and the remaining dimension gives exactly the enumerated
nonnegative two-term compositions. The script then checks full reciprocity,
duality and associativity, and all involutive invertible-group automorphisms
combined with the exchange of the two noninvertibles.

It examines 100 C4 and 456 V4 dimension-compatible tables, retaining three
and seven based tables respectively. In each group exactly one table admits
the required exchange, and its full tensor equals R_(3,G). Jordan--Larson
Theorem 1.4 excludes G=C4 and permits G=V4. Thus the extra swapping-action
premise, rather than the dimension type alone, correctly puts the relevant
rank-six quotient into the triality classification above.

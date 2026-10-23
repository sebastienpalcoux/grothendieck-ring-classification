# Triality equivariantizations R9_1_12 and R9_1_108

R9_1_12 and R9_1_108 are accepted after independent categorical and
coefficient audits. The second action uses the direct inner modification
and vanishing action obstruction below.

This supplements THEORY.md. The file `triality_equivariant_ring.py` reconstructs
both full fusion tensors from induction/restriction and the neutral group
representation rings. It checks associativity, the restriction homomorphism,
and every coefficient of an exact based isomorphism with the input.

## The baseline coherent action

Use the standard Tambara--Yamagami realization
D=TY(V4,chi,+1/2)=Rep(D8), where chi is alternating. Every automorphism of
V4 preserves chi. Permuting the invertible labels, fixing m, and using the
identity tensorators therefore defines a coherent S3 action. This statement
can be checked directly from the usual TY associators, which use only chi,
tau, group addition, and Kronecker delta functions.

The three nonregular invertible D-module categories of rank two are the two
reflection-subgroup modules and the projective D8-representation module for
the nontrivial Schur class. Tensor triality permutes them. This is also
visible in the module-category classification in THEORY.md; Aut_tensor(D)=S3
acts as all permutations of the three nontrivial invertible labels.
More explicitly, a simple in each of these module categories has internal
End object 1+h+m, and the three classes have the three distinct nontrivial
h labels (the kernels of the linear-character action). A tensor permutation
of V4 sends this label to its image, proving transitivity on the three
module classes.

Choose A=End(V), where V is the real two-dimensional projective representation
of D8 obtained from the ordinary representation of its central cover D16
in which the lifted rotation has angle pi/4. As an object of D,
A=1+h+m. It is an Azumaya algebra in the symmetric category Rep(D8), so its
bimodule category is tensor equivalent to D. Its module category is the
projective module above, and triality moves it to a reflection module.

Let t be the transposition fixing this module class. In group notation one
may choose the actual involution a of D8 defined by

  a(r)=r^{-1}, a(s)=sr, with r^4=s^2=1 and srs=r^{-1}.

Its action on the projective representation is implemented by a real
reflection T with T^2=1. Explicitly, if R is rotation through pi/4 and S is
a reflection, take T=S R^{1/2}; then T R T=R^{-1} and T S T=S R.
Conjugation by T supplies a coherent t-equivariant algebra structure on A.
Equivalently, the nontrivial Schur cocycle of D8 extends to
D16=D8 semidirect_a C2: the cover D32 -> D16 restricts to the nontrivial
cover D16 -> D8 on the normal D8 subgroup. Thus the projective module
category has a genuine coherent C2 module structure; no associator
correction on C2 is being assumed.
The restriction of the strict TY S3 action to this transposition is the
coherent Rep(a) action: its two extensions of the real m object are
self-dual. Equivalently, its equivariantization is Rep(D8 semidirect_a C2).
This group is D16: if q=st, then q^2=r, q has order eight, and sqs=q^{-1}.
For precision about coherence, a fixed transposition class has exactly two
coherent C2 actions, because Aut_tensor(Id_D)=C2 and
H^2(C2,C2)=C2. In the strict TY action, the two extensions of m have
equivariant scalar +1 and -1 and are self-dual. In the other coherence
class those scalars are +i and -i and duality interchanges them. The
actual group-automorphism action has self-dual m extensions in Rep(D16),
so it is coherently equivalent to the strict TY restriction, not merely
equal as an isomorphism class of tensor functors.

Form B=D crossed S3 and its dual C=A-Bimod(B). Because A lies in the neutral
component, C retains the S3 grading. Its neutral component D' is equivalent
to D. The C3 restriction E is nontrivial since triality moves the A-module
class. By the argument of THEORY.md its ring is R9_1_117. The coherent
t-equivariance of A gives a unitary invertible in C_t whose square and
associator are trivial. Conjugation by it is a genuine C2 action on E,
and C=E crossed C2. On the neutral category D' the Azumaya equivalence is
natural under Rep(a); thus the neutral equivariantization is Rep(D16).

## Why the two dimension-four objects are self-dual

A standard consequence of faithful group grading is that the subcategories
supported on conjugate subgroups are categorically Morita equivalent: the
sum of components on the corresponding group coset gives the invertible
bimodule category. Apply this to the three order-two subgroups of S3.
The t subextension is D' crossed C2 and is Morita equivalent to Rep(D16).
Each of the other two subextensions has neutral D' and a rank-two
nonregular component, so its dimension profile is 1^4,2^3 and it too is
Morita equivalent to Rep(D16).

Every fusion category Morita equivalent to Rep(D16) is C(D16,1,H,psi) for a
subgroup H and a 2-cocycle psi. For the profile 1^4,2^3 there are only two
possibilities for H:

- H is a reflection C2. Its Schur multiplier is trivial. The four
  invertibles and three dimension-two double-coset objects are all
  self-dual. Inversion fixes every double coset and every stabilizer
  character is real.
- H=D16. The fusion ring is the ordinary representation ring of D16,
  independent of the subgroup 2-cocycle, and all irreducibles are self-dual.

The other subgroups cannot give four invertibles. Cyclic normal subgroups
produce a pointed dual. For a Klein-four subgroup, its normalizer has order
eight and preserves its Schur class, already giving eight invertibles.
An index-two D8 subgroup likewise has an invariant Schur class and gives
eight invertibles. H=1 is pointed. This exhausts the subgroups.

Consequently the rank-two simples in either nonregular order-two component
are self-dual. Write E_1={X0,X1}, E_2={Y0,Y1}, with Xi*=Yi. The above
self-duality says t(Xi)=Yi. The two free C2 orbits therefore each contain
their own dual, so the two dimension-four equivariant simples are self-dual.

## Exact fusion reconstruction

Use the canonical R117 tensor in `triality_ring.py`, choosing left stabilizer
1 and right stabilizer 2 in V4={0,1,2,3}. Its labels are
0,1,2,3,m,X0,X1,Y0,Y1. The neutral equivariant category is Rep(D16), whose
four linear representations are indexed by their signs on q and s, and
whose three two-dimensional representations have rotation weights 1,2,3.
Restriction to D8 sends the four linears to 0,3,0,3 and the three
2-dimensional objects to m,1+2,m. The two additional simples restrict to
Xi+Yi. These rows form the matrix F in the certificate.

The induction map is F transpose by Frobenius reciprocity. Every product
involving an induced simple is determined by

  Ind(X) tensor W = Ind(X tensor Forget(W)),
  W tensor Ind(X) = Ind(Forget(W) tensor X).

Products between neutral simples are exactly those of Rep(D16). Thus these
formulas determine every coefficient without any choice of an unverified
trace sign. They produce R9_1_12, with source-to-model permutation
[0,3,2,4,8,7,6,1,5]. All coefficients are zero or one.

## The second coherent action and R9_1_108

A direct construction avoids choosing an S3 associator. Let alpha
be the accepted action above and choose g in V4 with g alpha(g)=h, the
nontrivial fixed invertible. Put beta=Ad_g composed with alpha. Then
beta^2 is tensor isomorphic to Ad_h. The nonregular triality fixes a
central invertible w=(z,h), where z is the central involution of D8.
It lifts to a central structure on h in E: the projective obstruction
for this C3-invariant simple lies in H^2(C3,C*)=0. Hence Ad_h is tensor
isomorphic to the identity and beta has order two as a tensor-functor class.

There is a genuine coherent C2 action lifting beta because its obstruction
is in H^3(C2,Aut_tensor(Id_E))=H^3(C2,C3)=0. Its choices form the trivial
H^2(C2,C3) torsor. Any correction is a character of the universal grading
C3 and therefore restricts identically to the neutral category D. Relative
to the symmetric central lift of h in D, the central structure w differs
by z. Thus the neutral square coherence changes by z, which acts by -1
on m. The neutral m extensions become a dual pair. The inner modification
also changes the nonneutral orbits from Xi+Yi to Xi+Y(i+1).

The independent derivation of the central lift, the vanishing obstruction,
and the neutral coherence comparison is in
`work/resolve_integral/TRIALITY_ACTIONS.md` and has passed the independent
categorical audit.

Explicitly the neutral group extension now has t^2=z=r^2, with the same
conjugation a. For q=st one obtains q^2=r^3 and sqs=q^3. Consequently
the neutral representation ring is now that of the semidihedral group
SD16=<q,s | q^8=s^2=1, s q s=q^3>. The three dimension-two irreducibles
are induced from the C8 character orbits {1,3}, {2,6}, {5,7}. Restriction
has the same matrix on the neutral part; the first and third irreducibles
are dual. Applying precisely the same induction formulas, with pairing
Xi+Y(i+1), produces R9_1_108 and the based permutation
[0,4,6,8,7,1,2,3,5]. The second-action existence statement is to be read
together with the independent cohomology audit, not as an inference from
this tensor calculation alone.

Both constructions use unitary TY data, finite unitary actions,
and separable unitary algebras, and therefore produce unitary fusion
categories. No completeness assertion for other involutions is needed
for either positive realization.

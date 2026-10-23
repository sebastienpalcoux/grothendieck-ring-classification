# Coherent involutions on the nonregular triality extension

This note concerns the `R9_1_117` de-equivariantization branch of the
four dimension-48 rings. It does not by itself exclude other possible
de-equivariantization branches. Its conclusions are:

1. There is a coherent involution giving `R9_1_12`.
2. The other extension-cohomology class gives `R9_1_108`.
3. These are the only fusion rings in this branch, allowing all associators
   and all coherent involutions. In particular the same branch does not
   realize `R9_1_62` or `R9_1_87`.

The exact ring reconstruction and basis maps are in
`work/resolve_small_models/triality_equivariant_ring.py` and its certificate.
The finite cohomology calculation here is independently replayed by
`python work/resolve_integral/triality_action_cohomology.py`.

## 0. No other neutral Tambara--Yamagami category is omitted

The adjoint neutral fusion ring of R9_1_117 is the TY ring on V4. Its
categorifications are `TY(V4,chi,tau)`, with chi a nondegenerate symmetric
bicharacter and `tau=+1/2` or `-1/2`. Let X be a simple in a nonneutral
component. The input fusion rules give

`X X* = 1+h_L+m`, and `X* X = 1+h_R+m`, with `h_L != h_R` nonidentity.

Both objects have their canonical internal-end algebra structures. In an
algebra `1+h+m`, the products from `h tensor m` and `m tensor h` to m are
nonzero: the h summand comes from an isomorphism `h tensor X -> X`, and
its multiplication acts invertibly. Associativity on `(h,m,h)` therefore
forces `chi(h,h)=1`, because the two nonzero scalar products agree except
for the TY associator `alpha_(h,m,h)=chi(h,h)`. Applying this on both sides
gives two distinct nonidentity isotropic elements of V4.

A nonalternating nondegenerate symmetric form on F2^2 has exactly one
nonzero isotropic vector. Hence chi must be alternating. The two remaining
TY categories are Rep(D8) and Rep(Q8). The quaternion possibility is
excluded by Nikshych--Riepel, Remark 9.4: all its Brauer--Picard classes
come from tensor autoequivalences, so every homogeneous component of an
extension is regular as a left module. A regular component has invertible
objects, whereas both nonneutral components here have only two
dimension-2 objects. Thus the neutral category is necessarily Rep(D8).
This argument covers all complex associators and both signs of tau.

For a fixed nonregular homomorphism `C3 -> BrPic(Rep(D8))`, the extension
classification has no multiplication-system ambiguity:
`H^2(C3,Inv Z(D))=0` by coprime averaging. The first obstruction also
vanishes for the same reason; the second lies in `H^4(C3,C*)=0`.
All associators therefore form the three-element torsor
`H^3(C3,C*)=C3`. These are precisely the scalar twists eta treated below;
there is no further neutral category or extension parameter.

## 1. Extension data and the relevant permutation groups

Put D=Rep(D8), where D8 has order 8. Its tensor autoequivalence group is
S3: in the Tambara--Yamagami realization with alternating bicharacter on
V4, these are all permutations of the three nonidentity invertibles.
Its Brauer--Picard group is S4. The image of the tensor autoequivalence
group is the stabilizer of the regular left-module class, denoted p.
Inner autoequivalences of D are tensor isomorphic to the identity because
D is symmetric.

Let E be a nonregular C3 extension of D with fusion ring R9_1_117.
Its degree-one bimodule class is a 3-cycle r in S4 which moves p.
Every such r is conjugate under the S3 stabilizer of p. Write q for the
unique point fixed by r. An involution of E reversing the C3 grading
produces an S3-graded crossed product over D. The corresponding
homomorphism to S4 sends its involution generator to the unique nonidentity
member s of

`N_S4(<r>) intersect Stab_S4(p)`.

This s fixes p and q and exchanges the remaining two points. Thus there
is one possible Brauer--Picard homomorphism, up to equivalence of the
neutral category and labeling of the C3 grading.

The universal grading of E is exactly C3, as checked from the input
fusion tensor. The neutral category is D, and the two nonneutral
components contain two dimension-2 objects each.

## 2. The coefficient module and the nonzero twist

Let `A=Inv Z(D)`. For D=Rep(D8),

`A=Z(D8) x Hom(D8,C*) = C2^3`.

Write z for its nontrivial element with underlying object equal to the
tensor unit. This is the tensor natural automorphism of Id_D which is +1
on the four invertibles and -1 on the dimension-2 simple m.

The S4 action on A is the quotient permutation representation
`F2^4/<(1,1,1,1)>`. Here is a way to identify the representation without
assuming a matrix for the Brauer--Picard action. The element z is fixed
by the S3 stabilizer of p, so its orbit under S4 has size 1 or 4. It cannot
have size 1: then z would be fixed by the triality and would lift to a
central invertible of E with underlying tensor unit. Such a lift exists
because the obstruction lies in `H^2(C3,C*)=0`, using the relative-center
description of centers of graded categories. But every element of
`Aut_tensor(Id_E)=Hom(C3,C*)` restricts trivially to D, whereas z is
nontrivial there. This is impossible. Therefore the orbit
has four distinct elements `w_p=z,w_q,w_a,w_b`.

Their only linear relation is that their sum is zero. Indeed the kernel
of the permutation-module map from F2^4 sending the four basis vectors to
them is S4 invariant. A relation of weight 1, 2, or 3 would force some
of the four vectors equal or zero; the weight-4 relation is the only
remaining possibility. They span A, proving the claimed representation.

The r-fixed subgroup is therefore `<w_q>`, of order 2. Choose coordinates
on D so that s is the actual group outer automorphism represented by

`r0 -> r0^-1, s0 -> s0*r0`

for standard generators `r0^4=s0^2=1` of D8. It fixes z and acts on the
four characters by a transposition. Let h be its unique nontrivial fixed
character. Its norm on A has image `<(1,h)>`, where 1 means the trivial
central-group coordinate. On the quotient permutation representation,
that same norm has image `<w_p+w_q>`. Consequently

`w_q=(central z, h)`.

In particular w_q has underlying object h, and its half-braiding differs
from the canonical symmetric half-braiding of h by the automorphism z.

Since C3 has order coprime to |A|, the Lyndon--Hochschild--Serre sequence
reduces the relevant cohomology to

`H^2(S3,A) = H^2(C2,A^C3) = C2`.

The nonzero class is represented by the parity cocycle
`c(x,y)=w_q` if x and y are odd, and 0 otherwise. The supplied standard-
library verifier constructs the normalized bar differentials and checks
that H2 has dimension 1, this cocycle is closed and nonzero, and all the
norm identities above hold.

## 3. Completeness of the coherent-action list

The extension classification of Etingof--Nikshych--Ostrik applies to the
fixed homomorphism `S3 -> BrPic(D)`. Its first obstruction vanishes because
one such extension exists by Morita transport of the strict S3 action on
the Tambara--Yamagami realization of D. The two multiplication classes
form the H2 torsor above. Both lift to associators because
`H^4(S3,C*)=0`. For either, the remaining scalar choices form
`H^3(S3,C*)=C6`; restriction identifies its primary factors with
`H^3(C3,C*)=C3` and `H^3(C2,C*)=C2`.

The C3 factor is precisely the scalar associator class eta of E.
For fixed eta, the remaining C2 scalar choice is fixed by requiring a
strict order-2 invertible object in the odd component, as a crossed
product by an actual C2 action has. Such an object can always be chosen
for exactly one of the two scalar choices: the underlying group of
invertibles in the C2 subextension is the split group V4 semidirect C2.
Indeed `H^2(C2,V4)=0` for the transposition action. Its two order-2 lifts
of the nontrivial quotient element are conjugate, and their restricted
3-cocycle classes agree. Inflating the nontrivial H3(C2,C*) class reverses
this common class. Thus precisely one choice makes their pointed
subcategory Vec(C2), as required. For either object the monoidal embedding
of Vec(C2) has no additional choice up to equivalence, since
`H^2(C2,C*)=0`. The two lifts give conjugate actions.

There are therefore at most two actions for each eta. Conversely the
construction just described produces an action for each of the two
multiplication classes, so the list is complete.

Changing eta does not change the resulting fusion ring. A scalar
associator twist changes neither the E fusion rules nor the object
permutation of the action. The C3-primary class restricts trivially to
the C2 subgroup, so it also leaves the neutral equivariantization and
its restriction matrix unchanged. Every nonneutral equivariant simple
is induced from one of the two simple objects in a nonzero C3 degree.
The projection formulas

`Ind(X) tensor Y = Ind(X tensor Forget(Y))`,
`Y tensor Ind(X) = Ind(Forget(Y) tensor X)`

therefore determine every product having a nonneutral factor from the
same E tensor and restriction matrix. This proves fusion independence
of eta directly. Equivalently, in a product of two nonneutral orbit
objects the involution exchanges the degree pairs (1,2) and (2,1), so
its trace on each fixed degree-zero fiber is zero; all nonzero-degree
fibers occur in exchanged pairs. No scalar eta can affect the character
projection multiplicities. Thus all three values of eta have the same
two possible fusion outcomes.

## 4. Existence and identification of the baseline action

Use the strict S3 action permuting the V4 labels of the standard
Tambara--Yamagami D. Its restriction to a suitable transposition is the
coherent action of the actual order-2 group automorphism above. Its
equivariantization is Rep(D16), where D16 has order 16. One can also
recognize this coherence class by the fact that both equivariant lifts
of m are self-dual; the other class gives Rep(SD16), with two dual
non-self-dual dimension-2 objects.

Choose the invertible D-bimodule M given, as a left module category, by
projective representations of D8 with its nontrivial Schur class. It is
an invertible bimodule because the matrix algebra End(V), for a
2-dimensional irreducible projective representation V, is an Azumaya
algebra in the symmetric category Rep(D8). M is fixed by the chosen
transposition and its Morita class moves the regular-module point p.
Conjugating the strict S3 extension by M therefore gives the nonregular
triality extension E.

There is no missing equivariance obstruction in this transport. The
nontrivial Schur class of D8 extends to its semidirect product D16 with
the transposition: use the central cover D32 -> D16. On the normal D8
subgroup `<u^2,t>` of D16, the restricted cover is D16 -> D8 and represents
the nontrivial Schur class. Hence M has a coherent C2 module structure,
obtained from projective representations of D16. Morita transport gives
an actual C2 action on E, including its square coherence. Its C2 crossed
subextension is Morita equivalent to Rep(D16).

The other two order-2 subgroup subextensions of the S3 extension are
Morita equivalent to this one: the homogeneous coset bimodule implements
the equivalence for conjugate subgroups. Each of these other subextensions
has dimension profile `(1^4,2^3)`.

Every fusion category Morita equivalent to Rep(D16) is
`C(D16,H,psi)` for a subgroup H and a 2-cocycle psi. The profile `(1^4,2^3)`
forces H to be D16 itself or a reflection C2. To check the other cases:
cyclic normal subgroups give pointed categories; a V4 subgroup gives
8 invertibles and two dimension-2 objects; an index-2 D8 subgroup gives
the same latter profile, for either Schur class. H=1 and the central C2
are pointed. For H=D16 the category is Rep(D16); for a reflection C2,
the three non-normalizer double cosets are inverse-stable and have
trivial stabilizers, while the four invertibles form V4. Thus in both
allowed cases all simples are self-dual.

If X lies in the nonneutral C3 component, X*t lies in one of these other
order-2 components. Its self-duality says that the involution sends X to
X*. Therefore the two dimension-4 orbit simples in E^C2 are self-dual.
Together with the neutral Rep(D16) fusion data, exact tensor reconstruction
identifies this baseline as R9_1_12.

## 5. Direct coherent construction of R9_1_108

There is a direct action construction, independent of the scalar-section
argument in Section 3. Let alpha be the baseline action from Section 4.
The invariant central object w_q from Section 2 lifts to a central
invertible of E: use the relative-center equivariantization for the C3
extension, and `H^2(C3,C*)=0`. Its underlying object is h. Thus h has a
half-braiding whose restriction to D is exactly `(central z,h)`.

Choose g in the neutral invertible group with `g*alpha(g)=h`, and set

`beta=Ad_g composed with alpha`.

Its square is tensor isomorphic to `Ad_h`, and the half-braiding of h
provides a monoidal natural isomorphism `Ad_h -> Id_E`. Therefore the
isomorphism class of beta defines a homomorphism
`C2 -> Aut_tensor(E)`.

Apply ENO, *Fusion categories and homotopy theory*, Corollary 7.9(i).
The obstruction to upgrading this homomorphism to a coherent C2 action
belongs to `H^3(C2,Aut_tensor(Id_E))`. Here
`Aut_tensor(Id_E)=Hom(U(E),C*)=C3`; all positive-degree C2 cohomology with
these coefficients vanishes, regardless of the action, by coprime
averaging. Thus the obstruction is zero and beta has a genuine coherent
action. The same vanishing in degree 2 makes its coherence unique up to
equivalence. This explicitly resolves the action-coherence obstruction.

The neutral square coherence can be read before making the final
coherence correction. On D, the symmetric braiding gives a canonical
tensor isomorphism `Ad_g -> Id_D`. Under that identification, the square
coherence for beta differs from that for alpha by the ratio of the
half-braiding of h and its canonical symmetric half-braiding. That ratio
is z by Section 2. Any correction required by the preceding obstruction
argument is a tensor natural automorphism of Id_E, hence a character of
C3; it restricts trivially to D. It cannot change this neutral ratio.

Consequently the two equivariant lifts of m change from self-dual to a
dual pair: in a strict realization their involution eigenvalues change
from +1,-1 to +i,-i. The neutral equivariantization changes from the
Rep(D16) fusion ring to the Rep(SD16) fusion ring. On the nonneutral
simples, beta changes the permutation by Ad_g, which is precisely the
second involution in the exact input restriction maps. Exact tensor
reconstruction with these two features gives R9_1_108.

This direct construction proves existence even without the exhaustiveness
statement of Section 3. In the extension classification it is the other
H2 class, represented by the parity cocycle w_q. That classification
rules out an additional action producing R9_1_62 or R9_1_87 within the
R9_1_117 branch.

All constructions use unitary group representations, unitary TY structure,
unitary module categories, and finite-order scalar cochains. Hence the
two positive witnesses are unitary.

## References

* Nikshych--Riepel, *Categorical Lagrangian Grassmannians and Brauer--Picard
  groups of pointed fusion categories*, arXiv:1309.5026, Section 9.1 and
  Example 9.3: BrPic(Rep(D8))=S4 and the nonregular triality extension.
* Etingof--Nikshych--Ostrik, *Fusion categories and homotopy theory*,
  arXiv:0909.3140, Theorem 1.3 (extensions) and Corollary 7.9(i) (coherent actions).
* Gelaki--Naidu--Nikshych, *Centers of graded fusion categories*,
  arXiv:0905.3117: the relative-center equivariantization used to lift
  C3-invariant central invertibles.
* The tensor autoequivalence group of a TY category is the isometry group
  of its bicharacter; this also follows directly by inspecting its
  standard associator matrices. For alternating V4 that group is S3.

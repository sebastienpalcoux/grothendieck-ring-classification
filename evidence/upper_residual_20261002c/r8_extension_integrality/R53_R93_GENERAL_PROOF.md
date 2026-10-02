# R53 and R93: every extension of the integral neutral is integral

**Conclusion: neither ring admits a fusion category over the complex field.**
The independent proof audit and normal/optimized exact receipts are stored
beside this file.

This proof does not assume a pivotal structure or unitarity. Its categorical
tools are solvability, equivariantization, Morita transport of graded
extensions, and the elementary classification of pointed module categories.

## 1. Source hypotheses

Both census rings have type `1^4,4^2,(3sqrt(2))^2`, of FP dimension 72.
The integral basis elements form a closed subring D of FP dimension 36,
and the two irrational basis elements form the odd component of a faithful
C2 grading. The group of invertibles in D is C4. In a basis `1,g,g^2,g^3,X,Y`,
the generator g fixes X and Y, and

    X*=X, Y*=Y,
    X^2 = 1+g+g^2+g^3+X+2Y,
    Y^2 = 1+g+g^2+g^3+2X+Y.

Consequently D_ad=D. The exact checker verifies all of these assertions
directly against both original census tensors; it also verifies the full
faithful grading and exact dimension character. R53 has self-dual irrational
simples; R93 has a dual pair. This difference is immaterial here.

## 2. First prime descent of any neutral categorification

Assume D has a complex categorification. By ENO's two-prime solvability
theorem it is solvable, since `FPdim(D)=2^2*3^2`. It has trivial universal
grading, so the final prime step of a solvability sequence must be an
equivariantization. A C3 equivariantization would embed Rep(C3), contrary
to Inv(D)=C4. Hence

    D = E^{C2},   FPdim(E)=18.

The sign object is g^2. It fixes both X and Y. The orbit formula therefore
gives `E` type `1^2,2^4`: the four units of D descend in sign pairs to two
units of E, while X and Y each split into two distinct 2-dimensional simples.
These assertions do not require trivial equivariant coherence: all
projective representations of a cyclic order-two stabilizer have degree one.

Let eta be E's nontrivial unit. For each 2-dimensional simple Z, the unit
occurs once in `Z Z*`. If eta did not also occur, the remaining FP dimension
would be 3, which cannot be a sum of dimensions of nonunit simples, all 2.
Thus eta fixes every Z, and `Z Z*` includes `1+eta` and one 2-dimensional
simple.

It follows that E_ad contains both units. A proper E_ad has FP dimension
dividing 18 and is of type `1^2,2^n`; the only possibilities are dimensions
2 and 6. Dimension 2 cannot contain the 2-dimensional simple constituent
of `Z Z*`. At dimension 6,
the universal grading would have order three. Either nonneutral component
has dimension 6 and contains only 2-dimensional simples, impossible because
its dimension would be a multiple of 4. Therefore E_ad=E.

Solvability of E and trivial universal grading again force a final
equivariantization. Its group must be C2, since Inv(E)=C2 has no subgroup
C3. Thus

    E = P^{C2},   FPdim(P)=9.

Every fusion category of dimension 9 is pointed. Write `P=Vec_A^alpha`,
where A is C9 or C3^2.

## 3. The two equivariantizations combine to a C4 action

In E the canonical central Rep(C2) has underlying nontrivial object eta.
There is only one half-braiding on eta: any two half-braidings differ by a
tensor automorphism of the identity, and
`Aut_tensor(Id_E)=Hom(U(E),C*)=1`. Consequently the outer C2 action on E
preserves this canonical central Tannakian subcategory.

Equivariantize this preserved central Rep(C2) by the outer action.
Equivariant half-braidings give a fully faithful braided embedding of this
equivariantization into `Z(E^{C2})=Z(D)`. It is symmetric and Tannakian:
equivariantization of Rep(C2) by a braided action is the representation
category of a group H fitting into

    1 -> C2 -> H -> C2 -> 1.

Its FP dimension is four. Its four simple objects are invertible and their
underlying objects exhaust Inv(D), whose group is C4. Thus H is C4, rather
than V4. De-equivariantizing D by this central Rep(C4) gives a category Q
of dimension 9, automatically pointed. We need not identify Q with the P
in the previous descent. Write `Q=Vec_A^alpha`. We have

    D = (Vec_A^alpha)^{C4}.

Each nonunit simple of D has dimension 4. Therefore C4 acts freely on the
eight nonidentity elements of A. In particular A cannot be C9, whose
automorphism group has order 6 and contains no element of order 4.
For `A=C3^2`, the generator acts by an irreducible matrix J satisfying
`J^2=-I`. For example take `J(a,b)=(-b,a)`. This action is fixed-point-free
for every nonidentity element of C4.

## 4. A general extension integrality criterion

Here is the criterion used in the final step.

**Lemma.** Let B be Morita equivalent to `Vec_G^omega`. If every normal
abelian subgroup of G has square order, then every graded extension of B
is integral.

**Proof.** First consider an invertible `Vec_G^omega` bimodule category M.
As a left module category it is transitive and is parameterized by a
subgroup N and a cochain trivializing the restriction of omega. Since its
dual category is pointed, the double-coset formula for simple objects of
the dual shows that N is normal: a nonnormal double coset would give a
simple of dimension at least `[N:N intersect aNa^-1]>1`. In the identity
double coset the ordinary irreducible representations of N occur, so N
must also be abelian. This is explicitly the subcategory Rep(N) in
Gelaki--Naidu, Theorem 4.1, for the general twisted category; no untwisted
associator assumption is made here. The left module has `[G:N]` simple objects. Its
normalized simple FP dimensions are all `sqrt(|N|)`, because the G action
is transitive and their squared sum is |G|. They are integral by hypothesis.

Each homogeneous component of a graded extension of `Vec_G^omega` is
such an invertible bimodule. Thus that extension is integral. Morita
equivalence of neutral categories transports graded extensions by
conjugating their invertible bimodule categories; the transported entire
extension is Morita equivalent to the original entire extension (ENO's
Brauer--Picard groupoid and extension classification).

Finally integrality is invariant under Morita equivalence for weakly
integral fusion categories. To see the required implication directly,
the center of an integral fusion category is integral, since restriction
preserves FP dimensions. A Morita equivalent category has the same center.
For any simple W in it, induction to its center has dimension
`FPdim(C) FPdim(W)`. If the center is integral this is an integer; as
`FPdim(C)` is a positive integer, `FPdim(W)` is rational. It is an algebraic
integer, hence an integer. This proves the lemma. QED.

The pointed crossed product dual to a pointed equivariantization is
pointed. Hence D is Morita equivalent to `Vec_G^omega` with

    1 -> A -> G -> C4 -> 1,

and conjugation action J. Schur--Zassenhaus, since orders 9 and 4 are
coprime, makes G the semidirect product `C3^2 rtimes_J C4`. No restriction
on omega is needed in the lemma.

G has exactly two normal abelian subgroups, 1 and A. Indeed, if a normal
abelian subgroup N contained an element whose C4 exponent is k!=0, its
commutators with A would contain `(J^k-I)A=A`. Then A would lie in N, but
that element does not commute with A, contrary to N being abelian.
Thus N is contained in A. J is irreducible over F3, so its only invariant
subgroups of A are 1 and A. Their orders are 1 and 9, both squares.

The lemma says that every graded extension of D is integral. In particular
a putative census categorification, a C2 extension of D, would be integral.
Its two odd simples have FP dimension `3sqrt(2)`, a contradiction.

## Primary sources and review points

- ENO, *Weakly group-theoretical and solvable fusion categories*,
  https://arxiv.org/pdf/0809.3031: the two-prime solvability theorem,
  closure of solvability, and the final prime extension/equivariantization.
- ENO, *Fusion categories and homotopy theory*,
  https://arxiv.org/pdf/0909.3140: Theorem 1.3 (extensions through the
  Brauer--Picard groupoid), Corollary 3.13 (Morita transport of bimodules),
  Proposition 4.2 (invertibility and pointed dual), Section 2.5 (normalized
  module FP dimensions), and Section 4.2 (integral bimodules).
- Nikshych--Riepel, *Categorical Lagrangian Grassmannians and
  Brauer--Picard groups of pointed fusion categories*,
  https://arxiv.org/pdf/1309.5026, Proposition 5.2 and Remark 5.4:
  normal abelian kernels and one-sided module restriction. Their displayed
  proposition is for the untwisted case; the proof above explicitly uses
  the general twisted double-coset formula instead of assuming that
  proposition applies verbatim to omega.
- Gelaki--Naidu, *Some properties of group-theoretical categories*,
  https://arxiv.org/pdf/0709.4326, Theorem 4.1 (the identity double-coset
  subcategory is Rep(N)), Theorem 5.1, and the simple-object FP-dimension
  formula for the general twisted group-theoretical dual.

The independent audit should check the preserved-Tannakian embedding
step and the identity-double-coset untwisted representation assertion.
All source-ring, grading, and finite-group premises have an exact checker.

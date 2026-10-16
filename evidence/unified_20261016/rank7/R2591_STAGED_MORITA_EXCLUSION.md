# R7_4_2591 is not categorifiable: a staged Morita obstruction

**Theorem.** There is no fusion category over C with the census fusion
ring R7_4_2591. No pivotality or unitarity assumption is made. The
argument is categorical and finite-group theoretic; it does not use a
classification of associators, a near-group terminal, or a numerical
search.

Write t=2+sqrt(5). The source has invertible group G=V4, a simple X of
dimension2, and mutually dual simples Y,Z of dimension2t. Every element
of G fixes each of X,Y,Z on both sides. The relevant products are

    X²=sum G, XY=YX=2Z, XZ=ZX=2Y,
    Y²=2X+4Y+4Z.

## 1. The already established twisted Morita reduction

Apply `R2591_TWISTED_V4_REDUCTION.md`. This gives a Morita equivalent
fusion category E with exactly eight invertibles and eight
noninvertibles of dimension t. The invertibles K act freely and
transitively on the latter. In the inverse Morita context the original
category is Q-bimod(E), where Q is a connected separable algebra whose
underlying object is the regular sum on a subgroup L=V4 of K.

The multiplication on Q may be twisted. Its existence implies that the
pointed associator restricted to L is cohomologically trivial. No
triviality outside L is asserted. The initial reduction is valid over C:
its projective-block ranks and the impossibility of the nonalgebraic-
integer dimension t/2 do not use a pivotal structure.

Choose rho in the free orbit. At the level of simple labels write

    rho g=phi(g)rho, rho²=a+N rho.

Here phi is an automorphism of K, a is an invertible, and associativity
gives phi²=Ad(a), phi(a)=a. In particular rho*=a^-1 rho. The only groups
of order8 containing V4 are C4×C2, C2³, and D8, so L has index2 and is
normal in every case.

## 2. Fixedness forces phi(L)=L, while duality forces a outside L

The pointed Q-bimodules supported on L are exactly the four character
twists of Q, parametrized by L-hat. They are the four source invertibles.
This remains true for a twisted multiplication on Q.

Suppose phi(L) differs from L. Then L phi(L)=K, and the action by left
and right L on the noninvertible orbit has just one support orbit of
size8. Its stabilizer has order2, with both projections injective into
L. Since H²(C2,C*)=0, it contributes two simple Q-bimodules, one for
each stabilizer character. These are the source Y,Z.

Tensoring by a character twist of Q twists the stabilizer character by
its restriction along one of these injective projections. The character
restriction L-hat -> C2-hat is surjective. Therefore some source
invertible interchanges Y and Z. This contradicts their individual
fixedness. Thus phi(L)=L.

There are consequently two noninvertible support orbits, L rho and
(K minus L)rho. Each contains at least one simple Q-bimodule, and the
source has exactly two irrational simples. Thus one orbit supports Y
and the other Z. Since Y*=Z, the inverse of L rho must be the other
orbit. The formula rho*=a^-1 rho and normality of L imply

    a notin L.

## 3. A fixed involution inside L

The possibility K=D8 is already impossible. Any index2 V4 subgroup
of D8 consists of 1, the central involution, and two opposite
reflections. Conjugation by every element outside L interchanges
those two reflections and fixes the central involution. Hence
Ad(a)|L is a transposition. But

    (phi|L)²=Ad(a)|L,

and a square in Aut(V4)=S3 cannot be a transposition.

Therefore K is abelian, and phi²=Id. The restriction phi|L is either
the identity or an involution of V4. In either case it fixes a
nontrivial element delta of L. Since K is abelian, delta is central
in K. We have obtained

    delta²=1, delta in L, phi(delta)=delta.

Because Q is a twisted regular algebra on L, its summands 1 and delta
form an actual unital subalgebra A. Rescaling a generator trivializes
the possible C2 multiplication scalar. Thus A=1+delta is connected
and separable.

## 4. Passing through the subalgebra preserves the free rank-sixteen type

Put E'=A-bimod(E). For pointed simples, centrality of delta means that
every H-by-H support orbit, H=<delta>, has size2 and stabilizer C2.
It contributes two invertible A-bimodules. There are four such orbits.

The same is true for the noninvertibles: phi(delta)=delta makes the
diagonal H action trivial, while the left action is free. Each of four
size2 orbits has stabilizer C2 and contributes two simple bimodules.
Their underlying objects contain the two dimension-t orbit members
once, so their E'-dimensions are (2t)/2=t. Projective stabilizers do
not change these counts because H²(C2,C*)=0.

Thus E' again has eight invertibles K' and eight noninvertibles of
dimension t. The relation t²=1+4t implies that W W* has exactly one
invertible constituent for every noninvertible W: compare rational and
irrational coefficients in the dimension identity. Consequently K'
again acts freely and transitively on the eight noninvertibles.

## 5. The inverse algebra now has dimension two

View Q as an A-bimodule using its subalgebra A. Multiplication descends
to Q tensor_A Q -> Q, and its unit is A -> Q. This makes Q an algebra
B in E'. It is separable, and

    FPdim_E'(B)=FPdim_E(Q)/FPdim_E(A)=4/2=2.

It is connected: an A-bimodule map A -> Q is determined by the image
of the unit, which lies in Hom_E(1,Q), a one-dimensional space. The
actual unit gives a nonzero such map.

Since every noninvertible of E' has dimension t>2, connectedness and
the dimension2 identity force B=1+h for an invertible h. The algebra
law and separability give h²=1. Equivalently, this is the regular
algebra of an actual order-two pointed subgroup, with some choice of
multiplication normalization.

The standard relative-bimodule identification is

    B-bimod(A-bimod(E)) = Q-bimod(E).

Indeed, a B-bimodule object is an A-bimodule object with left and right
Q actions whose restrictions are its specified A actions. Restricting
a Q-bimodule gives the inverse correspondence, and the relative tensor
products agree. Thus B-bimod(E') is exactly the original source
category.

## 6. A general dihedral obstruction to individual fixedness

The following argument uses only the new free-orbit rank-sixteen type
of E' and the source dimensions and fixedness.

Let H=<h> in K'. The integral part of B-bimod(E') is the Morita dual
of the pointed category on K' along H. Noninvertible support has
irrational dimension and cannot contribute to this integral part.
The source integral part has four invertibles and the dimension-two
simple X.

If H were normal in K', its four pointed double cosets would each
have stabilizer C2 and give two invertibles, making the integral part
pointed of rank8. Hence H is nonnormal. The only group of order8 with
a nonnormal order-two subgroup is D8. Write

    K'=D8=<r,s>, r⁴=s²=1, srs=r^-1, H=<s>.

Choose an irrational simple sigma of E' and write sigma g=psi(g)sigma.
Its H-by-H support orbit at g sigma has stabilizer

    H intersection g psi(H) g^-1.

If H and psi(H) were conjugate, some such orbit would have stabilizer
C2 and contribute simples of dimension t. The source has no such
dimension. Therefore psi(H) lies in the other reflection conjugacy
class. After changing dihedral generators, psi(H)=<rs>.

The two noninvertible double orbits are then represented by

    U={1,s,rs,r^-1}, and r² U.

They are distinct, disjoint and exhaustive. The central involution
r² normalizes H, so the pointed double coset H r² supports two
invertible B-bimodules. Tensoring either with a noninvertible
B-bimodule sends its support to the other orbit, because multiplication
by r² interchanges U and r²U. Hence these source invertibles
interchange Y and Z.

This contradicts the source rule that all four invertibles individually
fix Y and Z. The hypothetical categorification cannot exist.

## Scope and exact verification

The proof uses only the previously audited twisted V4 reduction,
separable-algebra Morita theory, projective representations of C2,
and elementary group theory of groups of order8. It does not require
the exploratory seven-profile enumeration or the new rank-four paper.

`verify_R2591_staged_morita.py` replays the original source-bound
twisted-block certificate, binds the source tensor, verifies all source
fixedness and duality hypotheses, and checks the finite group assertions
for every subgroup and automorphism involved. It also checks every
dihedral reflection/automorphism configuration in the final argument.
The categorical subalgebra and relative-bimodule steps are proved above
and independently audited rather than represented as a numerical test.

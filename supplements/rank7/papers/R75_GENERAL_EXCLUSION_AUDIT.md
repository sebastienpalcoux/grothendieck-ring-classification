# Independent audit: R7_2_75

Status: APPROVED as an exclusion of every complex fusion categorification.
This audit concerns the theoretical argument; the producer's exact certificate
binds its premises to the census tensor.

The ring has dimension 52, type 1^4 4^3, invertible group V4 and trivial
universal grading. All nontrivial invertibles fix every dimension-four object.
By solvability in dimension 2^2*13, a categorification C must have a final prime
equivariantization step. Its only possible prime is 2, and the orbit/stabilizer
formula gives C = D^{C2}, with D of dimension 26 and type 1^2 2^6.

D has no nontrivial grading. A prime quotient of such a grading has order 2
or 13. A faithful C13 grading needs at least 13 simple objects, but D has rank
eight. In a C2 grading the neutral component has prime dimension 13, hence is
pointed of rank 13, again impossible. Thus solvability supplies
D = (Vec_{C13}^omega)^{C2}. Its C2 action on C13 is inversion, as required by
the simple dimensions of D.

The central Rep(C2) in D is unique: the kernel of Inv(Z(D)) -> Inv(D) is
Aut_tensor(Id_D), which is the character group of the trivial universal
grading. It is therefore preserved by the outer C2 action. Equivariantization
in stages supplies C = (Vec_{C13}^omega)^G for an extension
1 -> C2 -> G -> C2 -> 1. The central Rep(G) embeds fully faithfully in C.
All groups of order four are abelian, so their four characters account for
the four invertibles of C. Since these form V4, G is V4 rather than C4.

The object action V4 -> Aut(C13) = C12 has image of order at most two and
contains inversion. Consequently every nonzero element of C13 has orbit
size two and stabilizer C2. Every projective representation of C2 over C
is one-dimensional, because H^2(C2,C*) = 0. The corresponding equivariant
simple objects therefore have dimension two. This contradicts the census
type 1^4 4^3.

The argument does not assume a trivial associator or a strict categorical
action. It uses the projective orbit/stabilizer formula and retains arbitrary
omega and action coherence. It requires no classification of order-13
cocycles and no unitarity assumption. The central-lift uniqueness argument
justifies the equivariantization-in-stages reduction for every possible
categorification, rather than merely excluding a chosen model family.

Primary theorem dependencies: ENO arXiv:0809.3031, Theorem 1.6 and the
solvable extension/equivariantization construction; the standard prime-
dimension pointedness theorem; DGNO arXiv:0906.0620, Theorem 4.18 and
Proposition 4.19 for equivariantization/de-equivariantization; and the
projective orbit/stabilizer parametrization of equivariant simple objects.

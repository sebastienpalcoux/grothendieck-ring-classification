# R9_2_1487: real-character self-duality obstruction

Use its independently verified Galois-pseudo-unitarity gate and suppose C is
a pseudo-unitary categorification. Put s=sqrt(3). The source dimensions, in
census order, are

    1, 2+2s, 2+2s, 1, 1, 1, 2, 4+2s, 4+2s,

and D=96+48s. Its only nontrivial duality exchange is b_1*=b_2.

The real scalar character

    chi=(1,2,2,1,1,1,2,-2,-2)

has formal codegree f=24. The distinguished central simple A in I(1)
associated to chi has dimension D/f=4+2s and its restriction contains the
source unit exactly once. The central-character identity gives

    S_(A,Z)=dim(A) chi(FZ).

The character satisfies chi(b*)=chi(b). Hence
S_(A*,Z)=S_(A,Z*)=dim(A)chi(FZ*)=S_(A,Z), and nondegeneracy of S forces
A*=A. Therefore the restriction multiplicities
of b_1 and b_2 must be equal.

On the other hand, the coefficient of s in dim(A) forces exactly one source
constituent among b_1,b_2,b_7,b_8. It cannot be b_7 or b_8: either already has
dimension4+2s, leaving no room for the required unit constituent. Hence the
restriction contains exactly one of b_1,b_2, contradicting self-duality.

Thus no pseudo-unitary categorification exists; the gate makes this an
exclusion of every complex categorification.

The argument is a general necessary condition: a dual-invariant scalar character must
admit a self-dual restriction vector for its distinguished I(1) simple. Its
dimension is D/f and its unit multiplicity is one in the commutative case.
No twist enumeration or LP is needed. The height-six LP certificate
`R9_2_1487_h6_dual.json` reduces to this single missing low-column count.

Primary ingredients are Ostrik, *Pivotal fusion categories of rank 3*,
Theorem2.13 (https://arxiv.org/pdf/1309.4822), and the central-character/S
identity in Deshpande, Corollary2.18 (https://arxiv.org/pdf/1611.04486).
The standalone exact character and restriction sweep is
`real_character_restrictions.py`.

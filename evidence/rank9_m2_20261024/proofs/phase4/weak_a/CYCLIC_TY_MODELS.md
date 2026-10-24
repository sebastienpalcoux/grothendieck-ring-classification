# Two unitary cyclic generalized Tambara–Yamagami orbifolds

## Result

The rings R9_2_746 and R9_2_1209 have explicit unitary categorifications.
They are the two parity-coherence inversion equivariantizations of a
12-simple-object generalized Tambara–Yamagami category with invertible
group C9 and three simple objects of dimension sqrt(3). This category is
constructed below by an explicit central C3 condensation, rather than
inferred from vanishing of a group cohomology obstruction.

All half-braidings in this note use the orientation
`c_z(X): z tensor X -> X tensor z`. This is inverse to the orientation
used for central structures in GNN Section 2.2; keeping this convention
explicit avoids a sign reversal in the bicharacter.

## 1. Starting unitary categories and central object

Let omega=exp(2 pi i/3), zeta=exp(2 pi i/9). Take the unitary category
T=TY(C3,chi,1/sqrt(3)), chi(a,b)=omega^(ab), with the skeletal associators
of GNN Section4.1. Its objects are a in C3 and m, with m^2=sum_a a.
The central lift z of the invertible a=1 has right half-braiding

    c_z(b)=omega^b,   c_z(m)=omega.

The equations are c_z(m)^2=chi(1,1)^(-1) and
c_(z tensor z')(m)=c_z(m)c_z'(m)chi(a,a')^(-1).
Thus z has order3 as a central object, and c_z(z)=omega.
These formulas follow by substitution in the displayed TY associators;
they are also the inverse-half-braiding form of the central invertibles in
GNN Proposition4.1. No braiding on T itself is asserted.

Let P=Vec(C9,Omega), with representatives0,...,8 and

    Omega(a,b,c)=zeta^(3a floor((b+c)/9)).

This is a normalized unitary 3-cocycle. The underlying invertible h=3
has right half-braiding beta(x)=zeta^(2x). Its central square has
underlying object6 and half-braiding zeta^(4x). Its central cube has
half-braiding

    zeta^(6x) Omega(x,6,3)=zeta^(9x)=1.

In the product category B=T boxtimes P, the central object

    g=(z,3)

has order3. Its self-braiding is omega*zeta^6=1. The associator on its
three powers is identically1, since Omega(3a,3b,3c)=1. Their braiding is
also identically1, because the self-braiding of a generator is1 and this
is a pointed category with trivial associator. They therefore give an
explicit central Tannakian Rep(C3). Set A=1+g+g^2, with the ordinary
group-algebra multiplication (all nonzero multiplication scalars1).
It is a commutative separable central algebra with the usual unitary
normalization. The right A-module category D=B_A is a unitary fusion
category of dimension (6*9)/3=18.

The action of g on every simple of B is free: its C9 charge shifts by3.
Hence every free simple A-module is simple, and these are indexed by the
12 orbits. Writing the nine invertibles as u^a, a in C9, and the three
other simples as X_r, r in C3, gives

    u^a u^b = u^(a+b),
    u^a X_r = X_r u^a = X_(r+a),
    X_r X_s = sum_(h=0,1,2) u^(r+s-3h).

For example, use orbit representatives (0,a) and (m,r); the relation
(1,3)=1 in the quotient identifies (h,r+s) with (0,r+s-3h).
The dimensions are1^9,(sqrt3)^3.

## 2. A coherent involution preserving the algebra

On T use the canonical orthogonal inversion autoequivalence
F(a)=-a,F(m)=m. The tensorator is the canonical identity map, including
the permutation of summands of m^2. This is an actual involutive tensor
autoequivalence, as in GNN Proposition4.8.

On P use F(x)=-x with tensorator

    J(a,b)=zeta^mu(a,b),  mu(a,b)=-3a*1_(b>0) modulo9.

Writing w for the exponent of Omega, direct substitution gives

    mu(a,b)+mu(a+b,c)-mu(b,c)-mu(a,b+c)
      = w(-a,-b,-c)-w(a,b,c) modulo9,
    mu(a,b)+mu(-a,-b)=0 modulo9.

Consequently F^2=Id as a tensor functor with identity square coherence.
On T it sends the central z to z^2. On P the transported half-braiding
of h=3 at the new argument x is

    beta(-x) J(3,-x)/J(-x,3) = zeta^(4x),

the half-braiding of the inverse central object h^2. Thus F(g)=g^2 as
central objects. On powers of g the tensorator is identically1 because
mu(3a,3b)=0. The permutation g^i -> g^(-i) therefore defines an actual
algebra isomorphism F(A)->A whose square is identity, respecting both
multiplication and the central structure. Hence F descends to a coherent
unitary C2 action on D. It acts by

    u^a -> u^(-a),    X_r -> X_(-r).

There is a second coherent action with the same tensor functor: multiply
the square coherence by the parity natural automorphism, +1 on pointed
simples and -1 on X_r. Parity is monoidal, invariant under F, and trivial
on A; hence it obeys the C2 action coherence before and after descent.
Both actions consist entirely of unitary structure maps.

## 3. Exact equivariant fusion tensors

Let E_0 and E_1 be the equivariantizations for the identity and negative
odd square coherence, respectively. They are unitary categories of
dimension36. Inversion fixes the unit and X_0, and has four two-element
pointed orbits and one two-element nonpointed orbit. Thus each E has
simple dimensions1^2,2^4,(sqrt3)^2,2sqrt3 and rank9.

The two fixed objects give two equivariant lifts each. Every free orbit
gives one simple. The fusion multiplicity for a fixed output is
(dim+trace)/2; for a free output orbit it is the multiplicity at either
representative. Only fixed input objects contribute to the trace.
The only nontrivial fixed-input fusion line is X_0 X_0 ->1. This line is
inherited from (m,0)(m,0)->(0,0), where the tensorator acts identically.
In E_0 its trace is the product of the equivariant signs. In E_1 each
fixed odd equivariant structure squares to-1, so their product contributes
the extra factor-1. This determines every tensor coefficient without
choosing unknown F-symbols on D.

The standalone generator `cyclic_ty_models.py` constructs both tensors
from these orbit/trace formulas, verifies the unit, duality, Frobenius
reciprocity and all associativity equations, and matches every one of
the729 original census coefficients. The source-to-model permutations are

| Source | Coherence | Basis permutation |
|---|---|---|
| R9_2_746 | identity | [0,1,6,7,2,5,3,8,4] |
| R9_2_1209 | negative odd square | [0,6,7,2,5,3,8,1,4] |

`cyclic_ty_models.json` contains both full tensors, the orbit labels, the
intermediate rank12 tensor, and the complete exact parameter checks.
The finite checks corroborate explicit categorical data; associativity of
the fusion tensor alone is not used as an existence argument.

## References

- D. Tambara and S. Yamagami, Tensor categories with fusion rules of
  self-duality for finite abelian groups, J. Algebra209(1998),692–707.
- S. Gelaki, D. Naidu and D. Nikshych, Centers of graded fusion categories,
  Algebra & Number Theory3(2009),959–990; arXiv:0905.3117.
  Sections2.4–2.5 give equivariantization/de-equivariantization;
  Section4.1 gives the explicit TY associators; Proposition4.1 describes
  central invertibles and Proposition4.8 gives the orthogonal action.
  Primary source checked: https://arxiv.org/pdf/0905.3117.

This settles existence only; no classification or novelty claim about
all tensor-equivalence classes with these fusion rings is made.

## 4. Uniform family

The same construction works with3 replaced by any odd n>1. Put
zeta=exp(2 pi i/n^2), chi(a,b)=zeta^(n ab) on Cn, choose
`c_z(m)=chi(1,1)^((n-1)/2)` (whose square is chi(1,1)^(-1)), and use

    Omega(a,b,c)=zeta^(n a floor((b+c)/n^2)),
    h=n, beta(x)=zeta^((n-1)x),
    J(a,b)=zeta^(-n a 1_(b>0)).

The n-th central power of h has half-braiding
`beta(x)^n zeta^(n x)=1`. The diagonal generator's self-braiding is1.
Both the associator and inversion tensorator restrict trivially to its
powers. Inversion sends its central lift to its inverse because
`-(2n-1)=(n-1)^2 modulo n^2`. This gives a unitary category of dimension
2n^2 with invertibles C_(n^2), n simples of dimension sqrt(n), and the
same cyclic generalized-TY formulas. The two equivariantizations have
dimension4n^2 and rank(n^2+n+6)/2. The two rank-nine models above are the
n=3 members. This uniform construction does not classify all generalized
Tambara–Yamagami categories or their actions.

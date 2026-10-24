# R9_2_516: a short structural exclusion

The conclusion is an exclusion of every complex categorification, using the
independently verified signed Galois-pseudo-unitarity gate for this ring. Thus
suppose, for contradiction, that C is a pseudo-unitary categorification, with
its canonical positive spherical structure. Put d=1+sqrt(3), e=2+sqrt(3).
The nine source dimensions are

    1,1,d,e,e,d,2,2e,2d,

and D=72+36sqrt(3). Write g=b_1 for the unique nontrivial invertible.
The exact arithmetic checks are in `replay516_structural.py`; the proof below
uses no LP, twist-order enumeration, or classification of higher-rank rings.

## A forced central Rep(S3)

The formal-codegree dimensions D/f_h of the distinguished simples in I(1)
contain exactly one 1 and one 2; every other value exceeds 4. Let A be the
unique distinguished central simple of dimension 2. Since its restriction
contains the unit once, necessarily F(A)=1+g. Uniqueness also gives A*=A,
and its twist is one.

Now F(A^2)=2(1+g). The unit central simple occurs once because A is simple
and self-dual. The total multiplicity of the source unit in F(A^2) is two.
Thus exactly one other distinguished central simple occurs, and dimension
forces it to be A. The remaining dimension is one. Consequently

    A^2=1+A+z,

where z is central invertible and F(z)=g. The product zA is simple, has
dimension 2 and forgets to 1+g; hence zA=A. Similarly z^2=1, since it is a
central invertible forgetting to the unit, and there is only one distinguished
central simple of dimension one.

The scalar character corresponding to A has chi_A(g)=1, checked directly
from the tensor. The central-character formula gives S_(A,z)=2. Balancing
and zA=A give S_(A,z)=2/theta_z. Therefore theta_z=1. All three simples
1,z,A have twist one, so their fusion subcategory is symmetric by balancing.
Its fusion rules and positive dimensions identify it as Tannakian Rep(S3),
with z the sign representation and A the standard representation.

## Condensation forces a C3 grading

Condense the central Tannakian Rep(C2)=<z>, using its regular algebra
B=1+z. Its image 1+g is connected in C, so the category

    E = C_(1+g)

of right modules is a fusion category, rather than merely a multifusion
category. Bosonic deequivariantization preserves the positive spherical
structure: module dimensions are underlying dimensions divided by 2. In
particular E is pseudo-unitary.

Multiplication by g has free pairs (0,1),(2,5),(3,4), and fixed simples
6,7,8. A free pair gives one simple module of dimension 1,d,e respectively;
each fixed simple splits into two module structures of half its dimension.
Thus E has simple dimensions

    1^3,d^3,e^3,

and FPdim(E)=36+18sqrt(3).

The central Rep(S3) descends, after condensing Rep(C2), to central Rep(C3)
inside Z(E). Precisely, it is a subcategory of local B-modules in Z(C),
and the Schauenburg equivalence identifies that category with Z(E)
(DMNO, Theorem 3.20). The standard representation A becomes the sum of
the two nontrivial one-dimensional representations of C3. Under forgetting
to E its free image is two copies of the unit: F(A)=1+g is the underlying
regular algebra. Therefore both nontrivial central invertibles forget to
the unit of E.

Such a central C3 of invertibles supplies a faithful dual C3 grading of E
(ENO, Proposition 5.10). Every homogeneous component has dimension
FPdim(E)/3=12+6sqrt(3). If a component has a,b,c simples of dimensions
1,d,e, respectively, its dimension gives

    b+2c=3,   a=c.

With 0<=a,b,c<=3, the only possibilities are (0,3,0) and (1,1,1).
The neutral component contains the unit, so it has dimensions 1,d,e.

## The rank-three neutral component is impossible

Call its nontrivial simples X,Y, of dimensions d,e. Their distinct dimensions
force both to be self-dual. Dimension identities, nonnegative multiplicities,
and the unit coefficients uniquely give

    X^2=1+X+Y,   XY=X+2Y,   Y^2=1+2X+2Y.

Its global dimension is D_0=12+6sqrt(3), and its formal codegrees are
3,12+6sqrt(3),12-6sqrt(3). The distinguished central simples therefore have
dimensions 1,4+2sqrt(3),7+4sqrt(3). Their unique restriction vectors are

    (1,0,0), (1,1,1), (1,2,2).

All have twist one. Their contribution to the twist trace of I(X) is thus

    M=(4+2sqrt(3))+2(7+4sqrt(3))=18+10sqrt(3).

The entire object I(X) has positive dimension

    D_0 d=30+18sqrt(3).

The first indicator of X is zero. Therefore the remaining twist terms must
sum to -M. Each twist has modulus one, and its coefficient is positive, so
their total dimension must be at least M. This would require

    2M <= D_0 d.

But 2M-D_0 d=6+2sqrt(3)>0, a contradiction. This is also the elementary
induction obstruction behind Ostrik's rank-three exclusion of K(2,1,2,1).

Hence C cannot exist. Combined with the signed Galois-pseudo-unitarity gate,
R9_2_516 has no complex fusion-category categorification.

## References and independent checks

- Ostrik, *Pivotal fusion categories of rank 3*, Theorems 2.5,2.13 and
  Lemma 3.10: https://arxiv.org/pdf/1309.4822
- Deshpande, central-character identity, Corollary 2.18:
  https://arxiv.org/pdf/1611.04486
- Davydov--Mueger--Nikshych--Ostrik, *The Witt group of non-degenerate braided
  fusion categories*, Theorem 3.20: https://arxiv.org/pdf/1009.2117
- Etingof--Nikshych--Ostrik, *On fusion categories*, Proposition 5.10 and
  Proposition 8.20: https://arxiv.org/pdf/math/0203060

An independent exact labelled-S/indicator certificate also excludes the ring;
its separate audit is `../audit_quadratic_symmetry/AUDIT516.md`. The structural
argument above makes the reason for exclusion explicit and avoids that large
certificate. The structural proof has its own independent audit in the same
audit directory.

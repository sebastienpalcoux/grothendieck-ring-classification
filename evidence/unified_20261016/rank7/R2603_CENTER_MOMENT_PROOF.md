# A full-character two-moment obstruction for R7_4_2603

**Theorem.** The fusion ring R7_4_2603 has no complex fusion categorification.

This extends the quadratic-center method without requiring equality in a
conductor compression bound. The two new ingredients are exact reciprocity
among all induced-unit characters and equality of Galois-paired relative
moments. The proof ends with one universal integer inequality.

## 1. Scope and exact source characters

The already proved four-case dihedral Morita reduction gives a dual with
eight invertibles and eight noninvertibles of dimension t=2+sqrt(5).
Schopieray's two-dimension Galois pseudo-unitarity theorem (corrected
published Lemma3.1), and Morita invariance of global dimension, reduce
general complex categorification to pseudo-unitary categorification.
This is the same scope bridge already used for the rank-seven family.
Work in the canonical positive spherical structure of that conjugate.

In source order the basis is (1,Y,Z,g,a,b,X), with

    d=(1,4+2sqrt(5),4+2sqrt(5),1,1,1,2),
    D=80+32sqrt(5),       Y*=Z.

The invertibles form V4. The complete source tensor is checked against
the following seven distinct one-dimensional characters. Put u=sqrt(-2)
and s=sqrt(5).

| Character | Values on (1,Y,Z,g,a,b,X) | Formal codegree |
|---|---|---|
| P | (1,0,0,1,1,1,-2) | 8 |
| U | (1,0,0,-1,1,-1,0) | 4 |
| V | (1,0,0,-1,-1,1,0) | 4 |
| C+ | (1,u,-u,1,-1,-1,0) | 8 |
| C- | (1,-u,u,1,-1,-1,0) | 8 |
| d-bar | (1,4-2s,4-2s,1,1,1,2) | 80-32s |
| d | (1,4+2s,4+2s,1,1,1,2) | 80+32s |

The verifier checks all 49 products for every character and its
duality-defined formal codegree. Seven distinct characters give the
complete basis of the commutative seven-dimensional fusion algebra.
The non-dimension character field Q(sqrt(-2)) is disjoint from Q(sqrt(5)),
so there exists a cyclotomic automorphism sigma that flips s and fixes
every other source character.

## 2. Full-row Galois transport and moment pairing

For a center simple A, let v(A)_i=[F(A):X_i]. With normalized center
S-matrix and the induced-unit constituent A_E, Ostrik's character
identity and modular Galois symmetry give

    chi_E(F(pi_sigma A))
      = epsilon_sigma(A) (f_E/f_(sigma E)) chi_(sigma E)(F(A)).

Write z(v)=A(v)+B(v)s, and let bvec=(0,2,2,0,0,0,0). The full signed
row transport is

    T(v)=v+bvec*(2A(v)-5B(v))/4.

This integer involution is checked on every character and each basis
vector, including the nontrivial dimension-codegree ratios 9+4s and
9-4s. An actual row must have partner T(v) or -T(v), with a uniform
sign making the row nonnegative. Mixed-sign images are impossible.

The vector of multiplicities in I(1) is fixed by S and hence by the
signed Galois action. Its support is preserved and its signs are
positive. The central unit therefore has forced partner J with row

    F(J)=1+Y+Z,        dim(J)=9+4s=D/conjugate(D).

The following observation replaces a conductor restriction. In a
cyclotomic field L containing all twists and K=Q(s), write t_K for
normalized relative trace. The canonical center has anomaly-free
modular data, so

    theta_(pi_sigma A)=sigma^2(theta_A).

Since sigma^2 fixes the quadratic field K and the cyclotomic Galois
group is abelian, for EVERY n

    t_K(theta_(pi_sigma A)^n)
       = sigma^2(t_K(theta_A^n)) = t_K(theta_A^n).

Thus paired row types have equal first and second relative moments.
Their individual twists need not coincide, and no conductor or exponent
bound is asserted. Aggregate multiplicities can be paired with the
same moment pair even when the Galois permutation on individual center
simples is not an involution.

## 3. Reciprocity forces exactly two induced-unit blocks

The six nonunit constituents of I(1) have dimensions

    9+4s;  10+4s,10+4s,10+4s;  20+8s,20+8s.

Every row has unit coefficient one and twist one. The induction Gram
matrix B_ij=sum_(k,l)N_(ki)^l N_(kj)^l has unit row

    B_(0,*)=(7,8,8,3,1,1,2).

After the forced J row, a codegree-eight row has the form
1+h+pY+(2-p)Z, where h is a nonidentity invertible and 0<=p<=2.
Both codegree-four rows must have X coefficient one: each can have
at most one, and their sum must supply the unit-row coefficient two.
They therefore have form 1+k+X+qY+(4-q)Z, with k a nonidentity
invertible and 0<=q<=4. The five h,k entries have multiset
{g,g,g,a,b}.

Symmetry of the S-matrix says

    f_F chi_E(F(A_F)) = f_E chi_F(F(A_E)).        (R)

Use the character names from the table. On a codegree-four row,
chi_P=1+1-2=0. Applying (R) to P with U and V forces the invertible
in the P row to be g. Applying (R) to P and C+ then forces p_P=1.
Thus the P row is 1+g+Y+Z.

For U or V against C+ or C-, the left side of (R) belongs to {0,16}.
The right side has real part in {0,8} and imaginary part proportional
to (2q-4)u. Equality therefore forces both real parts to be zero and
q=2. It follows that the two codegree-four rows have invertibles a,b,
one each, whereas both C rows have invertible g. Finally (R) between
C+ and C- gives p_++p_-=2. Up to permutation of the three
codegree-eight rows, the only possibilities are

    (p_P,p_+,p_-)=(1,0,2) or (1,1,1).

Consequently the two complete nonunit I(1) blocks are

    1+Y+Z;
    1+g+2Z, 1+g+Y+Z, 1+g+2Y;
    1+a+X+2Y+2Z, 1+b+X+2Y+2Z,

or the same block with all three middle rows equal to 1+g+Y+Z.

This is a theoretical enumeration. As an independent coverage check,
the verifier also reconstructs all50 bounded Gram/transport-compatible
low blocks, tries every character assignment within each codegree,
and rejects48 by the exact identities (R). The two survivors above
have respectively four and two distinct assignments of the named
characters, all covered by the same subsequent argument.

## 4. Arithmetic row bounds and a finite hull for all root orders

Every residual center row is (0,v), with v a nonnegative integer
six-vector. Its dimension z=A+Bs lies in Z[s]. The center's modular
formal-codegree integrality implies D/z is an algebraic integer.
Here the full ring of integers is Z[(1+s)/2]; we must not replace it
by Z[s]. With n=A^2-5B^2, the exact condition is

    2(80A-160B)/n and 2(32A-80B)/n
       are integers of the same parity.

Diagonal and entrywise Gram bounds leave465 global candidate rows.
For each of the two low blocks, subtract its rank-one contributions
to obtain R. Every residual row must satisfy vv^t<=R. The exact
principal-inverse/range test, and full-row Galois pairing, leave
72 and76 paired row types, respectively. The residuals have rank6.

For arbitrary roots of unity, the pair
(t_K(theta),t_K(theta^2)) lies in a seventeen-vertex hull. Put
u_±=(-1±s)/4. Its vertices are the five rational pairs

    (1,1),(-1,1),(1/2,-1/2),(-1/2,-1/2),(0,-1),

the six primitive pairs

    (u_+,u_-),(u_-,u_+),(-u_+,u_-),(-u_-,u_+),
    (0,-u_+),(0,-u_-),

and negative one-half times each of those six pairs.
The elementary complete proof is in Q5_ALL_ROOT_TWO_MOMENT_HULL.md.
It writes the root order as 2^a 5^b m. The only nonzero irrational
cases have b=1, a=0,1,2 and m odd, squarefree and prime to5.
Their primitive-order5,10,20 pair is scaled by mu(m)/phi(m), with
a possible exchange of signs. For m>1, phi(m)>=2, so the scale lies
in [-1/2,1]. All other cases vanish or lie in the rational hull.

## 5. One exact inequality

The pivotal odd-isotypic relations force the complete second-indicator
vector (1,0,0,1,1,1,1). In particular Y and Z are dual and have
indicator zero. A palindromic sandwich Y* X Y contains the unit once,
forcing nu_2(X)=+1; the TY square X^2 contains each invertible once,
forcing their indicators positive. The source verifier reconstructs
these implications rather than trusting the vector.

For each nonunit X_i, induction satisfies

    Tr(theta | I(X_i))=0,
    Tr(theta^2 | I(X_i))=D nu_2(X_i).

Subtract the known twist-one I(1) contributions and take relative
traces to K. Together with the residual Gram identity this gives45
rational equations:21 lower-triangular Gram coordinates,12 first
moment coordinates,12 second moment coordinates. Multiplication by8
clears all denominators in the seventeen hull vertices.

For a paired row orbit O and hull vertex (a,b,c,d), the column is

    8 sum_(v,z)inO vech(vv^t),
    8 sum_(v,z)inO (v_i z(a+b s))_(i=1..6),
    8 sum_(v,z)inO (v_i z(c+d s))_(i=1..6),

where the last two blocks are expanded in the basis (1,s).
The Gram order is lower triangular, with the first index increasing
and then the second, using zero-based residual indices. The target is
8*(vech(R), -k, D*nu_2-k), where k is the known low trace contribution.
Every genuine center gives a nonnegative real combination of these
columns; Section2 justifies using a common hull vertex on paired rows.

The universal covector, partitioned into its three coordinate blocks, is

    (38,58,26,63,76,8,57,69,-70,-72,7,19,-20,-100,-22,
      -100,-76,-100,-100,0,103;
     -17,50,-17,50,-43,100,37,-100,37,-100,33,-100;
     51,-100,51,-100,-72,100,-54,100,-54,100,-58,100).

Its dot product with EVERY allowed moment column is at least12.
There are1224 and1292 columns in the two branches, with1292 distinct
columns in their union. Its dot products with the two prescribed
targets are -1336 and -1240. Therefore neither target is a
nonnegative combination of allowed columns, which is the contradiction.

The proof uses no floating-point result. The portable verifier
verify_r2603_center_moments.py reads the original compressed census,
checks its immutable tensor hash, every character, the complete field
transport, low-block coverage, arithmetic row domain and all45-entry
integer inequalities. It imports only the exact enumeration helpers
from the separately audited quadratic-center verifier in the same
published stage. Both ordinary and optimized replays use only the
Python standard library.

The contradiction excludes pseudo-unitary categorification. The initial
two-dimension Morita/Galois bridge proves nonexistence over all complex
fusion categories.

Primary categorical identities are Ostrik, arXiv:1309.4822,
Theorems2.5,2.7,2.13 and Proposition2.8, the Ng-Schauenburg induction
indicator formula cited there, and the canonical center modular Galois
twist identity. The full-row derivation and its primary-source audit
are already recorded in GALOIS_FORGETFUL_ROW_LEMMA.md and
QUADRATIC_CENTER_TRACE_CATEGORICAL_AUDIT.md of the same evidence stage.

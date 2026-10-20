# Coupled cyclic rotation obstructions from center restrictions

This note separates the universal rotation identities from the arithmetic
specializations used for the two quadratic rank-seven rings. It states a
necessary-condition method; it does not assert that those two rings have
already been excluded.

## The universal C4/C8 condition

**Theorem.** Let C be a spherical fusion category over C, with simple objects
X_i, fusion coefficients N_ij^k, and indicators nu_n. Put
h_n(X)=dim Hom(1,X^n). For every object X there are nonnegative integers
u_0,...,u_3 and v_0,...,v_7 such that

\[
\begin{aligned}
\sum_{j=0}^3u_j&=h_4(X),&
\sum_{j=0}^3i^ju_j&=\nu_4(X),&
\sum_{j=0}^3(-1)^ju_j&=\nu_2(X^2),\\
\sum_{j=0}^7v_j&=h_8(X),&
\sum_{j=0}^7\zeta_8^jv_j&=\nu_8(X),&
\sum_{j=0}^7i^jv_j&=\nu_4(X^2),&
\sum_{j=0}^7(-1)^jv_j&=\nu_2(X^4).
\end{aligned}
\]

For X=X_i, the coupling terms are determined by the same simple-object
indicators used elsewhere in the system:

\[
\nu_4(X_i^2)=\sum_kN_{ii}^k\nu_4(X_k),\qquad
\nu_2(X_i^r)=\sum_k[X_i^r:X_k]\nu_2(X_k)\quad(r=2,4).
\]

All h_n and tensor-power multiplicities are computed from the fusion tensor.

**Proof.** Let E_n(X) be pivotal rotation on Hom(1,X^n). Ng–Schauenburg's
block-rotation identity, equation(5.4), identifies E_n(X)^r with the rotation
of r-fold blocks when r divides n. Their Theorem5.1 gives E_n(X)^n=1.
Hence E_4 and E_8 are diagonalizable with fourth and eighth roots of unity
as eigenvalues. Take u_j and v_j to be their eigenspace dimensions. The
block identifications give

\[
\operatorname{Tr}E_4^2=\nu_2(X^2),\quad
\operatorname{Tr}E_8^2=\nu_4(X^2),\quad
\operatorname{Tr}E_8^4=\nu_2(X^4).
\]

Taking traces proves the displayed relations. Additivity of ordinary
indicators on the Grothendieck group gives the source-fusion coupling.
The block-rotation argument itself needs only a pivotal category; sphericality
is used below to connect these traces to center induction. No dimension-field,
prime-divisor, or modular-compression assumption enters this theorem. □

**Explicit C4 form.** Write nu_4(X)=a+ib, m=h_4(X), and r=nu_2(X^2).
Then, in eigenvalue order1,i,-1,-i,

\[
(u_0,u_1,u_2,u_3)=\tfrac14
(m+r+2a,\ m-r+2b,\ m+r-2a,\ m-r-2b).
\]

These four quantities must be nonnegative integers.

**Explicit C8 form.** Put m=h_8(X), q=nu_2(X^4), and
nu_4(X^2)=s+it. Write uniquely
nu_8(X)=eta_0+eta_1 zeta_8+eta_2 zeta_8^2+eta_3 zeta_8^3.
Define

\[
A_0=(m+q+2s)/4,\quad A_2=(m+q-2s)/4,\quad
A_1=(m-q+2t)/4,\quad A_3=(m-q-2t)/4.
\]

Then v_j=(A_j+eta_j)/2 and v_(j+4)=(A_j-eta_j)/2 for0<=j<4.
They must all be nonnegative integers. In coordinates1,sqrt(2),i,i sqrt(2),
the coefficients of sqrt(2) and i sqrt(2) may be half-integers; requiring
all four coefficients to be integers would be an invalid extra constraint.
Keeping the eight eigenspace multiplicities avoids that error.

## Exact extraction from center data

Let F:Z(C)->C be forgetful, I its adjoint, D=dim(C), and d_i=dim(X_i).
For each central simple Y put v_Yi=[F(Y):X_i] and z_Y=sum_i v_Yi d_i.
Choose the twist convention in the center-indicator formula so that

\[
D\nu_n(X_i)=\sum_Yv_{Yi}z_Y\theta_Y^n. \tag{1}
\]

This is Ng–Schauenburg's spherical center formula. Using the opposite center
convention replaces every twist by its inverse and conjugates cyclic
characters; feasibility is unchanged if the convention is changed uniformly.

Let K be a number field containing D and all d_i, and let t_K denote the
normalized relative field trace from a common cyclotomic overfield. Applying
it to(1) gives the exact linear identity

\[
D\,t_K(\nu_n(X_i))=\sum_Yv_{Yi}z_Y\,t_K(\theta_Y^n). \tag{2}
\]

No constancy of fusion coefficients on Galois packets is required for this
averaging: v_Yi are integers and z_Y belongs to K. If K contains zeta_8,
then nu_4(X_i),nu_8(X_i) belong to K, so(2) determines the full indicators
needed in the theorem, rather than only their projections.

The restriction Gram identity M^t M=B, with M=(v_Yi), computes B from
F I(X)=direct sum_j X_j X X_j*. It bounds the integral restriction rows
and their multiplicities. For each finite candidate row, introduce counts
for its allowed relative phase records. Equation(2), the Gram identity,
and the C4/C8 equations form a rational linear system with nonnegative
integer variables. Clear denominators exactly. This construction is a
necessary relaxation of center data; feasible vectors do not supply
associators, a center fusion ring, or a categorical model.

## The special quadratic arithmetic used here

For the rank-seven application the dimension field is Q(sqrt(5)); we use
K=Q(sqrt(5),sqrt(2),i). A separately justified Cauchy-theorem argument limits
center twist prime factors to2 and5. This prime restriction is not a
consequence of the universal cyclic-rotation theorem.

For twist order2^a5^b, the 2-primary trace of its2^j-th power is zero exactly
when a>j+3. The nontrivial5-primary traces alternate between
(-1+sqrt(5))/4 and(-1-sqrt(5))/4; every power-of-two moment vanishes on the
5-primary factor when b>=2. CRT therefore gives exactly61 relative records
for moments1,2,4,8:60 visible records realized in Q(zeta_320), and one zero
record representing all orders with a>=7 or b>=2. This covers arbitrary
orders:320 is a modulus for the visible trace values, not a bound on all
twists. Choose L=Q(sqrt(5),sqrt(-2)), distinct from the larger trace field K.
This L contains both full source-character fields: it equals the field
for R5039, while R3895 has source-character field Q(sqrt(5)).
Automorphisms fixing L are therefore a valid, possibly smaller,
source-fixing subgroup for either ring. They act on twists by
squares, with packet size2^max(a-3,0)5^max(b-1,0), giving the zero
multiplicity relaxation16N+5N. The trace averages are taken over K, while
these row-fixing packet counts use L; those two subgroups must not be
confused.
The exact inventory and all-order proof are independently replayed in
`POWER_MOMENT_PHASES_PROOF.md` and the accompanying receipts.

Additional character-isotypic compression, conductor-eight mass identities,
prime-five saturation, and Galois row transport may reduce the finite domain.
Each is a separate hypothesis or previously proved lemma. In particular,
the raw normalized transport matrix can send a nonnegative row to a negative
vector; packet arguments must use the actual positive Galois row action.
None of those refinements is silently part of the universal C4/C8 theorem.

## Exact infeasibility certificates and scope

**Certificate corollary.** Suppose every categorification under a stated
spherical dimension/indicator choice maps to one of finitely many complete
integer systems A x=b, x>=0. If each system has an independently verified
integer infeasibility certificate, no categorification with that choice exists.
For example, an integer functional w and modulus m>1 with
wA=0 modulo m but wb nonzero modulo m exclude every integer x. Alternatively,
a rational Farkas functional or a finite exhaustive integer branch cover
with exact certificates can prove infeasibility. The proof is direct
application of each certificate to the necessary equations.

The finite row domain, phase inventory, and all branch coverage must be
verified as well as the certificate arithmetic. A solver's numerical
infeasibility flag is only discovery evidence. To exclude arbitrary fusion
categories, one must additionally prove that every possible categorification
admits one of the spherical structures or Galois reductions covered by the
systems. A pseudo-unitary computation alone does not supply that reduction.

## Primary references

1. S.-H. Ng and P. Schauenburg, *Higher Frobenius–Schur Indicators for Pivotal
Categories*, Contemporary Mathematics441(2007),63–90;
[arXiv:math/0503167v2](https://arxiv.org/pdf/math/0503167), equation(5.4) and
Theorem5.1, p12. This is the block-rotation source.
2. S.-H. Ng and P. Schauenburg, *Frobenius–Schur Indicators and Exponents of
Spherical Categories*, Advances in Mathematics211(2007),34–71;
[arXiv:math/0601012v3](https://arxiv.org/pdf/math/0601012), Theorem4.1 and
Remark4.3. These fix the center-indicator formula and twist convention.

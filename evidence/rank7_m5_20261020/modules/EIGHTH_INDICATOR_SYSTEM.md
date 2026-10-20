# Exact eighth-rotation system

This extends the independently audited fourth-rotation system. It is a
necessary condition on center data; no infeasibility outcome is claimed.

## Traces and grouping

Let R be the pivotal rotation on Hom(1,X^8). The grouping identity in
Ng--Schauenburg, arXiv:math/0503167v2, equation(5.4) and the proof of
Theorem5.1, gives

    R^8=1,
    Tr(R)=nu_8(X),
    Tr(R^2)=nu_4(X^2),
    Tr(R^4)=nu_2(X^4).

Thus put m=dimHom(1,X^8), q=nu_2(X^4), and
s+i*t=nu_4(X^2). The values m and q are fixed by the source tensor and
second-indicator case. The complex integer s+i*t is a fusion-linear
combination of the already introduced fourth indicators:

    nu_4(X_i^2)=sum_k N_(i,i)^k nu_4(X_k).

The unit contributes nu_4(1)=1. Its contribution must not be dropped.

## Integral Fourier coordinates

Write zeta=zeta_8 and use the actual integer basis

    O_(Q(zeta)) = Z[1,zeta,i,zeta^3].

If n_j is the nonnegative integer multiplicity of zeta^j, j=0,...,7,
then

    nu_8 = alpha + beta*zeta + gamma*i + delta*zeta^3,
    (alpha,beta,gamma,delta)=(n0-n4,n1-n5,n2-n6,n3-n7).

Let A_j=n_j+n_(j+4) for j=0,...,3. The complete inverse Fourier equations
are

    A0=(m+q+2s)/4,  A2=(m+q-2s)/4,
    A1=(m-q+2t)/4,  A3=(m-q-2t)/4,

    n0,n4=(A0 +/- alpha)/2,
    n1,n5=(A1 +/- beta)/2,
    n2,n6=(A2 +/- gamma)/2,
    n3,n7=(A3 +/- delta)/2.

These eight values must all be nonnegative integers. This includes every
parity condition, not only algebraic-integrality of nu_8. The remaining
traces are not independent: powers3,5,7 apply the corresponding Galois
automorphisms of Q(zeta_8) to nu_8; the sixth power conjugates s+i*t.

In the standard F8 basis used by the phase code, a permitted indicator
has the form

    nu_8 = a + r*sqrt(2) + i*(c+u*sqrt(2)),

with no sqrt(5) or sqrt(10) terms. Its integral coordinates are
alpha=a, gamma=c, beta=r+u, delta=u-r. Thus a,c must be integers and
r+u,u-r must be integers. The coefficients r and u may be half-integers.
Requiring integer coefficients separately on sqrt(2) and i*sqrt(2)
would wrongly remove valid cyclotomic integers such as zeta_8.

## Linear column implementation

`cyclic_eight_constraints.py` provides `append_cyclic_eight`. It accepts
the existing phase columns, the full source tensor, and the metadata of
`fourth_cyclic_constraints`. It appends eight nonnegative integer variables
n0,...,n7 for each nonunit source object. It enforces:

* the eight field coordinates of the induction identity
  sum_Y z_Y v_(Y,i) t_F(theta_Y^8) = D*sum_j n_j*zeta_8^j;
* the real and imaginary trace of R^2, coupled to existing C4 variables;
* the trace of R^4 and the dimension m.

The induced-unit constituents have twist1 and are included as the known
contribution. No division by D or hand-coded half-integral parity is
needed in the linear equations; the exact field coordinates of
D*zeta_8^j supply it automatically.

The C4 metadata stores, for source k, A_k=(m4+t2)/2 and B_k=(m4-t2)/2,
with fourth-indicator real part2a_k-A_k and imaginary part2c_k-B_k.
Accordingly the C8 R^2 constraints have targets

    N_(i,i)^0 - sum_(k>0) N_(i,i)^k*A_k,
    -sum_(k>0) N_(i,i)^k*B_k,

and coefficients -2N_(i,i)^k on a_k and c_k. This convention is tested
against the complete center of the pointed C2 category. The inverse
Fourier function is also checked exactly on all3^8=6561 choices
n_j in{0,1,2}. Both checks pass under optimized Python; all guards are
explicit exceptions, not assertions.

## All-order completeness of the phase inventory

For F=Q(zeta_8,sqrt(5)), the relative trace of a primitive two-primary
root is zero above order8, and that of a primitive fifth-primary root is
zero above order5. Twist orders are2^a5^b by categorical Cauchy.
For moments1,2,4,8 all four relative moments therefore vanish exactly in
the residual order regime a>=7 or b>=2. Every other order divides320.
The complete nonzero inventory has60 records:

* 24 records with nonzero first moment, from orders dividing40;
* 12 with first moment zero and second nonzero, from orders16/80;
* 12 with first and second zero and fourth nonzero, from orders32/160;
* 12 with first, second, fourth zero and eighth nonzero, from orders64/320.

Adding the genuine zero record gives61. The higher-order regime is not
omitted; it is represented by zero and its multiplicity packets.
The source-fixed per-row packet units for these four nonzero groups are
respectively1,2,4,8. Nontrivial fifth parts double those units on rows
whose actual sign-corrected T transport is fixed or dual.

The remaining genuine-zero per-row units, split by exact fifth-primary
part1/5/at least25, are16/16/5 generally and16/32/10 on actual fixed/dual
rows. These follow from the same all-order square-cycle proof as the C4
packets. In the conductor-eight c=0 active support the earlier cutoff
has a<=6,b<=1, so no genuine zero phase is allowed at all in this eighth
moment system. The previously proved order320 deletion may also be
retained for active rows.

This proves a complete finite phase description for the eighth-moment
test. It does not bound actual twists of inactive rows to320 and does
not assert that passing the test constructs a category.

Independent review subsequently checked the coupling signs and source-unit
term against the actual centers of Vec(C4), Vec(C8), and Vec(C16), including
objects with nu_4=0 and nu_8=1. The controls replay under normal and
optimized Python, with36,84,180 exact equations respectively; receipts are
`computation/cyclic_eight_coupling_*.json`. The independent phase audit also
rechecked all320 roots. These controls validate the implementation; they
are not tests of categorifiability of the two remaining source rings.

# R1768: exact sign of the diagonal finite dilogarithm

Date: 2026-10-27. This note proves positivity of the eleven nonzero diagonal
values. The separate norm-one argument is proved and independently audited
in `../r6_1660/R1768_LATTICE_LEMMA.md`; the independent phase audit is
`../r6_1660/R1768_PHASE_AUDIT.md`. Together they establish E(l,l)=1.
It does not by itself identify any Morita dual fusion ring.

Put tau=6+sqrt(37), epsilon=tau^2, gamma=[[145,12],[12,1]], and
T=[[1,1],[0,1]]. Then omega=tau+1 and

    gamma'=T gamma T^-1=[[157,-144],[12,-11]].

Its positive Hirzebruch--Jung period is (14,2,2,2,2,2,2,2,2,2,2,2).
The matrix product is gamma', and its attracting fixed point is omega.
Both eta multipliers are 1: their traces and lower-left entries agree,
and their lower-right entries agree modulo 12. Explicitly the multiplier
exponent is 146/144 - s(1,12) - 1/4 = 0, with s(1,12)=55/72.

The defining q-Pochhammer ratio gives exactly

    Phi_gamma',m,n(z; tau+1)=Phi_gamma,m,n(z; tau).

Here both modular arguments differ by 1 and m,n are integers, so no
exponential or square-root multiplier is introduced. The identity first
holds in a half-plane and continues to the nonsingular real values.
Thus the original index (l,l) becomes (l,0).

The original special argument is

    z=l omega/(epsilon^-1-1)=l-13l omega/12.

For l=1,...,11 choose x=1-l/12 and z0=x omega. Their difference is
(l+1)omega-l. The lattice-invariance calculation in RW Lemma 2 changes
the index to

    (l,0)+(l+1,-l)(gamma'^-1-I)
       =(l-12,144-12l)=(m,-12m),  m=l-12.

This is exactly the index attached to z0, since
(epsilon^-1-1)z0=m omega-12m. The two signs F+ and F- agree away
from the zero class. Therefore the nonzero diagonal value equals
Phi_gamma',m,0(z0;omega).

Let (omega_j,x_j,y_j) follow the HJ recurrence, with
omega_0=omega, x_0=x, y_0=0, and

    omega_(j+1)=1/(b_j-omega_j),
    x_(j+1)=b_j*x_j+y_j mod 1, chosen in (0,1],
    y_(j+1)=-x_j mod 1, chosen in [0,1).

All twelve pairs close up. Put t_j=x_j omega_j+y_j. For these eleven
nonzero classes, 0<t_j<1+omega_j. The defining Barnes-double-zeta
expression makes S(t_j;omega_j) a positive real number.

Keep the complex phase in RW Proposition 5's proof, using the exact
cocycle identity of Proposition 2(ii), instead of taking absolute values.
It gives

    product_j S(t_j;omega_j)
       = Phi_gamma',m,0(z0;omega) * exp(pi*i*P_l),

    P_l=sum_j [t_j^2-(omega_j+1)t_j
                   +(1+3omega_j+omega_j^2)/6]/(2omega_j).

The accompanying `verify_diagonal_phase.py` evaluates all terms in
Q(sqrt(37)) using rational arithmetic and proves P_l=0, for every
l=1,...,11. It also checks the twelve-step periodicity. Consequently

    E(l,l)=product_j S(t_j;omega_j)>0,  1<=l<=11.

This addresses the sign, not just the reality of E. To conclude E=1 one
must additionally prove that the displayed positive product has modulus
one. A direct lattice cone argument, rather than an unqualified invocation
of maximal-order ray-class theory, is appropriate: Z[sqrt(37)] is not
the maximal order of Q(sqrt(37)).

Primary source: Radchenko--Wheeler, *Real quadratic fields and finite
quantum dilogarithms I*, arXiv:2609.21892v2, Lemma 2 and Propositions 2,5.
https://arxiv.org/pdf/2609.21892

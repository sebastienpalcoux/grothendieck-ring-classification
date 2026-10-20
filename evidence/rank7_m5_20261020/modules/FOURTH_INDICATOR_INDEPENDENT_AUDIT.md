# Fourth rotation and the complete all-order phase domain

This is an independent audit of the fourth-indicator test and the extension
from visible phases to all possible twist orders. It is a necessary
categorical condition, not a claim that the complete domain has yet been
excluded.

## Cyclic multiplicities

Let X be a source object in the pseudo-unitary spherical Galois conjugate
whose existence follows from the already proved general reduction. Put

    m = dim Hom(1,X^4),
    t = nu_2(X^2) = sum_k N_(X,X)^k nu_2(X_k),
    nu_4(X) = a + b*i.

The pivotal rotation R on Hom(1,X^4) satisfies R^4=1. Moreover R^2 is the
second pivotal rotation on the grouped object X^2, under the associativity
identification. This follows directly from the composition identity and
its induction in Ng--Schauenburg, *Higher Frobenius--Schur indicators for
pivotal categories*, arXiv:math/0503167v2, equation(5.4) and proof of
Theorem5.1 (printed page12). Thus Tr(R^2)=t. These statements require a
pivotal structure; the established pseudo-unitary reduction supplies it.
They do not assume that an arbitrary categorification was originally
pivotal.

The eigenvalues of R are1,-1,i,-i. Consequently nu_4 belongs Z[i] and the
corresponding multiplicities are exactly

    (m+t+2a)/4, (m+t-2a)/4,
    (m-t+2b)/4, (m-t-2b)/4.

Each must be a nonnegative integer. The induction trace identity gives

    nu_4(X_i) = (1/D) sum_Y z_Y v_(Y,i) theta_Y^4.

Relative tracing to F=Q(sqrt(5),sqrt(2),i) is legitimate because both the
coefficients z_Y v_(Y,i)/D and the actual indicator belong to F. In
particular there is no need to impose reality of nu_4.

`integral_gram/fourth_indicator_audit.py` was read independently. It checks
that the supplied fixture has no hidden zero phases, computes theta^4
exactly in Q(zeta_80), verifies its constancy on every visible F-phase,
uses the tensor to obtain m and the chosen second-indicator case to obtain
t, and checks the four multiplicities above using exact fractions.
For that explicitly restricted input scope the implementation is sound.
A whole-domain test must use the additional phases below.

## Complete relative phases for moments1,2,4

The categorical Cauchy theorem gives twist orders2^a5^b. The field F is
Q(zeta_8,sqrt(5)). For a primitive two-primary root, relative trace to
Q(zeta_8) is the root itself when its order divides8 and zero at larger
orders. For a primitive fifth-primary root, relative trace to Q(sqrt(5))
is1 at order1, P_+ or P_- at order5, and zero at higher fifth powers,
where P_delta=(-1+delta*sqrt(5))/4. These independent primary factors
multiply, because the cyclotomic fields have coprime conductors.

Taking fourth powers lowers the two-primary exponent by2 and leaves the
fifth-primary exponent unchanged. Therefore all three moments1,2,4
vanish whenever a>=6 or b>=2. In every other case the order divides160.
This is an all-order reduction, not a trial cutoff on twists.

Let xi=zeta_8. The complete nonzero triple inventory has48 values:

* 24 values (xi^j*c1, xi^(2j)*c2, xi^(4j)*c1), j=0,...,7;
* 12 values (0,xi^j*c1,xi^(2j)*c2), j=1,3,5,7;
* 12 values (0,0,xi^j*c1), j=1,3,5,7.

Here (c1,c2) runs over (1,1),(P_+,P_-),(P_-,P_+). The first group comes
from orders dividing40. The second comes from exact orders16/80. The
third comes from exact orders32/160. Add the genuine zero triple to
obtain49 values. The12 new values have zero first and second relative
moments but nonzero fourth moment, and must not be folded into zero.

The model agent's `models/sqrt5/full_source_phases.py`, function
`phase_records_fourth()`, independently implements this inventory by
reduction modulo Phi_160. Its field-fixing subgroup is
{1,9,41,49,81,89,121,129}; its closed forms agree with the above48 values.
The published constant-coordinate representation therefore covers every
possible actual twist order, including all orders beyond160 through the
single genuine zero triple and the packet restrictions below.

## Source-fixed packets and refined genuine zero

For a row v, source-field-fixed squared Galois actions at exact order
2^a5^b force packet size divisible by

    2^max(a-3,0) * 5^max(b-1,0).

This gives packet units1,2,4 for the three nonzero groups above. On an
actual sign-corrected T-fixed or T-dual row, any nontrivial fifth-primary
part has a second disjoint packet: the sqrt(5)-changing automorphism can
fix the entire two-primary part and square to4mod5. Compose its label
permutation with duality if necessary. It returns to the same restriction
row and exchanges the exponent residue rmod5 with-rmod5. This remains
valid when raw T(v) is negative. The full proof is in
`SIGNED_FIXED_ROW_ZERO_PACKETS.md`.

After removing the new order32/160 records, the genuine zero triple has
only a>=6 or b>=2. Splitting it by exact fifth-primary order gives:

| Fifth-primary part | General per-row packet unit | Actual T-fixed/dual unit |
| --- | ---: | ---: |
|1 |8 |8 |
|5 |8 |16 |
|at least25 |5 |10 |

Thus the unrestricted zero semigroup is8N+5N. On fixed/dual rows its
three shared fifth-primary pieces have units8,16,10. For a visible new
order160 record, the basic unit4 similarly strengthens to8 on a
fixed/dual row; the exact order32 unit remains4.

## Active conductor-eight c=0 support

The prior sign-safe conductor-eight dichotomy bounds active twists in
case c=0 to a=4,5,6 and b=0,1, with total weighted support budget16 and
weight k(v)^2, k(v)=v_1-v_2. The genuine zero triple can then only have
a=6. Its per-row unit is8.

In fact the b=1 possibility is impossible on this active support. If
actual T is fixed or dual, the strengthened unit is16 per row; the
distinct dual row has the same nonzero k^2, so the cost is at least32.
Otherwise the actual T+duality orbit has at least four rows, each with
packet8 and the same |k|, again costing at least32. Both contradict16.
Thus active c=0 genuine zero support has exact order64 (b=0), with
per-row unit8. This conclusion uses the actual signed row orbit, not
unsigned positivity of the stored transport.

The full fourth-moment domain may impose these packet refinements and
the cyclic multiplicity equations simultaneously. Rejection of a
particular nozero fixture by the visible audit is not yet a rejection of
this enlarged complete domain.

Primary reference checked directly:
https://arxiv.org/pdf/math/0503167 (v2), equation(5.4) and Theorem5.1 proof.
The center induction trace formula is Ng--Schauenburg,
arXiv:math/0601012, Theorem4.1, already used by the existing moment code.

## Optional next doubling, if C4 is insufficient

The same rotation composition identity gives, for the eighth rotation,

    Tr(R8^2) = nu_4(X^2),
    Tr(R8^4) = nu_2(X^4).

The first right-hand side is the source fusion-linear combination of the
already introduced nu_4 variables; the second is a known fusion-linear
combination of the second indicators. Together with nu_8=Tr(R8), these
are linear conditions on the eight nonnegative integer eigenspace
multiplicities of R8. Powers coprime to8 act by cyclotomic conjugation on
nu_8, so no additional independent traces are missing.

For moments1,2,4,8 the all-order relative phase inventory has60 nonzero
values from roots320 and one genuine zero value (a>=7 or b>=2). It adds
only12 records to the fourth-moment inventory. The prior c=0 active
conductor-eight support cutoff has a<=6,b<=1, so no active genuine-zero
record remains in this eighth-moment domain. This is a proposed stronger
necessary test; no outcome has been asserted here.

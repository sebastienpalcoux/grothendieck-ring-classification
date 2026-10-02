# Finite spectral reduction for R7_4_1212 and R7_4_1213

This is a necessary-conditions reduction, **not a general exclusion**.
Both rings remain generally unresolved. It continues
`QUADRATIC_REMAINDER.md`, which reduces the dimension field to Q(sqrt5)
and initially leaves six possible global dimensions.

Choose the positive-second-indicator lift of every self-dual simple in
the full sphericalization. Opposite lifts have opposite indicators, and
the negative-indicator lift occurs with even multiplicity in every
square channel, by the pivotal parity theorem. The signed quotient T
therefore satisfies

    |T_ii^j| <= N_ii^j,  T_ii^j = N_ii^j modulo 4.

The source has an order-two invertible g fixing all five noninvertibles.
The square-channel congruence forces T_ii^g=1. Frobenius reciprocity
then forces g to act positively on every noninvertible. Its dimension
is +1, and the character (1,-1,0,0,0,0,0) has codegree two.

## All other signed codegrees belong to the quadratic field

Ostrik's Corollary 2.15, applied to the **full** sphericalization, places
every formal codegree in its categorical dimension field K. Its signed
sector codegrees are twice the signed Casimir eigenvalues. Since the
previous reduction proves K=Q(sqrt5), every signed codegree h belongs
to this field. Theorem 2.13 gives delta/h an algebraic integer; the
formal-codegree d-number theorem gives that h is a d-number, since
rational scaling preserves that property.

The two distinct dimension characters have codegrees delta and its
conjugate, with multiplicity two when delta is rational. Together with
the pointed codegree two they account for three of the seven signed
characters. Every other character sends g to +1 and has a nonzero
noninvertible coordinate, so its codegree is strictly greater than two.

Write a remaining irrational codegree as

    h=(a+b sqrt5)/2,  h'=(a-b sqrt5)/2,  b>0,
    n=Norm(h)=(a^2-5b^2)/4.

The exhaustive finite enumeration uses a and b of the same parity,
both roots greater than two, a bounded by the remaining Casimir trace,
and a^2/n integral (the quadratic d-number condition). For
delta=u+v sqrt5, integrality of delta/h is exactly

    c=u*a-5*v*b, d=v*a-u*b,
    n divides c and d,  c/n = d/n modulo 2.

This condition is imposed for both h and h'. Rational codegrees are
integers greater than two, with delta/h integral. The four residual
roots form four integers, two integers and a conjugate pair, or two
conjugate pairs. In each case they must satisfy

    sum 1/h = 1/2 - 1/delta - 1/delta',
    sum h <= B-delta-delta'-2,

where B is the source Casimir trace, 1036 or 1020. This exhausts a
bounded box of integer pairs and multisets, without enumerating signed
fusion tensors.

## Congruences and Casimir coefficients

Because T equals N modulo two, their Casimir characteristic polynomials
agree modulo two. The exact source polynomial is z^7 modulo two. Thus
each rational residual root is even, and each quadratic residual factor
z^2-a*z+n has both a and n even.

Let x=sum_i X_i^2 in the signed algebra, with coefficients x_j. The
commutative, self-dual Frobenius algebra identities give

    Tr(C_T)=coefficient_1(x^2)=sum_j x_j^2,
    x_j=sum_i T_ii^j.

The same identity holds for the source N. The square-channel congruences
therefore imply Tr(C_T)=B modulo eight. Here x_0=7 and x_g=5. For each
other x_j the checker computes the exact finite sum of the individual
square-channel coefficient domains. A surviving spectral trace must
occur as 74 plus the sum of the five possible x_j squares. This last
condition rules out the candidate of trace 1004.

## Exact surviving possibilities

The two dimensions 450+90sqrt5 and 450-90sqrt5 are excluded by the
modulo-eight trace condition. The complete remaining dimensions are

    180, 270+90sqrt5, 270-90sqrt5, 360.

The following table gives the residual four roots. A triple (a,b,n)
denotes the two roots (a plus or minus b sqrt5)/2, with norm n.

| delta (up to conjugation) | Rational residual roots | Quadratic pairs (a,b,n) | Total Casimir trace |
|---|---|---|---:|
| 180 | 12,18 | (140,60,400) | 532 |
| 180 | 4,180 | (210,90,900) | 756 |
| 180 | 18,60 | (300,132,720) | 740 |
| 270+90sqrt5 | 4,6,18,90 | none | 660 |
| 270+90sqrt5 | 4,6,30,30 | none | 612 |
| 270+90sqrt5 | 4,10,10,30 | none | 596 |
| 270+90sqrt5 | 4,10,12,20 | none | 588 |
| 270+90sqrt5 | none | (20,4,80), (210,90,900) | 772 |
| 270+90sqrt5 | none | (36,12,144), (210,90,900) | 788 |
| 360 | 4,6,20,36 | none | 788 |

`verify_spectral_remainder.py` reopens and validates the source census,
checks these finite spectra and the coefficient-domain condition, and
passes normally and under `python3 -O`. The output explicitly makes
zero classification decisions. Realizing or excluding these ten
possibilities is the remaining mathematical obstacle.

Primary references: Ostrik, arXiv:1309.4822, Theorem 2.13, Corollary 2.15,
and Section 5.1; Liu--Palcoux--Ren--Vercleyen, arXiv:2203.06522v5,
Theorem 3.9. The quotient construction and parity hypotheses are also
audited in the preserved `SIGNED_GENERAL_PROOF.md`.

# Weighted Q(sqrt2,sqrt3) central rotation

This is the specialization of `GENERAL_BIQUADRATIC_TRACES.md` to q=2,r=3.
The basis is (1,sqrt2,sqrt3,sqrt6), with conductors8,12,24 and linked signs
(epsilon2,epsilon3,epsilon2 epsilon3). The code verifies the quartic field,
the two square roots, the exact coordinate basis, and that the norm of the
global dimension has no prime factors outside {2,3}.

For height h the complete finite order box is

    2^(3+floor(log_2(h))) * 3^(1+floor(log_3(h))).

At height6 it is288. All divisors and all four linked signs are enumerated,
together with the joint zero type for orders outside this box. This is complete
for the retained powers, not a bound on an unknown categorical exponent.

The noncommutative Grothendieck algebra may have a two-dimensional simple
representation. Its central constituent has dimension D/f_E and occurs twice
in I(1); its column begins with2. The weighted low-frame enumeration handles
this multiplicity exactly. The whole Gram matrix is computed directly from
the fusion tensor, not replaced by a commutative Casimir shortcut. High-column
integrality, d-number, Gram, indicator, and cyclic-rotation constraints are
those detailed in the general proof.

`biquadratic_traces.py` certificates are explicitly pseudo-unitary only.
`biquadratic_lift.py` separately checks all original dimension characters and
all oriented signed quotients before accepting a general exclusion. Both
scopes are serialized and checked. The independent cyclotomic quotient checker
covers every in-box order and every retained power, using linked Gauss sums
rather than the production trace formula to compute the comparison values.

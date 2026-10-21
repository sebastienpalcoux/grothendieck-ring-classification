# Review of the character-labeled atomic modular relaxation

Accepted scope: a necessary pseudo-unitary central-induction relaxation
when every character of the commutative ring lies in its totally real
FP field. This review does not certify a new ring exclusion. A proposed
general exclusion must additionally verify every complete-domain ray,
every indicator branch and the general sphericalization reduction.
This is separate AI review, not human or formal proof-assistant review.

The earlier partial-S/STS review establishes the normalization

    sum_Z theta_Z chi_E(v_Z) chi_F(v_Z) = f_F chi_E(v_F).

For each non-FP character G, the new system has one independent simplex
of integral restriction columns c of dimension D/f_G. Every actual low
frame maps to one-hot choices in these simplices. Thus this construction
is a relaxation; an exact rational feasible point need not be a low
frame or a fusion category.

The linear S-symmetry coefficient is beta_E chi_E(c) for a choice in
simplex F, minus beta_F chi_F(c) for a choice in simplex E. Symmetry
identities involving the FP character hold automatically from the
prescribed dimensions and the fixed tensor-unit restriction.

Separating the tensor unit in STS gives the coefficient

    chi_E(c) chi_F(c) - delta(G,F) f_F chi_E(c)

on each nonunit choice, and right side delta(F,FP) f_F - 1. The unit
contributes exactly one on the left. This derivation also covers F=FP;
there is then no variable for v_F and its value on every character is
one. All coefficients lie in the relative-trace field. Dual high objects
are kept in complete pairs with the same twist, so the relative trace
can multiply their exact real coefficient. No complex phase is dropped.

The implementation uses disjoint appended row indices and positive exact
denominator clearing. Its factored high-column pairing is the exact
bilinear field product used in the direct column formula. The reviewer
read these formulas and freshly ran `verify_atomic.py` with Python
optimization. It passed: all 419 columns were compared to the complete
oracle for three integer covectors; all 576 permitted labelings of the
known Fib tensor Vec(V4) complete low frame reproduced the direct
S-symmetry and STS defects, including the tensor-unit term; all twelve
known central restriction types passed the spectral filter; and the
saved rational primal satisfied every equation exactly.

The narrower real-FP adapter cannot apply to R334 because its entire
character table does not split in that field. Its preflight failure is
not an obstruction to categorification. Fib tensor Vec(V4) is a valid
positive control for this implementation.

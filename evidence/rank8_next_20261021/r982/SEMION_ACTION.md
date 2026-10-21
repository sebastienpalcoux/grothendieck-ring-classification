# Central semion and semion-duality restrictions

These are necessary conditions under the pseudo-unitary hypothesis used by
the integer-center and phase systems. They are not a construction of a
fusion category.

The exact finite-domain propagation for frame2 forces the unique central
simple G whose forgotten restriction is the source invertible g (index6).
It has FP dimension1. The complete distinguished frame contains precisely
one simple restricting to the source tensor unit, so G squared is the
central tensor unit. Frames2 and3 have the same mathematical systems and
phase columns.

Every central simple containing source g upon forgetting is a translate
by G of one of the complete distinguished low simples: monoidality gives

`Hom(g,F(Z)) = Hom(1,F(G tensor Z))`.

Consequently those high masses are fixed by the low frame. All other high
restriction types must be permuted by multiplication by source g, and their
masses agree along this permutation. This gives106 new exact equations.

For the residual phase branches, the source second indicator of g is -1.
Since the forgetful functor preserves the pivotal structure, G has the
same second indicator; its order-two pointed ribbon subcategory has
`theta(G) = +/- i`. For every central simple Z, its monodromy with G is a
sign, since the fusion character of the order-two invertible G squares to1.
The balancing identity gives

`theta(G tensor Z) = +/- i * theta(Z)`.

Thus tensoring by G has no fixed central simple. Whenever the forgotten
restriction v is fixed by source multiplication by g, its multiplicity is
even.

There is a second, stronger parity restriction. Ribbon duality gives
`theta(Z*) = theta(Z)`, so `G tensor Z` cannot be isomorphic to `Z*`.
The permutation `H(Z) = G tensor Z*` is an involution without fixed points.
If `g*v = v*`, H preserves the restriction type v. Its multiplicity is
therefore even, including the case where g interchanges the two vectors
of a nontrivial duality orbit. This adds25 further parity conditions, for
54 even-mass conditions in total.

The duality argument and the central-action argument were independently
reviewed by the semion/fermion task. The resulting integer domain has an
exact integer survivor (`central_dual_milp24.json`); this is only a survivor
of necessary equations, bounds, parity conditions, and finitely many lifted
phase cuts. The whole phase domain is tested separately.

The direct positive control in `semion_action_control.py` checks the free
G action and free G-duality action in the actual double-semion modular
category (Semion tensor its reverse). Its four twists are 1,i,-i,1.

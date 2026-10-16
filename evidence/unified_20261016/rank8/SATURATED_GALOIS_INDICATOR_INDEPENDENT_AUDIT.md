# Independent audit of the saturated Galois indicator lemma

Auditor: `simple_global`, 2026-10-16. **Status: PASS.**

I independently checked the complete argument in
`SATURATED_GALOIS_INDICATOR_LEMMA.md` and its R630 application.
Writing a central dimension as `z=sum_i v_i d_i`, linearity gives
`ell(z)=sum_i v_i ell(d_i)`. Thus the weighted first trace is exactly
`sum_A ell(z_A) z_A theta_A = D ell(1)`.

The kernel of the nonzero rational functional `ell` on the quadratic
field is precisely the rational line spanned by `D`. Consequently all
rational-ratio terms vanish. The remaining terms have twists of order
dividing `f` by the explicitly assumed conductor conclusion, while
the constituents of `I(1)` have twist one.

The stated Chinese remainder construction does extend the prescribed
automorphism of the `f`th roots to the full twist field. This remains
true if `k` is not coprime to the larger twist conductor: at primes
outside `f`, one chooses a different representative modulo `f`.
That automorphism fixes every coefficient and replaces each surviving
twist by its `k`th power. The indicator trace formula therefore gives
the asserted exact complex equality. No real-part projection, reality
assumption on indicators, or commutativity of the source ring occurs.

For R630, the source weights `(3,3,-4,-1,-1,-4,2,2)` and cubic
multiplicities `(1,0,0,1,1,1,0,0)` reduce the identity to three
unit-modulus third indicators with weights `1,1,4`. The strict
triangle contradiction is valid. The general-complex scope uses the
separately audited spherical/Galois-PU gate, not unitarity.

This audit checks the lemma and this deduction. Each application must
still independently establish its conductor hypothesis, source data,
and scope bridge; they are not consequences of the lemma itself.

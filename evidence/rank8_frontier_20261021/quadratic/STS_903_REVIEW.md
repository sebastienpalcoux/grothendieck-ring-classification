# Independent review of the complete R903 STS obstruction

The candidate receipt is
`../global_induction/complete_results/R8_3_903_sts_frame_h4.json`.
The independent no-argument replay is `review_sts_903.py`; it compares
against `review_sts_903_results.json`. Run it normally and with `python -O`.
The receipt binds the source tensor, certificate, and exact operator sources.

The reviewed domain is a necessary pseudo-unitary center relaxation with
the complete height-four relative-twist trace domain. It has 341 rows and
52,127 columns: four labeled low frames, 1,532 complete high duality orbits
times 34 relative trace types, and 35 rotation columns. The 58,398 raw
complete low Gram frames are filtered by exact modular eigenvalue integrality
and full distinguished-center S symmetry. The complete character table lies
in Q(zeta_24), whose real subfield is the FP field Q(sqrt(2),sqrt(3)).
Every high duality orbit is summed before the relative trace is applied;
the independent reviewer checks that the unprojected summed character
product is real. Distinguished twists are one. Thus the stated real STS
equations apply without a larger trace field.

The review reuses the accepted finite-domain constructor but independently
recomputes every low S and STS coefficient and every high-orbit STS
coefficient directly in the character field. It then pairs every complete
column with every saved exact integer separator, checks every pairing is
nonnegative, and checks the right-hand-side pairing is strictly negative.
All eight allowed second-indicator assignments are covered by two separators.
The factored full-domain oracle is also compared against these direct scores;
it is not used to establish their inequalities. The positive controls for
this unchanged STS operator are retained in the shared operator validation
and the independent CM review's complete packed-column controls.

The general lift is a separate essential step, replayed through the accepted
oriented signed-extension verifier. The two spherical character orbits have
degree four; one is the FP Galois orbit and the other violates duality.
All 64 signed branches are exhausted: 32 are gauge equivalent to the source;
each of the other 32 has a duality obstruction and a formal-codegree norm
obstruction at the prime 3. The latter global-dimension polynomial is

    t^4 - 576 t^3 + 11520 t^2 - 73728 t + 147456.

Only the successful complete independent replay, including this lift,
supports a general complex fusion-category exclusion. In particular, the
pseudo-unitary linear obstruction alone is not promoted to general scope.

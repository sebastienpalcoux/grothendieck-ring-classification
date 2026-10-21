# Independent review of the complete R1617 STS obstruction

The candidate receipt is
`../global_induction/complete_results/R8_3_1617_sts_frame_h4.json`.
The isolated no-argument exact replay is `review_sts_1617.py`, with receipt
`review_sts_1617_results.json`. Run it normally and with `python -O`.
The receipt binds the tensor, producer certificate, and operator sources.

The necessary pseudo-unitary center relaxation has 341 rows and 130,431
columns: six labeled low frames, 3,835 high duality orbits times 34 relative
trace types, and 35 rotation columns. The complete height-four trace domain
uses the proved representative-order bound 288. The 118,696 raw complete
low Gram frames are filtered by exact modular eigenvalue integrality and
distinguished-center S symmetry. The complete character table lies in
Q(zeta_24), with FP field Q(sqrt(2),sqrt(3)).

The independent reviewer reuses the accepted complete-domain constructor
but recomputes all 216 low STS coefficients and all 138,060 high-orbit STS
coefficients from the exact character table. It checks S symmetry, constant
right-hand sides, and reality of unprojected high-orbit character products
before the relative trace. It pairs all 130,431 columns directly with both
integer separators and checks the strictly negative right-hand-side
pairings for both allowed second-indicator choices. The full factored oracle
is also compared with the direct scores; it does not establish those direct
inequalities. Numerical proposal routines are not used in replay.

General scope requires the separately replayed oriented signed-extension
certificate. The spherical character factors have degrees 2, 2, and 4.
Both quadratic alternatives fail the formal-codegree norm criterion at 3;
the quartic alternative is the FP Galois orbit and reaches the verified
pseudo-unitary obstruction. The norm certificate uses the polynomial

    t^4 - 576 t^3 + 11520 t^2 - 73728 t + 147456.

The complete signed-extension domain has two branches, both gauge equivalent
to the source. The unchanged operator's positive-model controls remain in
the shared validation receipts. Only successful complete independent replay,
including the signed lift, supports the general complex fusion-category
exclusion; the pseudo-unitary linear certificate alone does not.

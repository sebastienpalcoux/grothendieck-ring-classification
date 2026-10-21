# Independent review of the complete R1661 STS obstruction

The candidate receipt is
`../global_induction/complete_results/R8_3_1661_sts_frame_h4.json`.
The no-argument independent exact replay is `review_sts_1661.py`, with
receipt `review_sts_1661_results.json`. Run it normally and with `python -O`.
The receipt binds the tensor, producer certificate, and operator sources.

The necessary pseudo-unitary center relaxation has 341 rows and 103,773
columns: four labeled low frames, 3,051 high duality orbits times 34 relative
trace types, and 35 rotation columns. Its complete height-four trace domain
uses the proved order bound 288. The 76,984 raw complete low Gram frames
are filtered by exact partial modular integrality and distinguished-center
S symmetry. The retained full character table lies in Q(zeta_24), with
FP field Q(sqrt(2),sqrt(3)).

The reviewer reuses the accepted complete-domain constructor and independently
recomputes all 144 low STS coefficients and all 109,836 high-orbit STS
coefficients directly from the character table. It checks S symmetry,
the constant right-hand sides, and reality of the unprojected high-orbit
product before applying the relative trace. It then pairs all 103,773
columns directly with each of the two exact integer separators. Both
allowed second-indicator vectors are covered; the complete factored oracle
is additionally compared with the direct scores. It is not used to establish
their nonnegative pairings. No numerical proposal routine is used in replay.

General scope requires the separately replayed oriented signed-extension
certificate. The spherical character factors have degrees 2, 2, and 4.
The two quadratic alternatives fail the formal-codegree norm criterion at
3; the quartic alternative is the FP Galois orbit and reaches the verified
pseudo-unitary obstruction. All six signed branches are exhausted: two
are gauge equivalent to the source, and every character orbit in each of
the four others fails the norm criterion at 3. The global-dimension
polynomial used for these norm obstructions is

    t^4 - 576 t^3 + 11520 t^2 - 73728 t + 147456.

The unchanged shared operator's known-model positive controls remain in its
published validation receipts. Only a successful complete independent replay,
including all signed branches, supports the general complex fusion-category
exclusion. The pseudo-unitary linear obstruction by itself does not.

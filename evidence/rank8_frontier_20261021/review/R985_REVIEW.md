# Review of the R985 general exclusion

Accepted conclusion: R8_3_985 has no categorification by a complex fusion
category. This is separate AI mathematical and computational review, not
human review or proof-assistant formalization.

The pseudo-unitary obstruction uses the previously reviewed complete
low-frame hull, exact partial-S integrality and distinguished-center STS
equations. The full character table lies in Q(zeta_24), with the actual
relative-trace field Q(sqrt(2),sqrt(3)). Every high duality orbit is paired
before taking the relative trace: its character-product coefficient is
real and lies in that field. No identity replacing Re(theta c) by
theta Re(c) for an unpaired complex coefficient is used.

The complete raw low domain has 118,696 frames. Exactly two frames admit
distinguished-S-symmetric labelings, with two labelings each; these give
four separate low columns. No low column is removed by the partial-S
integrality filter. It removes 1,555 high restriction vectors, leaving
3,045 vectors in 1,605 duality orbits. Together with all 34 height-four
joint trace types and the proper-divisor rotation variables, this gives
54,609 columns and 341 equations. Both permitted second-indicator tuples,
(0,0,0,0,-1,1,1) and (0,0,0,0,1,1,1), have complete exact separators.

The reviewer freshly replayed the canonical general producer with Python
optimization; it passed. The additional `verify_r985_direct.py` check
does not use the factored Farkas oracle to establish any column inequality.
It first reconstructs all 144 low STS coefficients from the unnormalized
S-matrix identity and all 57,780 high-orbit character products directly in
the exact cyclotomic field. Every high coefficient is checked to be real
before tracing and to equal the stored relative-field coefficient. All
these identities passed.

It then constructs every one of the 54,609 columns explicitly and pairs
it with both saved integer rays. Every pairing is nonnegative; the two
right-side pairings equal the saved strictly negative integers. The exact
score sequences are hash-bound in `r985_direct.json`. This review shares
the already validated complete domain constructor, native low-frame
enumerator and exact character primitives. It does not claim an
independent rewrite of those components; its additional independence is
the direct modular formulas and full explicit-column evaluation instead
of the factored separator oracle.

For general complex scope, the ordinary spherical character alternatives
are one FP quartic orbit and one quartic orbit rejected by unequal dual
dimensions. The complete oriented signed lift has 24 branches: eight
are gauge-original, and the other sixteen are rejected by sixteen exact
norm obstructions and sixteen dual-dimension obstructions. The canonical
replay verifies every branch and the spherical-to-pseudo-unitary Galois
reduction. Thus no pivotality or unitarity assumption is imposed on the
final noncategorification conclusion.

The mathematical normalization and primary references are recorded in
`PARTIAL_S_STS_REVIEW.md`; the exact current coefficient checks and scope
are pinned in `r985_review_receipt.json`. The producer certificate is
`global_induction/sts_results/R8_3_985_h4.json`.

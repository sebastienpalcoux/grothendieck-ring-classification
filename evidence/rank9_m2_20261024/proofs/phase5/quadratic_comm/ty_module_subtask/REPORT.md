# TY module structure result

A uniform categorical reduction is proved in `THEOREM.md` for R9_2_137, R9_2_1607 and R9_2_1976. Their integral TY(V4) subcategories must have the nonalternating bicharacter. Condensing the uniquely determined isotropic involution (source indices 1, 5 and 8 respectively) gives a Morita dual of rank twelve, with invertible group D8 and four noninvertibles of dimension 4+3sqrt(2), stabilized by the center of D8. The argument applies to arbitrary complex fusion categories.

This identifies the correct algebra for the pointed integral dual. The internal end 1+h of a nonintegral simple uses an anisotropic h and is not that algebra; one must use the third, free involution g instead.

The exact ring hypotheses pass in `verify_structure.py` and `structure_certificate.json`. The categorical input is the general Tambara–Yamagami classification and the explicit subgroup-algebra bimodule formulas of Meir–Musicantov, not a unitary reconstruction theorem. The sign tau remains unrestricted.

No source ring is excluded or modeled by this result. The outstanding task is to classify the possible D8-quadratic dual rings, including their associators. At the coarsest level their noninvertible square has center-stabilizer contribution 1+z and four nonnegative noninvertible coefficients summing to eight. Full module-action data and lower-rank tests can narrow these choices, but a surviving based ring is not a category.

## Exact completion follow-up

`DUAL_COMPLETION.md` completes the full Morita action census. Each source yields exactly 28 labelled D8 based-ring completions. Twenty fail the formal-codegree field obstruction in the pseudo-unitary lane. Four contain previously general-excluded adjoint subrings R6_4_6 or R6_4_174, with full coefficient transports and prior certificates preserved. The remaining four labelled completions form three common uniform-multiplicity-two D8 ring isomorphism types. All three original source rings still remain unresolved. Source general-to-pseudo-unitary existence reductions are needed when using the field pruning for a general categorifiability implication.

The nontrivial quotient-action survivor has six distinguished I(1) central simples, while the two identity-action survivors have nine. This difference is preserved in `survivor_formal_codegrees.json`; equal regular-Casimir polynomials must not be interpreted as equal formal-codegree multiplicities.

## Forced-associator refinement: two surviving types

`FORCED_D8_ASSOCIATOR.md` now eliminates the nonidentity quotient-action type (cases 26 and 27 in each source). The pointed D8 dual has a forced nontrivial class 2 on its cyclic rotation subgroup, deduced from the Morita-invariant weighted fourth indicator of the nonalternating TY category. The candidate action equates rX=Xs for a rotation r of order four and a reflection s of order two. Its cyclic stabilizer would require this class to be a coboundary, whereas the reflection contribution pulls back trivially from C2 to C4. This is a general-complex module-associativity contradiction, with no positive, pivotal or unitary hypothesis on the full ambient category.

The exact certificate is `forced_associator_certificate.json`, reproduced with the standard-library script `forced_associator_check.py`. It checks the six tensor witnesses, all 64 values of the explicit pullback coboundary, and the supplementary induction overlaps. The current frontier consists of **two** common uniform D8 based-ring types: case 12 (identity theta, alpha zero) and case 25 (identity theta, nonzero reflection alpha). These are necessary possibilities, not models. All three rank-nine source rings remain unresolved.

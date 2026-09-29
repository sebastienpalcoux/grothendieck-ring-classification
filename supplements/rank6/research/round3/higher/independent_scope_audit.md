# Independent audit of the integral Morita criterion

The independent arithmetic workstream reviewed
`software/round3_integral_morita.py` against the inherited
`software/full_morita_gram.py` and found no integrality or categorical-scope
issue in the new step.

* Each unknown counts simple dual objects sharing one enumerated
  right-action matrix, so its value is a nonnegative integer.
* The inherited full Gram construction exhausts the bounded right-action
  matrices and retains multiplicities through the first-column count rows.
* The dual unit is subtracted once. Allowing another simple object with the
  identity action matrix is a valid weakening; it creates no false exclusion.
* Removing duplicate augmented equality rows preserves the integral
  solution set.
* The checked congruences yA=0 and yb≠0 modulo2 contradict every integral
  solution, without any hypothesis on categorical dimensions or pivotality.
* The composite verifier reconstructs the complete module domain before
  applying the conditional higher-indicator exclusions. General scope is
  obtained separately through the verified signed Galois reduction.

This is a review of the categorical and arithmetic logic. Optimizer-free
full computational-certificate replay is recorded separately in the
`*_verify_conditional0.json` and `*_general.json` reports.

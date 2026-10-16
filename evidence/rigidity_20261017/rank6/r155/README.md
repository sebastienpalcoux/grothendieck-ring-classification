# Odd cyclic Clifford constraints for R6_4_155

**AI-generated research · independent verification pending.** These arguments and data have not been independently verified by a human mathematician or formalized in Lean.

The spherical anticommuting-stabilizer argument gives a spin-character convolution constraint on every odd generalized pivotal rotation. The rank-six manuscript proves the categorical statement and its all-order path-divisibility consequence. This directory checks the finite character data of the surviving R6_4_155 modular candidate; it does not construct or exclude a categorification.

From the repository root:

```sh
python evidence/rigidity_20261017/rank6/r155/verify_odd_clifford.py --repo .
python -O evidence/rigidity_20261017/rank6/r155/verify_odd_clifford.py --repo .
```

The checker pins the inherited full generalized-rotation certificate by SHA256, verifies its complete index domain, and binds the noninvertible and stabilizer labels to the full multiplication tensor. It reconstructs the odd spin spectra directly from sign vectors and performs exact rational circulant inversion for both noninvertibles, all 52 central targets and orders 3, 5, ..., 23. All 1,144 blocks have nonnegative integral quotient multiplicities. The receipt records every quotient.

The same checker verifies the formal polynomial identities in the parameter m used in the all-order path argument. The infinite family of path-Clifford multiplicity divisibilities for R′(m) is equivalent to m being even. This gives no exclusion at m = 4.

Four deliberately invalid controls are rejected: a negative quotient, a nonintegral quotient, an inconsistent dimension and an even-order request. Normal and optimized Python produce identical receipts; checks do not depend on Python `assert` statements.

The source theorem and exact finite scope are recorded in `ODD_CLIFFORD_ROTATION.md`. No even-order half-spin condition is asserted or used. Passing these conditions does not supply compatible associators, a module category or a categorification.

# R6_8_1660: all indicators and central phase masses

**AI-generated research · independent verification pending.** These arguments and data have not been independently verified by a human mathematician or formalized in Lean. Exact checks certify their stated arithmetic and finite-domain scope.

The ring remains unresolved for general complex categorification. The two saturated irreducible modular summands fix all six indicator sequences at every order. Their period divides 48. Fourier inversion determines all 288 dimension-weighted restriction masses for either of two conjugate choices. This forces exactly eight spin simples, each restricting as `2X + 2gX + sigma + 3T`, two in each of four primitive order-16 phases. The homogeneous phase Gram identities leave 640 labelled restriction profiles, in branches of sizes 68, 286, 286. These necessary data do not construct a category or prove nonexistence.

From the repository root:

```sh
python evidence/rigidity_20261017/rank6/r1660/verify.py --repo .
python -O evidence/rigidity_20261017/rank6/r1660/verify.py --repo .
```

Python 3.12 and SymPy are sufficient. The standard-library primary calculation is `all_indicators.py` and `phase_masses.py`. The independent `independent_audit.py` uses SymPy polynomial remainders modulo the cyclotomic polynomial and rational linear solves; it imports none of the primary field arithmetic. It checks every mass, all inverse Fourier transforms, all 48 Ising indicators directly from their modular formula, and the dimension-field basis.

`phase_gram_audit.py` independently reconstructs the profile filter using exact coefficient convolution and meet-in-the-middle products. Its local residual Gram positivity test is the necessary inequality `(sum q²)(sum a²) >= (sum qa)²`. It checks every available multiplicity and every phase target, with explicit source hashes. The discovery profile witnesses are retained in `phase_full_gram_filter.json`; all passing allocations are checked against an independently exhausted domain. No floating-point optimizer is used.

The source tensor and finite-group character tables are hash-bound. The complete replay checks package identities and includes deliberately altered phase-mass and tensor-source rejection controls. Mathematical conditions use explicit exceptions, so optimized Python retains them. The replay manifest does not replace the separate categorical arguments, and no claim concerning an unknown modular-representation complement is inferred from a particular witness.

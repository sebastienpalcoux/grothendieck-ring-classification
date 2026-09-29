# Third-round arithmetic continuation

Four previously unresolved multiplicity-eight tensors are now excluded over
C with no pivotal, spherical, pseudo-unitary or unitary assumption:
`R6_8_6524`, `R6_8_6525`, `R6_8_6526`, and `R6_8_6999`.

The authoritative certificates are the four `*_general.json` files.
For 6524, 6525 and 6999, use `software/round3_arithmetic.verify(R,c)`.
For 6526, use `software/round3_split_arithmetic.verify(R,c)`.
Each certificate reconstructs the full signed dimension-field restriction,
finite spectrum enumeration, saturated signed associativity and an existing
exact pseudo-unitary moment obstruction. Every conclusion starts from the
complete tensor; identifiers do not enter the theorem or verifier.

* `proof.md` gives the inert quadratic and cyclotomic cubic local-factor
  isolation theorems and rational complementary-codegree search.
* `split_different_proof.md` proves the general different-ideal theorem and
  the finite abelian field analysis needed for the fourth ring. Its TeX
  version is `papers/chapters/round3_split_different.tex`.
* `full_census_scan.json` checks the first theorem on all 16,612 tensors:
  eleven satisfy its hypotheses, four have direct spectrum exclusions
  already present in the previous ledger, and three additional frontier
  tensors are excluded using the certified general-to-PU reduction.
* `verification.json` and `verification_optimized.json` are the normal and
  optimized-Python optimizer-disabled controls for those three exclusions.
* `split_verification.json` and `split_verification_optimized.json` do the
  same for 6526, including the all-census scan. Only that tensor has the
  required split quadratic arithmetic profile.

All 54 established realized rings were checked against both criteria and
are ineligible; no new positive-model construction is claimed. Both audit
launchers check a nontrivial tensor permutation and reject four altered
certificates. The quartic part uses exact root isolation and rational
trace-dual bounds, without numerical optimization.

Reproduce from the release root:

```sh
python research/round3/arithmetic/verify_arithmetic.py
python -O research/round3/arithmetic/verify_arithmetic.py
python research/round3/arithmetic/verify_split.py
python -O research/round3/arithmetic/verify_split.py
```

The standalone `explore_*.py`, `probe_6525.py`, `quartic_explore.py`,
`quadratic_allcomplements.py` and their logs retain the discovery history.
In particular the 60-second unrestricted signed CSP trials were incomplete
and supply no exclusion. The floating exploratory quartic boxes were
superseded by the fully exact bounds in `round3_split_arithmetic.py`.

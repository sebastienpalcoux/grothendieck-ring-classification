# Theoretical continuation of the eleven open cases

**24 October 2026: R10_1_189 is unitarily realized. Ten cases remain open.**

The rank-ten multiplicity-one classification is complete for the supplied
194-ring census: **136 general exclusions, 58 unitary models, no unresolved
rings**. This counts Grothendieck rings with at least one model, rather than
inequivalent categories.

The model is a fusion subcategory of the established conformal-embedding
module category for SU(4) at level 6 inside SU(10) at level 1. This is a
recognition in a classical construction; no new tensor category is claimed.
The proof constructs the category and checks all 1,000 source coefficients.
An associated rank-fourteen modular category and its actual étale algebra
are constructed as well. Consistent modular data alone are not used as an
existence proof.

## Read in rank order

| Rank | Current result | Proof and scope |
|---:|---|---|
| 6 | Both cases remain open. Even cyclic Clifford constraints pass all 1,144 tested exact blocks. The R1660–R941 Morita identification is conditional on the required algebra. | [Rank-six report](proofs/unresolved11_retry_20261024/rank6/RANK6_RETRY_REPORT.md) · [Earlier deductions](proofs/unresolved11_20261024/rank6_pair/RANK6_REPORT.md) |
| 8 | All four cases remain open. R928 has categorical Morita rigidity. A twisted GH(C6,2) precursor for R1768 now exists, but its required algebra is unproved. Five pointed-extension construction families for R1154 are ruled out. | [R928 rigidity](proofs/unresolved11_20261024/rank8_quartic_pair/R928_MORITA_RIGIDITY.md) · [R1768 construction](proofs/unresolved11_retry_20261024/quadratic8/TWISTED_GH6_CONSTRUCTION.md) · [Rank-eight report](proofs/unresolved11_retry_20261024/quadratic8/REPORT.md) |
| 9 | All four cases remain open. No central Tannakian subcategory exists; integral central simples are invertible. New stabilizer and Clifford theorems give exact cubic restrictions and conditional exponent restrictions. Feasible necessary data remain. | [Center obstruction](proofs/unresolved11_20261024/rank9_commutative/NO_CENTRAL_BOSON.md) · [Current report](proofs/unresolved11_retry_20261024/rank9/REPORT.md) · [Independent audit](proofs/unresolved11_retry_20261024/quartic/AUDIT_DISCRETE_CLIFFORD.md) |
| 10 | R10_1_189 is unitarily realized, completing multiplicity one. | [Categorical construction](proofs/unresolved11_retry_20261024/rank10/CONFORMAL_MODEL.md) · [Proof PDF](proofs/unresolved11_retry_20261024/rank10/rank10_conformal_model.pdf) · [Independent audit](proofs/unresolved11_retry_20261024/global/R189_INDEPENDENT_MODEL_AUDIT.md) |

The ordinary rank-six, rank-eight, rank-nine and rank-nine/ten manuscripts
integrate the current deductions. The [Atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/)
uses the common case directory and model catalogue for every rank.

## Exact decisions and replay

[Accepted transition](accepted.json) · [Current ranks-nine/ten ledger](rank9_rank10_m1_ledger.json)
· [CSV](rank9_rank10_m1_ledger.csv) · [Complete portable archive](replay.zip)

After extracting the archive, run:

```bash
python3 unresolved11_retry_20261024/verify_retry.py
```

The thirteen portable exact verifiers also pass with assertions disabled.
They supplement the categorical proofs; an arithmetic replay is not an
independent human verification of those proofs. The earlier research
directory is frozen history. Its former zero-resolution summary is
superseded by the current rank-ten construction.

For R1768 the twisted precursor is an actual complex category, without a
unitarity assertion. The image of the canonical near-group algebra is the
matrix algebra End(sigma), which does not supply the missing algebra
1+sigma. Its remaining associativity equations are explicit in two scalar
variables. This gap is stated in both the manuscript and the case profile.

For rank nine, exact rational witnesses certify feasibility only of the
stated necessary systems. They are not categories or associator solutions.
For the positive-TY R137 and negative-TY R1976 branches, exact separating
certificates and source relabellings force every projected third indicator
to be 1/2, hence 9 divides the FS exponent. Neither source ring is excluded.

The previous accepted ledgers and tensor sources are preserved. The sole
status change is reconciled coefficientwise and against the predecessor
ledger; the other results strengthen research records only.

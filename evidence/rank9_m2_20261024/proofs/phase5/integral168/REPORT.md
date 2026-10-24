# R9_2_1965: general exclusion

The new theoretical argument proves that `R9_2_1965` has no complex fusion categorification. Its earlier exclusion covered only group-theoretical categories. The complete proof is `GENERAL_EXCLUSION.md`; the exact finite-premise replay passes in `verify_general_exclusion.py`, producing `certificate.json`.

The argument has three new steps:

1. A central Tannakian lift of the nontrivial invertible would force an integral dimension-84 category. A two-by-two residual induction-Gram minor is strictly negative for every possible restriction vector, excluding that quotient.
2. Two scalar characters of formal codegree 56 force dimension-three central simples that mutually centralize, generating a nontrivial Tannakian subcategory.
3. The trivial universal grading and Step 1 force this Tannakian subcategory's group to be perfect. Its order divides 168, so it has order 168 and is Lagrangian. The hypothetical category is therefore group-theoretical, contradicting the complete phase-4 obstruction.

This proof uses pseudo-unitarity supplied by integrality; it does not assume unitarity. The group-theoretical dependency was already independently audited in phase 4. The new proof and verifier are ready for the root agent's independent audit. No phase-4 files, repositories, or online material have been modified.

Replay:

```sh
python rank9_m2_research/phase5/integral168/verify_general_exclusion.py
```

Result: `PASS: exact premises for the general exclusion of R9_2_1965`.

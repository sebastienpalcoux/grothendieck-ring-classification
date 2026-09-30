# Fermion and second-indicator constraints

The exact reduction removes 37 of the 1764 previously retained labelled
center profiles: 25 by fermion orbits and 12 by a mod-8 indicator congruence.
The remaining 1727 profiles are necessary data, not categorifications.

The proof is in the manuscript. From the package root:

```bash
python -O research/frontier/R6_8_1660/fermion_profiles/verify_fermion_profiles.py
```

The standard-library verifier reconstructs all profile tests and checks the
small adjacent certificate. It retains both possible actions on the low
odd pair; it uses no optimizer or floating-point arithmetic.

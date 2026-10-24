# Rank-nine multiplicity-two classification

**2,083 rings: 2,033 excluded over the complex numbers, 32 with unitary models, 18 unresolved.**

[Current ledger](ledger.json) · [CSV](ledger.csv) · [Models](models.json) · [Open cases](unresolved.json) · [Full proof and replay archive](replay.zip) · [Audit report](proofs/phase3/REPORT.md)

The archive is self-contained. Unzip it, install its requirements, and run:

```bash
python3 phase3/verify_audit.py
python3 phase3/verify_audit.py --fresh
```

Run those commands inside the extracted `Rank9_M2_Theoretical_Continuation_20261023` directory. **Only `phase3/results/` is the current accepted classification.** Older ledgers are retained as audit history and are superseded.

The audit removed 26 unsupported half-E6 subring claims. Seven formerly excluded rings have unitary models; three other exclusion conclusions have valid replacement proofs. Thirteen of the earlier 31 unresolved cases are settled: nine exclusions and four further unitary models. The Galois-unit restriction criterion unifies six new exclusions; the remaining new results have structural, Hopf-algebra or relative-cocycle proofs.

Current summaries and readable proofs are exposed here once. Complete source data, finite certificates, constructors and historical replay contexts live in the archive; its manifest binds every member. Computational replays and separate mathematical audits are not independent human verification or Lean formalization.

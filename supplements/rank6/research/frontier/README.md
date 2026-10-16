# Unresolved rank-six rings

**R6_4_155 and R6_8_1660 remain unresolved.** These necessary restrictions
establish neither categorification nor general nonexistence. All proofs and
data are AI-generated, not independently human-verified and not Lean-formalized.

| Ring | Current necessary restrictions |
|---|---|
| [R6_4_155](R6_4_155/CURRENT_STATUS.md) | Complete rank-26 modular candidate; a rank-22 based module passes 234,256 fermion Azumaya linking identities. |
| [R6_8_1660](R6_8_1660/CURRENT_STATUS.md) | A unique relative-center ring; graded induction gives 1,136 profiles; three possible Morita-dual rings; forced `nu_3(T)=2`. |

The [current manuscript](../../../../manuscripts/rank6/papers/manuscript.pdf)
gives the integrated arguments and precise hypotheses. The
[repository verification guide](../../../../docs/VERIFY.md) identifies the
complete computational campaign and each component replay. A based module,
modular datum or algebra support is not a categorical construction.

From the repository root:

```bash
python3 tools/verify_current_publication.py --historical
python3 -O tools/verify_current_publication.py --historical
```

The history option runs source-bound dependency checks with compatible input
snapshots. Individual subdirectories record the finite domain tested by their
own certificate; their intermediate profile counts are not the total current
frontier. Receipt audits check hashes and predicates, not mathematical proofs.
No timeout or unrefuted necessary branch establishes an exclusion.

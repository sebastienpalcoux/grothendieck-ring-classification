# Unresolved rank-six rings

> **AI-generated research · independent verification pending.** The proofs and
> data have not been independently human-verified or Lean-formalized.

**R6_4_155 and R6_8_1660 remain unresolved.** These necessary restrictions
establish neither categorification nor general nonexistence.

| Ring | Current necessary restrictions |
|---|---|
| [R6_4_155](R6_4_155/CURRENT_STATUS.md) | Complete rank-26 modular candidate; a rank-22 based module passes 234,256 fermion Azumaya linking identities. Odd cyclic Clifford constraints pass on 1,144 tested blocks. The all-order path divisibility condition for R′(m) holds exactly when m is even, including m=4. |
| [R6_8_1660](R6_8_1660/CURRENT_STATUS.md) | In the positive spherical representative, all indicators and central phase masses are determined. Eight spin objects form four dual pairs with restriction `2X+2gX+σ+3T`. Phase Gram constraints leave 640 labelled restriction-data profiles in branches 68, 286, 286; three Morita-dual rings remain possible. |

The [current manuscript](../../../../manuscripts/rank6/papers/manuscript.pdf)
gives the integrated arguments and precise hypotheses. The
[repository verification guide](../../../../docs/VERIFY.md) identifies the
complete computational campaign and each component replay. A based module,
modular datum or algebra support is not a categorical construction.

The [rank-six necessary-condition package](../../../../evidence/rigidity_20261017/rank6/README.md)
contains the Clifford, indicator and phase-mass arguments, exact data and
replay scope. The 640 surviving profiles are labelled restriction data, not
categories or complete modular fusion matrices.

From the repository root:

```bash
python3 tools/verify_current_publication.py --historical
python3 -O tools/verify_current_publication.py --historical
python3 evidence/rigidity_20261017/rank6/run_checks.py --repo .
python3 -O evidence/rigidity_20261017/rank6/run_checks.py --repo .
```

The history option runs source-bound dependency checks with compatible input
snapshots. Individual subdirectories record the finite domain tested by their
own certificate; their intermediate profile counts are not the total current
frontier. Receipt audits check hashes and predicates, not mathematical proofs.
No timeout or unrefuted necessary branch establishes an exclusion.

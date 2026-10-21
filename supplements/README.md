# Classification software and evidence

The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,506 general exclusions, 15 models and 6 unresolved cases. Every recorded model admits a unitary realization. The remaining rings retain unresolved status for general complex categorification.

The rank-seven multiplicity-five continuation addresses all 5,805 supplied exact-multiplicity-five rings: 5,804 general exclusions, 1 realization and 0 unresolved cases. The classification of the supplied census is complete through multiplicity 5. The new realization R7_5_5678 is Rep(AGL(1,7)).

> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.

Restore the source datasets with `python3 tools/restore_data.py` from the
repository root. Each rank's guide states its complete inputs, dependencies
and replay scope. A copy of `software/` alone is not a complete verification
package.

| Rank | Entry point | Classification scope |
|---:|---|---|
| 4 | [Guide](rank4/README.md) · [unrestricted replay](rank4/unrestricted/README.md) · [finite replay](rank4/PUBLIC_REPLAY.md) | Unrestricted: 15 models; theoretical bound and 1,692-input exact classification. Separate 889,530-input census through 128. |
| 5 | [Guide](rank5/README.md) · [complete public replay](../docs/VERIFY.md#complete-rank-four-and-rank-five-checks) | 40,999 inputs; 40,982 exclusions and 17 models through 20. |
| 6 | [Guide](rank6/README.md) · [combined full replay](../docs/VERIFY.md#complete-rank-six-route) | 25,421 inputs; 25,362 exclusions, 57 models and two open cases through 9. |
| 7 | [Guide](rank7/README.md) | Through multiplicity 5: 9,976 exclusions, 30 models and 0 unresolved; complete through 5. |
| 8 | [Guide](rank8/README.md) | Through multiplicity 3: 4,402 exclusions, 92 unitary models and 6 unresolved; complete through 2. |

The [historical 38-case continuation](../docs/RESEARCH_STATUS.md) records **36 decisions among 38 cases**: 29 proposed general exclusions and 7 unitary constructions. Within that historical 38-case study, two questions remain open: `R6_4_155` and `R6_8_1660`. The combined residual program records 140 decisions (120 exclusions and 20 constructions), all subject to independent mathematical verification.

Use the [verification guide](../docs/VERIFY.md) for full base loops and the
continuation chain. Their scopes are separate. The census and enumeration code
remain in [fusion-ring-census](https://github.com/sebastienpalcoux/fusion-ring-census).
Copied census code retains its license and notices. Authoritative classification
ledgers are identified in [provenance](../docs/PROVENANCE.md).

## Generalized Haagerup construction and further restrictions

R8_3_721 is realized by the inherited 1+rho Q-system Morita dual of the C2 de-equivariantization of the known GH(C8) category. Its rank and coefficient bound are proved exactly; identification uses its unique dimension type in the supplied complete rank-eight multiplicity-at-most-three census. The earlier center-action analysis reduces R8_3_1154 to three necessary center patterns. These model and pattern results are preserved in evidence/rank8_next_20261021/; the later R8_3_65 general exclusion is recorded separately in evidence/rank8_research_20261022/.

The integrated rank-eight article includes the new construction and restrictions. Categorical arguments, targeted mathematical replay receipts and independent reconstructions are in `evidence/rank8_next_20261021/`. The original frontier ledger, audit and completed replay receipts remain unchanged.

The following commands validate the accepted overlay metadata; they do not repeat the targeted mathematical checks:

```bash
python3 tools/rank8_next.py --check
python3 -O tools/rank8_next.py --check
```

A separately reviewed Galois follow-up reduces the 36 retained R8_3_1154 pair histograms to 25 across the same three center patterns. Its proof and exact replay are in `evidence/rank8_postpublication_20261021/r1154_galois_review/`; the ring remains unresolved.

## 22 October rank-eight research

R8_3_65 and R8_3_1795 have general-complex exclusions from pointed-induction Fourier integrality. Six exact separating certificates cover all four pointed associator classes for R8_3_65; sixteen cover both pointed classes and every admissible second-indicator assignment for R8_3_1795. The verified Galois reductions remove the pseudo-unitarity hypotheses. Every hypothetical categorification of each of the 6 remaining rank-eight rings admits a spherical structure and is Galois conjugate to a pseudo-unitary category. None is categorically Morita equivalent to a braided fusion category. For R8_3_1768 the pointed C2 associator must be nontrivial, forcing its nonidentity invertible to act freely on the simple objects of every indecomposable module category. R8_3_982 has a complete necessary based-module analysis; its remaining module data do not establish coherent module categories. A separate dimension-spectrum restriction for R8_3_3472 covers one specified rank-two module action only. These restrictions leave 6 general categorification questions unresolved.

The proof and exact verifier inventory is `evidence/rank8_research_20261022/README.md`. The current research stage has its own accepted ledger and source manifest; its exact replay is:

```bash
python3 tools/verify_rank8_research_20261022.py
python3 -O tools/verify_rank8_research_20261022.py
```

Run `python3 tools/rank8_research_20261022.py --check` for metadata reconciliation only. The original M3 replay and 108-check frontier receipts retain their historical scope. They do not replace the new targeted mathematical checks.

# Classification software and evidence

The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,506 general exclusions, 16 models and 5 unresolved cases. Every recorded model admits a unitary realization. The remaining rings retain unresolved status for general complex categorification.

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
| 8 | [Guide](rank8/README.md) | Through multiplicity 3: 4,402 exclusions, 93 unitary models and 5 unresolved; complete through 2. |

The [historical 38-case continuation](../docs/RESEARCH_STATUS.md) records **36 decisions among 38 cases**: 29 proposed general exclusions and 7 unitary constructions. Within that historical 38-case study, two questions remain open: `R6_4_155` and `R6_8_1660`. The combined residual program records 140 decisions (120 exclusions and 20 constructions), all subject to independent mathematical verification.

Use the [verification guide](../docs/VERIFY.md) for full base loops and the
continuation chain. Their scopes are separate. The census and enumeration code
remain in [fusion-ring-census](https://github.com/sebastienpalcoux/fusion-ring-census).
Copied census code retains its license and notices. Authoritative classification
ledgers are identified in [provenance](../docs/PROVENANCE.md).

## Generalized Haagerup construction and further restrictions

R8_3_721 is realized by the inherited 1+rho Q-system Morita dual of the C2 de-equivariantization of GH(C8). Exact rank and coefficient bounds identify its unique dimension type in the supplied complete rank-eight multiplicity-at-most-three census. The earlier center-action analysis leaves three necessary R8_3_1154 patterns. These results are in evidence/rank8_next_20261021/; the later R8_3_65 general exclusion is in evidence/rank8_research_20261022/.

The integrated rank-eight article includes the new construction and restrictions. Categorical arguments, targeted mathematical replay receipts and independent reconstructions are in `evidence/rank8_next_20261021/`. The original frontier ledger, audit and completed replay receipts remain unchanged.

The following commands validate the accepted overlay metadata; they do not repeat the targeted mathematical checks:

```bash
python3 tools/rank8_next.py --check
python3 -O tools/rank8_next.py --check
```

A separately reviewed Galois follow-up reduces the 36 retained R8_3_1154 pair histograms to 25 across the same three center patterns. Its proof and exact replay are in `evidence/rank8_postpublication_20261021/r1154_galois_review/`; the ring remains unresolved.

## E21 realization and further rank-eight research

R8_3_982 is unitarily realized by the neutral triality component of the exceptional E21 chiral fusion category from SU(3)_21 into E7_1. All 512 canonical fusion coefficients are identified exactly; the construction realizes both nonregular based-module types and the algebra 1+X5. Every Morita partner of any R982 categorification has the same based fusion ring. Five rank-eight general categorification questions remain: R8_3_928, R8_3_941, R8_3_1154, R8_3_1768 and R8_3_3472. Every hypothetical categorification admits a spherical structure and has a pseudo-unitary Galois conjugate; none has a braided Morita representative. New saturated-conductor and signed spectral-capacity theorems constrain all twist orders. R1768 has 39 of 40 necessary Gram/indicator branches excluded; its irrational dimension-ratio sector outside the two dimension-orbit objects has 18 or 72 simples. The final cone survives, and the 18-object option has a forced 19-dimensional Weil block with integral nonnegative distinguished products. R1154 has four forced semionic S columns and fusion matrices in all 25 histograms, which remain necessary data. R3472 has seven remaining first-action dual spectra and 400477 second-action arithmetic spectra, conditional on the specified rank-two modules. Exact integer phase counts eliminate six of the ten R928 center patterns, leaving four with exact necessary witnesses; all fourteen R941 allocations survive the stated phase refinements. Scoped construction obstructions and such witnesses neither exclude these five rings nor construct exotic categories.

Proofs, independent reconstructions and exact replay are indexed in `evidence/rank8_creative_20261022/README.md`. The new classification decision is the unitary E21 model for R8_3_982. The five other cases retain their explicit unresolved scope.

```bash
python3 tools/verify_rank8_creative_20261022.py
python3 -O tools/verify_rank8_creative_20261022.py
```

Use `--metadata-only` to validate published source bindings and replay receipts. Use `--historical` to replay the earlier rank-eight mathematical chain from its pinned immutable archive. The original publication documents and routers are retained there; current versions have new source bindings.

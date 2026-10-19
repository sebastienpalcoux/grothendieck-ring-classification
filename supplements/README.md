# Classification software and evidence

The 19 October rank-seven extension addresses all 5,805 exact-multiplicity-five rings: 5,789 general exclusions, 1 realization and 15 unresolved cases. The classification is complete through multiplicity 4. The new realization R7_5_5678 is Rep(AGL(1,7)). The unresolved records remain open for general complex categorification.

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
| 7 | [Guide](rank7/README.md) | Through multiplicity 5: 9,961 exclusions, 30 models and 15 unresolved; complete through 4. |
| 8 | [Guide](rank8/README.md) | Complete through 2: 896 exclusions and 77 models. |

The [historical 38-case continuation](../docs/RESEARCH_STATUS.md) records **36 decisions among 38 cases**: 29 proposed general exclusions and 7 unitary constructions. Within that historical 38-case study, two questions remain open: `R6_4_155` and `R6_8_1660`. The combined residual program records 140 decisions (120 exclusions and 20 constructions), all subject to independent mathematical verification.

Use the [verification guide](../docs/VERIFY.md) for full base loops and the
continuation chain. Their scopes are separate. The census and enumeration code
remain in [fusion-ring-census](https://github.com/sebastienpalcoux/fusion-ring-census).
Copied census code retains its license and notices. Authoritative classification
ledgers are identified in [provenance](../docs/PROVENANCE.md).

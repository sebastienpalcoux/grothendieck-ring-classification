# E21 realization and further rank-eight research

**R8_3_982 is unitarily realized.** Its fusion ring is the triality-zero
component of the exceptional E21 chiral fusion category associated with
the conformal embedding SU(3)_21 into E7_1. Reconstruction from the published
24-vertex graph identifies all 512 canonical coefficients, with a separate
exact reconstruction and categorical-existence audit.

The exact-multiplicity-three census now has **3,506 general exclusions,
16 unitary models and five unresolved rings**. Through multiplicity three
the totals are **4,402 / 93 / 5**. The five unresolved cases are R8_3_928,
R8_3_941, R8_3_1154, R8_3_1768 and R8_3_3472.

The new model changes exactly one classification record. All 4,499 other
records and all 92 inherited models are preserved. The
[acceptance manifest](accepted.json) binds the exact new decision,
case-specific research records and mathematical inputs. The
[per-ring audit](per_ring_research_audit.json) retains the earlier research
history and records the scope and limitations of each new result.

## Results

| Case or method | Verified conclusion | Remaining limitation |
|---|---|---|
| [E21 model for R982](r982/E21_MODEL.md) | A known unitary category has exactly the canonical tensor; both nonregular based-module types and 1+X5 are realized. | Categorifications and module associator choices are not classified. |
| [R982 Morita rigidity](r982/MORITA_RING.md) | Every Morita partner has the same based fusion ring, without a rank or multiplicity cutoff. | Different categories with these same fusion rules remain possible. |
| [Saturated conductor](unified/SATURATED_CONDUCTOR.md) | Equality in the dimension-character bound forces a conductor quotient of the cyclic modular representation. | A necessary condition, not a construction. |
| [Signed prime](unified/SIGNED_PRIME_SUPPORT.md) and [composite capacities](unified/COMPOSITE_SIGNED_SUPPORT.md) | Exact twist support and individual spectral masses at all orders. | Finite controls supplement the general proofs; they do not replace them. |
| [R928 integer phase refinement](r928_r941/integer_followup/PROOF.md) | Exact branching certificates eliminate six of ten center patterns; patterns 40, 49, 186 and 191 have exact integer-phase witnesses. | Four necessary patterns survive; their witnesses do not construct a center or associator. |
| [R941 phase and product constraints](r928_r941/PROOF.md) | All fourteen complete allocations retain exact necessary witnesses under stronger phase capacities, with 55 forced integral pair products per allocation. | Distinguished pair products do not give complete modular data. |
| [R1154 packet](r1154/PROOF.md) | Four full S columns and fusion matrices are forced in all 25 histograms; the packet generates the entire center. | All three global patterns survive. |
| [R1154 parent obstruction](r1154/QUANTUM_SUBGROUP_ROUTE.md) | A positive field-coordinate criterion excludes the direct index-five SU(3)_7 times Fibonacci construction. | Other constructions remain open. |
| [R1768 Galois restrictions](r1768/GALOIS_FIBRES.md) | Exactly 39 of 40 Gram/indicator branches are excluded; the dimension-orbit column is unique. | The last necessary cone is exactly feasible. |
| [R1768 Weil block](unified/R1768_WEIL_BLOCK.md) | The 18-object irrational-ratio option has a forced 19-dimensional modular block and integral nonnegative distinguished products. | Neither modular completion nor categorification is proved. |
| [R3472 dual restrictions](r3472/PROOF.md) | A new Galois Gram bound and exact product equations leave seven first-action spectra and 400,477 second-action arithmetic spectra. | Both actions are conditional on rank-two module categories; arithmetic spectra are not completed fusion rings. |
| [Cyclic parent obstruction](r3472/CONSTRUCTION_ROUTES.md) | A cyclic NG(C_n,n) parent de-equivariantized by order h requires h² to divide n. | Noncyclic parents and arbitrary Morita routes are not excluded. |

For R1768 the count of 18 or 72 refers precisely to the **irrational
dim(Z)/D sector outside 1 and A_sigma**. Rational-ratio objects may also
have primitive-37 twists and remain in the complete necessary domain.
All six noninvertible second indicators are forced to +1 in a
pseudo-unitary Galois form. The original categorification need not itself
be pseudo-unitary or unitary.

The remaining five rings have received extensive known and newly developed
exclusion and construction tests. They remain extensively investigated
exotic candidates in the stated research sense: their categorifiability
and novelty are not proved. Every hypothetical categorification admits a
spherical structure and has a pseudo-unitary Galois conjugate. The previous
general braiding and braided-Morita obstructions remain valid.

## Reproduce

From the repository root, or an extracted current scientific package:

```bash
python3 tools/verify_rank8_creative_20261022.py
python3 -O tools/verify_rank8_creative_20261022.py
```

These commands replay the 19 accepted mathematical checks. Mathematical
children retain assertions, including assertions in historical imports.
`--metadata-only` checks the complete source inventory and both published
replay receipts. `--historical` also replays the earlier rank-eight chain
from its pinned scientific archive. The archive retains the old publication
routers byte for byte; the current routers have separate new source bindings.
No earlier proof input, receipt or classification ledger is overwritten.

For the model alone:

```bash
python3 evidence/rank8_creative_20261022/r982/e21_model.py
python3 evidence/rank8_creative_20261022/unified/audits/verify_e21_independent.py
```

The optional `--pdf` argument of the second verifier checks all sixty
vector edges against Figure 43, printed page 37, of
[Coquereaux–Isasi–Schieber, arXiv:1007.0721v2](https://arxiv.org/abs/1007.0721).
The source PDF identity is recorded in the graph receipt. Categorical
existence follows from the actual local conformal inclusion and chiral
endomorphism category, not merely from a formal graph algebra; see
[the categorical bridge](r928_r941/E21_CATEGORICAL_BRIDGE.md) and
[the independent audit](unified/E21_MODEL_AUDIT.md).

Separate-agent audits and exact arithmetic checks are included. They are
not formal proof-assistant verification or independent human refereeing.

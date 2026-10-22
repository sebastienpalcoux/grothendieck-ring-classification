# Rank-8 Grothendieck rings through multiplicity 3

For the current checkout, replay `python3 tools/verify_rank8_creative_20261022.py`; add `--historical` to replay earlier rank-eight stages in their preserved contexts. Earlier-stage commands below apply inside their corresponding immutable archives.

The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,506 general exclusions, 16 models and 5 unresolved cases. Every recorded model admits a unitary realization. The remaining rings retain unresolved status for general complex categorification.

The rank-seven multiplicity-five continuation addresses all 5,805 supplied exact-multiplicity-five rings: 5,804 general exclusions, 1 realization and 0 unresolved cases. The classification of the supplied census is complete through multiplicity 5. The new realization R7_5_5678 is Rep(AGL(1,7)).

> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.

The authoritative decision ledger is `output/creative_20261022/ledger.json`, restored by `python3 tools/restore_data.py`. Classification is complete through multiplicity 2. Multiplicity 3 has unresolved classification records.

| Exact multiplicity | Rings | General exclusions | Unitary models | Open |
|---:|---:|---:|---:|---:|
| 1 | 96 | 48 | 48 | 0 |
| 2 | 877 | 848 | 29 | 0 |
| 3 | 3,527 | 3,506 | 16 | 5 |
| **Total** | **4,500** | **4,402** | **93** | **5** |

[Manuscript source](../../manuscripts/rank8/paper/rank8.tex) · [PDF](../../manuscripts/rank8/paper/rank8.pdf) · [Research status](../../docs/RESEARCH_STATUS.md)

From the repository root:

```bash
python3 tools/restore_data.py
python3 tools/verify_current_publication.py --historical
python3 -O tools/verify_current_publication.py --historical
```

The history option checks source-bound dependencies in isolated compatible
snapshots. These continuation checks do not replace the complete base-certificate
loops in the [full replay guide](../../evidence/prepublication_20261017/FULL_REPLAY.md).
Use normal Python for assertion-based checkers. Positive counts in an incomplete
band are lower bounds; a timeout or surviving necessary system proves no exclusion.
See [verification scope](../../docs/PREPUBLICATION_REVIEW.md).

## Multiplicity-three continuation

Run the original M3 source-bound replay with Python 3.12 and a C++17 compiler:

```bash
python3 -m pip install -r supplements/rank7/requirements-m5.txt
python3 supplements/rank8/software/verify_m3_continuation.py --output frontier-validation/baseline_normal.json
python3 -O supplements/rank8/software/verify_m3_continuation.py --output frontier-validation/baseline_optimized.json
```

Both full receipts bind the baseline decisions and explicit models to the preserved source files and proof implementation. `--metadata-only` checks those bindings without replaying mathematics. The M3 archive preserves the repository-relative dependency tree. Historical rank-eight data and decisions remain immutable; they are separate inputs to this continuation. Scoped unitary obstructions and unsuccessful searches do not establish general nonexistence.

## Further rank-eight frontier investigation

The historical frontier stage recorded 25 further general exclusions among the original 34 unresolved M3 cases. Subsequent construction and research stages leave 5 current questions. The original M3 ledger, proof inputs and full receipts are unchanged. The current ledger is `supplements/rank8/output/creative_20261022/ledger.json`.

Canonical normal and optimized frontier replays each passed all 108 checks. These receipts cover the historical frontier stage. Fresh replay after extraction from the publication archive is deferred.

Replay the original M3 package using the isolated outputs above, preserving its frozen receipts, then replay the continuation separately:

```bash
python3 tools/verify_rank8_frontier.py
python3 -O tools/verify_rank8_frontier.py
```

The new receipts bind accepted decisions and exact computations. The source-bound per-ring research inventory is `evidence/rank8_creative_20261022/per_ring_research_audit.json`. Construction-family exclusions and feasible necessary-condition witnesses have explicit scopes; neither establishes an exotic category.

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

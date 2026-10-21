# Rank-8 Grothendieck rings through multiplicity 3

The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,506 general exclusions, 15 models and 6 unresolved cases. Every recorded model admits a unitary realization. The remaining rings retain unresolved status for general complex categorification.

The rank-seven multiplicity-five continuation addresses all 5,805 supplied exact-multiplicity-five rings: 5,804 general exclusions, 1 realization and 0 unresolved cases. The classification of the supplied census is complete through multiplicity 5. The new realization R7_5_5678 is Rep(AGL(1,7)).

> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.

The authoritative decision ledger is `output/research_20261022/ledger.json`, restored by `python3 tools/restore_data.py`. Classification is complete through multiplicity 2. Multiplicity 3 has unresolved classification records.

| Exact multiplicity | Rings | General exclusions | Unitary models | Open |
|---:|---:|---:|---:|---:|
| 1 | 96 | 48 | 48 | 0 |
| 2 | 877 | 848 | 29 | 0 |
| 3 | 3,527 | 3,506 | 15 | 6 |
| **Total** | **4,500** | **4,402** | **92** | **6** |

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

The historical frontier stage recorded 25 further general exclusions among the original 34 unresolved M3 cases. Subsequent construction and research stages leave 6 current questions. The original M3 ledger, proof inputs and full receipts are unchanged. The current ledger is `supplements/rank8/output/research_20261022/ledger.json`.

Canonical normal and optimized frontier replays each passed all 108 checks. These receipts cover the historical frontier stage. Fresh replay after extraction from the publication archive is deferred.

Replay the original M3 package using the isolated outputs above, preserving its frozen receipts, then replay the continuation separately:

```bash
python3 tools/verify_rank8_frontier.py
python3 -O tools/verify_rank8_frontier.py
```

The new receipts bind accepted decisions and exact computations. The source-bound per-ring research inventory is `evidence/rank8_research_20261022/per_ring_research_audit.json`. Construction-family exclusions and feasible necessary-condition witnesses have explicit scopes; neither establishes an exotic category.

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

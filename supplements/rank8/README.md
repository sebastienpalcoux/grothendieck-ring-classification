# Rank-8 Grothendieck rings through multiplicity 3

The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,504 general exclusions, 14 models and 9 unresolved cases. Every recorded model admits a unitary realization. The remaining rings retain unresolved status for general complex categorification.

The rank-seven multiplicity-five continuation addresses all 5,805 supplied exact-multiplicity-five rings: 5,804 general exclusions, 1 realization and 0 unresolved cases. The classification of the supplied census is complete through multiplicity 5. The new realization R7_5_5678 is Rep(AGL(1,7)).

> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.

The authoritative decision ledger is `output/frontier_20261021/ledger.json`, restored by `python3 tools/restore_data.py`. Classification is complete through multiplicity 2. Multiplicity 3 has unresolved classification records.

| Exact multiplicity | Rings | General exclusions | Unitary models | Open |
|---:|---:|---:|---:|---:|
| 1 | 96 | 48 | 48 | 0 |
| 2 | 877 | 848 | 29 | 0 |
| 3 | 3,527 | 3,504 | 14 | 9 |
| **Total** | **4,500** | **4,400** | **91** | **9** |

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

The original 34 unresolved M3 cases now have 25 further general exclusions and 9 remaining questions. The original M3 ledger, proof inputs and full receipts are unchanged. The current ledger is `supplements/rank8/output/frontier_20261021/ledger.json`.

Canonical normal and optimized frontier replays each passed all 108 checks. Fresh replay after extraction from the publication archive is deferred.

Replay the original M3 package using the isolated outputs above, preserving its frozen receipts, then replay the continuation separately:

```bash
python3 tools/verify_rank8_frontier.py
python3 -O tools/verify_rank8_frontier.py
```

The new receipts bind accepted decisions and exact computations. The source-bound per-ring research inventory is `evidence/rank8_frontier_20261021/structural_models/per_ring_research_audit.json`. Construction-family exclusions and feasible necessary-condition witnesses have explicit scopes; neither establishes an exotic category.

## Further center-pattern constraints

A separately verified fourth-moment and center-action refinement excludes 2 of the four necessary center patterns for R8_3_721, leaving 2. For R8_3_1154, exact coordinate norm and interval bounds exclude 946 of 1,238 patterns, leaving 292. The surviving action matrices and patterns are necessary data only; no complete center fusion ring, associator or categorical model is constructed. Both source rings remain unresolved.

The integrated rank-eight article includes this separately verified addendum. Its proofs, complete pattern indices, necessary action matrices and independent reconstructions are in `evidence/rank8_center_followup_20261021/`. The original frontier ledger and audit remain unchanged.

The separate center-pattern addendum passed all eight checks in canonical normal and optimized Python, including independent arithmetic reconstructions and positive controls. Fresh replay after extraction from the publication archive is deferred.

```bash
python3 evidence/rank8_center_followup_20261021/verify.py --root .
python3 -O evidence/rank8_center_followup_20261021/verify.py --root .
```

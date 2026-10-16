# Rank-7 Grothendieck rings through multiplicity 4

> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.

The authoritative decision ledger is [`output/rank7_ledger.json`](output/rank7_ledger.json). Classification is complete through multiplicity 4.

| Exact multiplicity | Rings | General exclusions | Unitary models | Open |
|---:|---:|---:|---:|---:|
| 1 | 43 | 30 | 13 | 0 |
| 2 | 319 | 309 | 10 | 0 |
| 3 | 1,059 | 1,057 | 2 | 0 |
| 4 | 2,780 | 2,776 | 4 | 0 |
| **Total** | **4,201** | **4,172** | **29** | **0** |

[Manuscript source](../../manuscripts/rank7/papers/manuscript.tex) · [PDF](../../manuscripts/rank7/papers/manuscript.pdf) · [Research status](../../docs/RESEARCH_STATUS.md)

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

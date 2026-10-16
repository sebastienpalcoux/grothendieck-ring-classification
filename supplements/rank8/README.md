# Rank-8 Grothendieck rings through multiplicity 2

> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.

The authoritative decision ledger is [`data/decisions.json`](data/decisions.json). Classification is complete through multiplicity 1. Multiplicity 2 is partial; `R8_2_24` remains open.

| Exact multiplicity | Rings | General exclusions | Unitary models | Open |
|---:|---:|---:|---:|---:|
| 1 | 96 | 48 | 48 | 0 |
| 2 | 877 | 847 | 29 | 1 |
| **Total** | **973** | **895** | **77** | **1** |

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

# Rank-7 Grothendieck rings through multiplicity 4

The complete source census is pinned at `b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726`. Current categorification decisions are in `output/rank7_ledger.json`.

| Exact multiplicity | Fusion rings | Generally excluded | Unitarily realized | Generally unresolved |
|---:|---:|---:|---:|---:|
| 1 | 43 | 30 | 13 | 0 |
| 2 | 319 | 309 | 10 | 0 |
| 3 | 1,059 | 1,054 | 2 | 3 |
| 4 | 2,780 | 2,771 | 2 | 7 |
| Total | 4,201 | 4,164 | 27 | 10 |

The [16 October theoretical update](../../evidence/theoretical_20261016/README.md) records the new general exclusions, exact source applications, and the complete remaining-case register. Positive counts in incomplete bands are lower bounds. Scoped pivotal or spherical obstructions do not decide arbitrary complex categorifiability.

Current manuscript: [source](../../manuscripts/rank7/papers/manuscript.tex) and [PDF](../../manuscripts/rank7/papers/manuscript.pdf). The older archive and its paper copies retain the October 2 historical snapshot; use the dated theoretical update together with that archive, or the current repository, for the new results.

From the repository root:

```bash
python3 tools/verify_theoretical_20261016.py
python3 -O tools/verify_theoretical_20261016.py --historical
```

The second command restores historical ledgers in a temporary copy before replaying the frozen parent proofs. No timeout or unrefuted necessary-condition branch is an exclusion. See [verification instructions](../../docs/VERIFY.md).

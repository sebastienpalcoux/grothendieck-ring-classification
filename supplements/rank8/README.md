# Rank-8 Grothendieck rings through multiplicity 2

The complete source census is pinned at `b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726`. Current categorification decisions are in `data/decisions.json`.

| Exact multiplicity | Fusion rings | Generally excluded | Unitarily realized | Generally unresolved |
|---:|---:|---:|---:|---:|
| 1 | 96 | 45 | 48 | 3 |
| 2 | 877 | 830 | 24 | 23 |
| Total | 973 | 875 | 72 | 26 |

The [16 October theoretical update](../../evidence/theoretical_20261016/README.md) records the new general exclusions, exact source applications, and the complete remaining-case register. Positive counts in incomplete bands are lower bounds. Scoped pivotal or spherical obstructions do not decide arbitrary complex categorifiability.

Current manuscript: [source](../../manuscripts/rank8/paper/rank8.tex) and [PDF](../../manuscripts/rank8/paper/rank8.pdf). The older archive and its paper copies retain the October 2 historical snapshot; use the dated theoretical update together with that archive, or the current repository, for the new results.

From the repository root:

```bash
python3 tools/verify_theoretical_20261016.py
python3 -O tools/verify_theoretical_20261016.py --historical
```

The second command restores historical ledgers in a temporary copy before replaying the frozen parent proofs. No timeout or unrefuted necessary-condition branch is an exclusion. See [verification instructions](../../docs/VERIFY.md).

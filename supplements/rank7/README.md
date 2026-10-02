# Rank-seven Grothendieck rings through multiplicity four

The complete fusion-ring census is pinned at commit `b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726` of [fusion-ring-census](https://github.com/sebastienpalcoux/fusion-ring-census). The included `data/rank7_tables.txt.gz` has SHA-256 `6ddea4c66de7fbe077e9552e71e8cf95ec3fec5bbd30a615e68e2d8fcb9ae9c9`.

| Exact multiplicity | Fusion rings | Generally excluded | Unitarily realized | Generally unresolved |
|---:|---:|---:|---:|---:|
| 1 | 43 | 30 | 13 | 0 |
| 2 | 319 | 301 | 10 | 8 |
| 3 | 1059 | 1045 | 2 | 12 |
| 4 | 2780 | 2756 | 2 | 22 |
| Total | 4201 | 4132 | 27 | 42 |

Multiplicity one is complete. The later realization counts are certified lower bounds, and the 42 unresolved rings are general complex categorification questions. Multiplicities at least five lie outside this census bound.

Read the [manuscript source](papers/manuscript.tex) and [PDF](papers/manuscript.pdf). The authoritative files are `output/rank7_ledger.json`, `output/rank7_model_catalog.json` and `output/rank7_summary.json`. Every positive row has an actual unitary category and a complete 343-coefficient tensor comparison. Every general exclusion has a necessary theorem or a complete source-bound certificate.

The [latest residual stage](../../evidence/upper_residual_20261002b/README.md) adds sixteen general exclusions and the unitary modular D12 model. Prime descent reduces integral cases to finite pointed-module, orbit and Brauer–Picard obstructions. Four further complete signed-sphericalization certificates apply without a pivotality assumption. The separate pivotal exclusions at R7_4_1212, R7_4_1213, R7_4_1417 and R7_4_1420 leave general status unresolved.

From the repository root, replay the latest source-bound stage in both modes:

```bash
python3 tools/verify_upper_residual_20261002b.py
python3 -O tools/verify_upper_residual_20261002b.py
```

The earlier [residual](../../evidence/residual_20261002/README.md) and [AnyonWiki](../../evidence/anyonwiki/README.md) proofs retain their own exact verification reports. Full-tensor matches support general complex existence; an AnyonWiki flag alone is never used for a general exclusion.

The original census analysis and full certificate programs are retained for provenance. Discovery and release replay are distinct: later verified stages are preserved and replayed by the release pipeline. A timeout or an unrefuted signed branch gives no negative decision. See the repository [verification guide](../../docs/VERIFY.md) for current release commands.

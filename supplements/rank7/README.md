# Rank-seven Grothendieck-ring status through multiplicity four

This package separates a complete **fusion-ring census** from **proved categorification decisions**. The rank-seven census is pinned at commit `b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726` of [fusion-ring-census](https://github.com/sebastienpalcoux/fusion-ring-census); `data/rank7_tables.txt.gz` has SHA-256 `6ddea4c66de7fbe077e9552e71e8cf95ec3fec5bbd30a615e68e2d8fcb9ae9c9`. The census has respectively 43, 319, 1059, and 2780 rings of exact multiplicities 1 through 4.

The authorless manuscript in [`papers/manuscript.tex`](papers/manuscript.tex) and [`papers/manuscript.pdf`](papers/manuscript.pdf) states the **certified partial** classification. Multiplicity one is now complete: thirteen of its 43 rings have models and thirty are generally excluded. The higher bands remain partial. Multiplicities at least five lie beyond the pinned rank-seven source.

| Exact multiplicity | Fusion rings | Certified exclusions | Categorical models | Undecided |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 43 | 30 | 13 | 0 |
| 2 | 319 | 291 | 5 | 23 |
| 3 | 1059 | 1035 | 1 | 23 |
| 4 | 2780 | 2751 | 0 | 29 |

The first multiplicity needing the new exhaustive signed criterion is one.
Multiplicity one is complete; multiplicities two through four have 75 unresolved rings.

## Repeat all decisions

The source is included locally, so the checks require no web access. With Python 3, SymPy, and a C++17 compiler:

```shell
python analyze.py --max-m 4 --dnumber
python verify.py
python -O verify.py
python papers/generate_tables.py
python build_release.py
```

The analyzer derives all asserted positive model tensors from explicit constructions and pinned published full tensors, searches all unit-preserving basis permutations for an exact full-tensor match, and records each resulting permutation. It computes or replays a staged negative certificate for each excluded ring. The verifier re-reads the pinned census, repeats every tensor match, regenerates each inexpensive negative certificate from the tensor, reconstructs every exhaustive oriented signed-table search, and compares all status and stage totals. It raises on a discrepancy; `-O` checks that optional Python assertions are not the verification gate. `generate_tables.py` writes only tables from the verified machine-readable summary.

### Files and status vocabulary

| Path | Contents |
| --- | --- |
| `data/rank7_tables.txt.gz` | Complete pinned rank-seven source tensors, one ring per line |
| `data/lower_rank_positive_models.json` | Exact rank-four and rank-five classified model tensor registry |
| `data/integral_rank7_noncomm_published.txt` | Published, full noncommutative integral rank-seven fusion tensors from Alekseyev–Bruns–Dong–Palcoux's accepted paper; source blob `7bd5803c733d893dbd5978a9856ad8962b86ffb6` |
| `data/oriented_verified_certificates.json` | 246 complete general oriented proof trees; the analyzer and verifier replay each one against the source tensor |
| `output/rank7_ledger.json` | One record per census ring, preserving ID, tensor, source line, criterion, status and optional proof tree |
| `output/rank7_model_catalog.json` | Full tensors, exact model-to-census permutations, constructions and references |
| `output/rank7_summary.json` | Sequential exclusion counts and resulting status counts per multiplicity |
| `output/rank7_verification_report.json` | Earlier ordinary and optimized negative replays, plus the independently checked positive update and SHA-256 provenance |
| `analyze.py`, `verify.py`, `software/` | Discovery, independent replay, mathematical certificate checkers |
| `release/rank7-certified-through-m4.zip` | Reproducible research bundle with checksum manifest and authorless PDF |

The only valid record statuses are `excluded`, `unitarily_realized` and `unresolved`. **Unresolved is not a realized Grothendieck ring.** Every negative criterion is necessary for *any* complex fusion category, including categories with no initially specified pivotal structure. A bounded search without a complete proof is recorded only as unresolved. A stage count charges a ring to its first successful certificate, keeping each exclusion process transparent.

The longer signed-sphericalization criterion generalizes the rank-six method. In each positive result of this criterion, the checker re-enumerates the *entire* integer domain of normalized oriented signed quotient structure constants, all associative tables, and all negative branch witnesses. Screening budgets were used only to choose which candidates to explore; they cannot create an exclusion.

The source files for other ranks and the categorification literature remain cited in the manuscript. The Alekseyev–Bruns–Dong–Palcoux integral-rings paper is marked as accepted in *Letters in Mathematical Physics* as supplied with the project.

The 2026-10-01 positive update is documented in [`../../evidence/anyonwiki/README.md`](../../evidence/anyonwiki/README.md). Run `python tools/verify_anyonwiki_import.py` from the repository root to replay the exact added witnesses and verify preservation of every previous exclusion. The earlier full-certificate report is retained separately; this update does not rerun its costly unchanged searches.

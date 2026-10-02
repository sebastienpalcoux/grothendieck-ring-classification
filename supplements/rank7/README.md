# Rank-seven Grothendieck-ring status through multiplicity four

This package separates a complete **fusion-ring census** from **proved categorification decisions**. The rank-seven census is pinned at commit `b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726` of [fusion-ring-census](https://github.com/sebastienpalcoux/fusion-ring-census); `data/rank7_tables.txt.gz` has SHA-256 `6ddea4c66de7fbe077e9552e71e8cf95ec3fec5bbd30a615e68e2d8fcb9ae9c9`. The census has respectively 43, 319, 1059, and 2780 rings of exact multiplicities 1 through 4.

The authorless manuscript in [`papers/manuscript.tex`](papers/manuscript.tex) and [`papers/manuscript.pdf`](papers/manuscript.pdf) states the **certified partial** classification. Multiplicity one is now complete: thirteen of its 43 rings have models and thirty are generally excluded. The higher bands remain partial. Multiplicities at least five lie beyond the pinned rank-seven source.

| Exact multiplicity | Fusion rings | Certified exclusions | Categorical models | Undecided |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 43 | 30 | 13 | 0 |
| 2 | 319 | 295 | 9 | 15 |
| 3 | 1059 | 1039 | 2 | 18 |
| 4 | 2780 | 2752 | 2 | 26 |

The first multiplicity needing the new exhaustive signed criterion is one.
Multiplicity one is complete; multiplicities two through four have 59 unresolved rings. The full census has 4116 excluded rings and 26 rings with unitary models.

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

The 2026-10-02 update adds seven unitary models and nine general exclusions. Three models are standard-category identifications. Two more realize `R7_2_1` and `R7_2_195` by coherent `C2` equivariantizations built from `TY(C3)`; the latter uses an explicit unitary `C4` cocycle and tensorator. The proofs appear in the manuscript and [`papers/ty_equivariant_models.md`](papers/ty_equivariant_models.md). A third equivariantization, `Vec(Q8)^S3` for the signed permutation action on quaternion axes, realizes `R7_4_2`. The twisted quaternion group-theoretical category specified by a global Chern class realizes `R7_4_2019`; its construction is proved in [`papers/r7_4_2019_chern_proof.md`](papers/r7_4_2019_chern_proof.md). Portable replay checks the actions, coherence, characteristic-class restriction, equivariant fusion multiplicities, and all 1372 structure constants of these four models.

The two local TPE certificates use the published inconsistent system of arXiv:2203.06522v5, Theorem 7.2, including its identical local subsystem for the dimension-210 variation. Two dimension-40 cases violate a unitary support inequality while solvability forces every categorification to be unitarizable. A half-partition argument forces weak group-theoreticity in the dimension-140 case and contradicts the Frobenius property; an odd pointed group and center dimensions similarly upgrade the dimension-120 case. Finally, solvability forces two successive equivariantizations for `R7_2_75`; their combined `V4` action has an impossible simple-object dimension type. This excludes every complex categorification, as proved in [`papers/r7_2_75_proof.md`](papers/r7_2_75_proof.md). Two dimension-96 rings, `R7_2_252` and `R7_2_315`, are excluded by a forced `S3` action on a group of order sixteen: the required orbit pattern would make an involution fix exactly two elements, while a theoretical group argument forces at least four. The proof is [`papers/D96_GENERAL_EXCLUSION_PROOF.md`](papers/D96_GENERAL_EXCLUSION_PROOF.md). The verifier checks exact theorem hypotheses; it does not independently repeat the source paper's Groebner calculation. Run `python software/verify_residual_20261002.py` (or `python -O software/verify_residual_20261002.py`) to replay all sixteen changes and verify preservation of every unaffected record and the previous 4107 exclusions.

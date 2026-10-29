# Grothendieck ring classification

<!-- current-frontier -->
**Current classification · 29 October 2026.** R8_3_1768 is excluded over the complex numbers by pivotal conjugation parity, using the established existence and center-domain reductions. **Six cases remain unresolved:** two at rank six, three at rank eight and one at rank nine. No additional model is claimed. [Current proofs and exact checks](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/frontier/README.md).
<!-- /current-frontier -->

**Which low-rank fusion rings admit fusion categories over ℂ?**

[**Explore the atlas →**](https://sebastienpalcoux.github.io/grothendieck-ring-classification/) · [Theory and definitions](https://sebastienpalcoux.github.io/grothendieck-ring-classification/theory.html) · [Manuscripts](manuscripts/README.md) · [Open cases](https://sebastienpalcoux.github.io/grothendieck-ring-classification/unresolved.html) · [Verification](docs/VERIFY.md)

> **AI-generated research · independent verification pending.**
> Results and computations remain provisional. [Research status and verification scope](docs/PREPUBLICATION_REVIEW.md).

<a id="classification--what-is-decided"></a>

**26 October 2026 · rank twelve, multiplicity one.** All 632 supplied rings are decided: **480 excluded and 152 modeled**. Exactly **151 models are known unitary**; R12_1_623 has a complex/pseudo-unitary model with unitarity unproved. [Manuscript](publications/rank12/README.md) · [Proofs, ledger and replay](evidence/rank12_m1_20261026/README.md) · [All-rank count summary](data/classification_summary_all_ranks.csv).

## Classification at a glance

Ranks **2–4 have unrestricted classification claims**, with exactly **15 rank-four rings**.
Higher ranks have the explicit multiplicity bounds below.

| Rank | Full census | General classification | Current conclusion |
|---:|---:|---:|---|
| 2 | Symbolic, all multiplicities | **Unrestricted theorem** | Exactly the rings `n = 0, 1` are realized. |
| 3 | Through 1,000 | **Unrestricted theorem** | Five realized rings: four at multiplicity 1 and one at 2; see the standalone sphericality and ring-classification proof. |
| 4 | Through 128 | **Unrestricted theorem** | Exactly 15 realized rings; every categorification is spherical; multiplicity at most 6. |
| 5 | Through 20 | **Complete through 20** | Through 20: 40,982 excluded, 17 realized, 0 unresolved. |
| 6 | Through 9 | **Complete through 3** | Through 9: 25,362 excluded, 57 realized, 2 unresolved. |
| 7 | Through 5 | **Complete through 5** | Through 5: 9,976 excluded, 30 realized, 0 unresolved. |
| 8 | Through 3 | **Complete through 2**; multiplicity 3 partial | Through 3: 4,404 excluded, 93 realized, 3 unresolved. |
| 9 | Through 2 | **Complete through 1**; multiplicity 2 partial | Through 2: 2,148 excluded, 76 realized, [1 unresolved](https://sebastienpalcoux.github.io/grothendieck-ring-classification/unresolved.html?rank=9&m=2). |
| 10 | Multiplicity 1 | **Complete at multiplicity 1** | 136 excluded, 58 realized, 0 unresolved. |
| 11 | Multiplicity 1 | **Complete at multiplicity 1** | 155 excluded, 27 realized, 0 unresolved. |
| 12 | Through 1 | **Complete through 1** | 632 rings: 480 general exclusions, 152 modeled, none unresolved. 151 models are unitary; R12_1_623 is complex/pseudo-unitary, with unitarity unproved. |

**6 open cases.** General categorification remains undecided for these rings.
[Explore their status, invariants and research records](https://sebastienpalcoux.github.io/grothendieck-ring-classification/unresolved.html).

<details id="grothendieck-rings--known-realizations-at-each-exact-multiplicity">
<summary><strong>Known realizations at each exact multiplicity</strong></summary>

Multiplicity is the largest fusion coefficient. `≥` marks a lower bound where
general categorification remains open; a dash marks an unanalyzed band.

| Multiplicity | Rank 2 | Rank 3 | Rank 4 | Rank 5 | Rank 6 | Rank 7 | Rank 8 | Rank 9 | Rank 10 | Rank 11 | Rank 12 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 2 | 4 | 9 | 10 | 21 | 13 | 48 | 40 | 58 | 27 | 152 |
| 2 | 0 | 1 | 3 | 3 | 22 | 10 | 29 | ≥36 | — | — | — |
| 3 | 0 | 0 | 2 | 2 | 3 | 2 | ≥16 | — | — | — | — |
| 4 | 0 | 0 | 0 | 2 | ≥5 | 4 | — | — | — | — | — |
| 5 | 0 | 0 | 0 | 0 | 1 | 1 | — | — | — | — | — |
| 6 | 0 | 0 | 1 | 0 | 3 | — | — | — | — | — | — |
| 7 | 0 | 0 | 0 | 0 | 2 | — | — | — | — | — | — |

[Ranks 2–8 counts](data/grothendieck_counts.csv) · [Ranks 9–10 ledger](evidence/unresolved_retry_20261024/rank9_rank10_m1_ledger.csv) · [Rank-nine M2 ledger](evidence/frontier_20261027/rank9_m2_ledger.csv) · [Rank-11 ledger](evidence/rank11_m1_20261023/work/rank11/ledger.csv) · [Definitions and scope](docs/PROJECT_GUIDE.md#grothendieck-rings--known-realizations-at-each-exact-multiplicity)

</details>

<a id="read-the-mathematics"></a>
<a id="structure"></a>

## Read, inspect, reproduce

| Resource | Start here |
|---|---|
| **Rank-four theorem** | [Unrestricted classification and reading guide](manuscripts/rank4/README.md) |
| Mathematics | [Manuscripts by rank](manuscripts/README.md) · [Current open tensors](data/current_remaining_cases.py) · [Current frontier report · PDF](manuscripts/frontier/Fusion_Ring_Frontier.pdf) |
| Data | [Current decision records](data/current_publication_revision.json) · [All fusion rings and enumeration](https://github.com/sebastienpalcoux/fusion-ring-census) |
| Computation | [Rank-nine M2 replay](evidence/rank9_m2_20261024/README.md) · [Rank-11 replay](evidence/rank11_m1_20261023/README.md) · [Earlier replay instructions](docs/VERIFY.md) · [Provenance](docs/PROVENANCE.md) |
| Project details | [Research updates, models, band tables and repository guide](docs/PROJECT_GUIDE.md) |
| Announcement & citation | [Current four-page overview](announcements/hexagon-2026-10/Low_rank_Grothendieck_rings_announcement.pdf) · [Hexagon](https://hexagonmath.org/2610.00300) · [How to cite](https://sebastienpalcoux.github.io/grothendieck-ring-classification/#cite) |

The companion [Fusion Ring Census](https://github.com/sebastienpalcoux/fusion-ring-census)
enumerates based rings. This repository records their categorifications and exclusions.

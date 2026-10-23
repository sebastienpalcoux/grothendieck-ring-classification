# Grothendieck ring classification

**Which low-rank fusion rings admit fusion categories over ℂ?**

[**Explore the atlas →**](https://sebastienpalcoux.github.io/grothendieck-ring-classification/) · [Manuscripts](manuscripts/README.md) · [Open cases](https://sebastienpalcoux.github.io/grothendieck-ring-classification/unresolved.html) · [Verification](docs/VERIFY.md)

> **AI-generated research · independent verification pending.**
> Results and computations remain provisional. [Research status and verification scope](docs/PREPUBLICATION_REVIEW.md).

<!-- rank11-release -->

**23 October: rank eleven, multiplicity one.** **155 excluded over ℂ, 27 unitary models, 0 unresolved** among all 182 supplied tensors. [Browse every case](https://sebastienpalcoux.github.io/grothendieck-ring-classification/rank11.html) · [Manuscript](publications/rank11/paper/rank11.pdf) · [Proofs and exact replay](evidence/rank11_m1_20261023/README.md).

<details><summary>Ranks nine and ten · previous release</summary>

233 general exclusions, 97 unitary models and [6 unresolved](https://sebastienpalcoux.github.io/grothendieck-ring-classification/rank9-10.html?status=unresolved) among 336 supplied tensors. [Browse cases](https://sebastienpalcoux.github.io/grothendieck-ring-classification/rank9-10.html) · [Manuscript](publications/rank9-rank10/paper/rank9-rank10.pdf).

</details>

<!-- /rank11-release -->

<a id="classification--what-is-decided"></a>

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
| 8 | Through 3 | **Complete through 2**; multiplicity 3 partial | Through 3: 4,403 excluded, 93 realized, 4 unresolved. |
| 9 | Multiplicity 1 | **Complete at multiplicity 1** | 102 excluded, 40 realized, 0 unresolved. |
| 10 | Multiplicity 1 | **Partial at multiplicity 1** | 131 excluded, 57 realized, [6 unresolved](https://sebastienpalcoux.github.io/grothendieck-ring-classification/rank9-10.html?rank=10&status=unresolved). |
| 11 | Multiplicity 1 | **Complete at multiplicity 1** | 155 excluded, 27 realized, 0 unresolved. |

**12 open cases.** General categorification remains undecided for these rings.
[Explore their status, invariants and research records](https://sebastienpalcoux.github.io/grothendieck-ring-classification/unresolved.html).

<details id="grothendieck-rings--known-realizations-at-each-exact-multiplicity">
<summary><strong>Known realizations at each exact multiplicity</strong></summary>

Multiplicity is the largest fusion coefficient. `≥` marks a lower bound where
general categorification remains open; a dash marks an unanalyzed band.

| Multiplicity | Rank 2 | Rank 3 | Rank 4 | Rank 5 | Rank 6 | Rank 7 | Rank 8 | Rank 9 | Rank 10 | Rank 11 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 2 | 4 | 9 | 10 | 21 | 13 | 48 | 40 | ≥57 | 27 |
| 2 | 0 | 1 | 3 | 3 | 22 | 10 | 29 | — | — | — |
| 3 | 0 | 0 | 2 | 2 | 3 | 2 | ≥16 | — | — | — |
| 4 | 0 | 0 | 0 | 2 | ≥5 | 4 | — | — | — | — |
| 5 | 0 | 0 | 0 | 0 | 1 | 1 | — | — | — | — |
| 6 | 0 | 0 | 1 | 0 | 3 | — | — | — | — | — |
| 7 | 0 | 0 | 0 | 0 | 2 | — | — | — | — | — |

[Ranks 2–8 counts](data/grothendieck_counts.csv) · [Ranks 9–10 ledger](evidence/rank9_rank10_m1_20261023/deliverable/ledger.csv) · [Rank-11 ledger](evidence/rank11_m1_20261023/work/rank11/ledger.csv) · [Definitions and scope](docs/PROJECT_GUIDE.md#grothendieck-rings--known-realizations-at-each-exact-multiplicity)

</details>

<a id="read-the-mathematics"></a>
<a id="structure"></a>

## Read, inspect, reproduce

| Resource | Start here |
|---|---|
| **Rank-four theorem** | [Unrestricted classification and reading guide](manuscripts/rank4/README.md) |
| Mathematics | [Manuscripts by rank](manuscripts/README.md) · [Earlier construction-candidates report · PDF](docs/New_category_candidates_and_open_cases.pdf) |
| Data | [Current decision records](data/current_publication_revision.json) · [All fusion rings and enumeration](https://github.com/sebastienpalcoux/fusion-ring-census) |
| Computation | [Rank-11 replay](evidence/rank11_m1_20261023/README.md) · [Earlier replay instructions](docs/VERIFY.md) · [Provenance](docs/PROVENANCE.md) |
| Project details | [Research updates, models, band tables and repository guide](docs/PROJECT_GUIDE.md) |
| Announcement | [Five-page introduction](announcements/hexagon-2026-10/Low_rank_Grothendieck_rings_announcement.pdf) · [Hexagon](https://hexagonmath.org/2610.00300?version=1) |

The companion [Fusion Ring Census](https://github.com/sebastienpalcoux/fusion-ring-census)
enumerates based rings. This repository records their categorifications and exclusions.

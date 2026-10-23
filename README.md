# Grothendieck ring classification

**Which low-rank fusion rings admit fusion categories over ℂ?**

[**Explore the atlas →**](https://sebastienpalcoux.github.io/grothendieck-ring-classification/) · [Manuscripts](manuscripts/README.md) · [Open cases](https://sebastienpalcoux.github.io/grothendieck-ring-classification/unresolved.html) · [Verification](docs/VERIFY.md)

> **AI-generated research · independent verification pending.**
> Results and computations remain provisional. [Research status and verification scope](docs/PREPUBLICATION_REVIEW.md).

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

**6 open cases.** General categorification remains undecided for these rings.
[Explore their status, invariants and research records](https://sebastienpalcoux.github.io/grothendieck-ring-classification/unresolved.html).

<details>
<summary><strong>Known realizations at each exact multiplicity</strong></summary>

Multiplicity is the largest fusion coefficient. `≥` marks a lower bound where
general categorification remains open; a dash marks an unanalyzed band.

| Multiplicity | Rank 2 | Rank 3 | Rank 4 | Rank 5 | Rank 6 | Rank 7 | Rank 8 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 4 | 9 | 10 | 21 | 13 | 48 |
| 2 | 0 | 1 | 3 | 3 | 22 | 10 | 29 |
| 3 | 0 | 0 | 2 | 2 | 3 | 2 | ≥16 |
| 4 | 0 | 0 | 0 | 2 | ≥5 | 4 | — |
| 5 | 0 | 0 | 0 | 0 | 1 | 1 | — |
| 6 | 0 | 0 | 1 | 0 | 3 | — | — |
| 7 | 0 | 0 | 0 | 0 | 2 | — | — |

[Full count data](data/grothendieck_counts.csv) · [Definitions and scope](docs/PROJECT_GUIDE.md#grothendieck-rings--known-realizations-at-each-exact-multiplicity)

</details>

## Read, inspect, reproduce

| Resource | Start here |
|---|---|
| **Rank-four theorem** | [Unrestricted classification and reading guide](manuscripts/rank4/README.md) |
| Mathematics | [Manuscripts by rank](manuscripts/README.md) · [Candidates and open cases · PDF](docs/New_category_candidates_and_open_cases.pdf) |
| Data | [Decision ledger](data/classification_status.csv) · [All fusion rings and enumeration](https://github.com/sebastienpalcoux/fusion-ring-census) |
| Computation | [Replay instructions](docs/VERIFY.md) · [Provenance](docs/PROVENANCE.md) |
| Project details | [Research updates, models, band tables and repository guide](docs/PROJECT_GUIDE.md) |
| Announcement | [Five-page introduction](announcements/hexagon-2026-10/Low_rank_Grothendieck_rings_announcement.pdf) · [Hexagon](https://hexagonmath.org/2610.00300?version=1) |

The companion [Fusion Ring Census](https://github.com/sebastienpalcoux/fusion-ring-census)
enumerates based rings. This repository records their categorifications and exclusions.

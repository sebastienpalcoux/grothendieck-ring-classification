# Grothendieck ring classification

### Which low-rank fusion rings admit fusion categories over ℂ?

An atlas of **exact based-ring counts**, **categorification decisions** and the
proofs behind those decisions. The census and classification have different
bounds. A ring counted by the census is not thereby categorifiable.

**[Browse all counts](data/counts.csv)** · **[Classification outcomes](data/classification_status.csv)** · **[Provenance](docs/PROVENANCE.md)** · **[Verify the data](docs/VERIFY.md)** · **[Manuscripts](manuscripts/README.md)**

> **Scope.** Multiplicity is the maximum fusion coefficient. Each cell below
> counts based-isomorphism classes with *exactly* that multiplicity. A dash
> means the whole rank/multiplicity band has not been enumerated; it never
> means zero. The symbolic rank-two sequence continues beyond this table.

## Census · rings at each exact multiplicity

| Multiplicity | Rank 2 | Rank 3 | Rank 4 | Rank 5 | Rank 6 | Rank 7 | Rank 8 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 4 | 10 | 16 | 39 | 43 | 96 |
| 2 | 1 | 3 | 17 | 37 | 154 | 319 | 877 |
| 3 | 1 | 4 | 24 | 82 | 384 | 1,059 | — |
| 4 | 1 | 6 | 45 | 134 | 872 | 2,780 | — |
| 5 | 1 | 5 | 55 | 209 | 1,582 | — | — |
| 6 | 1 | 9 | 81 | 336 | 2,768 | — | — |
| 7 | 1 | 6 | 92 | 477 | 3,814 | — | — |
| 8 | 1 | 10 | 137 | 733 | 6,999 | — | — |
| 9 | 1 | 12 | 151 | 863 | — | — | — |
| 10 | 1 | 9 | 186 | 1,082 | — | — | — |
| 11 | 1 | 10 | 238 | 1,383 | — | — | — |
| 12 | 1 | 20 | 291 | 1,948 | — | — | — |
| 13 | 1 | 9 | 246 | 2,211 | — | — | — |
| 14 | 1 | 13 | 340 | 2,554 | — | — | — |
| 15 | 1 | 16 | 349 | 2,936 | — | — | — |
| 16 | 1 | 25 | 525 | 4,157 | — | — | — |
| 17 | 1 | 11 | 424 | 4,255 | — | — | — |
| 18 | 1 | 18 | 477 | 5,080 | — | — | — |
| 19 | 1 | 20 | 513 | 5,640 | — | — | — |
| 20 | 1 | 22 | 713 | 6,866 | — | — | — |

Full data: [JSON](data/counts.json) · [CSV](data/counts.csv). The source
[fusion-ring-census](https://github.com/sebastienpalcoux/fusion-ring-census)
contains the tensors and enumerator. The table here is pinned to its commit
`b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726`. Rank-two counts follow
directly from the normal form `X² = 1 + nX` for `n ≥ 0`: two rings at
multiplicity 1, then one at every multiplicity `m ≥ 2`.

## Classification · what is decided?

| Rank | Full census | General classification | Current conclusion |
|---:|---:|---:|---|
| 2 | Symbolic, all multiplicities | All multiplicities over ℂ | Exactly the rings `n = 0, 1` are realized; revised proof in preparation. |
| 3 | Through 1,000 | Unrestricted theorem | See the short rank-three sphericality and classification manuscript. |
| 4 | Through 128 | **Complete through 128** | 15 realized rings, 889,515 general exclusions. |
| 5 | Through 20 | **Complete through 17** | 17 realized rings. At 18, 5,078 excluded and two generally unresolved. At 19–20, the census is available but no classification ledger is supplied. |
| 6 | Through 8 | **Complete through 2** | Through 7: 9,530 excluded, 54 realized, 29 unresolved. Multiplicity 8 is census-only. |
| 7 | Through 4 | No manuscript classification ledger | Census counts only. |
| 8 | Through 2 | No manuscript classification ledger | Census counts only. |

Rank-six realization counts through multiplicity 7 split into **53 unitary
models** and **one spherical model whose ring has no pseudo-unitary
categorification**. “Realized” means that at least one categorification is
constructed; it does not assert that every categorification of that ring is
unitary. The rank-five two residual rings have spherical exclusions but their
general categorification status remains unresolved.

### The classification boundary, band by band

| Multiplicity | Rank 4 | Rank 5 | Rank 6 |
|---:|---:|---:|---:|
| 1 | 1 excluded · 9 realized | 6 excluded · 10 realized | 18 excluded · 21 realized |
| 2 | 14 excluded · 3 realized | 34 excluded · 3 realized | 132 excluded · 22 realized |
| 3 | 22 excluded · 2 realized | 80 excluded · 2 realized | 380 excluded · 3 realized · **1 open** |
| 4 | 45 excluded · 0 realized | 132 excluded · 2 realized | 855 excluded · 2 realized · **15 open** |
| 5 | 55 excluded · 0 realized | 209 excluded · 0 realized | 1,577 excluded · 1 realized · **4 open** |
| 6 | 80 excluded · 1 realized | 336 excluded · 0 realized | 2,761 excluded · 3 realized · **4 open** |
| 7 | 92 excluded · 0 realized | 477 excluded · 0 realized | 3,807 excluded · 2 realized · **5 open** |
| 8 | 137 excluded · 0 realized | 733 excluded · 0 realized | 6,999 census; analysis pending |
| 9 | 151 excluded · 0 realized | 863 excluded · 0 realized | — |
| 10 | 186 excluded · 0 realized | 1,082 excluded · 0 realized | — |
| 11 | 238 excluded · 0 realized | 1,383 excluded · 0 realized | — |
| 12 | 291 excluded · 0 realized | 1,948 excluded · 0 realized | — |
| 13 | 246 excluded · 0 realized | 2,211 excluded · 0 realized | — |
| 14 | 340 excluded · 0 realized | 2,554 excluded · 0 realized | — |
| 15 | 349 excluded · 0 realized | 2,936 excluded · 0 realized | — |
| 16 | 525 excluded · 0 realized | 4,157 excluded · 0 realized | — |
| 17 | 424 excluded · 0 realized | 4,255 excluded · 0 realized | — |
| 18 | 477 excluded · 0 realized | 5,078 excluded · 0 realized · **2 open** | — |
| 19 | 513 excluded · 0 realized | 5,640 census; analysis pending | — |
| 20 | 713 excluded · 0 realized | 6,866 census; analysis pending | — |

Full decision bands: [JSON](data/classification_status.json) ·
[CSV](data/classification_status.csv). Statuses come from the attached
rank-four, rank-five and rank-six certificate ledgers; their SHA-256 hashes,
row checks and scope appear in [the provenance record](docs/PROVENANCE.md).

## Read the mathematics

The [manuscripts](manuscripts/README.md) are kept as TeX/PDF pairs. The
classification programs proceed rank by rank: general necessary criteria,
exact automated applications, positive model matches, and explicit residual
frontiers. Rank three takes a separate, unrestricted route through the
sphericality theorem. The papers and computation records remain research in
progress; [the evidence guide](docs/VERIFY.md) identifies exactly what the
stored checks establish.

## Structure

```text
data/         Pinned census matrix and classification-status tables
docs/         Provenance, terminology and verification paths
manuscripts/  Revised TeX and PDF pairs, as released
site/         Static atlas source and private-preview assets
tools/        Deterministic count/status export and crosswalk checks
```

**Source of truth:** the [fusion-ring-census repository](https://github.com/sebastienpalcoux/fusion-ring-census)
owns the based-ring census and raw tensor files. This repository records the
classification, proofs and models; it does not recompute the census. Changes
to a source census cell are imported only from a named commit and rechecked
against classification ledgers.

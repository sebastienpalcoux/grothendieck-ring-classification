# Grothendieck ring classification

### Which low-rank fusion rings admit fusion categories over ℂ?

An atlas of **realized Grothendieck rings**, **categorification decisions** and
the proofs behind those decisions. The fusion-ring census and classification
have different bounds. A ring counted by the census is not thereby
categorifiable.

**[Grothendieck ring counts](data/grothendieck_counts.csv)** · **[Fusion-ring census](https://github.com/sebastienpalcoux/fusion-ring-census#readme)** · **[Classification outcomes](data/classification_status.csv)** · **[Provenance](docs/PROVENANCE.md)** · **[Verify the data](docs/VERIFY.md)** · **[Manuscripts](manuscripts/README.md)** · **[OEIS drafts](oeis/README.md)**

[**Private working atlas (owner-only)**](https://grothendieck-ring-atlas.sebastien-palcoux.chatgpt.site) · [Atlas source and snapshot](site/)

> **Scope.** Multiplicity is the maximum fusion coefficient. Each cell below
> counts known categorifiable based-isomorphism classes with *exactly* that
> multiplicity. A plain number is exact where classification is complete;
> `≥n` is a certified lower bound where general cases remain unresolved.
> A dash denotes a band not analyzed here. Rows with no known realizations
> are omitted; omission makes no assertion about unresolved cases.

## Grothendieck rings · known realizations at each exact multiplicity

| Multiplicity | Rank 2 | Rank 3 | Rank 4 | Rank 5 | Rank 6 | Rank 7 | Rank 8 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 4 | 9 | 10 | 21 | ≥10 | ≥25 |
| 2 | 0 | 1 | 3 | 3 | 22 | ≥5 | ≥8 |
| 3 | 0 | 0 | 2 | 2 | 3 | ≥1 | — |
| 4 | 0 | 0 | 0 | 2 | ≥5 | ≥0 | — |
| 5 | 0 | 0 | 0 | 0 | 1 | — | — |
| 6 | 0 | 0 | 1 | 0 | 3 | — | — |
| 7 | 0 | 0 | 0 | 0 | 2 | — | — |

Full realized-count data, including zero and unresolved bands:
[JSON](data/grothendieck_counts.json) · [CSV](data/grothendieck_counts.csv).
The [fusion-ring-census repository](https://github.com/sebastienpalcoux/fusion-ring-census)
contains the separate table of **all fusion rings** and its enumerator;
[this repository's pinned census import](data/counts.csv) supports the
classification cross-check. Rank-two realized counts follow directly from
`X² = 1+nX`: both categorifiable rings occur at multiplicity 1.

## Classification · what is decided?

| Rank | Full census | General classification | Current conclusion |
|---:|---:|---:|---|
| 2 | Symbolic, all multiplicities | All multiplicities over ℂ | Exactly the rings `n = 0, 1` are realized; see the revised proof. |
| 3 | Through 1,000 | Unrestricted theorem | Five realized rings: four at multiplicity 1 and one at 2; see the standalone sphericality and ring-classification proof. |
| 4 | Through 128 | **Complete through 128** | 15 realized rings, 889,515 general exclusions. |
| 5 | Through 20 | **Complete through 20** | 17 realized rings and 40,982 generally excluded. The two former multiplicity-18 residuals are now excluded by inert-prime parity and exact induction. |
| 6 | Through 9 | **Complete through 3** | Through 9: 25,351 excluded, 57 realized, 13 unresolved. |
| 7 | Through 4 | Partial at every band | Through 4: 4,107 excluded, 16 realized, 78 unresolved; full normal and optimized certificate replays passed. |
| 8 | Through 2 | Partial at both bands | Through 2: 824 excluded, 33 realized, 116 unresolved; positive tensors and transferred certificates verified. |

Rank-six realization counts through multiplicity 9 split into **56 unitary
models** and **one spherical model whose ring has no pseudo-unitary
categorification**. “Realized” means that at least one categorification is
constructed; it does not assert that every categorification of that ring is
unitary. Rank five has no unresolved ring through multiplicity 20.

The rank-six release covers **25,421 fusion rings through multiplicity 9**:
**25,351 excluded, 57 realized and 13 unresolved**.
The new stratum contains 8,809 rings, of which 8,798 have exact general
exclusion certificates and 11 remain unresolved. The previous decisions,
representatives and proof certificates are preserved.

The positive catalogue includes the three neutral module categories from
`(B2)_7 ⊂ (D7)_1`, `(C3)_4 ⊂ (B10)_1`, and `(B2)_12 ⊂ (E8)_1`, with full tensor identifications.

| Unresolved ring | Necessary reduction |
|---|---|
| `R6_4_155` | One rank-52 center profile remains, with forced twists of exponent 24 and four duality choices. This is not yet complete modular data or a model. |
| `R6_8_1660` | One relative-center based ring and 1670 labelled center profiles remain. A tensor involution and Vafa/indicator constraints remove 57 more profiles. |
| `R6_9_529` | Recorded multiplicity-nine searches leave this ring unresolved. No additional structural frontier reduction is asserted. |
| `R6_9_1060` | Recorded multiplicity-nine searches leave this ring unresolved. No additional structural frontier reduction is asserted. |
| `R6_9_2455` | Recorded multiplicity-nine searches leave this ring unresolved. No additional structural frontier reduction is asserted. |
| `R6_9_3748` | Braided categorifications are ruled out by the rank-three subcategory and centralizer obstruction. General, pivotal, spherical, pseudo-unitary and unitary existence remain unknown. |
| `R6_9_7018` | Pivotal, spherical, pseudo-unitary and unitary categorifications are ruled out by a retained exact certificate. General existence remains unknown. |
| `R6_9_7741` | Pivotal, spherical, pseudo-unitary and unitary categorifications are ruled out by a retained exact certificate. General existence remains unknown. |
| `R6_9_7742` | Pivotal, spherical, pseudo-unitary and unitary categorifications are ruled out by a retained exact certificate. General existence remains unknown. |
| `R6_9_8099` | Pivotal, spherical, pseudo-unitary and unitary categorifications are ruled out by a retained exact certificate. General existence remains unknown. |
| `R6_9_8101` | Pivotal, spherical, pseudo-unitary and unitary categorifications are ruled out by a retained exact certificate. General existence remains unknown. |
| `R6_9_8200` | Pivotal, spherical, pseudo-unitary and unitary categorifications are ruled out by a retained exact certificate. General existence remains unknown. |
| `R6_9_8785` | Recorded multiplicity-nine searches leave this ring unresolved. No additional structural frontier reduction is asserted. |

[Manuscript](manuscripts/rank6/papers/manuscript.pdf) ·
[Multiplicity-nine evidence](supplements/rank6/verification/m9/) ·
[Current frontier](supplements/rank6/research/frontier/README.md) ·
[Complete release](https://grothendieck-ring-atlas.sebastien-palcoux.chatgpt.site/downloads/Rank6_Categorification_M9_Revised_2026-10-01_v1.zip)


### The classification boundary, band by band

| Multiplicity | Rank 4 | Rank 5 | Rank 6 | Rank 7 | Rank 8 |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 excluded · 9 realized | 6 excluded · 10 realized | 18 excluded · 21 realized | 30 excluded · 10 realized · **3 open** | 41 excluded · 25 realized · **30 open** |
| 2 | 14 excluded · 3 realized | 34 excluded · 3 realized | 132 excluded · 22 realized | 291 excluded · 5 realized · **23 open** | 783 excluded · 8 realized · **86 open** |
| 3 | 22 excluded · 2 realized | 80 excluded · 2 realized | 381 excluded · 3 realized | 1,035 excluded · 1 realized · **23 open** | — |
| 4 | 45 excluded · 0 realized | 132 excluded · 2 realized | 866 excluded · 5 realized · **1 open** | 2,751 excluded · 0 realized · **29 open** | — |
| 5 | 55 excluded · 0 realized | 209 excluded · 0 realized | 1,581 excluded · 1 realized | — | — |
| 6 | 80 excluded · 1 realized | 336 excluded · 0 realized | 2,765 excluded · 3 realized | — | — |
| 7 | 92 excluded · 0 realized | 477 excluded · 0 realized | 3,812 excluded · 2 realized | — | — |
| 8 | 137 excluded · 0 realized | 733 excluded · 0 realized | 6,998 excluded · 0 realized · **1 open** | — | — |
| 9 | 151 excluded · 0 realized | 863 excluded · 0 realized | 8,798 excluded · 0 realized · **11 open** | — | — |
| 10 | 186 excluded · 0 realized | 1,082 excluded · 0 realized | — | — | — |
| 11 | 238 excluded · 0 realized | 1,383 excluded · 0 realized | — | — | — |
| 12 | 291 excluded · 0 realized | 1,948 excluded · 0 realized | — | — | — |
| 13 | 246 excluded · 0 realized | 2,211 excluded · 0 realized | — | — | — |
| 14 | 340 excluded · 0 realized | 2,554 excluded · 0 realized | — | — | — |
| 15 | 349 excluded · 0 realized | 2,936 excluded · 0 realized | — | — | — |
| 16 | 525 excluded · 0 realized | 4,157 excluded · 0 realized | — | — | — |
| 17 | 424 excluded · 0 realized | 4,255 excluded · 0 realized | — | — | — |
| 18 | 477 excluded · 0 realized | 5,080 excluded · 0 realized | — | — | — |
| 19 | 513 excluded · 0 realized | 5,640 excluded · 0 realized | — | — | — |
| 20 | 713 excluded · 0 realized | 6,866 excluded · 0 realized | — | — | — |

Full decision bands: [JSON](data/classification_status.json) ·
[CSV](data/classification_status.csv). Statuses come from the attached
rank-four through rank-eight certificate ledgers; their SHA-256 hashes,
row checks and scope appear in [the provenance record](docs/PROVENANCE.md).

### When did the current criterion repertoire stabilize?

| Rank | Last first use of a mathematical criterion family | Checked range afterward |
|---:|---:|---|
| 4 | Multiplicity 18 | The same criterion families suffice for the allocated exclusions at 19–128. |
| 5 | Multiplicity 18 | Inert-prime quadratic parity first closes two cases at 18; no new criterion family is needed at 19–20. |
| 6 | See the allocation ledger | The current criteria include stabilizer, cyclotomic-trace and signed arithmetic obstructions. Every new multiplicity-nine tensor is processed separately from the preserved earlier campaign; 13 general cases remain unresolved through multiplicity 9. |
| 7 | Multiplicity 2 | Signed sphericalization first contributes at 1; the last first successful application of a listed family occurs at 2. There are 78 open rings through 4, so no stabilization conclusion follows. |
| 8 | Multiplicity 2 | Signed obstructions first contribute at 1; the last first successful application of a listed family occurs at 2. There are 116 open rings through 2, so no stabilization conclusion follows. |

This records **first use in the chosen certificate allocation**, not an
optimal ordering theorem or a claim that the criteria settle higher
multiplicities. Rank-four nested signed cyclotomicity first succeeds at 95,
using a general cyclotomicity theorem already used at 9. The ordered
step-by-step exclusion tables and proof dependencies are in the manuscripts.

## Read the mathematics

The [manuscripts](manuscripts/README.md) are kept as TeX/PDF pairs. The
classification programs proceed rank by rank: general necessary criteria,
exact automated applications, positive model matches, and explicit residual
frontiers. Rank three takes a separate, unrestricted route through the
sphericality theorem. The papers and computation records remain research in
progress; [the evidence guide](docs/VERIFY.md) identifies exactly what the
stored checks establish.

## Structure

After cloning, restore the large datasets with one offline command:

```bash
python3 tools/restore_data.py
```

The repository stores those datasets as small compressed parts. The command
checks every part and reconstructed file against its released SHA-256 hash;
it requires only Python's standard library. See [verification instructions](docs/VERIFY.md).

```text
data/         Pinned census matrix and classification-status tables
docs/         Provenance, terminology and verification paths
manuscripts/  Revised TeX and PDF pairs, as released
supplements/  Proof software, compact certificates and verification reports
site/         Static atlas source and private-preview assets
tools/        Deterministic count/status export and crosswalk checks
oeis/         Sequence drafts, pending an OEIS submission
```

**Source of truth:** the [fusion-ring-census repository](https://github.com/sebastienpalcoux/fusion-ring-census)
owns the based-ring census and raw tensor files. This repository records the
classification, proofs and models; it does not recompute the census. Changes
to a source census cell are imported only from a named commit and rechecked
against classification ledgers.

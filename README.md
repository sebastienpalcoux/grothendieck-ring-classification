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
| 1 | 2 | 4 | 9 | 10 | 21 | 13 | ≥48 |
| 2 | 0 | 1 | 3 | 3 | 22 | ≥10 | ≥24 |
| 3 | 0 | 0 | 2 | 2 | 3 | ≥2 | — |
| 4 | 0 | 0 | 0 | 2 | ≥5 | ≥2 | — |
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
| 6 | Through 9 | **Complete through 3** | Through 9: 25,362 excluded, 57 realized, 2 unresolved. |
| 7 | Through 4 | **Complete at multiplicity 1** | Through 4: 4,135 excluded, 27 realized, 39 unresolved. |
| 8 | Through 2 | Partial at both bands | Through 2: 857 excluded, 72 realized, 44 unresolved. |

Rank-six realization counts through multiplicity 9 split into **56 unitary
models** and **one spherical model whose ring has no pseudo-unitary
categorification**. “Realized” means that at least one categorification is
constructed; it does not assert that every categorification of that ring is
unitary. Rank five has no unresolved ring through multiplicity 20.

The rank-six release covers **25,421 fusion rings through multiplicity 9**:
**25,362 excluded, 57 realized and 2 unresolved**.
All **8,809 rings of exact multiplicity nine are generally excluded**.
The completion certificates settle the final eleven cases; the two remaining
unresolved rings belong to earlier bands. Previous representatives and proof
certificates are preserved.

The positive catalogue includes the three neutral module categories from
`(B2)_7 ⊂ (D7)_1`, `(C3)_4 ⊂ (B10)_1`, and `(B2)_12 ⊂ (E8)_1`, with full tensor identifications.

| Unresolved ring | Necessary reduction |
|---|---|
| `R6_4_155` | The unique rank-26 modular candidate remains feasible. All 70 small B3 spectral-partition tests pass; neither these tests nor the modular datum constructs a category. No model or general exclusion is known. Exact probability couplings prove every Lim Corollary 3.4 inequality for every exponent and nonnegative vector. |
| `R6_8_1660` | Exact graded induction-packet identities eliminate 533 further center profiles, leaving 1,136 in branches 120, 508, 508. Every dominant pivotal tensor quotient of the positive spherical form would be an equivalence. Three Morita-dual based rings remain possible; none admits a braiding. No model or general exclusion is known. Exact probability couplings prove every Lim Corollary 3.4 inequality for every exponent and nonnegative vector. |

[Manuscript](manuscripts/rank6/papers/manuscript.pdf) ·
[Completion proofs](supplements/rank6/research/exclusions/m9_completion/) ·
[Completion replay](supplements/rank6/verification/m9/completion/) ·
[2 October research addendum](evidence/residual_20261002/rank6/research_addendum.pdf) ·
[Complete release](https://grothendieck-ring-atlas.sebastien-palcoux.chatgpt.site/downloads/Rank6_Categorification_M9_Frontier_2026-10-01.zip)


The [43-decision residual stage](evidence/upper_residual_20261002b/README.md) and its [14-decision continuation](evidence/upper_residual_20261002c/README.md) resolve 57 further rings: 44 general exclusions and 13 unitary models. The continuation generally excludes `R7_2_160`, `R7_4_1417`, `R7_4_1420`, `R8_2_312`, `R8_2_315`, `R8_2_317`, `R8_2_53`, `R8_2_93`, `R8_2_191`, `R8_2_299`, `R8_2_158`, `R8_2_186`, `R8_2_579`, `R8_2_682`. Stage b retains its frozen proofs and replay; stage c restores the historical ledgers when checking that replay.
These proofs supplement the [earlier 46-decision stage](evidence/residual_20261002/README.md).
Scope-specific obstructions retain their stated assumptions and do not change
a ring's general unresolved status.

### The classification boundary, band by band

| Multiplicity | Rank 4 | Rank 5 | Rank 6 | Rank 7 | Rank 8 |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 excluded · 9 realized | 6 excluded · 10 realized | 18 excluded · 21 realized | 30 excluded · 13 realized | 45 excluded · 48 realized · **3 open** |
| 2 | 14 excluded · 3 realized | 34 excluded · 3 realized | 132 excluded · 22 realized | 302 excluded · 10 realized · **7 open** | 812 excluded · 24 realized · **41 open** |
| 3 | 22 excluded · 2 realized | 80 excluded · 2 realized | 381 excluded · 3 realized | 1,045 excluded · 2 realized · **12 open** | — |
| 4 | 45 excluded · 0 realized | 132 excluded · 2 realized | 866 excluded · 5 realized · **1 open** | 2,758 excluded · 2 realized · **20 open** | — |
| 5 | 55 excluded · 0 realized | 209 excluded · 0 realized | 1,581 excluded · 1 realized | — | — |
| 6 | 80 excluded · 1 realized | 336 excluded · 0 realized | 2,765 excluded · 3 realized | — | — |
| 7 | 92 excluded · 0 realized | 477 excluded · 0 realized | 3,812 excluded · 2 realized | — | — |
| 8 | 137 excluded · 0 realized | 733 excluded · 0 realized | 6,998 excluded · 0 realized · **1 open** | — | — |
| 9 | 151 excluded · 0 realized | 863 excluded · 0 realized | 8,809 excluded · 0 realized | — | — |
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
| 6 | See the allocation ledger | The current criteria include stabilizer, cyclotomic-trace and signed arithmetic obstructions. All 8,809 exact-multiplicity-nine rings have general exclusion certificates; 2 earlier cases remain unresolved through multiplicity 9. |
| 7 | Multiplicity 4 | The dimension-310 group-theoretical criterion first contributes at 4. There are 39 generally open rings through 4, so no stabilization conclusion follows. |
| 8 | Multiplicity 2 | Graded Brauer-Picard obstructions contribute at 1 and 2; the rank-one fiber-functor obstruction contributes at 2. There are 44 generally open rings through 2, so no stabilization conclusion follows. |

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

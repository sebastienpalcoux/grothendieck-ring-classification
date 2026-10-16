# Grothendieck ring classification

**Which low-rank fusion rings admit fusion categories over ℂ?**

Explore realized Grothendieck rings, proposed categorification arguments and
the exact data behind them. The public atlas connects interactive tables,
individual ring profiles, manuscripts and reproducible computation records.

### [Open the interactive atlas →](https://sebastienpalcoux.github.io/grothendieck-ring-classification/)

> [!IMPORTANT]
> **AI-generated research · independent verification pending.**
> The results, proofs, code and data in this project are AI-generated and
> have not yet been independently verified by human experts or formalized
> in Lean. Treat them as provisional and use them with caution. Automated
> checks establish only their stated computational scope; they do not
> replace mathematical review or formal proof.
> [Research-status notice](docs/RESEARCH_STATUS.md) ·
> [Prepublication review and dated errata](docs/PREPUBLICATION_REVIEW.md).
> Read the errata alongside the frozen manuscripts.

| Start here | What you will find |
|---|---|
| [Explore the atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/) | Filter counts, inspect fusion rules and character data, and follow source links. |
| [Read the manuscripts](manuscripts/README.md) | TeX sources and PDFs, organized by rank. |
| [Inspect the data](data/classification_status.csv) | Classification outcomes, [realized counts](data/grothendieck_counts.csv) and the separate [fusion-ring census](https://github.com/sebastienpalcoux/fusion-ring-census#readme). |
| [Reproduce the checks](docs/VERIFY.md) | Replay instructions, [provenance](docs/PROVENANCE.md) and the limits of each check. |

**Current research snapshot · 17 October 2026.** The prepublication review
reopens **R8_2_24** after finding a gap in its proposed exclusion. The latest
continuation retains **35 of 38** decisions: 28 proposed general exclusions
and 7 unitary constructions. **Three general cases remain open:** `R6_4_155`,
`R6_8_1660`, and `R8_2_24`. Read the [correction and current case inventory](evidence/review_20261017/README.md)
alongside the frozen manuscripts. The tables below report the project's
current classification claims; “complete” and “certified” do not imply
independent human verification or Lean formalization.

[Realized counts](#grothendieck-rings--known-realizations-at-each-exact-multiplicity) · [Classification](#classification--what-is-decided) · [Manuscripts](#read-the-mathematics) · [Repository guide](#structure) · [OEIS drafts](oeis/README.md)

> **Scope.** Multiplicity is the maximum fusion coefficient. Each cell below
> counts known categorifiable based-isomorphism classes with *exactly* that
> multiplicity. A plain number is exact where classification is complete;
> `≥n` is a certified lower bound where general cases remain unresolved.
> A dash denotes a band not analyzed here. Rows with no known realizations
> are omitted; omission makes no assertion about unresolved cases.

## Grothendieck rings · known realizations at each exact multiplicity

| Multiplicity | Rank 2 | Rank 3 | Rank 4 | Rank 5 | Rank 6 | Rank 7 | Rank 8 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 4 | 9 | 10 | 21 | 13 | 48 |
| 2 | 0 | 1 | 3 | 3 | 22 | 10 | ≥29 |
| 3 | 0 | 0 | 2 | 2 | 3 | 2 | — |
| 4 | 0 | 0 | 0 | 2 | ≥5 | 4 | — |
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

These are the recorded outcomes of the current research program, subject to
the verification notice and [prepublication review](docs/PREPUBLICATION_REVIEW.md).

| Rank | Full census | General classification | Current conclusion |
|---:|---:|---:|---|
| 2 | Symbolic, all multiplicities | All multiplicities over ℂ | Exactly the rings `n = 0, 1` are realized; see the revised proof. |
| 3 | Through 1,000 | Unrestricted theorem | Five realized rings: four at multiplicity 1 and one at 2; see the standalone sphericality and ring-classification proof. |
| 4 | Through 128 | **Complete through 128** | 15 realized rings, 889,515 general exclusions. |
| 5 | Through 20 | **Complete through 20** | 17 realized rings and 40,982 generally excluded. The two former multiplicity-18 residuals are now excluded by inert-prime parity and exact induction. |
| 6 | Through 9 | **Complete through 3** | Through 9: 25,362 excluded, 57 realized, 2 unresolved. |
| 7 | Through 4 | **Complete through 4** | Through 4: 4,172 excluded, 29 realized, 0 unresolved. |
| 8 | Through 2 | **Complete through 1** | Through 2: 895 excluded, 77 realized, 1 unresolved. |

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
| `R6_4_155` | The inherited rank-22 based module passes all 234,256 linking identities forced by the fermion Clifford algebra and its Azumaya Morita self-duality. This strengthens the necessary compatibility check but constructs no coherent module category or categorification. The case remains unresolved. |
| `R6_8_1660` | Saturated modular character traces force nu_3(T)=2 and two conjugate options for nu_3(X). A separate exact Verlinde calculation now excludes the historical rank-37 witness by forcing a fusion coefficient 1/2. Other profiles remain open; no general exclusion or categorification is claimed. |

The October 16 revision identifies the entire twist-one support in the center
of a positive Galois representative of R6_8_1660 and retains tensor-functor
rigidity for both residual rings. Both categorification questions remain open.
The current source/PDF hashes are recorded separately from the frozen release.

[Manuscript](manuscripts/rank6/papers/manuscript.pdf) ·
[16 October theoretical update](evidence/theoretical_20261016/README.md) ·
[11 October theoretical revision](evidence/rank6_theoretical_20261011/README.md) ·
[Completion proofs](supplements/rank6/research/exclusions/m9_completion/) ·
[Completion replay](supplements/rank6/verification/m9/completion/) ·
[2 October research addendum](evidence/residual_20261002/rank6/research_addendum.pdf) ·
[Frozen 1 October release](https://sebastienpalcoux.github.io/grothendieck-ring-classification/downloads/Rank6_Categorification_M9_Frontier_2026-10-01.zip)


The [17 October prepublication correction](evidence/review_20261017/README.md) reopens **R8_2_24** because its categorical-to-linear bridge is unproved. The latest 38-case continuation retains **35 accepted decisions**: 28 proposed general exclusions and 7 unitary constructions. Three general questions remain open: R6_4_155, R6_8_1660 and R8_2_24. Together with earlier residual stages, 139 decisions remain accepted (119 exclusions and 20 constructions), subject to independent review. The [frozen 36-decision snapshot](evidence/unified_20261016/README.md) and manuscripts remain available with dated errata and exact historical replay; their R8_2_24 exclusion is superseded.
These proofs supplement the [earlier 46-decision stage](evidence/residual_20261002/README.md).
Scope-specific obstructions retain their stated assumptions and do not change
a ring's general unresolved status.

### The classification boundary, band by band

| Multiplicity | Rank 4 | Rank 5 | Rank 6 | Rank 7 | Rank 8 |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 excluded · 9 realized | 6 excluded · 10 realized | 18 excluded · 21 realized | 30 excluded · 13 realized | 48 excluded · 48 realized |
| 2 | 14 excluded · 3 realized | 34 excluded · 3 realized | 132 excluded · 22 realized | 309 excluded · 10 realized | 847 excluded · 29 realized · **1 open** |
| 3 | 22 excluded · 2 realized | 80 excluded · 2 realized | 381 excluded · 3 realized | 1,057 excluded · 2 realized | — |
| 4 | 45 excluded · 0 realized | 132 excluded · 2 realized | 866 excluded · 5 realized · **1 open** | 2,776 excluded · 4 realized | — |
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
| 7 | Multiplicity 4 | Group-theoretical, Morita and center arguments contribute through 4. There are 0 generally open rings in the analyzed range; higher multiplicities are not classified here. |
| 8 | Multiplicity 2 | Graded Brauer-Picard and fiber-functor obstructions contribute through 2; the proposed projective inner-square exclusion of R8_2_24 is withdrawn. There is 1 generally open ring in the analyzed range; higher multiplicities are not classified here. |

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
stored checks establish. For rank eight, start with the
[reading edition and dated corrections](manuscripts/rank8/paper/rank8-reviewed.pdf); the
[historical PDF](manuscripts/rank8/paper/rank8.pdf) retains the superseded
R8_2_24 exclusion for provenance.

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
site/         Public GitHub Pages atlas, source and reproducible snapshots
tools/        Deterministic count/status export and crosswalk checks
oeis/         Sequence drafts, pending an OEIS submission
```

**Source of truth:** the [fusion-ring-census repository](https://github.com/sebastienpalcoux/fusion-ring-census)
owns the based-ring census and raw tensor files. This repository records the
classification, proofs and models; it does not recompute the census. Changes
to a source census cell are imported only from a named commit and rechecked
against classification ledgers.

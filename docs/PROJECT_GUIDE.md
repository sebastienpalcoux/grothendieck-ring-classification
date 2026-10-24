# Grothendieck ring classification · project guide

<!-- current-audit-correction -->
**24 October audit correction.** R8_3_436 is unresolved for general complex
categorification; its unitary exclusion is retained. Rank eight through
multiplicity three now has 4,402 general exclusions, 93 models and five open
cases. With the rank-nine M2 continuation, the current project-wide total is
26 open cases. Earlier dated ledgers and replay receipts keep their historical
scope. [Correction and precise hypotheses](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/audit_20261024/README.md).
<!-- /current-audit-correction -->

<!-- current-high-rank-publication -->

**Current results · 24 October 2026.** Rank nine at exact multiplicity two has **2,033 general exclusions, 32 unitary models and 18 unresolved rings** among 2,083 inputs. The complete rank-nine census through multiplicity two contains 2,225 rings. The project now has **26 unresolved rings** across ranks six, eight, nine and ten. [Rank-nine M2 manuscript](../publications/rank9-m2/paper/rank9-m2.pdf) · [Current proofs and exact replay](../evidence/rank9_m2_20261024/README.md) · [All current manuscripts](../manuscripts/README.md) · [All open cases](https://sebastienpalcoux.github.io/grothendieck-ring-classification/unresolved.html).

<!-- /current-high-rank-publication -->

[Repository front page](../README.md) · [Interactive atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/)

**Which low-rank fusion rings admit fusion categories over ℂ?**

Explore realized Grothendieck rings, proposed categorification arguments and
the exact data behind them. The public atlas connects interactive tables,
individual ring profiles, manuscripts and reproducible computation records.

**Companion repository:** [Fusion Ring Census](https://github.com/sebastienpalcoux/fusion-ring-census)
enumerates all based fusion rings; this repository classifies which admit
categorifications over ℂ.

### [Open the interactive atlas →](https://sebastienpalcoux.github.io/grothendieck-ring-classification/)

> [!IMPORTANT]
> **AI-generated research · independent verification pending.**
> The results, proofs, code and data in this project are AI-generated and
> have not yet been independently verified by human experts or formalized
> in Lean. Treat them as provisional and use them with caution. Automated
> checks establish only their stated computational scope; they do not
> replace mathematical review or formal proof.
> [Research-status notice](../docs/RESEARCH_STATUS.md) ·
> [Verification scope and review](../docs/PREPUBLICATION_REVIEW.md).

> [!NOTE]
> **[Research announcement · 5 pages](../announcements/hexagon-2026-10/Low_rank_Grothendieck_rings_announcement.pdf)**
> Historical October announcement: classification scope, seven construction candidates, and the two rank-six open problems.
> [TeX source and Hexagon submission package](../announcements/hexagon-2026-10/).
> **[Read the announcement on Hexagon · 2610.00300v1](https://hexagonmath.org/2610.00300?version=1)**.

> [!TIP]
> **[Potentially new tensor categories and open cases (PDF)](../docs/New_category_candidates_and_open_cases.pdf)**
> Seven provisional construction candidates, the known `Rep(AGL(1,7))` model, and all 6 current open cases.
> Novelty up to tensor equivalence remains subject to independent verification.

| Start here | What you will find |
|---|---|
| [Explore the atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/) | Filter counts, inspect fusion rules and character data, and follow source links. |
| **[Unrestricted rank-four classification](../manuscripts/rank4/README.md)** | **[Main paper · 88 pages](../manuscripts/rank4/papers/companion.pdf)** · [LaTeX](../manuscripts/rank4/papers/companion.tex). No multiplicity bound or initial pivotality assumption. |
| [Read the manuscripts](../manuscripts/README.md) | TeX sources and PDFs, organized by rank. |
| [Inspect the data](../data/classification_status.csv) | Classification outcomes, [realized counts](../data/grothendieck_counts.csv) and the separate [fusion-ring census](https://github.com/sebastienpalcoux/fusion-ring-census#readme). |
| [Reproduce the checks](../docs/VERIFY.md) | Replay instructions, [provenance](../docs/PROVENANCE.md) and the limits of each check. |

**Current research account.** The 38-case continuation records **36 decisions**:
29 proposed general exclusions and 7 unitary constructions. **Two general
cases from that historical study remain open:** `R6_4_155` and `R6_8_1660`. Rank eight is complete
through multiplicity two, with 896 exclusions and 77 unitary models.
The exclusion of `R8_2_24` follows from an inner-square obstruction using
pivotal duality, short associator weights and tensor-functor rigidity.
The rank-seven multiplicity-five continuation addresses all 5,805 supplied exact-multiplicity-five rings: 5,804 general exclusions, 1 realization and 0 unresolved cases. The classification of the supplied census is complete through multiplicity 5. The new realization R7_5_5678 is Rep(AGL(1,7)).
The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,506 general exclusions, 16 models and 5 unresolved cases. Every recorded model admits a unitary realization. The remaining rings retain unresolved status for general complex categorification; R8_3_436 retains its unitary exclusion.

Canonical normal and optimized frontier replays each passed all 108 checks. These receipts cover the historical frontier stage. Fresh replay after extraction from the publication archive is deferred.

R8_3_721 is realized by the inherited 1+rho Q-system Morita dual of the C2 de-equivariantization of GH(C8). Exact rank and coefficient bounds identify its unique dimension type in the supplied complete rank-eight multiplicity-at-most-three census. The earlier center-action analysis leaves three necessary R8_3_1154 patterns. These results are in evidence/rank8_next_20261021/; the later R8_3_65 general exclusion is in evidence/rank8_research_20261022/.

[Separately verified center-pattern addendum](../evidence/rank8_center_followup_20261021/README.md).

The separate center-pattern addendum passed all eight checks in canonical normal and optimized Python, including independent arithmetic reconstructions and positive controls. Fresh replay after extraction from the publication archive is deferred.

[New GH(C8) Morita model and further unified restrictions](../evidence/rank8_next_20261021/README.md).

**22 October research.** R8_3_3472 admits no fusion categorification over the complex numbers. The sphericalization and Galois reduction covers general complex categories; complete center-frame and twist-orbit domains reduce the remaining case to 628 exact equations in 572 integer variables. A certificate of 1648 rational bound deductions and a final strictly positive separating gap proves infeasibility, with two independent exact checkers. The proof and reproducible certificate are in evidence/r3472_exclusion_20261022/. This complete obstruction supersedes the earlier feasible necessary systems and conditional Morita restrictions for R3472. R8_3_982 remains unitarily realized by the neutral triality component of the exceptional E21 chiral fusion category, with all 512 canonical fusion coefficients identified exactly. Apart from R8_3_436, four rank-eight general categorification questions remain: R8_3_928, R8_3_941, R8_3_1154 and R8_3_1768. Every hypothetical categorification of these four rings admits a spherical structure and has a pseudo-unitary Galois conjugate; none has a braided Morita representative. The R928 phase refinement leaves four of ten necessary center patterns, all fourteen R941 allocations survive the stated refinements, and R1154 retains its forced semionic data. R1768 has 39 of 40 necessary Gram/indicator branches excluded, while its final cone survives. These necessary data do not construct categories or settle the four remaining questions.

[Proofs and exact verifier inventory](../evidence/r3472_exclusion_20261022/README.md). Run this stage separately from the preserved baseline and frontier replays:

```bash
python3 tools/verify_rank8_exclusion_20261022.py
python3 -O tools/verify_rank8_exclusion_20261022.py
```

The tables below report the project's classification claims; “complete” and
“certified” do not imply independent human verification or Lean formalization.

[Realized counts](#grothendieck-rings--known-realizations-at-each-exact-multiplicity) · [Classification](#classification--what-is-decided) · [Manuscripts](#read-the-mathematics) · [Repository guide](#structure) · [OEIS drafts](../oeis/README.md)

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
| 2 | 0 | 1 | 3 | 3 | 22 | 10 | 29 |
| 3 | 0 | 0 | 2 | 2 | 3 | 2 | ≥16 |
| 4 | 0 | 0 | 0 | 2 | ≥5 | 4 | — |
| 5 | 0 | 0 | 0 | 0 | 1 | 1 | — |
| 6 | 0 | 0 | 1 | 0 | 3 | — | — |
| 7 | 0 | 0 | 0 | 0 | 2 | — | — |

Full realized-count data, including zero and unresolved bands:
[JSON](../data/grothendieck_counts.json) · [CSV](../data/grothendieck_counts.csv).
The [fusion-ring-census repository](https://github.com/sebastienpalcoux/fusion-ring-census)
contains the separate table of **all fusion rings** and its enumerator;
[this repository's pinned census import](../data/counts.csv) supports the
classification cross-check. Rank-two realized counts follow directly from
`X² = 1+nX`: both categorifiable rings occur at multiplicity 1.

## Classification · what is decided?

These are the recorded outcomes of the current research program, subject to
the verification notice and [verification scope](../docs/PREPUBLICATION_REVIEW.md).
Census bounds describe enumeration coverage; classification scope is stated separately.

| Rank | Full census | General classification | Current conclusion |
|---:|---:|---:|---|
| 2 | Symbolic, all multiplicities | **Unrestricted theorem** | Exactly the rings `n = 0, 1` are realized. |
| 3 | Through 1,000 | **Unrestricted theorem** | Five realized rings: four at multiplicity 1 and one at 2; see the standalone sphericality and ring-classification proof. |
| 4 | Through 128 | **Unrestricted theorem** | Exactly 15 realized rings; every categorification is spherical; multiplicity at most 6. |
| 5 | Through 20 | **Complete through 20** | Through 20: 40,982 excluded, 17 realized, 0 unresolved. |
| 6 | Through 9 | **Complete through 3** | Through 9: 25,362 excluded, 57 realized, 2 unresolved. |
| 7 | Through 5 | **Complete through 5** | Through 5: 9,976 excluded, 30 realized, 0 unresolved. |
| 8 | Through 3 | **Complete through 2**; multiplicity 3 partial | Through 3: 4,402 excluded, 93 realized, 5 unresolved. |

The [rank-four unrestricted proof](../manuscripts/rank4/papers/companion.pdf) gives the sharp bound FPdim ≤ 24+12√3, attained only by the near-group ring `NG(C₃,6)`. Its theoretical reduction gives FPdim < 1000 and multiplicity at most 31; an independent exact census then checks 1,692 rings, with 1,677 exclusions and 15 models. The separate multiplicity-128 census contains 889,530 rings and 889,515 exclusions.

Related work on the pivotal case: Jingcheng Dong, Sébastien Palcoux and Arnaud Plessis, [Classifying Grothendieck rings of pivotal fusion categories of rank four](https://arxiv.org/abs/2609.33272), arXiv:2609.33272. Its hypothesis is pivotality.

Rank-six realization counts through multiplicity 9 split into **56 unitary
models** and **one spherical model whose ring has no pseudo-unitary
categorification**. “Realized” means that at least one categorification is
constructed; it does not assert that every categorification of that ring is
unitary. Rank five has no unresolved ring through multiplicity 20;
inert-prime parity and exact induction cover multiplicity 18.

The rank-six classification covers **25,421 fusion rings through multiplicity 9**:
**25,362 excluded, 57 realized and two unresolved**. All **8,809 rings of
exact multiplicity nine are generally excluded**.

The positive catalogue includes neutral module categories from
`(B2)_7 ⊂ (D7)_1`, `(C3)_4 ⊂ (B10)_1`, and `(B2)_12 ⊂ (E8)_1`,
with full tensor identifications.

The rank-six, multiplicity-seven ring `R6_7_2274` is realized by the known
Extended Haagerup category **EH1**. Its fusion rules are given in
P. Grossman, S. Morrison, D. Penneys, E. Peters and N. Snyder,
[*The Extended Haagerup fusion categories*](https://doi.org/10.24033/asens.2541),
*Ann. Sci. Éc. Norm. Supér.* (4) **56** (2023), no. 2, 589–664,
§2.1, p. 597 ([arXiv:1810.06076](https://arxiv.org/abs/1810.06076)).
The original construction is S. Bigelow, S. Morrison, E. Peters and N. Snyder,
[*Constructing the extended Haagerup planar algebra*](https://arxiv.org/abs/0909.4099),
*Acta Math.* **209** (2012), 29–82.

| Open ring | Necessary restrictions |
|---|---|
| `R6_4_155` | A unique rank-26 semion-centralizer modular candidate; a rank-22 based module passes all 234,256 fermion Azumaya linking identities. No coherent module category or categorification is constructed. |
| `R6_8_1660` | Relative-center and Morita restrictions, full twist-one support and saturated indicators including `nu_3(T)=2`. A rank-37 candidate fails Verlinde integrality; other profiles remain open. |

Every tensor functor from a hypothetical categorification of either ring to
a complex fusion category is fully faithful under the recorded theoretical
arguments. These necessary restrictions do not decide categorifiability.

[Manuscript](../manuscripts/rank6/papers/manuscript.pdf) ·
[Verification scope](../docs/PREPUBLICATION_REVIEW.md) ·
[Completion proofs](../supplements/rank6/research/exclusions/m9_completion/) ·
[Replay guide](../docs/VERIFY.md)


The [historical 38-case continuation](../docs/RESEARCH_STATUS.md) records **36 decisions among 38 cases**: 29 proposed general exclusions and 7 unitary constructions. Within that historical 38-case study, two questions remain open: `R6_4_155` and `R6_8_1660`. The combined residual program records 140 decisions (120 exclusions and 20 constructions), all subject to independent mathematical verification.
The [proof inventory](../docs/VERIFY.md) gives the replay paths.
Scope-specific obstructions retain their stated assumptions and do not change
a ring's general unresolved status.

### The classification boundary, band by band

| Multiplicity | Rank 4 | Rank 5 | Rank 6 | Rank 7 | Rank 8 |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 excluded · 9 realized | 6 excluded · 10 realized | 18 excluded · 21 realized | 30 excluded · 13 realized | 48 excluded · 48 realized |
| 2 | 14 excluded · 3 realized | 34 excluded · 3 realized | 132 excluded · 22 realized | 309 excluded · 10 realized | 848 excluded · 29 realized |
| 3 | 22 excluded · 2 realized | 80 excluded · 2 realized | 381 excluded · 3 realized | 1,057 excluded · 2 realized | 3,506 excluded · 16 realized · **5 open** |
| 4 | 45 excluded · 0 realized | 132 excluded · 2 realized | 866 excluded · 5 realized · **1 open** | 2,776 excluded · 4 realized | — |
| 5 | 55 excluded · 0 realized | 209 excluded · 0 realized | 1,581 excluded · 1 realized | 5,804 excluded · 1 realized | — |
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

Full decision bands: [JSON](../data/classification_status.json) ·
[CSV](../data/classification_status.csv). Statuses come from the attached
rank-four through rank-eight certificate ledgers; their SHA-256 hashes,
row checks and scope appear in [the provenance record](../docs/PROVENANCE.md).

### When did the current criterion repertoire stabilize?

| Rank | Last first use of a mathematical criterion family | Checked range afterward |
|---:|---:|---|
| 4 | Multiplicity 18 | The same criterion families suffice for the allocated exclusions at 19–128. |
| 5 | Multiplicity 18 | Inert-prime quadratic parity first closes two cases at 18; no new criterion family is needed at 19–20. |
| 6 | See the allocation ledger | The current criteria include stabilizer, cyclotomic-trace and signed arithmetic obstructions. All 8,809 exact-multiplicity-nine rings have general exclusion certificates; 2 earlier cases remain unresolved through multiplicity 9. |
| 7 | See the allocation ledger | The multiplicity-five extension adds cyclic-module, quadratic compression, signed sphericalization, center-trace and Morita-descent arguments. There are 0 generally open rings in the analyzed range. Higher multiplicities are not classified here. |
| 8 | Multiplicity 3 | Quadratic-compositum compression, convex central induction, split-module polynomials and Morita transport extend the classification through multiplicity three. There are 4 generally open rings in the analyzed range; higher multiplicities are not classified here. |

This records **first use in the chosen certificate allocation**, not an
optimal ordering theorem or a claim that the criteria settle higher
multiplicities. Rank-four nested signed cyclotomicity first succeeds at 95,
using a general cyclotomicity theorem already used at 9. The ordered
step-by-step exclusion tables and proof dependencies are in the manuscripts.

## Read the mathematics

The [manuscripts](../manuscripts/README.md) are kept as TeX/PDF pairs. The
classification programs proceed rank by rank: general necessary criteria,
exact automated applications, positive model matches, and explicit residual
frontiers. Ranks two, three and four have unrestricted classification
theorems. The rank-four article supplies the complete theoretical reduction
and exact finite verification. The papers and computation records remain research in
progress; [the evidence guide](../docs/VERIFY.md) identifies exactly what the
stored checks establish. Each manuscript states its current classification scope
and the remaining questions directly; [rank eight](../manuscripts/rank8/paper/rank8.pdf)
records exclusions, explicit unitary models and individually investigated unresolved candidates through multiplicity three.

## Structure

After cloning, restore the large datasets with one offline command:

```bash
python3 tools/restore_data.py
```

The repository stores those datasets as small compressed parts. The command
checks every part and reconstructed file against its released SHA-256 hash;
it requires only Python's standard library. See [verification instructions](../docs/VERIFY.md).

```text
data/         Pinned census matrix and classification-status tables
docs/         Provenance, terminology and verification paths
manuscripts/  Current TeX and PDF pairs
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

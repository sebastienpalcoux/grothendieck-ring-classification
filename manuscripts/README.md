# Manuscripts

The 23 October 2026 multiplicity-one release resolves all 142 rank-nine rings and 188 of the 194 rank-ten rings: **233 general exclusions, 97 unitary models and 6 deferred cases**. Rank nine has 102 exclusions and 40 models; rank ten has 131 exclusions, 57 models and 6 unresolved rings. The five active cases are now completed: R10_1_21, R9_1_12 and R9_1_108 have unitary models; R9_1_62 and R9_1_87 are excluded over the complex numbers. The six deferred rank-ten cases remain unchanged.

[Report](../evidence/rank9_rank10_m1_20261023/deliverable/report.pdf) · [Complete ledger](../evidence/rank9_rank10_m1_20261023/deliverable/ledger.csv) · [Proofs and exact verification](../evidence/rank9_rank10_m1_20261023/README.md) · [All 336 case records](https://sebastienpalcoux.github.io/grothendieck-ring-classification/rank9-10.html).

The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,507 general exclusions, 16 models and 4 unresolved cases. Every recorded model admits a unitary realization. The remaining rings retain unresolved status for general complex categorification.

The rank-seven multiplicity-five continuation addresses all 5,805 supplied exact-multiplicity-five rings: 5,804 general exclusions, 1 realization and 0 unresolved cases. The classification of the supplied census is complete through multiplicity 5. The new realization R7_5_5678 is Rep(AGL(1,7)).

> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.

Each paper is a current TeX/PDF pair with its classification scope stated in
its own text. Ranks two, three and four are unrestricted in multiplicity.
Ranks five to eight use pinned finite censuses and explicit criteria.

**Project overview:** [Five-page research announcement](../announcements/hexagon-2026-10/Low_rank_Grothendieck_rings_announcement.pdf), with the historical classification scope, seven construction candidates, and both rank-six open cases. This announcement is separate from the research-manuscript page count.

## Unrestricted rank-four classification · 88 pages

**[Read the main PDF](rank4/papers/companion.pdf)** ·
[LaTeX source](rank4/papers/companion.tex) ·
[Rank-four reading guide](rank4/README.md)

**No multiplicity bound; no initial pivotality assumption.** The main
rank-four manuscript gives the fifteen-ring classification over ℂ and proves
that every categorification admits a spherical structure. Its proof combines
a theoretical reduction with exact finite verification.

The 29-page finite-range classification companion treats the separate census
through multiplicity 128. The unrestricted manuscript is the primary account
of the general rank-four result.

Related work on the pivotal case: Jingcheng Dong, Sébastien Palcoux and Arnaud Plessis, [Classifying Grothendieck rings of pivotal fusion categories of rank four](https://arxiv.org/abs/2609.33272), arXiv:2609.33272. Its hypothesis is pivotality.

## All manuscripts

| Manuscript | Source | PDF | Pages | Scope |
|---|---|---|---:|---|
| Rank two | [TeX](rank2.tex) | [PDF](rank2.pdf) | 3 | Unrestricted over ℂ; two realized rings |
| Rank three | [TeX](rank3.tex) | [PDF](rank3.pdf) | 12 | Unrestricted sphericality and five-ring classification |
| **Rank four, unrestricted classification** | [TeX](rank4/papers/companion.tex) | [PDF](rank4/papers/companion.pdf) | 88 | **No multiplicity bound or initial pivotality assumption**; 15 rings and automatic sphericality |
| Rank four, finite-range companion | [TeX](rank4/papers/finite.tex) | [PDF](rank4/papers/finite.pdf) | 29 | Complete through multiplicity 128 |
| Rank four, verification guide | [TeX](rank4/papers/verification_guide.tex) | [PDF](rank4/papers/verification_guide.pdf) | 9 | Exact certificate checks |
| Rank five | [TeX](rank5/papers/manuscript.tex) | [PDF](rank5/papers/manuscript.pdf) | 19 | Complete through multiplicity 20 |
| Rank five, verification guide | [TeX](rank5/papers/verification_guide.tex) | [PDF](rank5/papers/verification_guide.pdf) | 4 | Exact certificates, models and replay scope |
| Rank six | [TeX](rank6/papers/manuscript.tex) | [PDF](rank6/papers/manuscript.pdf) | 170 | 25,362 exclusions, 57 realizations, two open through 9; complete through 3 and exact bands 1, 2, 3, 5, 6, 7, 9 |
| Rank six, verification guide | [TeX](rank6/papers/verification_guide.tex) | [PDF](rank6/papers/verification_guide.pdf) | 6 | Models, certificates and open-case reductions |
| Rank seven | [TeX](rank7/papers/manuscript.tex) | [PDF](rank7/papers/manuscript.pdf) | 83 | Through multiplicity 5: 9,976 exclusions, 30 models and 0 unresolved; complete through 5 |
| Rank eight | [TeX](rank8/paper/rank8.tex) | [PDF](rank8/paper/rank8.pdf) | 148 | Through multiplicity 3: 4,403 exclusions, 93 unitary models and 4 unresolved; complete through 2 |

The eight mathematical manuscripts contain **552 pages**.
Including the three verification guides gives **571 pages**;
including the 8-page [research-status report](prepublication-review-2026-10-22.pdf)
gives **579 pages** across twelve distinct documents.
These counts include references and appendices and count duplicate download
copies only once. The [page inventory](../data/manuscript_page_counts.json)
records every path, count and PDF checksum. The [17 October status report](prepublication-review-2026-10-17.pdf) is retained as a historical snapshot and is not counted as a current document.

Download the [open fusion tensors as Python lists](../data/remaining_cases.py).
The file names each case and states the zero-based convention `N[i][j][k]`,
unit index, duality map and canonical source checksums.


The sources use sections and generated tables in their sibling directories.
The [document manifest](../data/current_document_revision.json) binds all
current papers and their website copies.

The [historical 38-case continuation](../docs/RESEARCH_STATUS.md) records **36 decisions among 38 cases**: 29 proposed general exclusions and 7 unitary constructions. Within that historical 38-case study, two questions remain open: `R6_4_155` and `R6_8_1660`. The historical residual program before the rank-eight M3 extensions records 140 decisions (120 exclusions and 20 constructions), all subject to independent mathematical verification.

The rank-six treatment includes conformal-embedding constructions, fermion
Azumaya compatibility, odd cyclic Clifford constraints and fully-faithful
tensor-functor restrictions. For the positive spherical representative of
`R6_8_1660`, all indicator sequences and central phase masses are determined,
and 640 labelled restriction-data
profiles remain in branches 68, 286, 286. These profiles and the rank-22
based-module witness are necessary-condition evidence. Both rank-six
categorification questions remain open.

Read the [research status](../docs/RESEARCH_STATUS.md),
[verification scope](../docs/PREPUBLICATION_REVIEW.md) and
[replay guide](../docs/VERIFY.md) with the papers.

## Generalized Haagerup construction and further restrictions

R8_3_721 is realized by the inherited 1+rho Q-system Morita dual of the C2 de-equivariantization of GH(C8). Exact rank and coefficient bounds identify its unique dimension type in the supplied complete rank-eight multiplicity-at-most-three census. The earlier center-action analysis leaves three necessary R8_3_1154 patterns. These results are in evidence/rank8_next_20261021/; the later R8_3_65 general exclusion is in evidence/rank8_research_20261022/.

The integrated rank-eight article includes the new construction and restrictions. Categorical arguments, targeted mathematical replay receipts and independent reconstructions are in `evidence/rank8_next_20261021/`. The original frontier ledger, audit and completed replay receipts remain unchanged.

The following commands validate the accepted overlay metadata; they do not repeat the targeted mathematical checks:

```bash
python3 tools/rank8_next.py --check
python3 -O tools/rank8_next.py --check
```

A separately reviewed Galois follow-up reduces the 36 retained R8_3_1154 pair histograms to 25 across the same three center patterns. Its proof and exact replay are in `evidence/rank8_postpublication_20261021/r1154_galois_review/`; the ring remains unresolved.

## General exclusion of R8_3_3472

R8_3_3472 admits no fusion categorification over the complex numbers. The sphericalization and Galois reduction covers general complex categories; complete center-frame and twist-orbit domains reduce the remaining case to 628 exact equations in 572 integer variables. A certificate of 1648 rational bound deductions and a final strictly positive separating gap proves infeasibility, with two independent exact checkers. The proof and reproducible certificate are in evidence/r3472_exclusion_20261022/. This complete obstruction supersedes the earlier feasible necessary systems and conditional Morita restrictions for R3472. R8_3_982 remains unitarily realized by the neutral triality component of the exceptional E21 chiral fusion category, with all 512 canonical fusion coefficients identified exactly. Four rank-eight general categorification questions remain: R8_3_928, R8_3_941, R8_3_1154 and R8_3_1768. Every hypothetical categorification of these four rings admits a spherical structure and has a pseudo-unitary Galois conjugate; none has a braided Morita representative. The R928 phase refinement leaves four of ten necessary center patterns, all fourteen R941 allocations survive the stated refinements, and R1154 retains its forced semionic data. R1768 has 39 of 40 necessary Gram/indicator branches excluded, while its final cone survives. These necessary data do not construct categories or settle the four remaining questions.

The complete center-domain reduction and exact infeasibility certificates are in `evidence/r3472_exclusion_20261022/README.md`. This accepted decision removes R8_3_3472 from the unresolved ledger. The earlier E21 construction and its research receipts retain their historical scope.

```bash
python3 tools/verify_rank8_exclusion_20261022.py
python3 -O tools/verify_rank8_exclusion_20261022.py
```

Use `--metadata-only` to check source identities and completed replay receipts. Use `--historical` to replay the preceding rank-eight stages in their preserved contexts. That replay explicitly records the reconstructed helper missing from the creative archive and its four revised cache-state diagnostics in a separate checkpoint; it also restores the omitted canonical tensor with its original receipt hash. The current ledger and proof have separate bindings from those historical releases.

# Manuscripts

The rank-seven multiplicity-five continuation addresses all 5,805 exact-multiplicity-five rings: 5,802 general exclusions, 1 realization and 2 unresolved cases. The classification is complete through multiplicity 4. The new realization R7_5_5678 is Rep(AGL(1,7)). The unresolved records remain open for general complex categorification.

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
| Rank seven | [TeX](rank7/papers/manuscript.tex) | [PDF](rank7/papers/manuscript.pdf) | 77 | Through multiplicity 5: 9,974 exclusions, 30 models and 2 unresolved; complete through 4 |
| Rank eight | [TeX](rank8/paper/rank8.tex) | [PDF](rank8/paper/rank8.pdf) | 61 | Complete through multiplicity 2: 896 exclusions and 77 models |

The eight mathematical manuscripts contain **459 pages**.
Including the three verification guides gives **478 pages**;
including the 5-page [research-status report](prepublication-review-2026-10-20.pdf)
gives **483 pages** across twelve distinct documents.
These counts include references and appendices and count duplicate download
copies only once. The [page inventory](../data/manuscript_page_counts.json)
records every path, count and PDF checksum. The [17 October status report](prepublication-review-2026-10-17.pdf) is retained as a historical snapshot and is not counted as a current document.

Download the [open fusion tensors as Python lists](../data/remaining_cases.py).
The file names each case and states the zero-based convention `N[i][j][k]`,
unit index, duality map and canonical source checksums.


The sources use sections and generated tables in their sibling directories.
The [document manifest](../data/current_document_revision.json) binds all
current papers and their website copies.

The [historical 38-case continuation](../docs/RESEARCH_STATUS.md) records **36 decisions among 38 cases**: 29 proposed general exclusions and 7 unitary constructions. Within that historical 38-case study, two questions remain open: `R6_4_155` and `R6_8_1660`. The combined residual program records 140 decisions (120 exclusions and 20 constructions), all subject to independent mathematical verification.

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

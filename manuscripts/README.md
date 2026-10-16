# Manuscripts

> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.

Each paper is a current TeX/PDF pair with its classification scope stated in
its own text. Ranks two, three and four are unrestricted. The rank-four
companion proves the complete fifteen-ring classification and sphericality
without a multiplicity or pivotality hypothesis. The finite article supplies
the separate classification through multiplicity 128.
Ranks five to eight use pinned finite censuses and explicit criteria.

Related work on the pivotal case: Jingcheng Dong, Sébastien Palcoux and Arnaud Plessis, [Classifying Grothendieck rings of pivotal fusion categories of rank four](https://arxiv.org/abs/2609.33272), arXiv:2609.33272. Its hypothesis is pivotality.

| Manuscript | Source | PDF | Pages | Scope |
|---|---|---|---:|---|
| Rank two | [TeX](rank2.tex) | [PDF](rank2.pdf) | 3 | Unrestricted over ℂ; two realized rings |
| Rank three | [TeX](rank3.tex) | [PDF](rank3.pdf) | 12 | Unrestricted sphericality and five-ring classification |
| Rank four, finite range | [TeX](rank4/papers/finite.tex) | [PDF](rank4/papers/finite.pdf) | 29 | Complete through multiplicity 128 |
| Rank four, unrestricted classification | [TeX](rank4/papers/companion.tex) | [PDF](rank4/papers/companion.pdf) | 88 | Unrestricted over ℂ; 15 rings and automatic sphericality |
| Rank four, verification guide | [TeX](rank4/papers/verification_guide.tex) | [PDF](rank4/papers/verification_guide.pdf) | 9 | Exact certificate checks |
| Rank five | [TeX](rank5/papers/manuscript.tex) | [PDF](rank5/papers/manuscript.pdf) | 19 | Complete through multiplicity 20 |
| Rank five, verification guide | [TeX](rank5/papers/verification_guide.tex) | [PDF](rank5/papers/verification_guide.pdf) | 4 | Exact certificates, models and replay scope |
| Rank six | [TeX](rank6/papers/manuscript.tex) | [PDF](rank6/papers/manuscript.pdf) | 165 | 25,362 exclusions, 57 realizations, two open through 9; complete through 3 and exact bands 1, 2, 3, 5, 6, 7, 9 |
| Rank six, verification guide | [TeX](rank6/papers/verification_guide.tex) | [PDF](rank6/papers/verification_guide.pdf) | 5 | Models, certificates and open-case reductions |
| Rank seven | [TeX](rank7/papers/manuscript.tex) | [PDF](rank7/papers/manuscript.pdf) | 56 | Complete through multiplicity 4: 4,172 exclusions and 29 models |
| Rank eight | [TeX](rank8/paper/rank8.tex) | [PDF](rank8/paper/rank8.pdf) | 58 | Complete through multiplicity 1; partial at 2: 895 exclusions, 77 models and one open case |

The eight mathematical manuscripts contain **430 pages**.
Including the three verification guides gives **448 pages**;
including the 4-page [research-status report](prepublication-review-2026-10-17.pdf)
gives **452 pages** across twelve distinct documents.
These counts include references and appendices and count duplicate download
copies only once. The [page inventory](../data/manuscript_page_counts.json)
records every path, count and PDF checksum.

Download the [three open fusion tensors as Python lists](../data/remaining_cases.py).
The file names each case and states the zero-based convention `N[i][j][k]`,
unit index, duality map and canonical source checksums.


The sources use sections and generated tables in their sibling directories.
The [document manifest](../data/current_document_revision.json) binds all
current papers and their website copies.

The [current research account](../docs/RESEARCH_STATUS.md) records **35 decisions among 38 cases**: 28 proposed general exclusions and 7 unitary constructions. Three general questions remain open: `R6_4_155`, `R6_8_1660` and `R8_2_24`. The combined residual program records 139 decisions (119 exclusions and 20 constructions), all subject to independent mathematical verification.

The rank-six treatment includes conformal-embedding constructions, the
fermion Azumaya compatibility test, saturated third indicators and
fully-faithful tensor-functor constraints. The rank-22 based-module witness
and modular-data candidates are necessary-condition evidence, not categorical
constructions. A rank-37 candidate for the second residual fails an exact
Verlinde integrality test; other profiles remain open.

Read the [research status](../docs/RESEARCH_STATUS.md),
[verification scope](../docs/PREPUBLICATION_REVIEW.md) and
[replay guide](../docs/VERIFY.md) with the papers.

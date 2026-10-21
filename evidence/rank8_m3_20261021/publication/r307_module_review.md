# R8_3_307: the Rep(A5) module-rank obstruction

The argument concerns arbitrary complex fusion categories. No pivotal, braided, spherical, or unitary assumption is imposed.

The exact source tensor has SHA-256 `8c1cad1664a341585edcd1b998161fb8b47264e8ba90d6db78cf94159b8bd0cc`. Its positive dimension character is
`(1,sqrt(10),sqrt(10),2sqrt(10),5,3,3,4)`, of total dimension120. The integral basis `{0,4,5,6,7}` has dimension60 and is the neutral component of a faithful C2 grading; the odd component has basis `{1,2,3}`. The neutral based ring has no proper nontrivial closed based subset. Thus a hypothetical neutral fusion category D is simple, integral, and of dimension60. By Etingof–Nikshych–Ostrik, *Weakly group-theoretical and solvable fusion categories*, arXiv:0809.3031v2, Theorem9.12, D is tensor equivalent to Rep(A5).

The odd component is an invertible D-bimodule category. In particular it is an indecomposable Rep(A5)-module category, and its dual category must be D again. Such module categories are classified by subgroups H≤A5 and projective representation multipliers ψ: Ostrik, *Module categories, weak Hopf algebras and modular invariants*, arXiv:math/0111139, Theorem2 and Remark12. Its simple objects are the irreducible ψ-projective representations of H.

The action matrices on the odd basis have a one-dimensional simultaneous positive dimension eigenspace with primitive vector `(1,1,2)`. The verifier checks both the eigenvector equations and rank2 of their combined coefficient matrix; therefore the projective degrees have the form `a(1,1,2)` with a positive integer a. Their squared sum is |H|=6a², and |H| divides60. Hence a=1 and |H|=6. A one-dimensional projective representation trivializes ψ. The three ordinary irreducibles have degrees1,1,2, so H is S3. Every order-six subgroup of A5 is conjugate to the normalizer of a three-cycle subgroup.

The dual of Rep(H) as a Rep(A5)-module is the category of H-biequivariant vector bundles on A5. Its rank is the sum of the numbers of irreducible representations of H∩gHg⁻¹ over H-double cosets. The three double cosets have sizes6,18,36 and stabilizers S3,C2,1. The dual rank is therefore3+2+1=6. But D has rank5. This contradiction excludes the source tensor.

## Exact replay scope

`r307_module_review.py` recomputes all dimension identities, the faithful grading, neutral simplicity, uniqueness and normalization of the module eigenvector, every order-six subgroup embedding via Sylow normalizers, and every double-coset stabilizer. It uses explicit integer/rational arithmetic and no assertion statements. The adjacent JSON is a source-bound premise certificate. These finite checks accompany the categorical theorems cited above; they are not a formal proof of those theorems.

This verifier was regenerated after an ephemeral-workspace loss. Its normal and optimized runs were freshly executed; no lost receipt was reconstructed from memory. Independent human review remains pending.

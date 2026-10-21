# Dimension-sixty Morita transport and R8_3_2132

This is a new application and unification of the existing dimension-sixty solvability dichotomy and the manuscript's square-kernels integrality principle. The proof strengthens the intermediate conclusion: the transported graded category is pointed. It concerns general complex fusion categories, without a pivotality or braiding assumption.

## Source and nonsolvability

R8_3_2132 has exact tensor SHA-256 `98c9fb73edbd05a2a38222776e7cc4912954bff817611ac5c3bd8ece1c83cd61` and positive dimensions
`(1,1,sqrt(30),5,5,sqrt(30),2,2)`.
The integral neutral basis `{0,1,3,4,6,7}` has dimension60, equals its adjoint subcategory, and has precisely two invertibles. The complement `{2,5}` is the odd component of a faithful C2 grading.

Suppose the neutral category D were solvable. In its description by cyclic-prime extensions and equivariantizations, the last step cannot be an extension because D_ad=D. It must be an equivariantization by Cp, and p divides the number2 of invertibles. Thus p=2. This uses ENO, arXiv:0809.3031v2, Definition1.2 and Proposition4.4. The nontrivial sign object must be the unique nontrivial invertible g. Its multiplication permutation on the full source basis is `(1,0,5,4,3,2,6,7)`.

In a C2-equivariantization, a fixed underlying simple yields two equivariant simples interchanged by the sign character; a free underlying orbit yields one sign-fixed equivariant simple of twice the underlying dimension. The neutral sign orbits are `{0,1}`, `{3,4}`, `{6}`, `{7}`. Consequently the de-equivariantization has dimensions `1,1,1,1,1,5`, hence the near-group ring NG(C5,4). Its entire canonical tensor is matched to the already published general negative R6_4_19, whose dimension-thirty Morita certificate permits only simple dimensions1 and2. Thus D is not solvable. Equivalently, the existing dimension-sixty argument uses the same dimension-thirty bound to rule out a last C2-equivariantization when D has a simple of dimension greater than4.

## Pointed Morita representative

By ENO Theorem9.16 every dimension60 fusion category is weakly group-theoretical. Hence D is Morita equivalent to a nilpotent category T, obtained from Vec by a tower of faithful finite-group extensions. The extension-group orders multiply to60. If every group in the tower were solvable, T and hence D would be solvable (ENO Proposition4.5 and Morita invariance). A nonsolvable factor must therefore occur. Every group whose order is a proper divisor of60 is solvable, and the only nonsolvable group of order60 is A5. Thus the tower has a single nontrivial factor of order60 and T is Vec_(A5)^ω for some associator ω. No triviality assumption on ω is made.

## Transport of the full extension

ENO Lemma3.4 transports the full graded category under Morita equivalence of its neutral component. Equivalently, choose the connected separable neutral algebra giving the Morita equivalence and take its bimodules in the whole graded category. This gives a faithfully graded category C' Morita equivalent to the original C, with neutral component Vec_(A5)^ω.

Each graded component is an invertible bimodule over the neutral category. Viewed as a one-sided module category, its dual is pointed. Naidu, *Categorical Morita equivalence for group-theoretical categories*, arXiv:math/0605530, Theorem3.4, applies for arbitrary ω and implies that the subgroup H defining this module category is abelian and normal in A5. The only such subgroup is1. Consequently every component has60 simple objects. Every graded component also has Frobenius–Perron dimension60; since every simple dimension is at least1, all these objects are invertible. Thus C' is pointed.

The original C is therefore group-theoretical and integral. Its source ring has odd dimensions sqrt(30), a contradiction. This excludes R8_3_2132 generally. The same transport argument applies to any finite-group extension of a nonsolvable dimension60 neutral category that is Morita equivalent to Vec_(A5)^ω.

## Exact replay scope

`r2132_morita_extension.py` recomputes the source dimension equations, grading, adjoint closure, invertible action, forced de-equivariantization dimensions, full near-group identification with R6_4_19, and A5's absence of nontrivial proper normal subgroups by explicit conjugacy classes and their normal closures. The prior negative decision and tensor hashes are recorded. It does not claim that a Grothendieck-ring match identifies an arbitrary categorification with Rep(A5), nor that ω=1.

The source was regenerated after an ephemeral-workspace loss and freshly checked in normal and optimized Python. Lost receipts were not reconstructed from memory. Independent human review remains pending.

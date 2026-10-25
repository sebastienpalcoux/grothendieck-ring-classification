# Independent unitarizability support for the three rank-seven AnyonWiki models

Audit supplement, 2026-10-25. This closes the categorical unitarity assurance issue in R7-A2 of `rank7.md`; it does not claim that the supplied F-symbol gauges are orthonormal.

The exact associator replay already verifies complex fusion-category existence for R7_1_19, R7_1_28 and R7_1_36: 64,773 pentagon equations, 2,007 invertible blocks, and the unit/rigidity constraints (`rank7-anyon-pentagons.json`). The construction therefore does not depend only on an AnyonWiki category-status flag.

## Independent theorem route

The new explicit-guard script `rank7-anyon-dimension-unitarity.py` checked the following positive dimension characters directly on all 49 products of each actual model tensor, and computed their sums of squares exactly. It passed under normal and optimized Python.

| Census ID | Positive FP dimension vector in the supplied model basis | Global FP dimension |
|---|---|---:|
| R7_1_19 | 1, 1, 1, 1, 2, 2, 2 | 16 |
| R7_1_28 | 1, 1, 2, 2, 2, sqrt(7), sqrt(7) | 28 |
| R7_1_36 | 1, 1, 1, 1, 2, 2, 2 | 16 |

For a fusion ring, a positive normalized dimension character is the Frobenius–Perron character. Consequently every complex fusion category realizing these particular tensors has the indicated total FP dimension.

1. Etingof–Nikshych–Ostrik, *Weakly group-theoretical and solvable fusion categories*, [arXiv:0809.3031v2](https://arxiv.org/pdf/0809.3031), **Theorem 1.6, p.2**, applies to any complex fusion category whose total FP dimension has at most two prime divisors: it is solvable. There is no assumption that every simple dimension is integral. Definitions 1.1–1.2, p.1, imply that solvable categories are weakly group-theoretical. Here the dimensions are 2^4 and 2^2·7.
2. Galindo–Hong–Rowell, *Generalized and quasi-localizations of braid group representations*, [author PDF](https://people.tamu.edu/~rowell/GHRarx1.pdf) ([arXiv:1105.5048](https://arxiv.org/abs/1105.5048)), **Theorem 5.20, p.23**, gives complete unitarity for every weakly group-theoretical fusion category. **Definition 5.13(1), p.21**, explicitly includes monoidal equivalence to a unitary fusion category. This does not assume the input category was already unitary or braided. I read the definition, theorem and its nilpotent/Morita reduction; the theorem is used as a primary literature input rather than re-proved here.

Thus the actual complex categories whose F-symbols were independently checked are unitarizable. In particular all three based rings admit unitary categorifications. The statement is stronger than inferring unitarity from a matching dimension vector alone: exact existence is established first, and the dimension theorems are then applied to those existing categories.

For the two dimension-16 rings the script also computes terminating adjoint chains of ranks 7→5→4→1, so their nilpotence gives a direct route to GHR without ENO's solvability theorem. The dimension-28 ring does not require this stronger nilpotence property.

## Correct scope of the earlier gauge experiment

The identity-Hermitian-form tests in `rank7-anyon-unitarity.json` remain unchanged and valid. They show that the particular supplied F matrices are not all unitary in those coordinates. Gauge changes in a unitary category need not preserve an identity Gram matrix, so that experiment never refuted unitary categorifiability. The newly checked theorem route now supplies independent support for the unitary existence claims. The only remaining limitation here is that this audit does not construct the positive Hermitian forms or an orthonormal gauge explicitly.

Recommended wording: “Exact associator certificates establish these three fusion categories; their FP dimensions 16, 28 and 16 imply unitarizability by ENO Theorem 1.6 and GHR Theorem 5.20. The supplied gauge is not asserted to be orthonormal.” No model-status downgrade is warranted.

# Review of the remaining noncommutative scope gates

Accepted conclusion: every complex categorification of R8_3_439,
R8_3_455 or R8_3_567 admits a spherical structure and has a pseudo-unitary
Galois conjugate. This does not establish existence, nonexistence or
unitarity. Together with the earlier four reviewed noncommutative gates,
it supplies the same general scope reduction for all seven remaining
noncommutative rows of the original frontier after R436's exclusion.
This is separate AI review, not human or proof-assistant review.

The canonical calculation exhausts all parity-compatible signed tensors
using ordered associativity, without positive-indicator normalization or
commutativity assumptions. The reviewer inspected the final source and
freshly replayed it with Python optimization; all three gates passed.

| Ring | Search nodes | Signed tensors | Gauge-original | Nongauge excluded |
|---|---:|---:|---:|---:|
| R8_3_439 | 3,455 | 256 | 64 | 192 |
| R8_3_455 | 1,119 | 32 | 32 | 0 |
| R8_3_567 | 439 | 64 | 32 | 32 |

For every ordinary algebra and every signed gauge-class representative,
the rational regular-projector audit checks star closure, the complete
four-dimensional commutator kernel, invariant complementary projectors,
both four-dimensional block algebras, scalar separability and all scalar
multiplication identities. It computes the center inside the complementary
algebra and obtains dimension one. Thus after complex extension the full
algebra is C^4 plus M2(C), with no omitted scalar character. The matrix
Casimir is accounted for with its representation dimension two; the
ordinary matrix formal codegree is 3. Signed codegrees are recomputed.

The new obstruction needed for 439 and 567 is a valid dimension-field
consequence of Ostrik's induced-unit theorem, arXiv:1309.4822, Theorem
2.13. If K contains every spherical simple dimension, the dimension of
any central simple belongs to K: the forgetful functor expresses it as
an integer linear combination of those dimensions. In sphericalization,
the ordinary-sector formal codegree is 2f and the global dimension is
2delta, so its corresponding distinguished central simple has dimension
delta/f. As delta is nonzero and lies in K, necessarily f lies in K.
This argument uses neither pseudo-unitarity nor a spherical structure on
the original hypothetical category.

In each of the two residual branches, the code verifies all simple
dimensions are rational, delta=24, and an ordinary-sector formal codegree
has the irreducible polynomial t^2-96t+576. Hence K=Q cannot contain f.
The required polynomial is checked against the original algebra's formal
codegrees, not merely the combined signed/original list. This excludes
the branch even though its norm integrality test alone is inconclusive.

All remaining signed tensors are gauge-original, giving spherical
sections. The ordinary character check leaves exactly the FP Galois orbit:
439's other orbit fails a norm condition, 567's other orbit fails dual
dimension equality, and 455 has only its quartic FP scalar orbit. The
previously reviewed Galois transport then yields the stated scope gates.

The computation explicitly shares the frozen ordered-associativity
generator and scalar arithmetic with the preceding unrestricted reviews.
The rational projector checks independently certify the full block
accounting; no claim is made that every primitive was reimplemented.

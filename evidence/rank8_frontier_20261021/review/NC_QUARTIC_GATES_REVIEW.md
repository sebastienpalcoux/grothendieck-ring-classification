# Review of the quartic noncommutative scope gates

Accepted conclusion: every complex fusion categorification of R8_3_928
or R8_3_941 admits a spherical structure and has a pseudo-unitary Galois
conjugate. This is a reduction of scope for subsequent obstructions. It
does not exclude or construct either category, and does not establish
unitarity. This is separate AI mathematical and computational review,
not human review or a proof-assistant formalization.

The unrestricted sphericalization argument and its noncommutative
applicability are reviewed in `NC_GALOIS_PU_REVIEW.md`. The new canonical
producer applies the same complete parity-domain enumerator, with all
ordered associativity equations and no positive-indicator normalization.
The final producer was freshly replayed with Python optimization by the
reviewer, including the added signed-block audit, and passed.

| Ring | Complete signed tensors | Search nodes | Gauge-original class | Nongauge class |
|---|---:|---:|---:|---:|
| R8_3_928 | 32 | 30,367 | 16 | 16 |
| R8_3_941 | 128 | 1,011,903 | 64 | 64 |

For each ring, the nongauge class has one irreducible quartic scalar
component. The global-dimension polynomial has constant term 278528,
whereas an ordinary formal-codegree polynomial, also of degree four,
has constant term 147456. Thus their absolute norm ratio is 17/9. In
every common number field containing the putative dimension delta and
formal codegree f, the norm of delta/f is a positive integer power of
17/9, and cannot be an integer. The sphericalization induced-unit
condition requires delta/f to be integral: its dimension and the two
sector formal codegrees are both doubled, so those factors cancel.
This rejects the entire nongauge scalar orbit. Arbitrary dual-compatible
sign gauges preserve this obstruction; class reduction is performed
only after the complete enumeration.

Each surviving tensor is gauge-original. Switching the simple lifts
then makes their negative multiplicities vanish, and the selected lifts
form a spherical fusion subcategory equivalent to the original category.
The ordinary scalar characters form a single irreducible quartic orbit,
and the everywhere positive member is verified to be the FP character.
A field conjugation carrying the spherical dimension character to that
embedding yields a pseudo-unitary conjugate.

## Complete scalar and matrix accounting

The independent ordinary audit constructs all five central idempotents
from the four scalar characters and the matrix trace character. It
checks their pairwise products, centrality, sum one, and regular ranks
1,1,1,1,4. The center has dimension five, and the full trace-character
orthogonality identities are checked. These identities certify the full
complex algebra C^4 plus M2(C), so no scalar dimension character is
omitted. The matrix block is not a dimension character, but is retained
for every formal-codegree condition; its formal codegree is 4.

The final added signed audit does not assume positivity or that the
signed quartic field is Galois. It independently forms the rational
common kernel of all regular commutators and its orthogonal projector P.
The code verifies that P and its complement Q commute with every regular
matrix and have ranks four. The scalar block algebra has dimension four
and is the verified irreducible separable quartic field; all its scalar
multiplication identities are checked in that field. Its four complex
embeddings therefore exhaust its scalar characters.

The complementary algebra has dimension four. The code computes its
center inside the span of its own multiplication matrices, rather than
computing their full commutant, and obtains dimension one. Regular star
closure ensures semisimplicity. These exact linear-algebra dimensions
persist after complex scalar extension, so the complement is M2(C).
The identity Q C = 8 Q for the regular Casimir gives matrix formal
codegree 8/2 = 4. This independently resolves the possible missing-block
issue in the signed calculation as well.

The final read-only replay command was:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -O evidence/rank8_frontier_20261021/noncommutative_followup/verify_scope_gates.py
```

The calculation shares the frozen ordered-associativity generator and
exact scalar arithmetic with the previously reviewed unrestricted gate.
Its new projector checks are additional independent algebraic accounting,
not a claim that every underlying algorithm was rewritten independently.
The theorem inputs remain Ostrik, arXiv:1309.4822, Theorem 2.13,
Corollary 2.14 and Section 5.1, and Etingof--Nikshych--Ostrik,
arXiv:math/0203060, canonical sphericalization and number-field
definability, as cited in the earlier review.

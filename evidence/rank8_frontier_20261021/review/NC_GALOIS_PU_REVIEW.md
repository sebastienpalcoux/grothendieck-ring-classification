# Noncommutative sphericalization and Galois-PU gate review

Accepted conclusion: every complex categorification of R8_3_721 or
R8_3_1154 is spherical and has a pseudo-unitary Galois conjugate. This
statement does not construct or exclude either category and does not
establish unitarity. It permits a later complete pseudo-unitary
nonexistence proof to exclude general complex categorification.
This is separate AI review, not human or formal proof-assistant review.

## Noncommutative applicability

A spherical dimension function is an algebra homomorphism to C, regardless
of whether the fusion algebra is commutative. The common kernel of all
regular commutators is exactly the sum of the one-dimensional Wedderburn
blocks: on a matrix block of size greater than one the commutators have
zero common kernel. The frozen scalar sieve verifies invariance, dimension,
commutativity of the restricted operators, a square-free separating
polynomial, and every character multiplication identity. Hence it
exhausts all possible scalar dimension functions. A matrix trace of a
two-dimensional irreducible representation is not an extra scalar
dimension function and is correctly omitted from that list.

The matrix block is correctly retained for formal-codegree conditions.
Its four-dimensional regular summand has Casimir eigenvalue 2f, so its
formal codegree is f, not 2f. In sphericalization the two sign sectors
have doubled formal codegrees, while total categorical dimension is
2delta. Ostrik's induced-unit theorem thus gives the necessary integral
quotients delta/f for every representation in both sectors. The exact
norm-divisibility inequalities apply without pseudo-unitarity.

A dual-compatible sign gauge of the original tensor really implies a
spherical structure on the original category. Switching its lifts makes
the signed tensor equal to N. The sum and difference of the two lift
multiplicities are both N, so all opposite-lift multiplicities vanish.
The chosen lifts form a full fusion subcategory of sphericalization,
and the forgetful functor on it is bijective on simples and fully
faithful, hence a tensor equivalence. This argument does not require
commutativity.

The ordinary scalar check leaves precisely one irreducible character
factor, identified with the FP orbit by exact positivity. Transporting
the spherical structure through the corresponding field conjugation
gives a category with positive FP simple dimensions. This proves the
Galois pseudo-unitary conclusion. Definability over an algebraic number
field follows from fusion-category rigidity; a chosen spherical structure
can be retained over an algebraic extension through its finite algebraic
structure equations.

## Larger independent signed enumeration

The producer's normalized enumeration was freshly replayed with Python
optimization: four signed tensors for 721 and sixteen for 1154, all
necessary branches checked. The reviewer additionally ran
`verify_nc_gate_unrestricted.py`, which expands every native variable
domain to its entire parity interval. It imposes no positive-indicator
or modulo-four normalization. It uses all the frozen ordered associativity
equations and only cyclic/dual-reflection coefficient orbits. The larger
domains have the same maximum absolute coefficient, so the explicit
native overflow bounds remain valid. Every emitted tensor is validated
again against all ordered tensor identities.

| Ring | Full signed tensors | Search nodes | Sign-gauge classes | Gauge-original tensors |
|---|---:|---:|---:|---:|
| R8_3_721 | 64 | 6,871 | 1 | 64 |
| R8_3_1154 | 288 | 7,340,655 | 6 | 64 |

For 1154 the other five classes have sizes 64,64,32,32,32. Their complete
scalar components give ten exact norm obstructions and three zero-dimension
obstructions. The class reduction is valid under arbitrary dual-compatible
basis signs: scalar characters correspond, zero dimensions remain zero,
the global-dimension expression is unchanged, and the Casimir/formal
codegrees are unchanged. Every class representative is independently
checked. For 721 both ordinary rational characters have a zero dimension;
for 1154 one has a zero dimension and the other a 3-adic norm failure. In
each case only the ordinary FP quadratic orbit survives.

The unrestricted optimized replay passed, with source-bound report
`nc_gate_unrestricted.json`. It proves the same scope reduction without
using the positive-indicator normalization theorem. It still explicitly
shares the frozen ordered-associativity generator and exact scalar
character arithmetic; it is not claimed as a complete independent
implementation of those algorithms.

Primary sources independently consulted:

- https://arxiv.org/pdf/1309.4822, Theorem 2.13, Corollary 2.14, Section 5.1.
- https://arxiv.org/pdf/math/0203060, rigidity/definability following
  Theorem 2.30 and the pseudo-unitary discussion in Section 8.4.

The unrestricted computation requires neither a pivotality conjecture nor
an assumption that an integral or pseudo-unitary category is unitary.

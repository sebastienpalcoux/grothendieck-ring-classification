# Independent review of the four general sphericality reductions

**Accepted conclusion.** Every complex categorification of R8_3_982,
R8_3_1768, R8_3_1795, or R8_3_3472 admits a spherical structure and has a
pseudo-unitary Galois conjugate. The spherical structure belongs to the original
category; pseudo-unitarity may require conjugation. The gate alone supplies
neither a model nor a general categorification exclusion.

This review covers the categorical assumptions, the coefficient-domain
normalizations, the scalar-character obstruction, a complete optimized replay,
and an additional direct integer check that imports no producer routines.
It is a separate mathematical/computational review, not human peer review or a
proof-assistant formalization.

## Categorical assumptions checked against primary sources

Ostrik, [arXiv:1309.4822](https://arxiv.org/abs/1309.4822), §5.1(a), explicitly
establishes that both sphericalization lifts of a selfdual simple are selfdual.
One can also see this without a positivity assumption: the opposite lifts have
opposite nonzero spherical dimensions, whereas dual objects have equal
dimensions. Thus a lift cannot have its opposite as dual.

The sphericalization has a central sign object of dimension -1. Switching a
selfdual lift changes its pivotal isomorphism from `alpha` to `-alpha`. The
second-indicator rotation changes sign, as its definition contains
`alpha^(-1)` once. Therefore exactly one lift has second indicator +1. The
positive unit lift already has that indicator.

The needed parity theorem is Liu–Palcoux–Ren–Vercleyen,
[arXiv:2203.06522v5](https://arxiv.org/abs/2203.06522v5), Theorem 3.9; the
indicator convention is in Definition 2.14 and Lemma 2.16. The theorem assumes
a **pivotal fusion category**, a simple selfdual target `Y`, and odd
multiplicity of `Y` in `X* tensor X`. It has no pseudo-unitarity or braiding
hypothesis. Applying its contrapositive to the negative lift gives an even
negative multiplicity. Consequently `N[j*,j,i]-T[j*,j,i]` is divisible by four
for each selfdual `i`. Replacing `j` by `j*` justifies the ordered convention
`N[j,j*,i]-T[j,j*,i]` used in the program. No commutation of objects is needed.

These observations validate the R3472 FS normalization for a completely general
original category. They do not assume that category is already pivotal.

When a dual-compatible sign choice makes `T=N`, all opposite-lift
multiplicities vanish. The chosen lifts form a spherical fusion subcategory
mapping equivalently onto the original category. This is also the criterion
in Ostrik §5.1(c). It gives sphericality, not merely pivotality.

## Enumeration and domain coverage

I inspected `oriented_signed.problem` and the new verifier. The generator
retains each nonzero cyclic/dual-reversal coefficient orbit as a symbolic
variable and forms all ordered associativity equations. Its original FS
domains affect the DFS loops, ordering heuristic, and coefficient-range bound;
they do not simplify the equations or eliminate variables. Thus replacing
every loop domain restores the complete parity domain. The verifier checks
every replacement and checks that maximum absolute values do not increase.

For R982, R1768, and R1795 the additional positive constraints concern only
nonzero odd coefficients. Their sign masks are independent linear forms on
the dual-compatible basis-sign group. Explicit surjectivity onto all sign
patterns proves that every gauge orbit meets the chosen domain. Residual
gauge identifications are handled afterward using the entire sign group.

For R3472 the search instead keeps the justified modulo-four restrictions.
It imposes no extra positive odd-coefficient gauge. The output is exactly the
original tensor, not just a selected collection of favorable branches.

## Character sieve and general-to-pseudo-unitary transport

The actual sphericalization dimensions provide a scalar character of the signed
quotient. Simple dimensions are nonzero and dual-invariant. Its two central-sign
sectors have codegrees `2f`, for the codegrees `f` of the original and signed
quotients respectively; its dimension is `2 delta`. Central induction therefore
requires `delta/f` to be an algebraic integer for every codegree in either
sector (Ostrik, Theorem 2.13 and Corollary 2.14).

The valuation test is valid even if the character and codegree fields differ:
in a common finite number field, norm integrality implies
`deg(q) v_l(p(0)) >= deg(p) v_l(q(0))`, where `p,q` are the monic minimal
polynomials of `delta,f`. Absolute constant terms may be used. This is a
necessary condition and its violation is a rigorous obstruction.

Every returned signed algebra is verified commutative after enumeration.
The regular representation is closed under transpose by duality, so it is
semisimple; the separating scalar polynomial's complete squarefree
factorization therefore accounts for all eight characters. The producer
rechecks their multiplication identities and every norm witness. Each nongauge
class is excluded by zero dimension, duality, or norm. The ordinary-ring sieve
leaves exactly the FP character's Galois orbit, whose positive embedding is
checked by exact root isolation.

Number-field definability follows from Etingof–Nikshych–Ostrik,
[arXiv:math/0203060](https://arxiv.org/abs/math/0203060), Theorem 2.30 and the
observation immediately after it. Galois transport of the spherical data sends
that dimension character to the positive FP character. This proves the stated
pseudo-unitary conjugate, without identifying pseudo-unitarity with unitarity.

## Replay and additional independent checks

The complete producer was replayed under Python optimization and passed exact
comparison with `general_spherical_gates.json`:

```sh
python -O evidence/rank8_research_20261022/pivotality/verify_general_spherical_gates.py
```

The output is saved as `pivotality_optimized_replay.log`. Optimization disables
Python `assert`, so success also confirms that these gates use their explicit
failure checks. All four enumerations and all character calculations completed.

| Ring | Normalized tensors | Unrestricted tensors | Gauge classes | Original class |
| --- | ---: | ---: | ---: | ---: |
| R8_3_982 | 3 | 96 | 3 | 1 |
| R8_3_1768 | 49 | 3136 | 28 | 1 |
| R8_3_1795 | 73 | 4672 | 42 | 1 |
| R8_3_3472 | 1 | Not used | 1 | 1 |

`review_pivotality.py` separately reconstructs every normalized tensor directly
from the recorded trace orbits. With ordinary Python integers it checks all
ordered associativity equations, the full coefficient bounds/parity, duality,
Frobenius reciprocity, and every claimed full sign-gauge identity. It also
reconstructs the complete unrestricted sign-orbit sets and compares their
hashes and cardinalities, checks that the output tensors are commutative, and
checks coverage of the character factors and obstruction kinds. It imports
none of the producer's enumeration, tensor-reconstruction, or validation code.
The resulting receipt is `pivotality_independent_review.json`.

This extra checker does not independently rewrite the exhaustive search or
the algebraic-number sieve; those were tested by the full optimized producer
replay. Its finite-output checks and the categorical source audit complement
that replay. Frozen inputs and the producing verifier are SHA-256-bound in the
independent receipt.

```sh
python evidence/rank8_research_20261022/r928_r941/review_pivotality.py
```

The computational evidence and source assumptions support all four stated
reductions. A pre-existing pseudo-unitary obstruction can now be applied to
general existence after verifying that any additional structures under
consideration transport through the chosen Galois conjugation.

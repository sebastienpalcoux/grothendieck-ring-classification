# General categorifications of four residual rank-eight rings are spherical

## Statement and scope

For each of `R8_3_982`, `R8_3_1768`, `R8_3_1795`, and `R8_3_3472`, every
complex fusion categorification admits a spherical structure. Every such
categorification has a pseudo-unitary Galois conjugate with the same fusion
rules.

The first assertion concerns the original category. The second permits
Galois conjugation; it does not say that the original category is
pseudo-unitary. These results assert neither existence, unitarity, nor an
exclusion of general unbraided categorification.

The source tensors are bound by the SHA-256 hashes in
`general_spherical_gates.json`. The complete finite computations, including
all scalar-character factors and exact obstruction witnesses, are regenerated
by `verify_general_spherical_gates.py`. This is a computer-assisted proof,
using exact integer and algebraic-number arithmetic.

## 1. Sphericalization and signed quotients

Let `C` be any complex fusion category with one of the four rings. Its
canonical sphericalization `C~` has two lifts `X_i^+`, `X_i^-` of each simple
`X_i`, related by the central sign object `epsilon = 1^-`, with
`dim(epsilon) = -1`. These properties, including the criteria below, are in
Ostrik, *Pivotal fusion categories of rank 3*,
[arXiv:1309.4822](https://arxiv.org/abs/1309.4822), §5.1.

Choose dual-compatible lifts, with `X_0^+` the unit. This is always possible.
For a nonselfdual pair choose one lift and then its dual. For an original
selfdual simple, the dual of a lift is another lift of the same object. It
cannot be its opposite lift: sphericality gives `dim(Y*) = dim(Y)`, whereas
`dim(epsilon Y) = -dim(Y)`, and the dimension of a simple object in a
spherical fusion category is nonzero. Thus both lifts of a selfdual simple
are themselves selfdual, as also stated explicitly in Ostrik §5.1(a).

Write `a_ij^k` and `b_ij^k` for the multiplicities of `X_k^+` and `X_k^-`
in `X_i^+ X_j^+`. Then

\[
 a_{ij}^k+b_{ij}^k=N_{ij}^k,\qquad
 T_{ij}^k=a_{ij}^k-b_{ij}^k,\qquad
 |T_{ij}^k|\leq N_{ij}^k,\quad T_{ij}^k\equiv N_{ij}^k\pmod2.
\]

The signed quotient `T = K_0(C~)/(epsilon+1)` has the same unit and duality,
cyclic trace symmetry, dual reversal, and every ordered associativity
identity. **Commutativity is not assumed**, even when `N` is commutative.
The enumeration engine identifies coefficients only under cyclic trace and
dual reversal, and imposes all ordered associativity equations.

Changing the lifts by signs `g_i`, with `g_0=1` and `g_i=g_(i*)`, changes
the signed coefficients to `g_i g_j g_k T_ij^k`. If one such change makes
`T=N`, then every `b_ij^k` is zero. The chosen positive lifts form a
spherical fusion subcategory, and forgetting the lifts gives a tensor
equivalence to `C`. This is the spherical-section criterion in Ostrik
§5.1(c).

## 2. Full parity enumeration modulo a valid sign gauge

For `R982`, `R1768`, and `R1795` (abbreviating the canonical IDs), start with
the **entire** parity interval for every active signed variable. No
indicator or modulo-four condition is imposed in these three searches.

For an odd original coefficient, its signed variable is never zero. Its
sign transforms by a linear character of the elementary abelian group of
dual-compatible basis signs. Choose a maximal independent family of these
characters and require the corresponding signed variables to be positive.
Every sign-gauge orbit has a representative satisfying these requirements:
independence makes the evaluation homomorphism onto all sign patterns
surjective. The verifier checks that surjectivity by listing the entire
sign group. Residual sign equivalence is handled by grouping under the
entire sign group, not just the signs fixed at this step.

| Ring | Signed variables | Independent sign fixes | Normalized solutions | Complete unrestricted solutions | Sign-gauge classes |
| --- | ---: | ---: | ---: | ---: | ---: |
| `R8_3_982` | 42 | 5 | 3 | 96 | 3 |
| `R8_3_1768` | 59 | 6 | 49 | 3136 | 28 |
| `R8_3_1795` | 59 | 6 | 73 | 4672 | 42 |

The unrestricted counts are reconstructed as actual sets by applying all
basis-sign masks to every normalized solution. No product-of-cardinalities
assumption is used to obtain the sets. The verifier additionally checks
that each count equals `normalized_count * 2^(number of independent fixes)`.

Exactly one gauge class in each row is the original tensor. Every other
class is incompatible with sphericalization, by the following complete
dimension-character test.

## 3. Exact elimination of all other sign classes

Spherical dimensions of the chosen lifts define a one-dimensional character
`d` of `T`, satisfy `d_i != 0` and `d_i=d_(i*)`, and give
`delta = sum_i d_i d_(i*)`. Every enumerated signed tensor has a commutative
semisimple algebra; this is **checked after enumeration**, not imposed on
the search. A separating regular multiplication matrix and its complete
squarefree factorization produce every character orbit. The verifier checks
all multiplication identities of each character.

Both sectors must be used in the codegree obstruction. Over the complex
numbers the sphericalization algebra splits under the central involution
`epsilon` into the original quotient `N` and the signed quotient `T`.
If `f` is a formal codegree in either quotient, its formal codegree in the
sphericalization is `2f`. The sphericalization has global dimension
`2 delta`. Central induction therefore requires

\[
 \frac{2\delta}{2f}=\frac{\delta}{f}
 \quad\text{to be an algebraic integer}
\]

for every formal codegree in both sectors. This is Ostrik, Theorem 2.13
and Corollary 2.14. In this computation both sectors are commutative, so the
complete factors of the regular Casimir polynomial give all codegrees.

The exact obstruction used is simple: if `p` and `q` are the monic minimal
polynomials of `delta` and `f`, of degrees `d` and `e`, then integrality of
`delta/f` implies, for every rational prime `ell`,

\[
 e\,v_\ell(|p(0)|)\ \geq\ d\,v_\ell(|q(0)|).
\]

Indeed, take norms in a common number field and cancel its degree. The
receipt records a codegree polynomial and a prime violating this inequality
for each norm obstruction. Its character records also give the defining
character polynomial, every simple dimension in that field, and the global
dimension polynomial. All witnesses are rechecked exactly.

Every character of every nongauge class is excluded by one of:

* a zero simple dimension;
* unequal dimensions on a dual pair;
* the norm inequality above.

Thus the actual sphericalization of any categorification has a signed
quotient gauge-equivalent to `N`. The spherical-section criterion proves
the assertion for these three rings.

## 4. A second-indicator normalization closes `R8_3_3472`

Here all eight original simples are selfdual. Their two spherical lifts are
selfdual by §1. For a selfdual simple in a pivotal fusion category, the
second Frobenius–Schur indicator is `+1` or `-1`. Passing from one lift to
the other changes the pivotal isomorphism from `alpha` to `-alpha` and
changes the second indicator's sign. This follows directly from the
defining rotation operator, which contains `alpha^(-1)` once; see Liu,
Palcoux, Ren and Vercleyen, *Triangular prism equations and categorification*,
[arXiv:2203.06522v5](https://arxiv.org/abs/2203.06522v5), Definition 2.14 and
Lemma 2.16. Therefore choose the lift of every nonunit simple with second
indicator `+1`. The positive unit lift already has indicator `+1`.

Theorem 3.9 of the same paper (the Fuchs–Runkel–Schweigert parity theorem)
states that if a selfdual simple `Y` occurs with odd multiplicity in
`X* tensor X`, then its second indicator is `+1`. It applies to pivotal
fusion categories and requires neither braiding nor pseudo-unitarity.
Apply it inside the sphericalization to the negative lift `X_i^-`, whose
indicator is `-1`. Its multiplicity in every `X_j^+ (X_j^+)*` is even.
Hence

\[
 \frac{N_{j,j^*}^{i}-T_{j,j^*}^{i}}2\equiv0\pmod2,
 \qquad T_{j,j^*}^{i}\equiv N_{j,j^*}^{i}\pmod4.
\]

The ordered form `X* tensor X` gives the same collection of conditions by
replacing `j` with `j*`; no commutativity is used.

Use precisely these congruences together with the parity bounds, duality,
and all ordered associativity equations. **No additional positive
odd-coefficient sign gauge is imposed in this search.** The indicator
normalization has already fixed the signs of the lifts, and arbitrary
sign changes would not preserve it.

The complete search has 84 signed variables and visits 298,865,973 native
nodes. It returns exactly one tensor, the original `N`. The verifier checks
the unique tensor against every full ordered identity and reconstructs the
modulo-four domains independently. The spherical-section criterion applies
directly.

A separate exploratory search using unrestricted parity and odd-coefficient
sign gauge for `R3472` timed out after 240 seconds. That search is
**inconclusive and is not used in this proof**. The complete search used here
is the justified second-indicator normalization.

## 5. Pseudo-unitary Galois conjugates

For each original ring, the same complete character calculation leaves
exactly the FP Galois orbit after the nonzero, duality, and codegree-norm
conditions. The receipt includes these ordinary-ring character tests and
identifies the FP character by exact real-root isolation and strict
positivity of all its values.

Thus the spherical structure just constructed has a dimension character
Galois-conjugate to the FP character. Work over a number-field model and
apply an automorphism carrying it to the positive FP embedding. The
transported spherical category has positive FP dimensions, and is therefore
pseudo-unitary. For the number-field model see Etingof–Nikshych–Ostrik,
*On fusion categories*, Theorem 2.30 and the following remark,
[arXiv:math/0203060](https://arxiv.org/abs/math/0203060).

This extends the previous conditional character tests in
`site/verify_scope_consequences.py`: the new step is the existence of a
spherical structure on every general categorification. It supplies no new
model by itself. Any pseudo-unitary obstruction invariant under Galois
transport may now be applied to general existence; for example an exclusion
of pseudo-unitary braided categorification gives an exclusion of general
braided categorification, since the braiding transports with the category.

## Replay and review

From the repository root:

```sh
python3 evidence/rank8_research_20261022/pivotality/verify_general_spherical_gates.py
```

The command regenerates the enumerations, character fields, and obstruction
witnesses, then compares the complete result with the saved receipt. Optional
`--ring R8_3_3472` (or another canonical ID) limits replay to one case.
`--write` regenerates the full four-case receipt and is not needed for review.

The enumeration generator uses signed 64-bit integer polynomial evaluation;
its exact coefficient/range bounds are checked before compiling. The gate
verifier checks that replacing the generator's domains does not increase
their maximum absolute values. Node and solution counters have overflow
guards. A timeout or compiler error aborts verification and never produces a
proof conclusion.

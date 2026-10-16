# Audit of the quadratic rank-four argument

**Assessment: passes this independent mathematical and exact-arithmetic audit.** No substantive gap or false inequality was found in Section 8, including the short-orbit theorem and the unconditional quadratic bound. The conclusion is conditional on the categorical inputs from Sections 2, 3 and 7; those inputs were separately reviewed by the structural audit agent. This is AI-assisted review, not independent human verification or Lean formalization.

## Material and scope

Reviewed the quadratic argument, corresponding to `manuscripts/rank4/papers/companion_sections/08_quadratic.tex`, together with the quadratic comparison lemma, signed second-moment lemma, dimension-field descent and the quartic Casimir-degree corollary.

Source SHA-256: `63eafe6ddf0fcb5e46e2da5e64bbff6da1bf5c2248864cffa12cc760c55db655`.

I read the argument line by line, reconstructed its cases, and wrote fresh checkers rather than importing the supplied scalar checkers. Neither audit script is a categorical theorem prover.

## Mathematical review

1. **Signed codegree two.** The codegree-two row gives the signed involution table by symmetry and orthogonality, without incorrectly identifying that signed basis element with an ordinary invertible object. Central integrality supplies the positive norm ratio. The upper-root comparison and the small-conjugate bound are consistent. The exclusions for `h >= 11`, `h = 4, 6, 7, 10`, and the `h = 3` Pell family all check. In particular, the Pell-family second-moment contradiction does not require the ordinary complementary characters to be rational. The three remaining ordinary global dimensions force a zero simple dimension by explicit integer-vector reconstruction.

2. **Rational complementary signed codegrees.** Both a repeated rational codegree on a quadratic orbit and two rational characters are treated. The codegree-five constant-codegree normal form is valid over the signed table. The field-intersection step correctly concludes that the two signed quadratic factors are the same field; it does not assume containment of arbitrary character values before establishing it.

3. **Signed involution.** The fixed and interchanged two-element sectors are distinct and exhaustive. In the interchanged case the norm-minus-one unit reduction is correct. The exceptional `Q(sqrt(5))` endpoint yields reciprocal sum one for the ordinary FP orbit and is impossible in rank four.

4. **Short quadratic character chart.** The orthogonality, parity, norm and d-number conditions give exactly fourteen rows. The denominator-cleared primitive idempotent norms agree with the table. The four norm-one rows have reciprocal trace one-half, so the primitive element squares to one. The five surviving complementary norms `25, 36, 45, 64, 96` are exhaustively excluded. The Pell descriptions and norm-square-class restrictions in `Q(sqrt(2))`, `Q(sqrt(3))`, and `Q(sqrt(5))` are valid.

5. **Ordinary endpoints.** Every endpoint dimension row is recovered independently from integer norms and inner products. The Fibonacci, rank-two and elementary multiplication exclusions are appropriate. The statements use ordinary dimensions only after the character-field reduction has been justified.

6. **Uniform quadratic bound.** The branches `h >= 2`, `h = 1` with large ordinary complementary product, short quadratic ordinary complement, and rational ordinary complement cover all possibilities. The two completed-square identities are correct. The small-`t`, chord, exceptional-unit and moderate-ratio estimates hold with their stated constants. The rational-selected-codegree endpoint cases are consistent. Finally, symmetry of the ordinary multiplication matrices gives each coefficient at most `d_i < sqrt(D) < 32`, hence at most 31.

## Independent exact checks

Run:

```sh
python evidence/rank4_unrestricted_20261017/check_quadratic.py
python evidence/rank4_unrestricted_20261017/check_quadratic_inequalities.py
```

The first checker verifies:

- Exhaustive short-row enumeration over every squarefree radicand allowed by `d J < 100`, with all parity restrictions and `L | (d J)^2`.
- Exactly fourteen row orbits, including each displayed norm, reciprocal trace, and primitive idempotent coefficient norm.
- The complete four-entry `(norm ratio, integral trace)` chart in the codegree-two Pell reduction.
- Rational-character linear normal forms for codegree pairs `(3,3)`, `(3,6)` and constant codegree five, as well as every special codegree-two row.
- Casimir characteristic polynomials, hence traces and products, for those three main normal forms.
- All seven ordinary endpoint rows and the three impossible ordinary global dimensions.
- All eight independent sign patterns in the constant-codegree-five ordinary family; only the two common-sign patterns admit nonnegative coefficients.

The second checker verifies **80 exact scalar identities and strict comparisons**, including the short-row second-moment contradictions, all four norm-ratio intervals, both completed squares, chord comparisons, exceptional-field endpoints, and the moderate and rational-selected-codegree bounds. Its interval comparisons inspect polynomial endpoints and interior stationary points.

Receipts:

- `quadratic_receipt.json`: PASS.
- `quadratic_inequalities_receipt.json`: PASS, 80 exact checks.

Checker SHA-256 values:

- `check_quadratic.py`: `6a031873e7704fb5c932a67bcaac5fde9c591e3a4d78def000a4058559e390df`.
- `check_quadratic_inequalities.py`: `6f99e1fe310c4b542b41d3335ff67ff4fcfdc4096655bfac6df889168c2e1f47`.

## Categorical input cross-check

The structural audit explicitly checked the signed second-moment construction: eight multiplicity-one constituents of induction of the unit have positive dimensions, while their canonical-sign translates have negative dimensions and are disjoint; both families have twist square one. Removing their squared mass gives the displayed second-moment inequality. It also checked central integrality and field containment against the primary formal-codegree source, and reviewed dimension-field descent.

## Two exposition improvements for integration

These are clarifications, not mathematical obstructions.

- In the first codegree-two subsection, the unit-gap lemma is stated for norm one. For norm two, replace its citation by the direct sentence: “The integral trace is at least four, so `s_0 >= 2 + sqrt(2)`.”
- Before the two nonnegative constant-codegree-five families in the short ordinary quadratic-orbit argument, state that nonnegativity forces the three nonunit basis sign changes to agree. The two common signs give precisely `s = 1, J >= 1` and `s = -1, J >= 0`. The independent eight-sign calculation above verifies this reduction and makes the otherwise compressed step transparent.

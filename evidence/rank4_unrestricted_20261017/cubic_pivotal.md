# Independent audit of the cubic and pivotal arguments

AI-generated research · independent verification pending.

**Assessment:** no mathematical obstruction was found in Sections 9–10 of the supplied manuscript. The cubic argument applies to a general complex categorification through its sphericalization; it does not assume that the original category is pivotal. The pivotal bound is correctly used as a separate result for pivotal categories or a Galois-transported positive dimension character. This assessment is conditional on the foundational sphericalization and induction statements audited separately, and is not human or Lean verification of the complete classification.

Supplied attachment source: `GeneralRank4_Aligned/rank_four_classification.tex`, SHA-256 `63eafe6ddf0fcb5e46e2da5e64bbff6da1bf5c2248864cffa12cc760c55db655`. The current argument is in `manuscripts/rank4/papers/companion_sections/09_cubic.tex` and `10_pivotal_bound.tex`; the executable receipt binds their hashes. The dependent core lemmas on induction, spectral saturation, sign translates, and positive central indicator measures were also read.

## Cubic field and positive central measure

The field reduction is valid. A cubic FP character field gives the rational algebra `Q × K`. Character cyclotomicity makes the cubic field cyclic and totally real, so duality fixes every character and hence every basis element. If the FP codegree were rational, the reciprocal identity gives `(f,D)=(2,6)` or `(4,4)`. The resulting order discriminants, 432 and 256, are incompatible with a cyclic cubic field: the first is not a square and the second is not divisible by its nontrivial odd conductor squared. Thus the codegree has degree three. The signed dimension field contains this codegree and has degree at most four, so it is precisely `K`; its rational algebra is also `Q × K`.

The signed Frobenius trace formula is correct for the coefficient-of-unit pairing. The rational character row `b_A=ρ(F(A))/(2g)` is rational, and its associated central object is self-dual. Thus its un-conjugated row norm is one, and its pairing with the unit row is zero. All dimensions in the unit row and all their conjugates are real.

I checked the unusually delicate Galois reindexing explicitly. If `W=σ̂(A)`, then

`σ²(a_A)=εσ(A)σ(a_W)` and `b_A=εσ(A)b_W`.

Consequently the reindexed average of `3σ²(a_A)²+σ²(a_A)b_A` is exactly

`Tr(a_W²)+(b_W/3)Tr(a_W)`.

This is not an unjustified replacement of a Galois average by a trace. The square map permutes `Gal(K/Q)=C3`; the independence from the indicator field persists after squaring, without requiring the square map to be surjective on that field's Galois group. The central indicator identity cancels the rational-row residual with the second term of the measure.

Pointwise positivity also checks: outside `I(1) ∪ I(ε)`, the trace equals `−b_W` and the weight is a variance. On `I(1)`, the trace is positive and `b_W=1/2−Tr(a_W)`, giving weight at least `Tr(a_W)/6`. The sign translate has the same weight. Commutativity ensures the induction constituents have multiplicity one. The supplied sign-translate lemma supplies the claimed atoms at `±1`.

The periodic Fourier argument is valid. Since the cubic degree is prime, disjointness fails exactly when the conductor divides the indicator order. Restriction to the `2F`th roots by Cesàro averaging preserves all moments in the other residue classes. Subtracting the specified two atoms leaves Fourier support `{0,F}`, hence constant weights on the two parity classes. Each class has ordinary roots other than `±1`, so positivity bounds their common extra masses. This establishes the conductor-sensitive inequality without assuming positivity of unsquared spherical dimensions.

## Cubic arithmetic and conductor reduction

The normalized polynomial argument was checked with prime valuations. From the `d`-number divisibilities and coprimality of `r` and `r−1`, one obtains `r² | h`; then `r | a`. The order discriminant gives the square norm and hence

`(H/r)^3 − A(H/r)^2 +(r−1)s²(H/r)−s² = 0`.

Applying the argument to twice a signed codegree is legitimate: multiplication by a nonzero rational number preserves the `d`-number condition. The Schur step is valid, including the congruence argument for the possible positive difference `4A−(r−1)²s²` and the special `r=3` boundary. The latter discriminant is exactly `s²(s²−4)`; it cannot be a nonzero square.

The divisibility `f | g` follows from an actual integral character value of an ordinary cubic induction constituent. The norm ratio is a positive integer, and trace domination gives `b+g≤a+f`. These are sufficient for all inequalities in the direct cubic reduction. The steps excluding `g≥2f`, then `f≥5`, then a norm ratio greater than one are algebraically consistent. A positive norm ratio is a square only after `f=g`; the proof uses it in that order. The remaining conductors and rational codegrees are exactly `(7,3,3)`, `(7,4,4)`, `(9,3,3)`.

In conductor nine, equality of the periodic bound forces `u=v=1/3`; equality of norm and reciprocal-square sum identifies the cubic polynomials and yields a signed character with FP codegree. Spectral saturation therefore supplies sphericality. Independently checked arithmetic gives discriminant `n²(4n−27)`, factor pairs `(1,27),(3,9)`, and the surviving value `s=3`. For the rational-character normal form, I rebuilt the full symmetric multiplication tensor and recomputed the Casimir trace and the stated associativity equation. The trace-30 equation has exactly the two stated nonnegative solutions. The second has an additional rational character, so the surviving table is the even `SU(2)_7` table as claimed.

The inert-prime obstruction is sound. The primitive idempotent gives kernel exactly `p Z_p × 0`; hence the order is the fiber product `Z_p ×_{F_p} B`. The order `B` is local because its integral normalization is the valuation ring of one local field. The perfect associative coefficient pairing identifies the canonical module of the finite flat `Z_p`-algebra with itself, so the fiber product is Gorenstein. The cited theorem then makes both factors discrete valuation rings, contradicting the residue degree greater than one. The conductor-seven polynomial reduces to an irreducible cubic modulo three, exactly as needed.

The rational-codegree-four trace-gap argument was checked at the level of all rational-algebra components. Both the signed and folded forgetful classes of the rational signed constituent equal the corresponding Casimir divided by four. Coefficient parity then gives `a−b ∈ 64 Z_{≥0}`. The norm/trace intervals imply that if the gap is positive, the two smaller codegrees in each triple lie in `(12/5,3)`. The aligned ratio of largest signed and FP codegrees is a totally positive integral unit of norm one. Its trace is an integer in `[3,7/2)`, so it is three and AM–GM forces the ratio to be one. This contradicts the positive trace gap.

The conductor-seven exclusion subsequently uses positive central identities obtained by Galois transport of the spherical section. It does not assert pseudo-unitarity at the original embedding. The bound `D<1500`, refined trace bound, divisibility `7 | s`, and congruence `A≡3 mod 4` give `s=7`, `A=110`, and the contradiction. All numerical thresholds in this chain were independently checked exactly.

## Pivotal bound

The centered third-moment inequality follows from a constrained real quadratic critical-point equation. Its coefficient and the expansion of the centered cube agree with the displayed formula. Integrating `|1+az+az²+z³|²` gives the asserted lower bound: the first indicator vanishes, the second has absolute value one, and the third is bounded by the relevant fusion coefficient. The argument uses an actual positive central measure only in the cases stated.

I checked the concentration argument beyond replaying its endpoint scripts:

- The three-term indicator estimate gives the stated variance bound and the lower bound on every non-FP reciprocal codegree. In particular every non-FP codegree is below five and every corresponding nonunit character coordinate is below `11/6` in absolute value.
- The elementary spectral estimate and the `a=2` lower bound give `B≤25+(4+11/6)S`, hence `B<11 sqrt(D)`.
- The function used to bound `C` has positive second derivative. Its exact value at zero, its rational endpoint bound, and `Q≥999/1000` give `C≤71/100+5 sqrt(V)`.
- The estimate on `R` and completion of the square give the stated bound `g(B)≤0`. Independently expanding the stronger preceding expression verifies every relaxed coefficient. For example the negative square-root coefficient is `4.71 sqrt(2)<20/3`, and the quartic coefficient is at most `2.00602<2.007`.
- Differentiation of `g` gives the displayed positive derivative lower bound on `[4t,11t]`; the endpoint is positive, so `B<4t`.
- Substitution `a=2−4/t` reproduces `L0` exactly. Replacing the two smaller dimensions by equal dimensions is permitted because the derivative in their sum is strictly positive throughout the allowed interval.
- For the three scalar functions in the second concentration step, differentiating directly gives the displayed common lower bound. The leading term is at least `2−12/t`; the square-root term is bounded by `5.03/sqrt(5t−2)`; the remaining derivative is bounded by `1.03·3.009/t^(3/2)`, together with `1/t²` in the zero-variance case. Their sum is greater than one at and above `t=158/5`.
- The rational endpoint expansion is consistent term by term. It yields lower values exceeding `1/2`, `5/2`, `12` and derivative lower bounds exceeding `19/10`, `5/2`, `4` respectively.

The determinant argument correctly uses both the weighted mean and variance of the three other eigenvalues. The cubic product bound follows by subtracting the common mean and applying the zero-sum triple product bound. Its function `P` is increasing on the specified interval and satisfies `P′≤1/6`. The endpoint reduction in `B`, `V`, and `t` respects their monotonicities. For `B<25` and for the third variance interval, the ordinary weighted AM–GM bound is sufficient. The exact displayed determinant bounds are below one, so the integral determinant vanishes.

The concluding rank argument has no hidden field-generation assumption. Every character outside the FP orbit has all conjugates of its `X` value smaller than one, forcing that algebraic integer to vanish. Every character in the FP orbit evaluates the nonzero element `x` nontrivially. Thus the matrix rank is the degree of the FP field. Its invertible `2×2` principal block excludes rank one, while its vanishing determinant excludes degree four. The degree-two Schur complement forces the other two dimensions to be integral; their conjugate codegree bound makes them both one, producing the impossible fourth invertible object. Degree three is already classified by the preceding cubic theorem.

The exceptional pivotal-character lemma also checks. If a dimension character lies outside the FP orbit, dimension-field containment leaves precisely two copies of the same real quadratic field. Central integrality supplies the norm ratio, and the squared-dimension first-moment measure supplies `w≤1/2+1/(2H)` even without positivity of individual dimensions. The resulting inequalities contradict `D≥576`. The non-self-dual conclusion correctly invokes the separately proved sphericality theorem and the two real-character orbits before applying Larson's pseudo-unitary result.

## Primary-source validation and exact receipts

Primary papers inspected:

- Ostrik, *Pivotal fusion categories of rank 3*, [arXiv:1309.4822](https://arxiv.org/pdf/1309.4822), Theorem 2.13 and Corollary 2.15: dimensions of induction constituents and codegree-field containment.
- Dong–Lin–Ng, *Congruence Property In Conformal Field Theory*, [arXiv:1201.6644](https://arxiv.org/pdf/1201.6644), Lemma 4.2 and canonical center normalization: the anomaly-free squared Galois action on twists.
- Nasseh–Sather-Wagstaff–Takahashi–VandeBogert, *Applications and homological properties of local rings with decomposable maximal ideals*, [arXiv:1802.00307](https://arxiv.org/pdf/1802.00307), Fact 2.6 and Corollary 2.7: Gorenstein fiber products have regular one-dimensional factors.

The independent script `cubic_pivotal_checks.py` passes 27 exact checks, with its source-bound receipt in `cubic_pivotal_checks.json`. It imports no supplied checker or census. The supplied `pivotal_scalar_certificate.py` and `verify_pivotal_mean_endpoints.py` were additionally replayed and passed. These arithmetic checks are supporting evidence; the categorical implications above were audited mathematically rather than inferred from checker success.

No canonical manuscript files were changed in this audit.

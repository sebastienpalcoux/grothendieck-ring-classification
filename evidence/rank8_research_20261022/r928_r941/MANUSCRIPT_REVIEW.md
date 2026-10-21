# Independent review of the 2026-10-22 manuscript chapter

Reviewed: `manuscripts/rank8/paper/m3_research_20261022.tex`, SHA-256
`61764ef5b538e5edd246e64fb189dd9f82ec7bc162bbb2425664bc1ab44d8c3d`.

**Conclusion:** the mathematical statements and their stated scopes are
consistent with the evidence reviewed. One reference locator must be
corrected before publication. No mathematical counterexample or unsupported
upgrade from pseudo-unitary to general categorification was found. This is an
independent computational and mathematical audit, not external peer review
or a proof-assistant formalization.

## Required reference correction

In the R8_3_3472 dual-spectrum proof, the citation for algebraic integrality
of `D/h` must be **EGNO, Theorem 7.17.6**, not Corollary 3.3.16.
The latter concerns simple FP dimensions below two. The relevant Lagrange
theorem applies to the integral-dimensional fusion subcategory constructed
in the proof. This changes no mathematical argument or computed spectrum.

The authoritative author's final book was checked directly:
<https://math.mit.edu/~etingof/egnobookfinal.pdf>, printed pp. 56 and 171.
The other specific EGNO locators in this chapter were checked: Proposition
6.3.4 is the equal-dimension dominant-functor criterion; Corollary 7.16.7
is Morita invariance of FP dimension; Theorem 8.12.3 is the center/Morita
criterion; Exercise 7.16.8 gives the regular-object rank-one action.

## Four general sphericalization reductions

Accepted with the exact distinction in the chapter: the original category
admits a spherical structure, and a Galois conjugate is pseudo-unitary.
The original category is not asserted to be pseudo-unitary or unitary.

The full parity domains, independent odd-variable sign normalization,
complete sign-gauge expansion, and the separate FS-positive normalization
for R8_3_3472 are correctly described. In particular, the second
normalization is not combined with an unjustified further sign gauge.
Opposite selfdual lifts have opposite second indicators; the negative
indicator parity theorem applies inside the canonical sphericalization.
It needs pivotality there, not a pivotal structure on the original category.

The factor of two in both sector codegrees and total sphericalization
dimension cancels correctly. The norm test is a necessary condition in a
common number field, and does not assume the two minimal polynomials define
the same field. The dimension-character exclusions and the final positive
Galois conjugate follow the complete character calculation.

The earlier independent full optimized replay and separately implemented
integer tensor/gauge checks are recorded in `PIVOTALITY_REVIEW.md` and
`pivotality_independent_review.json`. The reviewed producer receipt has hash
`89ad25baeb05b69c95519670eb4cdd894a29d3b7f4d920535b1f404f46ba13d4`.

## Braiding and Morita restrictions

The minimal tensor-image proposition is valid for arbitrary complex fusion
categories. A proper integral image forces every source simple to have
integer FP dimension; otherwise the image is dominant, and Morita equality
of FP dimensions makes the composite functor an equivalence. No preservation
of a chosen pivotal structure is needed.

The individual braided exclusions have the necessary scope: noncommutative
rings need no reduction; R8_3_65 uses a general braided near-group theorem;
the remaining four use the proved simultaneous Galois reduction of category
and braiding. The source-semion splitting for R8_3_982 requires a source
braiding, which the chapter explicitly assumes at that step. It does not
infer an unbraided tensor-product splitting from a central semion.

For R8_3_1795, the positive selfdual situation makes the reduced S-matrix
identity and its codegree consequence valid. Lacabanne's Lemma 3.1 and
Proposition 3.3 apply before the later negative-dimension pivotal hypothesis
in that paper: <https://arxiv.org/pdf/1807.00766>, pp. 13–14. Thus their use
does not import that incompatible later hypothesis. The asserted failure of
`d_i^2 = D/10` agrees with the recorded source dimensions.

The R8_3_1154/R8_3_1795 argument compares multiplicities of distinct center
simples, not merely a set of possible dimensions. Applying a Galois
automorphism to the complete Morita context and then using global-dimension
Morita invariance is a valid general-scope reduction. It excludes their
shared Morita class, not either individual unbraided categorification.

## R8_3_982 module theorem

The statement agrees with the complete small-lattice enumeration already
independently reviewed in `R982_MODULE_TYPES_REVIEW.md`. In particular,
nontrivial pointed associator implies that the involution acts freely on
every module category; all induction columns are nonzero by indecomposable
cyclicity; the unimodular and determinant-four Gram cases exhaust ranks;
and the parity obstruction is imposed after returning to original rows.

The exact module receipt hash is
`44d470d2e1cd8620dec52314c1aae9ab282d9cf0aa1f4b823c2b65b50a9eb768`.
The eight algebra objects and three module types are explicitly necessary
candidates. The chapter does not claim the two nonregular types admit
module associators, or that `1 + X5` has a separable algebra structure.

## R8_3_3472 first rank-two branch

The corrected statement covers exactly the action with `X1` matrix
`[[5,7],[7,7]]`; the other recorded branch is expressly outside scope.
The integral commutant calculation, positive eigenvalue `s + 5t sqrt(2)`,
three square-sum equations, and bounded spectrum enumeration are consistent.
The integral-dimensional subcategory is closed because every radical
coefficient is nonnegative. The dimension-five and dimension-seven
nonpointed alternatives are correctly excluded by tensor-product dimension
and stabilizer arguments. The order-seven orbit obstruction removes exactly
the spectrum with three objects of dimension `7 + 5 sqrt(2)`.

I independently replayed `r3472_rank_two_dual_spectra.py` while reviewing this
chapter: two recorded actions, one covered, eleven enumerated spectra,
one orbit exclusion, ten remaining necessary spectra. Multiplicity notation
in the table is now unambiguous. No action faithfulness or commutativity of
the Morita-dual ring is assumed.

## R8_3_65 pointed Fourier exclusion

The new Fourier-fiber lemma is valid in its stated positive spherical
setting. Equality in the triangle inequality fixes the nth powers of all
twists, and inversion of the first n indicator moments gives equal fiber
weights. Disjoint pointed induction supports then yield the two integer
coefficient identities. For R8_3_65 these force multiplicity one and the
coefficient bound eleven on the generator columns. Applying only these
necessary consequences is a valid relaxation of the complete fiber problem.

The published, corrected version of Schopieray's Lemma 3.1 was checked
directly at printed p. 1628:
<https://londmathsoc.onlinelibrary.wiley.com/doi/pdf/10.1112/jlms.12789>.
It states pseudo-unitarity **up to Galois conjugacy**, exactly as used in the
chapter. The older arXiv v1 states a stronger claim; the chapter correctly
cites the published result instead.

The cyclic associator representatives give the displayed generator and
involution indicators. The phase table distinguishes even and odd classes
correctly; merging classes one and three only weakens a necessary test.
The six branches cover all pointed associator classes and allowed second
indicators. The proof uses exact rational separating covectors, with no
numerical solver status treated as a certificate.

The twist-domain argument is a trace compression, not an order cutoff.
After the Cauchy prime-support restriction, orders outside the finite
`2^a 5^b` box have zero relative traces at all four tested powers. The
separate auxiliary order-three rotation domain is explicitly retained.
Thus the theorem's general complex exclusion has no residual bounded-order
or unitarity assumption. This paragraph is a mathematical cross-review of
the new lemma and the stated inherited cone dependencies; it is not a new
independent reimplementation of that entire earlier cone.

## Optional editorial precision

The phrase “necessary list ... contains eight objects” in the module theorem
could be made even more explicit as “eight candidate underlying objects.”
The present wording is already qualified and is not an existence claim.
Adding “Theorem 3.9” to the BNRW Cauchy citation would make the dependency
easier to locate. Neither point changes a theorem or its scope.

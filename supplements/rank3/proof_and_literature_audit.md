# Proof and literature audit

17 September 2026. This note accompanies the manuscript; it is not part of the research article.

## 1. Literature status

The precise starting reference is:

Victor Ostrik, *Pivotal fusion categories of rank 3*, with an appendix written jointly with Dmitri Nikshych, **Moscow Mathematical Journal 15** (2015), no. 2, 373–396, arXiv:1309.4822.

Theorem 1.1 assumes pivotality. Section 5.2 establishes sphericality for the quadratic case; the rational case follows from weak integrality. Section 5.3 leaves the cubic problem, and Theorem 5.8 provides a large-coefficient restriction rather than a general classification.

The literature searches undertaken for this request did not locate a subsequent published removal of this hypothesis. In particular, Jingcheng Dong, *On Grothedieck rings of rank 4 self-dual fusion categories*, arXiv:2505.19153v2, 28 May 2025, still describes the rank-three classification with its pivotal assumption in the introduction. This is supporting evidence, not a proof that no later or unindexed result exists. The spelling of “Grothedieck” here follows the displayed title of that preprint.

Other pertinent material checked included Andrew Schopieray, *Norm, trace, and formal codegrees of fusion categories*, Journal of Algebra 568 (2021), 362–385, arXiv:2005.13760, and Ken Kikuchi, *Classification of connected étale algebras in pre-modular fusion categories up to rank three*, arXiv:2311.15631v3. These do not supply the unconditional rank-three sphericality theorem asserted in the accompanying manuscript. The latter concerns algebras in pre-modular categories, not removal of pivotality for arbitrary categories.

Publication and submission dates were distinguished from automatically generated dates on arXiv's HTML renderings. In particular, the HTML rendering date of Ostrik's paper is not a new 2026 revision.

## 2. Exact external mathematical inputs

| Input | Location used |
|---|---|
| Rank-three based-ring presentation and the two codegree identities | Ostrik, Section 3.1, Section 3.2, equation (12) |
| Sphericalization and its signed quotient | ENO, Remark 3.1; Ostrik, Section 5.1 |
| Equivariantization realization and the canonical signs of dimensions | Bartlett, arXiv:1502.02882v2, Definition 5.13, Lemma 5.14, Corollary 5.15 |
| Induction of the unit has trivial twist | Ostrik, Theorem 2.5 |
| Multiplicities and dimensions of its simple constituents | Ostrik, Theorem 2.13 |
| Codegrees divide global dimension without assuming pivotality | Ostrik, Corollary 2.14 |
| Codegrees lie in the spherical dimension field | Ostrik, Corollary 2.15 |
| Normalized modular S-matrix columns are ring characters | Ostrik, Example 2.9 |
| The n-th indicator belongs to Q(zeta_n) | Ng–Schauenburg, *Higher Frobenius–Schur indicators for pivotal categories*, Theorem 5.1 |
| Central-induction twist formula for any spherical fusion category | Ng–Schauenburg, *Frobenius–Schur indicators and exponents of spherical categories*, Theorem 4.1 |
| Weak integrality implies the existence of a spherical structure | ENO, Propositions 8.23–8.24 |
| Quadratic rank-three categories are spherical | Ostrik, Theorem 5.1 |
| Classification after sphericality has been established | Ostrik, Theorem 1.1 and Section 4.5 |

The new Galois-averaged moment inequality is not attributed to these references. Its complete derivation is Proposition 4.1 of the manuscript.

## 3. Checks at the sensitive points

**The dimension field.** Irreducibility of the original cubic and inclusion of all its roots in the dimension field force that field to have degree three and to be Galois. The signed rational algebra is then a field, not merely an algebra with a chosen character. This is what permits the Frobenius trace identity to remove the non-unit dimensions.

**Norm comparison.** The norm is taken inside this common cubic field. Thus the integral element delta/f_1 has norm tilde(c)/c, not a square root or a norm in an unspecified extension. Positivity of both norms gives tilde(c) >= c. The signed coefficient bounds independently give tilde(b) <= b.

**The central sign.** The relevant copy of Rep(C_2) has its usual symmetric braiding but the negative spherical dimension on the sign representation. Consequently its twist is -1. For every even n, its n-th indicator is -1, not +1: the cyclic rotation contains one inverse pivotal map. This normalization is explicitly proved in Lemma 3.1.

**The twelve known objects.** Induction of the unit has six distinct constituents because the sphericalization has commutative Grothendieck ring of rank six. Their dimensions are positive under every embedding. Tensoring by the central sign negates these dimensions, so the other six objects are distinct from the first six. Squared twists, rather than twists themselves, are used. Their squared twists are one by the normalized S-matrix character calculation in Lemma 3.2.

**A single measure for all six moments.** The same three automorphisms are chosen to fix Q(zeta_120) pointwise. Its degree is 32, coprime to three, so this is possible. All six even orders 2, 4, 6, 8, 10, 12 divide 120. Changing the automorphisms separately for different moments would not justify a single positive measure; the proof does not do so.

**No Galois descent of associators is needed.** Automorphisms are applied only to identities between algebraic scalars. Central dimensions are integral combinations of the simple dimensions after forgetting to the sphericalization. All their conjugates are real. This supplies positivity even when individual dimensions are negative.

**Normalization of the measure.** It is the sum of three probability measures, not their average. Its total mass is 3 and its first six moments are 1. The known atom at 1 has mass at least 3(u+v)/2. The Fejer polynomial has value 49 at 1 and integral 63. Hence u+v <= 6/7 and c <= 7b/2.

**Descent to the given category.** The final argument does not stop with the existence of a unitary realization of the surviving ring. It changes the signs of two lifts, proves that the three chosen lifts are closed under tensor products, and restricts the forgetful functor to a tensor equivalence. Thus sphericality is transferred to the original hypothetical category.

**Classification scope.** There are five possible based rings, not five tensor-equivalence classes of categories. The existence of unitary realizations does not imply that every category in the list is unitary or pseudo-unitary.

## 4. Algebra and simplification checks

The three-by-three trace and determinant identities, the associativity relation, and the special values (b,c)=(14,49) were independently checked symbolically in this session. The constants 32, 49, 63, and 6/7 were checked separately. These small algebra checks are not used as a replacement for an argument in the paper.

A lower-degree moment polynomial was also considered. Using only the first five squared-twist moments would give c <= 18b/5 and b <= 20, which already suffices for classification. Six moments were retained because they give the sharp bound c <= 7b/2, attained by the surviving cubic ring, without adding any case split or any new cyclotomic field. Four moments give a weaker bound and require further small-case analysis.

No multiplicity cutoff, enumeration of parameter tuples, classification of signed tables, solution of associativity constraints by search, or evaluation of an unknown indicator is part of the proof.

## 5. Relation to the rank-four project and verification scope

The positive-measure viewpoint and the use of the central sign continue the methodological direction of the rank-four project. Every property needed here is re-established from the published inputs above; no claimed rank-four classification or computational certificate is assumed. The new step is to annihilate all non-unit terms simultaneously by the Frobenius trace identity while fixing the relevant indicator fields.

The proof and the checks were produced within the same conversation. This is not independent verification, formal verification in Lean, peer review, or certification of priority. No gap was identified in these checks, but independent expert review remains necessary before making a publication-level claim of a new resolution.

# Eleven unresolved fusion rings: research record

24 October 2026. Source classification commit: `323c4227ffb796a72eef506f1eb289437fbc95db`.

## Classification outcome

**Newly excluded: 0. Newly categorified: 0. Still unresolved: 11.**

This record contains stronger necessary conditions, a module-category rigidity theorem, exclusions of specific categorical branches, and explicitly incomplete construction routes. None of those results is counted as a categorification or as nonexistence of a whole source ring. No publication changes are included.

The input manifest and eleven profiles in `inputs/` bind the analysis to the source tensors and published classification. The reports in the six case folders give proofs, primary references, exact arithmetic receipts, and their dependencies. Existing sphericalization and Galois-pseudo-unitarity results remain explicit dependencies; no argument silently assumes that an arbitrary original category is unitary.

| Ring | New result or completed check | Remaining gap |
|---|---|---|
| R6_4_155 | Its previously forced central twists distinguish all four pointed objects. Consequently every tensor autoequivalence fixes those objects; this rules out a rank-nine Morita branch. The supplied laptop campaign has no verified solution. | Existence or nonexistence of the source category. |
| R6_8_1660 | The surviving rank-eight Morita alternative is exactly R8_3_941, with every structure constant checked. The proposed integral-center restriction is already satisfied by existing candidates. | Existence of the nonpointed algebra, and of either category. |
| R8_3_928 | Every indecomposable semisimple module category would be regular, without a rank bound. Hence all categorical Morita partners would be equivalent to the original category. | The original category itself; four necessary center patterns remain. |
| R8_3_941 | The relation to R1660 is identified exactly. Integral-center checks remove no surviving patterns. | An actual algebra and associator; fourteen necessary center allocations remain. |
| R8_3_1154 | Central-indicator computations recover the existing sign restriction and give no further cut. | Surviving center data and a categorical construction or obstruction. |
| R8_3_1768 | A previously undetermined rank-eight module action has exactly two completions. The prescribed GH(C6,2) Morita route requires pointed associator class 3 in H³(C6,C×). | A twisted GH category and an associative separable algebra; commuting matrices alone supply neither. |
| R9_2_137 | No central boson, no nontrivial Tannakian subcategory of the center, and all integral central simples invertible. | The remaining center and Morita possibilities. |
| R9_2_1607 | The same center restrictions; the positive Tambara–Yamagami sign is ruled out by an exact separating certificate. | The negative-sign branch. |
| R9_2_1975 | The extreme D8 Morita branch is ruled out, leaving two uniform types. The integral center is Vec. The positive TY sign is ruled out. | The negative-sign branch: the strengthened necessary system still has exact feasible witnesses. |
| R9_2_1976 | The same restrictions as R1607, including exclusion of the positive TY sign. | The negative-sign branch. |
| R10_1_189 | New all-coprime indicator restrictions and a finite Galois/twist analysis. The metric-C5 center branch reduces to two conjugate rank-fourteen modular-data candidates with exact nonnegative integral Verlinde coefficients and valid second indicators. | Categorification and the required algebra; modular data alone do not give a category. The trivial pointed-center branch also remains open. |

## Unified center obstruction for the four rank-nine rings

Their dimensions are 1, 2, and d=4+3√2, and their global dimension is D=144+96√2, of norm 2304=2⁸·3². Their integral subcategory is a Tambara–Yamagami category on V4 with nonalternating bicharacter.

For the three commutative rings, a hypothetical central lift of the free isotropic involution would give a central quotient whose ring is R6_4_174 or R6_4_6. Exact tensor maps identify these quotients with already excluded project cases. For R1975 the corresponding alternatives are the excluded R6_4_1 or R155 equipped with an impossible permutation of its pointed objects. Thus no central boson exists. The pointed center is Vec or sVec in the commutative cases, and is Vec for R1975.

Suppose Rep(H) were a nontrivial Tannakian subcategory of the center. Algebraic-integer dimension divisibility and the norm of D force the primes dividing |H| to be 2 and 3. Burnside's theorem makes H solvable, so H has a nontrivial one-dimensional representation. This would be a central boson, a contradiction. In particular no Morita representative has a nontrivial faithful finite-group grading.

The inverse image of the integral source subcategory under the forgetful functor is exactly the subcategory of integral-dimensional central simples. Its dimension is an integer with prime support contained in {2,3}. Etingof–Nikshych–Ostrik, Theorem 1.6, makes it solvable and hence weakly group-theoretical. With no Tannakian subcategory it is weakly anisotropic; Natale, Theorem 4.1, makes it pointed. This application concerns the integral subcategory, not the nonintegral ambient center.

See `rank9_commutative/NO_CENTRAL_BOSON.md`, `rank9_noncommutative/NEW_RESTRICTIONS.md`, and the independent audit in `rank8_quartic_pair/`.

## A finite TY twist restriction

Let Y have dimension two and let ε be the sign of the TY parameter. In a positive spherical representative, Shimizu's indicator formula gives

    (ν₁(Y), …, ν₈(Y)) = (0, ε, 0, 0, 0, ε, 0, 2).

The central-induction formula and positivity imply that every constituent of I(Y) has eighth-root twist. Fourier inversion fixes its weighted twist fibers. Each primitive-eighth-root fiber has weight D/4; the only remaining dimension pairs are

    (2+d, 2+7d), or (2+4d, 2+4d).

Combining this condition with the center obstruction and the existing complete induction/character systems excludes ε=+1 for R1607, R1975, and R1976. The reports retain exact rational separating certificates and distinguish them from numerical discovery. The ε=−1 systems do not give a whole-ring exclusion. In particular, the R1975 system through height six has an exactly checked nonnegative integer witness; this witness is only feasible necessary data.

## Module rigidity for R928

The forced nontrivial C2 associator makes the pointed involution act freely on every module category. The complete internal-end domain has 960 vectors. Exact positivity leaves four candidates. In each case the paired induction Gram has a plus block of determinant one and minus block I₃. Cauchy–Binet then forces exactly three remaining pairs of module simples, without any assumed rank cutoff.

Every integral factor gives the regular based module. The categorical step uses an object whose internal end is the tensor unit, so the module category is actually regular; it does not assume that a based module uniquely determines associators. Consequently every Morita partner is equivalent to the original category, there are exactly four connected separable algebra isomorphism classes within any hypothetical categorification, and every tensor functor is fully faithful onto its fusion image.

The full proof and exact verifier are in `rank8_quartic_pair/`. An independent audit and exact receipt comparison are in `rank6_pair/AUDIT_R928.md`. This closes an entire family of alternative-model searches, but does not settle existence.

## Construction routes and limitations

For R1768 the GH(C6,2) candidate has the correct global dimension, and the prescribed bimodule actions have been completed exactly. A diagonal C2 stabilizer forces a nontrivial restriction of the GH pointed associator to C2; a C3 stabilizer forces its restriction to C3 to vanish. Together they force class 3 modulo 6. Therefore the untwisted GH route cannot work. Existence of the required twisted category and the algebra 1+ρ remains unproved.

For R189 the new finite analysis retains Galois orbits of both columns and twists. Its first rank-seventy Gram/indicator witness is only necessary data. A further analysis conditional on a nontrivial pointed center produces two conjugate rank-fourteen modular-data candidates for the complementary factor. Their complete matrices satisfy the modular identities, all 14³ Verlinde coefficients are nonnegative integers, and their second indicators agree with duality. An independent exact extension checks indicators through order ten and all 140 associated cyclic-rotation spectra; these necessary tests also pass. Each nonunit object generates the full rank-fourteen fusion ring, so there is no proper nonpointed fusion subring to which an existing lower-rank exclusion applies. No associator or required algebra has been constructed. Integer-infeasibility reports for the alternative trivial pointed-center branch remain explicitly uncertified.

The rank-fourteen calculation uses positive double-braiding S and positive twists T. In this convention the tested relation is STS = ξ T⁻¹ conjugate(S) T⁻¹. The independent audit corrected the convention before accepting the candidates; using S instead of its conjugate would give a false obstruction on nonselfdual objects.

The rank-six laptop archive contains 29 verification reports, zero numerical passes, and zero exact certificates. Failure of that incomplete numerical campaign proves no exclusion. Its original uploaded archive is not duplicated here; the audit summary is retained.

## Replay and provenance

The portable verifiers identify their required inputs locally. Some discovery and full-reconstruction programs also require the pinned project checkout and the prior `rank9_m2_research` source tree. Those dependencies are intentional and are documented; a saved matrix certificate alone is not a proof that the matrix enumerates every categorical possibility.

The new rank-nine quotient arguments inherit the published lower-rank exclusions. Their tensor identifications, source bindings, and categorical scope were checked afresh. A duplicate reconstruction of all 128 old R174 certificate systems was stopped after approximately 23 CPU minutes; it did not finish, and the subsequent old C4 replay was not started. These old results are cited as dependencies, not represented as newly re-proved. See `rank9_commutative/dependency_replay_status.json`.

The combined archive includes an inventory with SHA-256 hashes. It omits downloaded third-party papers, interpreter caches, compiled executables, and the already supplied laptop archive. Reports link primary papers instead. Verification receipts distinguish exact arithmetic, inherited categorical theorems, exploratory computations, and unresolved existence claims.

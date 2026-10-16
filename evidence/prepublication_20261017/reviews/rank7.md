# Fresh pre-publication audit: rank-seven former residuals

Audit date: 2026-10-16 UTC (2026-10-17 Asia/Shanghai).
Auditor: a fresh AI review pass. This is not human verification or Lean formalization.
Repository snapshot reviewed: `the pinned repository snapshot`, the scientific content published before the requested public release.
No frozen evidence or manuscript was modified by this audit.

## Outcome and limits

I found no definite mathematical blocker in the ten rank-seven cases formerly unresolved at the start of `evidence/unified_20261016`. Their current allocation is eight general-complex exclusions and two unitary constructions. All ten records in `all_cases.json` point to existing proof files.

This conclusion means that the examined arguments survived a fresh adversarial reading, with important categorical hypotheses and primary-source statements checked. It does **not** certify that every statement is correct. In particular, the new central-base-change, commutation, conductor-equality and moment arguments remain research proofs requiring expert human scrutiny. The automatic checker validates finite arithmetic consequences, not the entire categorical argument. The 4,172 negative rows of the full historical rank-seven census were not each manually re-proved in this pass; the parent audit separately replays their aggregate evidence and historical gates.

The R7_4_2053 conclusion depends on the rank-eight R8_1_18 STS theorem. The separate fresh rank-eight audit reports no blocker there after independently deriving the STS identity and checking all four associator classes and the all-order moment hull. The rank-seven reduction itself was read here.

## Findings

| Severity | Finding | Consequence / recommended treatment |
|---|---|---|
| No mathematical blocker found | The ten current endpoint arguments have coherent scope bridges and distinguish ring arithmetic from categorical existence. | Current decisions need not be downgraded on the basis of this review. Continue describing them as provisional AI-generated research. |
| Moderate documentation issue | The rank-seven manuscript's verification paragraph lists only seven unified-stage scripts, omitting later endpoint verifiers. | The aggregate dispatcher covers these scripts. Add the complete command list in the current reproduction/audit guide; do not silently modify frozen evidence. |
| Presentation issue | Several frozen intermediate notes and JSON receipts still say `unresolved` or `classification_changes: 0`. These describe their original reduction-only stage, not the current endpoint. | Explain historical scope clearly in current documentation; use the current ledger/all-cases table as the current-status authority. |
| Presentation issue | Existing manuscript disclosure says AI “assisted”; several audit titles use “independent” without stating that these were independent AI passes. | The requested public caution should explicitly say AI-generated, not independently human-verified, and not Lean-formalized. Automated replay is not a substitute for either. |
| Residual research risk | The inversion-descent constructions rely on new categorical base-change and coherence deductions, not explicit full F-symbol tables. | This is not a discovered gap; it is a precise priority for subsequent expert review. A successful tensor comparison alone does not validate these deductions. |

The manuscript command-list omission is in `manuscripts/rank7/papers/manuscript.tex`, in the paragraph beginning “The new verifiers are in” and ending with the R601 explanation. The missing final-stage commands include:

- `verify_quadratic_center_trace.py`
- `verify_r2603_center_moments.py`
- `verify_R2591_staged_morita.py`
- `verify_R2053_rotational_fs.py`
- `verify_r2053_r18_reduction.py`

The current aggregate entry point `tools/verify_unified_20261016.py` is the preferable public reproduction route, including its historical mode as documented by the parent review.

## Scope table

| Case | Current conclusion | Fresh reading focus |
|---|---|---|
| R7_3_146 | General exclusion | Signed sphericalization scope bridge; full-row Galois transport; conductor 24 saturation; all-root two-moment hull; two indicator branches; separating inequalities. |
| R7_3_601 | General exclusion | Nonbraiding proof without a unitary-only criterion; simple integral center; nontrivial prime-power exclusion; complete induction lattice domain. |
| R7_3_1022 | General exclusion | C3/V4 reduction; commutation cocycle; forbidden V4 near-group terminal; inverse algebra and both cocycle choices. |
| R7_4_35 | Unitary construction | Noncyclic parent Morita square; honest right intertwiners; central descent; coherent inversion; TY exponent distinction. |
| R7_4_106 | General exclusion | Same quadratic-center argument at conductor 12, including both allowed indicator signs. |
| R7_4_2053 | General exclusion | Complete dihedral reduction; rotational indicator obstruction; actual R18 subcategory in the remaining reflection branch. |
| R7_4_2155 | General exclusion | Nonselfdual pair handled in signed quotient; character field Q(sqrt(-2)); correct zero second indicators; conductor 12 moment obstruction. |
| R7_4_2591 | General exclusion | Twisted V4 block reduction; staged subalgebra Morita equivalence; fixedness and duality constraints; dihedral support contradiction. |
| R7_4_2603 | General exclusion | Two-dimension Morita/Galois bridge; all-character reciprocity; relative-moment pairing without an exponent bound; full quadratic ring of integers. |
| R7_4_2665 | Unitary construction | Published C16 near-group input; central algebra; inversion descent and coherence; order-four pointed associator; TY(C4) output. |

## 1. General-to-pseudo-unitary reductions

I read `THREE_CASE_GALOIS_PU.md`, its source-bound verifier, and the corresponding manuscript inclusion. The signed sphericalization quotient does not assume a pivotal structure on the original category. The lift of the central involution has dimension +1; nonzero spherical dimensions then determine its square and its action on fixed objects. After quotienting by g=1, duality is trivial even in the case with a nonselfdual pair. The resulting commutativity is therefore justified.

The weighted multiplication pairing has weight two on the fixed object. The six displayed associativity equations and the matrix construction retain these factors. The simultaneous sign normalizations are legitimate: changing the a, b, and f signs independently normalizes A, B, and r in the cases where these coefficients are nonzero. Division by r is separately handled when r=0 in the enumerator.

The global-dimension condition is stronger than the rational-codegree least common multiple: sphericalization doubles both global dimension and the epsilon=+1 formal codegree, giving delta/f_E integral. Because f_E=48 eta with eta a unit, delta/48 is integral. Checking the monic rescaling p(48x) is the correct integral-closure test for an irreducible minimal polynomial. The surviving quadratic dimensions are the FP dimension and its conjugate; conjugating the category over a number field gives pseudo-unitarity without assuming it initially.

For the dihedral family I checked the *published*, corrected Schopieray Lemma 3.1. It guarantees Galois-conjugate pseudo-unitarity for categories with two simple FP dimensions. It does not claim the original category is pseudo-unitary. The manuscript uses the corrected conclusion. Transporting the existing separable algebras and Morita context through Galois conjugation, then using Morita invariance of global and FP dimensions, supplies the required scope bridge.

## 2. Quadratic-center exclusions R146/R106/R2155

Files read: `QUADRATIC_CENTER_TRACE_PROOF.md`, `GALOIS_FORGETFUL_ROW_LEMMA.md`, `CONDUCTOR_EQUALITY_LEMMA.md`, `QUADRATIC_RESIDUE_SATURATION.md`, `QUADRATIC_TWO_MOMENT_HULL.md`, `verify_quadratic_center_trace.py`, and their manuscript counterparts.

The induced-unit constituents have multiplicity one because the source fusion algebra is commutative. The character identity used for full-row transport is the induced-unit character identity, not an inference from dimensions alone. Applying Galois symmetry to the normalized S-matrix produces the codegree ratio f_E/f_sigma(E); this ratio is present. The integral induction vector is fixed by S, so its support is preserved with positive Galois signs. This correctly fixes the conjugate-unit row.

The separating-matrix factorization supplies a real character-field argument: the remaining character fields are disjoint from the relevant quadratic dimension field. Rational formal codegrees alone would not suffice, but the proof does not make that shortcut. Orthogonality of the dimension characters and all other characters explains the rank-one row-transport correction. Mixed-sign images are legitimately impossible, while a uniform negative sign is retained when appropriate.

I compared the conductor-equality refinement with the actual primitive-vector proof of Schopieray Lemma 4.1. In the local permutation representation, the big-cell line and the small-cell adjoint image are the two maximal-singular directions. Both pull back from the character-conductor level. The trivial-character equality case is fixed by upper and lower unipotents, hence by the entire local group. Orthogonal irreducible decomposition and the CRT tensor product then justify the global equality consequence. The argument uses equality of the projected norm, not the false assertion that the full S-image remains twist-fixed.

The quadratic-residue refinement keeps the local Gauss-sum signs and the CRT correction factor. At conductors 12 and 24, every unit squares to one, so paired nonrational rows have identical twists. This is sufficient for pairing their moment weights. The unrestricted rows retain an all-root hull, so no hidden universal root-order cutoff is used.

I independently checked the root-order cases in the two-moment hull proof. Nonzero irrational first moments occur at f*m with squarefree m coprime to 6; irrational second moments with vanishing first moment occur at 2f*m. The rational vertical segment and the five rational pairs cover the remaining cases. The bound phi(m)>=4 for nontrivial m coprime to 6 makes the stated convex combination valid, including the negative Moebius-sign correction for conductor 12.

The pivotal sign argument uses palindromic tensor words/sandwiches. It does not slide factors through each other or assume a braiding. Odd multiplicity in a nondegenerate alternating form is impossible, which yields the stated indicator restrictions; nonselfdual objects have indicator zero.

Code review found the finite-domain logic consistent with the proof: bounded nonnegative low rows; repeated-dimension lexicographic symmetry breaking; exact PSD Schur tests; singular-residual range tests; nonnegative paired Gram contributions; actual indicator branches; and exact integer separating inequalities. The low-row recursion only prunes by necessary conditions. The code does not depend on optimizer infeasibility or floating-point eigenvalue thresholds.

## 3. R2603: full-character reciprocity and moments

Files read: `R2603_CENTER_MOMENT_PROOF.md`, `Q5_ALL_ROOT_TWO_MOMENT_HULL.md`, `verify_r2603_center_moments.py`, and `r2603_center_moments.tex`.

The seven explicit characters are checked against the entire source multiplication table; hence reciprocity is imposed on a complete character basis. The choice of Galois automorphism fixes Q(sqrt(-2)) and flips sqrt(5), which is possible because the fields are disjoint. The coefficient ratio in the transport map is checked on every character.

For the moment pairing, sigma squared fixes K=Q(sqrt(5)); relative trace in an abelian cyclotomic extension commutes with sigma squared. Thus Galois partners have equal traced powers even when their individual twists differ. This justifies common moment pairs for paired rows without a conductor-equality hypothesis. No involutivity of the full permutation of central simples is required.

The reciprocity calculation explains why only two I(1) blocks survive. The independent exhaustive enumeration of the 50 preliminary blocks and all equal-codegree assignments is an appropriate coverage corroboration; it does not substitute for the character identity.

The arithmetic condition correctly uses O_K=Z[(1+sqrt(5))/2], with doubled coefficients of matching parity. Replacing it by Z[sqrt(5)] would have incorrectly discarded rows, but the actual verifier does not do that. The 17-vertex hull includes negative half-scalings of the six primitive pairs; this covers odd coprime factors with Moebius sign -1. The first/second trace formula, Gram identity, and universal separating covector align with the stated 45-coordinate system.

## 4. R601: simple-center induction lattice

Files read: `R601_CENTER_LATTICE_PROOF.md`, `verify_r601_center_lattice.py`, and `r601_center_lattice.tex`.

The source positive dimensions are integral, and each nontrivial basis element generates the full ring; thus a hypothetical category is simple and pseudo-unitary. The nonbraiding argument handles both possible Müger centers. In the modular case, 360/25 is not an algebraic integer. In the symmetric case, the negative weighted character expression is used as a finite-group class-algebra coefficient; this remains valid in the super-Tannakian case after forgetting the symmetric structure. It is not an unjustified use of the unitary Schur-product criterion.

I checked the primary simple-center theorem: nonpointed, simple, complex, and nonbraided are exactly the relevant hypotheses. I separately checked Nikshych's prime-power result in its original context: the center must be integral and nondegenerate braided, and the prime-power exponent must be positive. Nonidentity invertibles are excluded separately by simplicity. Thus the retained divisors of 360 are justified.

The finite checker regenerates the 336 possible low blocks and every residual row in the stated bounded box. The scaled inverse is explicitly checked by RH=hI. Its modular covectors annihilate every allowed rank-one row contribution while taking nonzero value on the target. Arbitrary repetitions of rows are permitted. This is an exact lattice contradiction, not a claim that a search failed to find a center.

## 5. R1022: inverse V4 Morita argument

Files read: `R1022_GENERAL_PROOF.md`, `verify_R1022_inverse_morita.py`, and the older complete `A4_C3_GENERAL_PROOF.md` on which the reduction depends.

The initial C3 action trivializes the pointed associator because it fixes a simple object. Multiplicity two is incompatible with a nontrivial C3-by-C3 projective block, which forces the first splitting. The rank-one pointed action on the unique irrational module then trivializes the entire order-12 pointed associator. The transitive four-point action with nonnormal order-three stabilizer correctly identifies A4.

The V4 block-rank argument covers both algebra cocycles. The nontrivial H^2 class extends from V4 to A4 via the binary tetrahedral extension, so the pointed dual is untwisted in both branches. The complete A4 quadratic-ring normalization leaves the asserted k=4 candidate after the rank-two exclusion.

In the new commutation lemma, a nontrivial V4 commutation cocycle gives a two-dimensional projective irreducible and Z=2 sigma. Expanding Z squared then produces the near-group level 8, which is ruled out by Schopieray's general-complex Theorem 1.1; the original C*-only terminal is not used. I checked that published theorem directly.

The inverse algebra has pointed support because its multiplicities are Hom(1,X) of actual underlying bimodules. This is proved from the actual Morita context, not guessed from dimensions. The remaining stabilizer cocycles cancel for both inverse algebra choices because every V4 automorphism fixes its order-two H^2 group. The resulting twelve t-dimensional simples contradict the three 2t-dimensional simples of the intermediate category.

## 6. R2591: staged Morita obstruction

Files read: `R2591_TWISTED_V4_REDUCTION.md`, `R2591_STAGED_MORITA_EXCLUSION.md`, both corresponding verifiers, and `r2591_staged_morita.tex`.

The initial projective-block calculation uses ordinary group cohomology and multiplicity spaces, so does not require a pivotal or unitary structure. Its rank-zero branch would force FP dimension t/2, which is not an algebraic integer. This is a valid impossibility, not a positivity shortcut.

The proof retains a possibly twisted inverse V4 algebra. Individual fixedness of the two irrational source simples forces phi(L)=L; otherwise a nontrivial character restriction interchanges the two stabilizer characters. Duality of Y and Z then forces the distinguished square invertible a outside L.

For K=D8, conjugation by a outside L restricts to a transposition of the two reflections in L. No square in S3 is a transposition. This removes that case before choosing the fixed central involution in the remaining abelian groups.

The subobject 1+delta is an actual subalgebra of Q, not just a proposed algebra of the correct dimension. Passing first through it gives another free-orbit rank-16 category. Q becomes a connected separable algebra of dimension two in that dual, hence 1+h. The equivalence of iterated bimodule categories is the standard restriction/extension of actions along a subalgebra, so the original category really is recovered.

The final nonnormal involution forces D8. The absence of t-dimensional source objects forces the two reflection classes to differ under the mixed automorphism. The central r squared then interchanges the two irrational support orbits, contradicting individual fixedness. The argument does not need an untwisted pointed associator or a unitary classification.

## 7. R2053: dihedral reduction and endpoint

Files read: `FOUR_RANK7_DIHEDRAL_REDUCTION.md`, `R2053_ROTATIONAL_FS_OBSTRUCTION.md`, `R2053_R18_MORITA_REDUCTION.md`, their verifiers, and the corresponding manuscript portions.

The multiplicity-one XY and YY* relations trivialize the relevant fixed-object projective blocks. The inverse algebra and nonnormal order-two subgroup are proved from the Morita context. The D8 normalization retains all five associative candidates; the exceptional one is excluded only after the two-dimension Galois scope bridge, using a genuine formal-codegree field incompatibility.

Self-duality of the two inverse irrational objects forces a=1 because the relevant support stabilizers are trivial. In the rotational branch, the odd cubic multiplicities force the order-two pointed indicator to be +1. This implies the rotation associator class is even. The group-theoretical exponent bound then contradicts the exact TY(C4) eighth indicator. The argument does not infer a coherent extension merely from a ring automorphism.

In the reflection branch, sigma=s rho commutes with r and satisfies sigma squared=r cubed+P sigma. The eight displayed objects therefore form an actual fusion subcategory. Full coefficient matching identifies it with R8_1_18. This implication is sound; the final exclusion uses the separate rank-eight theorem noted above.

## 8. R35 and R2665: construction audit

Files read: both `R35_INVERSION_CONSTRUCTION.md` and `R2665_INVERSION_CONSTRUCTION.md`, their independent model-constructor code, and `inversion_orbifold_model.tex`.

I checked Izumi Theorem 11.3 and Corollary 13.5 in the stored primary text. The latter identifies the tensor autoequivalence group faithfully with the stated subgroup of Aut(G) for m=n; thus fixing the central-invertible labels really removes the remaining parent tensor-auto-equivalence ambiguity.

The noncyclic R35 parent square does not rely on H^2(G)=0. Its right-module generators are given by an honest unitary representation U. Right whiskering leaves the implementing intertwiner unchanged; replacing it with alpha'_h(U(g)) would be invalid because U(g) need not lie in the fixed-point algebra. With the actual whiskering, the right internal-end cocycle is trivial. This is the necessary extra argument beyond the C16 case.

The free-orbit scalar calculation distinguishes left and right shifts and yields inversion, rather than merely an unspecified permutation of central labels. The central algebra and its multiplication are preserved. In central base change, the algebra identification is retained; changes give the dual C4 action. The proof does not silently discard this ambiguity.

The four dimension-one module simples and four irrational module simples establish that the descended left module is regular. This promotes the bimodule to a tensor autoequivalence. Its square is controlled only up to an inner functor and a dual-action power at first. The explicit monodromy identities T squared=Inn(r) and Inn(r squared)=Id then remove that ambiguity. Trivial universal grading gives Aut_tensor(Id)=1, so the C2 associativity coherence condition is satisfied. This is a categorical coherence argument, not a tensor-table test.

For R2665, Budinski's table contains J16^1 with m=3 and c=exp(pi i/4). The thesis states exact certification/completeness in the range including n=16; the proof is not relying only on rounded decimal b-values. The quotient cyclic kernel scalar is primitive order four, forcing a pointed rotation associator of that order. The TY exponent argument then selects C4 among the four output invertibles.

For R35, the cited Yu–Zhang Proposition 3.1 supplies the actual C4-by-C4 near-group input; the isotropic diagonal subgroup and a restricted to it equal to one give the stated selfdual neutral ring. The quotient rotation action has fourth power exactly identity. The TY fourth-indicator argument excludes C4 and selects V4. Neither construction assumes uniqueness of all categories with the neutral rank-eight fusion ring.

Finally, the relative tensor identity for actual free bimodules computes all mixed and irrational products. Comparing all 343 coefficients is correctly used to identify the already constructed category with the census ring; it is not presented as the reason the category exists.

## 9. Primary-source checks and local verification scope

Primary sources freshly checked on the web or against their already downloaded full text:

- Schopieray, *The dimension block of a spherical fusion category*, https://arxiv.org/html/2609.35287, Lemma 4.1 and its proof; local full text `work/literature/dimension_block.txt`.
- Schopieray, *Categorification of integral group rings extended by one dimension*, published version https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/jlms.12789, Lemma 3.1 and Theorem 1.1.
- Liu–Palcoux–Ren, https://arxiv.org/pdf/2102.01663, Section 5, especially Theorems 5.1, 5.9 and 5.10.
- Nikshych, https://arxiv.org/pdf/1208.0840, Corollary 6.16 with the integral nondegenerate braided context immediately preceding it.
- Izumi, https://arxiv.org/abs/1512.04288, stored full text `work/unified/two_dimension/izumi_near.txt`, Theorems 11.3, 12.5, 13.4 and Corollary 13.5.
- Budinski thesis, stored full text `work/unified/two_dimension/budinski.txt`, sections 3.3.1–3.3.2 and Table 3.1.
- Yu–Zhang, https://arxiv.org/html/2412.20763v2, stored full text `work/unified/two_dimension/yu_zhang.txt`, Proposition 3.1 and the stated bicharacter/quadratic form.

This pass inspected verifier source rather than trusting saved JSON status strings. A local structural check confirmed that every current rank-seven `verify*.py` uses explicit failure checks rather than Python `assert`, so `python -O` does not erase those checks. This is only a code property, not a mathematical certificate. The parent process performs the fresh comprehensive normal and optimized replays; their logs are separate from this report.

Public release wording should retain the distinction between (a) claimed mathematical classification, (b) exact finite checks that have been replayed, and (c) independent human verification or Lean formalization, neither of which has occurred here.

# Independent audit: ranks 2–5

Audit date: 2026-10-25. Repository: `/workspace/scratch/90f37cc83103/grothendieck-audit`, pinned commit `8014c749c17ddd2ad3d1b99a4359d49a8be921c5`. Auditor: child task `audit_lower`. This report concerns mathematical proof logic and the implementations described below; root is separately executing the full finite replays. No repository files were modified by this auditor.

## Finding and qualification

**No definite false exclusion, false positive model, or missing categorical premise was identified in the inspected rank 2–5 arguments and code. This is not a proof that the entire project is error-free.** In particular, reading a lengthy proof, replaying its arithmetic, and matching a tensor to a published model do not independently prove every external construction or associator. The report separates substantive review from the remaining coverage limitations.

No ring in this assigned scope is recommended for status reversal on the evidence obtained. The rank-four unrestricted theorem remains a substantial new computer-assisted theorem: its logical proof was inspected in detail, but this audit is not human peer review or formal verification.

## Mathematical manuscript coverage

Read all of `manuscripts/rank2.tex` (246 lines), all of `manuscripts/rank3.tex` (913 lines), the rank-four finite and unrestricted masters and every substantive included section, and the rank-five master and all eight substantive mathematical sections. Also read the displayed positive-model tables, rank-four low-trace generated chart, and relevant bibliographies. Generated census/allocation tables and verification guides were not all read line by line; the root replays address their numerical content.

| Scope | Proof reasoning specifically checked | Assessment |
|---|---|---|
| Rank 2 | Signed sphericalization; formal-codegree field/norm comparison; saturation of signed coefficient; resulting spherical structure; scalar Galois reduction before the positive Gauss-sum bound | No use of unitarity to exclude arbitrary complex categories found. Vec(C2) and Fibonacci supply existence. |
| Rank 3 | Nonselfdual pointed case; K(k,l,m,n) associativity; quadratic norm/field sphericality argument; cubic squared-twist measure; low-b chart and reducible/Pell cases; near-group and exceptional exclusions | No definite logical gap found. The complete five-ring statement and separate existence list agree. |
| Rank 4 sphericalization / indicators | Lift arithmetic, absolute-value saturation and gauge rigidity; total-real dimension characters; squared central dimensions; treatment of FS signs and central sign object | Positivity of *unsquared* dimensions is used after a stated pseudo-unitary/Galois reduction, not assumed for every spherical category. |
| Rank 4 field descent | Simultaneous Galois columns; folding and signed columns; central unit produces nontrivial grading when the dimension field is larger; classification of possible rank-four gradings | The sphericality of invertible cases is established before being invoked here. No circular dependence on the final census found. See `07_dimension_descent.tex` lines 26–202. |
| Rank 4 quadratic | Codegree-two case; rational complement; signed involution; small integral character rows and 14-row short quadratic chart; complementary norm at least 100; unconditional D<1000 estimates | The signed basis involution is not silently treated as an ordinary invertible. All rational/composite algebra cases used in the argument were retained. Exact 14-row chart independently reproduced. |
| Rank 4 cubic | Corrected Frobenius trace including rational-character cross term; Galois reindexing and positive averaged measure; periodic Fejer bound; conductor 7/9 reductions; inert-prime order argument; norm/trace gap and automatic sphericality | The cross term is present at `09_cubic.tex` lines 47–177. Positivity is derived rather than assuming a positive dimension character. Primary fiber-product Gorenstein theorem statement and local hypotheses were checked; the external theorem was not independently reproved. |
| Rank 4 pivotal bound | Centered third moments; Fejer estimate; concentration; small integer determinant forced to vanish; resulting field-degree alternatives; exceptional spherical dimension not in FP orbit | Followed the full argument in `10_pivotal_bound.tex` (543 lines). Did not independently recompute every endpoint derivative/factorization; root's deep verifier checks supplied scalar certificates. |
| Rank 4 quartic | Integral totally positive E/D, norm-square restriction; central ratios; nonexceptional low-trace reduction; exceptional Q(sqrt2,sqrt5) relative pair trace and arithmetic elimination | Followed all 650 lines and the low-trace chart. Distinction between the codegree field and character-value field is supplied by preceding descent results. |
| Rank 4 finite criteria | Arithmetic/d-number/cyclotomicity; low induction; arbitrary spherical and signed moment obstructions; skew-selfdual adjoint parity; root-length conductor 40; C3 near-group hypotheses; nonselfdual S_m exclusion | Finite proof is not dependent on unrestricted theorem. Positive-dimensional uses have explicit gates. Larson's pseudo-unitary classification is transferred by the two-FP-dimension Galois reduction. |
| Rank 5 | Rank-five commutativity; known arithmetic and PU gates; finite relative-root-trace reduction; exact Farkas certificates; q=2/3 mod4 parity and q=5 mod8 inert parity; cyclic C4 central support; Izumi equivariantization | No definite hypothesis gap found. Inert parity includes F18,5073 / F18,5076. C4 support derivation retains subgroup and indicator branches. |

The rank-four sections above are in `manuscripts/rank4/papers/companion_sections/`. Finite sections are in `manuscripts/rank4/papers/finite_sections/`. Rank-five mathematical files are `manuscripts/rank5/papers/{known_criteria,finite_indicators,quadratic_parity,cyclic_support,inert_parity,positive_models,automatic,census}.tex`.

## Important general-complex / model checks

1. **The two-FP-dimension gate is Galois pseudo-unitarity.** The published Schopieray Lemma 3.1 says a Galois conjugate is pseudo-unitary. The current proof and code use this form. An older arXiv v1 web text says pseudo-unitary outright; that stronger assertion is not the argument used here. Source: published DOI `10.1112/jlms.12789`.
2. **Formal codegree divisibility is available for nonspherical categories.** Ostrik `https://arxiv.org/pdf/1309.4822`, Corollary 2.14 explicitly treats the general case by sphericalization; Corollary 2.15 supplies the spherical dimension-field statement. These are not being applied as if arbitrary categories were already spherical.
3. **Near-group automatic sphericality is not a unitary-only classification.** Thornton `https://arxiv.org/pdf/1102.4640v1`, Theorem 1.3 concerns near-group categories generally and gives sphericality/Galois pseudo-unitarity. Larson `https://arxiv.org/html/1401.1879v2`, Theorem 1.1 lists the required pseudo-unitary rank-four candidates; the near-C3 multiplicities are 0,2,3,6. The code checks the complete multiplication tensor before applying this result.
4. **Rank-five Izumi equivariantization uses an actual action, not merely an outer symmetry.** In `positive_models.tex` lines 18–45, the product of the two actual symmetries in Izumi Example 13.10 is (-1,R(pi/4)L), whose matrix is an involutive reflection. Izumi `https://arxiv.org/pdf/1512.04288v2`, Lemma 13.1 gives the automorphisms on the Cuntz generators, with S0 fixed; Example 13.10 supplies the actual group. On C[C3] tensor C2 the trace is zero, so the two eigenspaces have dimension three. This produces the stated X^2, XY rules. A gap of the form “order-two outer class therefore coherent C2 action” was specifically checked and is not present.
5. **Rank-five other nonstandard existence sources.** Izumi Examples 9.5–9.6 supply C4+4 and V4+4. LPR `https://arxiv.org/html/2010.10264v5`, Sections 4.2 and 4.4, supplies the dimension-12 and dimension-24 unitary F-symbol constructions. Evans–Jones `https://arxiv.org/html/2404.14466v3`, Section 3.3, supplies unitary Ad(E8) categories. These source statements were checked; their entire construction proofs/pentagon systems were not independently re-solved.

## Code inspection

Fully read the following implementations, including elimination branches and numerical guards (not just API/docstrings):

- Rank 4: `software/{exact,rings,rapid,induction,proofs,applications,dispatch,signed,global_signed}.py`; `enumerate_signed.cpp`, `enumerate_signed_diophantine.cpp`, `enumerate_nonselfdual.cpp`, `enumerate_global_signed.cpp`, and the brute-force global reference. Also the unrestricted dispatcher and independent positive-model reconstruction script.
- Rank 5: `software/{exact,rings,induction,proofs,quadratic_parity,inert_parity,higher_traces,unified,extension,cyclic_four,signed,models,models_extension,gram_vectors}.py`; `gram_vectors.cpp` and `low_completion.cpp`. Rank-five `exact.py` is byte-identical to the read rank-four copy.

Specific checks:

- `rank4/software/signed.py` lines 27–100: gauge-normalization masks, signed ranges/parity, singular elimination branches, and necessary adjoint parity. Lines 213–265: global orbit expansion retains all nonunit permutations and sign gauges; orbit residue signature is a necessary filter, not a stronger condition than adjoint parity.
- `enumerate_global_signed.cpp`: every orbit has a preferred representative by taking the minimum absolute mixed coefficient as b, then independent gauges making b,c,d nonnegative; the e sign condition only occurs when its independent signs remain free. Dense and each zero-denominator branch were checked. Congruence projection is necessary only. Bounds use safe integer sizes under M<=1000; modular products use 128-bit integers.
- `enumerate_signed_diophantine.cpp`: the A*i+C*a=-B0 reduction was independently derived symbolically. The gcd progression treats U=0, V=0, and both zero. The modulo-16 mask uses at most four a-residues times four i-residues, fitting 16 bits.
- Native Casimir determinant uses an exact Schur complement and 128-bit arithmetic; Python uses exact Bareiss division. Formal-codegree d-number and Frobenius-factor-degree tests are exact.
- Rank-five low-completion: all row-sum joins, entrywise nonnegative remainders, and every principal minor are retained/tested. Equal candidate-set symmetry reduction exchanges indistinguishable low columns. The Python B<=10^6 guard bounds the internal 64-bit products; determinant accumulators are 128-bit.
- Rank-five Gram vectors: complete nonnegative coordinate boxes, exact entry bounds and adjugate quadratic bound; Python verifies positive definiteness and accumulator bounds.
- Rank-five signed enumerator: duality triple orbits and all nonzero coefficient domains; independent odd gauge pivots; gauge normalization is disabled when positive second-indicator normalization is selected. Equations are checked when all their variables become assigned, with an exact accumulator bound. Process failure/timeout raises, rather than certifying exclusion.
- Rank-five finite indicator traces: relative Gauss signs and divisors of powers; finite prime-box enumeration and zero trace beyond it; shared second-indicator branches; exact integer/rational Farkas verification. Floating LP discovery is not used as an exclusion certificate.

## Independent calculations and differential checks

`lower_kernel_checks.py` and its JSON output record fresh checks outside the repository:

- All 4^4 selfdual tensor associativity identities reduce to precisely the six displayed polynomial equations.
- Both native linear elimination formulas verified as symbolic identities.
- Global signed enumeration with coefficient absolute value <=2 compared with the complete rectangular 5^10 brute-force search: **1,832 tables, 48 sign/permutation orbits; exactly equal after orbit expansion**.
- Native vs Python per-ring enumeration on 24 heterogeneous selfdual boxes, including all-zero and uniform bounds 1,2,3; both determinant/parity filtered modes; and 24 nonselfdual boxes. **All retained tables and complete rejection partitions agree.**

Additional fresh hand-directed enumerations performed during this audit (not saved as a standalone script):

- Rank-three b<50 non-neargroup candidates modulo swapping basis objects: exactly five classes, equal to the manuscript table.
- Rank-four short quadratic chart: exactly the manuscript's 14 rows, with d,L,ell,||u||^2 equal to (2,32,1/2,1), (2,64,1/4,3), (2,64,3/4,3), (2,72,1/3,2), (3,36,2/3,2), (3,96,1/4,3), (3,96,3/4,3), (5,20,1/2,1), (5,25,2/5,6), (5,25,3/5,6), (5,45,1/3,2), (5,45,2/3,2), (5,80,1/2,1), (13,52,1/2,1).
- Root-length scalar inequality on every relevant n=3,...,127: no failed inequality.

`lower_registry_check.py` / `lower_registry_check.json` compare the rank-eight imported lower-rank models against the current rank-four and rank-five model tensors using a fresh exhaustive unit-fixing permutation key, not the imported registry canonicalizer. **All 15 rank-four and all 17 rank-five tensors match exactly once; no omitted or extra class.** The rank-three hardcoded K3 parameters also agree with the five-model theorem: Ising m=0, Rep(S3) m=1, half-E6 m=2, and PSU(2)5 independently matched the truncated SU(2) rule. The meaning of half-E6 here is the rank-three even part with g^2=1, gX=X, X^2=1+g+2X.

## Remaining limitations / required interpretation

- Root's full rank-four finite and unrestricted replays and rank-five replay must be reported separately with their actual exit status. No success is inferred from historical verification JSONs.
- Some release/export/crosswalk wrappers were not inspected line by line. Core ordinary and signed rank-four enumeration, parsing, canonicalization, and rank-five tensor arithmetic were inspected; the aggregate replay is handled by root.
- External categorical construction proofs, including every original associator and pentagon equation, were not completely independently verified. Several positive tensors are checked against published formulas rather than reconstructed associators.
- The Nasseh–Sather-Wagstaff–Takahashi–VandeBogert primary Fact 2.6 / Corollary 2.7 was subsequently checked at https://www.math.nagoya-u.ac.jp/~takahashi/gorfib3.pdf. It supplies the stated conclusion for the fixed nontrivial fiber-product decomposition. Its original homological proof was not independently reconstructed.
- Every coefficient and endpoint calculation in the long quadratic/pivotal/quartic bounds was not independently re-derived. Full logical case coverage was read; selected arithmetic was independently checked. Root subsequently completed the supplied replays; their actual outcomes and composite-run qualifications appear in `audit-report.md`.
- No Lean formalization was attempted. “No defect identified in this audit” should not be rewritten as “all proofs and models have been independently proved correct.”


## Follow-up coverage completed

- Read the entire 184-line unrestricted ordinary-census `supplements/rank4/unrestricted/supplementary/census/enumerate.cpp`, the 240-line exact parser/tensor checker/deduplicator `supplements/rank4/software/verify_census_tensors.cpp`, `rank4/software/census_data.py`, and `rank5/software/census_common.py`. Inspected all singular cases, canonical representatives, necessary interval/Diophantine pruning, strict dimension threshold, exact Bareiss minors, integer guards and hash-independent equality/isomorphism witnesses. No omission found.
- `rank4_ordinary_enumerator_check.py` / JSON independently compare complete rectangular nonnegative coefficient boxes (59,049 selfdual plus 729 nonselfdual) at multiplicity 2 against the optimized ordinary generator. Thresholds D<5,10,20,1000 give 2,5,16,27 classes respectively, and **every complete tensor set agrees**, with no duplicate output.
- `lower_registry_all_snapshots.json` extends the independent snapshot check to **all three** rank6/rank7/rank8 imports. Each contains exactly the same complete 15 rank-four and 17 rank-five positive classes.
- `rank23_classification_check.py` / JSON streams **all 460,353 supplied rank-three tensors**. Exactly 460,352 have the manuscript K3 form and satisfy its associativity equation; the other is Vec(C3). Independent unit-fixing tensor matching finds precisely the five modeled rings, and every exported multiplicity band agrees: **460,348 excluded, five realized**. The positive source lines are 1,2,3,4,1003 (half-E6 is line 4). All 1,000 rank-two exported bands also agree with X^2=1+nX, multiplicity max(1,n), and exactly n=0,1 realized. The production export uses these theorem-derived counts; this fresh loop verifies its full concrete allocation rather than assuming those counts identify every tensor.
- Additional primary-source model matching: Grossman–Snyder https://arxiv.org/pdf/1102.2631 Table 2 matches all six H1 products in the independent constructor. Evans–Jones Section 3.3 matches all six Ad(E8) products. Hong–Rowell https://arxiv.org/pdf/0907.1051 p.6 matches the full PSU(3)_4 tensor after respecting its explicit transpose convention. EIP https://arxiv.org/pdf/2108.01564 Theorem 3.1 supplies the R(m) realizations for m=1,2; its stated 2D2 R(2) rule is the tensor used here. These checks establish correct references and fusion rules, not new independent solutions of all source associators.

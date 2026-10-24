# Rank-eleven multiplicity-one exclusion criteria: scope audit

This audit concerns all 182 physical input lines in the supplied rank-eleven census, using identifiers `R11_1_i`. “Known” includes published theorems and accepted mathematical methods developed in this project at lower rank. A failed necessary test is an exclusion only in the stated categorical scope. A successful necessary test is never a model.

The inventory below covers the criterion families present in the surveyed literature and the project's accepted lower-rank proof corpus. It is not a claim that every conceivable consequence of the literature, every possible theorem, or every instance of the pentagon equations has been decided. A method can be mathematically applicable but have an incomplete implementation or a finite discovery limit; such cases must retain that limitation in the final attempt ledger.

## Direct general-complex criteria

| Family | Hypotheses / exact witness | Source and reusable implementation |
|---|---|---|
| Fusion axioms and based-isomorphism identity | Input must be a nonnegative integral based ring with rigid duality and associativity; invalid or duplicate inputs are census errors, not categorical exclusions. | `../audit_input.py`, `../common.py`. |
| Rank-two subring classification | A rank-two subring has square `X²=1+mX`; only `m=0,1` categorify. For M1 inputs this test is vacuous. | Ostrik rank-two classification; lower-rank `software/classify.py` stage `rank_two`. |
| Formal-codegree d-number | Every formal codegree is a d-number. For monic minimal polynomial with coefficients `a_j`, check `a_n^j | a_j^n`. Casimir eigenvalues are `e_E f_E`, where `e_E=dim E`; rational multiplication preserves the d-number property. | Ostrik [1], Theorem 1.2 and Lemma 2.7; `work/obstructions/arithmetic.py:dnumber`. |
| Cyclotomicity of FP dimensions | Every simple FP dimension is a cyclotomic algebraic integer, including in noncommutative rings. A nonabelian splitting field for its minimal polynomial is an obstruction. | ENO [2], Theorem 8.51; exact Perron-factor isolation followed by the field test. |
| Extended cyclotomicity | For a commutative Grothendieck ring all fusion-matrix eigenvalues are cyclotomic. The extension to every eigenvalue of an arbitrary noncommutative regular matrix is not assumed. | LPR [3], Theorem 2.11; `work/obstructions/exact.py`; `field_automorphisms.py`. |
| Finite-prime and field-automorphism certificates | Irreducible-factor Frobenius cycle patterns or two explicitly noncommuting field automorphisms can prove a splitting field nonabelian. Failure to find a witness is not a complete abelian-field test. | Exact consequences of cyclotomicity; `work/obstructions/exact.py`, `extra_arithmetic.py`, `field_automorphisms.py`. |
| Primitive formal codegree | If no rational integer greater than one divides a formal codegree `f`, then all formal codegrees are its Galois conjugates, the rank equals its degree, and the ring is commutative. Norm exponents strictly below the degree certify primitiveness for a cyclotomic d-number. | Schopieray [4], Corollary 4.3 and Theorem 4.4. **General**, not merely spherical. `work/obstructions/extra_arithmetic.py`. |
| Lagrange / fusion-subcategory index | For every closed based subring `S`, `FPdim(R)/FPdim(S)` must be an algebraic integer. Includes noncommutative rings; implementations restricted to commutative input need adaptation. | ENO [2], Proposition 8.15; EGNO [5], Theorem 7.17.6; `work/obstructions/subring_dimension/`; current `../arithmetic/subring_indices.py`. |
| Transfer from an excluded subring | Check dual and product closure and an entire based-tensor isomorphism to an independently excluded smaller ring. Carry the accepted source proof and hash. | Functorial restriction to a full fusion subcategory; lower-rank `negative_subring.py`, current structural scan. |
| Near-group / two-dimensional rules | When simple FP dimensions are exactly `1,d`, every categorification has a pseudo-unitary Galois conjugate. If irrational `d²=rd+s`, categorification forces `s|r`. Further near-group constraints require their actual group hypotheses. | Schopieray [6], Lemma 3.1, Propositions 3.2–3.4; `work/obstructions/gng.py`, `two_dimension_induction.py`. |
| Nonabelian near-group restrictions | Irrational near-group dimension forces the invertible group abelian and multiplicity divisible by its order. Multiplicity `|G|-1` forces `G` cyclic without an abelian assumption. | Nikshych–Ostrik appendix to [7], Theorems A.6 and A.14. Do not apply Siehler's abelian-group theorem to a nonabelian group. |
| Tambara–Yamagami / feudal stabilizer | The adjoint stabilizer in a feudal (GTY) categorification is abelian. Beyond that, complete Liptrap equations can certify either existence or obstruction. | Liptrap [8], Theorem 4, Corollary 4.10; `work/literature/gty_*`. |
| Zero spectrum | A finite support pattern contradicts invertibility and the pentagon equation. It uses no dimension positivity or pivotality. | Liu–Palcoux–Ren–Vercleyen [9], Theorem 6.7; `work/obstructions/spectra/`. |
| One spectrum | The corresponding unique-channel pentagon obstruction; evaluate all scalar conditions exactly. | [9], Theorem 6.8, equations (6.13)–(6.18); lower-rank `one_spectrum.cpp/.py`. |
| Cyclic isotypic-summand integrality | For `gX=X`, `Yg=Y`, `gZ=Zg=Z`, and `n=ord(g)`, `gcd(n,N_XY^Z) FPdim(Z)/n` is an algebraic integer. All nontrivial cyclic subgroups and fixed triples are eligible. | Project `rank7_m5_20261019/review/CYCLIC_ISOTYPIC_PROOF.md`; `run_cyclic.py`; independent replay below. |
| Involution / cyclic module matrices | The algebra `1+g` or a trivialized cyclic subgroup supplies actual module categories. Enumerate required nonnegative integer matrices, tensor identities, duality, and dimension normalization exhaustively. | Project `involution_module.py`, `module_all.py`, `module3.py`, `morita/module_dual_gram.py`. Rank-specific matrix-shape assumptions must be rederived. |
| Morita dual Gram constraints | A genuine connected separable algebra forces a nonnegative integral restriction Gram decomposition. A merely formal sum of invertibles does not establish algebra existence. | EGNO [5], Chapters 7–8; project `morita/full_morita_gram.py`, cyclic module proofs. |
| Full-I(1) quadratic compression | For quadratic Casimir fields, the project theorem gives `2^(r-1) Q_d <= 4` for arbitrary categorifications via sphericalization; the bound is `<=1` after a proved spherical / Galois-PU reduction. | Project `theoretical_20261016/compression/full_I1_compression.tex`, using Schopieray [10], Lemma 4.1; current `run_compression.py`. |
| Solvability / forced extension-equivariantization | For dimension `p^a q^b`, every categorification is solvable. Enumerate both cyclic extensions and equivariantizations, all admissible neutral categories, and coherent actions before declaring impossibility. | ENO [11], Theorem 1.6 and Proposition 4.4; project dimension48,52,96,160 and related structural proofs. |
| Group-theoretical and grading descent | Under a proved structural theorem, reduce to pointed data, grading component dimensions, group orbits, projective stabilizers, or algebra restrictions. No dimension-profile match alone is a proof. | EGNO [5], ENO [11]; project lower-rank `small_dimension_morita.py` and structural family proofs. |

## Spherical and pseudo-unitary systems

These remain necessary systems, not constructions. General exclusions require either weak integrality, the verified two-FP-value theorem, a complete signed-sphericalization analysis, or another explicit reduction.

| Family | Precise role and reusable source |
|---|---|
| All spherical dimension characters | A dimension character must be nonzero on every simple and equal on duals; test all irreducible scalar components, also for noncommutative algebras. Project `general_signed/`, rank-eight `noncommutative/scalar_sieve.py`; its old `C^4+M2` guard is rank-specific. |
| Formal-codegree divisibility / field containment | The categorical global dimension divides formal-codegree denominators in the required algebraic-integer sense; every formal codegree lies in the spherical dimension field. [7], Theorem 2.13 and Corollaries 2.14–2.15. The general-category global dimension is not automatically the FP dimension or a source character codegree. |
| Spherical dimension-order lattice | A constituent of `I(1)` has dimension `D/f_E`, and its forgotten dimension belongs to the integer span of source dimensions. An exact integer-valued functional or lattice obstruction certifies failure without assuming positivity. Project `dimension_order.py`, rank-nine cubic lattice. |
| Integral Drinfeld-center dimension | For integral source categories the center is integral. Its distinguished dimensions `D/f_E` must be integers. Noncommutative Casimir multiplicities must be decomposed into sums of squares of possible representation degrees. `work/obstructions/noncomm_integral.py`. |
| Codegree reciprocal-square inequality | In the PU case `2 sum_E 1/f_E² <= 1+1/D`; equivalently `2 Tr(B^-2) <= 1+1/D` for regular Casimir `B`. There is **no extra factor** `dim E` in the sum. [7], Theorem 2.21. |
| Low central restriction / positive dimension semiring | For each `E`, `v_E,0=dim E`, `sum_i d_i v_E,i=D/f_E`, central support and finite coordinate bounds. `two_dimension_induction.py`; current integral/nonintegral campaigns. |
| Induction Gram, duality, and integer atoms | `B_ind = sum_Z v_Z v_Z^t`. Remove forced low columns; residual is entrywise nonnegative and PSD and has an integral Gram decomposition with compatible duality. This induction matrix is distinct from the regular Casimir in noncommutative input. |
| Character-labelled S reciprocity | Distinguished central entries obey `beta_E chi_E(v_F)/dim E = beta_F chi_F(v_E)/dim F`. Scalar formula omits the degree only because it is one. Project rank9–10 central reciprocity and Deshpande [12]. |
| First/second twist moments | `Tr(theta I(X))=0` for nonunit `X`, and `Tr(theta² I(X))=D nu_2(X)`. Positivity plus roots of unity gives exact mass inequalities; refine with duality and indicator signs. [7], Theorems 2.5,2.7; Ng–Schauenburg [13]. |
| Relative-trace hulls and conductor bounds | Enumerate justified cyclotomic trace packets. A cutoff in root order is valid only after a theorem bounds conductor or an all-orders convex hull has been proved. Project rational/quadratic center trace engines, weak-integral quadratic adapter. |
| Higher indicators / rotation integrality | Tensor-rotation traces and higher indicators constrain both multiplicities and phases. Project `tensor_rotation.py`, `unit_pair_constraints.py`, `higher_indicators/`. |
| Modular Galois transport / S symmetry / Verlinde | Full rows, signs, twist squares, fusion integrality and joint character spectra can constrain a hypothetical center. Applying modular restrictions to the original category requires a separate braiding/modularity theorem. |
| Norm, trace, prime-norm and dimension-block bounds | The primitive-codegree theorem above is general; Schopieray [4], Proposition4.11 and Theorem4.13 are spherical. The dimension-block local bound [10] is used without the invalid inference that rational categorical dimension implies FP dimensional grading. |
| Signed sphericalization | Enumerate every oriented sign quotient with unit, dual reversal, Frobenius reciprocity, parity and associativity. Gauge-equivalence to the source supplies a spherical section; every remaining branch needs its own obstruction. `work/general_signed/`, `work/audit_signed/`; rank11 nonintegral campaign. |

## Scoped conditions that must not be silently promoted

* The Schur-product test, primary `n`-matrix / reduced-twisted positivity, and Minkowski/support inequalities are unitary conditions [14,15]. They can exclude general categories only when every possible categorification is separately known unitarizable. One valid route is ENO solvability [11] followed by Galindo–Hong–Rowell [16], Theorem5.20.
* The Isaacs property is not a universal categorification axiom; do not use the older conjectural criterion as a general exclusion. Its failure also obstructs Morita-based blanket arguments.
* Braided generalized-near-group classifications, modular low-rank classifications, and semion/fermion centralizer criteria require actual braided hypotheses. LPR's rank-at-most-seven modular criterion does not extend to rank eleven by analogy.
* The project's minimal-image braided-Morita lemma rules out constructions from braided Morita partners under its hypotheses. It does not exclude arbitrary unbraided categories.
* A model requires a proved category, coherence/existence of each action or algebra, and an exact full tensor identification. A passed Gram system, numerical modular datum, or failed bounded search proves neither existence nor nonexistence.

## Completed additional scans in this directory

`run_cyclic.py` applied the accepted cyclic isotypic theorem to all 182 rings and produced **66** exact witnesses. Relative to the initial 97 arithmetic exclusions, the new IDs are **R11_1_13 and R11_1_71**. The complete per-input receipt, including no-witness records, is `cyclic_results.json`. `verify_cyclic_independent.py` imports no producer and independently checks group order, all fixedness premises, the exact coefficient, irreducibility, Perron-root isolation, and the scaled nonintegral minimal polynomial.

`run_compression.py` examined every quadratic factor of every rank-eleven regular Casimir and every compositum squareclass. It produced **3** general-complex witnesses: **R11_1_29, R11_1_47, R11_1_144**, all overlapping the arithmetic exclusions. The precise weaker/stronger gate and all field ratios are retained in `compression_results.json` for all182. The adapter replaces the inherited rank-eight-only scalar-character path by exact Casimir Perron-factor weak-integrality checks or transitive-invertible-action two-value checks. No rank-eight algebra decomposition is assumed at rank eleven.

The earlier project files were read but not modified. No repository or website has been published by this audit.

## Primary references checked directly

1. V. Ostrik, *On formal codegrees of fusion categories*, [arXiv:0810.3242](https://arxiv.org/abs/0810.3242).
2. P. Etingof, D. Nikshych, V. Ostrik, *On fusion categories*, [arXiv:math/0203060](https://arxiv.org/abs/math/0203060).
3. Z. Liu, S. Palcoux, Y. Ren, *Classification of Grothendieck rings of complex fusion categories of multiplicity one up to rank six*, [arXiv:2010.10264v5](https://arxiv.org/html/2010.10264v5).
4. A. Schopieray, *Norm, trace, and formal codegrees of fusion categories*, [arXiv:2005.13760](https://arxiv.org/html/2005.13760v1), especially Sections4.1–4.2.
5. P. Etingof, S. Gelaki, D. Nikshych, V. Ostrik, *Tensor Categories*, [author's final version](https://math.mit.edu/~etingof/egnobookfinal.pdf).
6. A. Schopieray, *Categorification of integral group rings extended by one dimension*, [JLMS108(2023),1617–1641](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/jlms.12789).
7. V. Ostrik, with appendix by D. Nikshych and V. Ostrik, *Pivotal fusion categories of rank3*, [arXiv:1309.4822](https://arxiv.org/pdf/1309.4822).
8. J. Liptrap, *Generalized Tambara–Yamagami categories*, [arXiv:1002.3166v2](https://arxiv.org/html/1002.3166v2).
9. Z. Liu, S. Palcoux, Y. Ren, G. Vercleyen, *Triangular Prism Equations and Categorification*, [arXiv:2203.06522v5](https://arxiv.org/pdf/2203.06522v5).
10. A. Schopieray, *The dimension block of a spherical fusion category*, [arXiv:2609.35287v1](https://arxiv.org/html/2609.35287v1), Lemma4.1.
11. P. Etingof, D. Nikshych, V. Ostrik, *Weakly group-theoretical and solvable fusion categories*, [arXiv:0809.3031](https://arxiv.org/pdf/0809.3031).
12. T. Deshpande, *On centers of bimodule categories and induction-restriction functors*, [arXiv:1611.04486](https://arxiv.org/abs/1611.04486).
13. S.-H. Ng, P. Schauenburg, *Frobenius–Schur indicators and exponents of spherical categories*, [arXiv:math/0601012](https://arxiv.org/abs/math/0601012).
14. L. Huang, Z. Liu, S. Palcoux, J. Wu, *Complete Positivity of Comultiplication and Primary Criteria for Unitary Categorification*, [arXiv:2210.00792](https://arxiv.org/html/2210.00792v1).
15. J. Lim, *Noncommutative Minkowski integral inequality and a unitary categorification criterion for fusion rings*, [arXiv:2601.13490v2](https://arxiv.org/html/2601.13490v2).
16. C. Galindo, S.-M. Hong, E. C. Rowell, *Generalized and quasi-localizations of braid group representations*, [arXiv:1105.5048](https://arxiv.org/pdf/1105.5048).

## Unified dimension-120 structural obstruction

`D120_THEORY.md` and the embeddable `D120.tex` prove general exclusions for **R11_1_40 and R11_1_82**. Two forced dimension-two constituents of I(1) generate a central Rep(D10); C2 de-equivariantization then has rank16 but must be a C5 extension of a rank4 C3+2 category. Every such neutral category is Morita equivalent to Vec_A4^Ω, whose Brauer–Picard group has no five-torsion for every Ω. All components would therefore be regular rank4 bimodules, forcing rank20. The finite verifier uses the source tensor and a complete exact character table; no frame-search completeness is needed. The twisted stabilizer statement is explicitly justified by Marshall–Nikshych arXiv:1603.04318v3, Theorem3.3 and Proposition4.5, together with the twisted Lagrangian classification of Naidu–Nikshych arXiv:0705.0665v2.

The preceding high-column Galois/Gram and rational two-twist hull relaxations were feasible for both inputs. Their JSON receipts record **no_exclusion** and are exploratory records, not part of the accepted structural proof.

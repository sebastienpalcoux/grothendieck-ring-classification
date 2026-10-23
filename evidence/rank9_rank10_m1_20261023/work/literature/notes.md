# Literature and prior-data audit for the rank-9 and rank-10 multiplicity-one inputs

## Exact prior-data identification

The public [AnyonWikiDatabase](https://github.com/anyonwiki/AnyonWikiDatabase) `AlgebraicStructures/FusionRings/mult1.json` contains all142 rank9 and194 rank10 input rings. `crosswalk.json` matches every input tensor by a based-ring isomorphism, checked coefficientwise. The database commit retrieved was `badbfe299dd533c12a84e817f5890059705e0a3c`; the mult1 blob was `c8d7b6bebe6c230dc85a16a1e29a4025e9dc58bd`. Current rank9/rank10 category metadata is empty, so this is identification evidence rather than classification evidence.

The older [AnyonWiki table](https://anyonwiki.github.io/pages/Lists/losmffr.html) supplies rank9 model leads and67 exclusion flags. `rank9_legacy_crosswalk.json` joins these to the exact input tensors. Old positive flags total22. They must be supported by constructions; a matching dimension profile alone is insufficient.

The old problematic ring FR^(9,0)_38 is exactly input **R9_1_41**, with input-to-old basis map `[0,1,2,4,6,5,8,7,3]`. Its old exclusion is only pivotal. A general exclusion requires an additional argument.

## Scope of standard criteria

Liu–Palcoux–Ren, *Classification of Grothendieck rings of complex fusion categories of multiplicity one up to rank six*, LMP112(2022)54, [arXiv:2010.10264v5](https://arxiv.org/html/2010.10264v5):

| Result | Verified scope |
|---|---|
| Thm2.1 commutative Schur positivity | unitary only |
| Thm2.3 formal-codegree divisibility by some codegree | pivotal |
| Thm2.4 FPdim/codegree divisibility | pseudo-unitary |
| Thm2.7 formal-codegree inequality | pseudo-unitary |
| Thm2.9 formal codegrees are d-numbers | arbitrary complex fusion categories |
| Thm2.11 extended cyclotomic criterion | arbitrary complex categories with commutative Grothendieck ring |
| Thm2.13 Lagrange divisibility | all fusion categories |
| Thm2.14 zero spectrum | all fusion categories |
| Thm2.15 quadratic/generalized near-group categories | Galois conjugate pseudo-unitary; hence spherical |
| Thm2.16 modularity criterion | rank at most7; cannot extend merely by analogy |

The Isaacs property in that paper was conjectural. It must not be used as a general obstruction; this project already treats its counterexamples.

Schopieray, *Categorification of integral group rings extended by one dimension*, JLMS108(2023)1617–1641, [doi:10.1112/jlms.12789](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/jlms.12789): Lem3.1 applies to all rings whose simple FP dimensions are1 and a single d, and guarantees Galois conjugate pseudo-unitarity for any categorification. Prop3.3 states that for irrational d with d²=r d+s, categorifiability forces s|r. Prop3.2: a commutative two-orbit ring with0<r<|H|-1 is not categorifiable. These are general-complex obstructions, because Lem3.1 justifies their positive-dimensional arguments.

Vercleyen–Slingerland, *On Low-Rank Multiplicity-Free Complex Fusion Categories*, CMP407(2026)231, [doi:10.1007/s00220-026-05705-2](https://link.springer.com/article/10.1007/s00220-026-05705-2): Remark4.3 singles out FR^(9,0)_38 as excluded only under pivotality. The explicit F-symbol census concerns rank≤7, and cannot directly settle the new inputs. Section4.1.1 carefully distinguishes complex, pivotal and unitary criteria and notes that some expensive d-number/cyclotomic tests were not completed. The paper must not be interpreted as proving a complete rank9 complex classification.

## Generalized Tambara–Yamagami resolution

Liptrap, *Generalized Tambara–Yamagami categories*, [arXiv:1002.3166v2](https://arxiv.org/html/1002.3166v2), supplies a complete algebraic description of feudal fusion systems. Cor4.10 forces the adjoint stabilizer H to be abelian, including ordinary TY rings as a special case. Thus nonabelian TY groups are excluded over C, without a unitary assumption.

For all14 new rank10 rings of type1^8,2², we applied Theorem4, Definition4.3 and Lemma4.11. This yields11 explicit unitary realizations and3 rigorous complex exclusions. See `gty_proof.md`; the affirmative and negative certificates have independent exact verifiers. The four affirmative matches not found by the initial standard-model search are R10_1_150,154,167,183. Negative IDs are118,122,180. This is an exact application of an existing theorem, with new per-input certificates; novelty of the categories or theorem is not asserted.

## Known Haagerup–Izumi(C5) realization

R10_1_132 is exactly the known unitary HI(C5) ring, with basis map `[0,1,4,3,2,5,8,7,9,6]` to the ordered basis α0,…,α4,α0ρ,…,α4ρ. Its rules are αgαh=αg+h, αgρ=ρα−g, and ρ²=1+Σαgρ. `hi_c5_model.py` reconstructs these rules and checks all1000 coefficients; `hi_c5_certificate.json` stores the tensor and map.

Existence was established in Izumi, *The structure of sectors associated with Longo–Rehren inclusions II: Examples*, Rev Math Phys13(2001)603–674, Example7.2. The exact Hermitian HI matrix is restated in Gannon–Schopieray–Yadav, [arXiv:2609.25185v1](https://arxiv.org/html/2609.25185v1), §7.1, formula(7.1), with rules(2.1). This known C5 category is unitary. The new all-odd-order existence result in the latter paper is only pseudo-unitary in general, with unitarity independently checked for odd orders≤43; do not conflate the two scopes.

## Other model references and leads

Vercleyen–Slingerland, *On low rank fusion rings*, JMP64(2023)091703, [arXiv:2205.15637v4](https://arxiv.org/html/2205.15637v4), describes the song fusion-ring extension family. Example5.1(4) proves existence of the non-crossed rank9 GTY ring corresponding here to R9_1_111. A transparent alternative realization found in this work is the diagonal graded pullback of Ising and Vec(S3) along parity; root verified its exact tensor.

Ordinary TY(A) models require finite abelian A and a nondegenerate symmetric bicharacter; cyclic and finite products have explicit choices. The original source is Tambara–Yamagami, JAlg209(1998)692–707, doi10.1006/jabr.1998.7558. Standard pointed categories, representation categories, Deligne products, SU(2)/PSU(2) rules, metaplectic SO(N)2 categories and coherent finite-group equivariantizations/crossed products give further models, but every identification in the deliverable should use a full tensor isomorphism and justified coherence.

Dong–Sun, *Structure, examples and classification for generalized near-group fusion categories*, JAlg568(2021)386–407, [arXiv:2004.08735](https://arxiv.org/abs/2004.08735), classifies only certain **braided** generalized-near-group families. Its braided classification is not a general no-categorification criterion for unbraided inputs.

# Independent audit of the rank-eleven models

The independent checker `model_audit.py` passes **68 construction records covering all 25 selected inputs**. It reads the frozen construction parameters and reconstructs the tensors without importing any model-discovery program. Every selected recipe is required to occur among the audited records. The input catalog hashes are recorded in `model_audit.json`.

The audited input suffixes are 1, 10, 24, 26, 28, 30, 37, 45, 46, 48, 57, 64, 68, 72, 75, 103, 105, 112, 113, 146, 150, 157, 171, 176, 182, all with prefix `R11_1_`.

For each record the checker verifies the original tensor SHA-256, a unit-preserving bijective basis map, agreement of the independently reconstructed tensor with the stored model tensor, and all 1,331 coefficients against the supplied ring. It also checks the reconstructed fusion-ring axioms. Categorical existence uses the arguments below; equality of associative integer tensors alone is not used to infer existence.

| Construction | Audited records | Categorical basis |
|---|---:|---|
| Standard SU(2) categories and even subcategories | 3 | Established unitary quantum-group categories |
| Pointed and dihedral representation categories | 3 | Standard unitary categories |
| Standard metaplectic categories or the specified fusion subcategory | 3 | Established unitary quantum-group categories |
| Tambara–Yamagami category | 1 | Explicit nondegenerate symmetric bicharacter and positive parameter |
| Strict pointed equivariantizations | 10 | Actual group-automorphism actions |
| Tambara–Yamagami equivariantizations | 28 | Orthogonal automorphisms and coherent parity choices |
| Associative C2 zests | 12 | Central lifts and vanishing scalar H4 obstruction |
| SO(8)_2 zests by V4 | 4 | Neutral Tannakian coefficient objects, trivial obstruction |
| SU(2)_6 spin-current equivariantizations | 2 | Exact tensorator and action-coherence checks |
| Twisted cyclic pointed equivariantizations | 2 | Exact 3-cocycle, tensorator and action-coherence checks |

## SU(2)_6 spin-current action: inputs 24 and 68

The established unitary SU(2)_6 category is used with its standard real quantum-Racah associator. The audit independently evaluates that formula; it does not re-use the discovery program's cached F-symbols, linear-system solver, or tensor calculator. It works in Q(u), where u is the unique root of u^4−4u^2+2 in (1847759/10^6,1847760/10^6). Exact root counting verifies this interval, and rational interval refinement certifies all signs.

The squared F-symbols belong to this field. Squared magnitudes together with the exact signs determine the actual real F-symbols. For each action the checker verifies all **1,664 nonzero transformed F equations and 16 zero entries**. The quantum integers [1],...,[7] are positive and [8]=0. Every Racah denominator index is checked to lie between 0 and 7, including terms whose numerator contains [8] and therefore vanishes.

The tensorator is normalized on the unit and specified on all 84 admissible fusion channels. The permutation is checked to be an involutive based-ring automorphism. All 84 equations expressing monoidality of the natural isomorphism F²→Id are checked, together with its invariance under F, which is the remaining C2 group-associativity coherence. Thus the computation verifies a coherent categorical action, rather than only a permutation of labels. The choices μ=1 and μ_a=(−1)^a give inputs 68 and 24 respectively.

Equivariantization is independently recomputed using **orbits of fusion-channel bases**. For a fixed output, a free channel orbit contributes one invariant; a fixed channel contributes one exactly when its action eigenvalue is +1. For a free output orbit, its chosen representative has trivial stabilizer. The complete list of object orbits and both projective-stabilizer characters at every fixed object is checked. This method differs from the character-trace formula used in model discovery.

The base associator's pentagon and unitarity come from the established SU(2) construction. The finite calculation verifies the additional monoidal functor and C2-action equations required for these models.

## Twisted cyclic pointed action: inputs 48 and 146

Take residues in C16 and the normalized cocycle ω(a,b,c)=ζ16^(a floor((b+c)/16)). The two involutions are a↦15a and a↦7a. The audit reads the explicit J and μ cochains and checks, separately for each action:

- all 65,536 3-cocycle equations;
- all 4,096 monoidal-functor associativity equations;
- all 256 equations for monoidality of F²→Id;
- all 16 group-associativity equations μ(F(a))=μ(a), as well as units and the involutive group automorphism.

The tensorator convention is J:F(a)⊗F(b)→F(a⊗b). Accordingly δJ=ω/F*ω, and the tensor product of equivariance maps uses J^−1. The independent orbit calculation uses this inverse; it is not inferred by forcing an associative fusion tensor. All values are roots of unity, so the resulting action and equivariantization are unitary. Complete orbit/stabilizer labels and every coefficient match inputs 48 and 146.

## SO(8)_2 and V4 zesting: inputs 30, 57, 105 and 150

The base tensor is reconstructed from the explicit SO(8)_2 formulas. The grading is verified on every nonzero product, is faithful onto V4, and places every coefficient object in the neutral component. Each stored λ is a normalized invertible-object 2-cocycle, checked on all 64 triples. Multiplication by its values is checked to be an invertible-object permutation. The entire zested tensor is then rebuilt.

The pointed subcategory of SO(8)_2 is Tannakian: its four invertibles are bosons and centralize one another. In a coherent symmetric gauge equivalent to Rep(V4), the associator and mutual braiding on these coefficient objects are trivial. Their ambient braiding supplies central lifts. The associative-zesting 4-cocycle, built from these associators and mutual braidings, is therefore identically one. The scalar correction may be chosen identically one, giving unitary associative zests for all stored λ. The invertibles need not be transparent to every object of the ambient modular category; that stronger and false claim is not used.

For each C2 zest in the standard records, the independently reconstructed base is an actual braided unitary category, its grading is checked, and its neutral coefficient is an order-two invertible. The associative-zesting obstruction lies in H4(C2,U(1))=0, so a unitary scalar correction exists. No braided structure on the zested category is asserted or needed.

## Tambara–Yamagami and strict pointed actions

For every TY action the audit reconstructs the finite abelian group and the TY tensor. It checks the displayed bicharacter's symmetry, nondegeneracy, multiplicativity and invariance under the automorphism, as well as the automorphism's group law and finite order. These properties preserve all coefficients of the standard TY associator, giving the claimed strict tensor action. The parity function is independently checked to be a tensor natural automorphism and to satisfy the allowed cyclic coherence. Complete orbit/stabilizer labels are checked. Fusion multiplicities are obtained by counting channel cycles whose accumulated phase is trivial, independently of the discovery Fourier projections.

For strict pointed equivariantizations, the audit verifies the entire group table, unit, inverses, associativity, and the involutive group automorphism. This directly defines a strict tensor action on the standard unitary pointed category. Dihedral representation tensors are separately derived from exact character inner products using cyclic frequencies, rather than importing the discovery formulas.

## Reproduction and sources

Run from the package root:

```sh
python -O work/rank11/arithmetic/model_audit.py
```

The final output is `PASS 68 construction checks 25 distinct ids`. Verification conditions use explicit exceptions and remain active under Python optimization. The audit found no categorical coherence gap in the accepted 25 constructions. It proves existence for these records; it makes no assertion that their associators or categorical realizations are unique.

Primary sources used for the mathematical audit:

1. C. Delaney, C. Galindo, J. Y. Plavnik, E. C. Rowell and Q. Zhang, *Braided zesting and its applications*, Proposition 3.9, Remark 3.10 and Section 6.2: https://arxiv.org/html/2005.05544v2 . These give the H4 obstruction, its vanishing for cyclic grading, and the trivial obstruction for Tannakian coefficients.
2. P. Gustafson, E. C. Rowell and Y. Ruan, *Metaplectic Categories, Gauging and Property F*, Sections 3.1 and 3.3: https://arxiv.org/html/1808.00698v3 . These give the metaplectic fusion formulas, gradings and bosons used above.
3. Y. U. Taylor and C. T. Woodward, authors' quantum-6j formulas and implementation: https://sites.math.rutgers.edu/~ctw/6j.html . The quantum-integer, triangle and Racah-sum expressions agree with the gauge used in the independent evaluator, after the usual doubled-spin relabeling and recoupling normalization.
4. D. Tambara and S. Yamagami, *Tensor categories with fusion rules of self-duality for finite abelian groups*, J. Algebra 209 (1998), 692–707, Theorem 1; DOI https://doi.org/10.1006/jabr.1998.7558 . The invariant-bicharacter argument acts directly on their standard associator.
5. S. Burciu and S. Natale, *Fusion rules of equivariantizations of fusion categories*, corrected v2: https://arxiv.org/abs/1206.6625v2 . The independent calculation uses the underlying orbit/stabilizer and invariant-Hom-space description.

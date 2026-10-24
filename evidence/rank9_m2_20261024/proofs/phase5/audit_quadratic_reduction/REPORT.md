# Independent audit of the TY-origin D8 Morita reduction

**Verdict: PASS, including the subsequent associator refinement.** Every hypothetical complex categorification of `R9_2_137`, `R9_2_1607`, or `R9_2_1976` gives a rank-twelve Morita dual with eight D8 invertibles and four simples of dimension `d=4+3√2`. The complete based-ring calculation gives 28 labelled possibilities. The established field and lower-rank exclusions leave three abstract based-ring types. The additional theorem in `FORCED_D8_ASSOCIATOR.md` excludes the nonidentity quotient-action type **for these TY-origin duals**, leaving two identity-action types.

This is a necessary existence reduction. It constructs no associator for either survivor, proves no new source-ring categorification, and does not prove that the source categories are mutually Morita equivalent. The three source rings remain unresolved.

Files audited:

- `phase5/quadratic_comm/ty_module_subtask/THEOREM.md`
- `phase5/quadratic_comm/ty_module_subtask/DUAL_COMPLETION.md`
- `phase5/quadratic_comm/ty_module_subtask/FORCED_D8_ASSOCIATOR.md`
- Their exact input tensors, module actions, completion lists, filters, and transports.

The independent implementation `independent_checks.py` imports none of the author's discovery functions. It rebuilds the fixed-object module branch, full Gram matrix, exhaustive right-action domain, and all completions. It deliberately **does not use** the author's multiplicity-invariance prefilters: it enumerates every quotient automorphism, every α, and every weak composition of eight, then checks the full action and fusion axioms. The receipt is `independent_checks.json`.

## 1. The categorical TY reduction

The source integral subcategory has precisely the TY(V4) based ring. The Tambara–Yamagami classification applies over C without a pivotal or unitary hypothesis. Its pointed associator is trivializable; this is also forced by the rank-one module furnished by the unique noninvertible TY object.

The four nonintegral source simples form an indecomposable left module category over TY. Their two V4 orbits have distinct order-two stabilizers H1,H2, and the dimension-two object exchanges those orbits as stated. These are source-tensor facts, independently checked.

For a simple in the first orbit, the internal end in TY has underlying object `1+h1`: no dimension-two contribution occurs because its action goes to the other orbit. The internal end is a connected separable algebra. Its subgroup multiplication is nonzero, and H²(C2,C*)=0 removes the only two-cocycle choice. Hence the entire indecomposable module is the subgroup-induced module `Mod_TY(C[H1])`.

I checked the perpendicular-stabilizer calculation directly in [Meir–Musicantov, arXiv:1010.4333](https://arxiv.org/abs/1010.4333), Section 9.2 and Lemma 9.1. Left tensoring a Y-supported module by a changes its right H1-character by χ(a,−). Its stabilizer is therefore H1-perp. The two observed distinct lines force χ to be nonalternating, with diagonal values `(1,−1,−1,1)` in basis `(0,h1,h2,h1h2)`. Thus `g=h1h2` is the unique nonidentity isotropic element. It acts freely on the four nonintegral simples.

The algebra for the pointed dual is `A=1+g`, not the anisotropic internal end used to identify χ. This distinction in the proof is correct.

## 2. The pointed group really is D8 for both tau signs

For L=<g>=L-perp, the G-supported A-bimodules form the four-element group `(G/L)×L-hat`. The Y-supported bimodules have scalar commuting left and right L-actions, because χ(g,g)=1, giving four more invertibles. All have underlying dimension two and normalized bimodule dimension one.

The Meir–Musicantov formulas in Sections 9.3–9.5 give a Y-supported invertible s with both actions trivial. Setting the subgroup cocycle, the function ν, and the representatives t_h to one gives `s²=1`. The conjugation formula interchanges the two coordinates of `(G/L)×L-hat` under the nondegenerate quotient pairing. Hence the group is `V4 ⋊ C2`, with the swapping action, i.e. D8. This is not an inference from a five-object fusion ring or a guess between D8 and Q8.

The parameter τ affects the next associator obstruction; it does not enter this group multiplication calculation. Therefore both signs τ=±1/2 are covered. No trivial associator on the full pointed D8 subcategory is asserted.

## 3. All twelve simples and their actions are accounted for

In the nonintegral sector, g acts freely, giving two simple right A-modules with underlying objects `X+gX`. Each is stabilized under left multiplication by g: that functor preserves its underlying orbit, and there is only one simple right A-module on that free orbit. The resulting genuine C2 action on the module category allows two projective equivariant structures on each stabilized simple, since H²(C2,C*)=0. Thus there are four A-bimodule simples, each of dimension d. This reasoning addresses left-action existence and multiplicity, rather than merely assuming that every right module has two extensions.

Together with the pointed sector the dual has type `(1^8,d^4)`, whose total dimension is the source dimension. The irrationality of d forces the invertible action to be transitive: a product between different orbits would have no invertible term and would give `d²=nd`. The stabilizer is consequently of order two and normal. D8 has only one normal subgroup of order two, its center. These steps agree with [Schopieray, arXiv:2208.07319](https://arxiv.org/abs/2208.07319), Lemmas 2.6 and 2.8.

The independent fixed-block search has only scalar variables, because Y is the sole g-fixed source simple. Enumerating every parity-allowed scalar value gives precisely one branch for each source. Reconstructing every module coefficient gives the saved six-object module in each case.

The full Morita Gram identity is a consequence of associativity and Frobenius reciprocity in the two-object Morita linking multifusion category. It uses ordinary nonnegative multiplicities, not spherical dimensions. Every right-action vector lies in the Gram image, is nonnegative integral, and satisfies the coordinate-product bounds. Its first row and column belong to the complete restriction domain from `1+M_g=2I6`. The independent enumeration uses these necessary constraints with no node cutoff and recovers exactly ten distinct matrices. The unique Gram weights are eight ones and two twos: the two repeated matrices must represent four separate simples.

## 4. Full quotient-action and fusion-ring exhaustiveness

Let H=Z(D8), Q=D8/H=V4, and choose X=X0. Left and right invertible actions commute, both act transitively, and have the same stabilizer. Thus there is an automorphism θ of Q with `Xg=X_(θ(gH))`. If `X*=X_α`, duality forces θ²=id and θ(α)=α. The invertible part of X² is exactly the coset α, by Frobenius reciprocity. Irrational dimension then forces the noninvertible multiplicities to sum to eight. Consequently every product is specified by θ, α, and this four-entry nonnegative vector m.

I independently derived the necessary invariances used by the author:

- Comparing the invertible coefficients of `(X²)X` and `X(X²)` gives invariance under θ.
- Duality of X² then gives translation invariance by α.
- Comparing `(X²)g` and `X(Xg)` gives invariance under every element of `im(1+θ)`.

The independent program omits all three prefilters, so a mistake in their derivation could not remove a completion from the audit's search. It considers all six automorphisms of Q, tests their full right-action matrices, enumerates every α and every weak composition of eight, and checks all products against the module, duality, Frobenius reciprocity and all 20,736 associativity equations. The resulting tensors agree exactly with the author's 28, including all coefficients.

The 28-case parametrization is therefore exhaustive relative to the forced module action. It is not a classification of associators.

## 5. Field pruning and lower-rank dependencies have the stated scope

The field pruning is valid in pseudo-unitary scope: for each irreducible ring representation E, its distinguished central simple has dimension `FPdim(C')/f_E`. Forgetting it puts its dimension in Q(√2), so every formal codegree lies in that field. The regular Casimir eigenvalue is `dim(E) f_E`, with an integer scaling; it has the same field obstruction. Thus using this eigenvalue does not confuse representation dimension with the dimension of the central simple.

The 20 rejected cases have precisely the foreign factors listed in `DUAL_COMPLETION.md`. The explicit scalar-character calculation gives discriminant fields Q(√3), Q(√6), or Q(√11); the independent regular-Casimir calculation reproduces the same rejection set.

For the general existence statement, the proof correctly uses the previously audited source-specific Galois reduction first. The exact artifacts are:

- `phase2/signed/gate_R9_2_137.json`
- `phase2/signed/gate_R9_2_1607.json`
- `phase2/signed/gate_R9_2_1976.json`

Their categorical foundations were audited in `phase3/audit_signed_so3/AUDIT.md`; previous full replays are retained in phase 3. The independent receipt here checks each gate's complete outcome and exact source-tensor hash. The gate produces a possibly different, Galois-conjugate pseudo-unitary categorification with the same based ring. Its Morita dual is pseudo-unitary. The argument does **not** assert that every original categorification is pseudo-unitary or unitary.

All four corner cases contain the advertised adjoint subrings. The independent audit checks all 216 coefficients of each transport. The copied decisions for `R6_4_6` and `R6_4_174` explicitly have general scope and retain their full earlier certificates. Those established lower-rank results are dependencies, not newly reproved by this audit. Neither is the disputed spherical near-group argument for `R8_3_436`.

Before using associator information, the four labelled survivors have exactly three based-ring types. Every supplied cross-source transport is checked on all 1,728 coefficients. The numbers of self-dual simples, 10,6,8, distinguish the three types. Cases 26 and 27 are isomorphic, as claimed. No assertion of categorifiability follows from these transports.

## 6. The new forced-associator obstruction also passes

I independently identified the same weighted-fourth-indicator argument before reading the finished `FORCED_D8_ASSOCIATOR.md`, and then checked its primary sources.

[Shimizu, arXiv:1005.4500](https://arxiv.org/abs/1005.4500), Theorem 3.4 and the following fourth-indicator specialization, gives ν4(Y)=0 for the nonalternating V4 form, independently of the sign of τ. Thus the dimension-weighted fourth indicator of TY is four.

The weighted indicator is Morita invariant for the two integral categories involved. Summing [Ng–Schauenburg, arXiv:math/0601012](https://arxiv.org/abs/math/0601012), Theorem 4.1, with dimension weights expresses it through the dimensions and twists in the center. Morita equivalence preserves the braided center and its canonical positive pivotal structure. This argument uses positive structures only on the dimension-eight TY category and its pointed dual, not on an arbitrary larger ambient category.

In D8, the six elements of order at most two have fourth indicator one. The inverse rotations have equal indicators (Ng–Schauenburg Remark 4.2), so the common value is `(4−6)/2=−1`. The cyclic calculation preceding their Lemma 9.3 identifies this with class two in H³(C4,C*).

For the nonidentity θ cases, a rotation r of order four and a reflection s of order two satisfy `rX=Xs`. Hence `(r,s)` fixes X under the pointed action of `P⊠P^rev` and generates a cyclic order-four stabilizer. A rank-one module over a pointed category requires its associator class to restrict trivially to that stabilizer: the chosen intertwiner scalars give the required two-cochain in the module pentagon.

The first projection contributes class two. The second factors through C4→C2 and contributes zero, including any reversed/inverted associator convention. The explicit β in the author proof does trivialize the pullback of the nontrivial C2 cocycle; the independent program checks all 64 values. It also checks the class-two C4 cocycle on all 256 quadruples and its nontrivial cyclic invariant. The six source-labelled rotation/reflection relations and their induction overlaps are independently verified.

The resulting class `2+0` cannot be trivial. Therefore cases 26 and 27 cannot be the Morita duals arising from these sources. This is an **all-complex** module-associativity obstruction. It does not exclude every hypothetical categorification of the abstract rank-twelve ring with a different pointed associator. The two remaining TY-origin types are cases 12 and 25, both with θ=id and uniform multiplicity two.

## 7. The proposed order-32 near-group route remains only a model direction

The numerical match to an isotropic subgroup of order four in an order-32 near-group source is plausible: its noninvertible dimension is `16+12√2=4d`. It does not supply any of the required models by itself.

The direct isotropic orbifold formula has an abelian quotient group of invertibles, whereas the necessary duals have D8 invertibles. Thus a further categorical move is required. For the concrete `C8×C4` datum discussed in `phase5/quadratic_noncomm/REPORT.md`, the proposed image of the canonical near-group algebra, `1+Σ_(i=1)^4 X_i`, has a forced twelve-object module category. The displayed Gram factor implies this exactly: the eight orthogonal unit-norm rows force eight columns, and the remaining block after subtraction is I4. In a Morita linking category, its module rank twelve gives `12²≤12·rank(dual)`, so that move cannot produce a rank-nine dual. The stated additional invertible-action obstruction also distinguishes this abelian route from the required D8 frontier.

These are limitations of that particular construction, not general exclusions. A different nonintegral algebra, a different source, or multiple Morita moves might behave differently. Existence of a near-group category and a feasible based-ring formula do not alone prove that the needed orbifold algebra or subsequent associators exist. The separate orbifold-scope work remains an explicit prerequisite for extending unitary formulas to an algebraic nonunitary source.

## Replay

```sh
python rank9_m2_research/phase5/audit_quadratic_reduction/independent_checks.py
```

The output is PASS for each source and for the complete independent audit. The receipt binds the three author theorem files by SHA256 and records the exact Galois-gate dependencies, finite enumeration statistics, and new cyclic-stabilizer witnesses. Only this audit directory was written; no source evidence, repositories, or online material was changed.

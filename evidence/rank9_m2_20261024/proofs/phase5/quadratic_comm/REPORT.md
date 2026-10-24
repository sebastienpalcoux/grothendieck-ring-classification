# Rank-nine commutative quadratic continuation

**R9_2_137, R9_2_1607 and R9_2_1976 remain unresolved.** This continuation gives a uniform categorical reduction to two common rank-twelve D8 based rings, with a forced restriction on their pointed associators. It supplies neither associators for the survivors nor a contradiction for them. No repository or website was changed.

The distinction between a categorical theorem and a finite ring certificate is maintained throughout. The new TY and pointed-associator arguments apply to arbitrary complex fusion categories. The formal-codegree pruning uses the already audited existence reduction to pseudo-unitary categorifications; it does not assert that every original category is pseudo-unitary or unitarizable.

## 1. The unconditional TY reduction

Put d=4+3√2. Each source has four invertibles V4, one dimension-two simple Y, and four dimension-d simples. The integral subcategory is a Tambara–Yamagami category TY(V4,χ,τ).

Its nonintegral module has two V4 orbits of size two, with different order-two stabilizers H1 and H2. The TY module formulas identify H2 with H1-perp. Thus χ must be the nonalternating bicharacter. Its two anisotropic involutions are the stabilizer generators h1,h2, and its unique nontrivial isotropic involution g=h1h2 acts freely on the four large simples.

| Source | Y | Free isotropic g | Large-orbit stabilizers |
|---|---:|---:|---|
| R9_2_137 | b8 | b1 | ⟨b7⟩, ⟨b2⟩ |
| R9_2_1607 | b3 | b5 | ⟨b4⟩, ⟨b6⟩ |
| R9_2_1976 | b5 | b8 | ⟨b6⟩, ⟨b7⟩ |

All basis indices are zero-based. The algebra 1+g exists inside the pointed subcategory. Its bimodule dual has eight invertibles forming D8 and four dimension-d simples, transitively permuted with stabilizer Z(D8). Both signs τ=±1/2 are retained. This is a Morita dual, not a de-equivariantization: no half-braiding for g is assumed.

Proof and exact inputs: `ty_module_subtask/THEOREM.md`, `structure_certificate.json`, and the three locally copied source tensors in `source_dependencies.json`.

## 2. Complete finite dual-ring reduction

The full Morita Gram calculation has one rank-six module branch for each source. Its ten distinct action matrices represent twelve dual simples, because two noninvertible action matrices each occur twice. The complete two-orbit reconstruction produces 28 labelled D8 rings per source; all possible quotient involutions, duality shifts and nonnegative multiplicities are included.

Twenty candidates violate the formal-codegree field Q(√2). Four further candidates contain previously general-excluded rank-six adjoint subrings R6_4_6 or R6_4_174. Their full tensor transports and prior decision certificates are preserved in `ty_module_subtask/lower_rank_dependencies.json`. This continuation verifies those bindings and explicitly relies on the earlier categorical lower-rank proofs.

The four initially surviving labelled cases, numbered 12,25,26,27, give three common isomorphism types. The coefficient-level maps are in `survivor_isomorphisms.json`. Equal regular-Casimir polynomials do not mean equal formal-codegree multiplicities; these were separately resolved in `survivor_formal_codegrees.json`.

Detailed completeness argument: `ty_module_subtask/DUAL_COMPLETION.md`. Its three-type conclusion is refined by the next theorem.

## 3. New general-complex associator obstruction

For either τ sign, the nonalternating TY category has weighted fourth Frobenius–Schur indicator 4. Morita invariance transfers this number to the pointed D8 dual. The six elements of order at most two contribute 6, so each order-four rotation r has ν4(r)=−1. Equivalently, the pointed associator restricts to class 2 in H³(⟨r⟩,C*)=Z/4.

Suppose a simple X satisfies rX=Xs for an order-two invertible s. The element (r,s) of the left-right acting group fixes X and has order four. The module pentagon requires the acting associator to restrict trivially to this cyclic stabilizer. Its rotation contribution has class 2. Its reflection contribution pulls back from C2 along C4→C2 and is zero; an explicit two-cochain certifies this on all 64 triples. This is a contradiction.

The nonidentity quotient-action cases 26 and 27 have exactly this forbidden relation. They are therefore excluded **as duals with the forced TY-origin pointed associator**, without any positive or unitary structure on the ambient category. This is not a blanket exclusion of the abstract based ring with arbitrary pointed associators.

Proof: `ty_module_subtask/FORCED_D8_ASSOCIATOR.md`. Exact finite checks: `forced_associator_check.py` and `forced_associator_certificate.json`. The canonical positive structures used to compute the indicator belong only to the dimension-eight TY category and its pointed dual; their use does not import unitarity into the unknown source category.

## 4. The two remaining common types

Write H=Z(D8), Q=D8/H=V4 and label the four large objects X_q by Q. Both surviving types have trivial left-right quotient automorphism and uniform large multiplicity two:

g X_q = X_q g = X_(q+gH),

X_a X_b = Σ_(gH=a+b+α) g + 2 Σ_(q∈Q) X_q.

| Stored representative | α | Self-dual basis elements | Status |
|---|---|---:|---|
| R9_2_137 candidate 12 | 0 | 10 | Unresolved |
| R9_2_137 candidate 25 | A specified reflection coset h≠0 | 6 | Unresolved |

The second is also isomorphic to the uniform `alpha=2,a=2` candidate arising from R9_2_1975. This is a common necessary dual-ring frontier. It does not show that the source categories exist, that they are categorically Morita equivalent, or that constructing one arbitrary categorification of a survivor reconstructs every source.

The exact unresolved problem is whether either of these uniform D8 rings admits compatible associators with the forced pointed restrictions and the required inverse Morita module. No current computation supplies such associators, and no accepted obstruction eliminates these two possibilities.

## 5. Conditional central-lift reduction and its limitation

If the free involution g has a half-braiding on the whole source category, its lift is a boson: trivial universal grading makes the lift have order two, and its TY self-braiding is χ(g,g)=1. De-equivariantization would have rank six, four invertibles V4 or C4, and two self-dual dimension-d objects X,Y, with

X²=Y²=1+h+4X+4Y,   XY=u+hu+4X+4Y.

Both quotient tensors and all six source-to-quotient coefficient maps pass exact verification. The half-braiding itself has not been established. In the V4 case this is R(4,4), expressly still unconstructed in Meng–Yu, arXiv:2608.06064; the announced C4 classification is not an available result. In particular {1,h,X} is not closed, so replacing this ring by the near-group ring C2+8 would be invalid.

See `CENTRAL_LIFT_REDUCTION.md` and `central_lift_reduction_certificate.json`. A fermionic central lift of an anisotropic involution cannot be treated as a transparent fermion in a braided category.

## 6. Current literature and model-route checks

The recent Radchenko–Wheeler construction, arXiv:2609.21892, supplies algebraic near-group categories for all two-generator abelian groups, including the order-32 groups relevant to δ=4d. The recent He–Liu–Lu–Palcoux–Ren construction, arXiv:2610.11652, supplies cyclic near-group examples with spherical reconstruction and Galois/pseudo-unitary results. Their separate unitarity conjecture is not a theorem. These sources improve the model search but do not immediately supply any of the three rank-nine tensors.

An isotropic order-four orbifold of an order-32 near-group example is a natural dimension match: it would have eight invertibles and four dimension-d objects. Izumi's published C* orbifold construction cannot simply be applied to a nonunitary algebraic example without verifying its construction in that setting. The precise algebraic-extension issue is recorded by the parallel noncommutative research; no resulting model is claimed here.

There is also a structural obstruction to obtaining our forced D8 integral subcategory merely by further pointed Morita operations on an abelian rank-eight quotient. A pointed category on a two-generator abelian group of order eight has pointed Drinfeld center for every three-cocycle (the alternating Type-III contribution is absent). A pointed category on D8 has a nonpointed center: the identity conjugacy class already contains the degree-two ordinary representation of D8. They cannot be categorically Morita equivalent. This blocks that pointed-only construction route; it does not rule out algebras with nonintegral summands.

A proposed algebra 1+ΣX_q in a uniform rank-twelve quotient has an exact rank-twelve induction module. The general Morita rank inequality rank(M)²≤rank(C)rank(C*) then forces its dual rank to be at least twelve, so this particular move cannot produce a rank-nine category. Its additional model implications are kept separate from the accepted D8 reduction. A commuting based permutation matrix alone is not an actual categorical invertible module functor: coherence must still be proved.

The short appendix `ALGEBRA_WITH_TRIVIAL_INTEGRAL_PART.md` proves a broader limitation by integer Gram identities: any connected separable algebra in such a uniform ring whose integral part is only 1 has underlying object 1 or 1+ΣX_q. Thus every nontrivial algebra with that particular integral part is blocked as a direct route to rank nine. Algebras containing additional invertible summands and longer chains of Morita moves remain outside this lemma. This appendix is supplementary to the independently audited source-to-D8 reduction and makes no new source classification decision.

Primary sources checked for these boundaries:

- Meir–Musicantov, *Module categories over graded fusion categories*, sections on Tambara–Yamagami categories: https://arxiv.org/pdf/1010.4333.
- Shimizu, *Frobenius–Schur indicators in Tambara–Yamagami categories*, Theorem 3.4: https://arxiv.org/pdf/1005.4500.
- Ng–Schauenburg, *Frobenius–Schur indicators and exponents of spherical categories*, Theorem 4.1 and the cyclic pointed calculation: https://arxiv.org/pdf/math/0601012.
- Ostrik, *Module categories over the Drinfeld double of a finite group*, Example 2.1: https://arxiv.org/pdf/math/0202130.
- Meng–Yu, rank-six V4-quadratic classification and open R(4,4) discussion: https://arxiv.org/pdf/2608.06064.
- Radchenko–Wheeler, *Real quadratic fields and finite quantum dilogarithms I*: https://arxiv.org/pdf/2609.21892.
- He–Liu–Lu–Palcoux–Ren, *Triangular prism equations for near-group categories: algebraic solutions and a unitary conjecture*: https://arxiv.org/pdf/2610.11652.

## 7. Portable verification and precise scope

From any working directory, run:

    python -S /path/to/quadratic_comm/verify_packaged_records.py
    python -S /path/to/quadratic_comm/ty_module_subtask/forced_associator_check.py

Both use only the Python standard library and files inside this directory. The first rechecks all source tensors, 84 dual tensors and their module actions, explicit foreign-field witnesses, lower-rank tensor transports, the common isomorphism maps, and the six conditional quotient maps. The second checks the new cohomological witness and all forbidden rotation/reflection relations. Receipts are `packaged_records_receipt.json` and `forced_associator_certificate.json`.

The separate adversarial audit in `../audit_quadratic_reduction/REPORT.md` passed the categorical reductions, the unpruned 28-case enumeration, the existence-gate scope, the copied lower-rank transports, and the new three-to-two-type associator refinement. Its finite enumeration independently omits the author's multiplicity-invariance prefilters and reaches the same list.

The original search generators are retained as research provenance; some import the wider research tree and third-party packages. They are not required for this portable stored-certificate replay. Exact finite checks validate the stated algebraic data. They do not replace the categorical proofs or assert an associator exists for a surviving based ring.

The prior nonbraided exclusions for all three sources remain valid. This continuation makes **zero new source-ring exclusions and zero new source-ring models**. It unifies three unresolved source problems into the two constrained D8 possibilities above.

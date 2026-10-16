# Final adversarial audit of the R24 global torus argument

**Verdict: the common-chart, full-associator-weight, and tensor-functor-rigidity argument passes this independent audit.** I found no substantive gap in Sections 2–5 of `R24_TORUS_RIGIDITY_PROOF.md`. Both determinant cases for the second multiplicity space are covered. The torus constructed in the proof gives genuinely different tensor functors modulo tensor natural isomorphism; it is not merely a family of coordinate descriptions.

This audit is AI-generated research; independent human verification and Lean formalization remain pending. No canonical manuscript, categorification ledger, repository, or website was edited.

## Scope and source

Reviewed source SHA-256:

`3492f0ab0679286f8f15fec4a8c0ac5fa46277cebf240ea250b82a67a666863c`.

I first reconstructed the global argument directly from the proposed proof, then read the earlier typed audits. I independently checked the primary ENO source: Etingof–Nikshych–Ostrik, *On fusion categories*, Annals of Mathematics 162 (2005), Theorem 2.31, printed p. 592:

https://annals.math.princeton.edu/wp-content/uploads/annals-v162-n2-p01.pdf

The theorem gives finiteness of tensor functors, up to equivalence, between fixed source and target multi-fusion categories. It applies to the unital tensor autoequivalences of the fixed complex fusion category constructed below. It does not require a unitary category.

The local typed sign calculation and the conductor/indicator reduction are separate premises. In particular, this audit does not independently reprove the conductor-equality lemma or the signed indicator identity in Section 0. The global argument uses the local conclusion that the inner action `K` on `H = Hom(r r,r)` is non-scalar, with two opposite eigenvalues, and the typed covariance formula with the crossing scalar. I checked the compatibility of those conclusions with the common charts and the square-root comparison.

## 1. A common word chart exists

Let `T_2(X,Y):T(X) T(Y) -> T(XY)` be the tensorator. Fix the unit chart and choose simple charts `q_g:T(g)->g`, `q_r:T(r)->r`. On tensor words in `g,r`, define recursively

    q_(XY) = (q_X tensor q_Y) T_2(X,Y)^(-1).

Tensor coherence makes the construction compatible with reassociation in a strict monoidal realization. The transported action

    T_tilde(f) = q_Y T(f) q_X^(-1),    f:X->Y,

is strictly monoidal on these tensor words. Defining `s` to be the actual simple object `gr` and taking `q_s=q_(gr)` gives precisely the common chart required in the proof.

Rescaling `q_g` or `q_r` multiplies the transported evaluation by the inverse square of that scalar. The relevant evaluation spaces are one-dimensional, and their images are nonzero. Independent square-root rescalings therefore fix `e:gg->1` and `ev_r:rr->1` simultaneously over the complex numbers. Coevaluations are then fixed by the snake identities. This does not demand that the pivotal structure be strictly the identity.

The crossing `c:gr->rg` is multiplied by some scalar `alpha`. Its scalar does not change under either of the above rescalings, since its source and target have the same two letters. Applying the transported functor to the double-crossing identity gives `alpha^2=1`. If `alpha=-1`, the covariance equation makes `T_H` interchange the two `K` eigenlines. Its square is then scalar. A tensor natural isomorphism `T^2 -> Ad(g)` identifies the two actions on `H` projectively, since its component on the simple `r` is scalar. Consequently this case is impossible.

For `alpha=1`, every composite made from `e,c,ev_r`, their inverse isomorphisms, the cups, and identities is fixed in one and the same word chart. In particular the displayed evaluation of `s` is fixed. The intrinsic transpose forms on `H` and `J=Hom(rr,s)` are therefore simultaneously preserved. The positive indicators of `r,s` make these forms symmetric; no Hermitian positivity is used.

## 2. All thin channels and all thick transports are accounted for

I checked the domain and codomain of every `A_ab` and `B_abc` in Section 3. They are nonzero isomorphisms, and all their constituents are fixed in the word chart above.

For completeness, bases for the thin channels can be listed explicitly:

- `g_a g_b -> g_(a+b)` uses an identity or `e`.
- `g_a r_b -> r_(a+b)` uses an identity or `e tensor id_r`.
- `r_a g_b -> r_(a+b)` uses an identity, `c^(-1)`, or `(e tensor id_r)(id_g tensor c^(-1))`.
- `r_a r_b -> g_(a+b)` is `(id_g_(a+b) tensor ev_r) A_ab`.

Thus every thin eigenvalue is exactly one. No independent scalar character remains on an invertible or mixed thin vertex.

For a thick channel, tensoring by the invertible `g_(a+b)` is an equivalence. Composing with `A_ab` and `B_abc` gives a linear isomorphism from `H` or `J` onto the desired fusion space. Since these structural maps are fixed, the transported basis has exactly the same action as its source `H` or `J` basis. One transport is chosen for each fusion space. The proof does not need, and does not claim, that different structural transport paths agree.

Composition-dual incoming bases carry inverse eigenvalues: applying the tensor functor to a projection followed by its dual inclusion preserves their identity composite. This is ordinary composition duality, not a Hermitian or anti-linear operation.

**Small wording clarification:** “Every map in (12) is fixed by T” should read “Every structural transport map in (12) is fixed by T.” The variable `f` is not fixed; it carries the specified `H` or `J` action. The surrounding argument already uses the latter meaning.

## 3. The determinant split is complete

A two-dimensional complex orthogonal transformation of determinant minus one squares to the identity. Since the projective square of `T_H` is the nontrivial involution `[K]`, `det(T_H)=1`. In a hyperbolic basis,

    T_H = diag(u,u^(-1)),    u^4=-1.

The second multiplicity space has exactly two possibilities:

- Determinant one: a hyperbolic basis gives `T_J=diag(v,v^(-1))`.
- Determinant minus one: an eigenbasis gives `T_J=diag(1,-1)`.

There is no missing nonsemisimple case. Over the complex numbers, the determinant-one group of a nondegenerate two-dimensional symmetric form is a one-dimensional torus. In the other component the square is the identity and the two eigenvalues are distinct.

## 4. Every F entry has the stated weight bound

An associator entry uses four trivalent vertices and six labelled edges. At an allowed vertex, the number of noninvertible incident edges is zero, two, or three. The thick vertices are exactly those with three. Counting incidences over the tetrahedral pattern shows that the number of thick vertices is even.

At a thin or `H` vertex, the sum modulo two of the three `g` bits is zero; at a `J` vertex it is one. Each edge occurs twice across the four vertices, so the number of `J` vertices is even. Hence the number of `H` vertices is even as well.

Assigning weights `+(1,0),-(1,0)` on `H`, `+(0,1),-(0,1)` on `J`, and zero on thin channels therefore gives

    W = {(p,q) in (2Z)^2 : |p|+|q| <= 4}.

The signs introduced by incoming or outgoing incidence do not change either parity assertion. The norm bound uses all four vertices, including scalar and mixed channels. It requires neither tetrahedral symmetry of numerical F-symbols nor a nonzero entry chosen in advance.

For determinant-one `T_J`, the coherence of the actual tensor functor implies `u^p v^q=1` for each nonzero F entry. Let `L` be the lattice of its occurring weights. If `rank(L)=2`, choose two independent occurring weights. Divide them by two. The only nonzero possibilities are axial vectors of length one or two and unit diagonals. In each of the three independent-pair types—two axes, axis plus diagonal, two diagonals—the integer span contains both doubled coordinate axes. Before division, the span therefore contains `(4,0)` and `(0,4)`. This forces `u^4=1`, contradicting `u^4=-1`.

Thus the annihilator of `L` contains a positive-dimensional connected algebraic torus. It fixes every nonzero F entry, and the zero entries are automatically fixed. Unit channels are fixed as well.

For determinant-minus-one `T_J`, track only the `H` exponent `p`. If `p=+2` or `-2`, the `H` eigenvalue factor is `+i` or `-i`, and multiplication by any collection of `J` signs cannot produce one. If `p=+4` or `-4`, all four vertices must be `H` vertices, and the factor is minus one. Such entries vanish. Every nonzero F entry therefore has `p=0`, so the full one-parameter `H` torus fixes every F entry and every unit channel.

## 5. The stabilizer torus gives actual tensorators

Here is an explicit construction, which rules out the concern that only a change of notation has been produced.

Work in a skeletal semisimple realization with the fixed bases above. Let `U_ij^k` be any member of the stabilizing gauge torus acting on `V_ij^k=Hom(i j,k)`. Define an invertible endomorphism `J^U_(i,j)` of `i j` by

    f J^U_(i,j) = U_ij^k(f),    f in V_ij^k.

Projection and inclusion bases determine this endomorphism uniquely on every simple isotypic summand. Extend to general objects by direct sums, acting identically on the external vector-space multiplicities. This gives a natural invertible family for the tensor bifunctor.

The associator compares the two fusion-tree decompositions of a triple tensor product. The coherence equation for `J^U` says that the left two-vertex action and the right two-vertex action are intertwined by every F matrix. In the chosen diagonal bases that equation is exactly the weight condition already proved for each F entry. Thus `J^U` is a tensorator for the **identity underlying linear functor of the fixed category**. All unit channels have weight zero, so it is a unital tensor functor with the identity unit constraint. Its inverse matrices give the inverse tensor structure, hence an autoequivalence.

No associator is varied in this construction. The category, its objects, its morphisms, its fusion spaces, and every F matrix are held fixed.

## 6. Tensor natural equivalence cannot remove the family

A natural automorphism of the identity underlying linear functor is scalar on each simple: write its component as `lambda_i id_i`. Naturality with all projections and inclusions forces its component on every object to be the corresponding isotypic scalar. There is no independent matrix freedom on a multiplicity space.

For a tensor natural isomorphism between `J^U` and `J^V`, monoidality gives

    lambda_k U_ij^k = lambda_i lambda_j V_ij^k.

Consequently `U_H,V_H` differ only by a scalar, and the same is true for `U_J,V_J`. Their projective eigenratios are invariants under such equivalence.

For the determinant-one case these ratios are `z^2,w^2`. The map

    (z,w) -> (z^2,w^2)

has finite kernel. Its restriction to any positive-dimensional subtorus therefore still has positive-dimensional image. The stabilizer produces infinitely many distinct tensor-natural-isomorphism classes. In the reflection case the ratio `t^2` on `H` alone is already nonconstant.

ENO Theorem 2.31 forbids either family. This establishes the required contradiction once the local non-scalar-inner-action premise holds.

## Independent finite replay

A fresh script, `check_final_torus_audit.py`, uses a literal rank-four fusion tensor and does not import the existing checker. It verifies the full incidence and lattice argument using explicit failures, including under Python optimization.

Both normal and `python -O` runs pass and give identical receipts:

- 136 nonempty associator blocks.
- 1,472 F coefficient slots.
- 5,888 reflection-phase checks.
- 104 ordered independent weight pairs, each with explicit integer witnesses for both fourth coordinate axes.
- Exactly the thirteen vectors in `W` occur among possible slots.

Files:

- `final_torus_audit_receipt.json`.
- `final_torus_audit_receipt_optimized.json`.

These finite replays corroborate the combinatorial argument only. The categorical construction and the nontriviality modulo natural isomorphism are the mathematical arguments given above.

## Conclusion

I found no obstruction to accepting the global torus-rigidity step. It is valid for both determinant cases, includes all scalar and mixed channels, and uses the correct tensor-functor finiteness theorem. The sole requested textual refinement is to say “structural transport map” in the sentence following (12). Acceptance of the complete R24 exclusion additionally depends on the separately reviewed local pivotal-sign and conductor/indicator arguments.

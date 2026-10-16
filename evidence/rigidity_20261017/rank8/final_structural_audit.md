# Final structural audit of the R8_2_24 inner-square obstruction

AI-generated research · independent verification pending

## Verdict and scope

**PASS for the local pivotal calculation, the actual inner-square premise, the common chart, and the ensuing tensor-functor obstruction.** I found no counterexample or unresolved mathematical gap in Sections 1–5 of `R24_TORUS_RIGIDITY_PROOF.md`, under the stated pseudo-unitary hypotheses. The theorem does not assume a unitary realization, a known associator, or a unitary classification. It proves that the specified pseudo-unitary rank-four category has no label-fixing tensor autoequivalence whose square is inner conjugation by `g`.

The application to `R8_2_24` also has a valid structural square-root premise: any categorification supplies the actual tensor functor `Ad(a)` on the neutral subcategory. The source-binding checker passes. The full application additionally depends on the Galois pseudo-unitary reduction and the conductor-equality input establishing the three FS signs. I reviewed the displayed signed reindexing argument and found it sound; the local representation-theoretic proof of the conductor-equality lemma and the scope of Schopieray's published Galois reduction remain separately assigned prerequisite audits. This report is not a substitute for those audits and does not itself change publication status.

The three precise clarifications in the next section should be incorporated before publication. They make hypotheses and transport statements explicit; they do not require a different proof.

## Required clarifications

1. **State `dim(g)=1` in the local sign calculation.** The ambient category is pseudo-unitary, so this is already true. However, `coev_g=-e^{-1}` does not follow from `nu_2(g)=-1` alone in an arbitrary pivotal category. With the chosen dual data `g*=g` and `j_g=-id`, the pivotal dimension is `dim(g)=-e coev_g`. Positivity supplies `dim(g)=1`, giving the asserted coevaluation. The standalone typed audit's opening is otherwise phrased more generally than the derivation supports. Add: “Since the pivotal structure is the canonical pseudo-unitary one, `dim(g)=1`.”
2. **Construct the common word chart explicitly.** Fix the unit chart by the tensor functor's unit constraint. After selecting charts for the letters `g,r`, extend them multiplicatively to tensor words using the tensorator. In a strict word realization this makes the transported functor strict on the word category. The identities `T(e)=e`, `T(ev_r)=ev_r`, and `T(c)=alpha c` then refer to a single coherent transport. This prevents an apparent missing scalar in the covariance argument. The construction is given below.
3. **Qualify the sentence following (12).** Replace “Every map in (12) is fixed by T” with “Every structural transport map in (12) is fixed by T.” The variable vertex `f` is acted on by `T_H` or `T_J`; it is not claimed fixed. This distinction is exactly what the argument uses.

An optional helpful sentence identifies the signed convention for `F` with ordinary inner conjugation: the usual `Ad(g)` has tensorator `+e` and unit `-e^{-1}` under these duality conventions. Multiplying every component of a natural isomorphism by `-1` gives the manuscript's tensorator `-e` and unit `+e^{-1}`. Thus the theorem really concerns the usual inner autoequivalence class.

## 1. Independent derivation of the pivotal signs

Work in a strict monoidal rigid realization, retaining the pivotal isomorphism. Choose the right dual object of each of `g,Z` to be itself and use identity self-duality charts. The indicator identities then give `j_g=-id` and `j_Z=id`. Since `g` is invertible and the category is pseudo-unitary, its pivotal dimension is one. Consequently

    coev_g=-e^{-1},
    e g = -g e,
    e*=-e^{-1}.

The middle identity follows from either snake equation, and the third from dualizing evaluation with these right-dual choices. No pivotal strictification setting `j_g=id` is made.

For `F(X)=gXg`, the displayed tensorator `-gX e Yg` and unit `e^{-1}` satisfy both unit equations. This functor is monoidally isomorphic to the ordinary inner functor, as noted above.

The composite-square unit is `(g e^{-1} g)e^{-1}`. The raw contraction `e X e` sends this unit to `-1`; its negative sends it to `+1`. The same relation `e g=-g e` shows that the raw contraction has a tensor-product defect `-1`. Therefore

    eta_X=-e X e:F²(X)→X

is the correct monoidal comparison. Omitting this minus sign would reverse the conclusion of the local calculation.

The right-dual evaluation of `gZg` is the nested positive composite

    e (g ev_Z g)(gZ e Zg).

Transport through `F` adds exactly the tensorator's minus sign. The canonical dual comparison is therefore `delta_Z=-id`, as asserted.

For `c:gZ→Zg`, the self-duality of `gZ` is `(phi_Z tensor phi_g)c`. Expanding its FS equation gives

    (phi_Z^{-1} tensor phi_g^{-1})c*(phi_g tensor phi_Z)
       = nu_2(gZ)/(nu_2(g)nu_2(Z)) c = -c.

All map types agree: both sides go from `gZ` to `Zg`. The formula uses no braiding. In the identity charts, `c*=epsilon c` with `epsilon=-1`.

Set `q=(Z e)(c g)` and define `kappa` by the double-crossing equation. Every map in that equation is invertible, so `kappa` is nonzero. Dualization gives

    q*=-epsilon(g c)(e^{-1} Z),
    qq*=-epsilon kappa id_Z.

Since `q` is invertible, the corresponding equation on `F(Z)` is the same scalar. Comparing with `delta_Z=-id` gives `gamma=epsilon kappa`.

I checked the tensor-word types of all four lines of (5). The interchange step moves morphisms on disjoint factors. The only sign is the contraction identity `e(g e g)=-(e tensor e)`. Thus `qF(q)=-kappa(e Z e)=kappa eta_Z`, and `lambda=kappa`. Hence

    lambda/gamma=-1.

Both defects change by the same square when `q` is rescaled. The ratio is therefore not a normalization artifact.

## 2. The intrinsic multiplicity-space pairing

For `A=Z tensor Z` and a symmetric self-duality `phi_Z`, use the symmetric self-duality `phi_A=phi_Z tensor phi_Z:A→A*`; reversal of the tensor order is harmless because the two factors are identical. For `h:A→Z`, the full transpose is

    h^t=phi_A^{-1} h* phi_Z:Z→A.

The composition pairing between `Hom(A,Z)` and `Hom(Z,A)` is nondegenerate by semisimplicity. Transpose is an isomorphism between these spaces, so `beta(f,h)=tr_Z(fh^t)` is nondegenerate. All self-duality signs here equal `+1`, so transpose is involutive. Transposing the scalar composite proves symmetry. This is a complex bilinear form; no positive Hermitian form is being assumed.

Writing the induced inner action explicitly as

    K(f)=q F(f) F_2(Z,Z)(q^{-1} tensor q^{-1}),

the square comparison gives `K²=lambda^{-1} I`. The form-defect calculation gives the multiplier `gamma^{-1}`: one output chart contributes `gamma`, while the two input charts contribute `gamma^{-2}`. Equivalently one can compute the transpose of the displayed composite and cancel adjacent chart maps. Thus the two multipliers are opposite.

A scalar `K` would have its square equal to its bilinear-form multiplier, which is impossible. In dimension two, `K²` a nonzero scalar then forces two distinct opposite eigenvalues. Each eigenline is isotropic, since its eigenvalue square is `lambda^{-1}` but the similitude multiplier is `-lambda^{-1}`. Nondegeneracy pairs the two lines.

## 3. The square-root premise is an actual categorical premise

The full source tensor is commutative and contains an invertible `a` with inverse and square `g`. For each neutral simple `X`, the class of `a X a^{-1}` is `[X]`; hence inner conjugation restricts to a label-fixing tensor autoequivalence of the neutral fusion subcategory. This does not require a chosen half-braiding for `a`.

Inner conjugation is compatible with multiplication of invertible objects up to monoidal isomorphism. A chosen isomorphism `a²→g` therefore supplies

    (Ad(a)|D)² ≅ Ad(g).

No coherent trivialization of all powers of `a` is required. In particular, a nontrivial pointed associator on its cyclic subgroup does not remove this square relation. Changing the duality convention for `Ad(g)` changes only its representative, not this monoidal isomorphism class.

A monoidal natural isomorphism between label-fixing functors changes their actions on `Hom(r²,r)` by a scalar: its component at the simple `r` is a scalar, and monoidality gives the input product of two such scalars. Therefore the premise implies `[T_H²]=[K]` projectively, independent of choices of the isomorphism `T²⇒F`.

The fresh source-binding receipt is `final_structural_source_check.json`. It checks the declared tensor hash, all 64 neutral coefficients, source associativity, the actual invertible and its inverse, its square, and its neutral conjugation permutation. These are checks of the based ring, not a formalization of the categorical argument above.

## 4. One common chart and exact covariance

Let `T_2:T(X)T(Y)→T(XY)` and `T_0:1→T(1)` be the tensor constraints. In a strict tensor-word realization set the unit chart to `q_1=T_0^{-1}`. Choose charts `q_g:T(g)→g` and `q_r:T(r)→r`. Extend them by

    q_(uv)=(q_u tensor q_v) T_2(u,v)^{-1}.

Define the transported action on a morphism `f:u→v` by `q_v T(f) q_u^{-1}`. It respects composition and tensor products exactly. Words that are merely isomorphic are retained as separate objects, so this construction makes no illegal simultaneous identifications.

The transported images of `e:gg→1` and `ev_r:rr→1` are nonzero scalars times those maps. Rescaling `q_g` and `q_r` independently kills the two scalars by complex square roots. Define the chart of `s=gr` to be the induced word chart. Pseudo-unitary uniqueness ensures the functor preserves the canonical pivotal structure, so fixing these forms also fixes the compatible cups and duality operations.

Write `T(c)=alpha c`. Applying the transported functor to the double-crossing identity scales its left side by `alpha²` and leaves the nonzero right side fixed. Thus `alpha²=1`.

The action `K(f)` displayed above uses only `g`, the fixed evaluation `e`, the tensor structure built from it, and the map `q` linear in `c`. Under the same strict word transport, `T(q)=alpha q`, while `T(F(f))=F(T(f))`. Therefore direct substitution gives

    T_H K(f)=alpha^{-1} K(T_H f).

This establishes the exact covariance without an untracked scalar from a comparison between `TF` and `FT`.

If `alpha=-1`, `T_H` exchanges the two distinct `K` eigenlines. Every invertible two-by-two matrix interchanging two lines has scalar square. This contradicts `[T_H²]=[K]`, since `[K]` is nonscalar. Hence `alpha=+1`.

The explicitly constructed evaluation on `s` is nonzero and fixed by the same transport. Because `nu_2(s)=1`, its associated self-duality is symmetric; no independent scaling of the `s` chart is needed. Both full-transpose forms on `H=Hom(r²,r)` and `J=Hom(r²,s)` are therefore preserved exactly. The two formulas for the `s` evaluation in the three reviewed documents are both permissible nonzero composites; they need not be literally identical to serve this purpose.

On `H`, the determinant-minus component of `O(2,C)` has square the identity, so it is impossible. In a hyperbolic basis `T_H=diag(u,u^{-1})`, and projective comparison with `K` gives `u^4=-1`. On `J`, the two valid alternatives are the determinant-plus torus and a determinant-minus reflection with eigenvalues `1,-1`. No assertion about a local inner action on `J` is required.

## 5. Structural transports, gauge weights, and rigidity

I checked all eight cases of the maps `A_ab` and `B_abc` in (12). Their source and target tensor words agree. They are compositions of maps fixed in the common chart. Consequently transporting a variable vertex from `H` or `J` intertwines its functor action exactly; no extra scalar character appears. All multiplicity-one vertices likewise have fixed bases, and their composition-dual inclusions are fixed.

The four-vertex incidence argument is correct for every full associator coefficient. Every admissible vertex has zero, two, or three noninvertible edges. The parity of total marked incidence forces an even number of thick vertices. The parity of the `g` bits forces an even number of `J` vertices, and hence an even number of `H` vertices. There are only four vertices. Thus every weight lies in the displayed short even diamond, including scalar channels and zero coefficients.

Any two independent vectors in that diamond generate a lattice containing both fourth-coordinate axes. This can be checked without enumerating F-symbols: divide by two and distinguish two coordinate axes, one axis plus a diagonal, or two independent diagonals. A full-rank stabilizing weight lattice would therefore imply `u^4=1`, contradicting the local result. A lower-rank lattice has a positive-dimensional annihilator torus.

In the reflection case on `J`, an `H` exponent of magnitude two contributes `+i` or `-i` and cannot be canceled by a sign. An exponent of magnitude four uses all four vertices in `H` and contributes `-1`. Both types of coefficients must vanish, leaving an entire `H` torus stabilizer.

A stabilizer of every associator and unit channel defines strong tensor structures on the identity underlying linear functor in a semisimple skeletal realization. Monoidal natural isomorphisms have scalar components at simples and hence act by scalar changes on `H` and `J`. Two torus parameters can therefore be equivalent only if their projective ratios on both spaces coincide; this kernel is finite (`t²=w²=1` in the two-dimensional case). The positive-dimensional torus yields infinitely many inequivalent tensor functors.

ENO Theorem 2.31 applies to fixed fusion categories over the complex numbers and gives finiteness up to equivalence of unital tensor functors. The hypothesis is exactly the one contradicted here. I checked the theorem in its primary publication, p.592: https://annals.math.princeton.edu/wp-content/uploads/annals-v162-n2-p01.pdf . This final step uses no unitarity assumption on the category.

## 6. Signed Galois indicator calculation

I checked the reindexing calculation in Section 0 under its stated saturation hypothesis. The functional `ell` is rational valued on the dimension field. The modular Galois sign enters both `z_(pi A)` and `ell(z_(pi A))`, and cancels in their product exactly as displayed. The anomaly-free center normalization is essential for `theta_(pi A)=sigma²(theta_A)` and is the normalization used here.

Every term with nonzero functional has twist dividing five by the separate conductor-equality premise; the constituents of `I(1)` have twist one. Consequently the inverse exponent modulo five may be used after reindexing. The weighted first trace becomes the weighted higher-indicator identity with the quadratic character factor. Taking residue two gives the asserted equation. With three self-dual signs, its only solution is `nu_2(g)=-1`, `nu_2(r)=nu_2(s)=1`.

This algebraic reindexing does not assume the Galois permutation is an involution or that the exponent square is one modulo five. Neither the cubic indicators nor any decorated-rotation relation enters the subsequent proof.

## Reviewed file identities

- Main proposed proof: SHA-256 `3492f0ab0679286f8f15fec4a8c0ac5fa46277cebf240ea250b82a67a666863c`.
- Typed local audit: SHA-256 `7da033287dad90afe987a6a724cef4a89e636a9287609424902c92e3713a2a67`.
- Literature local audit: SHA-256 `8f9a510fae78d8fef67ba46958550fddf7ed5567dc32d9f87d7aa2311d389f97`.

No canonical repository or published classification file was edited for this audit.

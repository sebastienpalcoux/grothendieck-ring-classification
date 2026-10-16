# R8_2_24: independent audit of the prerequisites for the torus obstruction

AI-generated research · independent verification pending. This is an independent mathematical audit within the present AI workflow, not a human verification or Lean formalization.

**Verdict: the prerequisite chain passes.** Any complex fusion-category categorification of the canonical source ring has a Galois-conjugate categorification containing a pseudo-unitary neutral category with the stated fusion rules, indicators `(-1,+1,+1)` on `(g,r,s)`, and an actual label-fixing tensor autoequivalence `T` satisfying `T² ≅⊗ Ad(g)`. No unitarity hypothesis on the category is needed.

The scope of this report is Section 0 of `R24_TORUS_RIGIDITY_PROOF.md`, the conductor-equality lemma, and the character-weighted indicator lemma. It does not independently certify Sections 1–5 of the torus obstruction. In particular, the prerequisites alone do not exclude the source ring.

## 1. Exact source and the forced neutral subcategory

I independently parsed `repo/supplements/rank8/data/rank8_tables.txt.gz`, selected the 24th lexicographically ordered tensor with maximum structure coefficient two, and compared its compact-JSON SHA-256 with the published decision record:

```
2b4780441d9590e8e7269cd82b7675aa75cec11c39bd3e94bb372cca1ada6738
```

The source duality is `(0,2,1,4,3,5,6,7)`. The invertibles are `{0,1,2,7}`. The degree-zero labels are `{0,7,5,6}`, and the other four labels form the odd component of a faithful `Z/2` grading. This degree-zero part is exactly the adjoint subcategory: all products `X X*` lie there, and their tensor closure contains all four labels.

In the ordered basis `(1,g,r,s)=(0,7,5,6)`, the tensor is

```python
[
 [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],
 [[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]],
 [[0,0,1,0],[0,0,0,1],[1,0,2,2],[0,1,2,2]],
 [[0,0,0,1],[0,0,1,0],[0,1,2,2],[1,0,2,2]],
]
```

Thus all four neutral labels are self-dual and

\[
g^2=1,\qquad gr=rg=s,\qquad
r^2=s^2=1+2r+2s,\qquad rs=g+2r+2s.
\]

For `a=1` in source labels, `a*=2`, `a²=7=g`, and `a x a*=x` for every neutral simple label. These are identities of actual simple objects in any categorification, because an invertible tensor product preserves simplicity. Commutativity of the based ring is sufficient here; no braiding is inferred or required.

The usual inner functor `Ad(a)(X)=a⊗X⊗a*` is a tensor autoequivalence, with its tensorator formed by evaluating the adjacent `a*⊗a`. It preserves the neutral subcategory and fixes its simple isomorphism classes. The dual identification `(a⊗a)* ≅ a*⊗a*` and the associativity constraints give a monoidal natural isomorphism

\[
Ad(a)\circ Ad(a)\simeq_\otimes Ad(a\otimes a).
\]

Any chosen isomorphism `a⊗a ≅ g`, together with its dual, then identifies the latter inner functor with `Ad(g)`. This only asserts a monoidal isomorphism between two functors. It does not assert a strict group action, a trivial pointed associator, or a chosen trivialization of every higher coherence scalar.

## 2. Galois passage applies to the whole category

Put `d=2+√5`. The source has positive dimension vector

\[
(1,1,1,d,d,d,d,1),
\]

which satisfies every source multiplication equation. Positivity identifies it with the Frobenius–Perron character. Consequently the source is a two-dimension fusion ring in the precise sense of the published Schopieray Lemma 3.1.

I opened the publisher's PDF of *Categorification of integral group rings extended by one dimension*, J. London Math. Soc. 108 (2023), 1617–1641, DOI [10.1112/jlms.12789](https://doi.org/10.1112/jlms.12789). Lemma 3.1 is on printed page 1628. Its conclusion is **Galois conjugacy to a pseudo-unitary category**, and its hypothesis is only that every simple FP dimension belongs to `{1,d}` for a real `d>1`. It does not assume an initial pivotal structure. The stronger formulation in the initial arXiv version must not replace this published formulation.

Apply the lemma to the full rank-eight categorification. In the resulting conjugate, the same source labels still satisfy the same integer fusion rules, and the invertible `a` still defines the required inner functor. One can simply reconstruct that functor after conjugation; no separate extension theorem for an arbitrary prescribed autoequivalence is needed.

Equip the pseudo-unitary category with its canonical positive spherical structure. Its restriction to the neutral fusion subcategory has dimensions `(1,1,d,d)`, hence is the canonical positive spherical structure there. A tensor autoequivalence preserves this structure: transporting it gives another positive spherical structure, and uniqueness identifies the two. The argument therefore has general complex scope, not just pivotal or unitary scope.

## 3. Formal codegrees and the saturated vector

Write

\[
D=20+8\sqrt5,\qquad \bar D=20-8\sqrt5.
\]

The four neutral ring characters, in order `(1,g,r,s)`, are

\[
(1,1,d,d),\quad (1,1,\bar d,\bar d),\quad
(1,-1,1,-1),\quad(1,-1,-1,1),
\]

where `d̄=2−√5`. They are linearly independent and exhaust the four-dimensional commutative algebra. Their squared-character sums give formal codegrees `D,D̄,4,4`.

Let `A₀,A₁,B,C` be the corresponding simple summands of the induced unit in the center of the neutral category. Each occurs once and has twist one; their dimensions are

\[
1,\quad D/\bar D=9+4\sqrt5,\quad D/4=5+2\sqrt5,\quad D/4.
\]

Use the canonical normalization `s=S/D` and the actual center twist matrix `t`. The relevant standard dimension-block identity is

\[
s_{A_\sigma,Y}=\sigma\!\left(\frac{\dim Y}{D}\right).
\]

It follows either from the formal-codegree central character identity or from Schopieray's dimension-block Lemma 2.1. Every center dimension belongs to `K=Q(√5)`, since its forgetful image is a direct sum of the four neutral simples. The first two rows of the induced-unit block are therefore

\[
\begin{pmatrix}
1/D&1/\bar D&1/4&1/4\\
1/\bar D&1/D&1/4&1/4
\end{pmatrix}.
\]

For `w=e_{A₀}−e_{A₁}`, projection of `s w` to this known twist-one block is `λw`, where

\[
\lambda=1/D-1/\bar D=-1/\sqrt5.
\]

The modular diagonal torus acts on `w` by the quadratic character `χ₅`, of conductor five. To see this without assuming unknown center data, use `ρ(h_b)=σ_b(s)s⁻¹`: the dimension rows are fixed or exchanged according to `χ₅(b)`, and the resulting action on their two coordinate vectors is the same permutation. This gives `ρ(h_b)w=χ₅(b)w`.

The distinction between two uses of “unitary” matters. The category need only be spherical. Its canonical center modular representation is unitary for the standard orthonormal simple basis: complex conjugation satisfies `s̄=C_dual s`, while `s²=C_dual` and `s` is symmetric, giving `s s*=1`; `t` is unitary because its entries are roots of unity. Thus the standard orthogonal projection to twist-one vectors is legitimate. No positive definite form on categorical morphism spaces is being assumed.

If `P` projects to the entire twist-one space, including any unknown additional simples, the compression bound gives

\[
\|Psw\|^2\le \|w\|^2/5.
\]

The known two-coordinate projection already has that norm. Orthogonality therefore forces equality and `Psw=−w/√5`. The proof does not assume that the induced-unit constituents are all twist-one center simples.

## 4. Why equality really forces conductor level

I checked the retained refinement of the local compression argument. Here are its essential equality details.

For `M=ℓᵃ`, a nontrivial local torus character `α` of conductor `ℓᶜ`, and primitive vectors `Ωₐ`, every irreducible representation with a nonzero unipotent-fixed vector embeds in `C[Ωₐ]`. On the unipotent-fixed `α` eigenspace there is an orthogonal decomposition into the big-cell line `C F_α` and the small-cell subspace `Σ_α`. The compression `A=P s P` satisfies

\[
A F_\alpha=G_\alpha,
\quad F_\alpha(p,q)=\alpha(q)[q\text{ unit}],
\quad G_\alpha(p,q)=\alpha(-p)[q\equiv0\pmod{\ell^c}].
\]

Its restriction from `Σ_α` to the big cell has rank one, norm `ℓ^(−c/2)`, and adjoint image `C G_{ᾱ}`. The two output supports are disjoint. Hence the entire maximal singular subspace is exactly

\[
\operatorname{span}(F_\alpha,G_{\bar\alpha}).
\]

Both functions depend only on the primitive vector modulo `ℓᶜ`. The pullback space from `Ω_c` is invariant under the entire group, not just the torus and unipotent subgroup. Thus the cyclic subrepresentation of any equality vector factors through reduction modulo `ℓᶜ`. If the vector lies in an irreducible summand, that whole summand factors through the same reduction.

For a trivial local character, norm-one equality means that both `w` and `sw` are unipotent-fixed. Hence `w` is fixed by the upper and lower unipotent subgroups, which generate `SL₂(Z/ℓᵃ)`. This local factor is trivial on the cyclic representation.

For composite `N`, CRT splits the group, and the unipotent-fixed torus-character spaces split as tensor products. On each orthogonal irreducible summand, equality in the product bound forces membership in the tensor product of the maximal singular spaces: diagonalize the nonnegative operators `A_ℓ* A_ℓ`. Factors outside the conductor are trivial; other factors descend to their conductor powers. Orthogonal decomposition then gives the assertion for the cyclic representation generated by the original vector.

This establishes the retained conductor-equality lemma, including the nonprimitive-character case and the primes outside the conductor. Applied here, `t⁵ s w=s w`.

Define the rational linear functional

\[
\ell(z)=-20\,[\sqrt5]\,(z/D),
\]

where `[√5]` means the coefficient in the basis `(1,√5)`. It has values `(2,2,−1,−1)` on the four neutral dimensions. For each center simple `Y`, the dimension-block row identity gives the exact coordinate relation

\[
(s w)_Y=\frac{z_Y}{D}-\overline{\frac{z_Y}{D}}
=-\frac{\sqrt5}{10}\ell(z_Y).
\]

Consequently `ell(z_Y)≠0` implies `θ_Y⁵=1`. In fact saturation also shows that outside the known induced-unit block this twist cannot equal one. The weaker divisibility assertion is sufficient for the indicator argument.

## 5. The signed Galois indicator calculation

The character-weighted lemma's signs and inverse exponent are correct. For this application one can use a single automorphism and second indicators only.

Let `N` be the order of the center twist. Because `Q(√5)⊂Q(ζ_N)`, five divides the cyclotomic conductor. Choose an integer `m` coprime to `N` with `m≡3 (mod 5)`, and let `τ(ζ_N)=ζ_N^m`. Such a lift exists by CRT. Its restriction `σ` to `K` is the nontrivial automorphism. Modular Galois symmetry gives a permutation `π` and signs `ε_Y` such that

\[
z_{\pi Y}=\epsilon_Y\frac D{\sigma D}\sigma(z_Y),
\qquad \theta_{\pi Y}=\tau^2(\theta_Y).
\]

The functional then transforms by

\[
\ell(z_{\pi Y})=-\epsilon_Y\ell(z_Y),
\quad
\tau(\ell(z_Y)z_Y)
=-\frac{\sigma D}{D}\ell(z_{\pi Y})z_{\pi Y}.
\]

Thus the modular signs cancel; dropping them before this calculation would not be justified. The zero-weight support is also invariant under `π`.

Write `n_{Y,X}=[F(Y):X]=[Y:I(X)]`. Since `z_Y=Σ_X n_{Y,X} dim(X)` and `ell` is rational-linear, weighting the induction trace formula by `ell(dim X)` gives

\[
\sum_Y\ell(z_Y)z_Y\theta_Y^n
=D\sum_X\ell(\dim X)\nu_n(X).
\tag{*}
\]

At `n=1`, only the unit has nonzero first indicator, so the right side is `D ell(1)=2D`. Apply `τ`. Every term with nonzero weight has fifth-power twist one; for such a term,

\[
\tau(\theta_Y)=\theta_Y^m
=\theta_{\pi Y}^{\,2},
\]

because `2m²≡m (mod 5)`. Reindexing by `π` therefore gives

\[
-\frac{\sigma D}{D}
 \sum_Y\ell(z_Y)z_Y\theta_Y^2
=2\sigma D.
\]

Cancel `σD` and use `(*)` at `n=2`:

\[
2+2\nu_2(g)-\nu_2(r)-\nu_2(s)=-2.
\]

All three nontrivial neutral simples are self-dual. Their second indicators are therefore `±1` in the spherical pivotal structure. The only sign solution is

\[
\nu_2(g)=-1,\qquad \nu_2(r)=\nu_2(s)=1.
\]

This argument does not assume that the Galois permutation is an involution, that it fixes the unit, or that the full twist conductor is five. It only needs conductor five on the support of `ell`. It does not use third indicators or any decorated rotation.

The more general retained lemma follows by choosing any unit residue `k mod f` and taking a positive inverse `h mod f`; then `τ(θ_Y)=θ_{πY}^h`, and `χ(h)=χ(k)`. Renaming the inverse residue gives its stated formula. The two-coordinate computation above supplies its complete hypothesis in the present case.

## 6. Primary references and evidence boundaries

I checked these primary texts directly:

1. A. Schopieray, *Categorification of integral group rings extended by one dimension*, published Lemma 3.1, printed p.1628: [publisher PDF](https://londmathsoc.onlinelibrary.wiley.com/doi/pdf/10.1112/jlms.12789). This supplies the general-complex Galois reduction.
2. A. Schopieray, *The dimension block of a spherical fusion category*, arXiv:2609.35287v1, Lemma 2.1, Section 3, Lemmas 3.1 and 4.1: [primary preprint](https://arxiv.org/pdf/2609.35287). This supplies the dimension-block and compression inputs. The conductor-level equality refinement is the additional argument audited in Section 4 above, not a theorem attributed to that preprint.
3. C. Dong, X. Lin and S.-H. Ng, *Congruence property in conformal field theory*, canonical center normalization in Section 1.4 and Lemma 4.2: [primary preprint](https://arxiv.org/pdf/1201.6644). Its center-specific transformation uses the actual twists and has no anomaly scalar.
4. S.-H. Ng and P. Schauenburg, *Frobenius–Schur indicators and exponents of spherical categories*, Theorem 4.1 in arXiv v3: [primary preprint](https://arxiv.org/pdf/math/0601012). This is the general spherical induction trace formula used in `(*)`.
5. V. Ostrik, *Pivotal fusion categories of rank 3*, Theorems 2.5, 2.7 and 2.13: [primary preprint](https://arxiv.org/pdf/1309.4822). These preliminary results give the induced-unit constituents, their twist, and the self-dual second-indicator condition for general spherical fusion categories; the present use does not assume rank three.

No classification of unitary 2D2 categories, assertion about its tensor automorphism group, existence of an algebra `1+r`, or numerical associator data enters this prerequisite proof. The induced pointed `C₂` subcategory has the nontrivial indicator sign, but that fact alone is compatible with a pointed `C₄` extension and is not claimed as an exclusion.

## 7. Independent exact checks

The adjacent `check_prerequisites_independent.py` imports no project verification helpers. Its receipt is `prerequisites_independent_receipt.json`. All 32 checks pass under normal and optimized (`-O`) Python, including the full source associativity, neutral closure and grading, dimensions, formal codegrees, exact signed quadratic transformations, and the unique second-indicator sign solution.

An extra finite representation check at modulus 25 has 600 primitive vectors, 56 unipotent orbits, and a six-dimensional quadratic torus-character space. Its exact compression defect has a two-dimensional kernel, precisely `span(F,G)`, and both functions descend modulo five. This is an independent consistency check of the equality calculation; the all-level justification is the theoretical argument in Section 4.

The retained source checker was also rerun, producing `prerequisite_source_replay.json`. Its role is tensor binding only. No finite arithmetic receipt is offered as a substitute for the categorical or representation-theoretic arguments.

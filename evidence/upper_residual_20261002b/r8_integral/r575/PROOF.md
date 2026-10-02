# A unitary fusion-category model for R8_2_575

The ring R8_2_575 is realized by a rigid Davydov–Runkel extension
`Rep(H) ⊕ Vec`, where `H` is Kashina's self-dual Hopf algebra
`H_{C:σ₁}`. Its simple dimensions are `1,1,1,1,2,2,2,4`.
The model-to-census permutation is

```
[0, 5, 1, 2, 3, 7, 4, 6]
```

This conclusion concerns an actual unitary fusion category, not just an
associative fusion ring or a prospective self-duality of a Hopf algebra.

## 1. Explicit Hopf algebra and its semisimplicity

Put `ζ=exp(2πi/16)`, `ω=ζ²`, and `i=ζ⁴`. Let
`G=D₈={(p,q):p∈Z/4,q∈Z/2}` with multiplication

\[
(p,q)(r,s)=(p+(-1)^q r,q+s),\qquad
\tau(p,q)=(-p+q,q).
\]

The vector space `H` has basis `h(p,q,j)`, where `j∈Z/2`. Its structure
maps are

\[
\begin{aligned}
h(p,q,j)h(r,s,k)&=
 \delta_{(p,q),\tau^j(r,s)}\omega^{qjk}h(p,q,j+k),\\
1_H&=\sum_{p,q}h(p,q,0),\\
\Delta h(g,j)&=\sum_{ab=g}i^{-a_2b_1j}h(a,j)\otimes h(b,j),\\
\varepsilon h(p,q,j)&=\delta_{p,0}\delta_{q,0},\\
S h(p,q,j)&=\zeta^{(4p-2)qj}h(\tau^j((p,q)^{-1}),j).
\end{aligned}
\]

Every exponent and index is read in the indicated finite cyclic group. The
supplied exact checker verifies all 4096 algebra-associativity identities,
all 16 coassociativity identities, all 256 coproduct/product identities,
both unit and counit identities, both antipode identities, and `S²=1`.
Thus the formulas define a Hopf algebra, with invertible antipode.

Its algebra is a crossed product of `Fun(G)` by the involution `τ`, with
the displayed scalar cocycle. The fixed points of `τ` are `(0,0)` and
`(2,0)`; each contributes two one-dimensional representations. The remaining
three two-element orbits contribute full `2×2` matrix algebras. Indeed the
idempotents at the two points are diagonal matrix units and `t=Σ_g h(g,1)`
interchanges their eigenspaces; `t²=ω^q` is a nonzero scalar on each such
orbit. Consequently

\[
H\cong\mathbb C^4\oplus M_2(\mathbb C)^3
\]

as an algebra. In particular `H` is semisimple.

## 2. The necessary self-duality data exist

Define a bilinear pairing on basis elements by

\[
P(h(p,q,j),h(r,s,k))=
\delta_{s,j}\delta_{k,q}\,i^{-3rp}\zeta^{jq}/4.
\]

It is symmetric. The checker verifies both Hopf-pairing identities for
every ordered triple of basis elements, for a total of 8192 exact scalar
identities, and both unit identities. Its four Fourier blocks are
invertible: in the same ordered basis the inverse matrix is

\[
(P^{-1})_{(p,q,j),(r,s,k)}=
\delta_{s,j}\delta_{k,q}\,i^{-rp}\zeta^{-jq}.
\]

Both inverse-matrix identities are checked exactly. Therefore `P` gives a
Hopf isomorphism between `H` and its **ordinary** linear dual.

Davydov–Runkel use the dual convention
`H^∨=(H*)^{op,cop}`; see their equation (2.3), footnote 2 and equation
(2.6). Hence the map required by their theorem is

\[
\Gamma=S\circ P^{-1}:H^\vee\longrightarrow H,
\]

with matrices acting on coordinate columns. The antipode changes both
opposite structures, so this is a Hopf isomorphism. To remove any possible
convention ambiguity, the checker independently verifies its 256 product
identities and 16 coproduct identities using the **actual opposite-product,
opposite-coproduct dual**, together with its unit, counit and antipode
identities. It also verifies that the matrix of `Γ` is symmetric.

Set

\[
\lambda(h(p,q,j))=\tfrac12\delta_{j,0},\qquad
\Lambda=\tfrac12(h(0,0,0)+h(0,0,1)).
\]

The checker verifies that `λ` is a two-sided cointegral, that `Λ` is a
two-sided integral with `ε(Λ)=1`, and that

\[
(\mathrm{id}\otimes\lambda)\Delta=1_H\lambda,
\qquad \Gamma(\lambda)=4\Lambda,
\qquad \lambda(\Gamma(\lambda))=1.
\]

Thus the distinguished grouplike appearing in Davydov–Runkel's theorem is
`g=1`. In `Vec` the twist and the natural double-dual identification are
the standard ones. Their conjugate-self-duality condition therefore reduces
to symmetry of `Γ`, because `S²=1`. All conditions of their Theorem 2.5
are satisfied. That theorem provides the associator on `Rep(H)⊕Vec`;
their **Proposition 3.25** supplies rigidity. Since `H` is semisimple,
this is a fusion category over `ℂ`.

The Hopf algebra is noncommutative, and its Hopf self-duality makes it
noncocommutative. Its four one-dimensional representations give
`G(H*)=C₂×C₂`, as can also be read from the tensor products below.
Self-duality gives the same group for `G(H)`. Kashina's Theorem 1.2 and
Table 1 therefore identify this explicit Hopf algebra with `H_{C:σ₁}`.
This identification is not needed for existence of the constructed category.

## 3. Full fusion-data comparison and unitarity

Order the seven neutral characters first by the two signs over `(0,0)`,
then the two signs over `(2,0)`, then by the free orbits

```
{(0,1),(1,1)}, {(1,0),(3,0)}, {(2,1),(3,1)}.
```

The checker computes all 49 neutral character products directly from the
displayed coproduct, decomposes them into these seven irreducibles, and
verifies each decomposition at all 16 basis elements. Independently it
constructs the ordinary character table of `D₁₆=<r,s | r⁸=s²=1,
srs=r⁻¹>`: four sign characters followed by the three rotation characters
`ζ₈^{kp}+ζ₈^{-kp}`, `k=1,2,3`, vanishing on reflections. Character
orthogonality and all 343 product multiplicities agree. Thus the neutral
based ring is `K₀(Rep(D₁₆))`.

Let `M` be the unique odd simple, represented by the one-dimensional
object of the additional `Vec` summand. The tensor product in
Davydov–Runkel's equation (2.15) gives

\[
X\otimes M=M\otimes X=\dim(X)M,\qquad
M\otimes M=\bigoplus_{X\in\operatorname{Irr}(H)}\dim(X)X.
\]

Here the second product is the left regular `H`-module. It follows that
`FPdim(M)=4` and `FPdim(C)=32`. All 512 coefficients of the resulting
rank-eight tensor match the source census after the permutation stated
above. The checker also checks its 4096 associativity equations and all
dimension and self-duality equations.

By Etingof–Nikshych–Ostrik, Theorem 1.6, a fusion category of dimension
`32=2⁵` is solvable, hence weakly group-theoretical. Galindo–Hong–Rowell,
Theorem 5.20, implies that it admits a unitary structure. Therefore
`R8_2_575` has a unitary categorification.

## Reproducibility

Run from the repository root:

```
python3 evidence/upper_residual_20261002b/r8_integral/r575/verify_r575.py
python3 -O evidence/upper_residual_20261002b/r8_integral/r575/verify_r575.py
```

All calculations use the exact field `Q[z]/(z⁸+1)` and rational numbers;
the program uses no `assert`, floating-point arithmetic or external package.
It reads the actual compressed census and pins the decompressed source by
SHA-256 `97b86d2de8ca0352c5c6e14686cd1d43dbd52180dc53b2ff1ccf7a61788c9600`.
The canonical full target tensor has SHA-256
`b69b81c82fee86626ed0d7c132227bee7a67fbf8f4c54a84f31d62a3a51858cf`.
The accompanying normal and optimized receipts record the same checks.

## Primary references

1. A. Davydov and I. Runkel, *Z/2Z-extensions of Hopf algebra module
   categories by their base categories*, arXiv:1207.3611v2 (2013),
   Theorem 2.5, equation (2.3), footnote 2, equation (2.6), equation
   (2.15), and Proposition 3.25. https://arxiv.org/abs/1207.3611
2. Y. Kashina, *Classification of semisimple Hopf algebras of dimension
   16*, arXiv:math/0004114, Theorem 1.2 and Table 1.
   https://arxiv.org/abs/math/0004114
3. P. Etingof, D. Nikshych and V. Ostrik, *Weakly group-theoretical and
   solvable fusion categories*, arXiv:0809.3031, Theorem 1.6.
   https://arxiv.org/abs/0809.3031
4. C. Galindo, S.-M. Hong and E. C. Rowell, *Generalized and quasi-localizations
   of braid group representations*, arXiv:1105.5048, Theorem 5.20.
   https://arxiv.org/abs/1105.5048

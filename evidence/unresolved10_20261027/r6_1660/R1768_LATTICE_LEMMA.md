# R1768: norm-minus-one cancellation on the actual order lattice

This note supplies the absolute-value step independently of maximal-order
ray-class interpretations. It does **not** supply the separately needed
phase/sign calculation or the categorical identification of the Morita dual.

## Lattice cancellation lemma

Let `K` be a real quadratic field, with its first embedding fixed. Let
`Λ ⊂ K` be a full additive lattice containing `1`. Suppose `μ ∈ K` satisfies

\[
 \mu>1,\quad N_{K/\mathbb Q}(\mu)=-1,\quad
 \mu\Lambda=\Lambda,\quad (\mu-1)z\in\Lambda,\quad z\notin\Lambda.
\]

Set `ε=μ²`. Form the refined double-sine product of the coset `z+Λ`
over any rational cone fan fundamental for multiplication by `ε` on the
totally positive quadrant, using upper half-open boundaries relative to
the first coordinate axis. Then this product equals `1`.

No hypothesis that `Λ` is an ideal of the maximal order, no primitive
coset hypothesis, and no minimality hypothesis on `ε` is required.

### Proof by signed Barnes sums

Embed `K` in `R²`. Write `σ=cone(1,ε)`, `σ′=μσ`, and
`ρ=cone(1,μ)`. The first coordinate is positive throughout all three cones.
For a rational two-dimensional cone `κ` in that half-space define, initially
for `Re(s)>2`,

\[
 C_\kappa(s)=
 -\sum_{\beta\in\kappa^u\cap(z+\Lambda)}\beta_1^{-s}
 +\sum_{\beta\in\kappa^l\cap(-z+\Lambda)}\beta_1^{-s}.
 \tag{1}
\]

Here upper/lower closure is defined by whether `β−t e₁` / `β+t e₁`
lies in the open cone for all sufficiently small positive `t`. Generators
of each cone may be taken in `Λ`; their span is a finite-index sublattice.
Decomposing into its parallelogram representatives writes (1) as a finite
sum of the Barnes combinations

\[
 \xi(s,w;a,b)=
 -\zeta_2(s,w;a,b)+\zeta_2(s,a+b-w;a,b).
 \tag{2}
\]

The representative and its reflection use complementary half-open
parallelograms. They avoid both exceptional corners because `z∉Λ`.
Both periods `a,b` are positive first coordinates. Thus each combination
is holomorphic at zero, with `ξ(0,w;a,b)=0`; the latter follows directly
from the reflection symmetry of the degree-two Barnes Bernoulli polynomial.
Its derivative exponentiates to the positive real double sine.

Multiplication by `μ` preserves both cosets `±z+Λ` and preserves the
upper/lower boundary convention, since it multiplies `e₁` by the positive
number `μ`. Consequently

\[
 C_{\sigma'}(s)=\mu^{-s}C_\sigma(s).                 \tag{3}
\]

The disjoint cones `ε^k σ` and `ε^k σ′`, for `k≥0`, fill `ρ`, with
the corresponding upper/lower boundaries. The only omitted limit ray is
the first coordinate axis. That ray contains no nonzero embedded element
of `K`, and zero is absent from the cosets. Since `ε` also preserves the
cosets, summing the absolutely convergent series gives

\[
 C_\rho(s)=
 \frac{C_\sigma(s)+C_{\sigma'}(s)}{1-\varepsilon^{-s}}.
\]

Using (3), `ε=μ²`, and meromorphic continuation yields

\[
 C_\sigma(s)=(1-\mu^{-s})C_\rho(s).                 \tag{4}
\]

By the finite Barnes decomposition, `Cρ(0)=0`. Equation (4) therefore
gives `d Cσ(s)/ds` equal to zero at `s=0`.
Equivalently, the refined double-sine product on `σ` is `exp(0)=1`.

For completeness, passage to any fundamental fan uses only lattice
identities. The signed sums (1) are additive under finite cone subdivision
with the same upper/lower boundary convention. A translate of a cone by
`ε` multiplies its signed sum by `ε^(−s)`, and hence leaves its derivative
at zero unchanged because that cone's signed sum vanishes at zero.
Intersect two finite fundamental fans and translate pieces by powers of
`ε` to obtain a common subdivision. Additivity and translation invariance
identify their derivatives. This proves the lemma. ∎

## Application to the eleven diagonal points

Take

\[
 \Lambda=\mathbb Z[\sqrt{37}]=\mathbb Z+\mathbb Z\mu,
 \quad\mu=6+\sqrt{37},\quad\omega=1+\mu,
 \quad z_l=(1-l/12)\omega\quad(1\le l\le11).
\]

The identity `μ²−12μ−1=0` gives `μ^(−1)=μ−12`, so multiplication by
`μ` is a lattice automorphism. Further,

\[
 (\mu-1)z_l=(12-l)\mu\in\Lambda.
\]

The coefficients of `z_l` in the lattice basis `(1,μ)` both equal
`1−l/12`, which is not an integer; hence `z_l∉Λ`. These checks apply
also when `l` and `12` are not coprime.

The Hirzebruch–Jung cycle `[14,2,2,2,2,2,2,2,2,2,2,2]` for `ω`
has monodromy

\[
 \gamma'=\begin{pmatrix}157&-144\\12&-11\end{pmatrix},
 \qquad12\omega-11=\mu^2=\varepsilon.
\]

Its adjacent lattice bases `(A_(j−1),A_j)` give precisely a fundamental
fan for this `ε`. The choice
`x_j∈(0,1], y_j∈[0,1)` is the upper boundary convention above:
the ray `A_(j−1)` is included and `A_j` excluded. Homogeneity of the
double sine identifies the normalized factors with the cone factors.
Therefore the lemma gives the exact identity

\[
 \boxed{\displaystyle
 \prod_{j=0}^{11}\mathcal S(x_j\omega_j+y_j;\omega_j)=1
 \quad\text{for every }l=1,\ldots,11.}
\]

The modular-cocycle factorization and double-sine identity in the proof
of RW Proposition 5 identify this product with the modulus of the
corresponding modular quantum dilogarithm. That analytic factorization
uses only the displayed period and rational representatives; its proof
does not require an ideal interpretation. Thus it proves the needed
absolute value `1` on the actual conductor-two lattice.

The separate exact phase computation is still necessary to conclude
`E(l,l)=+1`, rather than merely a value of modulus one.

## Sources and scope of adaptation

- S. Yamamoto, *On Shintani's ray class invariant for totally real number
  fields*, <https://arxiv.org/pdf/0805.4282>, Proposition 2.2, §§4.2–4.3,
  and especially §5.2. The signed-cone proof above explicitly extracts
  and proves the required lattice statement; it does not invoke the
  ideal-theoretic theorem with unmet hypotheses.
- D. Radchenko and C. Wheeler, *Real quadratic fields and finite quantum
  dilogarithms I*, <https://arxiv.org/html/2609.21892v2>, §2.3,
  proof of Proposition 5, for the analytic double-sine/modular-cocycle
  factorization.

This establishes the absolute-value identity only. No classification
status is changed by this note alone.

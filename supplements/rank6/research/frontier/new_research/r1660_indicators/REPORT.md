# R6_8_1660: FRS exhaustion and additional even-indicator identities

The current relative-center ring passes every direct Fuchs–Runkel–Schweigert
second-indicator test, including tests on arbitrary nonsimple objects.
I obtain additional all-order even-indicator identities below, but no
contradiction and no reduction of the 1670 retained center profiles.
The precise remaining gap is stated at the end.

## Assumptions and notation

Use the proved pseudo-unitary Galois reduction. Let

\[
B=\mathcal I\boxtimes\mathcal I^{\rm rev},\quad
p=(g,1),\ q=(1,g),\ e=pq,\ u=(\sigma,1),\ z=(1,\sigma),\ w=uz.
\]

The remaining relative center has simples B and Bt, and

\[
t^*=et,\qquad t^2=e+(2u+2uq+3w)t.
\]

Write Y=ut, Z=zt, S=wt and T=σX. These letters Z and z denote
objects here, not a center functor. The frozen release proves a coherent
involution exchanging X and gX, so their ordinary indicators agree.
All indicator equalities below concern the canonical positive spherical
structures; none asserts general preservation by the forgetful functor.

## All-object FRS exhaustion: a complete proof

Liu–Palcoux–Ren–Vercleyen, *Triangular Prism Equations and Categorification*,
arXiv:2203.06522v5, Theorem 3.9, proves for a pivotal fusion category that
a self-dual simple V with odd multiplicity in U*U has second indicator +1.
The theorem allows arbitrary U. The primary source was checked at
<https://arxiv.org/pdf/2203.06522>, page 11; the abstract page confirms
this is v5, revised 14 December 2025.

The second indicators in B are products of the Ising signs (1,1,−1).
The four negative ones are u, uq, z, pz. Outside B, only S is self-dual:
multiplication by e fixes exactly w among the nine B simples. Its
forgetful image is X⊕gX, whose two distinct self-dual summands each have
indicator +1 and multiplicity one. A nondegenerate self-duality on S
therefore has positive transpose sign, so ν₂(S)=+1. The other eight
outside simples have indicator zero. This enumerates every possible
negative second-indicator simple of the relative center.

For a simple b of B, the product b² is supported only on the four
invertibles of B, because σ²=1+g in each factor. Consequently neither
b*b=b² nor

\[
(bt)^*(bt)=b^2 e t^2=b^2+b^2e(2u+2uq+3w)t
\]

contains u, uq, z, or pz. All 18 simple-source diagonal multiplicities
are therefore zero for all four negative targets.

Now let U=⊕ᵢmᵢUᵢ be arbitrary and V a self-dual target. Duality gives

\[
N_{U_i^*,U_j}^{V}=N_{U_j^*,U_i}^{V}.
\]

Thus

\[
[U^*U:V]=\sum_i m_i^2N_{U_i^*,U_i}^{V}
 +2\sum_{i<j}m_im_jN_{U_i^*,U_j}^{V}.
\]

For the four negative targets the first sum vanishes and the second is
even. This proves the assertion for every U without bounded enumeration.
The accompanying standard-library verifier reconstructs all 18 products,
checks associativity, duality, the full sign list, the zero diagonal
coefficients and the symmetric cross terms. It writes certificate.json.

The same reasoning applies directly in the original rank-six ring:
σ is the only negative simple and no simple square contains σ.
Hence applying Theorem 3.9 again to arbitrary direct sums, powers or
tensor words in either of these two categories cannot yield a new
contradiction.

## Additional all-order even-indicator constraints

For even n put

\[
a=\nu_n(t),\quad c=\nu_n(Y),\quad f=\nu_n(Z),\quad s=\nu_n(S),
\quad x=\nu_n(X),\quad v=\nu_n(T),\quad h=\nu_n(\sigma).
\]

Then necessarily

\[
\boxed{2a+\sqrt2(c+f)+s=(2+\sqrt2h)x+(\sqrt2+h)v.}\tag{1}
\]

Proof. The canonical central lifts of p and q are order-two invertibles
with twist −1. Central-invertible indicator transport therefore makes
the indicators of t,pt,qt,et all equal for even n. Duality makes the
indicators of Y,qY equal and those of Z,pZ equal. Write
Wₙ(D)=∑ᵢdᵢνₙ(i). The spherical center formula makes Wₙ Morita invariant
and multiplicative under Deligne products. Since E is Morita equivalent
to C⊠Iᵒᵖ,

\[
W_n(E)=W_n(C)W_n(I).
\]

The B contribution is Wₙ(I)², the contribution of Bt is
d[4a+2√2(c+f)+2s], and

\[
W_n(C)=(2+\sqrt2h)+d(2x+\sqrt2v),\quad W_n(I)=2+\sqrt2h.
\]

Subtracting the B contribution and dividing by 2d proves (1).
This uses only Morita invariance, central transport, duality, and the
already proved tensor involution.

For n not divisible by 8, Q(ζₙ) does not contain √2, while all six
unknown indicators in (1) lie in Q(ζₙ). The ordinary Ising modular
indicator formula, with ν₂(σ)=−1, gives

\[
\nu_n(\sigma)=\sqrt2\cos(n\ell\pi/8),\quad
\ell\in\{3,5,11,13\},\qquad n\text{ even}.
\]

These four choices give the same even-indicator sequence. Hence:

* For n≡4 mod 8, h=0 and (1) separates into
  **2a+s=2x** and **c+f=v**.
* For n≡2 mod 4, h is rational and equals −1 for n≡2,14 mod16,
  and +1 for n≡6,10 mod16. Equation (1) separates into
  **2a+s=2x+hv** and **c+f=hx+v**.

The absence of √2 follows from its conductor 8: the quadratic field
Q(√2) is a subfield of Q(ζₙ) exactly when 8 divides n. At n=2 these
identities reduce to a=c=f=0 and s=x=v=1, h=−1, and are consistent.
For 8|n the unsplit equation (1) remains valid; splitting coefficients
there would be unjustified.

The Ising formula is the specialization of the modular indicator
formula in Ng–Schauenburg, *Frobenius–Schur Indicators and Exponents of
Spherical Categories*, arXiv:math/0601012, Theorem 7.5. The same paper's
Theorem 4.1 supplies the center formula used for Wₙ. Primary source:
<https://arxiv.org/abs/math/0601012>.

## Degree-three projective-action boundary

The frozen release already combines the fermion stabilizer Clifford
action with even cyclic multiplicities. Its constraints are exactly

\[
a+b+c=4,\quad a,b,c\ge0,\quad
(4-a,4-b,4-c)\in(2\mathbb Z_{\ge0})^3.
\]

The six possibilities give ν₃(T)∈{2,2ω,2ω²,−4,−4ω,−4ω²}.
Each of these six is feasible as an abstract Clifford/rotation
representation: take the two-dimensional Clifford rotation with
eigenvalues ω,ω² and tensor its multiplicity space with the appropriate
order-three scalar eigenspaces. The required multiplicities a,b,c are
all even, so this representation can be split into two identical
rotation representations, compatibly with an independent commuting
involution. Thus the already stated relations alone cannot reduce the
six-element set. A stronger conclusion requires a further geometric
commutation relation, not just the assertion that a coherent C₂ action
exists. This abstract construction does not assert a tensor category.

## Precise remaining gap

There is no exclusion. To exploit (1), one must determine or bound
the simultaneous cyclic spectra of t,Y,Z,S in the relative center,
or compute generalized rotation traces with central targets in B.
The known rank-six twist profiles do not specify these spectra, and a
forgetful functor does not supply their ordinary indicators. Likewise,
an additional relation between the equivariant involution and the
fermion pair-insertion operators must be proved diagrammatically
before a larger projective symmetry algebra can be imposed.

No frozen-release file was changed. No profile count is claimed to
change. Run `python verify.py` here to reproduce the exact ring audit.

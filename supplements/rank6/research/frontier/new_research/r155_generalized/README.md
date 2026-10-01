# R6_4_155: generalized rotations for the completed modular candidate

These are necessary indicator checks, not a categorification certificate.
The checks use the rank-26 normalized S matrix and fusion tensor in
`../r155_modular/reconstruction.json`, together with the frozen profile-296
restriction vectors and twists. No frozen-release file is modified.

For the original rank-six category C, `check.py` constructs the full rank-52
normalized S matrix as the tensor product of the semion matrix and the
rank-26 matrix. The semion partner adds 6 to the twist exponent modulo 24,
and its restriction is obtained by tensoring with the original invertible g.
For every original simple V and every central simple Z, the trace used is

\[
\nu_{m,1}^{Z}(V)=\sum_{A\in\operatorname{Irr}Z(C)}
s_{ZA}\theta_A^m[F(A):V],
\]

where s is the normalized center S matrix. This is Ng–Schauenburg,
*Congruence Subgroups and Generalized Frobenius–Schur Indicators*,
[arXiv:0806.2493](https://arxiv.org/pdf/0806.2493), Corollary 5.6.
Lemmas 2.5 and 2.7 show that the generalized n-rotation E has
Eⁿ=θ_Z⁻¹. Accordingly the checker normalizes E by θ_Z^(1/n) before
Fourier inversion. Proposition 2.8 groups tensor factors for non-coprime
rotation powers. Cyclotomic automorphisms give the remaining powers.
The Hom dimension is computed from the rank-six fusion tensor.

The checker tests every one of 52 central targets against all six original
simples, at every order 2 through 24: 7176 cyclic spectra. All eigenvalue
multiplicities must be nonnegative integers. It also tests all 312
degree-one identities
ν₁,₁^Z(V)=θ_Z⁻¹[F(Z):V], fixing the target-twist convention.

`check_B.py` applies the same center formula to the modular category B.
For a target (i,j) in Z(B)=B⊠Bᵣₑᵥ, its underlying object is i⊗j and its
twist is θᵢ/θⱼ. With normalized B matrix s, its generator trace is

\[
\sum_{a,b}s_{ia}s_{j^*,b}
 (\theta_a/\theta_b)^2N_{ab}^{k}.
\]

The dual on the second S row is essential: the reverse-braided factor
has conjugate normalized S. Using a fusion-matrix convention
Nₖ[a,b]=Nₐ,b*^k instead would absorb this dual into the tensor indices.
Every one of the 26³ degree-one normalizations is checked explicitly.
The degree-two Hom dimension is
∑ᵣNᵢⱼʳNₖₖʳ. Multiplication of the trace by
(θᵢ/θⱼ)^(1/2) then gives the two eigenmultiplicities (H±trace)/2.
This covers all 26 original B simples and all 676 central targets.

The summary certificate records both scopes and hashes the detailed receipts
and the reconstructed modular-data source. Passing orders 2–24 is a finite
statement. The modular congruence theorem controls coprime indicator pairs;
it does not by itself make cyclic-spectrum feasibility at all tensor orders
a consequence of these checks. At non-coprime powers, traces involve V^g,
whose decomposition and Hom dimensions depend on the actual g.

Run `python check.py`, `python check_B.py`, then `python summarize.py`.

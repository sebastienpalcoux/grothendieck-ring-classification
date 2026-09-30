# A categorical realization of R6_4_91

Let C=C(sp_6,4) be the unitary WZW fusion category. We use finite Dynkin labels abc, with a+b+c≤4. Its root-lattice subcategory C_ad consists of the 19 weights with a+c even.

The adjoint representation gives the conformal embedding

    (sp_6)_4 ⊂ (so_21)_1.

The conformal extension has its actual connected étale algebra

    A = 000 ⊕ 210 ⊕ 004 ⊕ 121.

Thus D=C_A is a fusion category, and D0=(C_ad)_A is a fusion subcategory. These constructions use the multiplication of the conformal extension; an algebra is not being inferred from a modular invariant. The unitary conformal inclusion gives the corresponding Q-system and unitary module categories. We prove K0(D0)=R6_4_91.

## 1. Branching and the known local subcategory

Write I=C(so_21,1), an Ising category. Its simples are 1,ψ,σ with dimensions 1,1,√2, and twists 1,−1,exp(2πi·21/16). Their restrictions to C are

    U(1) = 000+210+004+121,
    U(ψ) = 200+030+022+301,
    U(σ) = 2·111.

These are direct instances of the adjoint conformal branching formulas of Cellini–Kac–Möseneder Frajria–Papi, Theorem 3.9 and Proposition 4.1 [1]. The former enumerates the abelian upper ideals of the positive-root poset: the sum of the roots is the highest weight and the parity of the ideal separates vacuum and vector. The latter gives 2^{floor(rank/2)} copies of the affine Weyl-vector module for the spinor. The program enumerates all 2^9 subsets of the nine positive C3 roots; exactly eight are abelian ideals. Hence no branching terms have been guessed.

The three local modules lie in D0. They obey ψ²=1, ψσ=σ, σ²=1+ψ.

## 2. The six simple objects are forced

For F(λ)=λ⊗A, the free-module adjunction gives

    <F(λ),F(μ)> = Σ_a [A:a] N_{λ,a}^{μ}.

Restricting λ,μ to the 19 even weights gives an exact Gram matrix G. The local columns are obtained from the displayed branching formulas. In addition F(010) has norm one and is orthogonal to 1,ψ,σ, so it is a new simple τ.

After subtracting the four known simple columns, the residual Gram matrix is 2vv^t, where v has integral nonnegative entries and v_002=1. Therefore F(002) consists of two distinct new simples, say x+y. To see uniqueness of this factorization, its diagonal entry is two, so the distinguished row is a sum of two unit vectors; rank one forces every other row to be proportional to this row. There can be no additional column supported away from that row. Free modules generate the module category, so these are all the simple objects:

    1, x, y, σ, ψ, τ.

The resulting 19×6 free-module matrix B is recorded in exact_certificate.json. In particular

    F(010)=τ, F(200)=ψ+τ, F(002)=x+y,
    F(111)=2σ+2x+2y+2τ.

The image of the central free functor spans a five-dimensional subspace of K0(D0)⊗C (the two x,y columns coincide and its rank is five). Consequently its algebraic center has dimension at least five. A six-dimensional semisimple algebra with a noncommutative matrix summand has dimension minus center dimension at least three. Thus K0(D0) is commutative.

All four known simples are self-dual. As F(002) is self-dual, either x*=y or x*=x and y*=y.

## 3. The exact tensor completion

The source fusion coefficients, B, the three Ising products, Frobenius reciprocity, and associativity suffice to enumerate the possible tensors. This is an enumeration of four or five bounded integer parameters, not an induction or modular-data search. The affine equations obtained before associativity imply each parameter lies between zero and four; the checker verifies that bound directly from coefficient nonnegativity.

If x*=y, there is exactly one associative nonnegative tensor. Its 216 coefficients agree with target_R91.json. If x,y are self-dual, there are three possibilities, with the following x²=y²:

    1+2y+2τ,  1+x+y+2τ,  1+2x+2τ.

The first and third differ only by interchanging x,y. We next rule out all three using the already existing conformal model.

## 4. Excluding the middle self-dual tensor

Corollary 3.30 of [2] gives the actual braided equivalence

    Z(D) ≅ C ⊠ I^rev.

The central simple (λ,a) forgets to F(λ)⊗_A a. By adjunction,

    <F(λ)⊗_A a,F(μ)> = Σ_ν [U(a):ν] N_{ν,λ}^{μ}.

The Ng–Schauenburg center formula [3] therefore computes the second indicator of F(μ) directly from the known source and branching data:

    ν2(F(μ)) = (1/dim D) Σ_{λ,a,ν}
      θ_λ² θ_a^{-2} d_λ d_a [U(a):ν] N_{ν,λ}^{μ}.

Exact arithmetic in Q(ζ32) gives ν2(F(002))=0. Since D0 is a full spherical fusion subcategory of D, this is also its indicator computed in D0.

For completeness, a self-dual simple X in a pivotal category has a symmetric self-duality on X⊗X: choosing f:X→X* with pivotal transpose f^t=εf, ε∈{±1}, the tensor-product self-duality has transpose ε² times itself. Every self-dual simple occurring with multiplicity one consequently inherits a nondegenerate symmetric self-duality and has second indicator +1. This argument uses the reversed-order identification (X⊗X)*=X*⊗X* and needs no braiding.

In the middle tensor, x is self-dual and x²=1+x+y+2τ. Both x and y occur with multiplicity one, so ν2(x)=ν2(y)=1. This contradicts ν2(F(002))=ν2(x+y)=0.

## 5. Excluding the other self-dual tensors

The simple current J=004 is a boson in the Müger center of C_ad. It is a summand of A, and 1+J is its regular algebra. Let

    E = (C_ad)_{1+J}

be the modularization. Condensation in stages identifies D0 with E_{A'}, where A' is A viewed as a (1+J)-module algebra. Its local module category remains I. Hence

    Z(D0) ≅ E ⊠ I^rev.

Equivalently, one can use the canonical Z2-grading of D: in Z(D)=C⊠I^rev its grading character is (J,1); centralizing and de-equivariantizing this object gives precisely E⊠I^rev.

The action of J on affine Dynkin labels is reversal; in finite labels it is

    J(a,b,c)=(b,a,4−a−b−c).

The program derives this action from its certified source fusion tensor. On the 19 even weights there are eight size-two orbits and three fixed weights 002,111,220. Each ordinary orbit gives one simple of unchanged quantum dimension; each fixed weight splits into two simples of half its quantum dimension. Thus E has rank14 and Z(D0) rank42. All these actual center dimensions are computed exactly without requiring any fixed-point S-matrix formula.

For either outer self-dual tensor, the Casimir characteristic polynomial is

    (t²−16t+32)(t⁴−128t³+2560t²−16384t+32768).

Its formal codegrees include f±=8±4√2. Since the ring is commutative, each formal codegree would require a simple constituent of I_D0(1) of dimension dim(D0)/f±; this is the standard formal-codegree induction theorem [4]. Neither value appears among the 42 known center dimensions. The exact checker verifies both nonoccurrences. This excludes the remaining self-dual tensors.

Only the non-self-dual tensor remains, and it is exactly R6_4_91. The construction provides a unitary categorification, with

    FPdim simples = (1,cot(π/16),cot(π/16),√2,1,√2 cot(π/16)),
    FPdim D0 = 4 csc²(π/16).

## 6. Exact, portable verification

From this directory run:

    python -m pip install -r requirements.txt
    python exact_certificate.py
    python complete_tensor.py

Together these take about two seconds in the development environment. They use explicit exceptions, so checks also run under python -O. No optimizer is used.

probe_data.json contains a proposed source C3_4 tensor. Its historical numerical proposal is not trusted: exact_certificate.py independently verifies all 42,875 character-product equations against the exact Weyl determinant over Q(ζ32), which uniquely certifies every fusion coefficient by the Verlinde diagonalization. It then reconstructs branching, the Gram factorization, the indicator zero, the simple-current orbits and the missing center dimensions. complete_tensor.py repeats the entire bounded completion with exact integer arithmetic, proves its parameter bounds, checks associativity, computes the Casimir polynomials and compares every target coefficient. target_R91.json is the frozen census tensor; both JSON files are bundled, with no dependency on the old archive.

## References

[1] P. Cellini, V. G. Kac, P. Möseneder Frajria, P. Papi, “Decomposition rules for conformal pairs associated to symmetric spaces and abelian subalgebras of Z2-graded Lie algebras,” Advances in Mathematics 207 (2006), 156–204. Theorem3.9 and Proposition4.1. https://arxiv.org/abs/math-ph/0506043

[2] A. Davydov, M. Müger, D. Nikshych, V. Ostrik, “The Witt group of non-degenerate braided fusion categories,” J. Reine Angew. Math. 677 (2013), 135–177. Corollary3.30; Sections6.1–6.2. https://arxiv.org/abs/1009.2117

[3] S.-H. Ng, P. Schauenburg, “Frobenius–Schur indicators and exponents of spherical categories,” Advances in Mathematics 211 (2007), 34–71. https://arxiv.org/abs/math/0601012

[4] V. Ostrik, “Pivotal fusion categories of rank3,” Theorem2.13. The theorem identifies a simple summand corresponding to a one-dimensional character with dimension dim(D0)/f. https://arxiv.org/abs/1309.4822

[5] Y.-Z. Huang, A. Kirillov Jr., J. Lepowsky, “Braided tensor categories and extensions of vertex operator algebras,” Communications in Mathematical Physics 337 (2015), 1143–1159. The extension/algebra and local-module correspondences give the categorical reading of the conformal extension. https://arxiv.org/abs/1406.3420

# A uniform Gram obstruction for another near-group model route

This lemma concerns a potential construction route, not a general exclusion of any rank-nine source. It does not assert the existence of any algebra.

Let B be a complex fusion category with eight invertibles G, four noninvertibles X_q forming a transitive left G-set with stabilizer H of order two, and uniform noninvertible fusion multiplicity two. Write Q=G/H; for the applications Q=V4 and H is normal. The argument allows any duality shift and any left-right quotient automorphism in the two-orbit ring formulas.

Suppose A is a connected separable algebra whose underlying object contains no invertible other than a single copy of 1. Then its underlying object is either

    A=1,   or   A=1+Σ_(q∈Q) X_q.

In the second case its right-module category has rank twelve. Consequently its Morita dual has rank at least twelve, and this move cannot directly produce one of the rank-nine source categories.

## Proof from the induction Gram matrix

Write A=1+Σ b_q X_q with b_q nonnegative integers and B0=Σ b_q. Let F(U)=U⊗A be induction into right A-modules. Frobenius reciprocity gives

    ⟨F(g),F(h)⟩=δ_(g,h),   g,h∈G.

Thus the eight induced invertibles are distinct simple modules. For each induced X_q, project off those eight orthonormal simple rows. The remaining Gram matrix R is the Gram matrix of genuine nonnegative integer module multiplicities, and in particular is positive semidefinite. Uniform multiplicity two gives

    ⟨F(X_q),F(X_p)⟩=δ_(q,p)+2B0.

The overlap vector with the eight F(g)'s is a translate of the four coefficients b, each repeated |H|=2 times. Therefore

    R_(q,q)=1+2B0−2Σ b_t²
           =1−2Σ b_t(b_t−1).

It is a nonnegative integer. Every summand b_t(b_t−1) is nonnegative and even, so all b_t are 0 or 1, and every diagonal entry of R is 1.

Let S={q:b_q=1}. For q≠p the remaining inner product is

    R_(q,p)=2(|S|−|S∩(S+φ(q−p))|),

where φ is the fixed automorphism of Q determined by the left-right quotient action (and is the identity for the two surviving D8 types). Equivalently one may relabel the four Gram rows by this automorphism.

It is a nonnegative even integer. Positive semidefiniteness of each two-by-two principal minor with diagonal entries 1 forces |R_(q,p)|≤1, so every offdiagonal entry is zero. Hence S is invariant under every translation of Q. It is empty or all of Q, proving the asserted list.

If S=Q, each F(X_q) contains the eight known simple modules once. After their removal the four residual rows have Gram matrix I4, so each is a different new simple module. There are exactly twelve simples: induction is dominant, since every A-module is a summand of induction of its underlying object for a separable algebra. In block form the uniquely forced induction matrix, up to ordering the simple modules, is

    F = [[I8, 0], [J_(4,8), I4]].

Finally, for any invertible Morita bimodule category M between fusion categories C and D,

    rank(M)² ≤ rank(C) rank(D).

One standard proof uses the two canonical algebra objects L_C,L_D in their common Drinfeld center. The dimensions of their endomorphism spaces are rank(C),rank(D), and dim Hom(L_C,L_D)=rank(M). Cauchy–Schwarz for their nonnegative simple-multiplicity vectors gives the inequality. Equivalently it follows from the full Morita Gram identity used in this project's rank computations. Here rank(M)=rank(B)=12, so rank(B*_M)≥12.

## Scope boundary

Algebras containing additional invertible summands are not covered. Nor does the argument exclude a longer chain of Morita moves or a different starting category. In particular the algebra 1+g used in the proven TY-to-D8 reduction has two invertible summands and falls outside the premise.

All steps above use exact integer Gram identities and the general separable-algebra/module-category formalism. No unitary reconstruction, numerical solution, or identification of a commuting based permutation with an actual module functor is used.

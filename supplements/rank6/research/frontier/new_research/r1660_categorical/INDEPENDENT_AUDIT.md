# Independent audit of the R1660 Morita-dual reduction

**Result: PASS for the stated necessary-condition claims.** In particular,
the IV equal-sign exclusion and the rank-eight second-indicator exclusion
are sound. The argument does not construct module associators or prove
categorification/noncategorification of the original ring.

This audit left the R155 modular-data artifacts unchanged. It read the
manuscript and all three scripts, checked the primary sources, and performed
an independent complete Gram enumeration in `independent_audit.py`.
The exact receipt is `independent_audit_receipt.json`; runtime was 6.5 seconds.

## Full-center saturation and faithfulness

Ostrik, *Pivotal fusion categories of rank 3*, Remark 2.19 explicitly gives
the linking-category bimodule identification with Hom between the two
induced-unit objects. The last paragraph of that remark explicitly supplies
the required twist condition in the positive-dimensional case and explains
pseudo-unitarity of the Morita dual. Corollary 2.16 supplies the endomorphism
algebra identification. Thus the manuscript is using the correct statement,
including the bimodule structure; it is not replacing categorical Morita
information by an unsupported ordinary-character analogy.

The four g=1 characters have formal codegrees 4(1+x²), with the two reciprocal
negative roots at each σ=±√2. Since xx'=-1,

    1/[4(1+x²)] + 1/[4(1+x'²)] = 1/4.

Their induced-unit dimensions therefore sum to D/2. The two g=-1 characters
both have codegree 4. Their multiplicities m₊+m₋=2 supply the other D/2,
regardless of the sign pattern of V. All dimensions are positive, so the
already known constituents exhaust the Lagrangian algebra. This validates
both ranks 6/8 and excludes unseen extra constituents.

Every constituent of the Lagrangian algebra occurs in I_C(1). Hence every
matrix block of its endomorphism algebra acts faithfully on the Hom
bimodule. Its dimension is exactly 4+m₊²+m₋², equal to the commutant dimension.
In particular, the simple dual action matrices are linearly independent.
This last point is essential for the square Gram-factor enumeration below.

## Gram identity and the forced columns

The identity follows directly from linking-category associativity. Expand

    (m_b m_a*) m_c = m_b (m_a* m_c)

and take the coefficient of m_d. The first side gives the sum over C
simples; the second gives the sum over D simples. Replacing the latter
summation label y by y* and using Q_(y*)=Q_yᵀ gives precisely equation (5).
With coordinates flattened as (c,a), its matrix is

    K[(c,a),(d,b)] = Σ_x N_x[c,d] N_x[a,b]
                   = Σ_y Q_y[c,a] Q_y[d,b].

Thus K=Σ_x N_x⊗N_x in the script's row-major convention is correct.
No rank or fullness assumption is needed for this identity itself.

I is always a simple dual action. The established central lift of g makes
left tensoring by g a module autoequivalence; its action is the nonidentity
permutation G, so it gives a distinct invertible dual simple. Subtracting
I and G is therefore justified.

For type III, K[0,0]=2, I[0,0]=1, and G[0,0]=0. Nonnegative integrality
forces exactly one other simple Q to have Q[0,0]=1. The full coordinate
column then gives Q=mat(K[:,0]-vec(I)). Its G-translate is again simple.
The matrices are directly distinct from one another and from I,G.

More importantly, my independent enumeration **does not subtract these
extra type-III columns at all**. It subtracts only I,G and finds the full
Gram factors. The purported Q and GQ appear automatically in every such
factor. Thus the final enumeration does not depend on an unchecked forced
subset or on the short type-III reconstruction.

## Completeness of the finite enumeration

After subtracting known simple columns, let H have rank r. Faithfulness
shows that exactly r simple columns remain. Select an invertible r-by-r
principal submatrix B=H[J,J]. In any factorization H=QQᵀ, the square matrix
V=Q[J,*] is invertible and VVᵀ=B. Consequently each column v of V satisfies

    vᵀ B⁻¹ v=1,     0≤v_i≤floor(sqrt(B_ii)).

Every full column is H[:,J]B⁻¹v. Conversely, r such lifted nonnegative
integer columns that are pairwise orthogonal for B⁻¹ give the whole Gram
factorization. This is an exact equivalence, not a relaxation. Searching
all bounded vectors and all r-element orthogonal subsets is complete.

The independent replay uses a different pivot tie-break, builds K by its
explicit index formula, enumerates ordinary combinations rather than the
original recursive clique routine, and subtracts only I,G in every case.
It also checks all associativity equations for each accepted fusion tensor.
The accepted action bases agree exactly, up to their ordering, with the
original receipt.

| Type | Remaining rank | Candidate columns | Full Gram bases | Fusion bases |
|---|---:|---:|---:|---:|
| II | 4 | 4 | 1 | 1 |
| III mixed | 4 | 4 | 1 | 1 |
| III equal | 6 | 12 | 2 | 2 |
| IV mixed | 4 | 12 | 3 | 2 |
| IV equal | 6 | 12 | 0 | 0 |

The different type-III intermediate counts arise solely because this audit
does not presubtract Q,GQ. The final bases are identical.

For IV equal, the independent pivot bounds are (1,1,2,2,2,3): only 432
integer coordinate vectors are searched. Exactly 12 lift to candidate
columns. Their orthogonality graph has maximum clique size **4**, whereas
six columns are required. This gives a particularly small complete
certificate of the zero result. The receipt stores its quadratic form,
all twelve vectors, and every orthogonality edge.

Global X↔gX sends V to -V and merely permutes the set of six left-action
matrices, leaving K unchanged. Thus choosing representative sign patterns
does not omit the opposite-sign-labelled cases.

I also directly checked the recorded generators: the three original-ring
solutions obey σ²=1+g and X²=1+3(1+g)X+4σX. The other rank-six solution
obeys the displayed E6-extension relations and has maximum coefficient 16.
Both rank-eight solutions are noncommutative and have maximum coefficient 3.

## Weighted second indicators

Ng–Schauenburg, *Frobenius–Schur indicators and exponents of spherical
categories*, Theorem 4.1 gives the indicator as the normalized center twist
trace. Multiplying by dimensions and summing gives

    τ₂(Z(F)) = dim(F) Σ_Z ν₂(Z) dim(Z).

Under pseudo-unitary Morita equivalence, the positive spherical center
structures agree, so this weighted sum is invariant. The original category
has W₂=12+6√2+6√3+4√6.

I independently enumerated u∈{0,2} and the two aggregate signs in
{-2,0,2}. When the a₀ pair is nonselfdual, no combination
u+s_d d+s_b b₀ equals W₂. When the b₀ pair is nonselfdual, the unique
combination is (u,s_d,s_a)=(2,2,2). This proves the exclusion and forces
all surviving selfdual simple indicators to +1. No assumed sign for the
nontrivial invertible is needed.

## Sources inspected

- Ostrik, arXiv:1309.4822, Theorem 2.13, Corollary 2.16, Remark 2.19,
  especially printed pages 7–8: https://arxiv.org/pdf/1309.4822
- Ng–Schauenburg, arXiv:math/0601012, Theorem 4.1:
  https://arxiv.org/pdf/math/0601012

The remaining three Morita-dual based-ring possibilities are therefore
correct as necessary alternatives: the original rank-six ring, the
rank-six E6 extension, and the rank-eight ring with nonselfdual b₀ pair.
They remain possible based rings, not constructed categories.

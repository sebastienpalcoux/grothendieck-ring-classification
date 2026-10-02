# Exhaustion of every finite-p Lim inequality for both rank-six residual rings

**Result.** Both R6_4_155 and R6_8_1660 satisfy every inequality in Junhwi Lim, arXiv:2601.13490v2, Corollary3.4, for every triple of simple labels, every real exponent 1≤p<∞, and every nonnegative input vector. This is an exact statement about the fusion tensors. It supplies neither a model nor a noncategorification proof. These particular inequalities are necessary for unitary categorification; their passage does not establish categorifiability.

The result is stronger than the earlier bounded numerical search and the exact p=∞ support test. It follows from finitely many exact nonnegative probability couplings and the ordinary Minkowski inequality.

## 1. Normalize the criterion

Let N_{uv}^w be the fusion coefficients and d_u their positive Frobenius–Perron dimensions. Set

    P_{uv}(w) = N_{uv}^w d_w/(d_u d_v).

Every P_{uv} is a probability vector. For fixed i,j,k, let μ_l=P_{ij}(l) and ν_m=P_{jk}(m). Dividing both sides of Lim's displayed inequality by the common positive factor d_i^{1/p}d_k gives exactly

    [ Σ_l μ_l (Σ_n P_{lk}(n) a_n)^p ]^{1/p}
        ≤ Σ_m ν_m [Σ_n P_{im}(n) a_n^p]^{1/p}.              (1)

This normalization is valid without a commutativity assumption.

## 2. A finite sufficient certificate for every exponent and vector

Suppose there is an array q_{lmn}≥0 satisfying the three pairwise marginal identities

    Σ_n q_{lmn} = μ_l ν_m,
    Σ_m q_{lmn} = μ_l P_{lk}(n),
    Σ_l q_{lmn} = ν_m P_{im}(n).                          (2)

The first identity makes L and M independent under this probability distribution. Ignore any zero-weight l or m, and define

    f(l,m) = Σ_n q_{lmn} a_n/(μ_l ν_m).

The second identity implies Σ_mν_m f(l,m)=Σ_nP_{lk}(n)a_n. Apply the ordinary weighted Minkowski inequality, then conditional Jensen:

    ||Σ_m ν_m f(·,m)||_{Lp(μ)}
        ≤ Σ_m ν_m ||f(·,m)||_{Lp(μ)}
        ≤ Σ_m ν_m [Σ_l μ_l Σ_n q_{lmn} a_n^p/(μ_lν_m)]^{1/p}
        = Σ_m ν_m [Σ_n P_{im}(n) a_n^p]^{1/p}.

The last equality is the third identity in (2). The left side is exactly the left side of (1). This proves (1) simultaneously for all real p≥1 and all a≥0. Taking p→∞ also recovers the support-limit inequalities. No finite grid, local minimum, numerical tolerance, or exponent cutoff is used in this implication.

## 3. Exact certificates for the two rings

The adjacent certificates.json stores the two full tensors, their source hashes, exact algebraic FP dimension vectors, and one sparse array q for every triple with all three labels noninvertible.

- R6_4_155 has two noninvertible labels: all8 such triples are supplied, with168 positive entries in total.
- R6_8_1660 has four noninvertible labels: all64 such triples are supplied, with952 positive entries in total.

For a triple containing an invertible label, at least one of μ or ν is supported at a single label. The verifier constructs q directly. If μ is concentrated at l0, use q_{l0,m,n}=ν_m P_{im}(n). If ν is concentrated at m0, use q_{l,m0,n}=μ_l P_{lk}(n). It checks all three identities explicitly rather than relying on an unchecked simplification.

Thus the verifier checks every one of216 triples for each ring. For each triple it verifies the108 exact pairwise marginal equations, for23328 equations per ring. It also verifies all probability entries are nonnegative in the specified real embedding, using rational root isolation. The positive FP character equations are checked against every fusion product. An optional external tensor file binds the certificates directly to the repository census.

The supplied number fields are exact; coefficient arrays use descending polynomial order. All sign conclusions and marginal equalities are exact. Floating-point linear programming was used only to discover sparse supports. The supports were then solved over the exact FP fields and independently replayed. The verifier imports no floating-point numerical package and does no linear programming.

## 4. Scope for further computation

A further numerical search over p or a in Corollary3.4 cannot find a valid violation for these tensors: (2) already proves all of its inequalities. The two categorification questions remain unresolved, so useful further searches must address a different necessary condition or a model construction.

This result does not assert that every possible commuting-square, Morita-equivalent-ring, or enlarged-object variant of Lim's framework has been exhausted. The exact exhausted family is Corollary3.4 on the two six-element fusion bases, with all triples, exponents, and nonnegative vectors.

Primary source: J. Lim, *Noncommutative Minkowski integral inequality and a unitary categorification criterion for fusion rings*, arXiv:2601.13490v2, Corollary3.4 and equation(15), pp9–10: https://arxiv.org/pdf/2601.13490 . The coupling implication above is proved explicitly, rather than attributed to that paper.

# Independent audit of positivity exclusions

Audit completed 2 October 2026. **PASS:** all 31 certificates for 28 rings are valid unitary obstructions. The two FP-dimension-40 cases additionally admit valid upgrades to general complex non-categorifiability. No other scope upgrade is asserted.

## The support-limit inequality

The normalization was checked against Junhwi Lim, *Noncommutative Minkowski integral inequality and a unitary categorification criterion for fusion rings*, [arXiv:2601.13490v2](https://arxiv.org/html/2601.13490v2), Corollary 3.4, equation (15). This is a necessary inequality for spherical unitary categories; unitary fusion categories have their canonical positive spherical structure.

For a subset S, put a_n=1 if n is in S and a_n=0 otherwise. Taking p to infinity in (15) gives

\[
\max_{l:N_{ij}^{l}>0}\frac{\sum_{n\in S}N_{lk}^{n}d_n}{d_l}
\ \leq\
\sum_{\substack{m:N_{jk}^{m}>0\\\exists n\in S:N_{im}^{n}>0}}
\frac{N_{jk}^{m}d_m}{d_j}.
\]

Indeed a finite weighted p-norm tends to the largest supported entry, and each right inner term tends to one when its support meets S, and zero otherwise. Thus checking one supported l against the right side is enough for an obstruction. A strictly positive limiting gap also implies failure for some sufficiently large finite p. This is a derived necessary inequality, not an assertion that the paper states a theorem at p=infinity.

The nine support certificates use exactly this formula. Their subsets, left support, right support and strictly positive algebraic gaps were checked.

## The primary-three operator

Huang–Liu–Palcoux–Wu, *Complete positivity of comultiplication and primary criteria for unitary categorification*, [arXiv:2210.00792](https://arxiv.org/pdf/2210.00792), Theorem 3.12, equation (3.7), requires

\[
Q=\sum_i d_i^{-1}N_i\otimes N_i\otimes N_i\succeq0
\]

for a unitarily categorifiable fusion ring. Here the regular fusion-matrix operator norm is d_i. Transposing the regular-action convention does not change its quadratic form. All audited tensors satisfy N_{i*}=N_i^T, so Q is self-adjoint. Each recorded integer vector v has an exactly negative value v^T Qv. These are necessary unitary conditions; passing or failing them alone is not a general categorification criterion.

## Exact and independent computation

I reviewed and reran `independent_audit.py`: **28 rings, 22 primary certificates and 9 support certificates passed**. It checks the tensors against the existing census, their SHA-256 values, nonnegative integral structure constants, units, duality and associativity. It verifies irreducibility of each field polynomial, isolation of exactly one real root, strictly positive normalized dimensions satisfying every dimension identity, and all signed values by rational interval arithmetic. No claimed positive model overlaps these 28 tensors.

I additionally wrote and ran `sparse_contraction_audit.py`, a second contraction implementation. It directly sums sparse six-index products with Python arbitrary-precision integers; it imports neither NumPy/SciPy nor the original contraction helper. All **22** primary coefficient vectors agree exactly with the certificates.

This also closes the potential original-int64 concern. For rank r, matrix bound M and vector bound V, every full contraction has absolute bound r^6 M^3 V^2. The largest bound here is **75,295,360,000**, below 2^63; the largest observed absolute coefficient is **33,663,164**. Every partial contraction is bounded by the corresponding sum of absolute monomials and hence by this same generous bound. The independent replay does not rely on fixed-width arithmetic in any event.

The input certificate SHA-256 is `868148f9ce8035fa52b6faabc69f563fa146ae603df9564804ba5e3111653c9b`. Receipts are `independent_audit_receipt.json` and `sparse_contraction_audit_receipt.json`.

## The two valid general upgrades

The exact FP-dimension lists are permutations of (1,1,1,1,2,4,4), hence their sum of squares is 40=2^3*5. Etingof–Nikshych–Ostrik, *Weakly group-theoretical and solvable fusion categories*, [arXiv:0809.3031](https://arxiv.org/pdf/0809.3031), Theorem 1.6, makes every hypothetical categorification solvable, hence weakly group-theoretical. Galindo–Hong–Rowell, *Generalized and quasi-localizations of braid group representations*, [arXiv:1105.5048](https://arxiv.org/pdf/1105.5048), Theorem 5.20 and Definition 5.13(1), then makes it tensor equivalent to a unitary fusion category. This contradicts the certified support inequality.

In zero-based census labels:

| Ring | (i,j,k), l | S | Right support | Forbidden inequality |
|---|---|---|---|---|
| R7_3_900 | (1,1,2), 1 | {0,3,4,5,6} | {2} | 2 <= 1 |
| R7_3_991 | (3,4,4), 3 | {0,1,2,5,6} | {4} | 2 <= 1 |

Therefore these two rings admit **no general fusion categorification over C**. For the other 26 rings this audit certifies **no unitary categorification only**; it does not exclude pseudo-unitary, spherical, pivotal, or general complex categorifications.

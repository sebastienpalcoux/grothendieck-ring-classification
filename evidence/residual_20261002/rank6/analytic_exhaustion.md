# Exact exhaustion of two analytic criteria for the rank-six residuals

Both R6_4_155 and R6_8_1660 satisfy every primary-n positivity criterion and
every support-limit inequality below. These are necessary tests only. Their
success is neither a model nor an exclusion, and does not settle finite-p
Minkowski inequalities, Frobenius–Schur indicators, or associator existence.

The replay reads the two census tensors at
`supplements/rank6/data/unresolved_tensors.json`, validates their fusion-ring
axioms, and binds their exact tensor hashes to `analytic_exhaustion.json`.
Its only nonstandard dependency is SymPy. It imports the existing exact
arithmetic helpers under `supplements/rank8/software` by a repository-relative
path and checks their SHA256 hashes. Run from any directory:

```
python evidence/residual_20261002/rank6/verify_analytic_exhaustion.py
```

All arithmetic is exact in Q(sqrt(2),sqrt(3),i); ordered quantities are reduced
to Q(sqrt(2)+sqrt(3)), whose positive primitive element is isolated by (3,4)
in t^4-10t^2+1. Rational interval refinement certifies every sign. Assertions
are explicit exceptions and remain active under `python -O`.

For a commutative fusion ring the commuting normal regular matrices N_i have
the characters as their simultaneous eigenvalues. A separating rational
linear combination supplies all six characters, each checked against every
fusion product. The eigenvalues of Q_3=sum_i N_i tensor N_i tensor N_i/d_i
are therefore sum_i chi_a(i)chi_b(i)chi_c(i)/d_i. All 216 triples are checked.
Huang–Liu–Palcoux–Wu, arXiv:2210.00792, Theorem 3.9, then gives positivity of
all primary-n matrices; Proposition 3.13 also gives the Schur product test.

| Ring | Character triples | Distinct eigenvalues | Zero values | Positive values |
| --- | ---: | ---: | ---: | ---: |
| R6_4_155 | 216 | 7 | 1 | 6 |
| R6_8_1660 | 216 | 15 | 1 | 14 |

Lim, arXiv:2601.13490v1, Corollary 3.4, gives a necessary Minkowski inequality
for unitary categorification. Its p→infinity limit applied to the indicator
of any subset S is, whenever N_ij^l>0,

    (sum_{n in S} N_lk^n d_n)/d_l <= (sum_{m in T} N_jk^m d_m)/d_j,
    T={m : N_jk^m>0 and some n in S has N_im^n>0}.

Cross-multiplying by positive d_l d_j and applying the dimension-character
equations reduces the difference to the integer linear form sum_v c_v d_v,
where c_v=sum_{m in T}N_jk^m N_lm^v-sum_{n in S}N_lk^n N_jn^v.
The script enumerates every i,j,k,l and every nonempty proper S; empty/full S
give trivial inequalities. It certifies the sign of every distinct form.

| Ring | Support inequalities | Distinct integer forms | Distinct exact values |
| --- | ---: | ---: | ---: |
| R6_4_155 | 17,856 | 54 | 18 |
| R6_8_1660 | 24,924 | 215 | 135 |

This also exhausts the entire p=infinity inequality for arbitrary nonnegative
vectors: decompose a vector by its level sets. Each coordinate and each maximum
over a finite support are the integrals of the corresponding indicator and
support-intersection indicator. Integrating the subset inequalities gives the
arbitrary-vector inequality. No such implication for finite p is asserted.

Primary sources:

* https://arxiv.org/abs/2210.00792 — Theorems 3.9 and 3.12, Proposition 3.13.
* https://arxiv.org/html/2601.13490v1 — Corollary 3.4, equation (15).

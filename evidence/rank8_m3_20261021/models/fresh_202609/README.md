# September 2026 odd Haagerup–Izumi model audit

The two new papers provide no model for any of the 277 exact-multiplicity-three baseline survivors, including all 35 currently unresolved rings. This is an exact exclusion of the specified **model families and their Morita duals**, not an exclusion of arbitrary categorification. No decision ledger is changed by this audit.

## Primary statements and their scope

* Tzu-Chen Huang, *Cyclic Haagerup–Izumi fusion categories at every odd order*, [arXiv:2609.15986v1](https://arxiv.org/html/2609.15986v1), Theorem 2.1, constructs spherical and pseudo-unitary categorifications of the cyclic HI rules for every odd order at least three. Section 1 explicitly says that a unitary structure on the positive-dimensional category is not established.
* Terry Gannon, Andrew Schopieray and Harshit Yadav, *On Haagerup–Izumi fusion categories*, [arXiv:2609.25185v1](https://arxiv.org/html/2609.25185v1), Theorem A(1), gives spherical and pseudo-unitary existence. Theorem A(3)/4.4 classifies Morita duals under the additional hypotheses **unitary, cyclic, untwisted, Q-system type**. The subgroup duals have HI rules and rank `2N`; the `1+rho` dual has rank `N+1`, with dimensions `1,d,(d-1)^((N-1)/2),(d+1)^((N-1)/2)`. Section 4.3 supplies its generating fusion matrix. Theorem 6.3 constructs the specified near-group family with `N^2` invertibles and noninvertible multiplicity `N^2`. The module-category rank `2[G:H]` in (4.4) is **not** the rank of its dual fusion category.

These are primary preprint statements checked on 2026-10-21. We have not independently verified their entire analytic constructions or algebra classification. The computations below need only their displayed fusion rules to derive the family dimensions. In particular, the dimension obstruction applies without using their unitary classification theorem.

## Independent exact dimension obstruction

For the HI rules, let `d` be the positive solution of `d^2=N*d+1`. Directly summing squared simple dimensions gives

\[
D_N=N(1+d^2)=\frac{N^3+4N+N^2\sqrt{N^2+4}}2,
\qquad
p_N(x)=x^2-N(N^2+4)x+N^2(N^2+4).
\]

The specified near-group rules have noninvertible dimension `N*d` and total dimension `N*D_N`, whose minimal polynomial is

\[
q_N(x)=x^2-N^2(N^2+4)x+N^4(N^2+4).
\]

For each of the 277 tensors the verifier reconstructs the dual involution and the integer Casimir matrix `C=sum_i N_i N_(i*)`, and checks `N_(i*)=N_i^T`. The positive FP-dimension vector is an eigenvector of `C` with eigenvalue equal to the global FP dimension, so this is its spectral radius. Morita equivalence preserves that dimension. A proposed quadratic dimension therefore has to be a root of the exact characteristic polynomial of `C`.

The verifier divides that characteristic polynomial by each candidate `p_N` or `q_N`. It handles **all** odd `N>=3`, not a numerical truncation: `D_N>N^3`, `N*D_N>N^4`, while the source dimension is bounded above by the maximum row sum of `C`. Once the respective power exceeds that integer bound, every larger order is excluded as well. The largest explicitly tested HI order in this dataset is eleven.

There is one nonzero-eigenvalue coincidence requiring care: `R8_3_486` has `p_3` as a Casimir factor. Its diagonal entry 47 forces its spectral radius to be at least 47, whereas `D_3<39`. Thus this is a lower spectral value, not a model. Every other division is nonzero. All 277 tensors fail both family comparisons exactly.

The classified rank-eight Q-dual would have `N=7`, global dimension `(371+49*sqrt(53))/2`, and minimal polynomial `x^2-371*x+2597`. Its displayed generating matrix and positive dimension eigenvector are independently checked and stored in the receipt. None of the 277 source tensors has this global dimension.

## Replay and limitations

Run from the repository root:

```sh
python evidence/rank8_m3_20261021/models/fresh_202609/verify_odd_hi_dimension_filter.py
python -O evidence/rank8_m3_20261021/models/fresh_202609/verify_odd_hi_dimension_filter.py
```

Both are read-only and compare exact recomputation with `odd_hi_dimension_filter.json`; `--write` explicitly regenerates it. Each record binds its source tensor SHA-256 and contains both complete family comparisons, Casimir data, and the infinite-tail bound.

The result does not classify arbitrary extensions, other equivariantizations, de-equivariantizations, products, or categories with modified HI multiplicities. In particular, a rational multiple of a known global dimension is not itself excluded by this comparison. It is also not evidence that the remaining rings are realized or impossible. It records a completed search against these two newly available families and every Morita-equivalent category.

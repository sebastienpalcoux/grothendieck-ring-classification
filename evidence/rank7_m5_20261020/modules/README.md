# Exact general exclusion of R7_5_4982

The raw ring of dimension type `(1,1,1,3,12,12,12)` is excluded by a complete Morita descent. Every categorification would have a Morita dual with one of two rank-39 based rings. Each contains a rank-13 subring of type `(1^4,4^9)` with Klein-four invertibles. The Jordan–Larson classification in dimension `4p`, followed by the group-theoretical double-coset argument proved here, rules out that subcategory.

The complete categorical proof is `r4982_morita_descent.tex`. It makes no pivotal, spherical, braided, or unitary assumption. It also proves the reusable statement: for prime `p>3`, an integral category of type `(1^4,4^((p-1)/4))` must have cyclic order-four invertibles.

Replay from the original tensor:

```sh
python evidence/rank7_m5_20261020/modules/verify_r4982.py
```

Requirements: Python 3, SymPy, NumPy, NetworkX, and a C++17 compiler. The replay refreshes the evidence files in this directory and takes approximately 32 seconds in the research environment. It uses exact arithmetic; no optimizer or floating-point infeasibility decision appears in the proof. Every Python stage refuses to run with assertions disabled.

The stages are:

1. `verify_fourier.py`: raw fusion identities force a cubic Fourier sector; complete finite domains give 639 matrices satisfying two moments and eighteen satisfying three moments.
2. `r4982_module.py`: reconstruct all eighteen 13-simple module actions, verify all fusion equations, and record basis isomorphisms fixing the distinguished free module.
3. `prepare_rightactions.py` and `enumerate_rightactions.cpp`: construct the complete full-Gram rational affine spaces and enumerate three integer boxes, each of size 2,048,000. Each has exactly one admissible normalized noninvertible right action.
4. `fullgram_completion.py` and `normalization_check.py`: generate all 27 noninvertible actions, prove their multiplicities from the cross-Gram block, and enumerate the permutation centralizer of order 72.
5. `invertible_group_completion.py`: enumerate all 53 possible image subgroups of orders dividing twelve, allowing uniform kernel multiplicities. Exactly two full-Gram frames remain.
6. `dual_fusion_completion.py`: enumerate all coefficient vectors for each of the 729 noninvertible products. Every product is unique in both frames, even though the 39 action matrices have span of dimension 37.
7. `certify_rank13.py`: verify the two based rings, dimensions, duality, both Frobenius reciprocity identities, and associativity; extract the closed rank-13 subring and verify its four invertibles have exponent two.

The final machine-readable conclusion is `r4982_exclusion_certificate.json`. The largest intermediate record, `r4982_dual_fusion_options.json`, contains both complete rank-39 tensors and all their right-action matrices. The proof includes the precise exhaustive domains and their completeness arguments; retained action matrices alone are not claimed to construct categories.

Primary references:

- D. Jordan and E. Larson, *On the classification of certain fusion categories*, Theorem 1.1, https://arxiv.org/abs/0812.1603.
- S. Gelaki and D. Naidu, *Some properties of group-theoretical categories*, Theorem 5.1, https://arxiv.org/abs/0709.4326.

`probe_fullgram.py` is an exploratory diagnostic and is not used by the verifier. The files `.in` and `.out` are transparent integer input/output records for the bounded C++ enumeration. The executable itself is compiled into a temporary directory during replay and is not a repository artifact.

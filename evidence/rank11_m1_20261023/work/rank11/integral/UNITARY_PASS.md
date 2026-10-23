# Exact positivity audit of the two final noncommutative dimension-32 rings

Both physical source tensors R11_1_104 and R11_1_153 pass the full primary/Schur criterion family and every inequality of Lim's Corollary 3.4 on their simple bases. These are necessary-condition passes, not categorification or exclusion conclusions.

The dimensions are exactly four 1s and seven 2s, with global dimension 32. Were either tensor categorifiable, the two-prime dimension theorem of Etingof–Nikshych–Ostrik would make its category solvable, hence weakly group-theoretical, and the unitarity theorem of Galindo–Hong–Rowell would supply a unitary categorification. Thus a violation of the tested unitary criteria would be a general exclusion here. No violation occurs.

## Primary criteria and Schur positivity

For the input-oriented regular fusion matrices M_i, let

P = 2 Σ_i M_i⊗M_i⊗M_i / d_i.

All coefficients are integers. Direct exact integer computation proves P is symmetric and

P(P−8I)(P−16I)(P−64I)=0.

Consequently its real spectrum is nonnegative, proving the full primary-3 matrix positive semidefinite. The producer checks its maximum absolute row sum is 120, and bounds every intermediate product by 120·128·136·184 < 2^63 before using int64 arithmetic. The independent verifier at `../criteria_audit/verify_primary3_tensor_algebra.py` instead works in the tensor product based algebra with ordinary unbounded Python integers; it proves the same identity and exact multiplicities 0^1147, 8^84, 16^84, 64^16. It imports neither the producer nor numerical matrix packages.

Huang–Liu–Palcoux–Wu, arXiv:2210.00792v1, Theorem 3.9, equates full primary-3 positivity with all full primary-n inequalities. Proposition 3.13 implies the Schur product property. The implication applies to noncommutative fusion rings. Therefore the test exhausts that entire family; separate higher-n or irreducible-representation Schur searches cannot exclude these tensors.

Primary source: https://arxiv.org/html/2210.00792v1 .

## All exponents of Lim's inequalities

Put P_ij(k)=N_ij^k d_k/(d_i d_j). For each of the 1331 triples (i,j,k), the stored rational entries q(l,m,n) are nonnegative and satisfy exactly

Σ_n q(l,m,n) = P_ij(l) P_jk(m),
Σ_m q(l,m,n) = P_ij(l) P_lk(n),
Σ_l q(l,m,n) = P_jk(m) P_im(n).

The first identity makes l and m independent. Weighted Minkowski followed by conditional Jensen yields, for every real p≥1 and every nonnegative a,

[Σ_l P_ij(l)(Σ_n P_lk(n)a_n)^p]^(1/p)
≤ Σ_m P_jk(m)[Σ_n P_im(n)a_n^p]^(1/p).

This is the dimension-normalized form of Lim's Corollary 3.4. The p→∞ limit also follows. This coupling argument is proved in the project's existing `rank6_laptop_20261002/all_p_minkowski/PROOF.md` and works without commutativity.

`unitary_checks.py` used floating linear programming solely to discover sparse rational couplings, then verified them with exact fractions. `verify_unitary_couplings.py` independently reads the original compressed census and source hashes, verifies the positive FP dimension character, and replays all 483153 pairwise marginal equations per ring using only the Python standard library. It does not run optimization or import the producer. Both cases pass every triple.

Primary source for the inequality: J. Lim, *Noncommutative Minkowski integral inequality and a unitary categorification criterion for fusion rings*, arXiv:2601.13490v2, Corollary 3.4, https://arxiv.org/pdf/2601.13490 .

## Reproduction

- Producer: `OPENBLAS_NUM_THREADS=1 python work/rank11/integral/unitary_checks.py`
- Independent all-p replay: `python work/rank11/integral/verify_unitary_couplings.py`
- Independent primary replay: `python work/rank11/criteria_audit/verify_primary3_tensor_algebra.py`
- Certificates: `unitary_checks.json`, `../criteria_audit/primary3_independent.json`.

The conclusion is confined to the stated families on these original rings. It makes no assertion about every possible Morita-equivalent ring or additional commuting-square variant.

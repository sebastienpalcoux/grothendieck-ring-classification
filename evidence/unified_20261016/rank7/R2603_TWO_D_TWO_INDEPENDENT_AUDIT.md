# Independent audit of the R2603 two-moment exclusion

Status: PASS. I read the complete proof and every line of the portable source-bound verifier, and replayed it independently under optimized Python. The receipt is r2603_two_d_two_independent_optimized.json.

## Categorical and exact coverage checks

The general-complex bridge through the audited dihedral Morita dual with two FP dimensions is appropriate: Galois pseudo-unitarity of the Morita dual transfers through the intrinsic global-dimension equality. This argument does not assume the initial category already pivotal.

I checked the seven character homomorphisms, duality-aware codegrees and chosen Galois automorphism: Q(sqrt(-2)) is disjoint from Q(sqrt5), so the automorphism flipping the dimension field can fix every other character. The verifier checks the full transport identity against all seven characters on every basis vector, including the irrational codegree ratios. It therefore does not infer row transport from codegrees alone.

The same-relative-moment pairing is valid without conductor saturation: the center twist transforms by sigma squared, and sigma squared fixes K. Normalized relative trace to K is invariant under that automorphism. Row orbits have one or two elements, even when the actual permutation of central simples has longer cycles; summing its cycles pairs row multiplicities and their average moment pairs. The common seventeen-vertex convex hull consequently applies. Its all-root derivation is independent of any exponent prime restriction.

I checked the theoretical two-block reduction by full character reciprocity. Codegree-eight rows have noninvertible multiplicity sum2, leaving one pointed term and no X term. Codegree-four rows have noninvertible sum4 and at most one X; the unit-row total of two X terms forces one in each. The five pointed terms have the stated multiset. The displayed reciprocity equations then force the two blocks. The code independently enumerates all50 lower blocks and excludes48, so the analytic count has a second exhaustive check.

The arithmetic row domain uses the correct maximal order Z[(1+sqrt5)/2], including its parity condition. The Gram and exact positive-semidefinite rank-one tests, inherited from the audited standard-library helper, give exhaustive residual domains. Frobenius-Schur signs are rebuilt from the source and the unbraided pivotal odd-isotypic lemma.

I checked the 45-coordinate convention, denominator-clearing factor8, low-trace subtraction, and paired-orbit column sums against the induction formulas. Every genuine center gives a nonnegative real combination of these columns. The exact separator has nonnegative value on every allowed column and negative value on the target; the resulting contradiction is independent of a numerical optimizer.

## Fresh replay

The independent optimized replay reconstructs465 global rows,50 low blocks,48 reciprocity exclusions, and two surviving blocks with72/76 paired row types. Their1224/1292 columns have minimum separator dot product12 and target dot products−1336/−1240. The union contains1292 distinct columns. All checks pass with assertions disabled; the verifier uses explicit failure conditions.

## Audited file digests

- R2603_CENTER_MOMENT_PROOF.md: `eabcf813b586f393d38af3251c4a778d1b338b94e9d182a2eb8cb975a25dd879`
- verify_r2603_center_moments.py: `e8360da0b9215febd244db6071d8aaec6b95f4e7e75a7cdddae3e99349dbf507`
- r2603_center_moment_certificate.json: `a9c914a1e154bcdb271b0ff5e0e58ae49c8600a2269b982d4614c96d814818f5`

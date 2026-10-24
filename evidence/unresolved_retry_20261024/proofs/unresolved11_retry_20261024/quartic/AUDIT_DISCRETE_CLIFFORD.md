# Independent semantic audit of the discrete rank-nine restrictions

## Verdict and exact conclusion

The new restriction is valid, subject to the existing audited necessary-center construction and its published lower-rank dependencies:

- In the positive TY-sign branch of R9_2_137, every large simple has projected third indicator 1/2.
- In the negative TY-sign branch of R9_2_1976, every large simple has projected third indicator 1/2.

The projection is normalized relative trace to Q(sqrt(2)). Combined with the categorical local Clifford theorem, this means the unprojected third indicator belongs to {-zeta_3,-zeta_3²}; it does **not** mean that the unprojected indicator equals 1/2.

Both source rings remain unresolved. The surviving assignment has an exact nonnegative rational witness only for a necessary center relaxation, not a categorical model.

## Reconstruction of the new rows

I independently executed the construction prefix of `../rank9/screen_morita_third.py`, using the restored source tensors and the existing quadratic center/labelled-S builders. I reconstructed the two matrices without invoking the optimizers and compared every entry with the portable saved systems. Both comparisons passed:

| Source/sign | Rows | Columns | System SHA-256 |
|---|---:|---:|---|
| R9_2_137, + | 248 | 22231 | 4e233363c447d8c396951bf6190bfc5a47ba9ffda5a23455e9afb211230a661a |
| R9_2_1976, - | 188 | 21697 | b95c0b3647dca943d52bdcfb29cca3e3f58651bf8867f113db44fc295ea8cb2c |

The inherited rows are the existing induction Gram, formal-codegree, Galois, cyclic-rotation, moment, and labelled low-column S-symmetry constraints. The inherited integral-center restriction removes integral-dimensional central simples other than the permitted invertibles; it excludes the central lift of the distinguished free involution g. The surviving nonunit central invertible, if present, has fermionic twist and total multiplicity at most one. The TY-support filter and exact second/fourth moments are those of the already audited eighth-root-spectrum theorem.

For each large source object i, the new row is the sqrt(2) coefficient of

    sum_Z v_i(Z) dim(Z) Tr_K(theta_Z³) = D Tr_K(nu_3(i)),

with D=144+96 sqrt(2). A high-column term uses its joint third twist trace. A low labelled or anonymous term uses twist 1; this is the distinguished-induction twist theorem, not a free phase choice. Auxiliary rotation and slack variables contribute zero to this center sum.

The local Clifford theorem permits exactly -1 and 1/2 for the projected indicator. The four new rows all have positive denominator-clearing factor 4. In a prescribed discrete branch their right-hand sides are therefore 384 times the chosen indicator. Removing the four corresponding slack columns converts the four inequalities into exactly these four equations. The earlier rows had zero entries in these newly appended slack columns and are unchanged by their removal.

The aggregate third-indicator upper bound retained in the system introduces no additional categorical premise for these commutative sources: the four local bounds already imply their sum is at most 2, and the weighted total-indicator formula gives the aggregate center equation. In particular this part need not rely on the separate D8 pointed-cocycle argument.

## Exact separating vectors

I replayed all 25 stored direct separating vectors with exact integer arithmetic. For every excluded assignment, the right-hand side is changed only in the last four rows, using the same positive scales. Every vector satisfies

    A^T y >= 0,       b^T y < 0.

All recorded minima of A^T y are zero. The strict negative b^T y values agree with `../rank9/discrete_branch_restrictions_receipt.json`. There are 13 direct exclusions for R137 with positive TY sign and 12 for R1976 with negative TY sign. No numerical optimizer status is used as an exclusion.

## Completion by based relabelling

The two and three remaining excluded assignments, respectively, are transported by full based-ring automorphisms. I independently checked all 729 tensor coefficients for each of the five transport permutations, together with preservation of the unit and the distinguished source labels:

| Source | Distinguished g | TY object Y |
|---|---:|---:|
| R9_2_137 | 1 | 8 |
| R9_2_1976 | 8 | 5 |

Every transport fixes both g and Y. It also preserves the full large-object set, the duality, FP dimensions, and the integral subring. Fixing Y preserves its TY sign/second indicator, and fixing g preserves the special central-column exclusion. The complete character list and all inherited constraints remain necessary after relabelling. The transport rule is

    new_assignment[p(i)] = old_assignment[i].

This is the direction implemented in the verifier and it maps each listed missing assignment to an assignment with a direct exact separating vector.

No realization of p by a tensor autoequivalence is needed: any hypothetical categorification can have its simples relabelled by a based-ring automorphism, producing a categorification of the same labelled tensor and the transported assignment. A contradiction for the latter therefore excludes the former. This distinction is essential.

All sixteen assignments in {-1,1/2}^4 are covered. The sole assignment not excluded is (1/2,1/2,1/2,1/2). Its saved nonnegative rational vector satisfies every matrix equation exactly. This proves the conditional indicator restriction and does not prove existence.

## Replay and limits

The standard-library replays `verify_discrete_branch_restrictions.py` and `verify_discrete_witnesses.py` both passed. The latter also checks the saved witnesses for R137 with negative TY sign and R1607 with negative TY sign, but no uniqueness conclusion is drawn for those branches.

This audit checks the semantic meaning of the newly added rows, exact reconstruction of the two saved systems, the new categorical Clifford premise, the exact rays, and the relabelling completion. It inherits the earlier audited center-system theorems and lower-rank exclusions; it does not claim a fresh full proof/replay of every inherited classification dependency.

# Independent audit of the quadratic neutral-block obstruction

**Verdict: APPROVED for R9_2_500 and R9_2_1235 in general scope**, using their independently replayed signed Galois-pseudo-unitary gates. The reduction in `../quadratic_theory/NEUTRAL_BLOCK_THEOREM.md` is a sound necessary relaxation, and both exact separating rays pass independent replay. The known model R9_2_515 has an independently recovered and exactly verified feasible rational solution of the same construction.

## Why the quadratic subsystem is legitimate

Let `B=V V^T` be the ambient induction Gram matrix, whose columns are the nonnegative restriction multiplicity vectors of simple objects of the center. The exact zero entries `B_ij=0` for `i in S`, `j outside S` imply `v_i v_j=0` for each individual column. Every column is therefore supported wholly in S or wholly outside S. This follows from nonnegativity, without a presumed grading or presumed central-object classification.

The source tensor checks that S contains the unit, is dual closed, and is closed under products. A discarded column consequently contributes zero to every retained Gram equation, every induced twist trace for a simple in S, and every induced twist trace for its tensor powers. In particular, it contributes zero even before any number-field trace is taken. Setting its missing dimensions to zero in the implementation is only a placeholder: no surviving equation uses those placeholders.

Every column occurring in `I(1)` is retained, since its unit multiplicity is one. Thus its **ambient** formal-codegree dimensions and multiplicities must all be imposed. The ambient global dimension likewise remains in the indicator formula; substituting the dimension of the rank-six subcategory would be incorrect. The code correctly retains the ambient quantities.

All retained object dimensions and all low-column dimensions lie in `K=Q(sqrt(2))`, as checked by exact membership tests inside the quartic character field. Taking normalized field traces over a cyclotomic extension fixing K therefore preserves all coefficients in the retained equations. No claim that the Galois action preserves the retained central objects is used. Omitting Galois partner constraints and all discarded equations enlarges the feasible region and is conservative.

The entrywise Gram inequalities and `v^T B^-1 v<=1` use the ambient matrix. Because it is block diagonal, the latter is also exactly the corresponding condition for the principal neutral block. It gives a finite exhaustive search. The arithmetic filters `D/z` integral and z a d-number apply to any central simple, irrespective of which support block it occupies.

## Twist traces: direct independent check

Here `D=32+16sqrt(2)` has norm 512. The Cauchy theorem for spherical categories implies that every center twist has order a power of two. The theorem concerns prime ideals; taking norms from a cyclotomic extension introduces no new rational primes. Thus the quartic ambient dimension field does not enlarge the allowed prime support.

The possible joint normalized traces `(t_1,t_2,t_3)` over `Q(sqrt(2))` can be listed directly:

| Order | Joint traces |
|---|---|
| 1 | `(1,1,1)` |
| 2 | `(-1,1,-1)` |
| 4 | `(0,-1,0)` |
| 8 | `(sqrt(2)/2,0,-sqrt(2)/2)` and its negative |
| 16 | `(0,sqrt(2)/2,0)` and its negative |
| at least 32 | `(0,0,0)` |

For orders at least 32, raising to a power at most three leaves at least a primitive sixteenth root; its trace down to the conductor-eight quadratic field is zero. This verifies the finite list independently of the general quadratic Gauss-sum implementation. `audit_neutral.py` checks that the implementation returns exactly these eight packets.

The order-three rotation trace over K is either 1 or `-1/2` for each one-dimensional eigenspace. These two normalized character packets are also checked directly. The only third-order rows with nonzero coefficients in the stored rays belong to the nontrivial invertible object g (index 1 for R500, index 6 for R1235). Since `g^2=1` and `g!=1`, the space `Hom(1,g^3)` is zero, so these rows simply impose `nu_3(g)=0`.

The first and second indicator rows retain their usual necessary values. The second-indicator sign is fixed only by the project's existing odd-multiplicity lemma, and otherwise relaxed to the interval `[-1,1]`. The relaxation is correct: writing the sign as `2u-1` with `0<=u<=1` gives exactly the displayed moment equation and its nonnegative bound slack. Nonselfdual objects use indicator zero.

## Modular integrality does not affect these two certificates

The ambient modular-character filter uses the correct operator `(D/z) B^-1 N_v`; retaining the ambient rank-nine matrices is essential to its S-ratio interpretation. More decisively for this audit, it rejects **none** of the 102 columns surviving the basic arithmetic filters in either ring. The independent verifier enumerates and applies the basic arithmetic filters without calling the modular filter, then proves that its complete resulting set equals the implementation's final set. Thus these two exclusions remain valid if the modular filter is removed entirely.

## Independent exact checks

The audit script recomputes B directly by contraction of the original fusion tensor, independently enumerates the neutral integer box, recomputes low-dimension counts from the exact factorization of the ambient Gram characteristic polynomial, checks block separation and closure, applies the dimension-integrality and d-number filters, rebuilds the integer equation system, and verifies the stored Farkas inequalities with exact integers. It invokes no optimizer.

Both rings give:

- 5,600 vectors in the neutral bounding box;
- 432 nonzero vectors passing the Gram inequalities;
- 102 columns passing the arithmetic conditions;
- 63 equations and 667 nonnegative variables;
- `minimum(A^T y)=0` and `b^T y=-896`.

The independently reconstructed system hashes agree with the author's replay. The signed-gate verification records are checked as dependencies and give general scope for both exclusions.

For the modeled control R9_2_515, a numerical feasible support was recovered independently, then its 50 coordinates were solved by rational row reduction. The resulting nonnegative rational vector satisfies all 61 equations exactly, with 2,207 total variables. It is stored in `neutral_515_primal.json` and rechecked from scratch by `audit_neutral.py`. Feasibility is therefore not inferred from a floating-point solver status.

## Artifacts and references

Run `python phase2/signed/audit_neutral.py`. Its output is `neutral_audit.json`; the separate exact control witness is `neutral_515_primal.json`.

The inherited center-induction and indicator results are documented in `../quadratic_theory/THEOREM.md`. The extension reviewed here uses no additional categorical assumption. Primary references checked for the field and ambient-center issues are:

- Bruillard–Ng–Rowell–Wang, [Rank-finiteness for modular categories](https://arxiv.org/abs/1310.7050), Theorem 3.9, including its general spherical-category formulation and passage to the Drinfeld center.
- Deshpande, [On centers of bimodule categories and induction-restriction functors](https://arxiv.org/abs/1611.04486), Section 2.7, especially Corollary 2.18 and equation (39). As noted above, the two accepted rays do not require any additional pruning by this formula.

The result is a single block-restriction principle followed by the same exact contradiction for both rings, rather than separate unexplained numerical failures.

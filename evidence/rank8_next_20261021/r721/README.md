# R8_3_721: twist rigidity and an explicit necessary center completion

**R8_3_721 is now unitarily realized.** The actual inherited-Q-system construction is proved in `../models/R721_QSYSTEM_CONSTRUCTION.md` and presented in `r721_qsystem_model.tex`. Its identification uses the exact multiplicity bound and the exhaustive cumulative census crosswalk recorded here.

The center calculations below record the preceding necessary-condition stage. They remove the rank-16 center pattern, remove two of the three rank-22 low-action types, and force the surviving center twists. They construct and check one complete rank-22 modular datum and its nonnegative integral Verlinde based ring, together with a based-ring restriction homomorphism to R8_3_721. These matrices alone are not an associator, a braided category, or a categorification; existence comes from the separate Q-system argument.

The tensor identity is `76e26a815651476dfda5c2aa654f0d1327bdc890e08086cb6dbfe39ef9a1cdc5`. Inputs are read-only files from `rank8_frontier_20261021` and `rank8_center_followup_20261021`. The previously proved pseudo-unitary Galois-conjugate reduction permits necessary pseudo-unitary center conditions to be applied to general complex categorifications. No source ledger is changed here.

## Reproduction

From the repository root:

```sh
python evidence/rank8_next_20261021/r721/twist_balancing.py
python evidence/rank8_next_20261021/r721/c_block_refinement.py
python evidence/rank8_next_20261021/r721/modular_completion.py
```

The corresponding JSON receipts are checked-in outputs. `modular_completions.json` contains the complete normalized S matrix over Q(zeta_17), T exponents modulo 136, the 22×22×22 fusion tensor, and all restriction columns. To regenerate that data explicitly, append `--output PATH` to the last command. All arithmetic is exact. Assertions use explicit exceptions and remain active under Python `-O`.

## Labels and conventions

Put r=sqrt(17), D=136+32r, s=17+4r, t=34+8r, and h=32+8r. D is the global dimension of the source category and the positive square root of the center's global dimension. We write S for the **normalized** center matrix, so S[0,Z]=dim(Z)/D. The canonical center anomaly is 1 and

    S T S = T^(-1) S T^(-1),     S^2 = charge conjugation.

The distinguished simples are labels 0,...,4, with dimensions 1, 33+8r, t, t, s, and twists 1. The remaining rank-22 labels are:

| Labels | Frozen restriction type | Dimension | Short name |
|---|---:|---:|---|
| 5,6,7,8 | 0 | s | A |
| 9 | 3 | s | B |
| 10,11,12,13 | 4 | t | C |
| 14,...,21 | 5 | h | H |

The surviving distinguished-character assignment is `[0,1,3,2,4]`. Both A and C perfect matchings may be chosen as `(0,1),(2,3)` within their four-element groups. Relabeling inside the groups accounts for the nine labelled representatives.

## 1. Ordinary twist sums, not averaged traces

For an irreducible source character chi_E of dimension m_E and formal codegree f_E, the unnormalized distinguished row is

    (D/(f_E m_E)) chi_E(F(Z)).

Because all distinguished twists are 1, their STS entries give

    sum_Z chi_E(F(Z)) chi_F(F(Z)) theta_Z
       = f_F m_F chi_E(F(A_F)).

Here the unknown for a high restriction type is the **ordinary sum** of its actual roots of unity theta_Z. The exact four-column system has rank four. In the swapped rank-16 pattern it forces the twist of its singleton type-8 simple to be zero, which is impossible. The identity assignment was already excluded; the same subsystem forces its singleton type-3 twist to be -7. The rank-19 patterns were excluded in the previous action-extension certificate.

For rank 22, the forced sums are

    sum_A theta = -4,     theta_B = 1,
    sum_C theta = 0,      sum_H theta = -(1+r)/2.

Equality in the unit-circle triangle inequality implies every A twist is -1.

## 2. Individual balancing and the C quartet

For each selfdual distinguished simple i, balancing reads

    sum_k N[i,j,k] dim(k) theta_k = theta_j (D S[i,j]).

Applying this to all 46 previously classified rank-22 action tuples forces every unmatched C vertex to have twist zero. Thus matching sizes zero and one are impossible; precisely the nine labelled perfect-matching tuples remain. Each matched C pair has opposite twists, so the C twists are `(z,-z,w,-w)`.

The second-indicator induction formula is

    D nu_2(X) = sum_Z dim(Z) [F(Z):X] theta_Z^2.

The source duality is `[0,2,1,3,4,5,6,7]`. All 32 possible choices of signs for the five nonunit selfdual source simples are checked. There is exactly one solution:

    (nu_2(X_0),...,nu_2(X_7)) = (1,0,0,1,1,1,1,1),
    sum_C theta^2 = 0,     sum_H theta^2 = -(1+r)/2.

Consequently w^2=-z^2, and up to exchanging labels the C twists are `(z,-z,iz,-iz)`. They are distinct. Duality preserves both twist and restriction type, so each C simple is selfdual.

## 3. A short modular-relation refinement forces primitive eighth roots

Let W be the nine-dimensional cyclic space from the frozen action certificate. It is the space of vectors constant on each high restriction group, with arbitrary distinguished coordinates. The four low action matrices determine S on W: each high-group column has a unique W-projection with its prescribed simultaneous eigenvalues and positive vacuum coordinate. `modular_completion.prepare()` solves these exact nine-dimensional systems.

Let Q_A and Q_C be the two-dimensional spaces spanned by differences within the matched A and C pairs. Let a and c be the unit pair-contrast vectors `(1,1,-1,-1)/2` in A and C respectively. From the simultaneous low eigenspaces and symmetry of S:

* Q_A and Q_C are separately S-invariant;
* S exchanges the lines spanned by a and c;
* the remaining hidden subspace lies wholly in H.

On Q_A, T=-I; the relation STS=T^-1 S T^-1 forces S=-I. The a/c exchange has coefficient ±1 because the C simples are selfdual and S^2 acts as identity there. Exchanging the two A pairs changes this sign, so either is equivalent; the verifier checks both.

Write the normalized S block on the orthonormal matched C differences as `[[x,y],[y,zeta]]`. For an arbitrary nonzero omega, insert the C twists `(omega,-omega,i*omega,-i*omega)`. The unit–C and A–C STS entries, using only the already forced H twist sum, uniquely give

    x = zeta = 0,     y = -i/omega^2.

This identity is checked symbolically for both cross signs, without a Galois or conductor assumption. Since Q_C is S-invariant and each C object is selfdual, S^2=I on Q_C. Hence `-omega^(-4)=1`. Therefore the four C twists are exactly the primitive eighth roots. The putative fourth-root quartet is excluded.

## 4. The eight H twists

The Cauchy theorem for spherical fusion categories implies that all prime divisors of the twist order divide the algebraic norm of D. Here Norm(D)=1088=2^6·17, so only 2 and 17 occur. This use is of the theorem for general spherical categories, not an integral-dimension variant.

The normalized H dimensions are `h/D=1/sqrt(17)`. Galois symmetry therefore preserves the eight H labels (up to the Galois signs in S). For a twist of order n, the square-unit orbit under theta -> theta^(k^2) must fit into those eight labels. If 17^b divides n, this forces b=1; if n=2^a·17, it forces a<=3, because the square orbit has size `8·2^max(a-3,0)`.

At least one H twist has a 17 component: otherwise their sum would belong to a 2-power cyclotomic field, which cannot contain sqrt(17). Its eight-element square orbit exhausts H. Thus the H twists have the form eta times one quadratic-residue or quadratic-nonresidue orbit of primitive seventeenth roots, with eta^8=1. The forced real sum `-(1+r)/2`, together with the two quadratic Gauss periods `(-1±r)/2`, forces eta=1 and the nonresidue orbit. We may therefore label

    theta_(H_l) = zeta_17^(3 l^2),       l=1,...,8.

All are distinct, so all H objects are selfdual. The A rows are real by the preceding block decomposition, so A is also selfdual. Thus the complete surviving center duality is trivial.

For these uses of Galois symmetry, S is normalized and the center is anomaly-free: `sigma^2(T_Z)=T_(hat_sigma(Z))`. On the H dimension column, the accompanying S sign is the Legendre symbol modulo 17.

## 5. Complete S, T and a based ring

The 2-power Galois automorphisms fix all H labels and their S-row signs. Hence the H×H block lies in Q(zeta_17). Its reality and Galois symmetry reduce it to

    S_(H_l,H_m) = (lm|17) sigma_(lm)(b)

for one element b of the eight-dimensional real subfield. The unit–H STS entries form a rational linear system of rank eight. Its unique solution is

    b = -(zeta_17^6 + zeta_17^(-6))/sqrt(17),
    S_(H_l,H_m) = -2 cos(12 pi l m/17)/sqrt(17).

Together with the forced W, A, C blocks, this gives the complete candidate. Its twist order is 136. The exact verifier checks:

* symmetry of S and all 484 entries of S^2=I;
* all 484 entries of STS=T^-1 S T^-1, in Q(zeta_17)[u]/(u^4+1);
* all 2024 unordered Verlinde triples, which are nonnegative integers with maximum coefficient 5;
* the tensor unit, trivial duality and all four prescribed distinguished actions;
* all 3872 source coordinates of the 484 forgetful multiplication identities.

Associativity follows exactly from the verified orthogonal Verlinde diagonalization. Consequently the file contains an actual commutative **based ring** with modular data and a based-ring homomorphism to the source ring. A lift to a modular tensor category, and then a compatible connected étale/Lagrangian algebra realizing the source, is not supplied. Matching known potential modular data also would not by itself supply either lift.

## References and scope

* S.-H. Ng and P. Schauenburg, *Frobenius–Schur indicators and exponents of spherical categories*, Adv. Math. 211 (2007), 34–71, https://arxiv.org/abs/math/0601012 — induction formula and twist exponent.
* P. Bruillard, S.-H. Ng, E. C. Rowell and Z. Wang, *Rank-finiteness for modular categories*, J. Amer. Math. Soc. 29 (2016), 857–881, https://arxiv.org/abs/1310.7050 — Galois symmetry and Theorem 3.9 (Cauchy).
* The distinguished-character formula, pseudo-unitary gate, complete Gram domain, and complete low-action classification are the frozen repository inputs cited above, not new assumptions.

The scripts ending `_probe.py` are exploratory calculations. In particular, an intermediate fourth-root construction passed orthogonality and Verlinde integrality but **failed STS**; it is not part of `modular_completions.json`. Only the three named verifiers and their receipts support the conclusions above.

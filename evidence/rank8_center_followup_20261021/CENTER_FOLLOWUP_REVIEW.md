# Independent review of the center-product follow-up

The follow-up yields necessary-pattern exclusions and necessary fusion-action data. It does not exclude either source ring, construct a complete center fusion ring, or produce a categorification. The frozen main 25-exclusion/9-open frontier is unaffected.

## Categorical scope and normalization

The previously verified unrestricted sphericalization and Galois-pseudo-unitarity gates apply to R8_3_721 and R8_3_1154. Any complex categorification therefore supplies a pseudo-unitary Galois conjugate with the same based tensor. Its center is modular, with dimension D² when D is the source category's dimension.

The full distinguished character row is

S(A_E,Z) = D chi_E(FZ)/(f_E dim(E)).

The two-dimensional source-algebra block contributes one distinguished central simple; dim(E)=2 is in this denominator, not a repeated simple in the spectral sums. This is the ordinary full-character normalization (Deshpande, arXiv:1611.04486, Lemma 4.3 and the associated center-character formulas).

Both inputs explicitly have chi_E(x*)=chi_E(x) for every full trace character and every source basis element. Thus S(A_E*,Z)=S(A_E,Z*)=S(A_E,Z), and nondegeneracy proves A_E*=A_E. This checks precisely the self-duality needed here. The individual high simples need not be self-dual.

For four self-dual low objects, ordinary Verlinde and S²=D²C give

sum_Y N(i,j;Y) N(k,l;Y) = D^(-2) sum_Z S(i,Z)S(j,Z)S(k,Z)S(l,Z)/d_Z².

This is a bilinear integer multiplicity pairing, with an ordinary transpose. It does not assume a C* structure or replace a complex Hermitian pairing without justification. Without the checked self-duality, the last two labels would require duals. Frobenius reciprocity also makes each low fusion matrix real symmetric, even when the category is not known to admit a C* structure. Ordinary Verlinde is the regular-module specialization of Deshpande, arXiv:1811.08447, Theorem 1.1.

The first independent reviewer derives the S3 characters from permutations and checks all 27 electric cubics and 81 fourth moments of Z(Vec(S3)). The extension reviewer adds an actual S3 cyclic-action control, using the electric actions on the identity-, transposition-, and three-cycle-flux centralizer blocks.

## R8_3_721: cyclic extension and its complete residual domain

The original independent quartic reviewer exhausts the 240-point integer restriction-Gram box, recovers all four multiplicity patterns and both character assignments, and independently proves uniqueness of the ten low-pair high-output columns in each case. It uses a Moore–Penrose solution and exhausts all coordinate choices, rather than the producer's row-wise minimum shortcut.

The extension reviewer starts from that independent receipt. It reconstructs the full low characters, all individual spectral columns, and all third- through fifth-order moments without importing any follow-up producer functions. Its cyclic computation uses all 15 redundant word columns and their Moore–Penrose inverse, rather than the producer's selected nine-column basis.

There are exactly nine distinct simultaneous eigenvalue tuples. The vacuum weight of a tuple is the sum d_Z²/D² over its constituent spectral labels, and is positive. This follows algebraically from the (0,0) entry of each Verlinde primitive idempotent, using S⁻¹=D⁻²SC; it does not require analytic unitarity of S. The grouped idempotents are the orthogonal spectral projectors of the real symmetric low fusion matrices. Since polynomials separate the finite tuple set, the vacuum cyclic subspace has dimension exactly nine. The already known rank-nine word space is consequently invariant and complete. This rules out a missing cyclic direction when the fifth moments determine the compressed actions.

Each spectral tuple contributes one cyclic direction; the hidden multiplicity is its total multiplicity minus one. This independently gives hidden ranks m_A−1, m_C−1, and 7, with eigenvalue tuples (1,−2,−2,1), (1,0,0,−1), and (−1,0,0,0). The formulas for N1,...,N4 in terms of the three orthogonal hidden projectors follow directly. No canonical-projector ansatz has been substituted for the full residual domain.

Both center-rank-19 patterns are impossible: one forces an N2 block equal to (9/2)J4, and the other forces an N1+N2 block equal to (5/2)J4−I4. These contradictions hold under both character assignments.

For center rank 16, the hidden spectrum forces a unique tuple of four low actions. For center rank 22, the producer's complete projector argument is valid:

* Every hidden projector is an orthogonal subprojector of Q, giving diagonal upper bound 3/4 on each four-element block.
* Integrality forces quarter residues; the identity P_ii=sum_j P_ij² saturates each row, eliminating cross-block entries.
* Nonnegative integrality of N2 forces matching projectors on the A block.
* Integrality of N4 forces P_A+P_C to be the complete canonical A/C difference projector, with no D component.
* The complementary C block is another matching projector. The rank-three condition forces equal matching sizes.

This gives exactly 1+6²+3²=46 labelled tuples, and three types under independent permutations within the two four-element groups. The independent replay reconstructs all 46 tuples, compares the full matrices with the producer receipt, and checks unit/low product columns, symmetry, nonnegative integrality, forgetful intertwining, pairwise commutation, and every joint second spectral trace. The two surviving Gram patterns still lack arbitrary high-high products and categorical coherence.

## R8_3_1154: independent norm and coordinate propagation

The second reviewer rebuilds all third- and fourth-moment coefficient rows directly from the full characters. It refilters all 14,211 saved integral Gram patterns to recover the exact 1,238 cubic-survivor domain, checks every complete restriction Gram, and independently obtains the four residual groups. It uses Q.pinv(), then enumerates every integer in each coordinate interval to obtain the minimum squared correction.

| Residual norm alpha | Patterns | First-stage exclusions | First-stage survivors |
|---|---:|---:|---:|
| 92/205 | 8 | 8 | 0 |
| 262/205 | 864 | 852 | 12 |
| 672/205 | 300 | 32 | 268 |
| 1082/205 | 66 | 0 | 66 |

In all groups, G−X0^t X0=alpha h^t h, with h=(1,0,1,−1,0,0,0,1,−1,1). Hence every real solution is X=X0+t h, with Mt=0 and sum t_i²=alpha. The exact integer/nonnegative coordinate domain is t_i=n−X0[i,0] with a bounded integer n. An empty active domain, or a sum of coordinate minimum squares above alpha, excludes the pattern. This gives exactly 892 exclusions and 346 survivors.

The independent propagation then expands every individual high simple, rather than using the producer's type-compressed implementation. It iterates exact norm lower/upper bounds and coordinate intervals for Mt=0. A candidate value is removed only when fixing that one individual coordinate violates a necessary norm or linear interval bound. Removing such a value from all interchangeable copies is valid; no fractional or numerical infeasibility is used. The independently expanded implementation gives the same additional 54 exclusions and 292 survivors.

The old height-six excluded indices are 207, 208, 376, 377, 898, 899, 1407, and 1408. All eight lie in the first 892. The combined exclusion union is therefore 946, comprising 938 additional exclusions beyond the old height-six stage. The exact common index domain and the frozen height-six tensor/domain hashes are checked. This reconciliation reuses the previously verified height-six certificate; it does not claim to independently rerun its full linear operator.

The 292 remaining patterns have merely survived these necessary bounds. No coupled integer solution or exact feasibility witness is asserted for them.

## Independent replay files

All scripts accept `--root /path/to/grothendieck-ring-classification`, default to read-only receipt comparison, emit a concise JSON PASS report, and retain checks under Python optimization. The `--write` option generates only the sibling review receipt.

* `quartic_center_independent_review.py` and `.json`: independent quartic reconstruction, eight-case uniqueness, and S3 third/fourth moments.
* `r721_extension_independent_review.py` and `.json`: independent cyclic/hidden reconstruction, complete action tuple comparison, and S3 fifth-moment control.
* `r1154_quartic_independent_review.py` and `.json`: complete source moment reconstruction, independent minimum-norm solution, complete coordinate interval enumeration, individual-copy propagation, and old-certificate index reconciliation.

These review artifacts are separate from, and do not modify, the frozen main evidence.

# Rank nine, exact multiplicity two: theoretical continuation

This research pass continues the 81 unresolved rings from the established-methods campaign. The input census contains 2,083 rings of exact multiplicity two; the 142 multiplicity-one input records retain their earlier classification. Ring identifiers below use the prefix `R9_2_`.

| Scope | Excluded | Unitary models | Unresolved |
|---|---:|---:|---:|
| Before this continuation | 1,995 | 7 | 81 |
| New results on the 81 | 36 | 14 | 31 |
| Cumulative exact-M2 census | 2,031 | 21 | 31 |

The accepted exclusions concern arbitrary fusion categories over the complex numbers. Every model counted has a categorical unitary construction and an exact based-ring identification. A feasible necessary system, a failed constructor search, a solver limit, a partial-branch exclusion, and a general-to-pseudo-unitary reduction do not settle a ring. GitHub repositories and the public website have not been changed in this pass.

## Unified criteria

The signed sphericalization argument imposes nonvanishing products of simple basis elements before enumerating signed associative tables. Multiplicity-two traces retain their entire domain {-2,0,2}. This closes nine general exclusions. A related signed global-dimension argument supplies twenty additional Galois-pseudo-unitarity gates. Together with the prior gates, every ring surviving those nine exclusions can be tested in pseudo-unitary scope after a justified Galois conjugation. See [the theorem](signed/THEOREM.md), the complete branch certificates, and the independent bit-vector replay receipts.

The joint-center criterion treats all possible simple restriction columns simultaneously. It combines the induction Gram identity, the dimensions and counts of simple summands in I(1), modular divisibility, finite joint relative-trace packets covering all allowed twist orders, and indicator/rotation constraints. It avoids enumerating complete low-column frames first. A new modular-integrality refinement tests characteristic polynomials of (D/z) B^{-1} N_v, using central Verlinde characters. Exact integer Farkas vectors certify every accepted infeasible linear system; numerical optimization only proposes a certificate. See [the integral theorem](integral_theory/joint_center_theorem.md) and [the quadratic theorem](quadratic_theory/THEOREM.md).

The structural exclusions use solvability and preserved central subcategories to force successive equivariantizations. For ring 907 the resulting S3 action on a cyclic prime group is impossible. For 1071 and 1724, the forced rank-two module over Rep(C13 semidirect C4) has a dual of rank sixteen, whereas a grading component would require rank seven. See [prime descent](integral_theory/prime_descent.md), [the rank-two-module argument](weak_integral/frobenius52.md), and their [independent audit](signed/audit.md).

| Criterion | Newly excluded identifiers |
|---|---|
| signed nonzero products | 686, 690, 726, 728, 736, 1187, 1241, 1377, 1424 |
| joint integral center | 301, 352, 366, 385, 725, 727, 1028, 1134, 1238, 1448, 1465, 1501, 1712, 1778, 1989 |
| prime descent | 907 |
| solvable rank two module | 1071, 1724 |
| joint quadratic center | 1569, 1886 |
| folded fermionic so3 | 920 |
| solvable central invertibles | 1356, 1933 |
| quadratic neutral block | 500, 1235 |
| larger fixed block morita | 396, 1265 |

A quadratic neutral-block relaxation excludes 500 and 1235 even though their full FP-dimension fields are quartic. Zero cross-block induction-Gram entries force every central restriction column into a single block. Keeping only the quadratic neutral block retains necessary Gram, I(1), and tensor-power trace equations, while using the ambient global dimension and codegrees. This reduces the problem to exact quadratic trace packets. Independent enumeration, integer separators, and an exact feasible witness for the known model 515 validate the implementation. See [the theorem](quadratic_theory/NEUTRAL_BLOCK_THEOREM.md) and [the audit](signed/neutral_audit.md).

A short solvability criterion excludes 1356 and 1933. A nontrivial solvable fusion category with trivial universal grading must end in a prime-order equivariantization, and therefore has a central subgroup of invertibles of prime order. Here the entire invertible group is C3, but it is noncentral in each input table. The FP dimension 96 invokes the two-prime solvability theorem. The same descent gives a structural reduction for the commutative dimension-96 family; see [the theorem and exact checks](integral_theory/dimension96_reduction.md).

The split-involution module/Morita criterion excludes 396 and 1265 after removing the former implementation restriction to at most two fixed simples. Each has three fixed simples and eighteen complete anti-module branches. Every branch fails an exact rank or partial/full Gram condition. An independent bit-vector encoding reproduces all eighteen classes, and optimizer-free replay checks the separating rays. Only FP dimensions enter, so no pivotality or pseudo-unitarity assumption is required. See [the proof](weak_integral/morita48.md).

A new theoretical family obstruction excludes pseudo-unitary categorifications of the rank-n folded rings PSU(2)_(4n−2)/(f=1), for n≥3. Local four-point trivalent relations yield a functor from the full even Temperley–Lieb category. Explicit zero-dimensional negligible idempotent objects map to zero in a pseudo-unitary target, so the functor descends to PSU(2)_(4n−2). The forced induced central algebra 1⊕f cannot be commutative: the universal grading is trivial, so f has a unique central lift, and that lift is fermionic. The independent signed gate upgrades the rank-nine instance 920 to general scope. The proof does not assume that the hypothetical category is generated by trivalent morphisms, and it does not identify pseudo-unitarity with a C*-structure. See [the full proof](quadratic_theory/R920_PROOF.md) and [the independent audit](signed/R920_audit.md).

## Models

The following table lists categorical constructions, rather than ring-level guesses. Exact constructors and source-to-model basis permutations are supplied in the model records. All 729 structure constants are compared for every identification. The independent replay also checks the based-ring axioms.

| Identifier | Unitary model |
|---|---|
| 21 | Parity-twisted V4 equivariantization of TY(C5) |
| 389 | Inversion orbifold of cyclic generalized Moore-Read category, dimension16 |
| 515 | Diagonal-fermion quotient (Ising box PSU(2)_10)_{1+psi box V10} |
| 748 | TY(C3)^S3 by inversion, parity coherence 0 |
| 812 | Rep(V4 semidirect Dih(C9)) |
| 813 | Rep(V4 semidirect Dih(C3 x C3)) |
| 1211 | TY(C3)^S3 by inversion, parity coherence 1 |
| 1372 | Asaeda-Haagerup category AH3 |
| 1373 | (Fib box Fib)^S3, sign quotient acts by swapping factors |
| 1396 | Pulled-back LPR-24 action along Dih(C9)->S3 |
| 1397 | Pulled-back LPR-24 action along Dih(C3 x C3)->S3 |
| 1857 | Spin(8)_2 WZW category equivariantized by order-three Dynkin triality |
| 1983 | Ordinary-swap equivariantization of the equal half-E6 diagonal-fermion product |
| 2029 | Triality equivariantization of the Tannakian-zested Spin(8)_2 category |

The ordinary-swap construction for 1983 requires care with central structures and balancing signs: it is not inferred from an involution of a fusion table. Its [construction](models/ordinary_swap.md) and [independent audit](signed/ordinary_swap_audit.md) explain the resulting order-four invertible lift. The parity modifications in the Tambara–Yamagami constructions are coherent weak group actions and are recorded explicitly.

For 1396 and 1397, the known unitary rank-five LPR-24 category supplies an actual S3 action after successive central descents. Pulling that action back along Dih(C9)→S3 and Dih(C3×C3)→S3 gives the two new models. Solvability forces the descents; uniqueness of central lifts makes the intermediate central subcategory invariant. The argument includes all coherence data and yields group-theoretical, unitarizable categories. See [the construction](group_models/PULLBACK_MODELS.md) and [the independent existence audit](integral_theory/pullback_model_audit.md).

For 389, an explicit inversion action on a cyclic generalized Moore–Read category is obtained from a closed tensorator formula on Vec(C16,ω2). A preserved central boson descends equivariantly and has a free condensation quotient. Cocycle, tensorator, centrality and equivariance identities are replayed exactly, separately from the final fusion-table comparison. See [the construction](weak_integral/mr_orbifold.md) and [the independent audit](models/additional_model_audit.md).

The model for 1857 is the C3-equivariantization of the standard unitary Spin(8)_2 WZW category by Dynkin triality. The actual Hopf-algebra automorphism supplies the coherent action. The rank-eleven seed tensor is computed by exact Weyl alternants and Verlinde coefficients in Q(ζ32), with no numerical reconstruction. The fixed nonunit object squares to the four invertibles, so its equivariant pairing can be normalized and all required Hom-space traces are determined. See [the construction](models/d4_triality.md).

For 2029, zest the same category by the triality-equivariant cocycle λ(a,b)=t(ab)² on the additive group of F4. The invertible subcategory is Tannakian, so this is an actual associative zest with scalar cocycle one. Schur–Zassenhaus supplies an equivariant symmetric trivialization of the pointed tensor data; thus triality preserves the entire categorical zesting datum and gives a coherent action on the new category. Its equivariantization has the required dual pair of dimension-six simples. See [the proof and generator](models/d4_zest_triality.md) and [the independent categorical audit](integral_theory/d4_zesting_audit.md). Both cocycle witnesses match all 729 coefficients.

## Remaining rings and scope of the attempts

Every ring still listed below is unresolved in general scope. All have a justified weak-integral, pseudo-unitary, or Galois-pseudo-unitary reduction. This does not assert that an unresolved ring is categorifiable. The exact profiles, duals, proper fusion subrings, formal codegrees, gate links, and per-ring attempt links are in [the residual inventory](results/unresolved.json).

The new pass includes higher indicator and rational-character symmetry constraints for the remaining commutative integral rings; joint quadratic center systems; module and Morita-integrality tests; coherent equivariantization and fermion-product constructions; and explicit finite-group/group-theoretical comparisons. The numerical limits of individual discovery searches remain no-conclusion outcomes. These searches are not claimed to classify all fusion categories with a given dimension.

For 1848, a weighted noncommutative-center argument forces the low restriction columns. Exact high-column Gram enumeration gives 420 patterns. A noncommutative modular-integrality refinement retains twelve; additional rotation and Clifford-indicator constraints exclude some subbranches but leave a feasible necessary system. The ring is therefore retained. The exploratory cyclic-C3 Fourier module test did not settle the dimension-96 family; its later classifications use the separate solvability and triality arguments above.

| Residual type | Identifiers |
|---|---|
| Integral, commutative (6) | 12, 92, 392, 941, 959, 1246 |
| Integral, noncommutative (1) | 1965 |
| Non-weakly-integral, commutative (10) | 114, 128, 137, 516, 1487, 1607, 1635, 1636, 1959, 1976 |
| Non-weakly-integral, noncommutative (2) | 1848, 1975 |
| Weakly integral, commutative (10) | 585, 746, 965, 1025, 1209, 1254, 1303, 1709, 1759, 1988 |
| Weakly integral, noncommutative (2) | 1225, 1673 |

The 5 noncommutative residual rings (1225, 1673, 1848, 1965, 1975) are excluded from braided categorification, since braided Grothendieck rings are commutative. Their general, pivotal, spherical, pseudo-unitary and unitary categorification problems remain unresolved. The residual profiles store these scopes separately. For a Galois gate, the equivalence concerns existence with the given ring; it does not assert that every original category is pseudo-unitary.

## Verification and use

The baseline in `results/` is preserved. The authoritative continuation is in `phase2/results/`; `phase2/accepted.json` is the explicit list of additions. Run `python3 phase2/verify_continuation.py` to check the partition, source hashes, tensor identifications, and accepted verification receipts. Add `--fresh` to rerun the family-specific exact exclusion verifiers. Running `python3 phase2/integrate.py` rebuilds that ledger. `python3 phase2/verify_models.py` checks the accepted model tensors independently. `python3 phase2/replay_constructors.py` regenerates the explicit constructors. The family-specific exact verifiers are documented with their theorems. The original root `verify.py` replays the baseline and the input audit.

Proof and construction claims remain AI-generated research pending independent human verification. Computational replay checks the stated finite certificates and tensor identities; it does not replace mathematical review of the supporting theorems.

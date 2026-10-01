# Identification status of the reconstructed rank-26 datum

1 October 2026. No named categorical realization was identified. The reconstruction and independent audits establish a full candidate modular datum and a compatible forgetful **fusion-ring** map. They establish neither a modular category nor a categorification of R6_4_155. Absence of a literature match is not a nonexistence theorem.

## Exact fingerprint

Write d=4+3√2 and z=exp(2πi/24). The candidate B has rank 26, dimension (12d)²=4896+3456√2, twist order 24, normalized Gauss sum z⁻³, two invertibles (the nontrivial one a fermion), and ten selfdual simple objects. Its dimension multiset is

| Dimension | Multiplicity |
|---|---:|
| 1 | 2 |
| d | 6 |
| 2d | 8 |
| 3d | 2 |
| 1+2d | 4 |
| 1+4d | 2 |
| 2+4d | 2 |

The full candidate center is Semion ⊠ B, of rank 52. The normalized modular representation for B has constituent dimensions 9+6+4+3+2+1+1. Its fusion coefficients are nonnegative integers with maximum nine. All 26² products also satisfy the frozen forgetful-matrix identities in R6_4_155, with the tensor unit preserved; see `modular_audit/forgetful_ring_audit.*`.

## Direct WZW identification is excluded

For a full untwisted WZW category associated with a simple Lie algebra at positive integral level, rank counts integrable dominant weights. Counting nonnegative solutions of Σ aᵢ∨λᵢ≤k gives exactly these rank-26 cases:

| WZW type and level | Incompatible fusion invariant |
|---|---|
| A₁ at level 25 | All 26 simple objects are selfdual |
| A₂₅ at level 1 | All 26 simple objects are invertible |
| B₂₂ at level 2 | All 26 simple objects are selfdual |
| C₂₅ at level 1 | All 26 simple objects are selfdual |
| D₁₉ at level 2 | Four invertible simple objects |

`wzw_rank26.py` and its JSON receipt perform the small exact weight-count calculation with the dual marks recorded. All levels beyond the checked bound have more than 26 weights by monotonicity. Lie ranks beyond 26 are excluded by the level-one/level-two rank formulas (A,C: r+1; B at level two: r+4; D at level two: r+7). The selfduality assertions follow from the longest Weyl element being −1 for A₁, B, C. These invariant mismatches also exclude Galois conjugates and braid reversals with the same fusion rules.

This is a direct WZW exclusion only. It does not exclude cosets, orbifolds, subcategories, nonstandard quantum-group root orders, or condensation constructions.

Primary cross-checks:

- Gannon–Höhn–Yamauchi, [online MTC catalog by rank](https://www.math.ksu.edu/~gerald/voas/mtc/mtc-byrank.html), lists A₁,₂₅, B₂₂,₂ and D₁₉,₂. The catalog has a finite Lie-rank range and is not being treated as a complete classification.
- Its [D₁₉,₂ entry](https://www.math.ksu.edu/~gerald/voas/mtc/kmD19_2.html) explicitly records four dimension-one objects.
- Ostrik–Rowell–Sun, [Symplectic level-rank duality via tensor categories](https://arxiv.org/pdf/2002.07744), introduction and §2, prove the C₂₅,₁ / C₁,₂₅ level-rank equivalence up to braiding modification and explicitly recall selfduality of all symplectic simple objects.

## The near-group route and present literature

The closest current classification is Meng–Yu, [Classification of some Z₂×Z₂-quadratic fusion categories of rank 6](https://arxiv.org/abs/2608.06064), August 2026. Its Theorem 1.1 and Theorem 4.8 leave the nonselfdual ring R′(4), which is this R155 ring, unresolved. The constructions in §5 concern R′(0) and R′(2).

Radchenko–Wheeler, [Real quadratic fields and finite quantum dilogarithms I](https://arxiv.org/pdf/2609.21892), Theorem 12 and Corollary 6, September 2026, provide actual complex near-group categories of type (G,|G|) for G=Cₙ×Cₘ. This supplies the previously unavailable order-32 examples C₃₂, C₂×C₁₆ and C₄×C₈. However, the independently audited argument in `../r155_categorical/rw_small_algebra_obstruction.md` proves that none of their centers has a connected étale algebra of dimension eight. Consequently none yields the required rank-52 center by the dimension-matching direct condensation. This conclusion uses the explicit algebraic half-braiding identities and does not presume unitarity of the new construction.

The alternate dimension-compatible near-group type (|G|,m)=(8,16) remains a conditional route. No actual category of this type, nor a central quotient realizing R155, was established in this investigation. The prior exclusions of the five direct Grossman–Izumi potential-data formulas remain valid.

The correct result is therefore a newly explicit, independently checked modular-data candidate for an unresolved rank-six categorification problem, with several concrete model families ruled out. A construction still requires associators and the relevant central/tensor structures, or an independent realization theorem.

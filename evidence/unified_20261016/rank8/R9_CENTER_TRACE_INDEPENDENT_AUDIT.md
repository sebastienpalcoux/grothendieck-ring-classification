# Independent audit: the general R8_1_9 center obstruction

Auditor: `/root/two_dimension`, 2026-10-16.

**Verdict: PASS.** The complete argument excludes both possible pointed
associator classes after the established two-dimension Galois
pseudo-unitarity reduction. It therefore proves a general complex
categorification obstruction, not only a unitary or pseudo-unitary result.

I read the complete `R9_CENTER_TRACE_PROOF.md`, the full standalone verifier
`verify_r9_center_trace.py`, and both integer covectors. I independently
checked the new categorical Fourier lemma and replayed the final source-bound
verifier with Python optimization enabled. The fresh receipt is
`r9_center_trace_independent_optimized.json`.

## Categorical points independently checked

1. **Pointed indicator reduction.** The two self-dual source noninvertibles
   have odd unit multiplicity in their cubes, so their palindromic pivotal
   forms have positive sign. The odd multiplicity of the involution in the
   same cubes forces its indicator to be positive. Restriction of a cyclic
   C4 associator class k to the involution gives indicator (-1)^k, leaving
   precisely k=0,2. The order-four indicators are respectively +1 and -1.

2. **Exact cyclic phase multiplicities.** For an invertible a of order4,
   induction and positivity force every twist in I(a) to satisfy
   theta^4=nu4(a). This uses equality in the triangle inequality, not a
   braiding on the underlying category. The lower three rotation spaces
   vanish. Fourier inversion on the four roots of nu4(a) then gives weighted
   dimension D/4 for each individual phase. The source pointed Gram block
   is exactly8I4, so a restriction row containing a contains no other
   invertible. Its dimension is v_a+B d. Comparing the rational coefficient
   in each phase gives sum v_a^2=2 and hence v_a<=1. The argument is uniform
   in all C4 associator classes; its use only in the class-zero numerical
   domain is a harmless weakening. Crucially, this comparison is performed
   before averaging non-real phases together.

3. **Complete low rows.** The canonical central unit and its Galois partner
   are fixed. Commutativity of the source ring makes every character
   one-dimensional, so the remaining six I(1) constituents each occur once,
   have dimension D/8=1+2d, and have unit multiplicity1. Their profiles of
   total noninvertible multiplicity2 are therefore exhaustive. The verifier
   imposes duality, aggregate FI(1), and actual character-labelled S symmetry.
   Repeated codegree8 does not authorize arbitrary relabelling of these
   characters. The resulting eight assignments are exhaustive.

4. **Full Galois partner rows.** The non-FP characters are fixed by an
   automorphism negating sqrt(5) and fixing i; their character sums on the
   nonpointed orbit vanish. Together with the FP/conjugate pair this gives
   the displayed transport T. Actual restriction rows have a nonnegative
   signed partner. Distinct row types occur with equal multiplicity, and
   joint Gram positivity is therefore necessary. If a row is fixed, the
   single-row column allows arbitrary multiplicity and does not incorrectly
   assume that the corresponding central simple is Galois fixed.

5. **Partner moments.** In the anomaly-free center, modular Galois symmetry
   sends theta to sigma^2(theta). Since sigma^2 fixes the quadratic dimension
   field, the normalized relative moments are identical for partner rows.
   This does not assert equality of actual twists. The all-root 17-vertex
   hull is valid for arbitrary conductor: the odd factor coprime to10 scales
   both moments by mu(m)/phi(m) in[-1/2,1], and all required zero cases lie
   in the stated convex hull. No Cauchy prime-support premise is needed.

6. **Exact row domain.** The dimension-divisibility filter is valid because
   (D/z)^2 is a modular formal codegree and integral; D/z is integral over
   that algebraic-integer ring. The trace/norm test is the full quadratic
   integer-ring test. Bounds, partner pairing, nonnegative entries, and all
   positive semidefinite tests are exact. The verifier uses rational Schur
   elimination, including zero-pivot checks; it performs no numerical
   pruning or optimization.

7. **Separating inequality.** For every allowed row orbit and phase vertex,
   the constructed column is its Gram contribution and its first two
   relative induction moments. All actual multiplicities are nonnegative,
   so a nonnegative real combination must reach the stated target. Each
   covector is nonnegative on every reconstructed column and negative on
   the target. This is a complete contradiction even in the relaxed real
   cone, and does not rely on an integer-programming infeasibility claim.

## Replay and scope

The optimized replay reconstructs the immutable source tensor, all ordered
fusion checks, the six rational-codegree characters, all low assignments,
all high row orbits, the universal moment hull, and the two exact covector
checks. It passes all16 branches (eight low frames in each pointed class).

- Class0:64 row orbits,405 moment columns, minimum column pairing0,
  target pairing-64.
- Class2:92 row orbits,389 moment columns, minimum column pairing0,
  target pairing-6432.

The source hash is
`1718ab13b6969ed751b621f7303b9e2bb29bb8280f692315499b130a420538f6`.

Earlier five-moment integer experiments and their longer rounding
certificate are unnecessary for this proof. The final packet establishes
the stronger conclusion with a shorter source-bound two-moment argument.

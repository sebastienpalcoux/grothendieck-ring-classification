# Independent review of the additional noncommutative central constraints

Result: PASS for the stated necessary conditions and pointed-associator consequences. This is a separate AI-agent review, not a human review or a formal proof-assistant verification. It proves neither existence nor nonexistence of R439, R455, or R567.

The previously reviewed unrestricted signed gates supply a spherical structure and a pseudo-unitary Galois conjugate for every hypothetical complex categorification. All indicator statements below concern the canonical positive spherical structure of that conjugate. No unitary structure is assumed.

## Independent finite domains

`verify_additional_nc_constraints.py` re-enumerates restriction vectors from complete integer boxes, using dimension equations and the rational kernel of the induction Gram matrix. It does not use the producer's affine restriction solver or native Gram enumerator. It reconstructs every weighted low frame, quotienting only permutations of identical column sets with identical unit multiplicities.

| Ring | Complete low-column counts | Complete low frames | Dimension-compatible S bijections tested | Symmetric frames |
|---|---|---:|---:|---:|
| R439 | 3, 2, 2, 3 | 5 | 10 | 1 |
| R455 | 1, 1, 1, 1 | 1 | 2 | 1 |
| R567 | 3, 2, 2, 3 | 5 | 10 | 1 |

Every retained frame has two symmetric assignments. The review checks every scalar multiplication identity and computes every entry of the five-by-five distinguished S matrix directly, including the two-dimensional trace character and its required factor of two. R567's nonreal scalar characters are retained in the exact extension of the FP field by i. Symmetry uses equality in this field, without taking real parts or selecting a positive complex embedding.

For each of R439 and R567, the unique symmetric frame is index 2 in both independently reconstructed ordered lists. The review separately exhausts all 11,907 high-vector box entries. Range, entrywise Gram, and exact principal quadratic-form bounds leave 91 Gram vectors; formal-codegree quotient integrality and the dimension d-number condition leave exactly 45, agreeing with the full producer domain. This does not identify a center fusion ring.

## Exact height-six constraints

The review shares the previously reviewed joint-rotation matrix builder and finite relative-trace primitives. It independently checks the full-column separator pairings and every primal equation, rather than calling the producer's LP verification routine. No numerical optimization is performed.

Each system has 19 complete relative-trace types, order bound 144, 932 nonnegative variables, and 182 equations. All eight indicator tuples permitted by duality and the odd-adjoint-multiplicity theorem are covered for each ring. Seven tuples per ring have exact integer Farkas rays with nonnegative pairing against every one of the 932 columns and strictly negative right-side pairing. Each remaining tuple has an exact nonnegative rational primal witness satisfying all 182 equations.

The forced tuples, in source order 1 through 7, are

- R439: `(0,0,1,1,1,1,1)`;
- R567: `(0,0,0,0,-1,-1,-1)`.

An exact feasible relaxation is not a categorical model. The evidence only excludes the other necessary-condition branches.

Fresh completed commands:

```
python -O evidence/rank8_frontier_20261021/noncommutative_followup/additional_joint_rotation.py
python evidence/rank8_frontier_20261021/review/verify_additional_nc_constraints.py
python -O evidence/rank8_frontier_20261021/review/verify_additional_nc_constraints.py
python -O evidence/rank8_frontier_20261021/structural_models/pointed_s3_scope.py
```

## Pointed S3 consequence

The source-bound bridge verifies the six invertibles form S3, identifies its C3 subgroup and all three involutions, and checks that each noninvertible is fixed by C3. A fixed simple provides a rank-one module over the pointed C3 category, so its module pentagon trivializes the restricted associator class.

In a pointed C2 subcategory with its positive spherical dimensions, the second indicator of its nonidentity invertible is the sign of the third-cohomology class. Therefore R439 has trivial restrictions to both C2 and C3. Restriction followed by corestriction multiplies by the subgroup index, for arbitrary finite-index subgroups. Consequently 3[omega]=0 and 2[omega]=0, whence [omega]=0. No claim about an untested component of H3(S3,C*) is needed. R567 instead has nontrivial C2 restriction.

It follows that every hypothetical complex R439 category has the full S3 subgroup algebra: establish it on the pseudo-unitary Galois conjugate, then transport the trivializing cochain and algebra back. For R567 this full subgroup algebra is impossible, although its C3 algebra remains available. These are unconditional necessary-structure results within hypothetical categorifications.

The separate complete conditional S3 condensation calculation and replayed rank-five exclusions then apply to R439. They force a rank-five dual with based ring R5_3_40. The conclusion that this dual cannot be the known equivariantization uses the separately established absence of center invertibles for R439. This review does not identify an associator on that positive based ring or assert that a different one exists; its rank-five dependency is the separately replayed structural package.

Primary sources checked directly:

- Ostrik, [Pivotal fusion categories of rank 3](https://arxiv.org/pdf/1309.4822), Theorem 2.13, Corollaries 2.14–2.15 and Section 5.1, for induction, dimensions, and sphericalization. Corollary 2.14 is divisibility; Corollary 2.15 is dimension-field membership.
- Schauenburg, [A Higher Frobenius–Schur Indicator Formula for Group-Theoretical Fusion Categories](https://arxiv.org/pdf/1502.02906), Definition 2.2 and Proposition 4.1 with trivial subgroup, for the pointed indicator. For an involution the inverse convention gives the same sign; no non-adapted-cocycle formula is used.
- Brown, [Lectures on the Cohomology of Groups](https://pi.math.cornell.edu/~kbrown/papers/cohomology_hangzhou.pdf), Section 3.3, equation (3.12), pp. 21–22, for restriction/corestriction at arbitrary subgroups.

## Manuscript source and scope check

The all-seven NC gate theorem correctly concludes only sphericality and existence of a pseudo-unitary Galois conjugate. The all-level SU(2)/adjoint product sieve correctly excludes the stated family of products, integer-dimension operations, and Morita changes, with no claim about arbitrary condensation or other Lie types. Its product-field lemma is sound: simultaneous maximality and positivity force every product stabilizer to fix every factor. The exact finite arithmetic has a separate completed review in `structural_models/su2_independent_review.json`.

The central-invertible refinement closes the sole nonintegral SU(2) dimension branch for R439/R567: its multiplier is exactly two, so one faithful C2 extension, equivariantization, or dimension-two product factor supplies a center invertible; any subsequent Morita change preserves it. This conclusion does not rely on equating categories from matching dimension or rank. The near-group NG(C_n,n) test remains explicitly restricted to the listed single operations; the more general R721 near-group dimension test allows positive integer multipliers and Morita changes but no dimension-decreasing operations.

The source citations for the SU(2) dimension, Morita dimension invariance, grading dimensions, center invariance, rank-two obstruction, and actual Izumi inversion action were checked against Coquereaux1209.6621 p.8; ENO math/0203060 Corollary8.14 and Proposition8.20; ENO0909.3140 Introduction p.3; Ostrik math/0203255 Main Theorem p.1; and Izumi1512.04288 Lemma13.1 and Example13.10. The two undefined manuscript aliases were replaced by existing ENOExt and Ostrik2 keys with parent authorization. Citation additions to the frozen quadratic NC fragment are to be performed only during publication assembly.

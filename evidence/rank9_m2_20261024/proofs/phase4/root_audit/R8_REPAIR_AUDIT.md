# Independent review of the R8_3_436 replacement

The old TPE parameterization argument is withdrawn. The replacement in
`../r8_scope/REPAIR.md` passes the following independent categorical review.

1. The source supplies a faithful C2 grading, a neutral NG(C3,3) subcategory,
   and an odd order-two invertible inducing inversion. The possible associator
   class of that invertible is genuinely an element of H3(C2,C*). Multiplying
   the graded associator by its inverse preserves the tensor and neutral
   category and trivializes this particular pointed subcategory. This proves
   existence of the coherent conjugation action needed later; it does not
   assert coherence for an arbitrary isolated autoequivalence.
2. Thornton Theorem1.3 applies to an arbitrary near-group fusion category,
   without braiding or unitarity. Tensor automorphisms of the identity of
   NG(C3,3) are trivial: gX=X forces the group scalars to1 and the X summand
   in X² forces the remaining scalar to1. Thus its pivotal structure is
   unique, so the action preserves it. Spherical equivariantization follows
   using the underlying pivotal maps, which are equivariant.
3. The equivariantization has precisely five simples. Projective stabilizer
   representations of C2 are one-dimensional over C. The canonical sign
   object is central; this, rather than a commutative input ring, forces
   the displayed rank-five multiplication to be commutative.
4. If the two lifts of X are dual to each other, duality of their equal
   squares forces equal splitting coefficients whose sum is3. This is
   impossible. All four self-dual splits are retained, without a positivity
   assumption on the spherical root d.
5. Their explicit scalar characters give formal codegrees in Q(sqrt5) or
   Q(sqrt13), neither contained in the spherical dimension field Q(sqrt21).
   Ostrik Corollary2.15 applies to arbitrary spherical categories. Its
   center-induction proof was checked directly in the primary text. The
   independent nonintegral field-norm calculation gives a second arithmetic
   formulation of the same contradiction.

I reran the source/tensor/formal-codegree verifier normally and under
Python optimization; both passed. Those computations check the finite
premises and arithmetic, while the argument above checks the categorical
steps. No claim that code proves the cited categorical theorems is made.

**Accepted:** general complex noncategorifiability of R8_3_436, with a new
proof. **Not accepted:** the stronger old assertion that every spherical
NG(C3,3) category is equivalent to one in a unitary-derived scalar table.
This assertion remains withdrawn even though the ring exclusion is repaired.

Primary texts read directly: Thornton arXiv1102.4640v1 Theorem1.3;
Ostrik arXiv1309.4822v1 Theorem2.13 and Corollary2.15.

# Scalar characters and weighted induction in rank eight

The common kernel of all commutators in the regular representation is exactly
the direct sum of the one-dimensional simple representations. On every matrix
block of size at least two the commutators have no common kernel. The code
checks the invariant subspace and all polynomial coordinates of a separating
element. Its simple spectrum therefore supplies every scalar character.

In the noncommutative cases used here this space has dimension four. Since the
whole semisimple algebra has dimension eight, the remaining block is M2. The
Casimir acts there by twice its formal codegree. Division of the full Casimir
polynomial by the scalar Casimir polynomial must give one fourth power of a
linear factor; the exact check then divides that eigenvalue by two. A repeated
scalar codegree causes no ambiguity in this polynomial division.

For a spherical categorification a scalar dimension character has nonzero
values, agrees on duals, and its global dimension D is divisible by every
formal codegree in the algebraic integers. All formal codegrees belong to its
dimension field. These are Ostrik, *Pivotal fusion categories of rank 3*,
Theorem 2.13 and Corollaries 2.14–2.15. The norm and field tests are inherited
exact necessary consequences, evaluated over each irreducible character field.

For a general category, every oriented signed quotient allowed by its
sphericalization is enumerated, with the full associativity relations and
the positive-second-indicator choice. A signed quotient is rejected only by
the verified adjoint parity test, a gauge equivalence to the excluded original
spherical ring, or failure of every scalar dimension character. For a signed
quotient the required formal codegrees include those of both summands; the
common factor two in the sphericalization cancels from the integrality test.
No pivotality conjecture is assumed.

In the pseudo-unitary case the constituent A_E of I(1) has dimension D/f_E
and multiplicity dim(E). Its restriction column consequently begins with
dim(E), not one. Every distinct central simple contributes its column square
once to the induction Gram matrix. The first row of the Gram identity has
the multiplicity-weighted sum of the columns. `weighted_rank8.py` computes
this Gram matrix directly from the tensor, and `weighted_data_fast.py`
exhausts the complete weighted row-sum constraint. The inherited induction
and indicator tests retain their exact arithmetic. A general exclusion via
this shorter route requires the explicitly checked weak-integrality or
two-FP-dimension reduction; otherwise it remains only a scoped attempt.

All regenerated certificates are checked from the restored source tensors.
Old counts and saved progress messages are not inputs to their acceptance.

# Independent audit: R8_2_191 and R8_2_299

**APPROVED: general complex exclusion.**

The exact source checker was read and rerun in ordinary Python and with
`python3 -O`. Both runs pass, and all mathematical output agrees after
removing the interpreter-mode and elapsed-time fields. The checker uses
explicit `require` calls, not removable assertions. It reopens the census,
checks associativity and the complete neutral tensor, both faithful
gradings, the transitive pointed action and its order-two stabilizer, and
the full positive dimension character. It also exhausts all ten subgroups
of A4 and its normal abelian subgroups, of orders one and four.

The theoretical proof was independently checked against Galindo,
*Clifford theory for graded fusion categories*, arXiv:1010.5283,
Theorem 1.3 and its proof on page 19. The theorem concerns the dual of the
**induced** module `D tensor_B N`, as used in the corrected draft. The
original odd component supplies an actual coherent D-module extension
of N. This is stronger than invariance of its abstract module class and
meets the theorem's hypothesis. No claim that the dual of the original
rank-two module is pointed is needed.

The rank-one components of the C3 grading force the pointed neutral
associator to be trivial. The rank-two pointed module is the subgroup
module for C2 inside V4, whose dual is the untwisted pointed V4 category.
The original rank-one bimodule is a nontrivial order-three
Brauer--Picard class; Morita conjugation preserves this fact. In the
semidirect product furnished by Galindo, its tensor autoequivalence
cannot have trivial underlying group automorphism, because that kernel
is H2(V4,C*)=C2. Thus the group of simples is V4 semidirect C3, namely A4.

The extension-integrality lemma in `R53_R93_GENERAL_PROOF.md` was read
separately. Its use of twisted group-theoretical dimensions, normal
abelian stabilizers, normalization by sqrt(|H|), transport of graded
extensions, and Morita invariance of integrality applies to arbitrary
pointed associator. Since the only normal abelian A4 subgroups have
square order, a graded extension of the neutral category is integral.
The verified sqrt(6) odd dimensions contradict this. No classification
of all neutral categorifications, pivotal structure, or unitarity is
assumed.

The checker establishes the exact ring and finite-group premises. The
categorical implication is the independently audited argument above,
not an automated theorem-proof claim.

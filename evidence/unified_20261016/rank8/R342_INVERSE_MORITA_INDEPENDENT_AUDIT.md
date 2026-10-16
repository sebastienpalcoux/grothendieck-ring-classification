# Independent audit: R8_2_342 inverse Morita obstruction

Status: **PASS for the general complex exclusion**.

I reviewed the complete source-bound reconstruction verifier and the final
`R342_INVERSE_MORITA_PROOF.md` in `evidence/unified_20261016/rank8`.
An independent optimized-Python execution passes, with receipt
`r342_inverse_morita_independent_O.json`. The source hash is
`6d9246ba099d4676e98ae3cc60bba5a176db651fa740b5f8c4c5906ff652ae5d`.

The finite completeness argument has the necessary coverage. The fixed
objects trivialize the pointed C2 associator, so the regular algebra is
actual. All bounded antisymmetric module representations are enumerated
using three generators and checked against every product. The distinguished
Gram matrix 2I forces two standard restriction columns per module label.
Every nonnegative right-action matrix lies in the explicitly bounded
commutant domains. Multiplication by the second invertible pairs those
domains; the simultaneous linking Gram equations leave exactly one joint
solution. The action is not incorrectly assumed faithful: its kernel is
handled by complete bounded coefficient equations, and ten forced fusion
matrices generate the whole fourteen-dimensional algebra. Thus associativity
determines the other products. All reconstructed products and all 14^4
associativity equations are then checked.

The neutral rank-seven identification is a complete based-ring comparison.
The matched PSU(3)_5 generator has a cyclic unit vector, so its seven powers
determine the entire algebra, not merely a dimension profile. The module
restricts regularly to this neutral subcategory. Depending on the matrix
composition convention, its bijection uses objects or their dual labels;
both give the required regular module and the same internal end algebra.

I independently checked the tensor-autoequivalence reduction against
Edie-Michell, arXiv:2002.03220v2, Theorem 1.1 and its gauge-kernel argument.
In the standard SU(3)_5 modular category the nondegenerate pointed C3
factor splits off. A label-fixing autoequivalence of PSU(3)_5 extends by
the identity on that factor. Triviality of the SU(3)_5 gauge kernel then
restricts back to triviality on PSU(3)_5. This statement transports under
Galois conjugation. Together with the exact based automorphism group C2,
the nontrivial based permutation therefore determines a unique tensor
autoequivalence class. The checked universal grading is trivial, so
Aut_tensor(Id) is trivial and any coherent action in that class is unique
up to equivalence. The general-complex Kazhdan--Wenzl scope used in the
proof is independently covered by the companion rank-six audit and
Feng--Ming--Rowell, Theorem 5.1: applying it to B times Vec_C3 and then
restricting to the adjoint subcategory removes the grading cocycle.

The key categorical reflection is justified by an actual algebra, not
just an abstract grading. The forced first columns show that the internal
endomorphism algebra of the regular neutral generator is 1 plus u.
Its multiplication trivializes the pointed associator and supplies the
coherence needed to identify the extension with the crossed product.
Its dual is the corresponding C2 equivariantization. Uniqueness of the
nontrivial action identifies this with the known R8_2_666 construction,
up to Galois conjugation. The self-duality discrepancy with R8_2_342 is
then a contradiction between full based rings.

No pivotality, pseudo-unitarity, unitarity, or braiding assumption is
introduced for the hypothetical source. No gap was found in the final
proof or in the finite-domain completeness argument.

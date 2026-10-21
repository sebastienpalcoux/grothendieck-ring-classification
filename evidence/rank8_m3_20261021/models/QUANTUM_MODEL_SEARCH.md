# Additional quantum-group model searches

The reproducible script `quantum_model_attempts.py` records a bounded
dimension search through classical WZW categories and an exact follow-up
to the resulting SU(3)_7 lead. Numerical comparisons are discovery aids
only. They are never positive model certificates or general exclusions.

For the quartic dimension
144+96sqrt(2)+80sqrt(3)+56sqrt(6), the numerical search covers types
A1–A12, B2–B12, C2–C12, D4–D12, levels1–35, and the explicitly recorded
fourteen dimension ratios. No candidate appears in this finite search.
This does not classify quantum-group constructions, algebra objects,
subcategories, tensor products, or arbitrary Morita equivalence classes.

The same bounded scan is replayed against all277 baseline survivor
dimension profiles, with every numerical lead preserved by census ID.
These are approximate dimension-ratio matches, not fusion-rule matches.
For R439/R567 the leads SU2_10, B2_3, C2_3, C3_2 and C10_1 do not yield
Morita models: each standard WZW category has the nontrivial C2 grading
from its weight/root-lattice quotient. Its center therefore contains
Rep(C2). The exact central-invertible/adjoint-generation test for these
two census rings shows their categorical centers have no nontrivial
invertibles. Morita invariance of the center rules out the named families,
regardless of the numerical dimension coincidence.

The scan also found that
R8_3_65 and R8_3_1453 have exactly the global dimension of the adjoint
subcategory P of C(SU(3),7): 250+110sqrt(5). The script verifies this
identity from the twelve triality-zero Weyl quantum dimensions. This
coincidence leads to a stronger scoped negative result: neither rank-eight
ring is a unitary Morita dual of this particular category P.

Here is the reason. Gannon, *The classification of SU(3) modular invariants
revisited*, [hep-th/9404185](https://arxiv.org/pdf/hep-th/9404185),
equations(4.1), Theorem2(i), Lemma2 and Theorem1, imply that at level7
every modular invariant is a permutation matrix. The necessary norm and
parity conditions already force the vacuum to couple only to itself;
the script verifies this directly over all36 shifted weights. Every such
matrix has squared entry norm36.

By Fuchs–Runkel–Schweigert, *The fusion algebra of bimodule categories*,
[math/0701223](https://www.math.uni-hamburg.de/home/runkel/PDF/bim.pdf),
TheoremO, the rank of the category dual to any unitary indecomposable
module category is the squared entry norm of its modular invariant.
Consequently every unitary Morita dual of C(SU(3),7) has rank36.

The three invertible objects of C(SU(3),7) form a nondegenerate pointed
subcategory Q, since 7 is coprime to3. Its braided centralizer is P, and
the standard nondegenerate centralizer decomposition gives
C(SU(3),7) ≅ P ⊠ Q. If a unitary module category over P had a rank-eight
dual D, its Deligne product with the regular module category over Q would
give a module category over C(SU(3),7) with dual D ⊠ Q^op of rank24.
This contradicts the rank36 consequence above. Indeed the same argument
forces every unitary Morita dual of P to have rank12.

This is a model-family obstruction. It does not rule out categorification
of R8_3_65 or R8_3_1453 by another construction.

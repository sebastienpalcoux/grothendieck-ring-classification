# Split-involution Morita Gram conditions without commutativity

Let C be any complex fusion category and let g be an invertible involution whose based-ring class is central and fixes some simple object. The fixed object trivializes the associator class on <g>, so A=1⊕g is a connected separable algebra. Put M=Mod_C(A), and let D be its dual fusion category. No braiding, pivotality or pseudo-unitarity is assumed.

Use row-oriented left action matrices M_i[a,b]=[X_i⊗m_a:m_b]. Then M_i M_j=Σ_k N_(ji)^k M_k. Transposition gives M_(i*)=M_i^t. Centrality of the based-ring class of g ensures that its left and right object permutations agree, so the same split-involution module formulas apply. Their verification must use the reversed product N_(ji), as `noncomm_morita.py` does.

To justify the full Gram identity, form the standard two-object Morita linking multifusion category, with diagonal corners C,D and off-diagonal corner M. Write B_j[a,c]=[m_a⊗Y_j:m_c] for the right D action. Frobenius reciprocity and associativity give

dim Hom_C(m_b⊗bar(m_a),m_d⊗bar(m_c))
=Σ_i M_i[a,b]M_i[c,d]
=dim Hom_M(m_b⊗(bar(m_a)⊗m_c),m_d)
=Σ_j B_j[a,c]B_j[b,d].

Thus the matrix indexed by pairs(a,c),(b,d) is the nonnegative integral Gram matrix of the flattened B_j. The implementation's expression Σ_i M_i[b,a]M_i[d,c] is equal to the same expression after replacing i by i*. This identity is independent of whether K0(C) is commutative.

Every B_j commutes with every M_i by the bimodule associativity constraint. Both its first row and its first column occur in the Gram decomposition of I+M_g: the forgetful functor from A-bimodules to right A-modules has free adjoint A⊗−, and its composite is 1⊕g acting on M. Since M_g is an involutive permutation, this Gram decomposition has exactly two unit columns at each fixed point and one pair-column at each transposition. This forces the number of simple objects of D and the first-row/first-column multisets used in the full Gram system.

The partial Gram systems also remain valid: fix a simple m, decompose its internal end in C, and apply the same Frobenius-reciprocity identity. The FP dimension normalization for module objects is positive for every fusion category. Consequently the existing exact Gram-column domains, commuting-action constraints, rank obstructions and Farkas separators remain necessary after correcting the row orientation.

The program changes the local verification formula only; baseline source files are untouched. A surviving branch is recorded as no conclusion. Any proposed exclusion still requires complete anti-module enumeration and an independently replayed exact obstruction for every branch.

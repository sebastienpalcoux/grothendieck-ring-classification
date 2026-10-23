# Independent audit of the C4-extension comparison for R11_1_153

Verdict: the comparison argument is valid, conditional on the separately
verified neutral-category reduction to Rep(D8), the known BrPic group S4 and
its stated action on Inv Z(Rep(D8)), and the exact R11_1_104 model.

## Aligning the grading homomorphism

The even nonneutral component has rank two. Therefore the grading-generator
class in BrPic(Rep(D8)) cannot have order one or two: its square would otherwise
be the regular bimodule class, which has rank five. Since its fourth power is
the identity and BrPic is S4, it is a four-cycle.

In the alternating Tambara–Yamagami presentation of Rep(D8), every isometry
of the bicharacter on V4 acts by reindexing the invertible labels and fixing the
unique noninvertible. The associator formulas are unchanged, so these are
actual tensor autoequivalences. This gives a subgroup
Aut(V4,χ_alt)=GL(2,F2)=S3 of Aut⊗(Rep(D8)). Its map to BrPic is injective:
the kernel of induction consists of inner autoequivalences from invertible
objects, and conjugation by an invertible is tensor-isomorphic to the identity
in this braided category. Equivalently, none of the six reindexings have the
same simple-object permutation.

Every S3 subgroup of S4 is a point stabilizer. Its conjugation action on the six
four-cycles is free and transitive, since the centralizer of a four-cycle is C4
and has trivial intersection with a point stabilizer. Therefore neutral tensor
autoequivalences align any relevant grading homomorphism with that of the
reference R104 model. This is stronger than conjugacy by an arbitrary Morita
autoequivalence: the aligning maps are actual tensor autoequivalences and do
preserve the reference neutral category.

## Restricting systems of multiplication

Let A=Inv Z(Rep(D8)), with generator action T=1+N on its three-dimensional
F2-space, where N has a single Jordan block of length three. For fixed
c:C4→BrPic(Rep(D8)), ENO *Fusion categories and homotopy theory*,
arXiv:0909.3140, Theorem8.5, makes the systems of products a torsor over
H²(C4,A). Once one actual reference extension exists, no separate obstruction
vanishing argument is needed for this comparison.

The difference between two systems is represented by a normalized A-valued
2-cocycle. Restriction of the multiplication functors to the even subgroup
restricts that same cocycle. Here

    H²(C4,A) = ker N / (1+T+T²+T³)A = ker N,
    H²(C2,A) = ker N² / (1+T²)A = ker N² / im N².

The even-degree restriction sends an invariant representative a to the same
representative a. This can also be seen by lifting a generator: if x⁴=a,
the square lift has (x²)²=a. Since kerN=imN², this restriction is zero.
Consequently the two even systems of products are equivalent by degreewise
bimodule equivalences. These equivalences can relabel simples, but preserve
fusion coefficients and the count of self-dual simples in degree two.

ENO Theorem8.9 parametrizes the remaining associativity choices for a fixed
system of products by scalar H³. Changing an associator does not change
multiplication multiplicities; duality on simple classes is already determined
by the unit coefficient in the multiplication table. Thus it cannot turn a
pair of self-dual simple classes into one mutually dual pair.

The actual R104 model has a self-dual degree-two pair, whereas the exact R153
tensor has a mutually dual degree-two pair. Once the listed categorical
premises are supplied, this contradiction excludes R153 for general complex
categorifications. It is not a claim that the whole C4 extension or all its
associators are unique.

## Independent finite replay

`verify_c4_torsor.py` solves the normalized cocycle equations directly over F2,
without importing a cyclic-cohomology formula or producer implementation. It
finds all128 normalized 2-cocycles and all64 coboundaries for C4 acting on A.
For every cocycle it supplies an explicit normalized C2 one-cochain whose
coboundary is the restriction. It separately enumerates all six four-cycles
and all six point-stabilizer permutations, with explicit conjugators.
Both ordinary and optimized-Python executions pass; the full certificate is
`c4_torsor_independent.json`.

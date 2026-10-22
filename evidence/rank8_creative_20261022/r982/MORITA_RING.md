# Complete based-ring restriction on the Morita class of R8_3_982

**Every complex fusion category categorifying R8_3_982 has the same based
fusion ring R8_3_982 at every object of its categorical Morita class.**
This conclusion has no search bound on the rank or fusion multiplicity
of a possible Morita partner. It is stronger than the rank and
commutativity restriction in `MORITA_OBJECT.md`.

Thus Morita equivalence with a category having different fusion rules
cannot construct this ring. Its unitary realization is now identified
separately in `E21_MODEL.md`. A categorification could still have several
inequivalent Morita partners with these same fusion rules; this theorem
does not classify their tensor or module associators.

## The bimodule Gram identity

Let M be an indecomposable module category over a hypothetical
categorification C, and D its dual. Its based left module has one of the
three completely classified types in the preceding stage. Use row action
matrices

    (M_i)[a,b] = multiplicity of m_b in X_i*m_a,
    (P_j)[a,b] = multiplicity of m_b in m_a*Y_j,

where the Y_j are the simple objects of D. Internal-Hom associativity in
an invertible bimodule category gives

    sum_i (M_i)[a,b] (M_i)[c,d]
      = sum_j (P_j)[a,c] (P_j)[b,d].

Indeed, compute the coefficient of m_d in
`(m_b * dual(m_a)) * m_c = m_b * (dual(m_a) * m_c)`.
This is the fusion-bimodule compatibility condition of Grossman–Snyder,
*The Brauer-Picard group of the Asaeda-Haagerup fusion categories*,
Definition 5.7 and Lemma 5.9, derived there from categorical internal-Hom
associativity; see [arXiv:1202.4396v2](https://arxiv.org/pdf/1202.4396).

Flatten each action matrix into a column. Let U have the eight columns
vec(M_i), and V have the columns vec(P_j). Set

    G[(a,c),(b,d)] = sum_i (M_i)[a,b] (M_i)[c,d].

The identity says V V^t=G. For each of the three complete R8_3_982 module
types, the exact calculation verifies G=U U^t. All eight columns of U
are independent. The theorem in `MORITA_OBJECT.md` proves that D has
exactly eight simples. Consequently V=UQ for a real orthogonal 8-by-8
matrix Q.

## The integral row lattice forces Q to permute coordinates

For the regular type the rows of U generate Z^8. For both nonregular
types they generate exactly

    D8 = {x in Z^8 : sum_i x_i is even}.

These equalities are certified directly. The regular matrix has eight
rows with determinant one. Every row of either nonregular matrix has
even coordinate sum, and the eight rows with flattened indices
`[0,1,16,3,4,5,6,7]` have determinant of absolute value two. Containment
and equal index prove the D8 assertion.

For the regular type, integrality of V implies that Q maps Z^8 into
Z^8; orthogonality forces a signed permutation matrix.

For a nonregular type, integrality of V implies D8 Q is contained in
Z^8, using row vectors and matrix multiplication.
Equivalently, the lattice L=Z^8 Q^t is an integral unimodular overlattice
of D8. It is odd, because it is isometric to Z^8. Its index over D8 is
two.

Here is a direct classification of the relevant overlattices. The dual
lattice of D8 has four cosets modulo D8, represented by

    0, e_1, h=(1/2,...,1/2), h-e_1.

Any integral index-two overlattice must adjoin exactly one of the three
nonzero cosets. Adjoining e_1 gives Z^8. The other two have even squared
norms throughout: D8 is even, both representatives have squared norm
two, and their scalar products with D8 are integers. They are therefore
incompatible with the odd lattice L. Thus L=Z^8, and Q again preserves
Z^8 and is a signed permutation.

Every column of U is nonnegative and has at least one strictly positive
entry. Since V is nonnegative, no column sign can be negative. Therefore
Q is a permutation matrix in every case.

## Consequence for the full fusion rules

After relabeling the simples Y_j, their right action matrices P_j are
exactly the eight matrices M_i. These matrices are independent and obey
all the source fusion multiplication rules. The coefficients in every
product P_j P_k are therefore uniquely the corresponding coefficients
of R8_3_982. The identity and duality are also determined by these
faithful action matrices. Hence K0(D) and K0(C) are isomorphic as based
fusion rings.

The categorical argument initially uses the pseudo-unitary conjugate
to obtain the rank-eight conclusion of `MORITA_OBJECT.md`. Applying the
known Galois-conjugate gate to C and M together leaves all fusion and
module integers unchanged, so the result applies to every complex
categorification.

The proof combines a general regular-representation/full-center theorem
with a general Gram-factor lattice argument. The special computation
needed here is only the complete list of three module types and their
Z^8 or D8 row lattices. No bounded enumeration of possible dual rings is
used.

## Replay and scope

```sh
python3 evidence/rank8_creative_20261022/r982/morita_ring.py
python3 -O evidence/rank8_creative_20261022/r982/morita_ring.py
```

The receipt checks all 4,096 Gram identities for each type, explicit
integral bases, all source products, and the elementary discriminant
coset norms. It incorporates the exact preceding rank-eight receipt.
This Morita restriction is neither an exclusion nor an existence proof
by itself. The independent E21 construction realizes `1+X5` and both
nonregular based module types. Their dual categories have the same
R8_3_982 fusion rules, as the theorem requires. The construction does
not assert uniqueness of the possible module or algebra structures.

# Independent review of the R982 Morita based-ring theorem

**Verdict: accepted within its stated conditional scope.** The proof shows
that every category in the Morita class of a hypothetical R982
categorification has the same based fusion ring. It constructs neither a
category nor a module associator, and it does not identify Morita partners
as tensor categories. The reviewer is a separate automated mathematical
agent, not an independent human reviewer.

Reviewed files: `../../r982/MORITA_OBJECT.md`, `MORITA_RING.md`,
`morita_object.py`, and `morita_ring.py`.

## Index placement in the bimodule identity

For an invertible C--D bimodule M, fix simple objects m_a. With the row
conventions of the proof, Xi has multiplicity `M_i[a,b]` in
`m_b tensor dual(m_a)`, by internal-Hom adjunction. Likewise Yj has
multiplicity `P_j[a,c]` in `dual(m_a) tensor m_c`. The multiplicity of
m_d in the two parenthesizations of

    m_b tensor dual(m_a) tensor m_c

is therefore respectively

    sum_i M_i[a,b] M_i[c,d],
    sum_j P_j[a,c] P_j[b,d].

This establishes the stated reshuffling without silently replacing a
matrix by its transpose or its dual index. With rows indexed `(a,c)`, the
right expression is exactly `(V V^t)[(a,c),(b,d)]`.

The certified equality with `U U^t`, where U's columns are vec(M_i), then
implies that V and U have the same column space. The preceding canonical
center-object theorem gives exactly eight columns in V; U has rank eight.
Writing `V=UQ`, multiplication by any left inverse of U on both sides of
`V V^t=U U^t` gives `Q Q^t=1`. Hence Q is square orthogonal, as required.

## The lattice step

The row lattice is Z^8 in the regular case. In the other two cases, every
row has even coordinate sum and a displayed eight-row sublattice has
determinant two. The row lattice is therefore precisely D8, with no
unproved assumption about saturation.

The implication `D8 Q subset Z^8` gives

    D8 subset L=Z^8 Q^t,

because x=(xQ)Q^t. This orientation of Q is correct. Orthogonality makes L
an odd integral unimodular lattice, with index two over D8. Since it is
integral and contains D8, it lies in D8*. The four discriminant cosets
have representatives 0, e1, h and h-e1, with h=(1/2,...,1/2). Their orders
are two. Adjoining e1 produces Z^8. Adjoining either spinor coset produces
an even lattice: D8 is even, the representative has norm two, and all
cross terms are even integers. Thus Z^8 is the only odd possibility.
It follows that Q preserves Z^8 and hence is a signed permutation.

Every U-column is nonnegative and nonzero. A negative sign would create
a negative entry in V, so all signs are positive. No ambiguity from a
zero column remains.

## Full multiplication and scope

For right row actions, `P_j P_k` represents tensoring first with Yj and
then with Yk, so it encodes Yj tensor Yk in the displayed order. Left row
actions reverse order, but the source ring R982 is commutative; thus the
source multiplication identities checked in the code have the right
coefficients here. The eight action matrices are independent, so every
product determines its coefficients uniquely. The identity and duality
are then determined by the based multiplication. This proves a based-ring
isomorphism, rather than only a complex-algebra or dimension-spectrum
match.

The preceding regular-module/full-center theorem supplies the required
rank-eight conclusion: regularity forces all source canonical center
summands with their correct multiplicities; equality of positive FP
dimensions leaves no additional summand. The use of pseudo-unitarity is
confined to that theorem and is transferred to general categorifications
by the previously established simultaneous Galois conjugation of the
category and its module data. It does not assert unitary structures.

The exact producer replay passed in this review. An additional independent
Smith-normal-form computation in `verify_r982_morita.py` reconstructs the
three row-lattice indices and the full reshuffled Gram identity directly
from the frozen module actions.

# Excluding the whole actual cyclic-eight Morita class

There is no complex fusion category with based ring R6_3_215 weakly Morita
equivalent to the **actual** Grossman–Izumi cyclic-eight quotient D. This
strengthens the first continuation's obstruction for a specified restriction
map. It does not prove uniqueness of a braided category from modular data,
or resolve general categorifiability of R6_3_215.

Write d=4+sqrt(17) and Delta=8+32d. Suppose C had based ring R6_3_215 and
were weakly Morita equivalent to D. Global dimension is invariant under
duality of fusion categories, and D is pseudo-unitary. Its Frobenius–Perron
dimension is Delta, as is that of C. Hence C is pseudo-unitary. The same
argument applies to every dual of C considered below. Use their unique
spherical structures with positive simple dimensions. The induced braided
equivalences of centers preserve these structures, hence their twists.

The six irreducible characters of the commutative ring R6_3_215 are all
one-dimensional. Canonical induction of the unit therefore has six distinct
constituents, each with multiplicity one. Their formal codegrees are Delta,
its conjugate, 4,4,8,8, giving dimensions

    1, 1+8d, 2+8d, 2+8d, 1+4d, 1+4d.

Each constituent has twist one. The actual center Z(D) has exactly six
twist-one simples, with precisely these dimensions. Thus the canonical
induction vector of C in Z(D) is forced: it is one on those six labels and
zero elsewhere. No choice of a restriction matrix is used.

Let M be the D–C Morita bimodule. The canonical-induction inner product
gives rank(M)=6, and pairing the forced vector with the actual source
restriction gives the left-action traces

    Tr(1,alpha,alpha²,alpha³,rho,alpha rho,alpha² rho,alpha³ rho)
       = (6,0,2,0,8,8,8,8).

The invertible g in C fixes a simple, so the algebra A=1+g exists. The
previous continuation's exact full-Morita calculation proves that C', the
A-bimodule dual of C, again has based ring R6_3_215. Consequently its unit
induction in this same actual center has the same forced six-label support.
The D–C' bimodule M_A therefore also has rank six.

If the involution g fixes f of the six simples of M, its free orbits give
(6-f)/2 simple A-modules and each fixed object gives two. Thus

    6 = rank(M_A) = (6-f)/2 + 2f,

forcing f=2. This recovers the remaining right-action trace used by the
previous module enumeration without assuming the old g-column of F.

All hypotheses of `../new_frontier/cyclic8_morita_exclusion.md` now follow
without a hypothetical restriction map. Its complete six-object module
enumeration leaves two types; condensation transforms the second to the
first, and the second available algebra 1+alpha rho contradicts the exact
small-algebra square test. Therefore C cannot exist in this actual Morita
class.

`actual_cyclic8_morita.py` checks the forced support, actual source dimensions,
all trace inputs and the fixed-point equation using integers. It relies on
the already verified full-Morita and second-algebra certificates for the
final contradiction.

Primary references: Etingof–Nikshych–Ostrik, *On fusion categories*, Theorem
2.15 (dimension of the dual category) and Proposition 8.23 (canonical
positive spherical structure), <https://arxiv.org/abs/math/0203060>;
Ostrik, *Pivotal fusion categories of rank 3*, Theorem 2.13,
<https://arxiv.org/abs/1309.4822>; Grossman–Izumi, *Drinfeld centers of fusion
categories arising from generalized Haagerup subfactors*, Theorem 6.8 and
Example 6.10, <https://ems.press/content/serial-article-files/36923>.

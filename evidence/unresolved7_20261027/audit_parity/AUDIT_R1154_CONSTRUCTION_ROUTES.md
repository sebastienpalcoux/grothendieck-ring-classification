# Independent audit: R1154 integral center and Haagerup-product routes

**Verdict: both structural arguments pass. Neither excludes R1154.**

I reviewed `../r8_1154/INTEGRAL_CENTER_OBSTRUCTION.md` and
`../r8_1154/HAAGERUP_PRODUCT_ROUTES.md`, including their categorical
premises, and replayed `verify_integral_center.py` successfully.

## Integral center

Positivity of the irrational coefficient of every noninvertible FP
dimension forces an integral-dimensional central simple to restrict to
m copies of 1 and n copies of g. Centrality of its class and the explicit
noncommutation gX1=X7, X1g=X6 force n=0. Half-braidings on sums of the unit
are representations of the universal grading group. Full adjoint closure
therefore makes such an object a sum of central units. A central simple
must be the unit. These arguments require no spherical or unitary premise.

I checked ENO, *Weakly group-theoretical and solvable fusion categories*,
https://arxiv.org/pdf/0809.3031, Theorem 1.3, directly: its equivalence
between a group-extension Morita class and a Tannakian subcategory in the
center is exactly the statement used. The corresponding central Rep(G)
in an equivariantization also gives the claimed obstruction. For the
rank-ten auxiliary category, the integral center is the pointed semion
double; its only nontrivial Tannakian subcategory is the bosonic C2.

## Product construction families

All dimensions in the quotient calculation are Frobenius–Perron
dimensions. No positivity of a particular categorical pivotal structure
is required. Noninvertible simple dimensions in the three products have
strictly positive phi coefficient, so rational-dimensional A has pointed
support.

For a connected separable algebra, the regular right module is simple.
For every supported invertible g, multiplication gives a nonzero map
gA to A and hence an isomorphism. Adjunction proves multiplicity one;
the stabilizer description proves the support is a subgroup. Multiplying
the corresponding isomorphisms also shows that products of supported
homogeneous summands are nonzero, so the subgroup pieces are the usual
twisted group algebras and remain separable in characteristic zero.

The first two dimension/index contradictions are immediate. For the
third, the first C4 factor K is central in the pointed product group J.
Thus KL is a subgroup and [KL:L] divides both 4 and 3, implying K is
contained in L. The restriction of the half-braiding to A_K is justified:
the full pointed group acts freely on every simple in GH(C4,1) tensor
GH(C4,1) tensor P. For g in the first factor, the unique h with gX=Xh
lies in the same factor (g or its inverse). Consequently no matrix entry
of the half-braiding can mix the K support with its complement. Naturality,
the hexagon, and central commutativity restrict to A_K.

Modules over this connected separable central commutative A_K form a
fusion category, with free induction a tensor functor. The right K-orbit
of rho is free, so adjunction gives End(rho A_K)=C. Every g in K induces
to the tensor unit. The simple image x is noninvertible and satisfies
x squared = 1 + 4x, hence generates a rank-two fusion subcategory.

I checked Ostrik, *Fusion categories of rank 2*,
https://arxiv.org/pdf/math/0203255, Main Theorem, directly. It excludes
all coefficients at least two for arbitrary complex fusion categories,
so its use here does not assume unitarity or a classification of spherical
generalized Haagerup categories.

The arguments rule out precisely the stated direct central-algebra
construction families, including arbitrary pointed factors and allowed
associators. Noncentral bimodule Morita constructions, other factors,
and arbitrary chains of operations are outside this conclusion. The
classification status of R1154 remains unresolved.

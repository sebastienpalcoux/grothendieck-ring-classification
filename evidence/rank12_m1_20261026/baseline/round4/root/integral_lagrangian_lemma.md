# Integral Lagrangians and the dimension-48 converse

Status: independently accepted by the exclusion and model audit agents.
No ledger decision is made by this file alone: the quotient binding and all
alternative central branches must also be checked for each original ring.

## Square class of a pointed Morita module

Let P=Vec(G,omega). A Lagrangian subcategory of Z(P) corresponds to an
indecomposable P-module category with pointed dual. The usual parametrization
uses a normal abelian subgroup N of G and a permissible G-invariant twisted
alternating bicharacter. The module has |G|/|N| simples, all with normalized
FP dimension sqrt(|N|), when their squares sum to |G|. Call the Lagrangian
integral when |N| is a square.

An invertible P-bimodule category M whose normalized simple dimensions are
integers preserves this subset. To see this, use the linking multifusion
category for M, the module L, and their composite. All endpoint pointed
categories have dimension |G|, so the normalizations agree. If the stabilizers
for M,L,M tensor_P L have orders n0,n,n', respectively, the tensor product of
any two simple objects is a nonzero sum of k simple objects in the composite,
and multiplicativity gives sqrt(n0)*sqrt(n)=k*sqrt(n'). Here k is a positive
integer. Therefore the rational square classes of n and n' agree if n0 is a
square. Applying the inverse M gives preservation in both directions.
The canonical normalization is ENO, Fusion categories and homotopy theory,
Section 2.5, Proposition 2.2: FPdim of an internal Hom is the product of
the two module dimensions. Multiplicativity of the balanced functor is
their Proposition 4.13, with the identical proof for different pointed
endpoints of equal dimension. This is not an assumed normalization of
unrelated Perron vectors.

Consequently, if the set of integral Lagrangians has odd cardinality, any
integral C2-graded extension of P is group-theoretical: its odd component
preserves that odd set, the induced involution fixes a Lagrangian, and the
invariant-Lagrangian extension criterion applies. More generally the same
argument works for any finite 2-group extension all of whose components are
integral.

## The two groups of order twenty-four

For G=A4 x C2, the only normal abelian subgroups of square order are 1 and
the normal V4 in A4. The trivial subgroup contributes one Lagrangian.
For V4, if a permissible invariant twisted alternating bicharacter exists,
the complete set is a torsor under the ordinary invariant alternating
bicharacters. There are two of these: the trivial form and the unique
nontrivial symplectic form, both invariant under G. Hence V4 contributes
either zero or two Lagrangians. The integral subset has cardinality one or
three, for every omega; no splitting assumption on omega is made.

For G=SL(2,3), the only normal abelian subgroups are 1 and its central C2.
Only the first has square order. Thus the integral subset has cardinality
one for every omega. Both groups therefore satisfy the preceding criterion.

## Use for the two rank-twelve dimension-twenty-four quotients

The separate quotient proofs establish group-theoreticity for every
categorification of R12_1_351 and R12_1_513, by an invariant Lagrangian for
their C3 extension of the pointed adjoint category of dimension eight.

Perform the graded Morita construction using its actual algebra in that
neutral pointed category. The resulting entire category is pointed,
Vec(Gamma,Omega), with a normal subgroup A of order eight and Gamma/A=C3.
Schur-Zassenhaus gives Gamma=A semidirect C3. Only A=C2^3 or Q8 admits a
nontrivial order-three automorphism; the nontrivial semidirect products are
A4 x C2 and SL(2,3).

If the action is trivial, Gamma=A x C3 and coprime Kunneth splits Omega
as the product of its two restrictions. The inverse algebra lies in the
neutral Vec(A) factor. Thus its dual is the neutral dual tensor Vec(C3).
That neutral dual is the original pointed adjoint category; the original
full category would be pointed, contradicting its four dimension-two
simples. So this case cannot occur.

Finally let C be an integral C2-equivariantization of either quotient D.
It is Morita equivalent to the integral crossed product D crossed C2.
Condensing an actual algebra in its neutral component, presenting the above
pointed Morita equivalence of D, gives a C2-graded category with neutral
Vec(Gamma,Omega). The whole dual is integral. Explicitly, if C is integral,
the forgetful functor makes every simple of Z(C) have integer FP dimension.
For any Morita equivalent D, the braided equivalence Z(D)=Z(C) and
FPdim(I_D(X))=FPdim(D)*FPdim(X) then show that FPdim(X) is rational.
It is an algebraic integer, hence an integer. This proves the needed
Morita invariance without assuming that tensor functors preserve simple
objects. The preceding odd-set theorem then makes
the extension, and hence C, group-theoretical.

This final step is essential: an equivariantization of a group-theoretical
category is not group-theoretical in general.

References: Gelaki--Naidu--Nikshych, Centers of graded fusion categories,
Corollaries 3.10--3.11; the normal-abelian-subgroup description of Lagrangian
subcategories of twisted finite-group doubles; normalized dimensions in
invertible module categories / linking multifusion categories.

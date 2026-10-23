# Independent audit of the rank-six central-boson reduction

**Accepted, conditional on the separately proved reduction to the
Jordan–Larson dimension-12 extensions.** This note checks the categorical
step that allows a different central involution to be used in dimension
48. It does not replace that initial reduction or the finite input check
identifying the alternative quotient as near-group.

Let E be a C3 extension of Vec(V4) with simple dimensions `(1^4,2^2)`,
and let B=E^C2 have profile `(1^4,2,4)`. The nontrivial C2 functor exchanges
the two nonzero C3 degrees. Put K=E⋊C2. The products XX* for dimension-2
simples are the sum of all four neutral invertibles. Invertibles contribute
only the tensor unit to the adjoint subcategory. Consequently
K_ad=Vec(V4), and the evident faithful S3 grading is its universal grading.

Every central invertible of K has universal degree in Z(S3): its
half-braiding identifies its products with objects in every homogeneous
component in both orders. Since Z(S3)=1, its underlying object lies in
Vec(V4). Restricting its half-braiding gives an element of
Inv Z(Vec(V4))=V4×V4^*=F2^4. Such an element is fixed by the C3
Brauer–Picard action, by compatibility with the two nonneutral components.

Write q(a,chi)=chi(a) additively in F2. The twist is (-1)^q. The canonical
positive pivotal structure on K restricts to the standard one on Vec(V4),
so this formula is also the twist of the restricted central invertible.
This observation uses actual twist compatibility, not just invariance of
an abstract bilinear form.

In the two Jordan–Larson classes the triality fixed spaces are, in the
coordinates of `work/resolve_rank9_integral/d12_normalizers.json`,

| Representative rows | Fixed space | q on nonzero fixed vectors |
| --- | --- | --- |
| (4,12,15,6) | {0,7,10,13} | 1,1,1 |
| (8,4,6,9) | {0} | none |

These calculations were independently checked directly by binary matrix
multiplication. All six matrices in their parabolic-conjugacy/inversion
orbits have no nonzero isotropic fixed vector. Thus every central boson
of K restricts to the tensor unit with its trivial neutral half-braiding.

The kernel of restriction consists of central structures on the tensor
unit that are trivial on K_ad. It is exactly
Aut_tensor(Id_K)=Hom(U(K),C*)=Hom(S3,C*)=C2. Both elements have twist one.
Hence K has exactly one nontrivial central boson, the grading sign.
There may be other central invertibles of twist minus one; their possible
existence does not affect this conclusion.

The canonical Morita equivalence between E^C2 and E⋊C2 gives a braided
center equivalence. For these unitary, equivalently pseudo-unitary,
categories it preserves the canonical positive ribbon structure. Therefore
B likewise has exactly one nontrivial central boson. The canonical central
Rep(C2) from the equivariantization supplies that boson, with underlying
object the nontrivial sign of B.

Now suppose C=B^C2. The induced action on Z(B) must preserve its unique
nontrivial boson, and therefore the full central Tannakian subcategory
Rep(C2). Its equivariantization embeds fully faithfully as a central
symmetric fusion subcategory of C of dimension four. It is Tannakian:
forgetting the equivariance, and then using the ordinary symmetric fiber
functor on Rep(C2), gives a symmetric fiber functor to Vec. It is thus
Rep(G) for a group of order four.

All four simple objects are invertible, and forgetting the center embeds
them as the four invertibles of the input ring. That group is V4, so
G=V4, rather than C4. In particular all three nonidentity invertibles of C
have compatible central bosonic structures. Any of them may be used for
C2 de-equivariantization. The separate input orbit-profile calculation
selects one with the already resolved near-group quotient.

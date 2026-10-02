# Independent audit of the R53/R93 exclusion

The proposed general complex exclusion is mathematically sound, after the two
clarifications below. No pivotal or unitary hypothesis is used. This audit is
independent of the proof author.

1. In the dimension-18 descent, the adjoint category cannot have dimension 2
   because each product `ZZ*` contains a 2-dimensional simple constituent.
   Its *total object dimension* being 4 would not, by itself, prove this.
2. The composition of equivariantizations can be replaced by an explicit
   central construction. Let `R=Rep(C2)` be the canonical central subcategory
   of `Z(E)`. The outer action preserves its unique half-braiding. Its
   equivariantization `R^{C2}` embeds fully into `Z(E^{C2})`: the original
   half-braiding is equivariant and therefore is a half-braiding on every
   equivariant object. This category is symmetric, has dimension 4, and
   has a fiber functor obtained by forgetting equivariance and then using
   the fiber functor on R. Thus it is `Rep(H)` for a group of order 4.
   Its four invertibles exhaust `Inv(D)=C4`, forcing `H=C4`. Directly
   de-equivariantizing D by this central subcategory gives a fusion category
   of dimension 9, necessarily pointed. No identification with an earlier
   de-equivariantization, nor an unquoted composition theorem, is needed.

The two-prime solvability descents, the orbit dimension formula, and the
dimension-18 universal grading exclusions have all their hypotheses. A
half-braiding on an invertible differs from another one by a tensor
automorphism of the identity, so `U(E)=1` gives the required uniqueness.
The pointed group of order 9 is `C3^2`: a free C4 action cannot occur on C9.
The C4 generator acts irreducibly with square `-I` over F3.

The general extension lemma also survives the twisted pointed case. In the
identity double coset the projective cocycle is the quotient of the same
subgroup cochain with itself (all normalized omega terms are 1), so its
representations are ordinary. A pointed dual forces a normal abelian left
stabilizer N. The homogeneous component has `|G:N|` simple objects of equal
dimension; its total squared dimension is `|G|`, hence each dimension is
`sqrt(|N|)`. The semidirect product `C3^2 ⋊ C4` has only the normal abelian
subgroups 1 and `C3^2`. These give dimensions 1 and 3.

Morita transport concerns the complete grading data, including tensor
products and associators, rather than just individual module categories.
ENO's Brauer--Picard groupoid construction supplies this transport and a
Morita equivalence of the resulting complete extensions. Integrality is
Morita invariant here: an integral category has integral center; induction
of a simple W in a weakly integral Morita equivalent category has dimension
`FPdim(C) FPdim(W)`, which is integral. Therefore `FPdim(W)` is rational
and an algebraic integer, and hence integral.

Thus every extension of the dimension-36 neutral category is integral,
contradicting the two census dimensions `3sqrt(2)`.

Primary documents independently consulted: ENO, *Fusion categories and
homotopy theory*, https://arxiv.org/html/0909.3140v2, Sections 2.5, 3.6,
4.1--4.2 and Theorem 1.3; Gelaki--Naidu, *Some properties of
group-theoretical categories*, https://arxiv.org/pdf/0709.4326, the general
twisted double-coset dimension formula. The exact independent checker
`verify_r53_r93_independent.py` checks the source bindings, full ring axioms,
grading, neutral tensor, and all fixed-point-free order-four matrices in
`GL(2,3)`; normal and optimized receipts accompany it.

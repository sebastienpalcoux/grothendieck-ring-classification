# Independent categorical review: a cyclic generalized-Haagerup Morita construction

This review checks the categorical steps separately from the finite fusion-ring
identification. It does not infer a category from modular data.

## A uniform statement

Suppose a generalized Haagerup category for the cyclic group C_(4m), m >= 1,
has the explicit realization of Grossman--Izumi, arXiv:1501.07679v2,
Section 6, with epsilon_(2m)(j)=(-1)^j, and the Q-system 1+rho of
equation (2.21). Let C be its C2 de-equivariantization, let r be the image
of rho, and let A=1+r be the image Q-system. Then the fusion category
of A-bimodules in C has no nontrivial invertible simple object.

These are assumptions on an existing category; the statement does not assert
existence of a generalized Haagerup category for every m.

The simples of C are g^j and g^j r, j modulo 2m. Their dimensions are 1
and d=2m+sqrt(4m^2+1), and g^j r=r g^(-j). A is connected and separable
because the de-equivariantization is a tensor functor and r remains simple.
The dual category therefore exists.

If an A-bimodule M is invertible, its underlying dimension is dim(A)=1+d.
Irrationality of d forces its underlying object to be exactly g^j+g^k r.
Adjunction from the summand g^j gives nonzero maps to M from the free simple
left and right modules A g^j and g^j A. Simplicity follows from
End_A(A g^j)=Hom_C(g^j,A g^j)=C, and similarly on the right. Equal dimensions
make both maps isomorphisms. Comparing supports forces k=j=-j modulo 2m.
Consequently j is 0 or m.

For j=0, the bimodule is A with one action twisted by an algebra
automorphism. Such an automorphism is scalar z on r and identity on 1.
The nonzero multiplication components r r -> 1 and r r -> r imply
z^2=1 and z^2=z. Thus z=1 and this is the tensor unit.

For j=m, existence would require an algebra isomorphism between A and
g^m A g^(-m). More explicitly, the left action gives a unital algebra map
from A to the internal end of the free right module g^m A. This target
is g^m A g^(-m). A connected separable algebra is simple as an algebra
(its bimodule endomorphism space embeds in Hom(1,A)); hence this map is
injective. Equal dimensions make it an isomorphism.

Section 6 realizes the de-equivariantization in End(M crossed C2), with
lambda^2=1, r(lambda)=lambda, and alpha'_(2m)=Ad(lambda).
Conjugation beta by alpha'_m sends r to Ad(lambda) r. The intertwiner
u=lambda from r to beta(r) has u tensor u=1. The original nonzero
r -> r^2 Q-system vertex lies on the t_0 line. Transporting beta(A) back
to 1+r sends this line to alpha'_m(t_0) lambda=t_(2m) lambda.
The Cuntz isometries make these lines orthogonal. An isomorphism of algebras
on 1+r is scalar on r, so cannot identify these lines. This rules out j=m.

## Application at m=2

The GH(C8) example in Grossman--Izumi, Example 4.4, satisfies (2.22), hence
(2.21). Its de-equivariantization and center are described in Section 6
and Example 6.10. Thus the preceding lemma applies to an existing unitary
category and an existing Q-system.

The complete free-bimodule Gram enumeration in
`../semion_fermion/construction/r721_bimodule_rank.py` permits ranks
6, 8, 9 and 11. Its rank-six alternative has two invertibles, so the
uniform lemma eliminates it. The complete twist-one S-fixed-vector
calculation for the known center permits ranks 6, 8 and 10; hence the
actual dual must have rank eight.

The independent rank enumeration was replayed during this review. The
positive-semidefinite inequality used to enumerate its restriction rows
is necessary for every Gram summand, and all subsequent multiplicity
boxes are finite and exhaustively checked. The identity
rank(B)=dim End(I_B(1)) follows from induction/forgetful adjunction and
F I_B(1)=sum_X X X*. Thus the center rank calculation applies to the
actual dual, not merely to a putative modular-data realization.

The full fusion-ring identification still requires the exact coefficient
bound and the complete census comparison in the model and R721 folders.
This review endorses the actual category, the uniform invertible-object
lemma, and the forced rank-eight restriction data; these steps do not use
census completeness or a multiplicity assumption.

## Primary source locations checked

- Grossman--Izumi, arXiv:1501.07679v2, equations (2.18)--(2.22), printed
  pages 13--14: isometries, their action, and the inherited Q-system.
- Section 2.5.1, printed page 15: crossed-product extension and the tensor
  de-equivariantization.
- Section 6, first paragraph, printed page 37: lambda, the extended
  endomorphisms, irreducible labels, and alpha'_m(t_0)=t_(2m).
- Example 4.4 and Example 6.10: the existing C8 example and its center.

No claim is made that this identification is the first in the literature.

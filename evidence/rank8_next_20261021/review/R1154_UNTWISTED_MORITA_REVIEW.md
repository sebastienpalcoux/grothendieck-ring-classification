# Independent review of the untwisted C2 Morita obstruction

The conclusion is conditional but categorical: a categorification of
R8_3_1154 cannot have trivial pointed associator on its subgroup C2.
This does not exclude the nontrivial associator class or the source ring.

Let g be the nontrivial invertible. If its associator class is trivial,
A=1+g has its usual connected separable group algebra structure. A-bimodules
are the equivariant objects for the commuting left and right C2 actions on
the underlying semisimple category. This is an action by linear equivalences;
no assertion that left tensoring is a tensor autoequivalence is needed.
The elementary orbit/stabilizer proof of the equivariant-simple classification
applies. Its projective stabilizer representations encode all possible
coherence scalars, so these scalars have not been silently set to one.

The three double orbits, verified in the source tensor, have sizes 2,2,4:
{0,3}, {4,5}, {1,2,6,7}. Their stabilizers are C2,C2,1. Since
H^2(C2,C*)=0, they contribute respectively 2,2,1 simples to the dual.
Their dimensions, after division by FPdim(A)=2, are
1,1,a,a,2a+2, where a=6+3 sqrt(5) and a^2=12a+9.

Write these objects as 1,u,x,x',y. The nontrivial character bimodule u
has order two. Twisting either stabilizer action by its character exchanges
the two projective characters on the second orbit. Thus ux=xu=x',
ux'=x'u=x and uy=yu=y. In particular u is central in the dual ring;
this is derived from the bimodule action and is not an assumed braiding.

Here is an independent check that the proposed dual list is exhaustive.
The unique dimension of y implies y*=y. Either x*=x and x'*=x', or
x*=x'. Dimension comparison in the basis (1,a), together with the
unit and u coefficients from duality, first gives

- xy has y coefficient 9 and total x,x' coefficient 8. Since multiplication
  by u fixes xy, its x and x' coefficients both equal 4. The same applies
  to yx.
- y^2 has coefficients 1 on 1,u; its y coefficient is 19 and its x,x'
  coefficients are both 9.
- Each of x^2,xx',x'^2 has y coefficient 4, total x,x' coefficient 4,
  and exactly one of 1,u. Multiplication by u determines all three
  products from x^2. Frobenius reciprocity in the nonselfdual case forces
  the two remaining coefficients to be 2 and 2.

Hence there are five selfdual labelled choices m=0,1,2,3,4 and one
nonselfdual choice m=2. Swapping x and x' identifies m with 4-m in
the selfdual cases, leaving exactly the four isomorphism types used in
`models/rank5_dual_exclusions.json`. There is no unexamined noncommutative
dual: all products above are forced to commute.

The root review reran `models/verify_rank5_duals.py` against the complete
125-entry tensors and the existing general-complex signed-extension
certificates. All four exclusions passed. Thus the dual cannot exist,
contradicting the existence of A. In a pseudo-unitary realization the
remaining nontrivial pointed associator class has nu_2(g)=-1.

Primary background for the orbit/stabilizer argument is Burciu--Natale,
*Fusion rules of equivariantizations of fusion categories*, Corollary 2.13,
https://arxiv.org/abs/1206.6625. The application to the linear C2-by-C2
action above uses its semisimple orbit argument, not its tensor-functor
dimension formula: bimodule dimensions are normalized separately by 2.

# Independent categorical audit: R9_2_746 and R9_2_1209

24 October 2026. Audited construction: `../weak_a/CYCLIC_TY_MODELS.md`.
Conclusion: **both unitary constructions pass** the categorical and exact
fusion-tensor audit. No categorical existence is inferred from a bare based-ring
match. No online publication was performed.

## Half-braiding orientation and the TY factor

I checked the explicit associators in Gelaki–Naidu–Nikshych,
*Centers of graded fusion categories*, arXiv:0905.3117v1, Section 4.1,
and its Section 2.2 convention for the center. The construction consistently
uses right half-braidings `c_h(V): h⊗V→V⊗h`, the inverse of that
section's displayed central-structure convention. This distinction is necessary.

Let `χ(a,b)=ω^{ab}` on C3. The proposed right half-braiding on an invertible
`h` is `c_h(b)=χ(h,b)`, `c_h(m)=κ_h`, where
`κ_0=1`, `κ_1=κ_2=ω`. The right half-braiding hexagon is

`c_h(U⊗V)=α_{U,V,h}^{-1}(id_U⊗c_h(V))α_{U,h,V}(c_h(U)⊗id_V)α_{h,U,V}^{-1}`.

Substitution of the TY associators checks every case. When `U=V=m`,
the component indexed by `b` gives
`κ_h² χ(h,h+b)=χ(h,b)`, exactly `κ_h²=χ(h,h)^{-1}`.
The other three parity patterns use only bicharacter multiplicativity or
cancellation of `χ(h,b)` and its inverse. Tensoring central objects gives

`κ_{h+k}=κ_h κ_k χ(h,k)^{-1}`.

The proposed κ-values satisfy this at all nine pairs. Hence the central
lift z of1 has order3, not order6, and self-braiding `ω`. Inversion of
C3 preserves χ, gives the actual tensor action of GNN Proposition 4.8,
and sends `(1,κ_1)` to `(2,κ_2)=z²` with the asserted identity tensorator.

## Pointed factor and central algebra

Independently checked over exponents modulo9:

* all 6561 equations for the pointed3-cocycle `Ω`;
* all 729 monoidal-inversion equations and 81 square-coherence equations;
* right half-braiding hexagons for all three powers of the central lift of3;
* tensor multiplication of all central powers, including the cube;
* transport of every central power under inversion;
* triviality of the associator and inversion tensorator on all powers of g;
* triviality of every pairwise braiding among the powers of g.

In particular, for powers `g^r,g^s`, the total right-braiding exponent is
`3rs+2r(3s)=9rs`, so every such braiding is1. This checks the full central
Tannakian subcategory, rather than using only a single self-braiding as a
proxy. Ordinary multiplication on `A=1⊕g⊕g²` is therefore associative and
commutative as a central algebra; the standard finite-group separability
normalization is positive. Inversion preserves this actual central algebra,
with square identity. There is no omitted algebra-equivalence coherence.

## Descent and the decisive fusion-line sign

De-equivariantization by this central unitary algebra gives a unitary fusion
category D. The group-algebra permutation `g^r↦g^{-r}` supplies an
involutive equivariant algebra structure; therefore inversion descends as a
coherent unitary action on D. The parity natural automorphism is monoidal,
inversion invariant, and identity on A, so multiplying the square coherence
by parity gives the second coherent action.

The free-module functor `H:B→D` is a monoidal functor equipped with the
inversion comparison induced by this equivariant algebra structure. The
fixed simples of D admit inversion-fixed representatives `(0,0)` and
`(m,0)` in B. Their canonical equivariant structures are induced from
identity maps on these representatives. Therefore the fixed line
`Hom_D(H(m,0)⊗H(m,0),1)` is the image of the fixed parent line
`Hom_B((m,0)⊗(m,0),(0,0))`; it has eigenvalue+1 because the parent
inversion tensorator at this pair is identity. The other two summands of
`(m,0)²` become distinct invertible D-simples that inversion exchanges.
No extra unidentified descent phase can enter the unit-channel line.

For the parity-twisted action the equivariant maps on the fixed odd
simple have eigenvalues `±i`. Two such factors contribute `i²=-1` to
that same unit-channel trace. When just one input and the output are odd,
the factors cancel. This is precisely the single additional sign in the
proposed orbit/trace formula. For a moving input orbit, inversion exchanges
its input-labelled summands, so the trace is zero, irrespective of the
phases on those off-diagonal maps.

## Independent exact tensor reconstruction

The independent verifier does not import the proposed generator. It starts
with all 36 simple objects `(a,c)` of `TY(C3)⊠Vec(C9,Ω)`, enumerates the
12 orbits of tensoring by g, and constructs the rank12 tensor from the
parent products. It then constructs both equivariantized tensors from
fixed and moving orbits with the independently justified signs above.
Both 729-coefficient comparisons against the original census tensors pass.

The code uses explicit exceptions, so checks remain active under Python-O.
Receipt: `cyclic_ty_audit.json`; replay: `verify_cyclic_ty.py`.
The source-to-model permutations are

* R9_2_746: `[0,1,6,7,2,5,3,8,4]`;
* R9_2_1209: `[0,6,7,2,5,3,8,1,4]`.

These are unitary categorifications, not claims classifying all tensor
categories with either ring, and not claims of novelty up to tensor equivalence.

Primary source independently opened:
https://arxiv.org/pdf/0905.3117
(Sections 2.2, 2.4, 2.5, 4.1 and Proposition 4.8).

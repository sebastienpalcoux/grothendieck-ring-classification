# A unitary model for R10_1_189

## The categorical construction

Let C be the unitary WZW modular category SU(4) at level 6, and let B be
the connected commutative separable algebra supplied by the conformal
embedding SU(4)_6 ⊂ SU(10)_1. In Dynkin labels,

    B = (000) ⊕ (060) ⊕ (202) ⊕ (222).

This is an actual algebra from a conformal inclusion, not an algebra whose
existence is inferred from a modular invariant. Bockenhauer–Evans,
*Modular Invariants from Subfactors*, arXiv:math/0006114v2, p.29, explicitly
construct the inclusion and give its dual canonical endomorphism as this
vacuum block. The same page lists all ten branching rules.

Put D=C_B, the fusion category of right B-modules with tensor product over
B. Let F:C→D be the free module tensor functor, and let v=(010). The
local-module subcategory C_B^0 is SU(10)_1. Its ten simples are invertible;
write them τ_j, j∈Z/10, with τ_i τ_j=τ_(i+j).

The free module functor F is central. In particular F(v) commutes, by its
categorical half-braiding, with every τ_j. Set

    β = F(v),     g = τ_2,     x = τ_5 β.

The full subcategory on the ten objects

    1,g,g²,g³,g⁴, x,gx,g²x,g³x,g⁴x

is closed under tensor products, direct summands and duality, as proved
below. It is therefore an actual unitary fusion subcategory of D. Its
Grothendieck ring is R10_1_189.

## Exact branching calculation

Let U:D→C be the forgetful functor. The ten objects U(τ_j), in the
orientation of Bockenhauer–Evans, are

| j | Dynkin labels of the summands of U(τ_j) |
|---|---|
|0|000,060,202,222|
|1|002,240,212|
|2|012,230,303|
|3|103,321,030|
|4|004,420,121|
|5|006,600,022,220|
|6|400,024,121|
|7|301,123,030|
|8|032,210,303|
|9|200,042,212|

The tensor powers needed here lie strictly below the level-six affine
wall, so the ordinary SU(4) Pieri rule gives the WZW fusion products:

    v² = (000) ⊕ (020) ⊕ (101),
    v³ = 3(010) ⊕ 2(111) ⊕ (030) ⊕ (200) ⊕ (002).

These two identities are independently reproduced by the verifier using
the vertical-two-strip Pieri rule, rather than entered as a presumed
fusion result.

Frobenius reciprocity and the projection formula give

    dim Hom_D(β, τ_j β)
      = dim Hom_C(v, U(τ_j)⊗v)
      = dim Hom_C(v², U(τ_j))
      = δ_(j,0).

Consequently β is simple and its ten τ_j-translates are pairwise
nonisomorphic. Similarly,

    dim Hom_D(β², τ_j β)
      = dim Hom_C(v³, U(τ_j))
      = 1 for j∈{1,3,7,9}, and 0 otherwise.

Also the tensor unit occurs once in β². No assertion about the other
objects of D is needed.

The quantum Weyl dimension formula gives

    FPdim(β) = [4][3]/[2] = φ³ = 2+√5 = d,

where φ=(1+√5)/2 and [n]=sin(nπ/10)/sin(π/10). Indeed [4]/[2]=φ and
[3]=φ². Since d²=1+4d, the unit and the four simple summands just found
exhaust the FP dimension. Thus

    β² = 1 ⊕ τ_1β ⊕ τ_3β ⊕ τ_7β ⊕ τ_9β.

This is an equality in an existing fusion category, not merely a
dimension-compatible proposed fusion rule.

## The rank-ten fusion ring

The object v is self-dual, and F preserves duality. Thus β is self-dual.
Since τ_5 has order two and commutes with β, x=τ_5β is self-dual. The
object g has order five and commutes with x. Moreover x²=β², and

    {τ_1β,τ_3β,τ_7β,τ_9β} = {gx,g²x,g³x,g⁴x}.

It follows that

    g⁵=1,      gx=xg,      x*=x,
    x² = 1+(g+g²+g³+g⁴)x.

The five invertibles and five dimension-d objects are distinct, and these
relations show closure of their span under products and duality. They
therefore define the promised full fusion subcategory. In particular this
proves a unitary categorification, and hence a complex categorification.

The source census tensor is identified coefficientwise with this ring by
the basis permutation

    (1,g,g²,g³,g⁴,x,gx,g²x,g³x,g⁴x)
      ↦ (0,1,8,7,2,9,4,6,5,3).

`verify_conformal_model.py` checks all 1000 structure constants, all ten
branching intersections, the independent Pieri calculation and the exact
dimension identity. It retains the tensor hash and primary source. Its
finite checks complement the categorical construction above; they are not
substituted for existence of the algebra or its module category.

## References and scope

1. J. Bockenhauer and D. E. Evans, *Modular Invariants from Subfactors*,
   arXiv:math/0006114v2, §7, p.29: actual conformal inclusion, vacuum algebra
   and full branching rules.
   https://arxiv.org/abs/math/0006114
   https://orca.cardiff.ac.uk/33657/1/Bockenhauer%202000.pdf
2. R. Coquereaux and G. Schieber, *Quantum symmetries for exceptional SU(4)
   modular invariants associated with conformal embeddings*,
   arXiv:0805.4678, §§1.4.3–1.4.5: independent construction and branching
   for SU(4)_6⊂SU(10)_1.
   https://arxiv.org/abs/0805.4678
3. The standard connected-étale-algebra theory in a nondegenerate braided
   fusion category supplies C_B and its free central tensor functor.
   See Davydov–Muger–Nikshych–
   Ostrik, *The Witt group of non-degenerate braided fusion categories*,
   §3, arXiv:1009.2117.

No inference from the previously found rank-fourteen modular data is
needed for the existence proof. Those data motivated recognition of the
conformal-embedding construction; the proof stands independently of
their completeness or reconstruction.

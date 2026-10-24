# A unitary cyclic Moore–Read orbifold realizing R9_2_389

This is a categorical construction followed by an exact full multiplication-tensor identification. It does not infer categorifiability from fusion-ring automorphisms alone.

## Construction and coherence

Let I be a unitary Ising category, with simples 1, ψ, σ, ψ²=1, ψσ=σ and σ²=1+ψ, and choose its usual braided central lift of ψ. Its self-braiding is −1. Put ζ=exp(2πi/16), and let P=Vec(C16,ω), where representatives a,b,c lie in {0,...,15} and

ω(a,b,c)=ζ^(2a floor((b+c)/16)).

Let D be the full fusion subcategory of I⊠P with simples (1,a),(ψ,a) for even a, and (σ,a) for odd a. Thus FPdim(D)=32. This is an ordinary parity subcategory of two existing unitary fusion categories.

The inversion functor F on P, F(a)=−a, has tensorator F(a)⊗F(b)→F(a+b) given by

J(a,b)=ζ^μ(a,b),  μ(a,b)=−2a·1_(b>0) modulo16.

Its tensor-functor pentagon is precisely

μ(a,b)+μ(a+b,c)−μ(b,c)−μ(a,b+c)
=w(−a,−b,−c)−w(a,b,c) modulo16,

where w is the exponent of ω. The formula satisfies this identity. Moreover μ(a,b)+μ(−a,−b)=0 modulo16, so F²=Id as a tensor functor and the identity coherence defines a genuine C2 action. Extend F by the identity on I; this preserves D. All structure maps have modulus one.

Inside Z(D), consider g=(ψ,8), with the product of the Ising half-braiding and the pointed half-braiding β(a)=ζ^(7a). The slant cocycle at8 is trivial, so this character gives a central lift. The central tensor square includes the pointed associator correction ζ^(2a):

β(a)² ζ^(2a)=ζ^(16a)=1.

Thus g has order two in Z(D). Its self-braiding is

(−1)β(8)=(−1)ζ^56=1.

It therefore generates a central Tannakian Rep(C2), and A=1⊕g is its regular commutative separable algebra. Inversion preserves this central lift: the central-transport equation is

μ(8,−a)−μ(−a,8)=14a modulo16,

which follows immediately from the displayed formula. Also μ(8,8)=0. Consequently the identity equivariant structure on g preserves the algebra multiplication and its central half-braiding; A is a central commutative separable algebra in D^C2.

Define E=(D^C2)_A, the category of right A-modules with tensor product over A. This is a unitary fusion category of dimension64/2=32. Equivalently it is the inversion equivariantization of the dimension16 generalized Moore–Read category D_A. Either choice of sign for the equivariant structure on g gives the same based ring in this construction.

## Exact fusion rules and census identification

The C2 action on the 24 simples of D fixes four invertibles and has ten other orbits: six pointed orbits and four nonpointed orbits. Thus D^C2 has eight invertibles, six dimension2 objects and four dimension2√2 objects. Tensor multiplicities are obtained by the usual invariant-subspace formula (dimension+trace)/2 on fixed output simples. A trace contribution can only come from fixed input simples; those are all pointed, and the closed-form tensorator restricts to1 on them.

The chosen equivariant g acts freely on all18 simple objects of D^C2. Therefore the simple A-modules are its nine orbits. For chosen orbit representatives X,Y and an output orbit {Z,gZ}, their tensor multiplicity is exactly

N_(X,Y)^Z + N_(X,Y)^(gZ).

The independent constructor `mr_orbifold.py` applies these formulas, verifies all fusion-ring axioms, and compares every one of the 9³ multiplication coefficients. It produces R9_2_389 with source-to-model basis permutation

`[0,5,6,2,4,1,8,7,3]`.

The final dimensions are 1⁴,2³,(2√2)², and the largest fusion coefficient is2. The exact tensor, labels, central-boson index and quotient orbits are recorded in `mr_models.json`; the closed-form action is recorded and independently checked in `mr_inversion.py` and `mr_inversion.json`.

## Family variation and limits

The same construction works with cocycle class p=2,6,10,14 and central character j=−p/2 modulo8. The involutory cyclic automorphisms r=7,15 preserve the central lift. An explicit tensorator is μ(a,b)=−pr a floor(rb/16) modulo16. `mr_variants.py` exhausts its coherent-square choices and the two boson equivariant signs: all32 resulting rank9 tensors match389. The other involutory cyclic automorphisms1,9 have the wrong orbit profile for rank9. Changing the Ising associator parameter does not change these traces, since fixed input objects are pointed. This is a bounded family scan, not a classification of all C2 actions on all Moore–Read categories.

No result is claimed here for1025,1254,1709,1759 or1988. In particular, the order-four cyclic automorphisms do not automatically descend to coherent C2 actions after condensation.

## Primary references

J. Dong, S. Natale and H. Sun, *A class of prime fusion categories of dimension 2^N*, New York Journal of Mathematics27(2021), 141–163, Theorem5.2 and its proof, https://nyjm.albany.edu/j/2021/27-5p.pdf. This provides related generalized Moore–Read constructions; the existence and action used above are also explicit here.

S. Gelaki, D. Naidu and D. Nikshych, *Centers of graded fusion categories*, Algebra & Number Theory3(2009), 959–990, Sections2.4–2.5 on equivariantization and central Tannakian de-equivariantization, https://arxiv.org/abs/0905.3117.

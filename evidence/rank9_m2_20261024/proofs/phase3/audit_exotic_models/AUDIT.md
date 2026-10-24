# Independent categorical audit of five rank-nine models

Audit scope: R9_2_389, R9_2_515, R9_2_1857, R9_2_1983 and R9_2_2029.
The conclusion is **accepted unitary categorical models for all five**. This is a
fresh audit of existence, action coherence, central algebras and fusion rules,
not an inference from an earlier PASS flag or from associativity of a candidate
fusion tensor. The checked constructions and their justifications follow.

`replay.py` independently reconstructs all five tensors and compares all 729
coefficients of each with `work/verification_corpus.json`. It imports no phase-two
constructor or stored model tensor. The D4 computation uses two determinants
for the Weyl alternant, independently of the earlier signed-permutation sum.
`replay.json` records basis permutations, hashes and exact checks. Numerical
agreement, by itself, is not the existence argument below.

## 515: a central diagonal-boson quotient

Take the standard unitary Ising category and the even-label subcategory of
SU(2)_10. Their central lifts of ψ and V10 are fermions. Here central means an
object of the Drinfeld center: ψ need not be transparent in the Ising category.
Thus b=ψ⊠V10 has central order two and self-braiding +1. The symmetric pointed
subcategory it generates is Tannakian, and A=1+b is its regular connected
separable central algebra. All A-modules form a unitary fusion category; the
claim does not incorrectly replace all modules by local modules.

The action (i,j)↦(ψi,10−j) on the 18 product simples is free: the only fixed SU2
label could be 5, which is not even. Hence the module category has nine simple
free modules, and its fusion coefficients are the orbit sums of the product
fusion rules. The fresh replay constructs those rules directly from the Ising
rules and SU2 level-ten truncation, then verifies the full tensor for 515.
There is no unproved action lift or fixed-point resolution in this construction.

## 389: explicit coherent inversion and a central boson

Put ζ=exp(2πi/16). On C16, represented by 0,…,15, set

    w(a,b,c)=2a floor((b+c)/16) mod 16,  ω(a,b,c)=ζ^w(a,b,c).

Use the parity subcategory D of Ising⊠Vec(C16,ω): (1,a),(ψ,a) for a even,
and (σ,a) for a odd. It has 24 simples and global dimension 32. Inversion on
the pointed factor is a tensor autoequivalence with tensorator exponent

    μ(a,b)=−2a·1_(b≠0) mod 16.

The replay verifies every one of the 16^4 cocycle pentagons and the 16^3 equations

    μ(a,b)+μ(a+b,c)−μ(b,c)−μ(a,b+c)
      = w(−a,−b,−c)−w(a,b,c).

It also verifies μ(a,b)+μ(−a,−b)=0. Therefore the square of this tensor functor
is the identity with identity comparison map: this is an actual coherent C2
action, rather than an involution only on the simple-object labels. All maps
are unitary scalars.

The degree-eight invertible h has central half-braiding β(a)=ζ^(7a). Its slant
2-cocycle is trivial. Although β^2 alone is not the trivial character, its
central tensor square has the associator correction:

    14a+w(8,8,a)−w(8,a,8)+w(a,8,8)=0 mod 16.

Thus h is centrally of order two, and β(8)=−1. Consequently g=(ψ,8) is a
central order-two boson. Also w(8,8,8)=0, so A=1+g is the usual regular
Tannakian algebra, with nonzero multiplication g²→1.

Compatibility with inversion is essential. Transporting the half-braiding
through the tensorator gives the equation

    14a=μ(8,−a)−μ(−a,8) mod 16,

which is checked for every a. Moreover μ(8,8)=0. Hence the identity equivariant
structure on g preserves both its central structure and its algebra
multiplication. A is a central algebra in D^C2, and (D^C2)_A is a unitary fusion
category of dimension 32.

For the fusion computation, the only inversion-fixed simples of D are the
four pointed simples in degrees 0 and 8. All their relevant tensorator values
are one, so their fixed fusion lines carry the ordinary product of the chosen
sign characters. Other contributions are free orbits, whose nonidentity trace
is zero. The replay uses this orbit/stabilizer trace formula to reconstruct all
18 simples of D^C2. Tensoring by the equivariant g is free: for pointed simples
it changes the Ising label; for σ-labelled simples a+8=−a would force a even,
contrary to the parity restriction. The rank-nine free-module quotient then
matches all coefficients of 389. Thus neither equivariantization nor quotient
relies on an unverified scalar choice.

## 1857: genuine D4 Dynkin triality

Let B be the unitary Spin(8)_2 WZW category. Permuting the three outer nodes of
D4 is an actual order-three Hopf automorphism of the quantum-group construction.
It preserves the defining relations, coproduct, ribbon/pivotal data, tilting
subcategory and negligible ideal, so induces a coherent braided C3 action on B.
The compact/WZW realization gives its unitary form. This is stronger than a
ring automorphism.

The eleven dominant level-two weights satisfy a1+2a2+a3+a4≤2. The fresh exact
Verlinde computation gives dimensions 1^4,2^7. Precisely 1 and f=ω2 are fixed
under triality; f has dimension two and f² is the sum of the four invertibles.
The remaining simples form three free orbits. The equivariant structure on f
can be chosen to have cube one. Its pairing line f²→1 has a cube-root scalar.
Changing that equivariant structure by ζ3^r changes this scalar by ζ3^(2r), so
one can normalize it to one, preserving the cube constraint. Unit lines are
already fixed. These are all nonzero fusion lines between fixed simples, hence
there are no additional unresolved trace choices. Equivalently the only
single-object projective obstruction is H²(C3,C×)=0, and the action itself
already exists by the Hopf construction.

The replay derives the S matrix in Q(ζ32) from

    S_(λ,μ)=(det(ζ32^(-L_i M_j)+ζ32^(L_i M_j))
             +det(ζ32^(-L_i M_j)−ζ32^(L_i M_j)))/256,

where L=2(λ+ρ), M=2(μ+ρ). It checks exact orthogonality and all Verlinde
coefficients, then applies the C3 orbit/stabilizer trace formula. This gives
rank nine, dimensions 1^3,2^3,3,6^2, and the complete tensor of 1857.

## 2029: equivariant associative Tannakian zest

The four invertibles of B form a Tannakian pointed subcategory P, indexed by
the additive group A=F4. Each nontrivial current 2ω1,2ω3,2ω4 has twist +1;
their mutual monodromy is trivial. They lie in the neutral component of the
universal A grading. A symmetric tensor identification Vec_A→P with trivial
associator and braiding exists. What must additionally be justified is a
triality-equivariant such identification.

The symmetric category P^C3 is Tannakian of dimension twelve. Write it as
Rep(E). Its canonical Rep(C3) subcategory gives an extension

    1 → V4 → E → C3 → 1.

This extension splits by Schur–Zassenhaus. Inverse equivariantization therefore
identifies the original action on P, as a symmetric tensor action, with the
strict split action on Rep(V4), equivalently on Vec_A. This supplies the
coherent equivariant tensor trivialization of P needed below. It resolves the
coherence issue; choosing trivial associators without this argument would not
suffice.

Write t²+t+1=0 in F4. Choose labels so triality multiplies both the grading
and current labels by t: degrees are a1+t a3+(t+1)a4. Set

    λ(a,b)=t(ab)²,   scalar associator cocycle ω1=1.

The map λ is a normalized symmetric group 2-cocycle and satisfies
λ(ta,tb)=tλ(a,b). The replay checks all 64 cocycle equations and all 16
triality-equivariance equations. Galindo–Mora–Rowell, Proposition 4.2(1),
including its proof, states that for Tannakian pointed data any such λ and
scalar 3-cocycle define an associative zest. We use the associative assertion;
a braided zest is neither claimed nor needed.

More explicitly, the new tensor product is X_a⊗λY_b=J(λ(a,b))⊗X_a⊗Y_b,
with the associativity supplied by the stated zest construction. The original
triality is braided, J is coherently equivariant, and λ is equivariant, so its
tensorator transports this new product and its associator. The old C3
comparison maps are still coherent. This supplies an actual C3 action on the
zested category, not merely a new invariant fusion tensor. All scalar and
structural maps can be chosen unitary. The fixed objects 1,f are neutral, so
their fusion-line normalization is exactly the one in the preceding case.
The independent zested Verlinde/orbit reconstruction matches the full tensor
of 2029.

## 1983: ordinary factor swap after equal half-E6 fermion condensation

Take the unitary half-E6 category E, with simples 1,f,x and
x²=1+f+2x, f²=1, fx=x. The published input includes its actual central fermion
f and the fixed-point rotation phase −i (Aasen–Lake–Walker, Sections 7.1–7.2).
Use the same category and phase in both factors. The central boson b=(f,f)
gives A=1+b and Q=(E⊠E)_A. The project's rank-six fixed-point calculation was
read afresh: the product of the two rotation phases is −1, so the two
resolutions u,v of x⊠x satisfy u*=v. The residual invertible g exchanges u,v.
Together with a,a' above x⊠1,1⊠x, the fusion rules are

    a²=1+g+2a,  (a')²=1+g+2a',  aa'=u+v,
    au=av=a'+u+v,  a'u=a'v=a+u+v,
    u²=v²=g+a+a'+u+v,  uv=1+a+a'+u+v.

These rules follow from the free-module tensor functor, fixed-point duality
and associativity; existence comes from the central algebra construction.
The ordinary Deligne factor swap, equipped with the identity algebra map on
A, is a coherent unitary C2 action on Q. It fixes 1,g,u,v and exchanges a,a'.
On x⊠x the two A actions are ±(t⊠t), each preserved by ordinary swap. There is
no super-interchange sign in this functor. Equivariantization therefore has
nine simples.

The invertible extension is important. On gA write e0,e1 for its components
in degrees (f,1),(1,f). Right A action exchanges them; left A action is the
negative exchange. The balanced multiplication g⊗_A g→A has coefficients

    μ00=1, μ01=b, μ10=−b, μ11=−1.

Simultaneously exchanging both indices negates μ. Thus for the lift t of g
with swap structure e0↔e1, one has t²=ε, the nontrivial C2 character. The
invertibles form C4. The replay checks the balancing and swap signs directly.

Centrality of t is also needed, and is not inferred from its underlying
invertible object. The central objects z1=(f,1), z2=(1,f) centralize A: their
monodromy with b is +1. Their free A-modules descend as central objects of Q.
Since z2=z1b and bA is the central unit, those descended central objects are
isomorphic. Their underlying object is the simple g, so their module-isomorphism
space is one-dimensional and every nonzero such isomorphism is central. In
particular the component-exchange swap is central and squares to one. It gives
an equivariant central structure, hence a central lift of t in Z(Q^C2).

Choose Y over u, and let X lie over a+a'. The four t^jY are distinct because t
exchanges u,v while t²=ε exchanges the two equivariant structures. Put
G=Σt^j and V=Σt^jY. The forgetful functor and ε invariance force

    tX=X,  X²=G+2X+V,  XY=YX=X+V.

Also Y²=t^a+X+(t^b+t^c)Y, with a,c odd and b even. Rigidity forces
{b,c}={a−b,a−c}, hence b+c=a modulo four. All four possibilities are related
by replacing Y by t^rY. Choose a=1,b=2,c=3. These relations determine all 729
coefficients, independently of the census, and the replay matches 1983.
Central Q-systems and the stated unitary actions preserve unitarity throughout.

## Primary inputs and reproducibility

- Galindo–Mora–Rowell, *Braided Zestings of Verlinde Modular Categories and Their
  Modular Data*, arXiv:2311.17255v2, Proposition 4.2(1) and its proof:
  https://arxiv.org/html/2311.17255v2 . Read afresh for the arbitrary associative
  λ statement and the role of Tannakian data.
- Aasen–Lake–Walker, *Fermion condensation and super pivotal categories*,
  arXiv:1709.01941v2, Sections 7.1–7.2 and Appendix D.1:
  https://arxiv.org/html/1709.01941v2 . Read afresh for half-E6 and the central
  half-braiding coefficients 1,−i,−1. HTML and PDF equation numbering differ;
  section references are used deliberately.
- Gelaki–Naidu–Nikshych, *Centers of graded fusion categories*, arXiv:0905.3117:
  https://arxiv.org/abs/0905.3117 . Standard equivariantization/de-equivariantization
  and center framework.
- Deaton et al., *Integral Metaplectic Modular Categories*, arXiv:1901.04462:
  https://arxiv.org/abs/1901.04462 . Context for the unitary Spin(8)_2 input;
  the particular fusion tensor is independently reconstructed by exact Verlinde.

Run `python phase3/audit_exotic_models/replay.py` from the research root.
The replay uses exact algebraic/rational arithmetic throughout. It verifies
finite scalar coherence identities and tensor identification; the cited
categorical constructions and the explicit action/algebra arguments above
supply the existence assertions that a ring-only calculation cannot supply.
No downgrade is required for these five models.

# Triality after Tannakian zesting realizes R9_2_2029

Let B be the unitary WZW category Spin(8)_2, with its order-three Dynkin
triality action T. There is a unitary associative zest B^λ such that

    K0((B^λ)^{C3}) ≅ R9_2_2029.

The explicit source-to-model permutation is

    [0,8,7,3,5,2,1,6,4].

The proof uses a genuine equivariant zesting datum. It does not assume that
an automorphism of a zested integer tensor lifts to a tensor functor.

## Tannakian seed and an equivariant choice of its tensor data

The seed and its actual triality action are established in d4_triality.md.
Its four invertibles form A≅V4, all with twist1: the nontrivial ones have
highest weights2ω1,2ω3,2ω4 and the twist formula
exp(πi(λ,λ+2ρ)/8) gives1 for each. Thus the pointed subcategory P is
Tannakian. It lies in the neutral component of B's universal V4 grading.
Triality cyclically permutes its three nontrivial objects and preserves
its symmetric braiding.

We require an equivariant symmetric trivialization of P, rather than an
arbitrary gauge for its associator. Such a choice exists for a structural
reason. The equivariantization P^{C3} is symmetric Tannakian of dimension12.
Write it as Rep(E). Its canonical Rep(C3) subcategory and inverse
de-equivariantization give an exact finite-group extension

    1 → V4 → E → C3 → 1.

Schur--Zassenhaus splits this extension, since the normal subgroup V4 is a
Hall subgroup. Choosing a complement identifies the original C3 action on
P, as a symmetric tensor action, with the ordinary split triality action
on Rep(V4). Via the character basis this is the symmetric pointed category
Vec_A with trivial associator and braiding, on which C3 acts by ordinary
permutation of labels. Hence the inclusion J:Vec_A→B can be equipped with
coherent equivariance. This provides exactly the equivariant pointed
tensor data used below, including compatibility of products of currents.
All these equivalences and maps may be chosen unitary.

## An actual associative zest and its actual triality action

Identify both the universal grading group and A with the additive group of
F4=F2[t]/(t²+t+1), in such a way that triality is multiplication by t in
both groups. For highest weight(a1,a2,a3,a4), use degree

    a1 + t a3 + (t+1)a4,

where coefficients are reduced modulo2. For currents, the element1 is2ω1,
t is2ω3 and t+1 is2ω4. Define

    λ(a,b)=t(ab)² ∈ A,    ω(a,b,c)=1.

The map λ is additive in both arguments, symmetric, and normalized, so it
is a group two-cocycle. It is also strictly triality-equivariant:

    λ(ta,tb)=t⁴ λ(a,b)=t λ(a,b).

The pointed part is Tannakian, so every such pair of a two-cocycle λ and a
scalar three-cocycle ω defines an associative zest. This is precisely
Proposition4.2(1) and its proof in Galindo--Mora--Rowell,
*Braided Zestings of Verlinde Modular Categories and Their Modular Data*,
[arXiv:2311.17255](https://arxiv.org/abs/2311.17255), Section4.1. In the
Tannakian gauge the current associator and braiding are trivial and the
associative-zesting obstruction vanishes. The new product is

    X_a ⊗_λ Y_b = X_a ⊗ Y_b ⊗ J(λ(a,b)).

The associator is the usual zesting associator formed from B's associator,
the braiding past these currents and J's coherent current multiplication;
its scalar correction isω=1. These are unitary maps, so the result is a
unitary fusion category. A braiding on the zested category is not required.

Crucially, triality preserves this entire datum, not just λ's values on
classes. Its equivariance on J identifies T(J(λ(a,b))) with
J(λ(ta,tb)), and its original tensor structure then gives

    T(X_a) ⊗_λ T(Y_b) ≅ T(X_a ⊗_λ Y_b).

Every diagram for the zested associator is assembled from the original
braided tensor functor T, the equivariant tensor functor J and the strictly
equivariant cocycle λ. Therefore these tensor structures preserve the new
associator, and the original C3 composition constraints remain coherent.
Equivalently, the zesting construction is functorial for braided tensor
functors preserving its pointed datum. This explicitly supplies an actual
unitary C3 action on B^λ and hence its equivariantization.

## Complete tensor and identification

Zesting changes no object or FP dimension and no triality orbit. The only
fixed simple objects remain1 and f=ω2. They are neutral, so their fixed
fusion lines and the rule f²=sum_A g are unchanged. The same normalized
trace argument as in d4_triality.md therefore computes all equivariant
fusion coefficients. The two free nonneutral orbits become dual to each
other after the zest, giving the two dual dimension-six simples of
R9_2_2029.

d4_zest_triality.py independently reconstructs the original WZW tensor,
checks the universal grading, current-group law and both triality actions,
verifies all64 cocycle identities and16 equivariance identities, and
forms the zested tensor by the actual product formula above. It checks its
fusion axioms and triality invariance, applies the complete character
average, and compares all729 census coefficients. Replacing t by t+1 in
the coefficient of(ab)² gives a second datum with the same based ring.
Both exact witnesses are recorded in d4_zest_triality_models.json.

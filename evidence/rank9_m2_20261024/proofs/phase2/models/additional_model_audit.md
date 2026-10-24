# Independent categorical audit of two weakly integral models

The weak-integral agent's models R9_2_21 and R9_2_389 pass this audit. Their
existence follows from actual coherent actions and central algebra quotients,
not from an integer tensor that happens to be associative. They remain owned
by phase2/weak_integral and are separate from the six models in this directory.

## R9_2_21

The action in ../weak_integral/projective_ty.md is well-defined. The orthogonal
group action on TY(A,χ,τ) is an actual tensor action, with identity tensorators
in its standard skeleton; this is explicitly Proposition 4.8 of
Gelaki--Naidu--Nikshych,
[arXiv:0905.3117](https://arxiv.org/abs/0905.3117). Pullback through V4→C2
and modification by the parity automorphism with cocycle b*c both preserve
the full action pentagon. On the odd simple the multiplier has a
nondegenerate alternating bicharacter, so its twisted group algebra is M2(C).
Thus the odd equivariantization consists of one simple of dimension 2√5.
Its products are forced by the ordinary even representation ring and
Frobenius reciprocity, exactly as in the agent's proof. The independent
replay reconstructs the tensor and checks every coefficient of the match.

## R9_2_389

Put ζ=exp(2πi/16) and let P=Vec(C16,ω), where

    ω(a,b,c)=ζ^(2a floor((b+c)/16)),   0≤a,b,c<16.

Let D be the fusion subcategory of Ising⊠P consisting of (1,a),(ψ,a) for
a even and (σ,a) for a odd. Closure follows from the usual Ising parity
grading, so D exists as a unitary fusion category without a classification
assumption. Its global dimension is 32.

Inversion a↦−a, acting trivially on the Ising factor, is a tensor functor
with tensorator

    μ(a,b)=ζ^(−2a·1_(b>0)).

Its square is the identity tensor functor: μ(a,b)μ(−a,−b)=1. The tensorator
pentagon is dμ=ω∘(−1)−ω in exponent notation. The code independently checks
the full cocycle equation, all 4096 pentagon equations and all 256 square
coherence equations. Thus inversion is a coherent C2 action, with square
constraint the identity.

The pointed object 8 has central half-braiding β(a)=ζ^(7a). Its central
hexagon follows because ω(8,a,b)=1 and ω(a,8,b)=ω(a,b,8), so β is an
ordinary character. Its central tensor square is trivial: the exponent of
the squared half-braiding is

    2·7a + w(8,8,a) − w(8,a,8) + w(a,8,8) = 16a = 0 (mod16).

Combining this central object with the standard Ising central fermion ψ
gives g=(ψ,8) of central order two and self-braiding
(−1)β(8)=(−1)(−1)=+1. Its associator on g,g,g is trivial. Hence 1+g is a
genuine central connected separable algebra.

The inversion action preserves the specified central lift, not merely its
underlying object. The transport identity is

    β(a)/β(−a)=μ(8,−a)/μ(−a,8),

which holds for every a. Since μ(8,8)=1 and the square constraint is one,
either sign of the identity equivariance on g equips 1+g with coherent
equivariant algebra structure. Thus it is a central bosonic algebra in
D^{C2}, and the ordinary module category (D^{C2})_(1+g) exists and is unitary.

There are 18 simple objects in D^{C2}. The two fixed degrees 0,8 contain
only pointed objects. Consequently the character trace used in
mr_orbifold.py has contributions only from fixed pointed input channels;
all nonfixed channels have zero trace. Its tensorator and square-coherence
factors are precisely those derived from the action above. This verifies
that the formula computes equivariant fusion coefficients rather than
assuming them. The boson acts freely on these 18 simples, so the central
quotient has nine simples and its fusion coefficients are the free orbit
sums. The exact resulting tensor matches R9_2_389.

additional_model_audit.py checks the above coherence identities independently
using the closed formula, reconstructs both boson-sign quotients through the
agent's general orbit constructor, validates the fusion axioms, and checks
all 729 census coefficients in each case. The independent report is
additional_model_audit.json.

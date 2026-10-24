# Independent categorical audit: R9_2_92

**Verdict: PASS.** The relative Schur-cocycle construction realizes
R9_2_92 by a unitary group-theoretical fusion category. This verdict uses
an independent derivation of the twisted fusion formula and a fresh
cochain/tensor replay; it does not rely on the candidate's stored PASS.

The audited construction is
`C(S5, ω, S3×C2, ψ)`, where `ω(g,h,k)=(-1)^(ε(g)α(h,k))` and α,ψ are
the explicit normalized cochains in
`phase3/group_models/s5_relative_twist.json`. The candidate's derivation
is `phase3/group_models/S5_RELATIVE_TWIST.md`.

## Existence and scope

The independent replay reconstructs S5 as all permutations of five
letters, with composition matching the supplied table, and reconstructs
H as the permutations preserving the blocks of sizes three and two.
It verifies the parity homomorphism and all 120³ two-cocycle identities
for the actual adjusted α. Thus ε cup α is a genuine normalized
three-cocycle. No assertion about Schur-cover naming is needed for
existence: the recorded cochain itself is verified.

The replay verifies normalization of ψ and its algebra associativity
identity on every one of the 12³ subgroup triples. With associator
`a_(g,h,k)=ω(g,h,k)`, multiplication `a_h a_k=ψ(h,k)a_hk` requires
`δψ=ω^(-1)|H`. The saved identity is sometimes written `δψ=ω|H`;
these coincide here because ω takes values in {±1}. This convention
does not create a sign gap.

Consequently A is the usual connected separable twisted subgroup
algebra in Vec_(S5)^ω. The category of A-bimodules is a fusion category.
The construction lies in the unitary setting: both cochains have unit
modulus, and the finite subgroup algebra supplies its standard unitary
separable algebra structure. Alternatively, group-theoretical fusion
categories are completely unitary by Galindo–Hong–Rowell, Theorem 5.20.
There is no assumption of a braiding or of a fiber functor on the new
category.

## Independent check of the three phase formulas

Write L_a,R_b for bimodule actions on a homogeneous degree-v fiber.
The associator convention directly gives

`L_a L_c = ψ(a,c) ω(a,c,v)^(-1) L_ac`,

`R_c R_a = ω(v,a,c) ψ(a,c) R_ac`,

`R_c L_a = ω(a,v,c) L_a R_c`.

For a double-coset representative t, let K=H∩tHt^(-1), and define
`ρ_t(a)=R_(t^(-1)at)^(-1) L_a` on the degree-t fiber. Substitution in
these three identities gives the multiplier

`α_t(a,c) = ψ(a,c) ω(a,t,t^(-1)ct) /
             (ω(a,c,t) ω(t,t^(-1)at,t^(-1)ct) ψ(t^(-1)at,t^(-1)ct))`.

This agrees with candidate equation (1). The independent replay also
checks all resulting stabilizer two-cocycle identities.

To transport a character from t to v=l t k, conjugate ρ along R_k L_l.
Putting u=l t, s=l^(-1) a l, c=t^(-1) s t and b=v^(-1) a v, the scalar is

`[ψ(a,l) ω(l,s,t) / (ω(a,l,t) ψ(l,s) ω(l,t,c))]
 [ω(u,c,k) ψ(c,k) / (ω(a,u,k) ω(u,k,b) ψ(k,b))]`.

This agrees independently with equations (3),(4) and with `char_at`.

Finally, the relative tensor-product relation is

`R_h(m_u) ⊗ n_v = ω(u,h,v) m_u ⊗ L_h(n_v)`.

On an output fiber t=u v, a trace contribution occurs precisely when
a stabilizes the right H-coset uH. Then h=u^(-1) a u lies in H and
b=t^(-1) a t. Left action contributes `ω(a,u,v)^(-1)`; after applying
the displayed balancing relation, inverse right action contributes
`ω(u,v,b)^(-1)`. The resulting contribution is

`ω(u,h,v)/(ω(a,u,v) ω(u,v,b)) · χ^M_u(a) χ^N_v(h)`.

The inverse-right-action simplification uses the three-cocycle identity,
and agrees with candidate equation (6). Since all output-fiber
representations have multiplier α_t, the usual unitary projective
character inner product gives multiplicities. In particular, no
untwisted convolution has been silently used.

## Exact independent replay

`audit_s5_relative_twist.py` imports no construction code. It rebuilds
the group, double cosets, coset representatives, multipliers and
characters, evaluates the independently audited formula in Q(ζ8), and
checks the unit, associativity and all 729 source coefficients.

The stabilizers have sizes 12,2,4 and the double cosets have sizes
12,72,36. The projective irreducible dimension lists are respectively
`[1,1,1,1,2,2]`, `[1,1]`, and `[2]`. The final V4 multiplier has trivial
commutator radical, so its twisted group algebra is M2(C); the unique
irreducible character is two at the identity and zero elsewhere.

The resulting dimensions are `1,1,1,1,2,2,6,6,6`, with squared sum120.
Every source coefficient matches under the source-to-model permutation

`[0,3,1,5,7,6,4,2,8]`.

Machine-readable audit: `s5_relative_twist_audit.json`.

## Primary references checked

* Etingof–Nikshych–Ostrik, *Weakly group-theoretical and solvable fusion
  categories*, §2.5 and the subgroup-algebra construction:
  https://arxiv.org/pdf/0809.3031 .
* Galindo–Hong–Rowell, *Generalized and quasi-localizations of braid
  group representations*, Theorem5.20:
  https://people.tamu.edu/~rowell/GHRarx1.pdf .

The three explicit phase formulas above are independently derived here
from the module axioms; they are not attributed as quotations from these
references.

# Direct anticommutation in the three commutative rank-nine sources

## Statement

In every spherical categorification of R9_2_137, R9_2_1607 or R9_2_1976, each of its four nonintegral simple objects X satisfies

`nu_3(X) in {-1,-zeta_3,-zeta_3^2}`.

Therefore each normalized relative trace to `Q(sqrt(2))` lies in `{-1,1/2}`, and in particular is at most `1/2`. This strengthens the aggregate Morita constraint of `POINTED_BIMODULE.md` to **four separate constraints**. It applies to either sign of the TY parameter. R9_2_1975 is deliberately not included: its nonintegral simples have different left and right pointed stabilizers.

The categorical anticommutation argument below works over C without a spherical structure. Spherical structure enters only in the final pivotal-rotation theorem. A positive center application uses the already audited source-to-pseudo-unitary Galois reduction.

**General module-functor criterion.** The proof only needs a full fusion subcategory D, a simple X in an indecomposable left D-module component M of C, its actual internal-end algebra with underlying object `1+h`, the relation `Xh≅X`, and a nonidentity permutation of the simples of M by right tensor h. The internal-end algebra itself supplies the associative multiplication on `1+h`; no separate TY classification or anisotropy premise is needed. Under these hypotheses the left/right h actions on X anticommute. The TY discussion below identifies the particular components and stabilizers in these rank-nine sources.

## The orbit information

The established TY module theorem gives an integral fusion subcategory

`D=TY(V4,chi,tau)`,

with nonalternating chi. The four nonintegral objects form an indecomposable left D-module category M. As a pointed V4-module it has two two-element orbits with distinct stabilizers `H={1,h}` and `H'={1,h'}`. The bicharacter forces `H'=H^perp`, so h and h' are anisotropic. The entire pointed subcategory has trivial associator.

For a nonintegral X in the H-stabilized orbit, its internal-end algebra in D has underlying object `B=1+h`. The internal-end construction gives an equivalence

`M ≅ Mod_D(B)`

that takes X to the **regular right B-module** B. There is only one possible associative subgroup-algebra structure on this underlying object up to gauge, since `H^2(C2,C*)=0`.

The original source ring is commutative. Consequently right tensoring by h fixes both simple objects of the first orbit and swaps the two objects of the second orbit. The latter assertion follows because h is nonidentity and is not in H'. In particular this right tensor functor is not isomorphic to the identity functor on M.

The exact source labels are:

| Source | First orbit, h | Second orbit, h' |
|---|---|---|
| R9_2_137 | {3,6}, 7 | {4,5}, 2 |
| R9_2_1607 | {1,2}, 4 | {7,8}, 6 |
| R9_2_1976 | {1,2}, 6 | {3,4}, 7 |

All indices are zero-based in the restored source tensors.

## The module functor is necessarily the sign twist

Let `F=(-) tensor h` on M. Ambient associativity makes F a **left D-module functor**. Under `M≅Mod_D(B)`, such functors are given by tensoring on the right over B with a B-bimodule P. The value `F(B)` is exactly P regarded as a right B-module.

Since `X tensor h≅X`, one has `P≅B` **as right B-modules**, not merely as objects of D. Transport the left B-action on P to this fixed regular right B-module. Such an action is determined by an algebra homomorphism

`B -> internal End_B(B) ≅ B`.

The unit goes to the unit. The h-summand must act nontrivially because its square is the unit action; hence the homomorphism is an algebra automorphism. Since 1 and h are nonisomorphic simples and the chosen h multiplication squares to 1, this automorphism is either

`h -> h` or `h -> -h`.

These exhaust all possibilities, over arbitrary complex scalars. The first is the regular B-bimodule and gives the identity D-module functor. That is impossible here, since F swaps the second orbit. Therefore P is necessarily the bimodule whose left h-action is negated relative to its regular right h-action.

To read the scalar conclusion in the original category, choose normalized maps `l:hX->X` and `r:Xh->X`, with h² identified with 1 by B. Under the internal-end equivalence, l is regular multiplication on B; the left B-action on F(B) is obtained by applying F to that multiplication and using the D-linearity of F. Transporting this action to B through r is exactly the comparison of

`r (l tensor id_h)` and `l (id_h tensor r)`.

The sign-twisted bimodule says these maps differ by −1. Thus

`r (l tensor id_h) = -l (id_h tensor r)`.

This is the normalized left/right stabilizer anticommutator required by the stabilizer-rotation proposition. Repeating the same internal-end argument at the other object of this orbit gives the same sign; alternatively transport through its invertible left-module action. Repeating with H' proves the assertion for the second orbit.

Notice that no based-central element has been promoted to a central half-braiding. The inference uses an actual D-module functor, its actual B-bimodule, and a forced nontrivial permutation of the other orbit.

## The cubic consequence

For all twelve source objects under consideration the exact fusion tensor gives

`dim Hom(1,X^3)=N_(X,X)^(X*)=2`.

The project’s stabilizer-rotation proposition now applies with B and the preceding anticommutator. Its Clifford algebra proof gives the three-element necessary set

`nu_3(X) in {-1,-zeta_3,-zeta_3^2}`.

Since `Q(sqrt(2))` is disjoint from `Q(zeta_3)`, normalized trace sends these values to `-1,1/2,1/2`, respectively. No assumption about self-duality or absence of the prime 3 from the Frobenius--Schur exponent is used.

In the positive central-induction system, if v_X is the multiplicity of X in the restriction of a central simple of dimension z and t3 its normalized twist trace, then

`sum_Z v_X z t3 = D * Tr(nu_3(X))`.

With `D=144+96sqrt(2)`, its sqrt(2) coefficient is at most 48. `screen_morita_third.py --local-clifford` adds these four inequalities with nonnegative slack variables. Any further exclusion requires an exact separating certificate; this categorical proof alone is a restriction, not a status change.

## Dependencies and audit

- TY module/internal-end proof: published `THEOREM.md` under `evidence/rank9_m2_20261024/proofs/phase5/quadratic_comm/ty_module_subtask/` at commit `323c4227ffb796a72eef506f1eb289437fbc95db`.
- Standard correspondence between module functors and bimodules: Etingof--Gelaki--Nikshych--Ostrik, *Tensor Categories*, module categories chapter; the proof here specializes it to the regular B module and records both possible algebra automorphisms explicitly.
- Pivotal Clifford theorem: `grothendieck-ring-classification/manuscripts/rank6/papers/chapters/stabilizer_rotation.tex`, Proposition `prop:stabilizer-rotation` and its projected-trace corollary.
- The rank6 research agent independently checked the sign-bimodule argument and the indicator consequence. A second independent audit was requested from the quartic-pair agent.

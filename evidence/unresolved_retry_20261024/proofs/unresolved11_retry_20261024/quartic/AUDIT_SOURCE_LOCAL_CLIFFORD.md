# Independent audit: source-local Clifford constraint

Audit target: `../rank9/SOURCE_LOCAL_CLIFFORD.md`.

**Verdict:** the categorical anticommutation argument is valid for R9_2_137, R9_2_1607 and R9_2_1976. Together with the already proved stabilizer-rotation proposition, it gives the claimed individual projected third-indicator constraint on all twelve large source objects. It does not, by itself, exclude any source ring.

The tensor check below was independently replayed from the restored input profiles. This audit is independent of the proposed D8 stabilizer cocycle computation and does not need that computation.

## A general formulation of the categorical step

Let D be a full fusion subcategory of C, M an indecomposable left D-module component of C, and X a simple in M. Suppose that an involution h in D satisfies:

1. The internal end of X for the D-action has underlying object B=1+h.
2. Xh is isomorphic to X.
3. Right tensoring by h moves at least one simple object of M.

Then the normalized left and right h-actions on X anticommute.

Indeed, the internal end is a connected separable algebra. Its h-times-h multiplication is nonzero, and fixes a coherent identification h² -> 1. The standard internal-Hom equivalence M ≅ Mod_D(B) carries X to the regular right B-module. Since right tensoring by h is D-linear by the ambient associator, it corresponds under Eilenberg–Watts to a B–B bimodule P. Condition 2 implies that P is isomorphic to B **as a right B-module**.

Transport P's left B-action through such an isomorphism. The space of right B-linear maps h tensor B -> B is one-dimensional: regular left multiplication identifies h tensor B with B, and End_B(B)=Hom_D(1,B)=C. Therefore the transported left h-action is a scalar multiple a of regular left multiplication. The left module axiom forces a²=1. The two possibilities are exactly the regular bimodule and its sign twist. This argument permits arbitrary complex coefficients; it is not a search over root-of-unity gauges.

If a=1, P is the regular B-bimodule and the corresponding D-module functor is isomorphic to the identity. Condition 3 rules this out, so a=-1.

For the explicit sign comparison, choose l:hX -> X from the internal-end action and r:Xh -> X. In strict monoidal notation, applying the functor F=(-) tensor h to l gives l tensor id_h. Its D-module constraint identifies the source with h tensor F(X). Transport through r gives the h-action

    r (l tensor id_h) (id_h tensor r^{-1})

on X. The sign-twisted bimodule says that this equals -l. Equivalently,

    r (l tensor id_h) = -l (id_h tensor r).

Restoring associators gives exactly the same comparison; strictification is only notation. Scaling r does not change the displayed sign. Both l and r can be normalized to square to the chosen h² -> 1 map. Thus the hypothesis of the stabilizer-rotation proposition is genuinely categorical, not a conclusion inferred from commuting fusion matrices.

Anisotropy of h in the TY bicharacter is one way the existing project establishes the required module structure. Once conditions 1–3 above are known, the sign argument needs no additional anisotropy or unitarity assumption.

## Source data independently checked

The restored tensors have the following large-object pointed orbits and stabilizers:

| Ring | First orbit and stabilizer generator | Second orbit and stabilizer generator |
|---|---|---|
| R9_2_137 | {3,6}, h=7 | {4,5}, h'=2 |
| R9_2_1607 | {1,2}, h=4 | {7,8}, h'=6 |
| R9_2_1976 | {1,2}, h=6 | {3,4}, h'=7 |

For every large X in these three rings, the D-part of X tensor X* is 1+h, the left and right h-stabilizers agree, and right h moves both objects in the opposite orbit. The dimension-two TY object connects the pointed orbits, so the four large objects form an indecomposable D-module component.

For every one of the twelve objects,

    dim Hom(1,X³) = N[X,X,X*] = 2.

This uses the actual dual index; several of the objects are not self-dual.

R9_2_1975 correctly lies outside this argument: its nontrivial left and right stabilizers differ. The source-local conclusion must not be copied to that fourth ring merely from the shared dimension vector.

## Indicator and inequality audit

The cited project proposition constructs adjacent involutions P,Q on Hom(1,X³), derives PQ=-QP, and uses naturality of pivotal cyclic rotation E to obtain EPE^{-1}=Q. The three conjugates of P form a Cl_3 representation. The universal implementing element has trace -1 on each two-dimensional Clifford simple, giving

    nu_3(X) in {-1,-zeta_3,-zeta_3²}

when dim Hom(1,X³)=2. No self-duality assumption is required. The two nonreal possibilities must be retained because 3 has not been excluded from the exponent.

Normalized relative trace to Q(sqrt(2)) gives {-1,1/2}, since Q(sqrt(2)) intersects Q(zeta_3) in Q. For the positive center application D=144+96 sqrt(2), so the sqrt(2) coefficient of D times this projected indicator is at most 48. Consequently the four separate coefficient inequalities used by `--local-clifford` are necessary for every pseudo-unitary realization. General-complex application continues to depend on the previously audited spherical/Galois reduction.

This audit does not certify a numerical LP infeasibility result. Any exclusion still requires an exact certificate covering all remaining center branches.

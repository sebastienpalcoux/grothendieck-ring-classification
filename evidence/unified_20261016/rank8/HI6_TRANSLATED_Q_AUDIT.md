# Exact closure of the translated HI(C6) Q-system lead

This note checks whether the odd translates of the algebra 1+ρ can produce R8_2_630 or R8_2_671 instead of the constructed R8_2_535. It closes this particular lead; it is not an exclusion of either open ring.

Let C be either known unitary HI(C6) category whose center inventory is used in HI6_DUAL_PROOF.md. Assume 1+α_tρ admits a Q-system, as provided by the Q2 condition in the cited examples. Put ρ'=α_tρ. For every t, including odd t, its fusion rules are

ρ'α_h=α_{−h}ρ',  ρ'^2=1+Σ_g α_gρ'.

Thus the translated algebra is 1+ρ' for a generalized Haagerup generator of exactly the same type. The analysis of its 3^G subfactor in Izumi, *The classification of 3^n subfactors and related fusion categories*, Proposition 7.4/Theorem 7.5, applies to this chosen generator. This is not an assumption that the even and odd translates are conjugate by an invertible object.

Write ι for the subfactor/module generator, i_g=α_gι, and κ for the complementary simple in ρ'ι=ι⊕κ. Its module simples are i_g (g∈C6) and κ, with α_gκ=κ. In the dual category define

1+ρhat=barιι, β_z=α_z|_N (z∈G[2]), π_h=barια_hι (h∉G[2], modulo h↦−h).

The two remaining simples σ_j have dimension d−1 by Theorem 7.5, where d=3+√10. Direct composition, using only the displayed fusion rules, gives

- i_g ρhat = i_g ⊕ κ;
- i_g π_h = i_{g+h} ⊕ i_{g−h} ⊕ κ;
- i_g β_z = i_{g+z};
- i_g σ_j = κ.

For the last identity, ισ_j=κ follows from Theorem 7.5 and Frobenius reciprocity; multiplication by α_g preserves κ. These formulas are independent of t. In particular the odd translate does not introduce an unnoticed shift in the top-left permutation blocks.

Normalize module dimensions as (1,1,1,1,1,1,d−1). Reciprocity fixes every off-diagonal κ entry to one for the six noninvertible dual objects and to zero for 1,β_3. The dimension equations then give the lower-right entries 5,5 for ρhat,ρhatβ_3; 6,6 for π_1,π_2; and 4,4 for σ_1,σ_2. Thus the entire canonical seven-object action is exactly the action in the accepted R535 proof, not just a principal-graph dimension profile.

The center of a Morita dual is braided equivalent to Z(C), so the same proven center inventory applies. The character reconstruction of HI6_DUAL_PROOF.md therefore identifies every one of these translated-Q duals with the R8_2_535 based ring. This holds for both cited HI(C6) solutions. The initial suggestion that the odd translate might yield R630/R671 is consequently ruled out by this explicit module calculation.

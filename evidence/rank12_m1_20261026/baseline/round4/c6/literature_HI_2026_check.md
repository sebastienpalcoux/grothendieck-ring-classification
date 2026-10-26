# Targeted check of the September2026 Haagerup–Izumi papers

Checked directly: Gannon–Schopieray–Yadav, *On Haagerup–Izumi fusion categories*, arXiv:2609.25185v1, submitted21September2026, full82-page primary PDF https://arxiv.org/pdf/2609.25185. This source was already noticed in round2 (`family_cubic/root_c6/findings.md`); the present check reads its exact hypotheses against R561/R623/R628.

**No theorem in this paper resolves these three rings.** The main theorem begins with an odd integer N≥3 and G=C_N. The general HI framework in Section2 likewise specifies an abelian group of odd order. Its fusion rules (2.1) require inversion action αρ=ρα^−1 and ρ²=1+Σ_g α_gρ. The completeness statements additionally concern untwisted Q-system-type categories; TheoremA(3)'s algebra/module classification explicitly assumes unitary, untwisted, Q-system type. Those stronger hypotheses cannot be inferred for the original three candidates.

| Candidate | Why it does not satisfy the stated HI framework |
|---|---|
| R12_1_561 | G=C6 has even order; the mixed action is the identity, not inversion. |
| R12_1_628 | G=C6 has even order; the mixed action is the identity; ρ² has pointed term z, the order2 element. |
| R12_1_623 | G=C6 has even order; inversion holds, but ρ² has pointed term z and every noninvertible is non-self-dual, with ρ*=zρ. Replacing ρ by gρ leaves this pointed term z unchanged. |

The dimension is d=3+√10, satisfying d²=6d+1, and FPdim=120+36√10. The paper's odd-order constructions, their stated Morita duals, and rational-dimension-scaling operations cannot directly give this dimension: for odd N, N²+4 is odd and cannot have squarefree part10. Thus their dimension field differs from Q(√10).

Section6 does contain one genuinely applicable general result: **Proposition6.1**, valid for any fusion category and any pointed tensor subcategory, constructs coherent conjugation and proves D^Γ≃Z_Q(D). Its proof explicitly cancels the pointed associator scalar against the inverse dual scalar. This independently supports our R332 argument and the coherent-inner-action step in the three unresolved cases. It does not prove an ambient braiding, an isotropic central lift, a rank4 tensor quotient for a noncommutative central algebra, or the missing model/obstruction.

The near-group assertion Theorem6.3 remains within the odd-order framework set at the start of Section6. Its proof uses that g↦2g is bijective, which fails for C6. The theorem must not be applied merely because its displayed statement repeats only part of the standing hypotheses.

Also opened primary Huang, *Cyclic Haagerup–Izumi fusion categories at every odd order*, arXiv:2609.15986v1, https://arxiv.org/html/2609.15986v1. Its construction and pseudo-unitary existence likewise explicitly require odd n and do not cover these cases.

Targeted searches for new even-order/C6 results returned the previously checked Grossman–Izumi generalized-Haagerup work (arXiv:1501.07679 / published *Drinfeld centers of fusion categories*) and the two odd-order2026 papers. The known even C6 constructions have the ordinary inversion/self-dual HI fusion rules and support the already modeled R326, not the three distinct rings above. No newly found primary even-order theorem removes their current gaps. This is a report of the targeted literature search, not a claim that every unpublished construction has been ruled out.

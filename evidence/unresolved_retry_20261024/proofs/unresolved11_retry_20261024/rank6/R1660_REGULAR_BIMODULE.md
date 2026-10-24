# R6_8_1660: audit of the existing regular Ising bimodule reduction

This retry independently recovered the following structural description. A full source reread located it already in `frontier_1660.tex`, Proposition `prop:1660-relative-center`, so it is not a new reduction and must not be counted as progress toward exclusion. No model or exclusion was obtained.

Write the basis as 1,g,sigma,rho,g rho,sigma rho, with Ising relations g²=1, g sigma=sigma, sigma²=1+g. Let I be the Ising fusion subcategory and let M be the full additive subcategory on rho,g rho,sigma rho. The multiplication rules give

`rho² = 1 + [3(1+g)+4 sigma] rho`.

The categorical decomposition `C=I ⊕ M` is a decomposition as I-bimodule categories, not a faithful group grading.

## The nontrivial component is the regular bimodule

As a left I-module, M is equivalent to I: the functor a↦a rho maps the three simples of I bijectively to the three simples of M, and the internal endomorphism object of rho in I is the tensor unit. Thus it is a module equivalence, not merely an equality of based module matrices.

Transporting the right I-action through this equivalence gives a tensor functor from I^rev to End_I(I), identified with I^rev by right multiplication. It maps each of the three simple classes to itself, so it is a tensor autoequivalence. Any tensor autoequivalence of an Ising category is tensor isomorphic to the identity: Drinfeld–Gelaki–Nikshych–Ostrik, *On braided fusion categories I*, Remark B.6(i), https://arxiv.org/pdf/0906.0620 (page82 of the PDF).

Consequently M is equivalent to the regular I-bimodule category. In particular rho has coherent commutation isomorphisms with I. These are a **relative** half-braiding, not a half-braiding with all of C.

## Where a further proof would have to act

The multiplication functor `M ⊠_I M -> C` is a functor of I-bimodules. After identifying both copies of M with I, its two components are described by objects of `End_(I-I)(I) ≅ Z(I)`. The forgetful objects of these two components are respectively 1 and `3(1+g)+4 sigma`. The existing manuscript goes further: after arithmetic and indicator cuts, its relative-center relation is forced to `t²=e+A t`, with `e=(g,g)` and `A=2(sigma,1)+2(sigma,g)+3(sigma,sigma)`, up to exchanging the two Ising factors.

This explains why the regular-bimodule observation does not force a central lift of sigma. The multiplication channels carry their own central data and their associativity compatibility is still unknown. Extending the relative commutation maps across M, or identifying C with a tensor product, would require an additional theorem or an actual verification of that compatibility. Neither follows from the based ring.

There is a compact identity in the Ising ring:

`3(1+g)+4 sigma = (1+g+sigma)²`.

It follows by expanding with sigma²=1+g and g sigma=sigma. This suggests organizing any construction as a quadratic extension over I with a square coefficient object. It does not assert that any corresponding algebra or extension exists.

The Ising subcategory, both categorical types of its associator, and nonunitary ambient categories are all allowed in this reduction. The statement uses no unitarity premise.

R6_8_1660 remains unresolved.

# Scoped necessary conditions and the multiplicity-one frontier

These statements do not change the general categorification ledger. `verify_scoped.py` checks the exact source hypotheses. Its normal and optimized receipts are separate from the general decisions.

## Five unitary obstructions from the 2D2 neutral category

The neutral rank-four rules are 1,g,x,y, g²=1, gx=xg=y, gy=yg=x, x²=y²=1+2x+2y, xy=yx=g+2x+2y. The classification of Edie–Michell–Izumi–Penneys (arXiv:2108.01564, self-dual case, in particular Theorem 3.43) gives its unique unitary categorification, the 2D2 even category Q1. Grossman (arXiv:1612.07185, Theorem 4.19) proves its Brauer–Picard group is exhausted by automorphism bimodules. Every such bimodule is equivalent to the regular left module and therefore has the regular module dimensions, including invertible simple objects.

In R152,R153,R166,R495 the displayed neutral subcategory has a faithful C2 extension whose odd component has no invertible object. A homogeneous component would be an invertible Q1 bimodule, contradicting the preceding regular-module requirement. These exclusions use the unitary uniqueness theorem and are asserted only for unitary categorification.

R24 has the same neutral Q1 and an odd invertible u with u²=g. It is a C2 extension with a C4 group of invertibles, rather than a C4 grading over Q1. Its commutative tensor forces Ad(u) to fix all neutral labels, and Ad(u)²=Ad(g). The label-fixing kernel of Aut_tensor(Q1) is C2×C2: Grossman's proof gives Aut(Q1) of order8 and nontrivial Ad(g); the order-two action of EIP Corollary 3.45 fixes labels and is outer, and commutes with Ad(g) because it fixes g. These two distinct involutions exhaust the order-four kernel. Thus no element in this kernel squares to the nontrivial Ad(g). This excludes a unitary realization of R24.

## Indicator overlap

R315 and R317 each contain ordinary PSU(2)_6 and pseudo-PSU(2)_6 rank-four subcategories with the same nontrivial invertible g. In the unitary classifications the former gives ν2(g)=+1 and the latter ν2(g)=-1. Their canonical spherical structures agree on a fusion subcategory, so the indicators cannot disagree. This is a unitary obstruction only; it is not promoted to a pseudo-unitary or general exclusion.

R312 contains the pseudo-PSU(2)_6 subring and also a simple object outside it fixed by g. In the pseudo-unitary rank-four analysis of Larson, *Pseudo-unitary non-self-dual fusion categories of rank4*, arXiv:1401.1879, Proposition 5.5 and the Case1 contradiction in the proof of Theorem 5.8, the pseudo-PSU ring forces ν2(g)=-1, equivalently nontrivial associator on its C2 pointed subcategory. A g-fixed simple defines a rank-one module over that pointed category, forcing its associator class to vanish. This excludes pseudo-unitary categorification, and therefore also unitary categorification, but leaves general categorification open. The code records a source basis map and the additional fixed simple explicitly.

## R8_1_9, R8_1_18 and R8_1_49

All three source tensors have exactly four invertibles and four noninvertibles of Frobenius–Perron dimension d=2+sqrt(5), and the invertibles act transitively on the noninvertible basis. Thus they are generalized near-group fusion rings, with irrational dimension.

The published Lemma 3.1 of Schopieray, *Categorification of integral group rings extended by one dimension*, J. London Math. Soc.108(4) (2023), DOI 10.1112/jlms.12789, states that any two-dimension categorification is **Galois conjugate to** a pseudo-unitary categorification. Consequently general, pivotal, spherical and pseudo-unitary **existence** are equivalent for these rings. This does not say every categorification is pseudo-unitary, and does not imply unitarity. Use the published corrected Galois-conjugacy formulation, not an earlier arXiv wording.

Schopieray, *Irrational braided generalized near-groups*, Canadian Math. Bull.66(4) (2023), Theorem 3.6, classifies such braided fusion rings, up to pointed products, as Fibonacci or the adjoint sl2 level6 family. Their nontrivial Frobenius–Perron dimensions are (1+sqrt(5))/2 or 1+sqrt(2), whereas here d=2+sqrt(5). Hence none of the three rings admits a braided categorification. For R49 noncommutativity also supplies an immediate independent braiding obstruction.

The previously audited finite scalar-tensorator gauge argument forces specific unique central lifts: g² in R9; all four C4 invertibles in R18; and the nontrivial phi-fixed invertible in R49. Its original full gauge certificates were removed with the old scratch workspace and have not been reconstructed in this source stage. These central-lift statements are retained research, rather than newly replayed gauge certificates. In any case they do not establish that those lifts are bosons. A central fermion in Z(C) may fix a simple underlying C-object; a transparent-fermion fixed-point argument is therefore unavailable without a braiding on C.

Known order-four Haagerup–Izumi Morita families do not match these rules: standard C4 is noncommutative with inversion, standard V4 is commutative, and the remaining C4 Morita families have nontrivial gradings. Grossman's Theorem 4.13 and Lemma 4.7 settle that known Morita family, not the unrestricted existence question. The odd-cyclic Q-dual classification of arXiv:2609.25185 does not cover the even-order4 frontier.

Sources:
- https://arxiv.org/pdf/2108.01564
- https://arxiv.org/pdf/1612.07185
- https://arxiv.org/pdf/1401.1879
- https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/jlms.12789
- https://www.cambridge.org/core/services/aop-cambridge-core/content/view/A505D85D2DFAE10E90305BE5BB5B7637/S0008439523000334a.pdf/div-class-title-irrational-braided-generalized-near-groups-div.pdf

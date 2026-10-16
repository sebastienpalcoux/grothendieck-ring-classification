# A Morita-dual obstruction for R8_2_260

**Status:** general exclusion, independently audited. The shorter direct cyclic-module proof in `CYCLIC_STABILIZER_DIVISIBILITY.md` is used in the manuscript. This file preserves an alternative Morita-dual argument. No pivotality assumption is used.

Suppose C categorifies R8_2_260. Put d=3+2sqrt(3). Its positive dimension character is

    (1,1,1,d,d,d,d,3).

The subset E={0,1,2,7} is the near-group ring C3+2: its invertibles form C3, fix b7, and b7²=b0+b1+b2+2b7. These invertibles fix each of b3,b4,b5,b6 on both sides as well.

Since a noninvertible simple is fixed by C3, the pointed associator is trivial. Thus A=b0+b1+b2 is a connected separable algebra, and B=A-bimod(C) is a fusion category.

By Etingof–Gelaki–Ostrik, *Classification of fusion categories of dimension pq*, arXiv:math/0304194v2, Lemma6.2 and Theorem7.1, the full fusion subcategory E'=A-bimod(E) is pointed with group G=N⋊C3, where |N|=4 and C3 acts fixed-point-freely. Necessarily N=C2×C2 and G=A4. This applies to the specific regular algebra A used here, as is explicit in the proof of Theorem7.1; it is not an arbitrary Morita-equivalent pointed category. There are precisely twelve invertibles in E': three over the orbit {b0,b1,b2}, and nine over the fixed simple b7.

Each outside simple bi, 3≤i≤6, is fixed by the full left-right C3×C3 action. The corresponding A-bimodule block is the projective representation category of its stabilizer, with some 2-cocycle. For C3×C3 the twisted group algebra is either C^9 or M3(C). Thus this block contributes either nine simple bimodules of FP dimension d/3, or one of FP dimension d. The first option is impossible: d/3=1+(2/3)sqrt(3) has norm −1/3 and is not an algebraic integer. Hence B has exactly twelve invertibles, with group A4, and four other simple objects, all of FP dimension d.

For any noninvertible simple X in B, its product XX* has dimension

    d²=3+6d.

The number of invertible summands is the order of its stabilizer under G, since all such summands occur once. Irrationality of d forces this stabilizer order to be3. Therefore its orbit has size4 and consists of all four noninvertible simples. In particular B is a generalized near-group category.

The stabilizer of a noninvertible simple in a generalized near-group category is normal in the group of invertibles (Dong–Sun, arXiv:2004.08735v1, Proposition3.3(1); alternatively Schopieray, *Categorification of integral group rings extended by one dimension*, published Lemma2.8(e)). This would give a normal subgroup of order3 in A4, which does not exist. Contradiction.

All categorical inputs above hold for arbitrary complex fusion categories. The left-right stabilizer calculation is the usual orbit/projective-representation description of equivariant objects for a finite pointed action. The scalar cocycle is not assumed trivial: both possible twisted group algebras are explicitly retained and integrality rules out the split case.

# Independent audit of the R189 pointed-associator reduction

23 October 2026. **Conclusion: the proposed structural theorem is valid**, after explicitly including the short argument identifying the ten restrictions in \(I(1)\). It proves that every hypothetical complex categorification has pointed subcategory tensor-equivalent to \(\mathrm{Vec}_{C_5}\). It does not yet exclude the entire ring.

## 1. Cyclic indicator and primitive twists

Write \([\omega]=k\in H^3(C_5,\mathbf C^\times)\cong\mathbf Z/5\). For the standard representative
\[
\omega(a,b,c)=\zeta_5^{ka\lfloor(b+c)/5\rfloor},
\]
the product of \(\omega(1,m,1)\), \(m=0,\ldots,4\), equals \(\zeta_5^k\). The cyclic-indicator formula therefore gives \(\nu_5(g)=\zeta_5^{\pm k}\), with the sign depending on associator conventions. In particular it is primitive when \(k\ne0\).

A precise primary source for the indicator product is Mignard–Schauenburg, *Morita equivalence of pointed fusion categories of small rank*, [arXiv1708.06538v1](https://arxiv.org/html/1708.06538v1), §3.3 and Corollary3.3: their convention uses the inverse product \(\pi_{-5}(g)\). The positive spherical structure restricts to the canonical positive structure on the pointed subcategory.

The induction trace identity and equality in the triangle inequality imply \(\theta_Z^5=\nu_5(g)\) for every \(Z\subset I(g)\). Thus a nontrivial pointed associator forces these twists to be primitive25th roots. This uses positivity; the reduction from an arbitrary complex categorification to a pseudo-unitary Galois conjugate is available by published Schopieray Lemma3.1. A nonzero cyclic cohomology class remains nonzero under such conjugation, so the eventual conclusion extends back to the original complex category.

## 2. Normalized modular Galois symmetry: no missing anomaly or sign

Put \(D=\dim\mathcal C\). For \(Z(\mathcal C)\), the Gauss sums satisfy \(p^+=p^-=D\), and its global dimension is \(D^2\). Hence \((s,t)=(S/D,\theta)\) itself is a normalized modular pair. The center Gauss sum is also recalled in Ostrik, *Pivotal fusion categories of rank3*, [arXiv1309.4822](https://arxiv.org/pdf/1309.4822), Example2.6.

Bruillard–Ng–Rowell–Wang, [arXiv1310.7050v3](https://arxiv.org/html/1310.7050v3), equation(2.13) and Theorem2.9(b), therefore give
\[
v_{\widehat\sigma Z}=\epsilon_\sigma(Z)T_\sigma v_Z,
\qquad \theta_{\widehat\sigma Z}=\sigma^2(\theta_Z).
\]
The first identity was independently audited in `center_galois_independent_audit.md`; it follows from \(s_{A_\chi,Z}=\chi(FZ)/f_\chi\). The second has **no extra central-charge scalar** here.

Choose \(\sigma\) restricting to \(\zeta_{25}\mapsto\zeta_{25}^2\). Such an automorphism extends to the full cyclotomic field; its exponent must be chosen coprime to the full conductor (in particular odd on an even conductor). It is not necessary or appropriate to use exponent2 on the full field.

The exact restriction transform is
\[
a'_i=a_{3i},\qquad b'_i=\sum_j a_j-a_{3i}-b_{3i},
\]
with indices modulo5. Its fourth power is the identity. For pointed-supported restrictions the Galois sign is +1, since the invertible coefficient remains a positive basis vector. Thus \(\widehat\sigma^4\) preserves each such restriction vector and each relevant induction block. Its action on primitive25th-root twists is raising to
\[
2^8\equiv6\pmod{25}.
\]
Since6 has order5 modulo25, every orbit has length divisible by5. An orbit could have length10 or another multiple of5; the proof only needs divisibility by5. Consequently the number of distinct central simples having any one restriction vector is divisible by5.

## 3. Ten multiplicity-free constituents and complementary pairs

The four vanishing indicator moments of \(I(g)\), together with the common fifth twist power, give total dimension \(D/5=2+4d\) in each of five twist eigenspaces. A constituent with invertible restriction multiplicity \(a\) contributes rational coefficient \(a^2\) to that dimension. Thus each eigenspace has two simple constituents, each with \(a=1\). This proves the ten-constituent, multiplicity-free claim independently of any Gram search.

Nonnegativity under the restriction transform bounds all allowed noninvertible coefficients by1. Each allowed coordinate occurs5times in \(F(I(g))\). Together with the divisibility-by5 statement this forces five copies of a subset restriction and five copies of its complementary subset restriction. A single ten-element orbit with only one restriction vector would require an allowed binary coordinate to satisfy \(10b=5\), which is impossible.

The four nontrivial induction blocks are related by \(T_\sigma\), so the full40-column contribution is determined by one unordered complementary subset pair.

## 4. Explicit justification for the I(1) contribution

The formal codegrees give dimensions \(1,1+4d,(1+d)^4,(1+3d)^4\). All restriction columns are binary, contain1, and omit \(X_0\). Hence the dimension1 and dimension\(1+4d\) columns have empty and full nonzero subsets. Let \(c_i\) count the singleton columns at \(X_i\), and let \(e_i\) count triple columns missing \(X_i\), for \(i=1,2,3,4\).

The coefficient5 of \(X_i\) in \(FI(1)\) gives
\[
1+c_i+4-e_i=5,\qquad c_i=e_i.
\]
Galois invariance of \(I(1)\) sends the singleton at \(i\) to the triple missing \(2i\), so \(e_{2i}=c_i\). Therefore the \(c_i\) are constant around the four-cycle multiplication by2. Their sum is4, so all are1. This proves the asserted \(I(1)\) Gram contribution without relying on prior computational enumeration:
\[
(G_0)_{00}=(G_0)_{0i}=0,
\quad(G_0)_{ii}=5,
\quad(G_0)_{ij}=3\quad(i,j\ne0,\ i\ne j).
\]

## 5. Independent exact residual checks

I recomputed the40 nontrivial-block columns by applying the integer transform, without using the saved residual matrices, and subtracted them and \(G_0\) from \(15I_5+15J_5\). The eight unordered complementary choices are represented by bits on \((0,2,3,4)\) with the first bit0. Every residual diagonal equals10.

| Bits | A negative-minor witness, or final obstruction |
|---|---|
|0000|Five central invertibles with the same underlying \(g\)|
|0001|\(Q_{12}=12\), determinant \(-44\)|
|0010|\(Q_{14}=12\), determinant \(-44\)|
|0011|\(Q_{14}=12\), determinant \(-44\)|
|0100|\(Q_{14}=12\), determinant \(-44\)|
|0101|\(Q_{14}=12\), determinant \(-44\)|
|0110|\(Q_{12}=12\), determinant \(-44\)|
|0111|\(Q_{01}=15\), determinant \(-125\)|

As an additional independent check, I allowed every one of the35 nonnegative integer vectors \((c_1,c_2,c_3,c_4)\) summing to4, without imposing their proved equality. Set \((G_0)_{ij}=5-c_i-c_j\) off diagonal. Each of the seven proper complementary pairs still gives a negative two-by-two minor for all35 choices. For the first six, the zero-cooccurrence edges of the40-column contribution cover all four nonzero indices; some positive \(c_i\) then forces \(Q_{ij}=10+c_i+c_j>10\). For0111, \(Q_{0j}=15\) directly. Thus the Gram contradiction is robust to this intermediate count.

## 6. Empty/full case and conclusion

Five empty-subset restrictions yield five distinct invertible central objects with the same underlying invertible \(g\). If two existed, their quotient would be a central lift of1 and hence a monoidal natural automorphism of \(\mathrm{Id}_{\mathcal C}\). Such an automorphism has scalars \(u\) on \(g\) and \(v\) on \(x\). The rules give \(v^2=1\) and \(v^2=u^jv\) for \(j=1,2,3,4\). Hence \(u=v=1\), and the automorphism is trivial. Therefore a fixed invertible has at most one central lift.

This eliminates the final pair and proves \([\omega]=0\). It is a new necessary structural constraint on any categorification, rather than a complete exclusion of R189.

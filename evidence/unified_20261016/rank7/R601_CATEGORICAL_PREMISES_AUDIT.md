# Independent audit of the categorical premises for R7_3_601

Audit date: 2026-10-16. Scope: the general-complex categorical reductions used before the finite induction-lattice obstruction. This audit does not convert numerical optimizer failure into a proof.

## Source ring and nonbraiding

I independently loaded ring (multiplicity 3, index 601) from the rank-seven census. Its canonical compact-JSON tensor SHA-256 is

`afbed9441f88f4ba296235d0dd6220f41ecbcf97a7424220125e73f255ff489c`.

The positive character is d=(1,5,5,8,8,9,10), with squared sum 360. I checked every one of its 49 product identities, and checked that each of the six nonidentity basis elements generates the entire based ring. Consequently any categorification is integral, nonpointed, and simple. Integrality implies pseudo-unitarity and a canonical positive spherical structure; no pivotality assumption is imposed on the initial categorification.

If such a category C were braided, simplicity forces its Müger center to be Vec or C. The first possibility makes it modular, contradicting the modular divisibility condition 360/5² being an algebraic integer. The second makes it symmetric. By Deligne, its underlying fusion ring would then be a representation ring of a finite group, also impossible as follows.

The two exact character rows

a=(1,0,0,-2,3,-1,0),  b=(1,2,-1,-1,-1,0,1)

both satisfy all 49 character identities. Their weighted Schur expression is

sum_i a_i² b_i/d_i = -5/8.

For an ordinary group representation ring this expression is nonnegative: characters of that based ring are evaluations at conjugacy classes; if a corresponds to K and b to L, the coefficient of the class sum of L in the square of the class sum of K is

(|K|²/|G|) sum_i chi_i(K)² conjugate(chi_i(L))/chi_i(1).

Here the rows are real, and the positive prefactor does not change the sign. A class-sum product counts factorizations and has nonnegative integer coefficients. This excludes every finite group without invoking the Schur-product criterion outside its unitary scope.

The symmetric argument also covers a super-Tannakian structure: forgetting that symmetric structure gives the same representation fusion ring. Thus C admits no braiding.

## Simplicity of the center

I independently read Liu–Palcoux–Ren, arXiv:2102.01663v4, Theorem 5.1 and its proof on PDF page 9. It states for a nonpointed simple complex fusion category that its Drinfeld center is simple exactly when the category has no braiding. All hypotheses have just been verified for C.

The nonpointed qualification is relevant when using the adjacent modular-or-symmetric discussion: pointed exceptions such as sVec do not enter here. No unitary assumption occurs in Theorem 5.1.

## Center dimensions

The forgetful functor Z(C) -> C preserves Frobenius–Perron dimensions. Since every underlying object of C has integral dimension, every simple of Z(C) has integral dimension z. The center is modular with its positive spherical structure and has dimension 360².

The modular divisibility theorem (LPR Theorem 5.9, citing EGNO Proposition 8.14.6) implies 360²/z² is an algebraic integer. This is rational, hence an integer. Prime-by-prime valuations then give exactly z | 360. This argument is not the unproved general Frobenius-divisibility conjecture for arbitrary fusion categories.

The center is nonpointed and simple, so it has no nonidentity invertibles: such an object would generate a nontrivial pointed proper fusion subcategory. The prime-power-dimension theorem (LPR Theorem 5.10, its source Corollary 6.16) says that a nondegenerate integral braided complex fusion category containing a simple object of nontrivial prime-power dimension contains a nontrivial symmetric fusion subcategory. In a simple modular category of dimension greater than one that is impossible. Therefore every nonunit central simple has dimension among

6,10,12,15,18,20,24,30,36,40,45,60,72,90,120,180,360.

## Status

All categorical premises used to remove the prime-power columns are valid for an arbitrary complex categorification of R7_3_601. An exact exhaustive induction/lattice contradiction using these premises would exclude general complex categorification. This file does not itself certify the completeness or infeasibility of the finite search.

Primary source read: https://arxiv.org/pdf/2102.01663v4, Section 5, Theorems 5.1, 5.9, 5.10, Proposition 5.3, and Remark 5.15.

I also independently read the original stated prime-power theorem and proof in Nikshych, arXiv:1208.0840, Corollary 6.16, PDF pages 33–34. Its hypotheses are nondegenerate integral braided over characteristic zero; there is no unitarity assumption. The exponent is explicitly positive, so the unit is not removed by that theorem. Nonidentity invertibles are removed separately by simplicity above.

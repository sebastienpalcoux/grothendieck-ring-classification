# Literature routes for the six remaining rank-10 multiplicity-one rings

Working research note, 23 October 2026. This note records primary-source checks and deductions; it does not assert a categorification or exclusion that has not been proved. The working ring data are `research/catalogue.json` and the recovered prior evidence package. No online repository has been changed by this investigation.

## 1. Scope and arithmetic

The cases 114, 115, 152, 153, 179 have dimensions
\[
1^4,(2+2\sqrt2)^2,(3+2\sqrt2)^4,
\qquad D=96+64\sqrt2=(8+4\sqrt2)^2.
\]
Their common formal-codegree polynomial is
\[
(t-16)^3(t-8)^5(t^2-192t+1024).
\]
The existing prior evidence gives the spherical/Galois reduction needed to pass to a pseudo-unitary categorification if a complex categorification exists. The dimension test alone is not an exclusion.

Case 189 is a commutative two-orbit fusion ring with invertible group \(G=C_5\), trivial stabilizer, and a self-dual choice \(\rho\) with
\[
\rho g=g\rho,\qquad
\rho^2=1+\sum_{g\ne1}g\rho.
\]
Here \(d=2+\sqrt5\), \(d^2=1+4d\), and
\[
D=5+5d^2=50+20\sqrt5,\qquad N_{\mathbf Q(\sqrt5)/\mathbf Q}(D)=500.
\]
The noninvertible coefficient vector is nonuniform: one zero and four ones. This distinction prevents direct application of the usual generalized-Haagerup construction/classification.

## 2. What the current low-rank literature actually supplies

Gert Vercleyen and Joost Slingerland, **On Low-Rank Multiplicity-Free Complex Fusion Categories**, Communications in Mathematical Physics 407, article 231 (2026), DOI [10.1007/s00220-026-05705-2](https://link.springer.com/article/10.1007/s00220-026-05705-2), classifies/computes through rank seven, not rank ten. It supplies lower-rank building blocks, including the pseudo-\(PSU(2)_6\) category, but no classification of these six rank-ten tensors. Its discussion of a corrected zero-pattern issue in older Anyonica calculations also prevents treating older numerical counts as a general theorem of nonexistence.

Zhengwei Liu, Scott Morrison, David Penneys, **1-supertransitive subfactors with index at most 6 1/5**, CMP334 (2015), 889–922, DOI [10.1007/s00220-014-2160-4](https://doi.org/10.1007/s00220-014-2160-4), [arXiv1310.8566](https://arxiv.org/html/1310.8566v1), constructs the pseudo-\(PSU(2)_6\) examples among three subfactors of index \(3+2\sqrt2\). The two pseudo examples are complex conjugates and are not braided; the paper uses a weaker sigma-braiding. Therefore one must not import the transparent-fermion braiding of ordinary \(PSU(2)_6\) into the pseudo category merely from similar fusion rules.

The pseudo category \(\mathcal Q\) has simples \(1,f,x,y\), with
\[
f^2=1,\quad fx=y,\quad x^*=y,
\quad x^2=y^2=f+x+y,\quad xy=1+x+y.
\]
Its universal grading is trivial. Author-maintained exact category data are indexed at [AnyonWiki, FR_4_1_2_4](https://anyonwiki.github.io/pages/FRPages/FR_4_1_2_4.html).

## 3. A useful restriction on pseudo-PSU products

Fabian Mäurer and Ulrich Thiel, **Computing the center of a fusion category**, [arXiv2406.13438v3](https://arxiv.org/html/2406.13438v3), 15 October 2026, Table7.1, computes the centers of the four pseudo-\(PSU(2)_6\) classes \(F^{4,1,2}_{4,j,a,b}\). The table gives rank14 centers and a maximal simple fusion subcategory of rank7 having half the center dimension. For ordinary \(PSU(2)_6\), the corresponding simple subcategory listed is rank2 and dimension2. The exact data behind the displayed decimals should be retained if this table is used in a final proof.

The following is a deduction from that computed rank7 subcategory, rather than a theorem quoted verbatim from the paper. Let \(\mathcal K\subset Z(\mathcal Q)\) be the simple rank7 fusion subcategory of dimension \(48+32\sqrt2\). Its Müger center, being a fusion subcategory of a simple category, is either Vec or all of \(\mathcal K\). The latter would make \(\mathcal K\) symmetric, which is impossible because a symmetric fusion category over \(\mathbf C\) has integer Frobenius–Perron dimension. Thus \(\mathcal K\) is nondegenerate. Müger decomposition gives
\[
Z(\mathcal Q)\simeq\mathcal K\boxtimes\mathcal B,
\qquad\operatorname{FPdim}(\mathcal B)=2.
\]
Consequently \(\mathcal B\) is semion or antisemion. Since \(U(\mathcal Q)=1\), the kernel of \(\operatorname{Inv}(Z(\mathcal Q))\to\operatorname{Inv}(\mathcal Q)\) is trivial; the central nontrivial invertible therefore underlies \(f\). Its self-braiding is \(\pm i\), and its pointed associator is the nontrivial class of \(H^3(C_2,\mathbf C^\times)\).

This creates an obstruction to a tempting construction, not an obstruction to the five rings themselves:

* In \(\mathcal Q\boxtimes\mathcal Q\), the diagonal central invertible \(f\boxtimes f\) is a fermion, so \(1\oplus(f\boxtimes f)\) is not a central commutative algebra for that central structure.
* In \(\mathcal Q\boxtimes\overline{\mathcal Q}\), the diagonal is a boson, so central condensation can be available.
* However, the semion sign distinguishes \(\mathcal Q\) and \(\overline{\mathcal Q}\) as tensor categories when the central invertible and spherical structure are unique. An ordinary factor-permutation action requires an actual tensor equivalence between the factors. It must not be assumed.

A proposed final construction needs exact half-braiding/associator data or an independent theorem establishing the relevant central structure. It cannot follow only from the based ring.

## 4. The existing ordinary-PSU model is already accounted for

The recovered `work/resolve_rank10_quadratic/model21.tex` constructs case21 as
\[
\left((\mathcal P\boxtimes\mathcal P)^{C_2}\right)_{1\oplus(f,f)_{-}},
\qquad\mathcal P=PSU(2)_6.
\]
The categorical inputs are canonical permutation equivariantization and central Tannakian condensation. Its fixed-point calculation gives four invertibles forming \(C_2^2\), all simples self-dual, and the exact case21 tensor. This is not a new model for one of the five unresolved cases.

One possible route to other models is a different genuine action on the rank8 central quotient \((\mathcal P\boxtimes\mathcal P)_{1\oplus(f,f)}\), or a Morita-dual category obtained from a nonpointed algebra in a product of rank4 categories. Both are only routes at this stage. Ring-level equivariance and a nonnegative induction matrix do not provide associators.

## 5. Exact literature scope for case189

Jingcheng Dong and Hua Sun, **Structure, examples and classification for generalized near-group fusion categories**, Journal of Algebra568 (2021), 386–407, [arXiv2004.08735](https://arxiv.org/html/2004.08735v1): Proposition3.6 shows, when the noninvertible coefficient vector is nonzero, that the adjoint category is the least nonpointed fusion subcategory; the classification is reduced to the case of trivial universal grading. This does not classify arbitrary categories with trivial universal grading.

Andrew Schopieray, **Irrational braided generalized near-groups**, Canadian Mathematical Bulletin (2023), [arXiv2212.14009](https://arxiv.org/pdf/2212.14009), published Theorem3.6 (Theorem1 in arXiv v1): an irrational braided generalized near-group category is a product of a pointed braided category and a Fibonacci or \(PSU(2)_6\) adjoint factor. Therefore case189 has no braided categorification. This statement does not exclude nonbraided categorifications.

Pinhas Grossman, Masaki Izumi, Noah Snyder, **Graded Extensions of generalized Haagerup categories**, [arXiv2201.11901](https://arxiv.org/html/2201.11901v1), §1 and §2.4, works with generalized-Haagerup rules
\[
gX=Xg^{-1},\qquad X^2=1+\sum_{g\in G}gX
\]
plus cohomological conditions. Case189 has both a different commutation automorphism and a different coefficient vector. Those construction and extension theorems cannot be directly applied.

A proposed blanket principle that a commutative free invertible action with odd \(G\) forces exponent2 is false: \(\mathrm{Fib}\boxtimes\mathrm{Vec}_G\) is a counterexample. Extra assumptions concerning the adjoint category would be essential. No applicable theorem with those extra assumptions was located in this search.

## 6. Corrected Galois restriction and a conditional Cauchy obstruction

Andrew Schopieray, **Categorification of integral group rings extended by one dimension**, JLMS108 (2023), 1617–1641, DOI [10.1112/jlms.12789](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/jlms.12789), §3.1, studies the Galois action on dimensions in the center. Care is needed with Lemma3.6: the displayed calculation establishes equality of squares. Its stated inequality cannot be applied when the coefficient of1 is zero. Section4.1 itself allows center simples having pure noninvertible restriction.

Here is a direct calculation for case189, avoiding the sign problem. For a central simple \(Z\), write its positive dimension as \(a+bd\), with \(a,b\ge0\) integral. For the nontrivial quadratic Galois action,
\[
\dim(\widehat\sigma Z)^2=(a+(4a-b)d)^2.
\]
If \(a>0\), uniqueness of the expression in the basis \(1,d\), together with nonnegative restriction coefficients, forces the positive sign and \(0\le b\le4a\). If \(a=0\), the negative sign is allowed and yields \(bd\) again. Thus pure noninvertible-supported center simples are **not excluded**.

The same paper's Lemma3.7 and Proposition3.8 imply, in the pseudo-unitary situation, that for \(g^5=1\) and a simple \(Z\subset I(g)\),
\[
\theta_Z^5=\nu_5(g),\qquad\nu_5(g)^5=1,
\qquad\theta_Z^{25}=1.
\]
This may also be proved directly using the induction trace identity and equality in the triangle inequality with positive dimensions.

Paul Bruillard, Siu-Hung Ng, Eric Rowell, Zhenghan Wang, **Rank-finiteness for modular categories**, JAMS29 (2016), 857–881, [arXiv1310.7050v3](https://arxiv.org/html/1310.7050v3), **Theorem3.9**: for a spherical fusion category, the prime ideals dividing its global dimension and its Frobenius–Schur exponent coincide in the conductor cyclotomic ring. The exponent equals the order of the twist of its center.

Our arithmetic consequence is: the prime2 divides the norm500 of the global dimension, so the exponent is even. Since every pointed-induced central simple has twist order dividing25, some center simple must have no invertible summand in its restriction and must have even-order twist. Therefore an independent proof that every central simple is pointed-induced would exclude case189. The Galois dimension formula alone does **not** prove that premise.

The stronger statement that all center twists have order dividing25 was considered and explicitly withdrawn after checking the sign. It must not enter a manuscript or classification table.

## 7. Current conclusion of this literature branch

No complete categorification or exclusion of one of the six cases follows from this literature branch alone. The concrete additions are: the pseudo-PSU semion restriction on candidate constructions; an unconditional exclusion of braided realizations of case189; a correctly delimited conditional Cauchy obstruction; and the precise hypotheses showing why generalized-Haagerup and existing generalized-near-group classification results do not settle case189. The independent tensor/Gram/action investigations may strengthen these partial results.


## 8. Later primary-source result for ordinary PSU2_6 autoequivalences

Cain Edie-Michell, *The Brauer–Picard groups of fusion categories coming from the ADE subfactors*, [arXiv1709.04721v2](https://arxiv.org/pdf/1709.04721), **Lemma4.10**, proves
\[
\operatorname{Aut}_\otimes(\operatorname{Ad}(A_7))\cong C_2.
\]
The proof explicitly states that there are no gauge autoequivalences and identifies the nontrivial autoequivalence as exchanging \(f^{(2)}\) and \(f^{(4)}\). Thus for ordinary \(PSU(2)_6\) the kernel of tensor autoequivalences on the based ring is trivial. This is stronger than \(\operatorname{Aut}_\otimes(\mathrm{Id})=1\). The paper considers the ADE categories and their Galois conjugates. No corresponding precise theorem for pseudo-\(PSU(2)_6\) was found in this search.

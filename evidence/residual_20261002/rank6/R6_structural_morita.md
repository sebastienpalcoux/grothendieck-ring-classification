# Final structural pass: braided Morita models and group constructions

Date: 2 October 2026. These are additional model restrictions, not a categorification or a nonexistence theorem for either residual ring. These results are included in the dated rank-six research addendum. The frozen 1 October release remains unchanged.

## 1. Neither residual has a Tannakian subcategory in its center

**Reusable criterion.** Let M be a pseudo-unitary braided fusion category with its canonical positive ribbon structure. Suppose the rational norm of FPdim(M), taken in a number field containing it, has at most two prime divisors, and the unit is its only invertible object of twist one. Then M contains no nontrivial Tannakian fusion subcategory.

Proof. If Rep(G) embeds as a braided fusion subcategory, categorical Lagrange implies FPdim(M)/|G| is an algebraic integer. Taking its field norm shows that every prime dividing |G| divides the norm of FPdim(M). Burnside's theorem makes G solvable. A nontrivial finite solvable group has a nontrivial one-dimensional character, whose image is a nonunit invertible object. The positive spherical structure restricts to the canonical positive structure on Rep(G), so this object has twist one. Contradiction.

For the established positive Galois forms of the two residuals, the complete central invertible inventories are:

- R6_4_155: twists 1, -1, i, -i (up to conjugation);
- R6_8_1660: twists 1, -1.

Put D=FPdim(C). Exact arithmetic gives

    Norm_Q(sqrt2)/Q(D155)=72^2-2*48^2=576=2^6*3^2,
    Norm_Q(sqrt2,sqrt3)/Q(D1660)=147456=2^14*3^2.

Since FPdim(Z(C))=D^2, both center norms have only primes 2,3. The criterion applies.

**Morita consequence.** No category Morita equivalent to either residual can be a nontrivial faithful finite-group extension or a nontrivial finite-group equivariantization. Each of those constructions supplies a central Tannakian Rep(G), and braided centers are Morita invariant. This excludes the construction as a last operation, including after Morita equivalence. It does NOT exclude inverse operations (de-equivariantization, taking a neutral component), general connected-etale condensation, or arbitrary chains allowing such inverses.

**General-complex scope.** The previous release proves that every complex categorification of either ring admits a positive pseudo-unitary Galois form. Centers, Morita contexts, braided embeddings and Tannakian fiber functors transport under the same Galois conjugation. A hypothetical Tannakian subcategory or listed construction for the original category would therefore give one for the positive form, where the contradiction holds. We do not use twists from an arbitrary nonpositive pivotal structure.

## 2. R6_8_1660 has no braided Morita representative

The complete frozen Morita reduction applies to every indecomposable finite semisimple module category, not merely pivotal functors or selected algebra supports. Its steps are:

1. Restriction to Ising has n regular blocks. The irreducible Perron matrix U+sqrt(2)R satisfies a degree-two irreducible polynomial over Q(sqrt2); simplicity of its Perron root forces n=2. Every indecomposable module therefore has rank six.
2. The exact four-row based-module list exhausts all such nonnegative integer matrices.
3. Module-character reciprocity and positive Lagrangian dimension saturate the full-center support for every row; the dual action is faithful and has rank six or eight.
4. The finite linking-Gram factorization exhausts all possible simple dual actions. The indicator comparison removes one rank-eight possibility.

Thus every Morita dual has one of three based rings: original R1660; the rank-six Ad(E6) extension; or the retained noncommutative rank-eight ring.

The original ring already has no braiding, by its Ising subcategory and braided decomposition. A noncommutative based ring cannot be the Grothendieck ring of a braided category. It remains to exclude a braiding on the rank-six Ad(E6) extension.

That ring contains the rank-three fusion subring

    g^2=1, gS=S, S^2=1+g+2S, FPdim(S)=1+sqrt(3).

Suppose this subcategory is braided in a positive pseudo-unitary form. Monodromy with the invertible g gives scalar charges compatible with fusion. Since S occurs in S^2, its charge mu satisfies mu=mu^2, hence mu=1. Since g occurs in S^2, its charge is also one. Thus g is transparent in this subcategory. The balancing equation and gS=S give theta_g=1. In the canonical positive ribbon structure this is the Tannakian Rep(C2), not a transparent fermion.

De-equivariantize by its regular algebra A=1+g. The free-module image F(S) satisfies

    dim End_A(F(S))=dim Hom(S,S tensor A)=2.

It therefore splits into two distinct simple modules. Its underlying object is 2S; each summand has underlying object S. The FP dimension of either summand in the module fusion category is consequently

    (1+sqrt(3))/2.

Its quadratic norm is -1/2, so it is not an algebraic integer, impossible for a simple object of a fusion category. This proves the required rank-three obstruction.

Pseudo-unitarity is Morita invariant: both ordinary global dimension and Frobenius--Perron global dimension are preserved under Morita equivalence. Their equality therefore passes to every dual, giving the positive structure used above. Finally, the already established Galois transport carries any hypothetical braiding and Morita context to the positive form. Hence **no complex categorification of R6_8_1660 is Morita equivalent to a braided fusion category**.

The analogous no-braided-Morita theorem for R6_4_155 was already proved in the frozen release.

## 3. No extra Morita-ring exclusion results

The term 'Ad(E6) extension' in the retained rank-six candidate does not mean a faithful group-graded extension. Its Y-square contains Y. Direct exact closure of the supports of i*i* in all six stored dual tensors gives the entire based ring in every case. Both rank-eight tensors are noncommutative. Thus the no-Tannakian theorem does not remove any of the three remaining Morita rings; each already has trivial universal grading.

`verify_morita_structure.py` and `morita_structure_receipt.json` record these small integer/rational checks and bind the dual-action input by SHA256. These checks do not re-enumerate module categories or reconstruct centers.

## Primary sources and precise inputs

- Frozen chapter `supplements/rank6/papers/chapters/frontier_1660_morita.tex`: Uniform module rank; Complete based-module list; Full-center saturation; Complete integral Morita Gram reduction; Morita second-indicator exclusion.
- Frozen chapter `frontier_1660.tex`, Corollary `cor:1660-no-braiding`; `frontier_155.tex`, Proposition `prop:155-no-braided-morita`, including the complete invertible-twist inventory.
- Etingof--Nikshych--Ostrik, *On fusion categories*, https://annals.math.princeton.edu/2005/162-2/p01, Theorem 2.15 (global dimension under Morita duality), Corollary 8.14 (FP dimension), Proposition 8.23 (canonical positive spherical structure).
- Etingof--Gelaki--Nikshych--Ostrik, *Tensor Categories*, https://math.mit.edu/~etingof/egnobookfinal.pdf, Theorem 7.17.6 (algebraic-integral dimension quotient), Proposition 8.23.1 (central Rep(G) for equivariantization), Proposition 8.23.11 (central Rep(G) for faithful grading), and Section 8.23 (de-equivariantization). Its Section 9.15 also uses the classical Burnside solvability argument.
- Gelaki--Naidu--Nikshych, *Centers of graded fusion categories*, https://msp.org/ant/2009/3-8/ant-v3-n8-p05-s.pdf, Corollary 3.7 and Section 3C.

The independent model-literature auditor approved both new arguments subject to the explicitly checked frozen prerequisites above. Neither conclusion supplies a model or excludes general, pivotal, spherical, pseudo-unitary or unitary categorifiability itself.

# A unified algebraic 2D2 obstruction

**Theorem.** None of `R8_2_152`, `R8_2_153`, `R8_2_166`, or `R8_2_495` is the Grothendieck ring of a fusion category over the complex numbers. No pivotal, spherical, pseudo-unitary, or unitary hypothesis on a hypothetical categorification is required.

The argument first constructs a positive-dimensional algebraic planar algebra from a forced module category. It then proves that its depth-three generator is conjugate, by a complex graph gauge, to the known unitary 2D2 generator. A mismatch of dual ranks gives the contradiction. The same proof treats all four tensors.

## 1. The common module graph

In each tensor the neutral component D of a faithful C2 grading has basis `1,g,r,gr` and rules

\[
 g^2=1,\qquad gr=rg,\qquad r^2=1+2r+2gr.
\]

The odd component M contains a simple X such that both XX* and X*X are 1+r. The ordered left and right multiplication graphs of X are both the rooted graph Gamma with edges

\[
01,\ 12,\ 23,\ 24,\ 35,\ 45,\ 56,\ 67,
\]

root 0 and even vertices 0,2,5,7. This is 2D2. The graph-vertex-to-census permutations, with zero-based census labels, are:

| tensor | graph vertices 0,1,2,3,4,5,6,7 |
|---|---|
| R8_2_152 | 0,1,5,3,4,7,2,6 |
| R8_2_153 | 0,1,5,3,4,7,2,6 |
| R8_2_166 | 0,3,7,1,2,6,4,5 |
| R8_2_495 | 0,2,6,4,5,3,7,1 |

The source-bound graph verifier checks these statements against every relevant ordered coefficient of the archived tensors, including closure, the faithful grading, the two internal ends, and generation of D by r. In particular neither even side is a proper subcategory hidden inside a larger rank-four category: both internal ends generate the full neutral category. Both even sides have rank four.

## 2. An algebraic pivotal planar algebra without an ambient pivotal assumption

The two distinct FP dimensions of D are 1 and d=2+sqrt(5). By Schopieray [S, Lemma 3.1], D is Galois conjugate to a pseudo-unitary fusion category. Apply the same field automorphism to the entire hypothetical category. This preserves its tensors, grading, and module category. We may therefore equip D with its canonical positive spherical structure. We do not impose a pivotal structure on the original rank-eight category.

Schaumann [Sch, Proposition 5.8] supplies the FP module trace on M. Give the regular D-module D its spherical trace, and give N=D direct-sum M the sum trace. Normalize the odd trace so that dim(X)=delta=sqrt(1+d). These are positive, nonzero weights on all simple objects. Theorem 4.5 of [Sch] constructs double-adjoint isomorphisms for module functors between **different** traced module categories and proves compatibility with composition. Consequently

\[
\mathcal E=\operatorname{Fun}_{D}(N,N)
\]

is a pivotal multifusion category, with its two distinguished diagonal units corresponding to D and M. Its two diagonal fusion categories are spherical by [Sch, Proposition 5.10(iv)]; Corollary 4.6 gives the compatible trace on the common module. This construction uses ordinary nondegenerate trace pairings, not Hermitian forms.

Let F_X:D -> M be the module functor a -> aX. Its adjoint is m -> mX*. Thus F_X* F_X and F_X F_X* correspond respectively to XX* and X*X. The generation statements in Section 1 imply that F_X and its dual generate the relevant linking category. The algebraic pivotal correspondence [EH, Theorem 3.45] therefore gives a connected semisimple shaded planar algebra P. Its rooted principal graph and dual graph are the two graphs verified in Section 1. Its scalar modulus is delta, and its trace pairings are nondegenerate.

For clarity, the graph embedding used here is algebraic. Forgetting module constraints gives a faithful tensor functor

\[
\operatorname{Fun}_{D}(N,N)\longrightarrow\operatorname{End}_{\mathbb C}(N).
\]

It is pivotal: both double-adjoint maps are constructed from the same trace pairings on N. This is also the criterion of [EH, Theorem 3.69], whose statement includes the nonunitary setting. Choose bases in the one-dimensional edge spaces and dual bases in the reverse edge spaces. Inserting the simple-object resolutions of the identity identifies the target planar box spaces with path matrix blocks. The evaluation and coevaluation factors are the square roots of ratios of the trace weights. These are precisely the state-sum factors in [EH, Definition 3.72 and proof of Theorem 3.75]. Thus P embeds into the graph planar algebra of Gamma with its positive FP weights. We use this explicit pivotal construction, not the unitary-only wording of [EH, Theorem 3.77].

There is no Frobenius-Schur choice for identifying X with X*: the basic strand is shaded and has different source and target units. All evaluation choices are accounted for by the dual edge bases and the pivotal trace.

## 3. The forced depth-three generator

The graph is 2-supertransitive. At depth three the Jones-Wenzl corner is

\[
f^{(3)}P_{3,+}f^{(3)}=\mathbb Cp\oplus\mathbb Cq,
\qquad p+q=f^{(3)},\quad pq=0.
\]

The two new depth-three vertices have equal FP weights, so tr(p)=tr(q). Set T=p-q. Then

\[
 T^2=f^{(3)},\qquad \operatorname{tr}(T)=0.
\]

The trace pairing makes T orthogonal to TL_3: f^(3) kills the other TL blocks, and its own pairing with T is zero. Any cap of T pairs trivially with every element of P_2 because the corresponding cup lies in TL_3. Nondegeneracy forces every cap to vanish. Conversely, at this depth the common cap kernel is one-dimensional. Hence two-click rotation acts on T by a cube root of unity. This establishes uncappability and the exact square normalization without self-adjointness, positivity of an inner product, or a presumed rotational eigenvalue.

## 4. Exact complex classification inside the graph planar algebra

Write z=sqrt(5), phi=(1+z)/2. The FP weights in graph order are

\[
\mu=(1,\delta,d,\delta\phi,\delta\phi,d,\delta,1).
\]

Use rectangular lopsided coordinates with parity-rescaled weights

\[
w=(1,1,d,\phi,\phi,d,1,1).
\]

A loop (v0,...,v5) denotes the matrix entry between paths (v0,v1,v2,v3) and (v0,v5,v4,v3). If D_p=sqrt(w(p1)w(p2)) on a length-three path p, the rectangular matrix is D times the spherical matrix times D^-1. Thus its loop coefficient differs by sqrt(w1 w2/(w5 w4)). Spherical two-click right rotation has coefficient sqrt(mu0 mu3/(mu1 mu4)); this diagonal change gives

\[
 T(v_4,v_5,v_0,v_1,v_2,v_3)
 =\omega\frac{w(v_0)w(v_5)}{w(v_2)w(v_1)}T(v_0,v_1,v_2,v_3,v_4,v_5).
\]

In these coordinates rectangular caps are unweighted sums over the inserted backtracking vertex. Indeed the spherical TL projection has entries sqrt(mu(p_i)mu(q_i))/sum_{a~p_(i-1)}mu(a), and the diagonal change makes them w(p_i)/sum_{a~p_(i-1)}w(a). Ordinary matrix multiplication is vertical stacking.

The primitive rotations are ruled out over the abstract field Q(z,omega), with z²=5 and omega²+omega+1=0. The cap and rotation equations on the 152 loop coefficients have rank 144. Substitution of a complete eight-dimensional basis into T²=f^(3) gives 90 distinct normalized quadratic equations. **A constant linear combination of five of these equations is 1.** The adjacent `gpa_omega_certificate.json` records the five coefficients; `verify_gpa_omega_certificate.py` reconstructs the equations directly and checks the identity with exact fractions. Because this is an identity in the abstract number field, it excludes both primitive cubic roots. No conjugation or reality equation is used. This independently verifies and strengthens the auditability of [MP, Lemma 3.2].

For omega=1 the cap and rotation space again has dimension eight. Choose coordinates at the loops

\[
012321,\ 212323,\ 212354,\ 212453,
\quad232323,\ 232354,\ 232453,\ 235453.
\]

In coordinates x0,...,x7 the ideal of T²=f^(3) is exactly

\[
\begin{aligned}
 x_0+(3+z)x_7/2&=0,&x_1+(3-z)x_7/2&=0,\\
 x_2+2x_5&=0,&x_3+2x_6&=0,\\
 x_4+(z-1)x_7/2&=0,\\
 x_5x_6&=(5z-11)/2,&x_7^2&=(7-3z)/2.
\end{aligned}
\]

The equality of ideals is certified in both directions: all 82 distinct square equations reduce to zero by these seven generators, and each generator is an explicit polynomial combination of square equations of total degree at most three. The certificate does not divide by any unknown variable. `verify_gpa_certificate.py` reconstructs all graph inputs and checks these identities using only rational arithmetic in Q(sqrt(5)).

Put k=(3-z)/2 and c=(5z-11)/2. Both are nonzero. Every complex solution is obtained from epsilon in {+1,-1} and lambda in C^x by

\[
 x_7=\epsilon k,\qquad x_5=\epsilon\sqrt c\lambda,
 \qquad x_6=\epsilon\sqrt c/\lambda,
\]

and the five linear equations. This parameterization covers every complex solution, including all exceptional specializations.

Multiplying the directed edge 3->5 by lambda and the reverse edge by lambda^-1 defines a graph planar algebra automorphism: internal factors cancel in each state sum. The winding exponents of the eight coordinates are (0,0,1,-1,0,1,-1,0). Hence every solution is complex-gauge conjugate to one of the two solutions at lambda=1. Those base matrices satisfy T H=H T^t, H[p,p]=w(p1)w(p2), so their spherical forms are self-adjoint. Both full Laurent parameter families, the primitive winding exponents, and this self-adjointness are independently checked by the verifier. The two signs generate the same planar subalgebra.

## 5. No hidden higher-depth extension and the contradiction

By [MP, Lemma 3.4 and the construction proving Theorem 1.1], a self-adjoint, uncappable rotation-one solution with T²=f^(3) generates the known unitary 2D2 planar algebra P0. After the complex graph gauge, P therefore contains P0. The two planar algebras have the same positive principal graph Gamma. For every n, the dimension of their positive n-box space is the number of length-2n loops on Gamma based at its root. Thus each inclusion P0_(n,+) subset P_(n,+) is an equality. Rotation identifies the corresponding negative box spaces for n>0, and both zero-box spaces are one-dimensional. Therefore P=P0. This dimension argument precludes additional higher-depth extension data without applying a unitary classification theorem directly to the unknown P.

The dual even category of P0 has **six** simples; its dual principal graph is displayed in [MP, Theorem 1.1]. The source tensors force the dual even category of P to have **four** simples. This contradiction proves the theorem.

## Scope, replay, and sources

This argument does not classify all abstract categorifications of the rank-four 2D2 ring. It classifies the particular positive-dimensional algebraic planar algebra forced by the module with internal end 1+r and principal graph 2D2. Thus it does not presume an unproved passage from pseudo-unitarity to unitarity, and does not use the unitary tetrahedral-symmetry step in the general Z/2-quadratic classification.

The source-bound wrapper replays the graph identification and both portable GPA certificates. All arithmetic verifiers also pass with Python optimization enabled. The JSON files contain rational coefficients and the exact polynomial identities; discovery notebooks and numerical computations are unnecessary.

- [S] A. Schopieray, *Categorification of integral group rings extended by one dimension*, J. London Math. Soc. 108 (2023), 1617–1641, Lemma 3.1.
- [Sch] G. Schaumann, *Traces on Module Categories over Fusion Categories*, J. Algebra 379 (2013), 382–425; [arXiv:1206.5716v3](https://arxiv.org/abs/1206.5716v3), Theorem 4.5, Corollary 4.6, Propositions 5.8 and 5.10(iv).
- [EH] P. Grossman, S. Morrison, D. Penneys, E. Peters, N. Snyder, *The Extended Haagerup fusion categories*, Ann. Sci. Éc. Norm. Supér. 56 (2023), 589–664; [arXiv:1810.06076](https://arxiv.org/abs/1810.06076), Theorems 3.45 and 3.69, Definition 3.72 and proof of Theorem 3.75. The unitary-only Theorem 3.77 is not invoked in the algebraic bridge.
- [MP] S. Morrison, D. Penneys, *2-supertransitive subfactors at index 3+sqrt(5)*, J. Funct. Anal. 269 (2015), 2845–2870; [arXiv:1406.3401](https://arxiv.org/abs/1406.3401), Theorem 1.1 and Lemmas 3.2 and 3.4.

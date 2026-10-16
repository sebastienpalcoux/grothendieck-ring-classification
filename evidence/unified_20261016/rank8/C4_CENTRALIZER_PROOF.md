# A unitary braided construction of R8_2_666

**Theorem.** The census ring R8_2_666 admits a unitary braided categorification: the centralizer of the full pointed subcategory in the Drinfeld center of a near-group C4+4 category.

## Categorical existence

Grossman–Izumi, *Infinite families of potential modular data related to quadratic categories*, arXiv:1906.07397, §3.2.3.1, explicitly identify the smallest hyperbolic example with the actual Drinfeld centers of the two complex-conjugate near-group C4+4 categories. Their statement precedes, and is separate from, their conjecture for larger groups. They cite Izumi, *The structure of sectors associated with Longo–Rehren inclusions. II. Examples*, Rev. Math. Phys. 13(5) (2001), 603–674, Theorem 6.8, equations (6.18)–(6.21), and Example A.2. The underlying near-group C*-categories also appear in Evans–Gannon, arXiv:1208.1500, Proposition 6/Table 2.

Bonderson–Rowell–Wang, *On Realizing Modular Data*, arXiv:1910.07061, §2.4.1, independently state the existence of these hyperbolic examples and supply convenient complete labels and the center matrix. We use the hyperbolic example only; no categorical realization of the other candidate metric forms is assumed.

Let C be this existing unitary modular center. Put G=C4×C4 and H=C16×C2, with quadratic forms and involutions

\[
q_G(x,y)=i^{-xy},\quad \theta_G(x,y)=(y,x),\qquad
q_H(x,y)=\zeta_{32}^{3x^2}i^{y^2},\quad
\theta_H(x,y)=(3x+8y,x+y).
\]

The fixed subgroups are both K=C4, embedded by k↦(k,k) in G and k↦(4k,k mod 2) in H. The pointed objects of C are K, with restricted twist q_K(k)=i^{-k²}. Their full subcategory P has dimension four. Its centralizer B=P' is a unitary braided fusion category. Its Müger center is the Tannakian order-two radical of P, so B is not asserted to be modular.

## Complete centralizer basis

Choose the transversals

\[
G_*=[(1,0),(2,0),(2,1),(3,0),(3,1),(3,2)],
\]
\[
H_*=[(1,0),(2,0),(3,0),(4,0),(5,0),(9,0),(10,0),
(0,1),(1,1),(2,1),(5,1),(6,1),(7,1),(13,1)].
\]

The 28 center simples are K, K×{π}, G_*, H_*. Their dimensions are respectively 1, 3+2√2, 4+2√2, 2+2√2. The monodromy test S_{k,Y}=S_{0,Y} for every k∈K selects precisely

\[
(0,0),\ (2,2),\ (0,0,\pi),\ (2,2,\pi),\
(3,1)_G,\ (2,1)_H,\ (6,1)_H,\ (4,0)_H.
\]

This is also the explicit set J_ad in BRW §2.4.2. Its dimension profile is

\[
(1,1,3+2\sqrt2,3+2\sqrt2,4+2\sqrt2,
2+2\sqrt2,2+2\sqrt2,2+2\sqrt2),
\]

with total squared dimension 96+64√2. The center has dimension 384+256√2, so the centralizer dimension formula independently confirms completeness.

## Exact tensor identification

Write B_G(x,y)=q_G(x)q_G(y)/q_G(x+y) and similarly B_H. With α=1/4 and β=1/(4√2), the normalized center S matrix has blocks, in the order K,Kπ,G_*,H_*,

\[
\begin{pmatrix}
(\alpha-\beta)B_G/2&(\alpha+\beta)B_G/2&\alpha B_G&\beta B_H\\
(\alpha+\beta)B_G/2&(\alpha-\beta)B_G/2&\alpha B_G&-\beta B_H\\
\alpha B_G&\alpha B_G&\alpha(B_G(x,y)+B_G(\theta_Gx,y))&0\\
\beta B_H&-\beta B_H&0&-\beta(B_H(x,y)+B_H(\theta_Hx,y))
\end{pmatrix}.
\]

Embeddings of K into G or H are understood in mixed blocks. The standard-library certificate `verify_c4_centralizer.py` reconstructs this matrix directly in Z[ζ32], with ζ32^16=−1 and √2=ζ32^4+ζ32^−4. It uses the integral scaling U=16S. The scaled inverses 4/U_{0j} are 4+2√2, 4−2√2, 1, √2 in the four blocks, so every Verlinde coefficient is an integer-ring expression divided by 1024. No floating-point arithmetic or numerical embedding is used.

The verifier checks all 784 unitarity identities; identifies the complete pointed centralizer by the S-row criterion; evaluates all 1,792 coefficients N_{ij}^k with i,j in its eight labels and k in the full 28-label center; verifies closure, nonnegative integrality, and self-duality; checks all 4,096 associativity equations; and matches all 512 coefficients against the SHA-256-bound census tensor. The model-to-census map is

\[
(0,1,3,4,7,2,5,6).
\]

The source tensor SHA-256 is
`cfbe81aa760b11ab636b164d65c6985bafe05d675eeae0404a42b0ebc4c0d35b`.

The existence theorem is categorical; the exact finite calculation identifies its Grothendieck ring. Normal and Python `-O` replays pass identically. This settles R8_2_666 affirmatively in every existence scope through unitarity. It makes no status assertion about the distinct, non-self-dual ring R8_2_342.

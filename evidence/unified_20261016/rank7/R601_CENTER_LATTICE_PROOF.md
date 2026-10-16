# R7_3_601: general exclusion by the center induction lattice

## Theorem and scope

The source ring `R7_3_601` admits no fusion-category categorification over the complex numbers. No unitary, pivotal, or braided structure is assumed. Its integral Frobenius–Perron dimensions force pseudo-unitarity; the obstruction then uses the simplicity of its Drinfeld center and exact central induction.

The source is line 2455 of `supplements/rank7/data/rank7_tables.txt.gz`, with compact-JSON tensor SHA-256

`afbed9441f88f4ba296235d0dd6220f41ecbcf97a7424220125e73f255ff489c`.

The proof separates a categorical reduction from an exhaustive finite arithmetic certificate. The latter consists entirely of integer arithmetic, rational matrix inversion, and congruences modulo 2 or 3. Numerical optimization is not part of the proof or verifier.

## 1. A hypothetical category has simple integral center

Write the source basis as \(X_0=1,X_1,\ldots,X_6\). Its positive dimension character is

\[
d=(1,5,5,8,8,9,10),\qquad D=\sum_i d_i^2=360.
\]

The verifier checks every character identity and that each nonidentity basis element generates the entire based ring. Thus a hypothetical categorification \(\mathcal C\) is integral, simple, and nonpointed. Integrality implies pseudo-unitarity, with its canonical spherical structure [ENO, Proposition 8.24].

The category cannot be braided. Otherwise its Müger center, being a fusion subcategory of a simple category, is trivial or all of \(\mathcal C\). In the first case \(\mathcal C\) is modular, but modular divisibility would require \(D/d_1^2=360/25\) to be an algebraic integer, which it is not [EGNO, Proposition 8.14.6; LPR, Theorem 5.9]. In the second case it is symmetric and its fusion ring is a finite-group representation ring, including the super-Tannakian possibility. The source has exact character rows

\[
a=(1,0,0,-2,3,-1,0),\qquad b=(1,2,-1,-1,-1,0,1),
\]

but

\[
\sum_{i=0}^6\frac{a_i^2b_i}{d_i}=-\frac58.
\]

For a finite-group representation ring, its ring characters are evaluations at conjugacy classes. The coefficient of the class sum of a class \(L\) in the square of the class sum of a class \(K\) is the displayed expression times the positive factor \(|K|^2/|G|\), when \(a,b\) correspond to \(K,L\). All rows here are real. A class-sum product counts factorizations, so that coefficient cannot be negative. This excludes the symmetric case without extending a unitary-only criterion to arbitrary fusion categories.

By LPR, Theorem 5.1, a nonpointed simple complex fusion category that admits no braiding has simple Drinfeld center. Consequently \(\mathcal Z(\mathcal C)\) is simple, integral and modular, of dimension \(D^2=129600\). Integrality follows because the forgetful functor preserves Frobenius–Perron dimensions.

Let \(A\ne1\) be a central simple, of integer dimension \(z\). Modular divisibility gives \(D^2/z^2\in\mathbb Z\), hence \(z\mid360\). Simplicity rules out nonidentity invertibles. LPR, Theorem 5.10 (Nikshych, Corollary 6.16), says a nondegenerate integral braided category containing a simple of nontrivial prime-power dimension has a nontrivial symmetric fusion subcategory. This is impossible in our simple modular center. Thus

\[
z\in\mathcal D=\{6,10,12,15,18,20,24,30,36,40,45,60,72,90,120,180,360\}.
\]

These are precisely the divisors of 360 greater than one that are not prime powers.

## 2. Exact central-induction constraints

Let \(F:\mathcal Z(\mathcal C)\to\mathcal C\) be forgetful and \(I\) its adjoint. For every central simple \(A\), put

\[
m_A=([F(A):X_i])_{i=0}^6\in\mathbb Z_{\ge0}^7.
\]

Frobenius reciprocity and \(FI(X)\cong\bigoplus_Y Y\otimes X\otimes Y^*\) give

\[
\sum_A m_A m_A^t=B,\qquad B=\sum_a N_aN_a^t.
\]

In the source basis,

\[
B=\begin{pmatrix}
7&6&6&5&9&9&10\\
6&32&23&39&39&45&49\\
6&23&32&39&39&45&49\\
5&39&39&71&60&73&78\\
9&39&39&60&75&69&78\\
9&45&45&73&69&85&88\\
10&49&49&78&78&88&106
\end{pmatrix}.
\]

The complete orthogonal character table, checked directly against every source product, is

\[
\begin{array}{rrrrrrr}
1&1&1&0&0&1&-2\\
1&0&0&1&0&-1&0\\
1&0&0&-2&3&-1&0\\
1&-1&-1&0&0&1&0\\
1&2&-1&-1&-1&0&1\\
1&-1&2&-1&-1&0&1\\
1&5&5&8&8&9&10
\end{array}.
\]

Its formal codegrees are \(8,3,15,4,9,9,360\). Since the based ring is commutative, the seven simple constituents of \(I(1)\) have multiplicity one. Their dimensions are \(D/f\), namely

\[
1,24,40,40,45,90,120
\]

[Ostrik, Theorem 2.13]. The dimension-one constituent is the central unit, whose forgetful row is \(e_0\).

Write the other six rows as \(\ell_1,\ldots,\ell_6\), in the indicated dimension order, and order the two dimension-40 rows lexicographically. They obey

\[
\ell_{a,0}=1,\qquad \ell_a\cdot d=z_a,\qquad
\sum_a\ell_a=Be_0-e_0,
\]

and every partial remainder \(B-e_0e_0^t-\sum_{a\le k}\ell_a\ell_a^t\) is entrywise nonnegative and positive semidefinite. The coordinate bounds

\[
0\le\ell_{a,i}\le\min(B_{0i},\lfloor\sqrt{B_{ii}}\rfloor)
\]

make the search finite. The verifier enumerates the full integer boxes with the dimension equations and only these necessary conditions. It uses exact Schur elimination, treating a zero diagonal pivot by requiring its entire row to vanish. There are exactly **336** possible six-row blocks. The dimension-specific row domains contain 14, 44, 66, 542, and 1101 rows for dimensions 24, 40, 45, 90, and 120. The recursion node counts, by depth, are

\[
1,8,78,212,398,336,336.
\]

Thus no numerical spectral threshold or preexisting list of blocks is used for coverage.

## 3. The uniform modular obstruction

Fix one of the 336 blocks. Delete coordinate zero from the remaining Gram matrix to obtain a positive-definite integer \(6\times6\) matrix

\[
R=(B-e_0e_0^t-\sum_a\ell_a\ell_a^t)_{1\ldots6,1\ldots6}.
\]

Each remaining central simple has forgetful row \((0,v)\), with \(v\in\mathbb Z_{\ge0}^6\). Such a row must satisfy:

1. \(v\cdot(5,5,8,8,9,10)\in\mathcal D\);
2. \(v_iv_j\le R_{ij}\) for all \(i,j\);
3. \(v^tR^{-1}v\le1\).

The third condition follows from \(R-vv^t\succeq0\); for positive-definite \(R\), it is exactly the rank-one Schur-complement condition. It does not assume a bound on the number or multiplicities of central simples.

All rows belong to the finite box \(0\le v_i\le\lfloor\sqrt{B_{i+1,i+1}}\rfloor\). The dimension condition and the initial entrywise bounds leave 4700 rows before the block-specific tests; each block retains between 1 and 111 rows. Rational inversion is exact: the verifier computes a positive integer \(h\) and an integer matrix \(H=hR^{-1}\), checks \(RH=hI\), and tests \(v^tHv\le h\).

Index the lower-triangular matrix entries by

\[
(0,0),(1,0),(1,1),(2,0),(2,1),(2,2),\ldots,(5,5).
\]

For every block, the certificate provides \(p\in\{2,3\}\) and \(y\in\mathbb F_p^{21}\) such that

\[
y\cdot\operatorname{vech}(vv^t)=0\pmod p
\quad\text{for every admissible row }v,
\qquad
y\cdot\operatorname{vech}(R)=1\pmod p.
\]

There are 218 certificates modulo 2 and 118 modulo 3. These identities contradict

\[
R=\sum_{A\notin I(1)}v_Av_A^t,
\]

regardless of repetitions among the rows. This rules out every possible block and proves the theorem.

For example, the first block has only three admissible rows. Its dual vector is the coordinate functional on matrix entry \((1,0)\), modulo 2: all three admissible outer products have an even entry there, while the residual matrix has an odd entry there. The remaining blocks use exactly the same finite-field argument; their complete data are in the adjacent certificate.

## 4. Reproduction and audit

Run from any directory:

```sh
python /absolute/path/to/evidence/unified_20261016/rank7/verify_r601_center_lattice.py --repo /absolute/path/to/repo
```

The script loads the immutable source census and checks its ledger identity, tensor associativity, self-duality, exact characters, simplicity, global dimension, and the nonbraiding arithmetic. It regenerates all low blocks, exhausts every possible remaining row, and checks all 336 congruence certificates. It uses only Python's standard library and explicit checks, so optimized Python does not disable any mathematical check.

Files:

- `verify_r601_center_lattice.py` — source-bound exhaustive exact verifier;
- `r601_center_lattice_certificate.json` — low-row blocks and finite-field dual vectors;
- `r601_center_lattice_normal.json`, `r601_center_lattice_optimized.json` — replay receipts;
- `R601_CATEGORICAL_PREMISES_AUDIT.md` — independent categorical audit.

## References

- ENO: P. Etingof, D. Nikshych, V. Ostrik, *On fusion categories*, Annals of Mathematics 162 (2005), Proposition 8.24, https://doi.org/10.4007/annals.2005.162.581.
- EGNO: P. Etingof, S. Gelaki, D. Nikshych, V. Ostrik, *Tensor Categories*, AMS (2015), Proposition 8.14.6.
- LPR: Z. Liu, S. Palcoux, Y. Ren, *Interpolated family of non-group-like simple integral fusion rings of Lie type*, https://arxiv.org/abs/2102.01663, v4, Section 5, Theorems 5.1, 5.9, 5.10 and Remark 5.15.
- D. Nikshych, *Morita equivalence methods in classification of fusion categories*, Contemporary Mathematics 585 (2013), Corollary 6.16, cited in LPR Theorem 5.10.
- V. Ostrik, *Pivotal fusion categories of rank 3*, Moscow Mathematical Journal 15 (2015), Theorem 2.13 and Proposition 2.4, https://doi.org/10.17323/1609-4514-2015-15-2-373-396. The central-induction statements apply at arbitrary rank.

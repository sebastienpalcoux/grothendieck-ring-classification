# A cyclic-induction, STS, and fourth-moment obstruction for R8_1_18

## Theorem and scope

The based ring **R8_1_18 admits no categorification by a complex fusion
category**. The proof uses a pseudo-unitary Galois conjugate, cyclic induction,
the full character-labelled modular STS identity, and a finite exact
nonnegative-cone certificate. It does not assume unitarity or classify
associators. The criterion name is
`cyclic_induction_STS_fourth_moment`.

The immutable source tensor has SHA-256
`cdd3aa4477861e8521c75ac63cb0f9e4e5d0a021073d1619aae358a0850704f2`.
It is the eighteenth lexicographically sorted tensor of exact multiplicity
one in `supplements/rank8/data/rank8_tables.txt.gz`. In model order its rules
are

\[
 a^4=1,\qquad a\rho=\rho a,\qquad
 \rho^2=a+\sum_{j=0}^3a^j\rho.
\]

The model-to-source permutation is
\((1,a,a^2,a^3,\rho,a\rho,a^2\rho,a^3\rho)
\mapsto(0,1,7,2,3,6,5,4)\). In what follows indices are source indices.
Put

\[
 d=2+\sqrt5,\quad d^2=1+4d,\quad K=\mathbb Q(\sqrt5),\quad
 D=8+16d=40+16\sqrt5.
\]

The pointed indices are \(0,1,2,7\); the other four indices are
\(3,4,5,6\). All four nonpointed simples are nonselfdual. The published
two-FP-dimension Galois pseudo-unitarity theorem [S, Lemma 3.1] permits us to
replace any hypothetical complex categorification by a pseudo-unitary
Galois conjugate. We use its canonical positive spherical structure. Every
dimension and positivity assertion below refers to this structure.

## 1. Induction, actual character labels, and the eight low frames

Let \(F:Z(\mathcal C)\to\mathcal C\) be forgetful and \(I\) its right
adjoint. For a central simple \(Z\), write
\(v_Z=( [FZ:X_i])_{i=0}^7\). The induction Gram identity is

\[
 \sum_Zv_Zv_Z^{\mathsf t}=C,\qquad
 C_{ij}=\sum_{k,l}N_{ki}^{l}N_{kj}^{l}.
 \tag{1}
\]

The source gives \(C_{0,*}=(8,0,0,4,4,4,4,0)\), and the pointed block is
\(8I_4\). Thus a central restriction row contains at most one distinct
pointed label.

In addition to the two FP characters, of formal codegrees \(D,\bar D\),
there are six characters of formal codegree eight:

\[
 \chi_{r,\epsilon}(a)=\zeta_8^{2r},\qquad
 \chi_{r,\epsilon}(\rho)=\epsilon\zeta_8^r,
 \qquad r=1,2,3,\quad\epsilon=\pm1.
 \tag{2}
\]

All eight characters are one-dimensional. Their actual associated central
simples \(A_\chi\subset I(1)\) occur once, have twist one, and have
dimensions \(D/f_\chi\). In particular their restriction rows are

\[
 e_0,\qquad J=(1,0,0,1,1,1,1,0),\qquad
 b_{r,\epsilon}=e_0+\text{two nonpointed constituents}.
 \tag{3}
\]

The last description follows directly by comparing the coefficients of
\(1,d\) in \(D/8=1+2d\). After removing \(e_0,J\) from (1), each
nonpointed coordinate occurs three times among those six low rows.

The labels in (2) cannot be assigned arbitrarily to rows of equal dimension.
Actual character reciprocity requires
\(\chi(b_\psi)=\psi(b_\chi)\); duality requires the dual row to carry
the dual character. To enumerate all possibilities, take the ten
nonnegative four-tuples of sum two for each of the six profiles, impose
coordinate sums three, reciprocity, and duality. The dual profile in model
nonpointed order sends its coordinate \(j\) to \(-1-j\bmod4\).
These explicit conditions leave exactly **eight** assignments. The replay
enumerates them afresh from (2); it does not load a saved list. All eight
have a positive-semidefinite, entrywise nonnegative residual in (1).

## 2. A cyclic Fourier multiplicity bound

The induction indicator formula [NS] reads

\[
 \sum_Z v_{Z,i}\dim(Z)\theta_Z^m=D\nu_m(X_i).
 \tag{4}
\]

Suppose \(a\) is invertible of order four. Its fourth indicator is a unit
complex number \(\eta\), whereas its first three indicators vanish.
Since the sum of the positive weights on the left at \(m=0\) is \(D\),
equality in the triangle inequality at \(m=4\) forces
\(\theta_Z^4=\eta\) whenever \(v_{Z,a}>0\). Fourier inversion of the
equations for \(m=0,1,2,3\), on these four possible phases, gives weight
\(D/4\) in **each** phase.

A row containing \(a\) has dimension \(v_{Z,a}+B_Zd\), since the pointed
off-diagonal entries of (1) are zero. Therefore in each individual phase

\[
 \sum_{\theta_Z=\lambda i^j}
 v_{Z,a}(v_{Z,a}+B_Zd)=D/4=2+4d.
\]

Comparing constant coefficients gives
\(\sum v_{Z,a}^2=2\). Consequently

\[
 v_{Z,1}\le1,\qquad v_{Z,2}\le1.
 \tag{5}
\]

This argument is independent of the pointed associator class. It applies
to both order-four generators and uses individual phases before taking
any relative field trace.

Write \(k\in H^3(C_4,\mathbb C^\times)=\mathbb Z/4\) for that class,
with a convention in which
\(\nu_4(a)=i^k\) and \(\nu_2(a^2)=(-1)^k\). The conventions for a
generator or its inverse do not change the three cases below. Thus on
the support of an order-four generator \(\theta^4=i^k\), and on the
support of \(a^2\), \(\theta^2=(-1)^k\). The cases \(k=1,3\) have
identical relative moment restrictions and are combined as the odd case.

## 3. Complete Galois row orbits and exact row bounds

For a restriction row \(v\), put
\(A=\sum_{i\in\{0,1,2,7\}}v_i\),
\(B=\sum_{i=3}^6v_i\), so \(\dim Z=A+Bd\). Character-labelled modular
Galois symmetry gives the following generators on row types.

First the automorphism flipping \(K\) and fixing \(\zeta_8\) gives

\[
 T(v)_i=v_i+\boldsymbol1_{\{3,4,5,6\}}(i)(A-B/2),
 \tag{6}
\]

up to one overall sign, chosen to make the row nonnegative. If it has no
integral nonnegative signed value, \(v\) is impossible. Formula (6)
follows either by inverting the full character matrix or by checking the
two FP characters and the six characters (2): their nonpointed sums
vanish, while the FP pair is exchanged with its modular dimension factor.

The automorphism \(\zeta_8\mapsto\zeta_8^3\), fixing \(K\), gives the
based permutation

\[
 P(a^j)=a^{3j},\qquad P(a^j\rho)=a^{3j+1}\rho,
\]

or \(P=(0,2,1,6,5,4,3,7)\) in source notation. Source duality is
\(U=(0,2,1,4,3,6,5,7)\). These three transformations generate the row
orbit used in the proof; their formulas and every source character
identity are checked exactly.

There is one common relative phase distribution throughout each such
orbit. Indeed, for a modular Galois permutation,
\(\theta_{\pi_\sigma Z}=\sigma^2(\theta_Z)\), since the center has
trivial anomaly. Every \(\sigma^2\) fixes the quadratic field \(K\).
Normalized relative trace \(t_K\) is invariant under automorphisms fixing
\(K\), hence

\[
 t_K(\theta_{\pi_\sigma Z}^m)=t_K(\theta_Z^m)
 \quad(m\ge1).
 \tag{7}
\]

Duality preserves ribbon twists as well. The induced bijections between
central simples having different row types preserve the entire relative
moment vector. Thus their counts and their relative-phase histograms are
equal. This statement does not require the actual twists to be equal.

Let \(R\) be (1) after subtracting one of the eight low frames. Every high
row has \(v_0=0\), \(v_i\le\lfloor\sqrt{R_{ii}}\rfloor\), and (5).
We also impose the necessary algebraic integrality of \(D/\dim Z\).
For a simple in the modular center, its squared quotient is a formal
codegree, hence an algebraic integer; its square root is consequently an
algebraic integer as well. If
\(n=A^2+4AB-B^2\), then

\[
 \frac D{A+Bd}=x+yd,
 \qquad x=\frac{8A+16B}{n},\quad y=\frac{16A-8B}{n}.
\]

The correct maximal-order test is that both
\(2x+4y\) and \(x^2+4xy-y^2\) are integers. It is not necessary that
\(x,y\) themselves be integers.

For every candidate orbit we subtract once every distinct row's outer
product from \(R\). The remainder must be entrywise nonnegative and
positive semidefinite. This is necessary even when several central
simples have the same restriction row. The replay uses rational Schur
elimination, including the zero-pivot condition, rather than numerical
eigenvalue thresholds. These exhaustive exact filters leave **25** row
orbits for each low frame.

## 4. An exact thirteen-point relative moment domain

By the general spherical Cauchy theorem [BNRW, Theorem 3.9], global
dimension and Frobenius--Schur exponent have the same prime-ideal support
in the cyclotomic integer ring. This theorem applies to spherical fusion
categories, including nonintegral and nonbraided ones; its proof passes
through their centers. Here

\[
 N_{K/\mathbb Q}(D)=320=2^6\cdot5.
\]

If a rational prime does not divide this norm, \(D\) is a unit at every
prime above it, including in any cyclotomic extension. The Cauchy theorem
therefore excludes that prime from the exponent. Every central twist has
order \(2^a5^b\).

Consider the ordered triple
\((t_K(\theta),t_K(\theta^2),t_K(\theta^4))\). If \(b\ge2\), all
three entries vanish: none of the exponents \(1,2,4\) removes the
primitive fifth-power conductor above five. If \(a\ge4\), all three
entries again vanish: even the fourth power still has primitive
two-power part of order at least four, with trace zero over \(K\).
Otherwise the order divides forty. Hence the exact domain is the
thirteen distinct triples obtained from all fortieth roots together
with the zero triple. No bound on the exponent's prime powers is assumed.

For reproducibility, the primitive fifth-root traces are
\(u_+=(d-3)/4\), \(u_-=(1-d)/4\); the two-part contributes its rational
normalized Ramanujan trace. The replay computes the thirteen triples
directly and multiplies each coefficient by eight to make every moment
column integral.

The pointed-support restrictions from Section 2 replace this domain by:

| Support | Pointed class | Allowed relative triples |
|---|---|---|
| \(a\) or \(a^{-1}\) | 0 | \((1,1,1),(-1,1,1),(0,-1,1)\) |
| \(a\) or \(a^{-1}\) | 2 | \((0,0,-1)\) |
| \(a\) or \(a^{-1}\) | odd | \((0,0,0)\) |
| \(a^2\) | even | \((1,1,1),(-1,1,1)\) |
| \(a^2\) | odd | \((0,-1,1)\) |

## 5. The full unweighted STS constraint

Let \(C_{\chi i}=\chi(X_i)\) now denote the character matrix (distinct
from the Gram matrix in (1)), put
\(X=\operatorname{diag}(f_\chi^{-1})C\), and let \(B\) have rows
\(b_\chi=F(A_\chi)\). The actual character correspondence [O] gives,
for **every** central simple \(Z\),

\[
 S_{A_\chi,Z}=\chi(FZ)/f_\chi=(Xv_Z)_\chi.
\]

Normalize \(S_{1Z}=\dim Z/D\). The center is anomaly-free, and all
\(A_\chi\) have twist one. Its relation
\(STS=T^{-1}ST^{-1}\), restricted to these rows and columns, gives

\[
 X\Big(\sum_Z\theta_Zv_Zv_Z^{\mathsf t}\Big)X^{\mathsf t}=XB^{\mathsf t}.
\]

Character orthogonality implies \(X^{-\mathsf t}=\overline C\), so

\[
 \boxed{\ \sum_Z\theta_Zv_{Z,i}v_{Z,j}
 =\sum_\chi b_{\chi,i}\overline{\chi(X_j)}.\ }
 \tag{8}
\]

This is unweighted: no factor \(\dim Z\) appears. Taking normalized
trace to \(K\), (2)--(3) give, for all nonunit indices,

\[
 \sum_Zv_{Z,i}v_{Z,j}t_K(\theta_Z)=
 \begin{cases}4-d,&i,j\in\{3,4,5,6\},\\0,&\text{otherwise}.\end{cases}
 \tag{9}
\]

The six non-FP characters have nonpointed values of trace zero from
\(\mathbb Q(\zeta_8)\), which is disjoint from \(K\). The conjugate-FP
row contributes \(4-d\). The pointed-column cancellations follow from
the actual low profiles; the replay checks all 392 entries over all eight
frames, so none of these cancellations is assumed for arbitrary
equal-codegree assignments. A separate independent source verifier and
audit accompany this proof.

## 6. A fourth-moment equation with no unknown indicator

For each \(X_i\), its fourth indicator is the trace of a rotation of
order four on \(\operatorname{Hom}(1,X_i^{\otimes4})\). Consequently
\(\nu_4(X_i)\in\mathbb Q(i)\), and its normalized trace to the real
quadratic field \(K\) is rational. Define

\[
 \ell(x+yd)=2x-y.
\]

Since \(\ell(D)=0\), taking the relative trace of (4), with \(m=4\),
and applying \(\ell\) eliminates its entire unknown right side:

\[
 \ell\Big(\sum_Zv_{Z,i}\dim Z\,t_K(\theta_Z^4)\Big)=0.
 \tag{10}
\]

No fourth-indicator value, bound, reality assumption, or tensor-block
rotation formula is used. In particular no third or fifth indicators
are required. For the second moments in (4), all nonunit indicators
vanish except \(\nu_2(X_7)=(-1)^k\).

## 7. Exact separating inequalities

After subtracting the known low rows, form a column for each of the 25
row orbits and each compatible triple in Section 4. One common triple
per orbit is legitimate by (7); taking nonnegative mixtures permits any
actual histogram of phases. Each column records these 119 coordinates:

1. the 28 upper-triangular entries of the residual Gram matrix on
   indices 1 through 7;
2. the two coefficients in the basis \(1,d\) for each of the seven
   first and seven second induction moments (28 coordinates);
3. the seven projected fourth moments (10);
4. the two coefficients for each upper-triangular STS moment (56
   coordinates).

The Gram coordinates are unscaled; all other coordinates are multiplied
by eight. Let \(M\) be the integer matrix of these columns and \(b\)
the source-derived target vector. A categorification necessarily yields
\(Mx=b\) with \(x\ge0\). It is enough to contradict this relaxation;
no integrality assumption on \(x\) is needed.

The accompanying JSON supplies one sparse integer covector for each of
the three effective pointed classes. Direct integer multiplication gives:

| Pointed class | Low frames | Row orbits per frame | Columns per frame | Nonzero covector entries | Minimum column pairing | Target pairing |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 8 | 25 | 167 | 16 | 0 | -256 |
| 1 or 3 | 8 | 25 | 145 | 12 | 0 | -256 |
| 2 | 8 | 25 | 153 | 12 | 0 | -256 |

Thus every branch has \(yM\ge0\) but \(yb=-256\), which is impossible
when \(x\ge0\). This completes the general-complex exclusion.

For a compact human-readable specification of the covectors, write
\(G_{ij}\) for Gram coordinates, \(M^n_{i,1},M^n_{i,d}\) for the
scaled induction coordinates, \(L_i\) for the scaled projected fourth
coordinate, and \(S_{ij,1},S_{ij,d}\) for scaled STS coordinates. All
unlisted coefficients are zero:

\[
\begin{aligned}
y_0={}&-192G_{11}+224G_{33}-32(G_{34}+G_{35}+G_{45})\\
 &-16M^1_{2,d}+6M^1_{5,d}-4M^1_{7,d}
 -6M^2_{1,d}+12M^2_{4,1}-5M^2_{7,d}-4L_6\\
 &-6(S_{34,1}+S_{45,1}+S_{46,1})+26S_{55,1},\\[2pt]
y_{\rm odd}={}&-256G_{11}+256G_{44}-13M^1_{3,d}
 +4M^2_{4,d}-28M^2_{6,1}+9M^2_{7,d}-8L_5\\
 &+137S_{33,1}-55(S_{34,1}+S_{35,1}+S_{36,1})+128S_{66,d},\\[2pt]
y_2={}&-192G_{11}-32(G_{34}+G_{35}+G_{36})+224G_{55}\\
 &+20M^2_{5,1}-7M^2_{7,d}+4L_6
 -8(S_{34,1}+S_{35,1}+S_{36,1})+24S_{44,1}.
\end{aligned}
\]

The finite inequalities concern a domain reconstructed from categorical
necessities and the immutable tensor. They are not numerical solver
infeasibility reports. Discovery used optimization, but the published
proof replay uses only the Python standard library, exact fractions,
source enumeration, and integer dot products. Normal and optimized
Python executions both check all 24 branches. No `assert` statements,
floating positive-semidefinite tests, cached row lists, or optimizer
dependencies are used in that replay.

## Reproduction and references

From the repository root, with this packet under its published
`evidence/unified_20261016/rank8` location:

```sh
python -O evidence/unified_20261016/rank8/verify_r18_sts_moments.py --repo . --output /tmp/r18_sts_replay.json
```

The verifier checks the immutable source hash and all 512 model
coefficients before constructing the complete characters, low frames,
row orbits, phase triples, 119-coordinate targets, and inequalities.
Its certificate is `r18_sts_moment_certificate.json`. The normal and
optimized receipts, and independently authored categorical/code audits,
are included alongside it.

- [S] A. Schopieray, *Categorification of integral group rings extended
  by one dimension*, Journal of the London Mathematical Society 108
  (2023), 1617--1641, DOI 10.1112/jlms.12789, published Lemma 3.1.
  The two-FP-dimension Galois pseudo-unitarity result is used with its
  published hypotheses.
- [O] V. Ostrik, *Pivotal fusion categories of rank 3*,
  [arXiv:1309.4822](https://arxiv.org/abs/1309.4822), Example 2.9 and the
  character construction preceding Theorem 2.13, for the actual
  character-labelled center summands and central character formula.
- [NS] S.-H. Ng and P. Schauenburg, *Frobenius--Schur indicators and
  exponents of spherical categories*,
  [arXiv:math/0601012](https://arxiv.org/abs/math/0601012), for spherical
  indicators, induction trace formulas, and exponent/twist relations;
  and the standard modular Galois symmetry used in (7).
- [BNRW] P. Bruillard, S.-H. Ng, E. C. Rowell, Z. Wang,
  *Rank-finiteness for modular categories*,
  [arXiv:1310.7050v3](https://arxiv.org/abs/1310.7050v3), Theorem 3.9.
  The general spherical statement and its center reduction, not merely
  the modular special case, are used here.

The theorem establishes nonexistence for R8_1_18 alone. Its application
to R7_4_2053 additionally uses the separately audited dihedral Morita
reduction and rotational-branch obstruction.

# R10_1_189: additional exact restrictions, 24 October 2026

**Decision: unresolved. No general exclusion or categorical model is established.**

This report adds restrictions to the published proof package at commit
`323c4227ffb796a72eef506f1eb289437fbc95db`; it does not change that classification.
The ring is

\[
g^5=1,\qquad gx=xg,\qquad x^*=x,\qquad
x^2=1+(g+g^2+g^3+g^4)x.
\]

Write \(Y_i=g^ix\), \(d=2+\sqrt5\),
\(d'=2-\sqrt5=-1/d\), and \(D=10+20d\).
The corrected, published Galois reduction to a pseudo-unitary categorification is retained (Schopieray, JLMS108 (2023), Lemma3.1, DOI10.1112/jlms.12789). The original arXiv v1 wording is not used for this categorical premise. So are
the proved untwisted pointed associator, center restriction/Galois formulas,
and exponent bound \(\operatorname{FSexp}\mid1600\). Their categorical premises
are in the preceding package, not supplied by the computations below.

## 1. All indicators prime to 1600 are forced

For a central simple \(Z\), write
\(FZ=\sum a_jg^j+\sum b_jY_j\), and put
\(a_Z=\sum a_j\), \(b_Z=\sum b_j\).
Every mixed column has \(a_Z=1\); every pure column has \(a_Z=0\).
All mixed twists are fifth roots. Define

\[
A_i(n)=\sum_Z a_Z b_i\theta_Z^n,
\qquad B_i(n)=\sum_Z b_Z b_i\theta_Z^n.
\]

The induction indicator formula gives
\(D\nu_n(Y_i)=A_i(n)+dB_i(n)\).
Since \(\nu_1(Y_i)=0\), applying \(\sigma_n:\zeta_{1600}\mapsto
\zeta_{1600}^n\), for \((n,1600)=1\), gives

\[
A_i(n)+\sigma_n(d)B_i(n)=0. \tag{1}
\]

The tensor gives \(\dim\operatorname{Hom}(1,Y_0^3)=0\) and
\(\dim\operatorname{Hom}(1,Y_i^3)=1\) for \(i\ne0\).
The latter indicator is a cubic root, and lies in both
\(\mathbb Q(\zeta_3)\) and \(\mathbb Q(\zeta_{1600})\), whose intersection is
\(\mathbb Q\). Hence \(\nu_3(Y_i)=1-\delta_{i0}\).
Subtracting (1) for \(n=3\) from the indicator formula, and using
\(D/(d-d')=5d\), yields

\[
B_i(3)=5d(1-\delta_{i0}),\qquad
A_i(3)=5(1-\delta_{i0}).
\]

Because \(A_i(n)\) is an integer-weighted sum of fifth roots, its nonzero
Fourier moments are Galois conjugate. The last expression is rational, so
\(A_i(n)=5(1-\delta_{i0})\) for every \(5\nmid n\).
Equation (1) now proves

\[
\boxed{\quad
\nu_n(Y_i)=
\begin{cases}
0,& n\equiv\pm1\pmod5,\\
1-\delta_{i0},&n\equiv\pm2\pmod5,
\end{cases}
\qquad (n,1600)=1.\quad} \tag{2}
\]

This is a theorem about any hypothetical category, not a prediction inferred
from a numerical witness.

## 2. Mixed twist incidence is forced

Let \(M_{i,q}\) count the occurrences of \(Y_i\) among mixed restriction
columns with twist \(\zeta_5^q\). The mixed columns are binary, and their total
incidence at every \(Y_i\) is20, by the induction Gram matrix.
Fourier inversion of \(A_i(n)\) gives

\[
(M_{0,0},\ldots,M_{0,4})=(4,4,4,4,4),
\qquad
(M_{i,0},\ldots,M_{i,4})=(8,3,3,3,3)\ (i\ne0).
\tag{3}
\]

## 3. Center invertibles: a necessary dichotomy

The adjoint subcategory of a hypothetical category is the whole category.
Indeed, \(x^2\) contains \(Y_1,Y_2,Y_3,Y_4\); their products give a generator
of \(C_5\), and then \(x\). Thus the universal grading is trivial.
The kernel of \(\operatorname{Inv}Z(\mathcal C)\to\operatorname{Inv}\mathcal C\)
is the group of tensor automorphisms of the identity, hence is trivial.
Consequently the center invertibles form either the trivial group or \(C_5\).

If the latter pointed braided subcategory is symmetric, it is Tannakian
(its order is odd). Its regular algebra is then a central commutative algebra.
De-equivariantization makes the two-simple right-module category into a fusion
category with rule \(y^2=1+4y\), contrary to Ostrik's rank-two theorem.
Therefore a nontrivial center pointed part must be a **nondegenerate metric
\(C_5\)**. This does not imply a braided structure on \(\mathcal C\), a central
commutative regular algebra in that branch, or a tensor splitting of
\(\mathcal C\).

## 4. Exact finite necessary-condition witness

`twist_gram_probe.py` enumerates full Galois orbits of restriction/twist pairs,
using the established conductor bound. In CRT coordinates modulo \(64,25\),
the integers1151,901,577 generate the unit group, corresponding to
\((-1,1),(5,1),(1,2)\). For \(r=a\bmod5\), a pure column transforms by
\(b'_i=b_{r^{-1}i}\), and its twist by \(\theta\mapsto\theta^{a^2}\).
For mixed columns, the same permutation is followed by complementary subsets
when \(r=2,3\), exactly as in the existing full restriction transform.

There are80 mixed orbit types and1260 pure types after the residual diagonal
Gram bound10 at each coordinate. The equations impose the entire induction
Gram matrix, the two constituents of noninvertible-total4 in every twist
eigenspace of every \(I(g^j)\), and the indicator identities for orders1,2,3.

An **exact integer witness** exists, with center rank70, all twists of order
dividing10, and \(\nu_2(x)=-1\). It is stored in
`twist_gram_witness.json`. The independent standard-library verifier
`verify_restrictions.py` checks the tensor normal form, all Gram entries, the
full Galois action on the data, (3), and indicators1--4 using integer
coordinates modulo \(\Phi_{1600}\). In particular it finds
\(\nu_4(Y_i)=1\) for all five objects.

This also passes the exact fourth-rotation test. On
\(\operatorname{Hom}(1,x^4)\), dimension5 and square trace1 allow multiplicities
\((2,1,1,1)\) of \((1,i,-1,-i)\). For \(Y_i\), \(i\ne0\), dimension3 and
square trace\(-1\) allow \((1,1,0,1)\). Both have fourth indicator1.
A separate exploratory floating evaluation found nonnegative integral cyclic
rotation multiplicities through order60; this is not advertised as an exact
certificate and is not needed for any theorem here.

The witness does **not** specify a modular S-matrix, Verlinde fusion rules,
associators, half-braidings, or a categorical construction. In particular its
mixed columns need not satisfy the tensor action of the proposed center
invertibles. It is deliberately labeled a necessary-condition witness only.

Forbidding all additional center invertibles makes this integer program
infeasible according to HiGHS, while its linear relaxation remains feasible.
No exact integer infeasibility certificate was obtained. This observation is
**not a theorem** that a center \(C_5\) must exist.

## 5. A further conditional reduction in the metric-C5 branch

This part is conditional on the nontrivial branch of §3. Write
\(Z(\mathcal C)=\mathcal P\boxtimes\mathcal E\), where \(\mathcal P\) is metric
\(C_5\), \(\theta_{g^j}=\zeta_5^{qj^2}\), \(q\ne0\). Only the center is split.
The pointed action is free on all its simple objects. Its mixed columns are
the five translates of the ten columns of \(I(1)\).
Their pure residual Gram matrix is \(4I+6J\).

Each \(\mathcal P\)-orbit of pure objects has a base column \(v\), total
\(b=\sum v_i\), and contributes \(\sum v_i^2\) to each Gram diagonal.
Summing all entries and all diagonal entries gives, over base columns,

\[
\sum b^2=34,\qquad \sum\sum_i v_i^2=10.
\]

Together with \(b\in\{1,2,5,10\}\), these force exactly one base object of
total1, two of total2, and one of total5. To see this, total10 already costs
at least20 diagonal units. Without total5 one has \(b^2\le2\sum v_i^2\),
which cannot sum to34. There is exactly one total5 object, since two cost50
in the first sum. The modular Galois permutation acts componentwise on the normalized tensor-product S-matrix and preserves the centralizer factor E: the pointed factor has a fixed unit label, so the product Galois permutation sends its unit component to itself. Therefore there is no additional g-translation in the inherited Galois action on E base columns. Galois invariance forces its column \((1,1,1,1,1)\).
The remaining sums are9 and5, forcing two spread total2 columns and one
total1 column. Galois invariance then forces their base columns to be

\[
e_0,\quad e_1+e_4,\quad e_2+e_3,\quad(1,1,1,1,1).
\]

The unique total1 and total5 base objects have twists of order dividing8.
The two total2 objects have twists \(\epsilon\zeta_5^{\pm r}\), where
\(\epsilon^8=1\). This follows from squared Galois symmetry, using their
respective Galois orbits of sizes1,1,2.

The conditional finite check `central_metric_probe.py` imposes the actual
pointed translation on the mixed columns, the four possible I(1) reciprocal
character assignments from the preceding package, and indicators1--3. Its
exact integer cyclotomic arithmetic leaves four assignments, all with
\(\nu_2(x)=-1\). Up to the two possible signs of \(q\), the resulting
necessary modular-factor dimensions and twists are

| Multiplicity | Dimension in E | Twist |
|---|---:|---|
|1|1|1|
|1|d²|1|
|1|d|1|
|2|1+d|ζ5|
|2|1+d|ζ5⁻¹|
|2|1+3d|ζ5|
|2|1+3d|ζ5⁻¹|
|1|2d|ζ5²|
|1|2d|ζ5⁻²|
|1|5d|−1|

Thus this branch reduces to a rank14 modular factor of dimension
\(100d^2\), with the displayed necessary data. Section7 below completes two
algebraic modular-data candidates and their fusion rings. **No categorical
realization is established**, and neither is an accepted model for R189.

## 6. Literature and model checks

- The existing pseudo-unitarity and induction results come from A. Schopieray,
  *Categorification of integral group rings extended by one dimension*,
  JLMS108 (2023), DOI10.1112/jlms.12789, Lemma3.1, §3 and §4.1:
  https://doi.org/10.1112/jlms.12789 . The corrected published Lemma3.1 is
  the source of the Galois existence reduction; the original arXiv v1
  statement is not its source. The uniform Haagerup--Izumi hypotheses
  do not cover this nonuniform ring. The prior sign correction concerning
  pure restriction columns remains essential.
- The indicator formula and squared-twist Galois symmetry are used in their
  ordinary spherical/modular form; no unitarity-only reconstruction theorem is
  imported. See Ng--Schauenburg, *Frobenius--Schur indicators and exponents of
  spherical categories*, Adv. Math.211 (2007), and the cited Schopieray §3.2.
- Ostrik, *Fusion categories of rank2*, applies to the Tannakian quotient in
  §3, which is actually a fusion category. It is not applied to the ordinary
  two-simple module category without a central commutative algebra.
- A. Schopieray's new preprint *The dimension block of a spherical fusion
  category*, arXiv2609.35287 (28 September2026), was checked:
  https://arxiv.org/html/2609.35287 . Its Theorem5.1 is satisfied here:
  \(1/D+1/D'=1/5\) and \((1/D-1/D')^2=4/125\le1/5\).
  It gives no exclusion. Its Eq.(5) also explicitly records the S-matrix
  character/forgetful-functor compatibility needed for subsequent modular
  completion work.
- Numerically \(D=2\operatorname{FPdim}(\mathrm{Fib}^{\boxtimes3})\).
  The immediate product and ordinary C2-permutation models are unsuitable:
  their centers contain a simple of dimension \(\phi<d\), whereas any central
  simple here has dimension \(a+bd\), \(a,b\ge0\) integers. This does not
  classify all categories of that global dimension.
- The tempting near-group completion \(NG(C_{25},20)\) has noninvertible
  dimension\(5d\), but cannot be obtained by a transitive C5 equivariantization
  of this ring. Tensor autoequivalences preserve duality, and this ring has
  exactly one self-dual noninvertible. A transitive orbit containing one
  self-dual object would have all objects self-dual. This rules out that model
  route without assuming a near-group existence theorem.

The missing step is an actual obstruction or construction. Low indicator
equations and exact integer Gram factorizations alone cannot supply it.


## 7. Exact modular-data completion in the metric branch

This section is conditional on that branch; it does not prove the existence
of a category. Let the rank14 labels be
`1,U,B1,...,B4,C1,...,C4,Y,P1,P2,X`, with dimensions
\(1,d^2,(1+d)^4,(1+3d)^4,d,2d,2d,5d\).
Use the normalized **positive double-braiding** S-matrix, and write
\(\Theta=\operatorname{diag}(\theta_i)\). Our convention is

\[
S\Theta S=\xi_{\mathcal E}\Theta^{-1}\overline S\Theta^{-1}.
\tag{4}
\]

Equivalently one may use \(T=\Theta^{-1}\), as in EGNO's modular-representation
convention. Omitting the conjugation in (4) would give false failures at
nonselfdual entries. This convention was checked independently against the
pointed Gaussian sum and EGNO, *Tensor Categories*, Definition8.13.2 and
Theorem8.16.1: https://math.mit.edu/~etingof/egnobookfinal.pdf .

The unique dimension5d simple X has formal codegree4 and
\(S_{1X}=1/2\). Its Galois-fixed normalized column defines a rational integer
character \(\lambda_X(i)=S_{iX}/S_{1X}\) with sum of squares4. The ten induction
rows already give values1 at the unit, -1 at U, and0 at the B and C objects.
Thus precisely two of its remaining four entries are ±1. Dimension-weighted
orthogonality leaves two possibilities: both P entries are +1; or the X entry
is +1 and the Y entry is -1. The former violates the twist-weighted relation
\(\sum_i d_i\lambda_X(i)\theta_i=-10\xi_{\mathcal E}d\): its left side has
absolute value \(d(5+\sqrt5)<10d\). The latter has left side -10d. Consequently
\(\xi_{\mathcal E}=1\) and

\[
\lambda_X=(1,-1,0,0,0,0,0,0,0,0,-1,0,0,1).
\]

The unique dimensiond simple Y similarly has a rational integer character,
of squared norm100. The induction rows and symmetry give
\(\lambda_Y(1)=1\), \(\lambda_Y(U)=-1\), all four B values -2, all four C
values2, and \(\lambda_Y(X)=-5\). Galois symmetry makes the P values equal,
say u; write \(\lambda_Y(Y)=t\). Orthogonality and the norm give
\(t+4u=13\) and \(t^2+2u^2=41\). The sole integral solution is u=4,t=-3.
Thus

\[
\lambda_Y=(1,-1,-2,-2,-2,-2,2,2,2,2,-3,4,4,-5).
\]

The remaining P block has the form
\(\left(\begin{smallmatrix}a&b\\b&a\end{smallmatrix}\right)\).
The equality of its diagonal entries follows by applying the Galois
permutation P1↔P2 to either row or column, and using symmetry. Orthogonality
with the unit and the column norm give \(a+b=3/5\) and
\(a^2+b^2=7/25\), hence
\(\{a,b\}=\{(3+\sqrt5)/10,(3-\sqrt5)/10\}\).

All other entries follow from the induction-character formula. If
\(\chi(g)=\zeta_5^l\), its induction constituent Aχ has pointed-factor label
\(l/(2q)\). For two induction constituents,

\[
S_{\mathcal E}(A_\chi,A_\psi)
=\frac{\dim A_\chi}{10d}\,\chi(F A_\psi)
 \zeta_5^{-l_\chi l_\psi/(2q)}. \tag{5}
\]

For a pure E base column there is no final phase. Equation(5) is the
normalized tensor-product S formula combined with Schopieray's induction
character formula, explicitly restated in Eq.(5) of
https://arxiv.org/html/2609.35287 . This calculation was independently audited.

`metric_modular_completion.py` performs exact rational arithmetic in
\(\mathbb Q(\zeta_5)\), and checks both P-block choices for each of the four
prior phase assignments. Exactly the pair (q,c)=(1,2),(4,3), with
\(a=(3+\sqrt5)/10\), survives. Each passes symmetry, \(S^2=C\), (4), and
**every Verlinde coefficient is a nonnegative integer**. The other two
phase assignments have \(N_{B1,B1}^{B1}=1/5\), hence cannot be fusion rules.
The charge-conjugation permutation is l↦-l on B and C; all four pure objects
are selfdual.

The two surviving S, twist, dimension and complete fusion tensors are exported
in `metric_candidate_q1_c2.json` and `metric_candidate_q4_c3.json`. Their
complex-conjugate relation explains the pair. Every nonunit basis object
generates the full rank14 fusion ring, checked by exact closure under products
and duality. Thus there is no proper nonpointed fusion subring to which a
lower-rank exclusion could be transferred.

An independent exact Bantay second-indicator check agrees with a direct
double sum over the fusion tensor. The indicator vector in this basis is
\((1,1,0,0,0,0,0,0,0,0,-1,1,1,-1)\), which has the required zero values on
nonselfdual simples and ±1 on selfdual simples. Its independent certificate
is `../rank6_pair/metric_c5_fs2_certificate.json`, produced by
`../rank6_pair/verify_metric_c5_fs2.py`.

An independent SymPy reconstruction in Q(zeta5) reproduced all2744 Verlinde coefficients; the exported fusion tensor has SHA256 `750dfbdbf9cddde4efb5b62d389bf4cd8e6040b77c7aaf73e9d10b020e6f75d1` under the auditor's compact-JSON serialization.

These are **algebraic modular-data candidates**, not fusion categories or
models of the original rank10 ring. The associator, categorical realization,
and the algebra object producing the original center/forgetful functor remain
unconstructed. No categorical promotion is justified by these tests alone.

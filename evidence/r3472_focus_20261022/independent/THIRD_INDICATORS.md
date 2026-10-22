# Maximal third indicators for R8_3_3472

**Result.** In the canonical spherical structure of every pseudo-unitary
categorification of `R8_3_3472`,

\[
 (\nu_2(X_i))_{i=0}^7=(1,1,1,1,1,1,1,1),\qquad
 (\nu_3(X_i))_{i=0}^7=(1,2,2,2,2,2,2,2).
\]

In particular, the order-three rotation on each two-dimensional space
\(\operatorname{Hom}(1,X_i^{\otimes3})\), \(i>0\), is the identity.
This is a necessary restriction on any proposed associator. It does **not**
exclude the ring or supply a categorification.

The repository's existing sphericality and Galois pseudo-unitarity gate
(`evidence/rank8_research_20261022/pivotality/PROOF.md`, Section 4) means this
restriction must hold in a pseudo-unitary Galois form of any hypothetical
complex categorification. Since the indicated values are rational, they
also transport unchanged with that spherical structure under Galois
conjugation. No new sphericality assertion is proved here.

## Exact source data

Use the canonical tensor at
`site/dist/downloads/fusion-tensors/R8_3_3472.txt`, whose normalized tensor
SHA256 is
`33984d45e69ff778e70847def8349abda79ed6c0eaea242a73b533649f9b153a`.
Write \(r=\sqrt2\) and \(\delta=7+5r\). Its positive dimension character is

\[
 (d_0,\ldots,d_7)
 =(1,\delta-1,\delta-1,\delta,\delta-1,
       \delta+1,\delta+1,\delta+1).
\]

Thus

\[
 D=\sum_i d_i^2=700+490r,\quad
 D'=700-490r,\quad
 DD'=9800=2^3 5^2 7^2,\quad
 \frac D{D'}=\delta^2=99+70r.
\]

Every simple is self-dual, and the source tensor gives

\[
 h_i:=\dim\operatorname{Hom}(1,X_i^{\otimes3})
 =N_{ii}^{i}=(1,2,2,2,2,2,2,2)_i.
\]

The decisive identity is

\[
 \sum_i d_i h_i=1+2\sum_{i>0}d_i
 =1+14\delta=\delta^2=\frac D{D'}.
\tag{1}
\]

All these claims are checked directly, using integer pairs for
\(\mathbb Z[\sqrt2]\), by `verify_third_indicators.py`.

## Categorical proof

Let \(\mathcal C\) be pseudo-unitary with this tensor, with its canonical
positive spherical structure, and set
\(N=\operatorname{FSexp}(\mathcal C)\).

1. The spherical Cauchy theorem of Bruillard--Ng--Rowell--Wang,
   Theorem 3.9, implies that every prime divisor of \(N\) lies in
   \(\{2,5,7\}\), by the computed norm of \(D\). Therefore \(3\nmid N\).
   Their Theorem 2.12 also records that all spherical dimensions lie in
   \(\mathbb Q(\zeta_N)\). Since they generate \(\mathbb Q(\sqrt2)\), the
   conductor-eight quadratic field, \(8\mid N\).

2. For a spherical fusion category define the weighted regular indicator
   \(\nu_a(\mathcal C)=\sum_i d_i\nu_a(X_i)\). Ng--Schopieray--Wang,
   Theorem 4.4, equation (4.17), proves that for \((n,N)=1\),

   \[
   \nu_{an}(\mathcal C)=\sigma(\nu_a(\mathcal C))
                         \frac D{\sigma(D)},
   \quad
   \sigma(\zeta_N)=\zeta_N^{\widetilde n},\quad
   n\widetilde n\equiv1\pmod N.
   \tag{2}
   \]

   This is a theorem about every spherical fusion category, via its
   Drinfeld center; it does not require the source category to be braided.
   Take \(a=1,n=3\). We have \(\nu_1(\mathcal C)=1\) and
   \(\widetilde3\equiv3\pmod8\), hence \(\sigma(\sqrt2)=-\sqrt2\).
   Equation (2) therefore gives the **complex equality**

   \[
   \sum_i d_i\nu_3(X_i)=\frac D{D'}=\delta^2.
   \tag{3}
   \]

3. By definition \(\nu_3(X_i)\) is the trace of an operator \(E_i\)
   on an \(h_i\)-dimensional space, with \(E_i^3=1\).
   Consequently \(\operatorname{Re}\nu_3(X_i)\le h_i\).
   Since every \(d_i>0\), equations (1) and (3) imply

   \[
   0=\sum_i d_i\bigl(h_i-\operatorname{Re}\nu_3(X_i)\bigr).
   \]

   Each summand is nonnegative, so every summand vanishes. Every
   eigenvalue of \(E_i\) is a cube root of unity and must have real part
   one. All its eigenvalues are therefore one. The polynomial \(x^3-1\)
   has distinct roots over \(\mathbb C\), so \(E_i=1\), proving
   \(\nu_3(X_i)=h_i\). This argument neither presupposes that the
   indicators are real nor assumes unitarity of \(\mathcal C\).

For the second indicators, the verifier supplies, for each \(i\), a
simple \(X_j\) for which \(N_{jj}^{i}\) is odd. The
Fuchs--Runkel--Schweigert parity theorem, as stated in Liu--Palcoux--Ren--
Vercleyen, Theorem 3.9, forces \(\nu_2(X_i)=1\). This second-indicator
restriction was already used in the repository's sphericality proof.

## Consequences and exact limits of the result

The center induction indicator formula gives, for every \(i>0\),

\[
 \sum_{Z\in\operatorname{Irr}\mathcal Z(\mathcal C)}
   \theta_Z^3\dim(Z)[F(Z):X_i]=2D.
\tag{4}
\]

Thus an associator search can impose identity rotation in every
monochromatic trivalent space, and a phase-expanded central induction
search can fix all third-indicator variables to two. More generally,
equation (2) determines the weighted regular indicators at all exponents
coprime to \(N\): the value is one for \(n\equiv1,7\pmod8\) and
\(\delta^2\) for \(n\equiv3,5\pmod8\). The coprimality qualification is
essential; in particular this does not prescribe the fifth or seventh
indicator without knowing that the relevant exponent is coprime to \(N\).

The existing exact feasible point
`evidence/rank8_frontier_20261021/global_induction/atomic_spectrum_results/R8_3_3472_h4.json`
**already satisfies (4)**. Its complete cone has 253 rows and 57,441
variables. The first rotation column has index 57,406. For each nonunit
simple, the order-three block has normalized trace types \(-1/2\) and
\(1\), followed by three order-four columns. The saved point has weights
zero and two in each such order-three block: its only occupied
order-three columns are \(57407+5k\), \(0\le k\le6\), each of weight two.
The source-bound verifier decodes and checks those exact rational weights.
This audit is limited to the rotation coordinates; it does not claim to
replay the earlier full-cone verification. Consequently the new theorem
does not eliminate that already certified phase relaxation.

The stronger 3,347-row system initially contained no twist variables.
The subsequent construction in `PHASE_EXTENSION.md` supplies an exact
rational phase extension of its newly verified integral center point,
checking the complete relative indicator/rotation moment system through
degree four. This is still a necessary relaxation, with rational phase
weights, and does not impose the complete complex modular equations.
The present proof uses no bound on the FS exponent.
In particular, 1,120 in the existing height-four receipt is a finite
relative-trace compression bound, not an asserted categorical exponent.

## Reproducibility

From the repository root:

```sh
python evidence/r3472_focus_20261022/independent/verify_third_indicators.py
python -O evidence/r3472_focus_20261022/independent/verify_third_indicators.py
```

The script uses only the Python standard library and explicit checks
that remain active under `-O`. The two receipts are identical. It does
not solve an associativity system or rely on floating-point arithmetic.

## Primary sources checked

- S.-H. Ng, A. Schopieray and Y. Wang, *Higher Gauss sums of modular
  categories*, Selecta Math. (N.S.) **25** (2019), Paper 53.
  [arXiv:1812.11234v2](https://arxiv.org/abs/1812.11234v2), Definition (3.2),
  Proposition 3.4 and Theorem 4.4, especially equations (4.17) and (4.19).
  **Version detail:** the general center Gauss/indicator relation is
  Proposition 3.4 in the checked v2, not Corollary 3.5 (which is the
  quasi-Hopf specialization).
- P. Bruillard, S.-H. Ng, E. C. Rowell and Z. Wang, *Rank-finiteness for
  modular categories*, J. Amer. Math. Soc. **29** (2016), 857--881.
  [arXiv:1310.7050](https://arxiv.org/abs/1310.7050), Section 2.2.5,
  Theorem 2.12 and Theorem 3.9. Section 2.2.5 explicitly states
  \((E_V^{(n)})^n=1\).
- S.-H. Ng and P. Schauenburg, *Frobenius--Schur indicators and exponents
  of spherical categories*, Adv. Math. **211** (2007), 34--71.
  [arXiv:math/0601012](https://arxiv.org/abs/math/0601012), Theorem 4.1
  (center indicator formula) and Theorem 5.5 (FS exponent equals center
  twist order).
- Z. Liu, S. Palcoux, Y. Ren and G. Vercleyen, *Triangular prism equations
  and categorification*, [arXiv:2203.06522v5](https://arxiv.org/abs/2203.06522v5),
  Theorem 3.9 (the Fuchs--Runkel--Schweigert parity theorem); this source
  and its application are inherited from the repository's existing proof.

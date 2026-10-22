# Independent audit: maximal third indicators

Reviewed on 22 October 2026 by a separate audit agent.

**Verdict: accepted.** The higher-indicator argument proves, in the canonical
positive spherical structure of every pseudo-unitary categorification of
R8_3_3472,

\[
\nu_3(1)=1,\qquad \nu_3(X_i)=2\quad(i>0),
\]

and proves that each nonunit third-rotation operator is the identity.
It does not prove nonexistence or produce a categorification. The inherited
sphericality/Galois-transport gate is a separate input, not a new theorem
established by this calculation.

## Materials and primary sources

Reviewed `../independent/THIRD_INDICATORS.md`,
`../independent/third_indicators.tex`,
`../independent/verify_third_indicators.py`, and both saved receipts. The
primary-source statements were checked directly in the locally downloaded
PDF text of:

- Ng--Schopieray--Wang, *Higher Gauss sums of modular categories*,
  [arXiv:1812.11234v2](https://arxiv.org/abs/1812.11234v2), equation (3.2),
  Proposition 3.4, and Theorem 4.4, especially (4.17) and (4.19).
- Bruillard--Ng--Rowell--Wang, *Rank-finiteness for modular categories*,
  [arXiv:1310.7050](https://arxiv.org/abs/1310.7050), Section 2.2.5,
  Theorem 2.12, and Theorem 3.9.
- Ng--Schauenburg, *Frobenius--Schur indicators and exponents of spherical
  categories*, [arXiv:math/0601012](https://arxiv.org/abs/math/0601012),
  Theorem 4.1 and Theorem 5.5.

In the checked NSW version, the general relation between center Gauss sums
and weighted indicators is Proposition 3.4. Corollary 3.5 is a specialization
to quasi-Hopf representations. The new note uses the correct general
statement.

## 1. Coprimality with the FS exponent

Let `N=FSexp(C)` and `D=700+490sqrt(2)`. The BNRW Cauchy theorem is
an equality of prime-ideal supports of the global dimension and `N` in
the ring of integers of `Q(zeta_N)`. Their notation `D^2` for global
dimension must not be confused with this note's notation `D`; the proof
uses the global dimension, not its square root.

The norm computation gives

\[
D D'=9800=2^3 5^2 7^2.
\]

If a prime ideal above 3 divided `D`, it would divide `DD'=9800`, which is
impossible. If 3 divided `N`, every prime ideal above 3 would divide `N`,
and hence `D` by Cauchy. Therefore `3` is coprime to `N`. The same argument
restricts rational prime divisors of `N` to `{2,5,7}`. It neither determines
`N` nor places a numerical upper bound on it.

BNRW Theorem 2.12 gives every spherical simple dimension in `Q(zeta_N)`.
The displayed dimensions generate `Q(sqrt(2))`, whose conductor is 8.
The inclusion `Q(sqrt(2)) subset Q(zeta_N)` therefore implies `8|N`.
This conductor statement is valid also for the usual redundancy
`Q(zeta_(2m))=Q(zeta_m)` when `m` is odd: neither of those fields can
contain the conductor-eight quadratic field unless the 2-part is at least
8.

## 2. The inverse convention and the exact weighted indicator

NSW Theorem 4.4 uses `N=ord(T_(Z(C)))`. Ng--Schauenburg Theorem 5.5
identifies this with `FSexp(C)`, so the preceding coprimality result applies
to exactly the exponent required by NSW.

The source formula, for a spherical fusion category, is

\[
\nu_{an}(\mathcal C)
=\sigma(\nu_a(\mathcal C))\frac{\dim(\mathcal C)}
 {\sigma(\dim(\mathcal C))},
\qquad \sigma(\zeta_N)=\zeta_N^{\widetilde n},
\qquad n\widetilde n\equiv1\pmod N.
\]

Here the weighted indicator is
`nu_a(C)=sum_i d_i nu_a(X_i)`, not an unweighted sum or an indicator of
the Drinfeld center itself. The formula is applicable to arbitrary
spherical fusion categories through their centers; no braiding of `C`
is assumed.

Take `a=1,n=3`. The first indicator of a simple object is 1 for the
tensor unit and 0 otherwise, hence `nu_1(C)=1`. Since `8|N`, the
inverse of 3 modulo `N` is congruent to 3 modulo 8. With
`sqrt(2)=zeta_8+zeta_8^(-1)`, this automorphism sends `sqrt(2)` to
`-sqrt(2)`. Thus the inverse convention in the theorem gives precisely
the claimed conjugate `D'`; replacing the inverse convention without
checking it would be unjustified in general, although 3 is its own inverse
modulo 8 here.

It follows that

\[
\sum_i d_i\nu_3(X_i)=D/D'=99+70\sqrt2.
\]

The equality is an equality of complex numbers. It is not merely a
statement about an absolute value, a norm, or a real part. The denominator
is `sigma(D)`, and there is no square, extra global-dimension factor, or
additional simple-dimension weight missing from the expression.

## 3. Positivity makes the rotation bound sharp term by term

The source tensor is self-dual and has

\[
h_i=\dim\operatorname{Hom}(1,X_i^{\otimes3})
=(1,2,2,2,2,2,2,2)_i.
\]

Writing `delta=7+5sqrt(2)`, the seven nonunit dimensions consist of three
copies of `delta-1`, one of `delta`, and three of `delta+1`. Consequently

\[
\sum_{i>0}d_i=7\delta,\qquad
\sum_i d_i h_i=1+14\delta=\delta^2=D/D'.
\]

BNRW Section 2.2.5 explicitly defines the indicator as the trace of the
rotation operator on `Hom(1,X_i^n)` and states that its `n`th power is
the identity. Thus `E_i^3=I`. Its eigenvalues are cube roots of unity,
and it is diagonalizable in characteristic zero because `x^3-1` is
separable. In particular `Re Tr(E_i)<=h_i`, with equality only when
all eigenvalues are 1.

The canonical spherical dimensions in a pseudo-unitary category satisfy
`d_i>0`. Taking real parts in the weighted equality yields

\[
0=\sum_i d_i\bigl(h_i-\operatorname{Re}\nu_3(X_i)\bigr).
\]

Every summand is nonnegative. Each must therefore vanish, proving
`E_i=I` and `nu_3(X_i)=h_i`. This does not assume that the indicators
are real beforehand and does not assume a unitary category or unitary
rotation operators. Pseudo-unitarity enters through the positive weights.

The publication fragment now explicitly states `nu_3(1)=1`, limits the
two-dimensional trace bound to `i>0`, and names the canonical positive
spherical structure in the proposition. These presentation clarifications
were applied by the author and re-read during this review; no proof changes
were required.

## 4. Center consequence and the existing phase witness

Ng--Schauenburg Theorem 4.1 expresses `D nu_3(X_i)` as the pivotal
trace of the cube of the center twist on induction of `X_i`. Decomposing
that induction and using adjunction gives exactly

\[
\sum_Z \theta_Z^3\dim(Z)[F(Z):X_i]=2D\quad(i>0).
\]

The note's normalization is therefore correct. This is a restriction
on any actual categorification and on a necessary phase relaxation; it
is not sufficient to construct center data or associators.

The cached phase-witness coordinate claim is also consistent with its
source implementation. I inspected `streaming.Cone` in the earlier
global-induction code and `rotation_types` in
`supplements/rank8/experimental_signed/tensor_rotation.py`. The columns
are ordered by nonunit object, then by rotation order. At height four,
the third-order trace types over `Q(sqrt(2))` are `(-1/2,1)`, followed
by three fourth-order types. The computed start index 57406 and the
five-column stride therefore identify the claimed third-order blocks.
Each cached block is `(0,2)`, so it already has indicator 2.

This coordinate audit does not reproduce the full cone's feasibility
certificate. The note correctly leaves that earlier certification and
the separate 3,347-row twist-free system distinct. No combined-system
feasibility or exclusion follows from this audit.

## 5. Reproduction and scope

Both source-bound commands were independently run and returned `PASS`:

```
python evidence/r3472_focus_20261022/independent/verify_third_indicators.py
python -O evidence/r3472_focus_20261022/independent/verify_third_indicators.py
```

The two saved receipts agree. The verifier uses exact integer pairs and
rational numbers, checks the source dimension character and cubic invariant
dimensions, confirms the saturation identity, and enumerates all six
possible eigenvalue-multiplicity triples for a two-dimensional order-three
rotation. The unique spectrum with real trace 2 is `(2,0,0)`.

The canonical tensor digest is
`33984d45e69ff778e70847def8349abda79ed6c0eaea242a73b533649f9b153a`.
The cached witness digest is
`5202401998f4029018fcf8d40f500f2dc8e399ab85ee2a08b03661592b4bce16`.

The inherited second-indicator parity theorem and the prior
sphericality/Galois-pseudo-unitarity gate were not re-proved in this
review. The third-indicator proof itself is unconditional within its
stated pseudo-unitary/canonical-spherical hypotheses. Rational indicator
values transport unchanged when that spherical structure is transported
under Galois conjugation. The result supplies a necessary associator
restriction and leaves categorification of R8_3_3472 unresolved.

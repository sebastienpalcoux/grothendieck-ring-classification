# A phase extension of the integral center relaxation

**Verified result.** The exact integer point in
`../center/integer_witness.json` admits a nonnegative rational extension
satisfying all relative indicator and rotation moment equations through
degree four, including the forced third indicators from
`THIRD_INDICATORS.md`. The extension has **80 equations, 391 variables,
and 40 positive entries**. The standard-library verifier reconstructs
the equations and the complete finite relative-trace domain and checks
every equation over the rationals.

The underlying center row multiplicities and the base auxiliary fusion
coefficients are integers. The new phase and rotation weights are
rational. This is a feasible point of a necessary relaxation, not an
assignment of genuine twists, a full modular datum, or a categorification.
The added equations are indicator/rotation moment equations; they do
**not** impose the complete complex modular relation `STS`.

## Fixed source point and binding

The separately verified center point satisfies all 3,347 equations and
13,242 finite bounds of the strengthened Gram/S/cubic-Verlinde/Galois/FP/
unit-product system. Its 17 positive restriction variables consist of
seven distinguished twist-one restrictions and ten higher restrictions.
Nine higher vectors have multiplicity two. The vector

\[
 u=(0,1,1,1,1,1,1,1)
\]

has multiplicity 98. The center verifier independently reconstructs the
full system and verifies `restriction_bindings`, which associate every
positive restriction variable with its precise source index and vector.
The phase verifier checks those same bindings and weights, and pins the
entire integer witness by SHA256. It therefore need not reconstruct the
large center matrix a second time.

The numerical discovery first used the related rational point with
weight \(49/50\) on \(10u\). The full center column for \(10u\) is exactly
100 times that for \(u\), as independently proved by the center verifier.
Every phase coefficient \(v_i\dim(v)\) likewise scales quadratically.
Multiplying each phase weight on \(10u\) by 100 gives the saved extension
on 98 copies of \(u\). The final verifier uses the integral point
directly and does not depend on this discovery history.

## Complete relative-trace domain

Let \(K=\mathbb Q(\sqrt2)\). The spherical Cauchy restriction allows only
the primes \(2,5,7\) in a twist order. For a root \(\theta\), replace
\((\theta,\theta^2,\theta^3,\theta^4)\) by its joint normalized relative
trace to \(K\). This yields a tuple of pairs in the basis
\((1,\sqrt2)\). The degree-four domain has exactly 37 distinct types.

The verifier regenerates these types from the Ramanujan/quadratic
Gauss-sum formula. For an order \(m\), a power \(1\le k\le4\), and
\(g=(m,k), n=m/g\), the rational coordinate is
\(\mu(n)/\varphi(n)\). The radical coordinate is zero unless
\(n=8z\) with \((z,8)=1\), in which case it is

\[
 \frac{\epsilon\,2\mu(z)\chi_8(z)\chi_8(k/g)}{\varphi(n)},
 \qquad \epsilon\in\{1,-1\}.
\]

Here \(\chi_8(a)=(2/a)\) for odd \(a\), with value zero for even \(a\).
One common sign is used throughout a tuple. All orders dividing
\(2^5\cdot5\cdot7=1120\) are visited, and the all-zero tuple is included.
This is complete for arbitrary permitted orders: if a prime exponent
exceeds that divisor box, then for every \(k\le4\) both the rational
Möbius term and the radical Gauss term vanish. For 2 the reduced order
has 2-part at least 16; for 5 or 7 the reduced order retains a square
factor. Thus 1120 is a compression bound, not a bound on the categorical
FS exponent.

This independently implemented formula reproduces the 37 types of
`supplements/rank8/experimental_signed/higher_traces.py`; the final
verifier has no dependency on that implementation.

## Exact equations checked

For each of the ten higher restriction vectors \(v\), introduce
\(x_{v,t}\ge0\) for each of the 37 joint types \(t\). Their sum equals
the fixed integer multiplicity \(m_v\), giving ten equations. Write
\(z_v=\sum_i v_i d_i\), and let \(L_i\) be the contribution from the
seven distinguished restrictions, whose twists are one. For
\(k=1,2,3\) and \(i>0\), impose

\[
 L_i+\sum_{v,t}x_{v,t}v_i z_v t_k
 =D\nu_k(X_i),\qquad
 \nu_1(X_i)=0,\quad\nu_2(X_i)=1,\quad\nu_3(X_i)=2.
\]

Each equality has two rational coordinates, giving 42 equations.

For each nonunit \(X_i\), introduce three nonnegative rotation weights
\(a_i,b_i,c_i\), corresponding to the normalized fourth-root trace
types \((-1,1),(0,-1),(1,1)\), where the second coordinate is the
trace of the square of the rotation. Impose

\[
 \begin{aligned}
 a_i+b_i+c_i&=\dim\operatorname{Hom}(1,X_i^{\otimes4})
                 =\sum_j(N_{ii}^j)^2,\\
 a_i-b_i+c_i&=\nu_2(X_i^{\otimes2})=\sum_jN_{ii}^j,\\
 L_i+\sum_{v,t}x_{v,t}v_i z_v t_4&=D(-a_i+c_i).
 \end{aligned}
\]

The first two equations give 14 rows; the last equation has two
rational coordinates for each \(i\), giving another 14. The square
trace identity is the usual tensor-rotation identity used by the
existing `streaming.Cone`: rotating a fourfold tensor twice has trace
\(\nu_2(X_i^{\otimes2})\). Its value follows from additivity and the
already forced positive second indicators.

Thus the extension has \(10+42+14+14=80\) rational equations and
\(10\cdot37+7\cdot3=391\) nonnegative variables. The central unit is
absent from the displayed nonunit moments because its restriction has
zero nonunit coordinates. The fourth-square trace includes its source
unit contribution through \(\sum_jN_{ii}^j\).

## Replay and scope

First run the center stage's full source-bound integer-witness replay.
Then, from the repository root, run:

```sh
python evidence/r3472_focus_20261022/independent/verify_phase_extension.py
python -O evidence/r3472_focus_20261022/independent/verify_phase_extension.py
```

The normal and optimized receipts are identical. The complete file
dependency closure of this fast replay is pinned in
`phase_certificate.json`: the verifier, its local arithmetic helper,
the canonical tensor, and the source-bound integer witness. The latter
is separately verified by the center stage with its own source inventory.
No numerical solver is imported during acceptance, and no scratch
pickle or discovery output is needed.

This settles feasibility only for the stated conjunction of necessary
conditions. It leaves unresolved integrality and compatibility of the
individual phase/rotation weights, a genuine complex twist assignment,
the remaining modular equations, associativity data, and categorification.

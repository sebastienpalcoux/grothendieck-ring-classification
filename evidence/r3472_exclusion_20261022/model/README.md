# Source-derived terminal model

From the repository root, run:

```sh
python3 evidence/r3472_exclusion_20261022/model/check.py
```

The command is read-only. It requires Python 3 and SymPy, which is used only to construct the cyclotomic polynomial. It does not import an optimizer, NumPy, binary model, or cache. All subsequent calculations use Python integers. The optional `--write` flag refreshes `replay.json`.

The checker reads the canonical fusion tensor at `site/dist/downloads/fusion-tensors/R8_3_3472.txt`, verifies its SHA-256 digest, and independently reconstructs the two models in `../terminal/models.json`. This connects the portable terminal certificate to the fusion tensor. The preceding center-domain and surviving-frame arguments are recorded elsewhere in this evidence package.

The surviving frame supplies the weighted twist moments

\[
P_1=-2-10\sqrt2,\qquad P_2=-2,\qquad P_3=-2+10\sqrt2,
\qquad\sum c^2=98.
\]

Cauchy's theorem restricts exponent primes to \(2,5,7\). Modular Galois symmetry makes the weighted twist multiplicity constant on squared-unit orbits. The local orbit sizes for primitive orders \(2^a,5^b,7^c\) are respectively \(2^{\max(a-3,0)}\), \(2\cdot5^{b-1}\), and \(3\cdot7^{c-1}\), with the stated small 2-power exceptions and size one for an absent prime. Requiring their product to be at most 98 gives exactly 424 product orbit types. Their multiplicities are nonnegative integers bounded by 98 divided by the orbit size.

The orbit power sums are evaluated by local Gauss-period identities. Every identity actually used is checked independently: the checker enumerates the squared-unit residue coset and compares the claimed period with direct polynomial reduction modulo the relevant prime-power cyclotomic polynomial. The saved replay records 3,344 such checks across 76 moment exponents.

The cyclotomic order 1120 is a coordinate field for these reduced periods and the rotation roots. It is **not** an assumed upper bound on the orders of central twists. The 424 orbit types include higher prime powers, whose complete squared-unit power sums reduce to this coordinate field.

For a nonunit source simple, the surviving-frame indicator formula is

\[
\nu_m(X_i)=b_i(m)+\frac{\sqrt2}{20}(P_m+2),
\]

where \(b_i(m)=1\) when \(7\nmid m\), and otherwise is 6, 7, or 8 according to the source dimension class. Tensor powers of the three representative source simples are computed directly from the fusion tensor. The cyclic-rotation power-trace identity then gives exact Fourier multiplicities on \(\operatorname{Hom}(1,X_i^n)\). At orders \(4,5,7,8,10,16,20\), their constant coefficients must be integers. Reduction modulo \(140n\), with exact quotient bounds, produces 362 equations in 572 integer variables. The checker reconstructs every coefficient, right-hand side, and starting bound.

For every cyclotomic automorphism \(a\equiv1\pmod n\), indicator field membership gives

\[
P_n-\chi_2(a)P_{an}=2(\chi_2(a)-1),
\qquad
\chi_2(a)=\begin{cases}1&a\equiv1,7\pmod8,\\-1&a\equiv3,5\pmod8.\end{cases}
\]

The checker constructs these rows by substituting \(x\mapsto x^a\) into already reduced moments, and separately checks the result against direct evaluation of \(P_{an}\). Removing repeated primitive integer rows adds exactly 266 equations, giving the final 628-row model. The field model starts from the previously certified bounds in `../terminal/certified_all_bounds.json`; equality of that interface is checked explicitly.

The terminal checker independently verifies every bound deduction and the final separating inequality. This model checker verifies the exact coefficient derivation and the interfaces to those certificates; it performs no numerical search.

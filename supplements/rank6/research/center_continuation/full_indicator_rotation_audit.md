# Complete rotation audit through the candidate conductor

The exact cyclic-eight modular datum and proposed restriction matrix define
candidate indicators

\[
 \nu_n(X)=\frac{1}{D}\sum_Z [F(Z):X]d_Z\theta_Z^n,
 \qquad D=136+32\sqrt{17}.
\]

This is a necessary indicator formula for a positive spherical
categorification with this center and restriction functor. It does not
construct that functor.

For every simple object X and every n from 1 to 136, the script
`full_indicator_rotation_audit.py` computes the entire multiplicity vector
of the order-n rotation on `Hom(1,X^n)`. All 55,896 multiplicities in the
816 resulting spaces are nonnegative integers. The multiplicities sum
exactly to the dimension of the corresponding invariant space, computed
from the original rank-six fusion tensor.

## Exact formula used

Let g=gcd(n,k), d=n/g and t=k/g. Grouping the n copies of X into d blocks
of size g identifies the g-step rotation with the ordinary rotation of
`(X^g)^d`. Therefore

\[
 \operatorname{Tr}(E_X^{(n)k})
   =\sigma_t\bigl(\nu_d(X^g)\bigr),
 \qquad \sigma_t(\zeta_d)=\zeta_d^t.
\]

Write `nu_d(X^(n/d))=a_d+b_d sqrt(17)`, using additivity and the exact
fusion powers. If 17 does not divide d, then b_d=0. If d=17m (with
17 not dividing m, as is always the case in the checked range), quadratic
Gauss sums and Chinese remaindering give

\[
 \sum_{t\in(\mathbb Z/d\mathbb Z)^\times}
 \left(\frac{t}{17}\right)\zeta_d^{-jt}
 =\sqrt{17}\left(\frac{jm}{17}\right)c_m(j),
\]

where the Legendre symbol is zero when 17 divides j, and `c_m(j)` is
the Ramanujan sum. Thus the multiplicity of `zeta_n^j` is exactly

\[
 \frac1n\left(
 \sum_{d\mid n} a_d c_d(j)
 +\sum_{17m\mid n}17b_{17m}
       \left(\frac{jm}{17}\right)c_m(j)
 \right).
\]

All calculations use rational numbers and integers. The bound 136 is
explicit; no assertion about all n, an associator, an etale algebra,
or categorifiability follows from this successful audit.

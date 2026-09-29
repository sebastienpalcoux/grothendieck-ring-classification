# Generalized central indicators: exact necessary tests

`generalized_indicator_audit.py --write` checks every central simple Z,
every simple X of R6_3_215, and powers 1 through 8 in the supplied
cyclic-eight modular datum. It computes the rotation traces on
Hom(F(Z),X^m) from the modular action and performs the exact Fourier
transform for eigenvalues whose mth powers equal theta_Z^(-1).

All 1,056 spaces and all 4,752 eigenvalue multiplicities pass the
nonnegative-integrality requirement. The canonical restriction to the
actual rank-eight cyclic-eight quotient is also checked as a positive
control: 1,408 spaces and 6,336 multiplicities pass. Arithmetic uses
arbitrary-precision integers in cyclotomic polynomial quotients;
the stored outcome is `generalized_indicator_audit.json`.

The identities used are Ng–Schauenburg, *Congruence Subgroups and
Generalized Frobenius–Schur Indicators*, Theorem 5.4 and Lemma 5.3:
<https://arxiv.org/abs/0806.2493>. The Euclidean recursion applies their
SL(2,Z) action to the base multiplicity vector of X^gcd(m,k).

Passing these tests gives no associator, tensor functor, connected
etale algebra, or categorification. In particular, the separate
`../new_frontier/cyclic8_morita_exclusion.md` explains a categorical
obstruction to lifting this restriction data with the actual known
cyclic-eight center as source.

# Independent audit: center restriction Galois filter

23 October 2026. Files audited: `central_filter.py` and `full_gram.py`. No change was made to either implementation.

## Categorical normalization and signs: valid

Assume a pseudo-unitary categorification \(\mathcal C\) of a commutative based ring \(R\), and put \(D=\operatorname{FPdim}(\mathcal C)\). Use the normalized center matrix \(s=S/D\); the center dimension is \(D^2\).

For every scalar character \(\chi:R\to\mathbf C\), let \(A_\chi\) be the corresponding simple summand of \(I(1)\). The association is specifically the one obtained by pulling \(\chi\) back along the forgetful ring map. Ostrik, *Pivotal fusion categories of rank 3*, [arXiv1309.4822](https://arxiv.org/pdf/1309.4822), Example2.9, the paragraph immediately before Theorem2.13, and Theorem2.13 give
\[
\chi(FZ)=\frac{S_{A_\chi,Z}}{\dim A_\chi},
\qquad\dim A_\chi=\frac D{f_\chi},
\qquad [I(1):A_\chi]=1.
\]
Thus, with \(v_Z=[FZ]\) as a coefficient column and \(H_{\chi i}=\chi(i)/f_\chi\),
\[
(s_{A_\chi,Z})_\chi=Hv_Z.
\]
There is no missing complex conjugate, extra dimension factor, or sign in this convention.

Normalized modular Galois symmetry is
\[
\sigma(s_{aZ})=\epsilon_\sigma(Z)s_{a,\widehat\sigma Z},
\qquad\epsilon_\sigma(Z)\in\{\pm1\}.
\]
See Bruillard–Ng–Rowell–Wang, *Rank-finiteness for modular categories*, [arXiv1310.7050v3](https://arxiv.org/html/1310.7050v3), equation(2.13). Since \(v_Z\) is integral,
\[
v_{\widehat\sigma Z}=\epsilon_\sigma(Z)T_\sigma v_Z,
\qquad T_\sigma=H^{-1}\sigma(H).
\]
Consequently the full-column filter must allow either sign, exactly as `full_gram.py` does.

For the special columns \(A_\chi\), pulling characters back commutes with Galois conjugation, so \(\widehat\sigma A_\chi=A_{\sigma\chi}\). Moreover
\[
s_{A_\chi,1}=1/f_\chi,
\qquad \sigma(1/f_\chi)=1/f_{\sigma\chi}=s_{A_{\sigma\chi},1}>0.
\]
The sign on these columns is therefore +1. The unsigned test `T V[h] == V[sqchars[h]]` in `central_filter.py` is justified. Duality acts by \(\chi\mapsto\chi\circ *\), again as implemented.

Character orthogonality gives \((H^{-1})_{i\chi}=\chi(i^*)\), hence the code's expression
\[
(T_\sigma)_{ij}=\sum_\chi\chi(i^*)\frac{\sigma(\chi(j))}{\sigma(f_\chi)}
\]
is correct. For a cyclotomic character field, \(T_\sigma\) is rational: the character-row permutation matrices of its abelian Galois group commute, so every field automorphism fixes \(H^{-1}\sigma(H)\). Integrality is an extra property verified for the present five tensors.

## Exact arithmetic checks performed

Independent exact checks, run using rational arithmetic and the original fusion tensors, passed for all five cases:

* ten distinct normalized ring characters, all multiplication identities, and recomputed formal codegrees;
* \(H^{-1}H=1\), the recorded \(T_\sigma\), and \(T_\sigma^2=1\);
* commutation of \(T_\sigma\) with duality and \(T_\sigma B T_\sigma^t=B\);
* nonnegative entries and zero unit row for every surviving residual Gram matrix.

The numbers of surviving \(I(1)\) assignments in cases114,115,152,153,179 are respectively **8,24,24,8,64**.

Every currently stored full-Gram witness was replayed with Python integers, independently of the floating-point solver output: **2,8,8,2,26** witnesses respectively. Each has positive integral multiplicities, nonnegative integral columns, closure under the signed Galois operation and duality, and exact sum of outer products equal to the residual Gram matrix.

## Full Gram search: scope and limits

The column enumeration uses necessary diagonal and pairwise Gram bounds. The kernel/pseudoinverse conditions are the exact criterion that subtracting one column outer product preserves positive semidefiniteness. Orbit multiplicities must agree because Galois and duality permute the center simples, even when several center simples have identical restrictions. Grouping equal restrictions does not invalidate this necessity.

The `dimok` formula is the exact integrality test in \(\mathbf Z[\sqrt2]\) for
\[
\frac{D^2}{(a+b\sqrt2)^2},\qquad
D^2=17408+12288\sqrt2.
\]
This quotient is the formal codegree of a center simple. Algebraic integrality is necessary but weaker than the additional d-number condition. Thus the filter is sound, with room for strengthening.

The solver uses floating-point LP/MILP. A returned positive witness can be and has been checked exactly. A timeout is not infeasibility, and numerical infeasibility alone should not be used as an exact exclusion certificate without a separate proof. In the stored results all statuses are feasible and all witnesses replay exactly. They are necessary-condition witnesses, not categorifications.

## R189: precise nonbraidability audit

The published result is Schopieray, *Irrational braided generalized near-groups*, DOI [10.4153/S0008439523000334](https://doi.org/10.4153/S0008439523000334), **Theorem3.6** (Theorem1 in arXiv2212.14009v1). It applies to braided fusion categories over \(\mathbf C\) with irrational Frobenius–Perron dimension and a transitive invertible action on noninvertible simples. It has no pseudo-unitarity hypothesis. Section2.2.1 defines the complex setting; the end of Section2.2 explains the Galois reduction to pseudo-unitarity used in its proof.

R189 satisfies the generalized-near-group and irrationality hypotheses. The theorem allows only the Fibonacci or \(PSU(2)_6\) adjoint factors, times a pointed category, so the unique noninvertible FP dimension would be \((1+\sqrt5)/2\) or \(1+\sqrt2\). Neither equals \(2+\sqrt5\). Therefore **there is no braided complex fusion category with ring R189**, including non-pseudo-unitary braided categories. This leaves the ordinary, potentially nonbraided, categorification question open.

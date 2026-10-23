# Independent audit of ten rank-10 reciprocity exclusions

**Verdict: all ten exclusions are accepted over general complex fusion
categories.** The IDs are R10_1_65, 89, 90, 91, 120, 143, 144, 147, 162,
and 182.

The independent replay is:

    python work/audit_new_models/verify_rank10_reciprocity.py

It uses only Python's standard library and imports no discovery, character,
or algebraic-number code. Its exact arithmetic uses the basis
\(1,\sqrt2,i,i\sqrt2\). It reads the original tensors and the ten exact
reciprocity receipts, checks the supplied distinct scalar characters directly
against all multiplication coefficients, recomputes their formal codegrees,
and verifies their central dimensions. It regenerates every candidate column
from exact dimension equations and integer Gram bounds. All ten searches
terminate with zero possible assignments, after three or five nodes.

The detailed result is in rank10_reciprocity_audit.json. The replay does not
need either a complete scalar-character table or equality of the first Gram
row: it proves infeasibility using only distinct supplied characters and the
Gram inequalities. Thus the noncommutative cases require no reconstruction
of the two-dimensional algebra character.

## Necessary categorical constraints

Suppose first that \(\mathcal C\) is pseudo-unitary. Set
\(D=\operatorname{FPdim}(\mathcal C)\), and let \(F:Z(\mathcal C)\to\mathcal C\)
be the forgetful functor with adjoint \(I\). For each scalar ring character
\(\chi\), let \(A_\chi\) be the associated central simple and let
\(v_\chi\) record the multiplicities of the original simples in \(F(A_\chi)\).
Ostrik's Theorem 2.13 gives

\[
(v_\chi)_0=1,\qquad
\sum_i(v_\chi)_i d_i=\beta_\chi,\qquad
\beta_\chi=\frac D{f_\chi},\qquad
f_\chi=\sum_i\chi(i)\chi(i^*).
\]

These columns are distinct central-simple columns, even if some central
dimensions or some underlying forgetful objects coincide.

The exact adjunction Gram matrix is

\[
B_{ij}=[F I(X_j):X_i]
      =\sum_{a,k}N_{aj}^{k}N_{ka^*}^{i}
      =\sum_{A\in\operatorname{Irr}Z(\mathcal C)}
         [F A:X_i][F A:X_j].
\]

Consequently, after removing any chosen columns, the residual matrix is
entrywise nonnegative and positive semidefinite. In particular,
\((v_\chi)_i\leq B_{0i}\), \((v_\chi)_i^2\leq B_{ii}\), and every residual
two-by-two principal minor is nonnegative. These are necessary conditions
without any assumption about the unchosen central simples.

For these rings, all \(d_i\) and \(\beta_\chi\) have nonnegative integer
coordinates in \(1,\sqrt2\). Splitting the dimension equation into those two
coordinates, together with the stated finite bounds, exhausts every
nonnegative integral column. The independent enumeration agrees exactly
with the receipt's lists.

## Derivation and normalization of S reciprocity

The correspondence used in Ostrik's Theorem 2.13 is defined immediately
before the theorem. A simple representation \(E\) of the original ring gives
a scalar action \(\widehat E\) of the central ring via \(F\). For a scalar
character \(\chi\), this is simply \(\widehat E=\chi\circ F\).

Ostrik's Example 2.9 identifies the character corresponding to a central
simple \(A_\chi\) as

\[
\chi(F B)=\frac{S_{A_\chi,B}}{\dim A_\chi}.
\]

Substitute \(B=A_\psi\) and use symmetry of the unnormalized modular
S-matrix. The result is precisely

\[
\beta_\chi\,\chi(v_\psi)
 =
\beta_\psi\,\psi(v_\chi).
\]

There is no complex conjugation and no dual index in this equation. No
commutativity of the original ring is assumed; only the selected characters
are scalar. The exact replay uses this convention. The same derivation
also validates the S-reciprocity identity used in the rank-9 irrational
exclusions in work/resolve_rank9_irrational/proofs.tex.

The unnormalized convention is also compatible with Deshpande,
arXiv:1611.04486v1, equations (35)–(36). The direct Ostrik argument already
suffices.

## General-complex bridge

For each of these ten IDs, the exact oriented signed-table replay and the
complete original dimension-character replay were run again during this
audit:

    verify.verify_record(original_tensor, signed_ledger_record)
    verify_characters.verify_original(original_tensor, character_record)

All passed. The records are in work/general_signed/ledger.json and
original_characters.json. The independent mathematical audit of the bridge
is work/audit_signed/AUDIT.md, and all ten IDs occur in its explicit
sphericality-certified list.

The bridge says that every hypothetical complex categorification admits a
spherical structure, and that every surviving spherical dimension character
has a Galois conjugate which becomes the positive FP dimension character
after twisting by a tensor sign character. Such a categorification therefore
would give a pseudo-unitary categorification of the same original based
ring. The exact impossibility above excludes it.

This implication uses no unitarity assumption. The Galois/sign reduction is
only an implication from hypothetical existence, not a construction of a
category.

## References checked

- V. Ostrik, *Pivotal fusion categories of rank 3*,
  [arXiv:1309.4822](https://arxiv.org/abs/1309.4822), Proposition 2.4,
  Example 2.9, the correspondence preceding Theorem 2.13, and Theorem 2.13.
- T. Deshpande, *On centers of bimodule categories and induction-restriction
  functors*, [arXiv:1611.04486v1](https://arxiv.org/abs/1611.04486v1),
  equations (35)–(36).
- The signed-bridge audit records the relevant sphericalization,
  dimension-field, and Galois-realization sources separately.

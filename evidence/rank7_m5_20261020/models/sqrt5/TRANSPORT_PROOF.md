# Complete Galois transport for R3895 and R5039

This is an exact algebraic certificate for the normalized character transport.
It is an input to the center-trace obstruction, and is not an exclusion or a
categorification by itself. All indices below are the original census indices
0 through 6. The matrix acts on **column** multiplicity vectors.

Write the dimension vector as `d=a+b sqrt(5)`. For the two cases,

| ID | a | b | permutation S |
| --- | --- | --- | --- |
| R7_5_3895 | (1,5,5,10,8,8,9) | (0,2,2,4,4,4,4) | swap 4 and 5 |
| R7_5_5039 | (1,5,5,8,8,10,9) | (0,2,2,4,4,4,4) | swap 3 and 4 |

Both have global dimension `D=720+320 sqrt(5)`. Their complete transports are

\[
T=S+b\bigl(a-\tfrac94 b\bigr)^t.
\]

In particular, `T e_0=e_0+b=(1,2,2,4,4,4,4)^t`; its positive dimension is
`161+72 sqrt(5)=D/Dbar`. The matrix includes the action on the non-FP character
components. Omitting the permutation S would give an incorrect transport.

## Exact reconstruction

Let `N_i` denote the row-convention regular fusion matrices. The separating
element `H` and its squarefree minimal polynomial are reconstructed by the
repository's `Characters` routine. Since the characters of each ring have
degree at most two, the chosen automorphism of the complete character field
is represented by the following polynomial congruences:

* On a quadratic factor `f=t^2+c t+e` with discriminant a rational square
  times 5, take `q(t)=-c-t mod f`.
* On all other factors take `q(t)=t mod f`. In R5039 this explicitly fixes
  the quadratic field `Q(sqrt(-2))`.

The Chinese remainder theorem gives `q mod charpoly(H)`. Set `H'=q(H)`.
The exact polynomials `p_i` satisfying `N_i=p_i(H)` then give the algebra
automorphism `A(N_i)=p_i(H')`. The verifier checks all congruences, `A^2=1`,
and all 49 multiplication identities for the transported fusion matrices.

Let `B=sum_i N_i N_(i*)` be the Casimir and put

\[
F=B\,A(B)^{-1},\qquad
T_{\bullet i}=\bigl(\operatorname{row}_0(F A(N_i))\bigr)^t.
\]

Indeed, the zeroth row extracts the basis coefficients of an element in the
regular representation. If `C` is the character table (characters in rows),
`f` its vector of formal codegrees, and `P_sigma` the permutation such that
evaluating `A(x)` in a character equals evaluating `x` in the corresponding
Galois-conjugate character, then evaluation gives

\[
CT=\operatorname{diag}(f)P_\sigma\operatorname{diag}(1/f)C.
\]

Thus the certificate reconstructs the full normalized character transport
without numerical root choices or an assumed permutation of repeated
formal codegrees. The resulting integral matrices and all CRT data are in
`transport_certificate.json`.

## Verification and interface

Run `python verify_transport.py`, also with `python -O verify_transport.py`.
The verifier pins each exact source tensor by SHA-256, verifies the fusion
axioms and dimension characters, checks the complete formal-codegree
polynomials, reconstructs the transport, and checks `T^2=I` and the compact
formula above. As an independent convention control it reconstructs R443
and obtains exactly `T=I+b(a-4b)^t`, including `T e_0=e_0+b`.

Importing the module and calling `verify_all()` returns a dictionary keyed
by the two census IDs. Each result includes the SymPy matrix `T`, the column
matrix `forced_unit`, `dimension_a`, `dimension_b`, `D_a`, `D_b`, `radicand`,
`rational_codegrees`, `sha256`, `swap`, and the rational CRT proof record.
The JSON receipt represents rational numbers as strings and matrices in
row-major order. No floating-point arithmetic or solver is used.

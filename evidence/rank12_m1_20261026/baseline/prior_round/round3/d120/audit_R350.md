# Independent audit of the R12_1_350 exclusion

This audit is separate from the C6 author's files. It checks the categorical
scope and independently reconstructs the finite obstruction. The executable
`audit_R350.py` imports neither the rank-six induction code nor an optimizer;
it reads the original tensor and the proposed integer rays.

The complete input is frozen in `audit_R350_inputs.json`: the original
tensor, all 30 low-branch records, and all 32 integer rays. The executable
binds the tensor to a hard-coded SHA-256 digest. It reads no parent checkout
or other project directory. For a portable replay, copy this input JSON
and `audit_R350.py` into any directory and run `python -O audit_R350.py`.
Only Python 3 and SymPy are required. Explicit checks remain active under
optimization; no `assert` statements are used.

## 1. The general-complex scope is justified

The exact dimension character takes only the values 1 and
`d = 3 + sqrt(10)`, with `d^2 = 1 + 6d`. The applicable result is
Schopieray, *Categorification of integral group rings extended by one
dimension*, JLMS 108 (2023), 1617–1641, **published Lemma 3.1**:
<https://doi.org/10.1112/jlms.12789>.
It supplies a pseudounitary Galois conjugate of any fusion categorification
of a ring with FP dimensions contained in `{1,d}`. It has no rank,
commutativity, braiding, or initial pivotality assumption. Thus excluding a
pseudounitary categorification here excludes every complex categorification.

The older preprint cached in `audit-20261025/primary/` incorrectly phrases
this as pseudounitarity of the original category. The published version,
checked directly on Wiley during this audit, has the needed Galois wording.
The argument must use that version. Nothing here infers unitarity from
pseudounitarity, or sphericality from FP positivity alone.

## 2. All low columns are covered

The full original tensor has a pointed group `S3` on input labels
`0,1,2,5,8,10` and a central self-dual noninvertible `rho=11`.
The twelve basis elements are `g` and `g rho`, and

`rho^2 = 1 + (sum_g g) rho`.

Consequently its complex algebra has six irreducibles. The trivial group
character gives the two roots `d` and `3-sqrt(10)` for rho. The sign and
standard group representations each give rho eigenvalues `+1,-1`. Their
degrees are `1,1,1,1,2,2`, and their formal codegrees are respectively
`D,D',12,12,6,6`, where

`D=120+36 sqrt(10)`, `D'=120-36 sqrt(10)`, `D D'=1440`.

The independent script also checks the regular Casimir polynomial
`(t-12)^10 (t^2-240t+1440)`. In particular the four-dimensional matrix
blocks have Casimir eigenvalue 12, and formal codegree **6**, not 12.

For the positive spherical structure, the distinct central simples in
`I(1)` therefore have restriction-unit coefficients `1,1,1,1,2,2` and
dimensions `1,1+6d,1+3d,1+3d,2+6d,2+6d`.
The first column is the actual tensor unit. Rational/irrational coefficient
comparison forces every other low column to have no invertible summands
except its prescribed copies of the tensor unit.

If `Z` is central, `F(Z)` is invariant under conjugation by every invertible
object. The conjugacy orbits on the noninvertibles are exactly
`(3,4)`, `(6,7,9)`, `(11)`, of sizes `2,3,1`.
Thus a low column is described by a triple `(a,b,c)`, with
`2a+3b+c=m` for its required noninvertible total `m`.
The values of `m` are `6,3,3,6,6`.

The correct induction Gram matrix is reconstructed directly as

`B[i,j] = sum_(a,k) N[a,i,k] N[k,a*,j]`.

Its first column is 12 at the unit, zero at other invertibles, and 6 at
each noninvertible. Hence the five triple-valued low columns satisfy
`a+b+c+2e+2f=(6,6,6)` componentwise. This gives exactly 30 ordered
assignments. In the Gram subtraction each distinct central simple occurs
once; the factors 2 belong only in the weighted first-column equation.

The independent audit enumerates all 30 assignments and checks PSD by a
different exact method: all coefficients of `det(t I + Q)` are nonnegative
for the real symmetric residual `Q`. This is equivalent to PSD, because a
negative eigenvalue would give a positive root of that polynomial.
Exactly four frames survive. No unenumerated low labeling remains.

## 3. The high columns are a necessary exhaustive domain

The complete nonunit conjugacy orbit list is
`(1,2)`, `(5,8,10)`, `(3,4)`, `(6,7,9)`, `(11)`.
Every high restriction vector is constant on these orbits and has zero
unit entry. The independent code compresses the residual Gram matrix to
one representative per orbit. Positivity of the full matrix is equivalent
to positivity of this five-by-five matrix: expanding constant rows and
columns is a congruence by a full-column-rank orbit incidence matrix.

For each candidate nonnegative integral vector `v`, it checks entrywise
Gram bounds, the full rational kernel, and the rank-one Schur condition
`v^T Q^+ v <= 1`. These are exactly the conditions that
`Q-v v^T` is PSD, not an approximate eigenvalue cutoff. Dimension tests are:

- `z = sum_i v_i d_i` is a d-number;
- `D/z` is an algebraic integer.

They hold for central simples: the center is braided, so its simple squared
norms are d-numbers (Ostrik, *On formal codegrees*, Theorem 1.8); the square
root is again a d-number. The modular formal codegree `D^2/z^2` is an
algebraic integer, which makes `D/z` integral by transitivity of integral
dependence. These statements do not require the original ring to commute.

The resulting four high-column counts are `30,43,43,28`.

## 4. All twist orders and indicator choices are covered

The categorical Cauchy theorem (Bruillard–Ng–Rowell–Wang,
*Rank-finiteness for modular categories*, Theorem 3.9,
<https://arxiv.org/abs/1310.7050>) restricts exponent primes to `2,3,5`,
the prime divisors of `Norm(D)=1440`. This is not an assertion of weak
integrality. The dimension field is `Q(sqrt(10))`, of conductor 40.

The first six joint normalized relative traces of all allowed roots of
unity are covered by orders dividing

`2^(3+floor(log_2 6)) 3^(1+floor(log_3 6)) 5^(1+floor(log_5 6)) = 7200`,

together with the zero vector. Any larger prime-power layer makes all six
Ramanujan and quadratic Gauss sums vanish. At orders within the box the
explicit Gauss formula gives 45 joint trace tuples. This finite trace image
is not an imposed bound on the actual twist exponent.

Every non-self-dual simple has second indicator zero. Every self-dual
simple occurring oddly in some `X X*` has second indicator +1 by the
adjoint parity theorem. The remaining three invertible transpositions
retain independent signs `+/-1`. Thus all eight possible assignments are
included. Allowing independent signs even where categorical conjugation
could impose equality only enlarges the domain and is safe.

For orders 3,4,5,6, the relative average of the rotation indicator is
rational because `Q(sqrt(10))` has trivial intersection with `Q(zeta_j)`.
For `H=[X^j:1]` and least prime divisor `p` of `j`, averaging the rotation
eigenvalues gives the bounds `-H/(p-1) <= nu_bar_j <= H`. Each eigenvalue's
average is `mu(n)/phi(n)` for a divisor `n` of `j`, which proves these
bounds directly.

Together with the Ng–Schauenburg center trace identities, these give the
exact rational Gram/first/second/higher indicator system. No part of this
argument uses rank six. The rank-six package is only the location of a
generic implementation; the independent audit reconstructs all equations
without importing it.

## 5. Exact certificate acceptance

There are four low frames times eight indicator assignments, hence 32
systems. For each, the independent script reconstructs all 242 integer
rows, including the 88 slack variables for higher-indicator inequalities,
and checks the supplied integer vector `y` by the two exact inequalities

`A^T y >= 0`, `b^T y < 0`.

No floating-point calculation or optimizer is used in this replay.
`audit_R350.json` records the individual strict separating values.
Passing all 32 systems proves the pseudounitary obstruction; Section 1
then promotes it to nonexistence of an arbitrary complex fusion
categorification of `R12_1_350`.

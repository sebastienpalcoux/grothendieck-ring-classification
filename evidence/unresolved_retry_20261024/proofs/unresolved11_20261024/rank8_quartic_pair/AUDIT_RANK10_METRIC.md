# Independent audit of the metric-C5 reduction for R10_1_189

Date: 2026-10-24. Sources audited: the new rank-ten `REPORT.md`,
`central_metric_probe.py`, `metric_modular_completion.py`, and the published
`case189/STRUCTURAL_PROGRESS.md` and pointed-associator package.

**Conclusion:** the conditional metric-C5 branch reduces to two
complex-conjugate rank-14 algebraic modular-data candidates, with a
nonnegative integral Verlinde fusion tensor. This branch is **not excluded**.
Neither candidate is a category construction. The initially proposed
modular-relation obstruction was a convention error, corrected during this
audit before any classification change.

## 1. Categorical and Galois premises of Section 5

Work in the pseudo-unitary Galois representative supplied by the published
general-complex gate. This preserves whether the pointed center is trivial,
Tannakian, or metric. The established pointed-associator, restriction-column,
and exponent results remain explicit project dependencies; this audit does
not independently reprove those older results.

If the pointed center is metric C5, its nondegeneracy gives the braided
factorization `Z(C)=P box E`. This applies to the center, not to C. Tensoring
by a nontrivial simple of P acts freely on all simples of that product.
Every orbit has a unique representative in E. The fifty mixed restriction
columns consequently are the five translates of the ten I(1) columns.
Subtracting their contribution from the induction Gram matrix gives the
pure matrix `4I+6J`, as stated.

One useful premise must be explicit: **E is preserved by modular Galois
permutation.** The normalized S matrix of the center is the tensor product
of the normalized matrices of P and E. In the metric pointed factor the
Galois permutation sends its label j to a multiple of j and fixes label 0;
a possible sign from conjugating `sqrt(5)` does not change that label.
Thus the P-unit sector E is stable. The inherited restriction transform
therefore acts on its pure base columns by `v'_i=v_(r^-1 i)`, without an
additional pointed translation.

The two Gram totals for E base columns are

`sum b^2=34`, `sum ||v||^2=10`, with `b in {1,2,5,10}`.

These imply the stated four pure base objects without a search cutoff.
Total 10 costs at least 20 in squared norm. Without total 5 one has
`b^2 <= 2||v||^2`, impossible. Two total-5 objects exceed the first budget.
The unique total-5 vector costs at least 5. The remaining squared-total
budget 9 then forces two total-2 vectors and one total-1 vector, attaining
all minimum norm bounds. Hence the total-5 vector is uniform and the
total-2 vectors have distinct support entries. Galois invariance now forces
the remaining columns to be `e0`, `e1+e4`, and `e2+e3`.

The twist reduction also follows. In the center, whose anomaly is trivial,
squared Galois symmetry sends a twist to its a-squared power. The unique
total-1 and total-5 E objects are fixed by every Galois permutation, forcing
their twist orders to divide 8, using the inherited prime support {2,5}.
The two total-2 objects are individually fixed when `a=+/-1 mod5` and
interchanged when `a=+/-2 mod5`; their twists are therefore
`epsilon*zeta5^r` and `epsilon*zeta5^-r`, with `epsilon^8=1`.
This argument uses the anomaly-free center, so does not silently normalize
the still-unknown central charge of E.

I replayed the finite exact indicator grid in `central_metric_probe.py`,
redirecting its output into this folder. Its four solutions agree with the
saved receipt. The integer coordinate bounds are small, so its int64
arithmetic has no overflow issue. The resulting choices `(q,c)` are
`(1,2),(1,4),(4,1),(4,3)`, all with the pure twists recorded in the report.

## 2. Fixed rows, remaining block, and mixed S formula

Let X be the unique dimension-5d object and Y the unique dimension-d object.
Their formal codegrees are 4 and 100. Every Galois conjugate of either
character has the same codegree, and positive dimensions make these
codegrees unique. Thus both characters are rational, hence integer-valued.
Orthogonality gives their squared norms 4 and 100. This conclusion requires
no unitary-category reconstruction theorem.

The first ten entries of the X row are fixed by the induction-character
formula: `1,-1,0,...,0`. Its remaining norm is 2. The dimension-weighted
sum permits exactly the two alternatives stated in the report. The choice
supported positively on both P objects violates the absolute-value bound
in the twist-weighted identity. The other gives

`lambda_X=(1,-1,0,0,0,0,0,0,0,0,-1,0,0,1)`

and central charge `xi_E=1`. For Y the known induction entries, symmetry,
and rationality give equal P values u and Y value t. The equations
`t+4u=13` and `t^2+2u^2=41` have only the integral solution `(t,u)=(-3,4)`.
The displayed Y row follows. The remaining symmetric P block has equal
diagonals by its Galois interchange; its norm and unit orthogonality give
the two values `(3+sqrt(5))/10` and `(3-sqrt(5))/10` as claimed.

The mixed S formula is consistent with positive double braiding. If
`chi(g)=zeta5^l`, its constituent A_chi has P label `l/(2q)`, because
monodromy with g is `zeta5^l`. Dividing the center's normalized S entry by
the pointed-factor entry contributes `sqrt(5)` and the phase
`zeta5^(-l_chi*l_psi/(2q))`. Since `sqrt(5)/dim(C)=1/(10d)`, this gives
exactly the report's formula. A pure E object has P label zero, hence no
phase correction.

Duality is also correctly identified. The constituent associated with a
character has dual associated with its complex conjugate; thus B_l and
C_l are paired with labels -l. Their P labels change sign at the same
time, so the same pairing holds in E. The unique objects of dimensions
d and 5d are selfdual. The two dimension-2d objects have distinct twists,
and duality preserves twist; each is therefore selfdual.

## 3. Convention error found and corrected

With positive-monodromy normalized S and the actual twist matrix Theta,
the identity in this central-charge-one case is

`S Theta S = Theta^-1 conjugate(S) Theta^-1`.

The original checker omitted `conjugate` on the right. That would falsely
exclude nonselfdual data. A direct check on a metric cyclic pointed
category already exhibits the problem: summing the Gaussian kernel gives
the negative cross term, hence the conjugate S entry.

This agrees with the primary convention in EGNO: Definition 8.13.2 uses
positive double braiding, while Theorem 8.16.1 pairs it with the matrix of
**inverse twists**. The rank-ten investigator corrected the script and
report after this audit identified the discrepancy. The proposed
metric-branch exclusion is withdrawn; no such exclusion appears in the
final report.

## 4. Independent exact replay and remaining scope

`audit_rank10_metric.py` independently constructs the first surviving
matrix, twists and dimensions using SymPy's algebraic field Q(zeta5),
rather than the investigator's coefficient-array arithmetic. It verifies
the positive first row, global dimension, central charge, symmetry,
`S^2=C`, conjugation/duality compatibility, the corrected modular relation,
both rational character rows, and all **2744** Verlinde coefficients.
Every coefficient is a nonnegative integer; the maximum is 4.

The fusion tensor SHA256 is

`750dfbdbf9cddde4efb5b62d389bf4cd8e6040b77c7aaf73e9d10b020e6f75d1`.

It agrees with the independently exported rank-ten tensor. The second
surviving presentation is exactly the complex conjugate of the first,
including its twists. The alternative mixed assignments fail integrality,
while the other pure-block sign fails `S^2=C`. See
`audit_rank10_metric_receipt.json` for the standalone audit result.

The rank-six investigator independently checked the modular second
indicators by both the full Bantay double sum and a factored S formula,
obtaining

`(1,1,0,0,0,0,0,0,0,0,-1,1,1,-1)`.

This passes the selfduality requirements. The corresponding files are
`../rank6_pair/verify_metric_c5_fs2.py` and
`../rank6_pair/metric_c5_fs2_certificate.json`.
The rank-six investigator also reports exact passes for indicators 1
through 10 and all 140 corresponding cyclic rotation spectra. Those
additional checks belong to that investigator's receipts; this audit's
independent replay is the complete matrix and Verlinde calculation above.

The verified objects are algebraic modular-data candidates with a fusion
ring. Associators and a categorical realization of the rank-14 factor
have not been supplied. Even such a realization would still need the
appropriate center/Lagrangian-algebra realization to recover the original
rank-ten category. The source ring therefore remains unresolved.

Primary references checked for this audit:

* EGNO, Definition 8.13.2, Propositions 8.13.8 and 8.14.2, Corollary
  8.14.4, Theorems 8.16.1 and 8.21.4:
  <https://math.mit.edu/~etingof/egnobookfinal.pdf>.
* Bruillard-Ng-Rowell-Wang, normalized Galois symmetry Theorem 2.9 and
  modular-indicator Theorem 2.13:
  <https://arxiv.org/html/1310.7050v3>.
* Schopieray, induction-character/forgetful compatibility, Equation (5):
  <https://arxiv.org/html/2609.35287>.

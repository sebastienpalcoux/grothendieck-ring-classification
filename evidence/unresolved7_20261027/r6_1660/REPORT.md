# R6_8_1660: individual theoretical continuation

27 October 2026. **Unresolved. No complex categorification was constructed or
excluded.** This pass obtained two further module-category obstructions and
new restrictions on any possible center. All calculations were short exact
matrix or character calculations; there was no pentagon search.

## Two possible module realizations are excluded

Using the positive pivotal-Frobenius forgetful pairing lemma, the archived
III_mixed solution0 and IV_mixed solution1 cannot be module categories.
In the first, a selfdual simple bimodule forgets to sigma+T; in the second,
one forgets to X+gX+sigma+T. The source sigma has second indicator-1 and
all other source simples have indicator+1. Both restrictions have odd
multiplicities of opposite signs, which no nondegenerate pure-sign
selfduality pairing can accommodate.

These are two possible self-Morita realizations, not two new excluded census
rings. The typeII realization still permits the original based-ring type;
the rank-eight R941 route and the Ad(E6)-based rank-six alternative also
pass the new filter. `MORITA_PAIRING_FILTER.md` records the exact restrictions,
its pivotal-Frobenius hypothesis, and the surviving scope. Independent audit
and source-bound replay are in `../audit_fs2/`.

## New center constraints

`SPIN_CONSTRAINTS.md` proves the following necessary conditions.

* The six-dimensional negative spin representation W_44,2 is impossible in
  low frame0. In frame1 it requires four phase12 columns, two X+T and two
  gX+T, and also requires asymmetric phase36 columns.
* If phase36 is symmetric, a dual-difference fusion diagonal is exactly
  -1/2, contradicting integrality. The frame1 total asymmetry budget is8,
  so the condition does not cover every frame1 placement. Even fermion
  partners at phase36 give a surviving diagonal0.
* For the distinguished Galois-unit simple A_7 with dimension d^2, fusion
  on the charge-conjugation-negative space is a signed permutation
  involution. Its eigenvalues are+1 on the S-transformed spin sector and
  -1 on its complement. This is stronger than an integrality check on its
  trace, but no contradiction from this condition alone was established.

Both complete spin alternatives W_16,2+W_20,2 and W_44,2 retain possible
placements. Necessary representation data is not counted as a model.

## Construction routes reconsidered

The existing regular Ising-bimodule and Ad(E6)-based Morita descriptions were
revisited as potential construction routes. Neither supplies the missing
associator or a forced separable algebra. The previously excluded exceptional
SU(4)_8, SU(3)_21, F4_3 and G2_4 dimension/Morita routes were checked against
this approach; no dimension match was promoted to a category. A fermionic
reduction gives a superfusion problem with additional odd morphisms, so an
ordinary rank-two classification does not close it. The earlier no-real-form
obstruction remains compatible with the known complex-conjugate Ad(E6)
precursors and therefore is not itself a construction obstruction for all
such routes.

## Checks

`verify_spin_constraints.py` binds the source tensor, rebuilds the induction
Gram, checks both high asymmetry budgets, the exact Galois ratios, and the
three short representation transition calculations. It also checks the
surviving diagonal0 explicitly, preventing the erroneous promotion of the
conditional -1/2 to a full-branch exclusion. Runtime is about2 seconds in
ordinary Python; the same explicit checks run with `python -O`.

`spin_constraints_receipt.json` records the inputs and results. The separate
module-pairing audit reconstructs the source action matrices and duality
rather than trusting the displayed restriction vectors. None of this
research changes public classifications or website data.

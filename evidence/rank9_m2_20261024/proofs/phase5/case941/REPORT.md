# R9_2_941: new exclusion by central dimension parity

A new general-complex exclusion is proved in `EXCLUSION_THEOREM.md`.
It settles the exact dimension-504 exotic ring displayed in
Alekseyev–Bruns–Dong–Palcoux, arXiv:2507.07023v2, Question 1.14.
Independent parent audit is requested before integration into the canonical
ledger; this folder does not mutate previous phases or any online source.

The proof is theoretical. Modular-character integrality restricts every
63-dimensional central simple to one of two underlying objects U,V.
V is the unique such summand of I(1). The dimensions of I(Y) and I(C_l),
reduced modulo two, then force an odd number of central dimension-nine
simples above each of the three dimension-nine source simples.
The hypothetical center is simple because the source category is simple
and cannot be braided. A prime-power-dimensional central simple contradicts
that simplicity by ENO Corollary 7.2.

The two-column lemma is proved by explicit congruences modulo nine and
seven, followed by seven elementary aggregate cases and two exact norm
bounds. No bounded associator search, floating-point claim, or unitary-only
result occurs in the final proof.

`verify_odd_columns.py` independently checks the original tensor and all
729 coefficients against the published tensor, all ring axioms, simplicity,
all character identities, and the complete odd-column arithmetic with exact
rational operations. The regenerated dimension-63 list contains exactly
U and V. The standard-library replay finishes in under one second here.
It also verifies an independent 15-term mod-two Gram relation with odd
right side 937. Output is `odd_columns_verified.json`.

Exploratory optimization first found integer infeasibility; an exact mod-two
linear relation then replaced that computation entirely. `integer_gram.py`
also finds an independent mod-three contradiction and Z3 confirms integer
infeasibility, but neither is needed in the final proof. `full_center.py`
records a feasible integer frame when prime-power center dimensions are
allowed, demonstrating why the structural center-simplicity input matters.

All new work is confined to `phase5/case941/`.

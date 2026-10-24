# Weak-integral continuation: two theoretical obstructions

All four assigned cases have general-complex exclusion proofs:

| Case | Argument |
| --- | --- |
| R9_2_1303 | Every extension of its dimension-60 neutral category is group-theoretical, contradicting dimension 2 sqrt(5) |
| R9_2_1709 | Cyclic internal-end multiplicity-free obstruction |
| R9_2_1759 | Cyclic internal-end multiplicity-free obstruction |
| R9_2_1988 | Cyclic internal-end multiplicity-free obstruction |

The same arguments also exclude R9_2_585 and R9_2_1025, respectively.
Neither obstruction assumes a pivotal, spherical, unitary or braided
structure. Both proofs cover arbitrary associators of a hypothetical
categorification. The exact checks bind all six unchanged input tensors
by SHA-256 and verify every required ring hypothesis.

Run:

    python verify_cyclic_obstruction.py
    python verify_dimension120_obstruction.py

Both checks passed. They use explicit exceptions, so python -O does
not disable the mathematical checks.

The independent audit in `BRAIDED_SCOPE_INDEPENDENT_AUDIT.md` supports
the three additional braided-only refinements from the integral group.
An attempted upgrade through central induction did not establish a
central Rep(S3) for arbitrary categorifications of R12/R959. Their
general status is therefore not changed by that attempt.

No repository or website was edited by this work. No classification
ledger is modified here; the parent integration must record decisions
after independent proof review.

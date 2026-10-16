# Separate computational checks

`independent_models.py` reconstructs all fifteen fusion tensors using group,
product, truncated SU(2), near-group, and stated exceptional fusion rules,
then finds explicit based isomorphisms. The existence of categories is cited
in the manuscript, not established by these tensor checks.

`unpruned_census_audit.py` disables both dimension prunings in a temporary copy
of the ordinary enumerator and filters its full output using separately written
Python tensor formulas and determinant expansion. It still shares the
Diophantine elimination with the production search.

`../census/audit_small.py` uses direct matrix commutators on the complete
multiplicity-two box instead of the optimized elimination. It shares the tensor
presentations and canonicalization, and is a small-bound regression rather than
a second all-bound completeness proof.

The root `audit/check_regressions.py` also compares signed optimized/reference
searches at bounds one and two and checks exact model and scalar identities.
All these checks are included by `python3 supplementary/check.py --deep`.

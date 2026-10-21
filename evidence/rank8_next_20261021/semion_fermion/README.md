# New semion/fermion center constraints

R8_3_928 and R8_3_941 remain unresolved. This package adds exact constraints
on their distinguished central fusion products. It changes no ledger or
manuscript and constructs no category.

The useful new result is rigidity: all three negative-charge pair products
have uniquely forced multiplicities. For each of the fourteen current R941
allocations, the positive products are constant on fermion pairs and have the
same **unique** integral completion up to relabeling equal-type pairs. All ten
current R928 cases also have exact integral pair-product witnesses. These
witnesses do not resolve the separate twist-feasibility questions.

| Test | Exact outcome |
|---|---|
| Fourth Verlinde moments and coupled restriction Gram | 343/343 patterns pass for each ring |
| Charges and five translated distinguished objects | 15/15 semion patterns;49/93 fermion allocations pass |
| Intersection with current final cases | 10/10 R928;14/14 R941 pass |
| Integer pair-product completions | Exact witnesses for all24 current cases |
| Unit coefficients of words through degree10 | 2002 per case, all integral and nonnegative |

[PROOF.md](PROOF.md) gives the normalization, linear algebra, involution
argument, complete finite integer-row bound and scope. Producer scripts have
matching JSON receipts with source SHA256 bindings. `verify.py` checks the
witnesses, independently enumerates the sixteen R941 uniqueness cases, and
checks2070 actual Z(Ising) and200 double-semion identities. Normal and `-O`
outputs are identical.

[QUADRATIC_REVIEW.md](QUADRATIC_REVIEW.md) is the separate independent review
of the quadratic workstream. Its read-only verifier reproduces the148-object,
182-factor Morita closure,75 full-rank actions,32 classes and32 positive
controls without importing any quadratic producer.

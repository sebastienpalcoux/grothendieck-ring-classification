# Twelve integral rank-seven general exclusions

The six proofs cover the following exact census identifiers.

| Family | Census rings | Obstruction |
|---|---|---|
| Dimension (8p) | R7_2_70, R7_2_213, R7_4_358 | Iterated equivariantization; order-eight representations and coprime action strictification |
| Dimension 112 | R7_3_386, R7_3_966 | A Singer cycle cannot be inverted in GL3(2) |
| Dimension 96, existing branch | R7_2_113, R7_2_273 | Impossible S3 orbit pattern on a group of order sixteen |
| Dimension 96, other branch | R7_2_50, R7_2_280 | Three inequivalent rank-one Vec(V4) modules, but only two classes |
| Dimension 54 | R7_3_398, R7_3_478 | Inversion is central in the pointed Brauer–Picard group |
| Dimension 310 | R7_4_963 | Square-free group-theoretical double-coset dimensions |

All twelve conclusions are general exclusions over the complex numbers.
`STRUCTURAL_INPUTS.md` separates the published inputs from the new arguments.
`approved_general_decisions.json` binds each tensor to its original raw-census
line and hash. The immutable recovery stage also preserves all full tensors.

The exact checker uses Python 3's standard library:

```sh
python3 evidence/upper_residual_20261002b/r7_integral/verify_general_families.py
python3 -O evidence/upper_residual_20261002b/r7_integral/verify_general_families.py
```

Each run checks all 343 coefficients against the raw census for each case,
2401 associativity identities per ring, the positive dimension character,
duality, adjoint closure, invertible-group structure, the actual sign
permutation and conditional first-descent dimensions. It also exhausts the
small binary and modulo-four matrix groups needed in the arguments, and
rejects altered unit and sign-action controls. Both saved receipts have
identical mathematical content and passed with optimization enabled.

Correction to the retained pre-failure summary: R7_2_213 has invertibles

\(C_4\), whereas R7_2_70 and R7_4_358 have invertibles

\(V_4\). Its exclusion is simpler: the forced order-eight representation
subcategory would have 
\(V_4\) linear-character group. The complete source tensor establishes
this distinction; no relabelling can turn 
\(C_4\) into 
\(V_4\).

The checker verifies algebraic premises and finite calculations. The written
proofs and their primary citations supply the category theory; no automated
formalization of those cited theorems is claimed.

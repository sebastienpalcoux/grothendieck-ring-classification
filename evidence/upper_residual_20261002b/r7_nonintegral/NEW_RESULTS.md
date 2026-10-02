# Rank-seven nonintegral decisions and scoped results

General exclusions: R7_3_1036, R7_3_1044, R7_4_2510, R7_4_2706.
Their full oriented signed enumerations contain 8, 24, 4, 48 tables. Every
character of every table is explicitly rejected by zero, duality or norm.

Unitary modular model: R7_2_240, the D12 even part, with complete coefficient
comparison and the model-to-census map [0,5,3,6,4,1,2].

Pivotal-only exclusions: R7_4_1212, R7_4_1213, R7_4_1417, R7_4_1420.
Their general status remains unresolved. No unfinished signed search is
interpreted as a mathematical exclusion.

Run from the repository root:

    python3 evidence/upper_residual_20261002b/r7_nonintegral/verify_nonintegral_results.py
    python3 -O evidence/upper_residual_20261002b/r7_nonintegral/verify_nonintegral_results.py

The source census and all loaded signed-engine modules have explicit SHA256
bindings. `verification_normal.json` and `verification_optimized.json` record
fresh complete replay, including incomplete-branch, invalid-norm, omitted
pivotal-character and scope-promotion rejection controls.

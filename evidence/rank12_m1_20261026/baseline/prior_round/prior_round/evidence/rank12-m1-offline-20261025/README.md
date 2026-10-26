# Rank 12, multiplicity one: established-method offline pass

**632 supplied rings = 393 excluded over C + 127 unitarily realized + 112 unresolved.**

No GitHub repository or website was modified. Results concern based rings, not a count of tensor-equivalence classes. Independent human verification remains pending.

## Read first

- `report.pdf` / `report.tex`: conclusions, theoretical scope, precise limits and references.
- `ledger.csv`: one readable decision per permanent physical input line.
- `ledger.json`: hashes, all overlapping exclusion evidence and preferred construction.
- `unresolved_tensors.json`: all 112 remaining based tensors.
- `unresolved_families.json`: independently checked exact positive dimension characters.
- `verification.json`, `verification_optimized.json`: successful complete accepted-witness replays.

## Exact replay (short; no network or discovery solver)

Python 3.10 or newer, NumPy, SymPy and NetworkX are needed. Install `requirements.txt`, preserve this extracted layout, and run:

```sh
python verify.py
python -O verify.py
```

The complete accepted replay checks the source bindings and fusion axioms, every stored closed subring embedding, accepted arithmetic/support/cyclic/central-order/primary/Liptrap witnesses, the inherited lower-rank proofs, all 127 positive rings and all 402 recorded model identifications. Some standard algebraic-number infrastructure and standard tensor constructors are shared: independent witness checks do not mean an independent formalization of every referenced categorical theorem.

The C++ canonical input audit is in `independent_input/output`. Its source is `sources/census_verifier/verify_tables.cpp`; recompile it and feed the decompressed original table file to repeat that separate check. It found exactly 632 associative distinct based rings, with no duplicates. The input archive's own verification and provenance remain in `input/rank12_M1_verified`.

## Evidence and code

All tensors use N[i][j][k], coefficient of b_k in b_i*b_j. The unit is b_0. IDs R12_1_i use one-based physical lines and have not been reordered.

`arithmetic.json`, `subrings.json`, `cyclic.json`, `spectra.json`, `field_checks.json`, `primary_full.json`, `feudal.json`, and `lower_known.json` contain accepted witnesses and exact attempt records. `models.json`, `additional_models.json`, `group_models.json`, and `twisted_c2_models.json` contain explicit constructions, full model tensors and basis maps. `lower_rank*.json` and `sources/` preserve the accepted lower-rank premises and implementation snapshots.

`modules.json`, `induction.json`, reduced primary results and construction attempt inventories include feasible relaxations, search limits and unsuccessful candidates. These are never exclusion or existence proofs. In particular, a failed finite phase search is not a complex obstruction; the accepted negative Liptrap records cancel arbitrary nonzero complex variables by integer monomial relations. The ordinary and optimized witness replays do not rerun discovery.

The discovery scripts are included for transparency. They are separate from `verify.py` and may overwrite attempt receipts when deliberately rerun. The low-induction script resumes its bounded attempt ledger. Its initial interrupted log is historical research output, not a completed campaign. There is no long frame, conductor, modular-data or numerical pentagon search in this package.

All general exclusions using unitary positivity carry the proved solvability/unitarizability bridge. Two-FP-value Galois-pseudo-unitarity is not assumed to imply unitarity. No Isaacs conjecture or braided-only classification is promoted to a general exclusion.

`MANIFEST.sha256` binds the delivered snapshot. Generated verification times can change on replay. This is an offline established-method pass; the remaining 112 cases have not been declared impossible, and no novelty up to tensor equivalence is claimed for the recorded constructions.

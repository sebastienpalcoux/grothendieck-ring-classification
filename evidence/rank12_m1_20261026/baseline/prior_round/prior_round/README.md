# Rank 12, multiplicity one: audit and theoretical continuation

**632 supplied based rings: 425 excluded over C, 141 unitarily modeled, 66 unresolved.**

The first round's 393 exclusions and 127 models were retained after independent mathematical review and exact rechecking. The new work settles 46 of its 112 unresolved cases: 32 exclusions and 14 models. No repository or website was revised. Independent human verification remains pending.

## Read first

- `report.pdf` / `report.tex`: complete mathematical report, new theoretical arguments, construction premises, references and limits.
- `ledger.csv` / `ledger.json`: all 632 permanent IDs and input hashes, previous and current decisions, proof routes and model data.
- `new_decisions.json`: all 32 new negative decisions and 14 new modeled rings, including recorded alternative constructions.
- `unresolved_tensors.json`: all 66 remaining complete tensors, exact dimension characters and scoped categorical implications.
- `evidence/`: frozen first-round data plus the continuation's full proofs, constructor data and independent audits.

## Theoretical progress

The new exclusions use arbitrary subgroup stabilizers and balanced bimodules; an elementary Morita enlargement; a small mod-four signed-sphericalization reduction; full extension/cohomology classification of the dimension-40 family; and the known duality of stabilizers of invertible pointed bimodules. Every general exclusion has the necessary categorical scope proof. All 20 cubic cases and all four large quadratic cases are excluded. The original dimension-24 and dimension-40 families are completely settled.

The 14 new model IDs are 25,30,79,80,156,263,322,323,417,428,449,513,541,597 in the permanent R12_1_i notation. They include ordinary representation categories, actual group-theoretical subgroup algebras, triality gaugings, coherent TY equivariantization, central zests and fully reconstructed Morita duals. Matching a proposed modular datum or a based-ring automorphism alone is never used as a categorical construction.

The remaining families have respectively 15 cases of dimension120, 22 of dimension48, 20 of dimension32, four of dimension144, and five two-dimension cases of C6 type. They received several structural and construction attempts, but no unsupported status was assigned. Conditional candidates and unsuccessful finite searches remain research notes, not proofs.

## Standalone exact replay

Use Python 3.10 or newer with `requirements.txt`, and run from this extracted directory:

```sh
python verify.py
python -O verify.py
```

The accepted replay needs no network, optimization solver, or discovery search. It takes roughly a minute per pass on the recorded machine. Each subprocess log and the aggregate receipt appear in `verification/`. It verifies all first-round evidence and independent audits, all new exclusion premises and complete cohomology coverage, the new categorical constructions' exact data, every accepted new basis identification and all delivered ledgers. Symbolic arithmetic and standard categorical theorems remain explicitly identified premises; this is not a proof-assistant formalization.

The top-level ledger is authoritative. Some subtask files describe results local to one family and may list a case resolved independently elsewhere; this is historical scope, not a competing final status. Discovery scripts are included for transparency and may overwrite exploratory receipts if deliberately rerun. They are not needed by the accepted replay.

The source input and all based-ring labels are unchanged. First-round evidence is at `evidence/rank12-m1-offline-20261025/`; current proofs are at `evidence/rank12-m1-round2-20261025/`. The full SHA-256 manifest binds the delivered snapshot; verification receipts acquire new timings when replayed.

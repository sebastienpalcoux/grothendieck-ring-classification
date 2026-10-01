# New necessary reductions for the two unresolved rank-six rings

Both **R6_4_155** and **R6_8_1660** remain unresolved. This supplement records
audited necessary conditions, not constructions of fusion categories.

- **R6_4_155:** the complete modular datum of the forced rank-26 semion
  centralizer is unique in the established conventions. Its Verlinde tensor
  is nonnegative integral, with maximum coefficient 9. It has ten self-dual
  objects. All stated finite Vafa and indicator checks pass. Three possible
  connected-étale underlying objects remain; a proposed condensation route
  from three order-32 near-group centers is excluded.
- **R6_8_1660:** every indecomposable module category has rank six. A formal
  codegree bound, exact Morita reconstruction and a second-indicator obstruction
  leave three possible Morita-dual based rings. A Galois/duality divisibility
  condition excludes profile 133, leaving **1,669** labelled center profiles
  in branches **163, 753, 753**.

Read [the research report](report/frontier_research.pdf) for the proofs and
the scope of each finite check. The report's LaTeX source and all required
exact scripts and receipts are included. Independent audits are in
`r155_models/modular_audit/`, `r1660_categorical/` and `r1660_indicators/`.

## Replay

Python 3.12, NumPy and SymPy are sufficient. Tested versions are recorded in
`requirements.txt`. Within the complete release, run:

```sh
python research/frontier/new_research/replay.py
python research/frontier/new_research/replay.py --optimized
```

For a standalone supplement, supply the extracted completed multiplicity-nine
package using `--package /path/to/Rank6_Categorification_M9`.
Each of the twenty jobs runs in a fresh interpreter with a three-minute limit.
The ordinary replay took about three minutes in total. The scripts use explicit
checks which remain enabled under Python optimization. Replaying regenerates
local receipts and logs; it does not change the base classification ledger.

`verification/replay.json` and `verification/replay_optimized.json` record the
two full replays. Finite indicator checks cover exactly the orders stated in
the report, with no assertion about untested tensor orders.

The original multiplicity-nine release and its source-bound certificates remain
unchanged. Counts remain **25,362 excluded, 57 realized, 2 unresolved** among
25,421 rings. All 8,809 rings of exact multiplicity nine remain excluded.

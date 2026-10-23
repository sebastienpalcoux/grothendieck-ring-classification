# Ranks nine and ten: current publication

The common Atlas records 102 exclusions and 40 unitary models at rank nine, and **136 general complex exclusions, 57 unitary models and one unresolved ring at rank ten**. The sole rank-ten frontier is R10_1_189.

[Current manuscript](../publications/rank9-rank10/paper/rank9-rank10.pdf) · [Accepted ledger and proofs](../evidence/rank10_m1_exclusions_20261023/README.md). The original [baseline package](../evidence/rank9_rank10_m1_20261023/README.md) remains frozen for replay.

## Ordered presentation

Every rank uses the same counts, model catalogue, manuscript shelf, records directory and case renderer. Current findings precede invariants and fusion data; supporting reports and searchable evidence stay folded by default. There is no separate high-rank interface.

## Source and build

The baseline builder reads the original 336 tensors and ledger. It then automatically applies `site/rank10_exclusions.py`, which validates the six tensor hashes against `evidence/rank10_m1_exclusions_20261023/classification_updates.json` and the current accepted ledger. The overlay changes five decisions and records the proved restrictions for case 189. No data from ranks two through eight are rewritten.

```bash
python3 site/build_rank9_10.py
python3 tools/sync_rank10_m1_publication.py
python3 site/build_rank11.py
python3 site/check_rank9_10.py
python3 site/check_rank11.py
python3 site/smoke_test.py
node site/check_cases.mjs
```

Recompile the canonical manuscript before synchronizing publication hashes. The synchronization script also builds a portable proof archive, updates the manuscript page inventory, and binds the current website PDF. The full general-complex exclusions and the finite scope of the imported superpentagon result are stated in the manuscript. Case 189 remains unresolved, with separate spherical/Galois implications and a braided exclusion.

Historical receipt scopes and baseline archives are preserved byte for byte. Current hashes are checked against the accepted source tree before publication.

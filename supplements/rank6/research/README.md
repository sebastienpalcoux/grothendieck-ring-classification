# Automated frontier research

The main paper proves the necessary criteria and states their categorical scope.
All current decisions come from `data/decisions.json`; feasible relaxations do
not establish existence.

The current research is in `m8_frontier/`:

- `low_product_gram.py --check` reconstructs and checks the joint fourth-order
  Gram and restriction equations at the first unresolved tensor. The retained
  point survives; no general exclusion or model is asserted.
- `premodular_bound.py` derives exact Frobenius–Perron dimensions and applies
  the Dong–Schopieray rank-six bound to all nonexcluded ledger entries. Its
  conclusions concern braided spherical categorification only.
- `nrw_rank6_scan.py` compares the entire trusted census with the pinned
  Ng–Rowell–Wen rank-six modular tensors, including every unit-preserving basis
  permutation after invariant prefilters.

These commands use standalone exact programs and local source data. They do
not invoke AI services or enumerate a new census. Source URLs, hashes, computed
certificates and explicit nonconclusions are included alongside the scripts.
The `m8_audit/` notes record scope checks and targeted automation controls.

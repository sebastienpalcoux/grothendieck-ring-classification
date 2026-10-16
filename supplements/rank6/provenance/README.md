# Census and literature sources

The rank-six census contains 25,421 tensors through exact multiplicity nine,
including 8,809 at multiplicity nine. Its published data commit is
`2a340871242879665fa7ba2b01fa15b8bdeaada3` in the
[fusion-ring-census repository](https://github.com/sebastienpalcoux/fusion-ring-census).
`rank6_M9_verified/repository_source.json` binds the compressed and uncompressed
hashes and distinguishes the enumeration-code commit from the data commit.

All 17 source checksums pass. `software/import_verified_census.py` checks the
based-ring axioms by bounded exact integer arithmetic and examines all 120
unit-fixing basis permutations per tensor; no duplicate based ring is found.
Enumeration completeness uses the source run manifest and completed logs;
this classification package does not repeat that enumeration.

`verification/m9/census_import.json` records the exact preservation of 16,612
established representatives, identifiers and labels. The correspondence in
`rank6_M9_verified/classification_transport.csv` uses identity basis
permutations while recording the source's different row order.

`census_LICENSE.txt` reproduces the census repository notice and its scope.
It does not assign a license to the mathematical manuscript. Ng–Rowell–Wen
ancillary fusion tensors, download URL and hash are identified in
`research/m8_frontier/nrw_rank6_scan.json`. The manuscript bibliography and
model catalogue attribute the categorical inputs.

Use the [current frontier](../research/frontier/README.md),
[decision ledger](../data/decisions.json) and
[repository provenance](../../../docs/PROVENANCE.md) for the current scope.
Source-bound calculation files state their own finite domains. Hash identity
is not mathematical verification; all project research is AI-generated and
has not yet been independently human-verified or Lean-formalized.

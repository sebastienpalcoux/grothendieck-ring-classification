# Census and literature sources

The classification uses the supplied verified laptop rank-six census through
exact multiplicity nine: 25,421 tensors, including 8,809 new tensors. The full
supplied archive is retained in `rank6_M9_verified/`; `repository_source.json`
records its exact compressed and uncompressed hashes. Its source commit refers
to enumeration code and systems, not a repository commit containing these data.
The subsequently published data commit is
`2a340871242879665fa7ba2b01fa15b8bdeaada3`; it is recorded separately as
`published_data_commit`, with the original enumeration-code commit retained.

All 17 supplied checksums pass. `software/import_verified_census.py` independently
rechecks the based-ring axioms using bounded exact integer arithmetic and examines
all 120 unit-fixing permutations per tensor. The audit finds no duplicate based
rings. The complete enumeration is evidenced by the supplied run manifest and
completed logs; this package does not repeat that enumeration.

`verification/m9/census_import.json` records the independent checks and exact
preservation of all 16,612 earlier rows, including every identifier, tensor and
source label. The classification-to-source correspondence is recorded explicitly
in `rank6_M9_verified/classification_transport.csv`. All current transports are
identity permutations; the source uses a different row order. The original
multiplicity-eight source manifest is retained as
`rank6_M9_verified/previous_repository_source.json`.

`census_LICENSE.txt` reproduces the repository notice, whose stated scope is
new code in that repository. It does not assign a new license to this paper.

The Ng–Rowell–Wen rank-six ancillary tensors and their exact download URL and
hash are recorded in `research/m8_frontier/nrw_rank6_scan.json`. The manuscript
bibliography and model catalogue give attribution for categorical inputs.

The retained revision notes preserve earlier releases and their original
status statements:

- [`REVISION_NOTES_first_continuation.md`](REVISION_NOTES_first_continuation.md)
- [`REVISION_NOTES_second_continuation.md`](REVISION_NOTES_second_continuation.md)
- [`REVISION_NOTES_third_continuation.md`](REVISION_NOTES_third_continuation.md)

These files are historical provenance. The [root revision notes](../REVISION_NOTES.md),
[decision ledger](../data/decisions.json) and
[current frontier summary](../data/frontier_summary.json) describe the current
unresolved rings and their necessary reductions. The earlier
[`research/frontier/coverage.json`](../research/frontier/coverage.json) retains its
historical multiplicity-eight scope. Earlier proof sources remain available
with their original scope; the additional campaign is under `verification/m9/`.

The full-tensor import audit for the standalone R3582 and B13 arguments is
retained in [`IMPORT_AUDIT.md`](../research/round2_external/IMPORT_AUDIT.md);
B13 lies outside this census.

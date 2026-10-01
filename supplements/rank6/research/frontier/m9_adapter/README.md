# Historical frontier bindings in the M9 extension

The historical `research/frontier/coverage.json`, `inputs.json`, certificate
files and retained mathematical receipts remain unchanged. Their two rings are
still distinct from the new multiplicity-nine frontier.

`manifest.json` declares the extension of their source bindings:

- The first 16,612 census and ledger rows must reconstruct the exact historical
  compact JSON bytes, including row order, every metadata field and the final
  newline. Their original SHA-256 hashes remain authoritative. Extra rows must
  have multiplicity greater than eight.
- Every frozen or embedded source hash is checked. The historical inventory
  contains 99 distinct files. `software/proofs.py` and the mathematical
  verification code retain their original bytes.
- The original frontier driver is preserved in
  `frozen_sources/frontier_replay.py.txt`. Its replacement must equal the closed
  exact patch declared in `software/frontier_m9.py`, and match its declared
  adapted hash. The patch changes only source-binding routing and audit output;
  it leaves mathematical predicates, commands and replay execution unchanged.
- Any other source change is rejected. There is no rule that silently refreshes
  a historical hash or treats a changed verifier as freshly replayed.

Run `python -B -O software/frontier_m9.py --audit-only` for the retained receipt
audit, or `--controls` for temporary prefix/patch mutation controls. The adapted
historical command also works:
`python -B -O software/frontier_replay.py --check-receipts`.
These commands do **not** replay the mathematics. The retained inventory has
19 receipt predicates covering the two historical rings.

After the final source-bound M9 release is built, run
`python -B -O software/frontier_m9.py` to create separate
`research/frontier/m9/inputs.json` and `coverage.json`, and regenerate
`data/frontier_summary.json` from all unresolved ledger IDs. Use `--check-current`
to validate those generated files without rewriting evidence. New rings inherit
no historical spherical or Galois reduction. Each separately proved pivotal,
spherical or pseudo-unitary nonexistence claim is shown once at its strongest
declared scope, with its exact-replay receipt and the resulting five existence
columns. General existence remains unknown for every scoped-only claim.

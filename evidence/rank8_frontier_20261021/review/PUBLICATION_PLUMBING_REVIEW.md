# Publication and research replay plumbing review

This is a source/packaging review, not an additional mathematical proof.
It was performed before the final prepared ledger and release replays.

## Confirmed invariants

- `accepted.json` contains25 general exclusions and does not accept R941.
  `commands()` includes every accepted verifier and deduplicates explicit
  research commands. No registered command declares a required CLI option.
- All808 inherited baseline proof/source/log hashes pass `baseline_inputs`.
  The immutable archive has1011 checksum-covered members. Its rank-eight
  M3 evidence and software members are byte-identical to the local copies.
- The final four NC canonical commands and the independent R928/R941
  reviewers are registered. The final NC ledger distinguishes exact
  necessary-data witnesses from six unresolved integer-feasibility branches.
- The updated final-domain guard covers the four NC joint-spectrum IDs,
  their hashed terminal ledger, the16 fermionic integer attempts, all93
  fermionic paired cones, all15 semion-moment cones, all10 semion-pair
  cones, and all48 R455 cones. It also requires the separate five-case
  commutative integer ledger. Before that ledger exists, it correctly blocks
  a screening-complete designation; it does not silently waive the queue.
- The obsolete incomplete R941 unpaired calculation is identified as
  exploratory. The corrected charge receipt is bound by hash in the new
  charged joint-spectrum receipt. No obsolete R941 numerical conclusion
  appears in the accepted decision registry.

## Concrete omissions found and corrected by the registry owner

The pinned rank-four theorem file
`manuscripts/rank4/papers/companion_sections/14_finite_certification.tex`
was absent from both the baseline archive and explicit dependency list.
It is read by the R65, generalized-near-group, and R941 quotient verifiers.
The registry now explicitly includes it.

The accepted R439 verifier imports the rank-five software tree, which was
also absent from the baseline archive. The exact static import/runtime
closure is now explicitly included:

- `exact.py`, `gram_vectors.py`, `higher_traces.py`, `induction.py`,
  `proofs.py`, `rings.py`, `signed.py`;
- the compiled inputs `gram_vectors.cpp` and `low_completion.cpp`.

All these paths are under `supplements/rank5/software/`. The native sources
have no further local include or data dependencies. A scan of existing
literal external input paths found no additional unbound inputs. No
compressed/text frontier data files fall outside the inventory suffix set.

## Stronger extracted-package validation

The release builder now retains its four metadata checks and subsequently
runs one full normal-Python frontier replay from the extracted archive.
The output receipt and logs are written to a separate temporary directory,
so the frozen normal/optimized publication receipts cannot be overwritten.
The builder requires actual PASS, the complete current command list,
all log hashes, and unchanged source inventory. It preserves the new logs
and a copy of the actual receipt in the package, relocating only log paths
and retaining the original report digest. These are recorded separately
under `standalone_full_replay_checks`; all four existing
`standalone_metadata_checks` remain intact.

Package checksums are rebuilt after adding the extracted replay artifacts.
The README now accurately distinguishes the fresh full frontier replay
from metadata checks and the protected baseline replays.

Only syntax/static review of this new builder path was performed at this
stage. The expensive extracted full replay is deliberately deferred to the
final release-builder invocation after all mathematical sources are frozen.

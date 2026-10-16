# Rank-eight prepublication audit

**Treat these AI-generated results and data with caution. They have not been independently verified by a human or formalized in Lean.**

The proof review found an unsupported decorated-phase cancellation in the proposed general exclusion of `R8_2_24`. That case is reopened. The proposed eight-slot repair is conditional research material, not an accepted proof. See [PROOF_REVIEW.md](PROOF_REVIEW.md) and the project’s dated errata for the precise scope.

The fresh full historical baseline replay passed under normal Python: all 973 source tensors, 832 negative certificate applications, 60 positive model records, and 81 then-open records. Imported signed proof trees, appendix transfers, and all counts and stage tallies also passed. This finite replay does not close the R24 categorical gap.

- [Full receipt](full_baseline_receipt.json) lists all 973 checked source IDs and criterion totals.
- [Run log](full_baseline.log) records the original checker’s completed loop.
- [External driver](run_full_baseline.py) imports the byte-identical frozen original checker and explicitly invokes its unchanged `main()`. It requires assertions, disables no checks, and writes only into the isolated audit copy and output directory.
- [Restoration receipt](baseline_restoration.json) and [final file overlay](baseline_final_overlay.json) bind the exact historical inputs.
- [Record coverage](record_coverage.json) partitions the 892 unchanged baseline decisions and 81 later transitions. Its unified totals are historical, before R24 was reopened.
- [Dependency review](R24_DEPENDENCY_REVIEW.md) checks whether another accepted decision uses the withdrawn R24 argument.
- [Correction-stage review](REVIEW_STAGE_CHECK.md) records independent normal/optimized metadata checks, six negative controls, and preservation of every other rank-eight record.
- [File hashes](files_sha256.json) bind this audit bundle.

Follow the [full replay instructions](../FULL_REPLAY.md) to reconstruct the isolated historical snapshot. The original full checkers must run with normal Python: their decision checks use assertions, so `python -O` is unsuitable for that step. A successful finite replay checks the specified calculations and source bindings; it does not independently prove all categorical premises or census exhaustiveness.

# Independent check of the R24 review stage

Date: 17 October 2026. This is an AI review, not human verification or Lean formalization.

**The correction stage passes the bounded independent checks below. It reopens only R8_2_24 and does not establish a new categorification result.** The mathematical reason is the original unsupported decorated-phase cancellation; the proposed paired-diagram replacement still has an unproved oriented categorical transport step.

The checked review source manifest has SHA-256 `c42ceb269f72760d53b374480dd97556ce8cb569774e2c360c3e16e1945c60d6`. The exact verifier and relevant review-file hashes are recorded in the normal and optimized receipts. Later changes to those files are outside this recorded run.

## What was checked

1. **Independent before/after comparison.** All 973 rank-eight source IDs are preserved. R8_2_24 alone changes; its ID, multiplicity, index, source tensor hash, and commutativity field are unchanged. The other 972 records are identical as JSON values. Rank-six and rank-seven ledgers and rank-eight model/catalog files remain byte-identical. The 35 accepted continuation decisions are exactly the frozen unified stage's 36 decisions with R8_2_24 removed, in the same order and with unchanged fields.
2. **Fresh normal and optimized metadata checks.** Both `python3` and `python3 -O` complete the unmodified review checker's metadata mode, including all bound-source identities and restoration of 26 byte-exact historical parent files into a temporary directory. Each produces the same totals: rank eight has 895 excluded, 77 unitarily realized, and one unresolved record. The exact open IDs are R6_4_155, R6_8_1660, and R8_2_24.
3. **Negative controls.** The independent driver injects in-memory bad JSON values, without changing any file. Reinstating the withdrawn exclusion, changing another rank-eight tensor identity, and adding R24 to the accepted continuation list are all rejected. Attempts to restore over or inside the source tree are rejected before writes. Combining metadata-only and historical modes is also rejected. These controls pass under both normal and optimized Python. The review verifier uses explicit exception checks rather than decision-critical assertions.
4. **Historical isolation, inspected in source.** Default and `--historical` modes copy into a new temporary directory, restore the fixed parent file inventory by byte identity, verify the reconstructed complete parent ledger, and invoke the original unified verifier in that separate directory. `--historical` adds the earlier update-chain replay; default replays only the frozen unified stage. The source tree is not a restoration target. These costly replay paths were not executed again during this bounded review; the separate earlier full-baseline and update-chain receipts supply their computational coverage.
5. **Wording and scope.** Both the current record and the all-case register distinguish the original unsupported phase cancellation from the still-conditional replacement. The checker states that historical computational PASS results do not reinstate the withdrawn categorical argument.

## Files and reproduction

- `review_stage_partition.json`: independent pre-correction/current comparison, including both source ledger byte hashes.
- `review_stage_normal.json` and `review_stage_optimized.json`: final metadata and negative-control receipts, with exact checked-file hashes.
- `verify_review_stage_independent.py`: bounded external check driver. It imports the unchanged review verifier, checks both execution modes, and writes only its output receipt.

Run from the repository root:

```sh
python3 evidence/prepublication_20261017/rank8/verify_review_stage_independent.py --repo . --output /tmp/review-stage-independent.json
python3 -O evidence/prepublication_20261017/rank8/verify_review_stage_independent.py --repo . --output /tmp/review-stage-independent-optimized.json
```

The independent driver never invokes a historical computational replay. Its optimized run is suitable for the new review checks because those checks use explicit exceptions. It does not change the separate requirement that the original full baseline checkers run with normal Python.

The dependency review in `R24_DEPENDENCY_REVIEW.md` found no other accepted decision that uses the withdrawn R24 exclusion or its six-slot phase lemma. These are bounded source and consistency checks, not a mechanically complete theorem dependency graph, a proof of all categorical premises, or a human assessment of the results.

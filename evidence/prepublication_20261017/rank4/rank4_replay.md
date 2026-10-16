# Rank-four complete replays — prepublication audit

Status: **PASS**, completed 2026-10-16 UTC. Both the original archived release and the exact current GitHub publication source were fully replayed, separately and without modifying their verification logic. Each checked all **889,530 inputs**, obtaining **15 realized, 889,515 excluded and zero unresolved**.

| Replay | Exit code | Fresh verifier time | Fresh exhaustive signed gate |
|---|---:|---:|---:|
| Original archived release | 0 | 1,022.235 s | 812.406 s |
| Current GitHub publication source | 0 | 777.339 s | 638.419 s |

The small difference between recorded verifier time and the final console timing includes receipt writing. These are replay timings under shared load, not controlled performance benchmarks.

## Recovery and integrity

Recovered the complete rank-four package from `archive_inputs/FusionFrontier.tar.xz` into `rank4_recovered/`. Extraction accepted only regular files/directories under `Rank4/Rank4_Dong_Palcoux_Through128/Rank4_Through128`, rejected absolute/traversing paths and links, and did not modify the archive. There are 147 recovered files (141,328,294 bytes).

The previously missing certificate stream is present and matches the expected identity exactly:

- Path: `certificates/classification.jsonl.gz`
- Size: **75,825,461 bytes**
- SHA256: **969a2a5a84b794a3da1d9cd3978f92324d631760f503f5d208011923a723920f**

Every entry in the recovered release's `SHA256SUMS` passed before any verification receipts were regenerated. The log is `rank4_release_hash_check.log`.

## Environment and commands

Python 3.12.14, SymPy 1.14.0, python-flint 0.8.0, and g++ 13.3.0. The missing pinned python-flint wheel was installed from the configured Python package registry. No verifier source was edited, no precompiled executable was trusted, and no discovery checkpoint was accepted as proof.

The full command is:

```sh
python verify.py --workers 4
```

The verifier regenerates the complete shared signed catalog, checks all its arithmetic filters, reconstructs every input tensor, audits fusion axioms and all six unit-fixing permutations, checks every certificate, and reruns required bounded signed/induction searches. Its log is `rank4_fresh_replay.log`.

The documented default command validates the supplied unsigned census but does not independently regenerate it. To close that gap, I also ran:

```sh
python count_rings.py --bound 128 --threads 2
```

This enumerator imports no census and has no timeout. Its log is `rank4_unsigned_recount.log`. It exited 0 after 215.402 seconds and generated **889,530 classes: 889,157 self-dual and 373 with one dual pair**. Every one of the **128 exact-multiplicity counts** matched the pinned census manifest. The comparison is recorded in `rank4_unsigned_recount_comparison.json`. The default verifier summary correctly still reports its own `independent_complete_enumeration_repeated: false`; the separately invoked fresh enumeration is documented by this additional receipt.

## Full replay results

- **889,530 distinct rank-four input rings at multiplicity at most 128 checked.**
- **15 realized, 889,515 excluded, zero unresolved.**
- **7,084 signed certificate records** and **801,047 required signed candidate tables** checked.
- **6,470,006 signed sign/permutation orbits** freshly regenerated; 6,439,426 d-number rejections, 373 cyclotomic rejections and 30,207 retained orbits matched the pinned shared catalog exactly. The fresh signed gate took 812.406 seconds. The receipt also preserves the original catalog generation time; that original time is not the fresh replay time.
- All 907,266 source records, including historical duplicates, were audited: 889,530 distinct rings; 17,736 duplicate records split into 7,812 literal repeats and 9,924 additional labellings. All tensor axioms, associativity, published tensor hashes and all six unit-fixing basis permutations were checked.
- All 16,905 non-d-number certificate tasks completed successfully.

Fresh standalone receipts are `rank4_fresh_summary.json`, `rank4_fresh_global_signed_catalog.json`, and `rank4_fresh_criterion_usage.json`. The complete console log is `rank4_fresh_replay.log`. The identified certificate hash is repeated in the fresh summary.

A post-replay comparison against all 145 entries in the release hash manifest confirmed that **all source and certificate hashes are unchanged**. Only expected regenerated verification receipts and the new unsigned census runtime record differ. Exact changed paths are recorded in `rank4_post_replay_integrity.json`. The recovered archive and repository were not modified.

## Completed regression checks

All eight further packaged verifier/regression entry points passed freshly:

- `test_verifier.py`: 24 Python/C++ small-ring comparisons, 24 naive signed-domain checks, and seven deliberately corrupted certificates rejected.
- `test_applications.py`: 24 basis-permutation checks and eight corruptions rejected.
- `test_census.py`: full brute-force cross-checks at multiplicities 1 and 2.
- `test_extension.py`: 402 FLINT/SymPy polynomial/d-number comparisons, 397 witness cross-checks, and 62 model-gauge parity checks, sampling through multiplicity 128.
- `test_signed_scaling.py`: 23 local Python/C++ signed comparisons, 23 global-orbit comparisons, 729 non-self-dual bounded boxes, 200 native/arbitrary-integer Casimir determinants, five degenerate boxes, and four corruptions rejected.
- `test_global_signed.py`: exhaustive 9,765,625 integer tensors at bound 2, 1,832 associative signed tensors and 48 sign/permutation orbits; parallel-set and independent reference comparisons passed.
- `test_global_signed_queries.py`: independent query tests passed.
- `verify_companion.py`: both packaged unbounded-family verifiers passed.

Exact commands, elapsed times, exit codes, and individual logs are recorded in `rank4_regression_results.json` and `rank4_test_*.log` / `rank4_verify_companion.log`.

## Current publication source: separate full replay

The local working snapshot did not contain all remote rank-four files. The authoritative GitHub inventory was therefore used: **all 59 rank-four blobs were materialized and validated against their exact Git blob SHAs**. The commitments are preserved in `rank4_current_source_blobs.json`. The pinned parameter stream and restored certificate were separately checked by SHA-256.

The publication source differs from the original archived release in nine program/data-manifest files. All deltas were inspected; the complete differences and SHA-256 identities are preserved in `rank4_current_source_deltas.diff` and `rank4_current_source_deltas.json`. The substantive criterion revision removes the named type-42 tensor recognizer, requires weak integrality, recomputes the uniform residual-involution induction certificate and checks that certificate. Its generator/dispatcher revisions agree with that check. The census revision removes the optional unsigned-enumeration entry point and delegates census completeness to the pinned census source. The separate fresh archived recount above closes that audit gap for the same pinned inputs. Report-generation changes concern criterion order, first-use reporting and explanatory text.

The **unmodified current `python verify.py --workers 4` exited 0** after 777.339 seconds. No cached historical or fresh-original signed-catalog result was substituted: this current run regenerated and checked all 6,470,006 signed orbits again. It checked every one of the 889,530 input records, all 16,905 non-d-number certificate tasks, all 7,084 signed records and 801,047 required signed tables, with the same 15/889,515/0 partition.

All seven regression/companion commands present in the current publication also passed freshly: `test_verifier.py`, `test_applications.py`, `test_extension.py`, `test_signed_scaling.py`, `test_global_signed.py`, `test_global_signed_queries.py`, and `verify_companion.py`. In particular, the revised residual-involution application was tested under all 24 basis permutations; the application suite rejected eight deliberately corrupted witnesses. These runs are recorded in `rank4_current_regression_results.json` and their individual logs.

Fresh current-source receipts are `rank4_current_fresh_summary.json`, `rank4_current_fresh_global_signed_catalog.json` and `rank4_current_fresh_criterion_usage.json`; the complete log is `rank4_current_replay.log`. A post-replay comparison against all 59 source inventory entries found only three expected generated verification-receipt changes. **All current source and input hashes remained unchanged** (`rank4_current_post_replay_integrity.json`). Subsequent public README and restoration-guide edits do not modify this audited verification code.

## Public certificate restoration

The exact original 75,825,461 gzip bytes are published as thirteen binary parts, with per-part hashes, total length, whole-file SHA-256 and recovery provenance. No decompression or recompression was used. The portable Python restoration helper was tested successfully on full restoration and idempotent reuse. It also rejected an altered part, a missing part, a modified whole-file commitment and a mismatching pre-existing destination; failed restorations left no partial output. These six checks and the restored SHA-256 are recorded in `rank4_restoration_tests.json`.

The small original unsigned recount program and C++ enumeration sources are preserved unchanged in `unsigned_recount_sources/`, with their source-hash manifest, license and notice. They reproduce the additional independent census audit without requiring the private original archive. See the public restoration and replay guide at `supplements/rank4/PUBLIC_REPLAY.md` in the repository.

## Interpretation

This successful replay validates the implemented necessary conditions and their exhaustive finite domains on the identified dataset. It does not turn the mathematical inputs into a Lean formalization, supply independent human verification, or prove the unrestricted fifteen-ring conjecture. This audit is AI-performed and should remain disclosed as such.

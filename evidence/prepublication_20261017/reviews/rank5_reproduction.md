# Rank-five prepublication reproducibility audit and repair

## Conclusion

A fresh complete replay passed for **all 40,999 pinned rank-five fusion rings through multiplicity 20**, in both ordinary Python and `python -O`. Each mode verified **17 unitary model matches** and **40,982 general exclusions**, with no residual. The two newly generated decision ledgers are byte-identical. Their SHA-256 is:

`12886636134e0500a403ae1b635f5b901612d64b203dad1e1fdf94b0da2c31f1`

Normal replay took **631.973 seconds**; optimized replay took **634.376 seconds** under shared audit load. These are fresh executions, not copies of the earlier PASS receipts.

The earlier complete release archive and its final ledger were not recovered. The historical ledger digest `9261917451d469ece9929a1756f505924cf84adf34e79a0d2e6f68fed43f55cf` is retained only as provenance. It is **not** the digest of the reconstructed ledger. The fresh proof replay, exact tensor coverage, per-band agreement, and explicit new ledger digest resolve the current reproducibility blocker without inventing byte identity for an unavailable file.

The scientific limitation remains: these are AI-produced arguments and AI inspections, not independent human verification or Lean formalization. Exact replay verifies the finite arithmetic and coverage encoded in the checkers; the mathematical implications still depend on the theorems and categorical arguments.

## Blocking defects found in the old public path

The compact `supplements/rank5/verify.py` still classified the two former multiplicity-18 residuals as general-unresolved, with complete bound 17. Its `software/unified.py` omitted dispatch for `inert_parity_spherical`. The compact supplement also omitted the complete tensor/certificate inputs. Its newer README and receipts described a complete 40,999-case release, but that final named release archive was unavailable during this audit.

These were reproducibility and presentation blockers. The reconstructed current replay resolves them in a new evidence directory. Historical modules, reports, and archives were not overwritten.

## Recovered sources and preservation checks

1. `Rank5_Unified_Frontier.zip`, SHA-256 `057aff6c4f910136a4486eeb65b0fa69020560d40d2ab9a6a1257de8a4cb54cb`. All **100** internal checksum entries pass.
2. `rank5_multiplicity20_verified.zip`, SHA-256 `2362d401cab2e827a26b9332f21a4b16d2b8f232e506966ca512048b26270618`. All **16** internal checksum entries pass.
3. The latter archive's compressed tensor table has exactly the already published pinned SHA-256 `4542c0871498337ef38ce3903407933289699a5ff06c85ad0f6c2bd57da823fb`. Its pinned census commit is `b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726`.
4. Every one of the **28,493** prefix tensor records is unchanged after reversing the bookkeeping rename `independent_index` to `local_index`.
5. All **28,474** original general-exclusion certificate objects are unchanged. Both original spherical witnesses are unchanged. Exactly two new composite certificates attach the published inert-prime criterion, reconstructed from each full tensor, to those original spherical witnesses.
6. Every one of the **25** delivered published software files matches its exact Git blob SHA. The current replay adds inert dispatch in the new orchestration; archived `unified.py` remains unchanged. `github_source_blobs.json`, `reconstruction.json`, and `discovery_unified.diff` record the source identities and the small discovery-workspace change.

The complete historical archive that remains unavailable is `Rank5_Complete_Through20_InertParity_2026-09-23.zip`, previously recorded with SHA-256 `6981c0ade02db714e38076ff30b3119712ce6b137ac376c2a8ae474a01bb9f49`.

## Fresh certificate reconstruction and replay

The multiplicity-19/20 reconstruction processed all **12,506** exact pinned tensors. The basic arithmetic phase excluded 12,438 and left 68 categorical survivors; the full engine certified all 68, with no residual. Discovery used the existing exact-checking engine, with the published inert criterion added to its dispatcher; none of the extension certificates uses that extra criterion. Numerical LP may propose rational discovery witnesses; replay validates them exactly and does not invoke numerical LP.

The extension allocation agrees exactly with the older published allocation:

| Criterion | Multiplicity 19 | Multiplicity 20 |
| --- | ---: | ---: |
| dnumber | 5,609 | 6,825 |
| signed_extension_positive | 25 | 33 |
| subring | 2 | 0 |
| cyclotomic | 1 | 1 |
| quadratic_parity_pseudo | 3 | 5 |
| cyclic_four_central | 0 | 1 |
| pseudo_gate | 0 | 1 |
| **Total** | **5,640** | **6,866** |

A separate fresh prefix run also passed all 28,493 cases, including the two inert composites, in 646.934 seconds. Its full criterion allocation agrees with the older complete prefix report. The final package's new checker subsequently replayed the complete prefix and extension again in both normal and optimized modes.

The fresh 40,999-row ledger has this total allocation:

| Decision / criterion | Count |
| --- | ---: |
| unitary_model | 17 |
| dnumber | 40,558 |
| signed_extension_positive | 340 |
| pseudo_gate | 30 |
| quadratic_parity_pseudo | 20 |
| subring | 14 |
| cyclotomic | 8 |
| quadratic_parity_spherical | 6 |
| cyclic_four_central | 4 |
| inert_parity_spherical | 2 |

## What the new checker establishes

`verify_current.py` checks the pinned compressed table hash, then rechecks fusion axioms for every source tensor, canonicalizes under every one of the 24 unit-fixing basis permutations, rejects duplicates, and verifies that the complete decision set equals the pinned set. Prefix records are checked by exact isomorphism and their local metadata; extension records are checked against the source tensors in source order. Every exclusion is bound to its full tensor fingerprint and dispatched to its exact verifier. Every positive case is matched to the regenerated explicit model registry.

The two formerly unresolved cases require both halves of the composite proof: the tensor-derived inert-prime certificate and the unchanged original spherical-character witness. Removing the spherical character data is rejected, as are corrupted inert-field data and missing residue character data. There are **six** added tampering tests, covering these three changes for both former residuals. The original coordinate-system, Gram-vector, low-join, positive-feasibility, mutation, and exact Farkas-ray controls also pass in both modes.

All 20 published multiplicity-band counts and statuses are compared with the newly checked decisions. The repository's existing rank-five metadata records realizations in `realized_other_or_unspecified`; the checker compares the sum of that column and `realized_unitary` to the 17 verified model matches. It does not silently rewrite publication categories.

An independent lower-rank AI auditor inspected the orchestration and found no coverage or dispatch gap. This is an independent AI inspection, not human verification. The inspector correctly noted that supplied input hashes establish file identity rather than independently proving provenance; provenance is separately supported by the recovered source archives, pinned-table identity, preservation checks, and published code blob hashes. The mathematical checks do not accept a certificate merely because its file hash matches.

## Ready-to-publish package

The delivery directory is:

`/workspace/scratch/b038cfaffb82/work/prepublic_audit/rank5_delivery/evidence/prepublication_20261017/rank5`

It contains exactly eight files: `README.md`, `SHA256SUMS`, `current_normal.json`, `current_optimized.json`, `package.json`, `rank5_current_replay.zip`, `reconstruction.json`, and `replay.py`.

The deterministic ZIP contains **50 files**, including the complete sources, tensors, certificates, new ledger, both full receipts, and provenance. ZIP size is **8,624,181 bytes**; its base64 representation is **11,498,908 bytes**, below the requested 16 MiB request ceiling. Its SHA-256 is:

`264fd1b7f1851cbce142ea248a19bc2d0196ba44f350b2f5852e1e77a647a92d`

Every proof-source and input hash was rechecked against both full replay receipts before packaging. The small accessible launcher checks the ZIP hash, all 50 extracted member hashes, and agreement with the live published rank-five scope before optionally running the exact core checker. Normal and optimized `--check-package` both pass; an optimized negative test rejects a one-byte-corrupted ZIP before extraction. A shallow-path override issue found during that negative test was corrected in the launcher, then all launcher tests were repeated successfully. No third expensive mathematical replay was necessary because the extracted proof sources and inputs are byte-identical to those used in the two completed runs.

The final external file inventory is `work/prepublic_audit/rank5_delivery_inventory.json`; the launcher smoke receipt is `work/prepublic_audit/rank5_package_smoke.json`.

## Integration requirements

- Copy the eight delivery files into the matching `evidence/prepublication_20261017/rank5` path in the repository. No large direct JSON upload is required.
- Link the new replay path from the current root/supplement documentation. Preserve older verifiers and receipts as historical artifacts with their original scope.
- Keep `data/classification_status.json`'s historical rank-five input digest as historical provenance; add fresh replay references separately. The new package clearly distinguishes that unavailable ledger from the reconstructed, freshly verified ledger.
- Retain the explicit AI-generated / not human-verified / not Lean-formalized caution. The package already includes it prominently.

No canonical repository, frozen evidence, external publication setting, or website was modified by this subtask.

# Verification of the delivered release

The final package contains 182 source-bound records: 155 exclusions, 27 unitary models and no unresolved cases.

All **25 accepted stages passed in ordinary Python** from the extracted portable layout (476.0 seconds). The ledger was regenerated and every input status and both tensor hashes stayed unchanged.

All 25 stages were also covered under optimized Python: 19 established stages in the first isolated package replay, followed by the complete 8-stage dependency closure for the new C4 argument. The overlap is source verification and ledger assembly. The final optimized ledger check uses the completed 155/27 classification. The earlier receipt preserves its historical two in-progress statuses; no input hash changed, and those two statuses are replaced only by the newly verified model and exclusion.

| Stage | Ordinary Python | Optimized Python |
|---|---:|---:|
| source | PASS | PASS |
| arithmetic | PASS | PASS |
| subring-indices | PASS | PASS |
| cyclotomic | PASS | PASS |
| noncomm-codegrees | PASS | PASS |
| cyclic | PASS | PASS |
| compression | PASS | PASS |
| baseline-spectra | PASS | PASS |
| comm-module | PASS | PASS |
| noncomm-module | PASS | PASS |
| inherited-solvability | PASS | PASS |
| signed-scalar-reduction | PASS | PASS |
| spherical-lattice | PASS | PASS |
| two-character | PASS | PASS |
| selected-models | PASS | PASS |
| independent-model-audit | PASS | PASS |
| model-179 | PASS | PASS |
| dimension-120 | PASS | PASS |
| model-104-primary | PASS | PASS |
| model-104-independent | PASS | PASS |
| c4-reduction | PASS | PASS |
| c4-cohomology | PASS | PASS |
| c4-torsor | PASS | PASS |
| c4-exclusion | PASS | PASS |
| ledger | PASS | PASS |

Detailed output is retained in `work/rank11/replay_logs/`, `work/rank11/replay_logs_base_optimized/`, and `work/rank11/replay_logs_optimized_final/`.

Supplementary exact primary/Schur and all-exponent Minkowski replays pass for both final dimension-32 inputs. These necessary-condition passes do not assign either classification status.

The 18-page report was compiled with resolved citations and references, checked for overfull text, and visually inspected page by page. The mathematical replay preceded publication; its receipts preserve that original research-stage context. This publication revision changes report disclosure and adds reader-facing tensor projections, without changing the 182 mathematical decisions or any proof/certificate implementation.

The SHA-256 manifest records every delivered file except itself. Replaying regenerates receipts and logs, so compare the manifest before replay if byte-for-byte snapshot verification is desired.

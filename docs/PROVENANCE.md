# Provenance and boundaries

The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,506 general exclusions, 15 models and 6 unresolved cases. Every recorded model admits a unitary realization. The remaining rings retain unresolved status for general complex categorification.

The rank-seven multiplicity-five continuation addresses all 5,805 supplied exact-multiplicity-five rings: 5,804 general exclusions, 1 realization and 0 unresolved cases. The classification of the supplied census is complete through multiplicity 5. The new realization R7_5_5678 is Rep(AGL(1,7)).

> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.

The [fusion-ring-census repository](https://github.com/sebastienpalcoux/fusion-ring-census)
owns the based-ring enumeration and tensors. The original classification import is pinned
to [`2a340871242879665fa7ba2b01fa15b8bdeaada3`](https://github.com/sebastienpalcoux/fusion-ring-census/tree/2a340871242879665fa7ba2b01fa15b8bdeaada3).
Rank-specific source manifests identify the exact census revision used by each
certificate. Classification decisions are separate from census completeness.

## Current scope

| Rank | Census range | General classification |
|---:|---|---|
| 2 | Symbolic, all multiplicities | Two realized rings, both at multiplicity one. |
| 3 | Export through 1,000 | Unrestricted five-ring theorem. |
| 4 | Unrestricted | Exactly 15 models; every categorification is spherical; multiplicity at most 6. |
| 5 | Through 20 | Complete: 17 models and 40,982 exclusions. |
| 6 | Through 9 | Complete through 3 and exact bands 1, 2, 3, 5, 6, 7, 9; two open cases. |
| 7 | Through 5 | Through multiplicity 5: 9,976 exclusions, 30 models and 0 unresolved; complete through 5. |
| 8 | Through 2 | Complete: 77 models and 896 exclusions. |

The [historical 38-case continuation](../docs/RESEARCH_STATUS.md) records **36 decisions among 38 cases**: 29 proposed general exclusions and 7 unitary constructions. Within that historical 38-case study, two questions remain open: `R6_4_155` and `R6_8_1660`. The combined residual program records 140 decisions (120 exclusions and 20 constructions), all subject to independent mathematical verification.

The [current document manifest](../data/current_document_revision.json) binds
the manuscript sources, PDFs and web copies. The
[classification status](../data/classification_status.json) binds the decision
ledgers and records every exact-multiplicity partition.

## Ledger identity

| Rank | Ledger SHA-256 | Records | Partition |
|---:|---|---:|---|
| 4 | `969a2a5a84b794a3da1d9cd3978f92324d631760f503f5d208011923a723920f` | 889,530 | 889,515 excluded; 15 realized |
| 5 | `12886636134e0500a403ae1b635f5b901612d64b203dad1e1fdf94b0da2c31f1` | 40,999 | 40,982 excluded; 17 realized |
| 6 | `abb36cb0e7f9196e0a231cb85a601c82a1c8fd398996f77a8961487a7ca692e5` | 25,421 | 25,362 excluded; 57 realized; 2 open |
| 7 | `577d5796f92966900def5aaa934f95a4508461967937c4c6d7f7aaab4826e279` | 10,006 | 9,976 excluded; 30 realized; 0 open |
| 8 | `521b9b9fb16a86c7c4ba491b8c2c0ebad05de1e41aafb5bc225d6342c9477e4e` | 4,500 | 4,402 excluded; 92 realized; 6 open |

Rank-six realizations comprise 56 unitary models and one spherical model whose
ring has no pseudo-unitary categorification. The rank-four certificate contains
one header and 889,530 decision records. Missing classification coverage is
recorded as `unassessed`, never inferred to be an exclusion.

The rank-five ledger is reconstructed; its [package manifest](../evidence/prepublication_20261017/rank5/package.json)
binds the exact public inputs. Its archive digest is `264fd1b7f1851cbce142ea248a19bc2d0196ba44f350b2f5852e1e77a647a92d`.
The separately retained digest `9261917451d469ece9929a1756f505924cf84adf34e79a0d2e6f68fed43f55cf`
identifies an unavailable source ledger and is not a claim to possess those bytes.

## Archive and source bindings

The rank-six source archive `Rank6_Categorification_M9_Frontier_2026-10-01.zip` has SHA-256
`6f57efc66646f75b5ca307b6cc6660d17972f1453910d92c109b6002ba313cdc` and 780 files.
Its source-bound certificates and replay receipts are identifiable independently
of the current manuscript manifest. The [current research download](https://sebastienpalcoux.github.io/grothendieck-ring-classification/downloads/review-update-2026-10-17.zip)
collects the integrated manuscripts and supporting evidence.

The rank-four compressed certificate is 75,825,461 bytes with SHA-256
`969a2a5a84b794a3da1d9cd3978f92324d631760f503f5d208011923a723920f`;
its [public parts manifest](../supplements/rank4/certificates/manifest.json)
is checked during restoration. The 610-file computational source manifest has
SHA-256 `aea53af376ee1622554e969a3d178b0c42124abd8da3eadc08d62cc5ee5cd851`.
Hashes identify sources and do not certify their mathematics.

## Tensor crosswalks

The [rank-five crosswalk](../data/rank5_crosswalk.json) compares all 28,493
inputs at multiplicities 1–18 under all 24 unit-fixing basis permutations.
The two sets of canonical representatives agree at every multiplicity.
Labels may differ, so certificate transport requires the recorded based-ring
isomorphism. At multiplicities 19–20 the extension verifies 12,506 tensors
in the pinned source order. Its [report](../supplements/rank5/verification/extension19_20_verification.json)
binds tensor source SHA-256 `4542c0871498337ef38ce3903407933289699a5ff06c85ad0f6c2bd57da823fb`.

The [rank-six crosswalk](../data/rank6_crosswalk.json) compares all 25,421 full
tensor lines through multiplicity nine and identical compressed-file hashes.
The import additionally checks all 120 unit-fixing basis permutations and
retains 16,612 established representatives and identifiers.

For the exact scope of full-certificate and continuation checks, see
[verification coverage](PREPUBLICATION_REVIEW.md) and [replay commands](VERIFY.md).
The [AnyonWiki packet](../evidence/anyonwiki/README.md) binds the associators
and tensor identifications used by the positive constructions.

The rank-seven M5 extension is pinned separately to census commit `4e81914a6772ccd5aa2a2b5fe1b6e2cd06e2d700`. Its 5,805 new exact-multiplicity-five tensors and agreement with the earlier 4,201 tensors passed independent computational checks; exhaustive enumeration completeness relies on the supplied producer completion record. The optimized enumeration itself was not independently rerun.

## Rank-eight multiplicity-three continuation

The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,506 general exclusions, 15 models and 6 unresolved cases. Every recorded model admits a unitary realization. The remaining rings retain unresolved status for general complex categorification.

The complete census is producer-reported, with independent tensor and isomorphism audits. The supplied optimized source matches both producer run receipts; full enumeration was not independently rerun. The normal and optimized mathematical replay receipts, individually investigated residuals and proof dependencies are in [`evidence/rank8_m3_20261021`](../evidence/rank8_m3_20261021). A candidate has neither a general exclusion nor a constructed associator; it is not an established exotic category. New arguments remain subject to independent human review.

```bash
python3 supplements/rank8/software/verify_m3_continuation.py --output frontier-validation/baseline_normal.json
python3 -O supplements/rank8/software/verify_m3_continuation.py --output frontier-validation/baseline_optimized.json
```

Metadata-only mode checks source identity and reconciliation with both full receipts, without repeating their finite mathematical checks.

## Further rank-eight frontier investigation

The historical frontier stage recorded 25 further general exclusions among the original 34 unresolved M3 cases. Subsequent construction and research stages leave 6 current questions. The original M3 ledger, proof inputs and full receipts are unchanged. The current ledger is `supplements/rank8/output/research_20261022/ledger.json`.

Canonical normal and optimized frontier replays each passed all 108 checks. These receipts cover the historical frontier stage. Fresh replay after extraction from the publication archive is deferred.

Replay the original M3 package using the isolated outputs above, preserving its frozen receipts, then replay the continuation separately:

```bash
python3 tools/verify_rank8_frontier.py
python3 -O tools/verify_rank8_frontier.py
```

The new receipts bind accepted decisions and exact computations. The source-bound per-ring research inventory is `evidence/rank8_research_20261022/per_ring_research_audit.json`. Construction-family exclusions and feasible necessary-condition witnesses have explicit scopes; neither establishes an exotic category.

## Generalized Haagerup construction and further restrictions

R8_3_721 is realized by the inherited 1+rho Q-system Morita dual of the C2 de-equivariantization of the known GH(C8) category. Its rank and coefficient bound are proved exactly; identification uses its unique dimension type in the supplied complete rank-eight multiplicity-at-most-three census. The earlier center-action analysis reduces R8_3_1154 to three necessary center patterns. These model and pattern results are preserved in evidence/rank8_next_20261021/; the later R8_3_65 general exclusion is recorded separately in evidence/rank8_research_20261022/.

The integrated rank-eight article includes the new construction and restrictions. Categorical arguments, targeted mathematical replay receipts and independent reconstructions are in `evidence/rank8_next_20261021/`. The original frontier ledger, audit and completed replay receipts remain unchanged.

The following commands validate the accepted overlay metadata; they do not repeat the targeted mathematical checks:

```bash
python3 tools/rank8_next.py --check
python3 -O tools/rank8_next.py --check
```

A separately reviewed Galois follow-up reduces the 36 retained R8_3_1154 pair histograms to 25 across the same three center patterns. Its proof and exact replay are in `evidence/rank8_postpublication_20261021/r1154_galois_review/`; the ring remains unresolved.

## 22 October rank-eight research

R8_3_65 and R8_3_1795 have general-complex exclusions from pointed-induction Fourier integrality. Six exact separating certificates cover all four pointed associator classes for R8_3_65; sixteen cover both pointed classes and every admissible second-indicator assignment for R8_3_1795. The verified Galois reductions remove the pseudo-unitarity hypotheses. Every hypothetical categorification of each of the 6 remaining rank-eight rings admits a spherical structure and is Galois conjugate to a pseudo-unitary category. None is categorically Morita equivalent to a braided fusion category. For R8_3_1768 the pointed C2 associator must be nontrivial, forcing its nonidentity invertible to act freely on the simple objects of every indecomposable module category. R8_3_982 has a complete necessary based-module analysis; its remaining module data do not establish coherent module categories. A separate dimension-spectrum restriction for R8_3_3472 covers one specified rank-two module action only. These restrictions leave 6 general categorification questions unresolved.

The proof and exact verifier inventory is `evidence/rank8_research_20261022/README.md`. The current research stage has its own accepted ledger and source manifest; its exact replay is:

```bash
python3 tools/verify_rank8_research_20261022.py
python3 -O tools/verify_rank8_research_20261022.py
```

Run `python3 tools/rank8_research_20261022.py --check` for metadata reconciliation only. The original M3 replay and 108-check frontier receipts retain their historical scope. They do not replace the new targeted mathematical checks.

# Provenance and boundaries

> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.

The [fusion-ring-census repository](https://github.com/sebastienpalcoux/fusion-ring-census)
owns the based-ring enumeration and tensors. The classification import is pinned
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
| 7 | Through 4 | Complete: 29 models and 4,172 exclusions. |
| 8 | Through 2 | Complete through 1; multiplicity 2 partial: 77 models, 895 exclusions, one open case in total. |

The [current research account](../docs/RESEARCH_STATUS.md) records **35 decisions among 38 cases**: 28 proposed general exclusions and 7 unitary constructions. Three general questions remain open: `R6_4_155`, `R6_8_1660` and `R8_2_24`. The combined residual program records 139 decisions (119 exclusions and 20 constructions), all subject to independent mathematical verification.

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
| 7 | `00edf884caa59384a1f7b9a91d7273539306443035db5144c02f9bda5bda3d2b` | 4,201 | 4,172 excluded; 29 realized; 0 open |
| 8 | `d77a3aa234d86db69c2cf47499d857ba991ca8d29f0e5cc8c3cd09a4eaff2d51` | 973 | 895 excluded; 77 realized; 1 open |

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

# Provenance and boundaries

This release combines two distinct kinds of input. The public
[fusion-ring-census](https://github.com/sebastienpalcoux/fusion-ring-census)
supplies **all based-ring counts and tensors**, pinned at commit
[`b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726`](https://github.com/sebastienpalcoux/fusion-ring-census/tree/b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726).
The attached research bundle `FusionFrontier.tar.xz` supplies rank-four
**categorification decisions** and rank-five decisions through multiplicity
18, SHA-256
`5ef85daaa2f582f7466de5d122335eaedfa683d2804703ef18bdf36f22c0cfd9`.
The filtered rank-four publication bundle
`Rank4_Revised_Publication_Bundle_2026-09-23.zip` has SHA-256
`6ddd84ff22e947095d9508529556121e94e1f4d33b2acca92ff8efcb4173e940`.
It contains paper sources and compact code/data; the full 75,825,461-byte
rank-four compressed certificate is in the original attachment, SHA-256
`969a2a5a84b794a3da1d9cd3978f92324d631760f503f5d208011923a723920f`.
The revised rank-five release adds complete exact-multiplicity 19–20
exclusion certificates against that same pinned census.
Its final bundle `Rank5_Revised_Final_LocalIndex_2026-09-23.zip` has SHA-256
`020a86f964db952545b5f284241c940fe2b7b4d2b0539ec178f6643cead50931`.
For multiplicities 1–18, internal archival indices are explicitly named
`local_index`; at 19–20, `repository_index` directly identifies the pinned
source census record within its exact-multiplicity band.
The updated rank-six source `Rank6_Categorification_M8(1).zip`, SHA-256
`6d8618e43cb0d16a78d9913e3ff6d6de615345b619d33f33e737f1dea99c280e`,
extends its ledger through multiplicity eight.
The authorless, citation-updated rank-six reading/source release
`Rank6_Categorification_M8_Revised_2026-09-23.zip` has SHA-256
`5981d4ee065f78cf3057eb3c289c9675480f5f59f8e7534e74c13155a99d6a63`;
its decision partition agrees with the prior M8 ledger.

| Rank | Census source | Census complete through | Classification ledger | Classification status |
|---:|---|---:|---|---|
| 2 | Symbolic `X²=1+nX` | All | Rank-two theorem | Per-band decisions exported through 1,000; two realized at multiplicity 1 |
| 3 | `results/census.json` | 1,000 | Five-ring unrestricted theorem | Per-band decisions exported through 1,000; four realized at multiplicity 1 and one at 2 |
| 4 | `results/rank4/tables.txt.gz` | 128 | `certificates/classification.jsonl.gz` | Complete through 128 |
| 5 | `results/rank5/tables.txt.gz` | 20 | Revised `data/decisions_all.json` | Complete bands 1–17 and 19–20; two general residuals at 18 |
| 6 | `results/rank6/tables.txt.gz` | 8 | New `data/decisions.json` | Complete through 2; 47 general residuals through 8 |

The original source manifest is `results/census.json`. Its count rows are
imported by `tools/generate_counts.py`, with exact bounds and cumulative sums
checked. The GitHub source repository, rather than a separate enumeration in
this classification repository, is authoritative for the census. The
classification ledger entries are aggregated by `tools/generate_classification.py`.
Rank-two rows use the normal form `X²=1+nX`: only `n=0,1` are realized over
ℂ. Rank-three realized counts come from the five-ring unrestricted
categorification theorem. The revised stand-alone proof of sphericality and
the ring-level necessity argument are in [the manuscript](../manuscripts/rank3.tex),
with its [arithmetic checker](../supplements/rank3/audit_rank3.py).

## Ledger integrity

| Rank | Compressed or JSON ledger SHA-256 | Records assigned a decision | Outcome totals |
|---:|---|---:|---|
| 4 | `969a2a5a84b794a3da1d9cd3978f92324d631760f503f5d208011923a723920f` | 889,530 | 889,515 excluded; 15 realized |
| 5 | `4ca1313570668d55b4d9203de4d5e613d381d32e7db7155bbacfff30ce8757b2` | 40,999 | 40,980 excluded; 17 realized; 2 generally unresolved |
| 6 | `1747b3e94815ccd90ca8bf7b798bd61e5c6f8537af633894e7ad25c062a32876` | 16,612 | 16,511 excluded; 53 unitary models; 1 spherical model with no pseudo-unitary categorification; 47 generally unresolved |

The rank-four list in the attachment contains a header record and 889,530
individual records. Each ledger partition matches its census total at each
exact multiplicity. A missing ledger above its scope appears as `unassessed`
in the status file, never as a zero exclusion or a mathematical obstruction.

## Tensor crosswalks

Count agreement does not itself identify the classified tensors with the live
census. Two exact comparisons record that relationship:

* Rank five: [`rank5_crosswalk.json`](../data/rank5_crosswalk.json) compares
  all 28,493 attached tensors at multiplicities 1–18 with the corresponding
  source-census tensors. For each tensor, it minimizes its flattened integer
  array over all 24 simultaneous permutations of the four nonunit basis
  elements. For every multiplicity the two sets of canonical representatives
  agree exactly. Source labels need not agree. The release's SHA-256
  fingerprints hash the **labeled** tensor and are not isomorphism invariant;
  certificates must be transported through the actual basis isomorphism or
  applied via the proved invariance of their criterion. For multiplicities 19
  and 20, the revised release verifies all 12,506 tensors in precisely the
  same per-multiplicity source order and validates every exclusion certificate:
  see [`extension19_20_verification.json`](../supplements/rank5/verification/extension19_20_verification.json),
  checked against source tables SHA-256
  `4542c0871498337ef38ce3903407933289699a5ff06c85ad0f6c2bd57da823fb`.
* Rank six: [`rank6_crosswalk.json`](../data/rank6_crosswalk.json) checks that
  the new attachment's 16,612 full tensor lines through multiplicity 8 are
  exactly the same lines in the same order as the live source census. Their
  compressed table files also have identical SHA-256 checksums.

The crosswalk scripts are [rank five](../tools/check_rank5_crosswalk.py) and
[rank six](../tools/check_rank6_crosswalk.py), with the additional rank-five
extension verifier under `supplements/rank5/software/`. They need the full
attached input files and corresponding source census tensors; their recorded
outputs are shipped here because raw tensor archives are maintained in their
source release and census repository.

## Reading the status columns

`excluded_general` records a general categorification obstruction proved by
the manuscript criteria and certified for the ring. `realized_unitary`
records a unitary model; `realized_other_or_unspecified` records realization
without a finer status encoded in the particular ledger (the rank-four and
rank-five manuscripts establish unitary models for their positive rings).
`realized_spherical_nonpseudounitary` is a distinct rank-six model class.
`unresolved_general` names rings for which the release does not decide
categorification over ℂ. `unassessed` names rings in a census band for which
the attached classification ledger has no entries. Each row partitions its
whole census count into these disjoint columns.

The datasets are exact computational outputs linked to mathematical arguments,
not proof assistant formalizations. Positive model existence invokes the
constructions cited in each manuscript; the crosswalk and per-ring checks do
not replace those categorical proofs.

# Provenance and boundaries

This release combines two distinct kinds of input. The public
[fusion-ring-census](https://github.com/sebastienpalcoux/fusion-ring-census)
supplies **all based-ring counts and tensors**, pinned at commit
[`b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726`](https://github.com/sebastienpalcoux/fusion-ring-census/tree/b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726).
The attached research bundle `FusionFrontier.tar.xz` supplies **categorification
decision ledgers and certificates**, SHA-256
`5ef85daaa2f582f7466de5d122335eaedfa683d2804703ef18bdf36f22c0cfd9`.

| Rank | Census source | Census complete through | Classification ledger | Classification status |
|---:|---|---:|---|---|
| 2 | Symbolic `X²=1+nX` | All | Mathematical manuscript | Complex characteristic treated in manuscript; rank-two counts recorded through 1,000 for display |
| 3 | `results/census.json` | 1,000 | Unrestricted manuscript | Per-band decisions are not exported here |
| 4 | `results/rank4/tables.txt.gz` | 128 | `certificates/classification.jsonl.gz` | Complete through 128 |
| 5 | `results/rank5/tables.txt.gz` | 20 | `data/decisions.json` | Complete through 17; two general residuals at 18; 19–20 unassessed |
| 6 | `results/rank6/tables.txt.gz` | 8 | `data/decisions.json` | Complete through 2; 29 residuals through 7; 8 unassessed |
| 7 | `results/rank7/tables.txt.gz` | 4 | None | Census only |
| 8 | `results/rank8/tables.txt.gz` | 2 | None | Census only |

The original source manifest is `results/census.json`. Its count rows are
imported by `tools/generate_counts.py`, with exact bounds and cumulative sums
checked. The GitHub source repository, rather than a separate enumeration in
this classification repository, is authoritative for the census. The
classification ledger entries are aggregated by `tools/generate_classification.py`.

## Ledger integrity

| Rank | Compressed or JSON ledger SHA-256 | Records assigned a decision | Outcome totals |
|---:|---|---:|---|
| 4 | `969a2a5a84b794a3da1d9cd3978f92324d631760f503f5d208011923a723920f` | 889,530 | 889,515 excluded; 15 realized |
| 5 | `9373cd1e58dbd5ad28cfafef4d1f31a4e95f8d2e0d9e7c9892ff05eb98fae928` | 28,493 | 28,474 excluded; 17 realized; 2 generally unresolved |
| 6 | `6a3ecde5a089287e9a306c539e89a9a2e91584ef9fc44f7aa8ef1c56b6d619fe` | 9,613 | 9,530 excluded; 53 unitary models; 1 spherical model with no pseudo-unitary categorification; 29 generally unresolved |

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
  applied via the proved invariance of their criterion.
* Rank six: [`rank6_crosswalk.json`](../data/rank6_crosswalk.json) checks that
  the attached 9,613 full tensor lines through multiplicity 7 are exactly the
  same lines in the same order as the live source census restricted to 7.

The crosswalk scripts are [rank five](../tools/check_rank5_crosswalk.py) and
[rank six](../tools/check_rank6_crosswalk.py). They need the full attached
input files and corresponding source census tensors; their recorded outputs
are shipped here because the raw tensor archives are maintained in their
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

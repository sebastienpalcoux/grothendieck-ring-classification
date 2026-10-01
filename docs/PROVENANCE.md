# Provenance and boundaries

This release combines two distinct kinds of input. The public
[fusion-ring-census](https://github.com/sebastienpalcoux/fusion-ring-census)
supplies **all based-ring counts and tensors**, pinned at commit
[`2a340871242879665fa7ba2b01fa15b8bdeaada3`](https://github.com/sebastienpalcoux/fusion-ring-census/tree/2a340871242879665fa7ba2b01fa15b8bdeaada3).
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
The revised rank-five release adds an inert-prime parity proof closing the two
former multiplicity-eighteen general cases and all certificates for 19–20.
Its complete bundle `Rank5_Complete_Through20_InertParity_2026-09-23.zip` has SHA-256
`6981c0ade02db714e38076ff30b3119712ce6b137ac376c2a8ae474a01bb9f49`.
For multiplicities 1–18, internal archival indices are explicitly named
`local_index`; at 19–20, `repository_index` directly identifies the pinned
source census record within its exact-multiplicity band.
The current rank-six release is `Rank6_Categorification_M9_Frontier_2026-10-01.zip` (SHA-256
`6f57efc66646f75b5ca307b6cc6660d17972f1453910d92c109b6002ba313cdc`). The [complete archive](https://grothendieck-ring-atlas.sebastien-palcoux.chatgpt.site/downloads/Rank6_Categorification_M9_Frontier_2026-10-01.zip) contains
780 files and the pinned census, proof certificates and exact constructors.
The partition is **25,362 excluded, 57 realized and 2 unresolved**.
There are 56 unitary models and one spherical model with no pseudo-unitary
categorification. All 8,809 rings of exact multiplicity nine are generally excluded.
The final eleven cases have portable proof bundles and exact completion replays
in normal and optimized Python. Only the two earlier frontier rings remain open.
The release identity binds the completion certificates, both replay reports,
every completion proof file, and the manuscript and verification-guide sources and PDFs.

The current ledger is `supplements/rank6/data/decisions.json`, SHA-256
`abb36cb0e7f9196e0a231cb85a601c82a1c8fd398996f77a8961487a7ca692e5`. The unchanged earlier negative proofs retain their
original exact verification evidence; this release does not claim a fresh
replay of every earlier proof. See [verification instructions](VERIFY.md).

| Unresolved ring | Necessary reduction |
|---|---|
| `R6_4_155` | The unique rank-26 semion-centralizer modular candidate is completely reconstructed, with nonnegative integral Verlinde coefficients (maximum 9), ten self-dual objects, and all stated finite Vafa and indicator checks passing. The rank-52 center would have twenty self-dual objects. No categorification is known. |
| `R6_8_1660` | One relative-center based ring and 1669 labelled center profiles remain, in branches 163, 753, 753. Every indecomposable module category has six simples; exact Morita and indicator reductions leave three possible dual based rings. No categorification is known. |

The verified rank-seven release through
multiplicity four has SHA-256 `3377a10544cfeb356b5fb3c391e73f61bb7794c664c504015e55c768e314abbe`.
Its previous negative-certificate replays are preserved; the three additional
AnyonWiki associators have independent exact pentagon, invertibility, unit
and rigidity checks. Multiplicity one is complete with thirteen realized rings.
The rank-eight release through multiplicity two has SHA-256
`700aa0188c6c4060c0cb239cf08a2007dca3dae8a15b77e8a00d52971839dd19` and adds five sourced models with
exact full-tensor matches. The remaining 75
and 111 cases respectively are
categorification questions. See the [positive update](../evidence/anyonwiki/README.md).

| Rank | Census source | Census complete through | Classification ledger | Classification status |
|---:|---|---:|---|---|
| 2 | Symbolic `X²=1+nX` | All | Rank-two theorem | Per-band decisions exported through 1,000; two realized at multiplicity 1 |
| 3 | `results/census.json` | 1,000 | Five-ring unrestricted theorem | Per-band decisions exported through 1,000; four realized at multiplicity 1 and one at 2 |
| 4 | `results/rank4/tables.txt.gz` | 128 | `certificates/classification.jsonl.gz` | Complete through 128 |
| 5 | `results/rank5/tables.txt.gz` | 20 | Revised `data/decisions_all.json` | Complete general classification through 20 |
| 6 | `results/rank6/tables.txt.gz` | 9 | `supplements/rank6/data/decisions.json` | Complete through 3; exact bands 1, 2, 3, 5, 6, 7, 9; 2 unresolved through 9 |
| 7 | `results/rank7/tables.txt.gz` | 4 | `supplements/rank7/output/rank7_ledger.json` | Complete at multiplicity one; higher bands partial; 75 unresolved |
| 8 | `results/rank8/tables.txt.gz` | 2 | `supplements/rank8/data/decisions.json` | Partial at both bands; 111 unresolved |

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
| 5 | `9261917451d469ece9929a1756f505924cf84adf34e79a0d2e6f68fed43f55cf` | 40,999 | 40,982 excluded; 17 realized; 0 unresolved |
| 6 | `abb36cb0e7f9196e0a231cb85a601c82a1c8fd398996f77a8961487a7ca692e5` | 25,421 | 25,362 excluded; 56 unitary; 1 spherical non-pseudo-unitary; 2 unresolved |
| 7 | `4c0ff9f0cd73f994a941ef77c278c1d08f0ddc0409ea5ba9f50356a6388bf472` | 4,201 | 4,107 excluded; 19 unitary models; 75 unresolved |
| 8 | `ea80964db4b32b1c6fbc79e0822ad4fa8041dddb81fd6dd2a09fd76713ef39d0` | 973 | 824 excluded; 38 unitary models; 111 unresolved |

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
* Rank six: [`rank6_crosswalk.json`](../data/rank6_crosswalk.json) compares
  all 25,421 full tensor lines through multiplicity 9 with the pinned
  source export, and verifies identical compressed-file checksums. The import
  separately checks every tensor against all 120 unit-fixing basis permutations
  and preserves all 16,612 earlier representatives and identifiers.

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

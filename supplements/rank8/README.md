# Rank-eight categorification, multiplicities one and two

This is the source and exact-certificate supplement for
[`paper/rank8.pdf`](paper/rank8.pdf). Its scope is the complete rank-eight
fusion-ring census **only through exact multiplicity two**. An unresolved ring
in this bundle is a fusion ring whose categorifiability remains undecided;
it is not counted as a Grothendieck ring.

| Exact multiplicity | Census fusion rings | Generally excluded | Explicit unitary models | Unresolved |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 96 | 41 | 30 | 25 |
| 2 | 877 | 783 | 8 | 86 |
| Total | 973 | 824 | 38 | 111 |

The source `data/rank8_tables.txt.gz` is a copy of the public
[Fusion Ring Census](https://github.com/sebastienpalcoux/fusion-ring-census),
commit `b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726`,
`results/rank8/tables.txt.gz`. The uncompressed source SHA-256 is
`97b86d2de8ca0352c5c6e14686cd1d43dbd52180dc53b2ff1ccf7a61788c9600`.
The census's terminated strata support completeness for 96 and 877 fusion
rings, respectively. We rely on its completeness instead of enumerating
those fusion rings again.

## Explore

- `data/decisions.json`: all 973 stable IDs `R8_m_j`, their exact source
  tensor SHA-256, and one of `excluded`, `unitarily_realized`, `unresolved`.
  An exclusion carries an independently checked certificate.
- `data/realized_models.json`: 38 source multiplication tensors and all
  matched unitary constructors with explicit model multiplication tensors,
  `basis_map_source_to_model` permutations and specific references. Five
  published group-theoretical constructors include direct `source_url` links.
- `data/exclusion_stages.csv`: the order used by the pipeline and its first
  certified applications. It lists zero-yield tests as well.
- `data/criterion_first_occurrence.json`: the smallest exact multiplicity in
  the present source at which each criterion first excludes a ring. Null means
  no application through multiplicity two. **No criterion-stabilization
  claim follows from these two rows.**
- `experimental_signed/signed_certified_campaign.json`: IDs, source-tensor
  hashes, proof hashes, and complete signed-branch counts for 75 exact
  sphericalization no-go witnesses. Proof files are in
  `experimental_signed/certificates/`.
- `data/rank7_certified_negative_subrings.json`: four transferred negative
  rank-seven tensors and their full exact proof trees. Only rings containing
  one of these four exact closed subrings inherit the exclusion.
- `experimental_signed/appendix_mle2_tensors.json`: transcribed published
  rank-eight full tensors, including direct constructions and two published
  induction-matrix exclusions. The independent checker verifies every
  full-tensor match; it does not repeat the paper's original Normaliz search.

The first unresolved multiplicity-one ring is `R8_1_3` and the first
multiplicity-two ring is `R8_2_24`. In particular, a final fusion-ring census
number alone is not a classification of Grothendieck rings at this bound.

## Recompute and check

Python 3 with SymPy and a C++17 compiler are required. From this folder run:

```sh
python3 software/analyze.py
python3 software/verify.py
```

The first command regenerates the ordered ledger and positive catalogue.
The second checks all 973 input tensors and statuses; every negative
certificate; every positive source-to-model map at all 512 tensor entries;
all 75 signed proof trees and four inherited rank-seven proof trees; and
six full archived-appendix tensor transfers. The final success line is
`VERIFIED [{"multiplicity":1,...},{"multiplicity":2,...}]` and
`verification/report.json` records the exact counts. Timeouts or incomplete
searches in discovery files never constitute negative certificates.

The paper is authorless and explicitly separates complete fusion-ring
input, proven Grothendieck-ring models, and the remaining categorification
frontier. Source and tool hashes are recorded in `manifest.json` after the
final verification.

The 2026-10-01 positive update is documented in [`../../evidence/anyonwiki/README.md`](../../evidence/anyonwiki/README.md). Run `python tools/verify_anyonwiki_import.py` from the repository root to replay the exact added witnesses and verify preservation of every previous exclusion. The earlier full-certificate report is retained separately; this update does not rerun its costly unchanged searches.

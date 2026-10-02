# Rank-eight categorification, multiplicities one and two

This is the source and exact-certificate supplement for
[`paper/rank8.pdf`](paper/rank8.pdf). Its scope is the complete rank-eight
fusion-ring census **only through exact multiplicity two**. An unresolved ring
in this bundle is a fusion ring whose categorifiability remains undecided;
it is not counted as a Grothendieck ring.

| Exact multiplicity | Census fusion rings | Generally excluded | Explicit unitary models | Unresolved |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 96 | 45 | 48 | 3 |
| 2 | 877 | 787 | 12 | 78 |
| Total | 973 | 832 | 60 | 81 |

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
- `data/realized_models.json`: 60 source multiplication tensors and all
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

The first unresolved multiplicity-one ring is `R8_1_6` and the first
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

The 2026-10-02 extension and subfactor update adds twenty-two unitary models and eight general exclusions. Run `python3 software/verify_oct2.py` for its finite independent replay. The constructors include generalized Haagerup and Asaeda-Haagerup categories, unitary graded extensions, group and TY equivariantizations, a twisted group-theoretical category, and a bosonic quotient. Three exclusions use Brauer-Picard groups of small pointed categories; two use the dimension-six Hopf classification. Three further exclusions exhaust the forced prime equivariantizations, using a module-rank divisibility obstruction in dimension 72. The full proofs are in the manuscript. All 943 unaffected ledger records and 38 earlier positive records are preserved exactly; the earlier report is `verification/pre_oct2_report.json`.

The central-square-root model R8_1_7 uses the two source-bound pseudo-PSU(2)_6 associator tables in `data/*.jl`. `software/verify_r8_1_7_zesting.py` checks every pentagon and central half-braiding equation over an exact cyclotomic field; it requires SymPy and is included in `verify_oct2.py`.

The further flip extensions, Vec(Q8) equivariantization, and TY(C9)/TY(C3 x C3) inversion equivariantizations have independent tensor constructors in `software/extension_models.py`. The nontrivial pseudo-PSU action is checked by `software/verify_pseudo_psu_swap.py`, included in the finite replay.

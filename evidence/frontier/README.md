# Current categorification frontier

**Six unresolved cases.** R8_3_1768 remains excluded over the complex numbers. This continuation excludes branches and construction routes; it adds no whole-ring exclusion or categorical model.

The proofs are integrated into the existing rank-six, rank-eight and rank-nine manuscripts and the [current frontier report](../../manuscripts/frontier/Fusion_Ring_Frontier.pdf). [Manuscripts](../../manuscripts/README.md) · [Classification status](../../docs/RESEARCH_STATUS.md).

| Case | Current conclusion and proof |
|---|---|
| R6_4_155 | The specified order-32 near-group route forces parent group C4 × C2³. Its existence is not proved. [Conditional parent theorem](replay/current/r155/CONTINUATION.md). |
| R6_8_1660 | A nonreal Morita invariant excludes real forms and braided representatives in the positive Morita class. The center is prime, restricting direct modular sources. [Proof](replay/current/pair/REPORT.md). |
| R8_3_928 | Three center patterns are excluded. The surviving rank-20 factor is exactly [Anyon Atlas B20-02148](https://anyonatlas.org/data/B20-02148), not an established category. [Proof](replay/current/r928/REPORT.md) · [exact comparison](replay/current/r928/atlas/atlas_match_receipt.json). |
| R8_3_941 | The center is prime and satisfies the same direct-source obstruction. The proposed Morita link with R1660 still requires a category and separable algebra. [Proof](replay/current/pair/REPORT.md). |
| R8_3_1154 | One branch of a hypothetical smallest algebra forces an explicit simple rank-seven Morita-dual ring. Neither the algebra nor a categorification is constructed. [Conditional construction](replay/current/r1154/CONDITIONAL_RANK7_ROUTE.md). |
| R9_2_137 | Nine exact certificates exclude the positive Tambara–Yamagami sign. A rational witness survives for the negative sign. [Proof and scope](replay/current/r137/NEW_RESULTS.md). |

A model requires a categorical construction and identification of the full fusion tensor. Modular data, necessary-condition witnesses and proposed algebras do not suffice. The Atlas comparison checks all 400 S entries, 20 twists and 8,000 fusion coefficients exactly. On 29 October 2026, the record was labeled *Not CS* and was not marked *Known Categorifiable*. Its proposed condensation does not supply the required algebra.

## Proof scope

Center arguments use the positive spherical representative supplied by the established general-complex existence reduction. Complete center domains and inherited indicator reductions remain explicit premises. No arbitrary original complex categorification is assumed unitary or positive.

The previous [general exclusion of R8_3_1768](replay/new/r1768/PALINDROMIC_EXCLUSION.md) uses pivotal conjugation parity and those reductions. Its six separation certificates and frozen inputs are retained. No classification count changes in this continuation.

## Exact replay

Run the current finite checks with ordinary Python 3.10 or later:

~~~sh
python3 evidence/frontier/replay/current/run_checks.py --include-native --receipt /tmp/fusion-frontier-current.json
~~~

All 28 checks passed, including the optional native spectrum check and exact Atlas comparison. The [receipt](current_run_receipt.json) records their scope. The [manifest](replay/current/manifest.json) binds the inputs and lists dependencies. The runner uses a temporary copy, preserves shipped evidence, and invokes no optimizer or associator search.

The earlier R1768 exclusion remains independently replayable:

~~~sh
python3 tools/restore_data.py
python3 evidence/frontier/replay/run_checks.py --output /tmp/fusion-frontier-exclusion.json
~~~

That runner checks the twelve frozen predecessor calculations. [Runtime and relocation instructions](replay/new/r1768/REPLAY_README.md).

## Data and provenance

- [Current rank-eight ledger](rank8_ledger.json): 4,404 exclusions, 93 unitary models, three unresolved.
- [Multiplicity-three ledger](rank8_m3_ledger.json): 3,508 exclusions, 16 unitary models, three unresolved.
- [Accepted transition](accepted.json): R8_3_1768 was excluded; this continuation changes no status.
- [Current six unresolved tensors](../../data/current_remaining_cases.py).
- [Current proof directory](replay/current/README.md); predecessor inputs are retained for reproducibility.

**AI-generated research; independent human verification remains pending.** Exact checks certify their stated computations and do not replace categorical hypotheses.



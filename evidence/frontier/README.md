# Current categorification frontier

**Six unresolved cases; R8_3_1768 is generally excluded. No new model is claimed.**

The current mathematics is integrated into the rank-six, rank-eight and rank-nine manuscripts. [Manuscripts](../../manuscripts/README.md) · [Current report](../../manuscripts/frontier/Fusion_Ring_Frontier.pdf) · [Public Atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/unresolved.html).

| Case | Current conclusion and proof |
|---|---|
| R6_4_155 | Unresolved. [Complete connected-algebra reduction and Morita based-ring rigidity](replay/new/r155/MORITA_RING_RIGIDITY.md). |
| R6_8_1660 | Unresolved. [Nonsplit fermion centralizer, multiplication-space reduction and conditional Morita partner](replay/new/r1660_941/REPORT.md). |
| R8_3_928 | Unresolved. [Forced necessary fusion matrices](replay/new/r928/SPECTRAL_FUSION_REDUCTION.md). |
| R8_3_941 | Unresolved. [Conditional Morita identities](replay/new/r1660_941/REPORT.md) and [whole-column Galois restriction](replay/new/r1660_941/R941_GALOIS_ADDENDUM.md). |
| R8_3_1154 | Unresolved. [Simple-center theorem](replay/new/r1154/SIMPLE_CENTER.md). |
| R8_3_1768 | **Excluded over the complex numbers.** [Pivotal conjugation parity and six exact separators](replay/new/r1768/PALINDROMIC_EXCLUSION.md). |
| R9_2_137 | Unresolved. [Whole-column Galois orbits and fourth-indicator bounds](replay/new/r137/REPORT.md). |

A model requires a categorical construction and exact identification of the full fusion tensor. Necessary matrices, rational witnesses and proposed algebras are not counted as models.

## Exclusion and proof scope

Pivotal conjugation preserves the symmetry sign of a nondegenerate self-duality. Consequently, an opposite-sign self-dual constituent must occur evenly in X tensor V tensor X*. R1768 violates that parity. The proof explicitly uses the previously established general-complex sphericalization/Galois existence reduction and the categorical completeness of the center domains. These premises are identified and source-bound; numerical checks do not substitute for them.

The independent two-sign route reconstructs the complete parity domain and replays six rational Farkas certificates over all permitted columns. The new categorical lemma received two independent agent reviews. Independent human verification remains pending.

## Exact replay

After restoring the repository datasets:

~~~sh
python3 tools/restore_data.py
python3 tools/verify_current_publication.py
python3 evidence/frontier/replay/run_checks.py --output /tmp/fusion-frontier-replay.json
~~~

The replay executes twelve finite checks in a temporary copy, preserving the frozen receipts. It invokes no optimizer, associator search or new long enumeration. See the [runtime and relocation instructions](replay/new/r1768/REPLAY_README.md). Ordinary Python is required for the combined runner because some short checks use assertions. The R1768 adapter and separate R137 auditor also pass optimized Python.

## Data and provenance

- [Current full rank-eight ledger](rank8_ledger.json): 4,404 exclusions, 93 unitary models, three unresolved.
- [Exact multiplicity-three ledger](rank8_m3_ledger.json): 3,508 exclusions, 16 unitary models, three unresolved.
- [Accepted transition and source bindings](accepted.json): exactly R8_3_1768 changes status; every source tensor and model is preserved.
- [Current six unresolved tensors](../../data/current_remaining_cases.py).
- [Separate audit of the R137 bounds and witnesses](replay/new/r155/AUDIT_R137_CONTINUATION.md).

The portable proof directory contains only current notes, exact checks and the frozen input files required for them. The frozen tensor snapshot deliberately includes previously decided cases; it is not the current unresolved list. Earlier categorical certificates retain their original immutable contexts and are not presented as competing current reports.


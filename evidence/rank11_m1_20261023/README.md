# Rank-eleven multiplicity-one categorification

Research result, 23 October 2026: **182 rings = 155 excluded + 27 unitarily realized + 0 unresolved**.

All exclusions concern arbitrary complex fusion categories. Each positive record supplies an actual unitary category with an exact match of every multiplication coefficient. This classifies the supplied based rings by existence of a categorification; it does not classify all associators on a realized ring.

## Read first

- `Rank11_Multiplicity1_Report_2026-10-23.pdf`: consolidated results and new proofs.
- `work/rank11/ledger.csv`: one row per physical input line.
- `work/rank11/ledger.json`: full tensor hashes, all accepted overlapping evidence, proof paths and replay commands.
- `work/rank11/criteria_audit/CRITERIA_AUDIT.md`: surveyed literature and accepted lower-rank criteria, with precise scope and applicability.
- `VERIFICATION.md`: the recorded release checks.

Identifiers `R11_1_i` are permanent physical line numbers in `repositories/fusion-ring-census/results/rank11/tables.txt.gz`. Every input is a rank-11 multiplicity-one fusion ring; exact refinement separates all 182 isomorphism classes. The uncompressed input SHA-256 is `3186c410888e0bc7f30c9e423e0184a15618246bc9f4d0ef503e708c4081eff8`.

## Replay

Python 3.10 or later is supported; this release was checked with Python 3.12.14, SymPy 1.14.0, NumPy 2.3.5 and NetworkX 3.6.1. Install the three Python packages listed in `requirements.txt`, preserve the extracted directory layout, and run from its root:

```sh
python work/rank11/replay_all.py
```

The default runs all 25 accepted stages twice, once ordinarily and once with Python optimization enabled. It reconstructs the ledger and requires the status and both source hashes of every input to stay unchanged. Every critical check uses explicit exceptions rather than removable assertions. A full single-mode replay takes approximately eight minutes on the audited machine, mainly for the exhaustive noncommutative module check.

```sh
python work/rank11/replay_all.py --mode normal
python work/rank11/replay_all.py --mode optimized
python work/rank11/replay_all.py --check-package
python work/rank11/replay_all.py --list
```

`--only STAGE` selects a stage together with its mathematical verification dependencies. For example `--only c4-exclusion` includes the independently reconstructed positive reference model, both cohomology replays, and the source/ledger checks. A failed command must be investigated; never replace it by a stored PASS field. Replay updates generated receipts and logs, so the delivered SHA-256 manifest describes the initial archive snapshot.

The compressed source tables are included. No network service, external category database, compiled discovery executable, numerical optimizer or old census is required for accepted classification replay. `work/rank11/packaging_dependencies.json` lists the minimal dependency files. The `repositories/` directory here contains only necessary data/proof snapshots, not a checkout or publication.

## Main additional arguments and constructions

- All admissible signed and spherical dimension branches are checked before invoking spherical or positive-center arguments. The dimension lattice treats the mixed dimension-40 branches directly. A uniform two-character reciprocity argument excludes inputs 3, 52, 142 and 149.
- A central dihedral and Brauer–Picard argument excludes inputs 40 and 82. A hypothetical de-equivariantization would simultaneously have ranks 16 and 20. The twisted pointed case is explicitly included.
- Actual coherent actions realize the spin-current pair 24/68, twisted cyclic pair 48/146, and quaternionic triality input 179. Bilinear zesting gives input 150 along with already recognized cases.
- An explicit nonsplit group of order 32, a complete eighth-root-valued cocycle, and a Klein-four subgroup realize input 104. The entire tensor is independently reconstructed from actual bimodules and balanced quotients, without using the primary character-convolution implementation.
- A general zero-restriction lemma for extension multiplication torsors then excludes input 153. All neutral Tambara–Yamagami forms are considered; all 128 normalized cocycles and all six relevant four-cycle conjugacies are checked. The proof uses the verified input-104 category as a positive reference, not failure of a model search.

These are project results derived using established categorical theorems. The report distinguishes a new application or refinement from an established theorem; it makes no claim of priority over the mathematical literature.

## Supplementary known-criterion checks

The final dimension-32 pair passes all primary and Schur criteria, and all instances of the recorded Minkowski inequality for every real exponent p ≥ 1. Exact independent replays are included separately because these passes do not assign a classification status:

```sh
python work/rank11/criteria_audit/verify_primary3_tensor_algebra.py
python work/rank11/integral/verify_unitary_couplings.py
```

The Titsworth–Hagge package was cross-referenced exactly: its rank-11 dimension-32 tensor is input 30. Only the factual provenance and crosswalk receipts are included; their third-party archive and category data are not redistributed. The complete strict pointed-action scan and its scope are recorded in `known_models/pointed16_attempts.json`.

## Publication and provenance

This is the portable proof package for the rank-eleven publication. Its mathematical replay receipts retain the preceding research-stage context. The current manuscript is `Rank11_Multiplicity1_Report_2026-10-23.pdf`; the repository canonical copy is `publications/rank11/paper/rank11.pdf`. Both contain the same proof text and the publication disclosure. The census remains owned by the separate census repository.

Preserve physical IDs and input hashes when integrating. The two public parts should continue to distinguish the full 182-ring fusion census from the 27 realized Grothendieck rings, with 155 exclusions and no unresolved cases. Carry the reviewed ordered-and-cleaned display policy forward; archival discovery notes are not public result rows. Do not interpret a modeled-ring count as a count of inequivalent fusion categories.

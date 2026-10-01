# Reproduce the data

## Fast, offline checks

From this repository root:

```bash
python3 tools/restore_data.py
python3 tools/validate_release.py
python3 tools/render_publication_docs.py --check
python3 tools/render_readme.py
git diff --exit-code README.md
```

These commands check every displayed cell, rank bound, exact-multiplicity
sequence, CSV/JSON agreement, and each classification partition. They do not
rerun the mathematical criteria or enumerate the fusion rings. Continuous
integration performs the same checks on every change.

`restore_data.py` reconstructs large source datasets and the complete rank-six
download archive from small
compressed parts stored in this repository. It needs only the Python standard
library, uses no network, and checks SHA-256 for every part and every restored
file. Run it once after cloning, before running the full rank-specific
verifiers. `python3 tools/restore_data.py --check` verifies reconstruction
without writing files. The complete downloadable research archive already
contains all 567 current release files. It is restored at
`site/dist/downloads/Rank6_Categorification_M9_Revised_2026-10-01_v1.zip`.

## Rebuild from the pinned census

Check out the source commit and use its manifest:

```bash
git clone https://github.com/sebastienpalcoux/fusion-ring-census.git
git -C fusion-ring-census checkout 2a340871242879665fa7ba2b01fa15b8bdeaada3
python3 tools/generate_counts.py fusion-ring-census/results/census.json
```

The exporter requires complete, verified whole-rank bands and verifies that
every count from 1 to the declared bound exists and sums to the published
cumulative total. Rank two follows its symbolic normal form, independent of
the repository enumeration.

## Rebuild classification partitions

Unpack the attached `FusionFrontier.tar.xz` and the updated
`Rank6_Categorification_M9_Revised_2026-10-01_v1.zip` and the revised rank-five release. The
rank-four ledger is the `Rank4/.../certificates/classification.jsonl.gz` file.
The revised rank-five `data/decisions_all.json` extends the attached archive's
28,493 decisions to all 40,999 census tensors through multiplicity 20,
including general proofs for both former multiplicity-18 residuals;
rank-six decisions use the current M9 ZIP. The command below rebuilds ranks
2–8; rank-seven and rank-eight decisions are imported from the included
frozen ledgers and audited with `tools/validate_release.py`. Their own full
certificate replays are described in `supplements/rank7/README.md` and
`supplements/rank8/README.md`.
Then run, substituting the actual extracted paths:

```bash
python3 tools/generate_classification.py \
  --bundle FusionFrontier.tar.xz \
  --rank6-bundle Rank6_Categorification_M9_Revised_2026-10-01_v1.zip \
  --census fusion-ring-census/results/census.json \
  --rank4 classification.jsonl.gz \
  --rank5 rank5-decisions_all.json \
  --rank6 rank6-decisions.json \
  --rank7 supplements/rank7/output/rank7_ledger.json \
  --rank8 supplements/rank8/data/decisions.json
```

The exporter records source checksums and verifies cardinalities against
every census band. The released rows have no unassessed bands. Rank five is
complete through multiplicity 20. Rank six is complete through multiplicity
three, with exact completed bands 1, 2, 3, 5, 6, 7 and 13 cases through
multiplicity 9 generally unresolved. Isolated completed bands do not
complete intervening unresolved bands.
Rank seven has 78 open cases through
multiplicity four, and rank eight has 116 through multiplicity two. Those
figures are stored as unresolved, never as exclusions or zero positive counts.

To refresh only rank six from the revised archive while preserving every
other rank's current rows and provenance, use:

```bash
python3 tools/generate_classification.py --refresh-rank6 \
  --rank6 supplements/rank6/data/decisions.json \
  --rank6-bundle site/dist/downloads/Rank6_Categorification_M9_Revised_2026-10-01_v1.zip
python3 tools/export_grothendieck_counts.py
python3 tools/render_readme.py
python3 tools/validate_release.py
```

The incremental exporter verifies all 25,421 distinct records and each pinned
census-band total before replacing rank-six rows. Its input hash and current
bundle are explicit in `data/classification_status.json`. Other ranks' rows
and provenance are preserved. `validate_release.py` compares all 9
rank-six bands with the authoritative ledger, checks the
25,351/57/13 excluded/realized/unresolved
partition, every completed band and the release summary. These export checks
are separate from mathematical certificate replay.

## Rank-six continuation evidence

From the complete mirrored release:

```bash
cd supplements/rank6
python check_manifest.py
python -O software/conformal_models.py --verify
python -O software/release_consistency.py
python -O software/replay_m9.py --jobs 2
python -O software/replay_m9_structure.py
python -O research/exclusions/R6_5_1204/verify_exclusion.py
python -O software/frontier_replay.py --check-receipts
python -O software/frontier_replay.py --list
```

The conformal-model command freshly reconstructs the three unitary models.
The frontier receipt audit checks hashes and completion predicates, not the
mathematics. To replay a necessary reduction, select one current ring, for
example `python -O software/frontier_replay.py --select R6_4_155`.
Each command has a 15-minute deadline. A timeout establishes no exclusion.

The multiplicity-nine replay checks the newly accepted certificates. A complete fresh replay of every accepted certificate is:

```bash
python -O verify.py --jobs 2 --out verification/current/recheck_O.jsonl
```

The authoritative decisions and all unresolved tensors are in `data/`.
The [frontier](../supplements/rank6/research/frontier/README.md) identifies the
current necessary reductions, and the model catalogue lists all realizations.

## Tensor crosswalks

The rank-five and rank-six source-tensor crosswalks can be rerun:

```bash
python3 tools/check_rank5_crosswalk.py census_independent.json \
  fusion-ring-census/results/rank5/tables.txt.gz \
  --report data/rank5_crosswalk.json
python3 tools/check_rank6_crosswalk.py rank6_tables.txt.gz \
  fusion-ring-census/results/rank6/tables.txt.gz \
  --report data/rank6_crosswalk.json
```

The rank-five check tests exact based-ring isomorphism classes under every
unit-fixing permutation of basis; the rank-six check tests identical labeled
tensor lines in identical order. Their recorded reports alone cannot verify
certificate proofs. For the individual obstruction certificates, positive
models and theoretical coverage arguments, use the `verify.py` programs and
verification guides in the attached rank-specific research releases and the
revised manuscripts.

The rank-seven bundle includes a full 4,201-record checker and a second pass
under `python -O`, both passed on the released bytes. The rank-eight bundle
includes a 973-record replay with 75 completed exhaustive signed trees,
independently replayed inherited rank-seven subring proofs, and exact positive
tensor comparisons. Some published upstream negative lemmas are used by
citation rather than rerunning external Normaliz computations; see the
rank-eight manuscript for the precise dependency.

The revised rank-five proof uses `software/inert_parity.py` for the
former multiplicity-18 residuals. The extension includes
`software/verify_extension.py` and its
`verification/extension19_20_verification.json` PASS record for 12,506
per-tensor general exclusions at exact multiplicities 19 and 20. Its
`repository_index` is the 1-based position in the corresponding pinned
`results/rank5/tables.txt.gz` multiplicity band; the earlier 28,493 decisions
are matched through the canonical crosswalk above.

## Release discipline

When the source census advances, record its new commit and compare every
affected rank/multiplicity band before changing `data/`. A newly enumerated
band must not be shown as classified until the criterion engine has addressed
it; unassessed bands can be withheld from the classification explorer. Do
not infer exclusions or count unresolved rings from census data alone. Do
not treat a search timeout as a negative categorification result.

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
contains all 780 current release files. It is restored at
`site/dist/downloads/Rank6_Categorification_M9_Frontier_2026-10-01.zip`.

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
`Rank6_Categorification_M9_Frontier_2026-10-01.zip` and the revised rank-five release. The
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
  --rank6-bundle Rank6_Categorification_M9_Frontier_2026-10-01.zip \
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
three, with exact completed bands 1, 2, 3, 5, 6, 7, 9 and 2 cases through
multiplicity 9 generally unresolved. Isolated completed bands do not
complete intervening unresolved bands.
Rank seven has 39 open cases through
multiplicity four, and rank eight has 44 through multiplicity two.
These are general categorification questions. Separate unitary-only obstructions
never change the general partition.

To refresh only rank six from the revised archive while preserving every
other rank's current rows and provenance, use:

```bash
python3 tools/generate_classification.py --refresh-rank6 \
  --rank6 supplements/rank6/data/decisions.json \
  --rank6-bundle site/dist/downloads/Rank6_Categorification_M9_Frontier_2026-10-01.zip
python3 tools/export_grothendieck_counts.py
python3 tools/render_readme.py
python3 tools/validate_release.py
```

The incremental exporter verifies all 25,421 distinct records and each pinned
census-band total before replacing rank-six rows. Its input hash and current
bundle are explicit in `data/classification_status.json`. Other ranks' rows
and provenance are preserved. `validate_release.py` compares all 9
rank-six bands with the authoritative ledger, checks the
25,362/57/2 excluded/realized/unresolved
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
python software/replay_m9_completion.py --output verification/m9/completion/replay_normal.json
python -O software/replay_m9_completion.py --output verification/m9/completion/replay_optimized.json
python -O research/exclusions/R6_5_1204/verify_exclusion.py
python -O software/frontier_replay.py --check-receipts
python -O software/frontier_replay.py --list
python research/frontier/new_research/replay.py
```

The conformal-model command freshly reconstructs the three unitary models.
The frontier receipt audit checks hashes and completion predicates, not the
mathematics. To replay a necessary reduction, select one current ring, for
example `python -O software/frontier_replay.py --select R6_4_155`.
The dated October 1 research replay checks the completed R6_4_155 modular-data candidate,
finite indicator tests, and the R6_8_1660 module/Morita and 1,669-profile reductions.
Its exact scope and receipts are in `research/frontier/new_research/`. The October 2
[addendum](../evidence/residual_20261002/rank6/research_addendum.pdf) reduces the
second frontier further to 1,136 profiles and proves a pivotal tensor-quotient
obstruction. It also excludes braided Morita representatives and nontrivial
finite-group extensions or equivariantizations in either Morita class. These are
necessary conditions; both categorification questions remain unresolved.
Exact probability couplings also prove every Lim Corollary 3.4 inequality on
both six-element fusion bases, for every real exponent p >= 1 and nonnegative
input vector. Replay the source-bound certificates with
`python evidence/rank6_laptop_20261002/all_p_minkowski/verify.py --tensors supplements/rank6/data/unresolved_tensors.json`
from the repository root.
Each command has a 15-minute deadline. A timeout establishes no exclusion.

The completion replay checks all eleven final multiplicity-nine exclusions
against the frozen tensors and portable proof bundles. Its normal and optimized
reports, input and proof manifests, and negative controls are recorded in
`verification/m9/completion/`. The release identity hashes these records and
every file in `research/exclusions/m9_completion/`. All 8,809 rings at exact
multiplicity nine are excluded; the two remaining open rings have lower multiplicity.

A complete fresh replay of every accepted certificate is:

```bash
python -O verify.py --jobs 2 --out verification/current/recheck_O.jsonl
```

The authoritative decisions and all unresolved tensors are in `data/`.
The [frontier](../supplements/rank6/research/frontier/README.md) identifies the
October 1 necessary reductions; the October 2 addendum and its portable
verifiers record subsequent progress. The model catalogue lists all realizations.

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

The upper-rank bundles retain the earlier full-certificate runs, including the
rank-seven normal and optimized replays and the rank-eight exhaustive signed
proofs. Subsequent finite updates have separate reports that check new models,
new theoretical obstructions and exact preservation of earlier unaffected
records. Published upstream lemmas remain explicit citation dependencies;
external Normaliz or Groebner calculations are not claimed to have been rerun.

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

## AnyonWiki positive update

Run `python tools/verify_anyonwiki_import.py` from the repository root. It checks
all 139 multiplicity-one tensor matches, the added model permutations, and three
published associators over exact cyclotomic fields. Its historical preservation
checks account explicitly for the separately certified October 2 changes.
Multiplicity one at rank seven is complete; rank eight currently has
3 generally open multiplicity-one cases.
See [the original evidence](../evidence/anyonwiki/README.md).

## October 2 residual update

The [43-decision residual stage](../evidence/upper_residual_20261002b/README.md) and its [14-decision continuation](../evidence/upper_residual_20261002c/README.md) resolve 57 further rings: 44 general exclusions and 13 unitary models. The continuation generally excludes `R7_2_160`, `R7_4_1417`, `R7_4_1420`, `R8_2_312`, `R8_2_315`, `R8_2_317`, `R8_2_53`, `R8_2_93`, `R8_2_191`, `R8_2_299`, `R8_2_158`, `R8_2_186`, `R8_2_579`, `R8_2_682`. Stage b retains its frozen proofs and replay; stage c restores the historical ledgers when checking that replay.
The [earlier residual stage](../evidence/residual_20261002/README.md)
retains its own proofs and reports. Pivotal, pseudo-unitary, unitary and braided
obstructions are distinguished from general nonexistence. Replay the latest
source-bound stage in both normal and optimized Python:

```bash
python3 tools/verify_upper_residual_20261002c.py
python3 -O tools/verify_upper_residual_20261002c.py
```

The verifier checks all latest source identities, model tensors and certificates,
as well as preservation of earlier decisions.
The historical constructor replays run automatically against isolated copies
of their original ledgers and model catalogues. Their original entry points
are retained for provenance; they must not be run directly against an expanded
current catalogue without restoring the corresponding historical snapshot.

To refresh the upper-rank status and publication indexes from their ledgers:

```bash
python3 tools/update_upper_rank_status.py
python3 tools/export_grothendieck_counts.py
python3 tools/render_readme.py
python3 tools/render_publication_docs.py
python3 tools/validate_release.py
python3 tools/render_publication_docs.py --check
```

The upper-rank exporter preserves every lower-rank status row and input identity.
Archive checksums must be refreshed only after the corresponding bundle is rebuilt.

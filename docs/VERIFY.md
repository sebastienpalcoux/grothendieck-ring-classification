# Reproduce the data

> **AI-generated research — independent verification pending.** The results, proofs, code and data have not yet been independently verified by human experts or formalized in Lean. Read the [prepublication review and dated corrections](PREPUBLICATION_REVIEW.md) alongside these materials.

## Complete prepublication replays

The [dated review](PREPUBLICATION_REVIEW.md) separates fresh base-certificate
checks from later transition checks. For complete public inputs and commands,
use the [rank-four guide](../supplements/rank4/PUBLIC_REPLAY.md), the
[rank-five current replay package](../evidence/prepublication_20261017/rank5/README.md)
and the [full upper-rank replay guide](../evidence/prepublication_20261017/FULL_REPLAY.md).
These replace private-attachment dependencies and stale entry-point guidance.

For rank four, run from the repository root (Python 3.10 or newer and a C++17
`g++` compiler are required):

```bash
python3 tools/restore_data.py
python3 supplements/rank4/restore_certificate.py
python3 -m pip install -r supplements/rank4/requirements.txt
cd supplements/rank4
python3 verify.py --workers 4
```

For rank five, return to the repository root and use the public package below.
Its [guide](../evidence/prepublication_20261017/rank5/README.md) lists the pinned
Python dependencies and C++17 compiler requirement.

```bash
python3 evidence/prepublication_20261017/rank5/replay.py --check-package
python3 evidence/prepublication_20261017/rank5/replay.py --jobs 2
python3 -O evidence/prepublication_20261017/rank5/replay.py --jobs 2
```

The rank-five replay reconstructs all 40,999 decisions and checks each
multiplicity band against the published partition. Its new ledger has its own
recorded digest; the unavailable historical ledger is not claimed to have been
recovered. Neither public replay requires the original private attachments.

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

## Historical full partition export

The original full-export workflow is retained here for provenance. It requires
the original `FusionFrontier.tar.xz` and revised rank-five release; that older
rank-five archive and its final `decisions_all.json` were not recovered in the
prepublication audit. This archive-dependent command is not a prerequisite for
the complete public replays above. The exporter's full-export mode still
requires `--bundle` to record the original archive identity.

For readers who retain those original inputs, unpack `FusionFrontier.tar.xz`,
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
Then run, substituting the actual extracted paths. Do not substitute the
reconstructed rank-five ledger while claiming the historical ledger's digest:

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
Rank seven has 0 open cases through
multiplicity four, and rank eight has 1 through multiplicity two.
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

**The new complete-replay orchestrator has not been executed end to end.**
Its read-only identity checks and rejection controls have been tested. No
all-Python full-replay pass is claimed. The [backend packet](../evidence/prepublication_20261017/rank6_backend/README.md)
records the actual combined audit: the original complete receipt stream,
strict Python replays of every failed complete certificate, separate original
post-loop checks, and aggregate coverage validation. The original process's
failed status remains preserved. Its loaded backend/version was not measured
at startup. The global python-flint installation changed from 0.8.0 to 0.9.0
during the run, so workers and later child processes may have loaded different
versions. The new wrapper records actual per-process observations explicitly.

For the complete two-backend route, use a fresh restored checkout with no
pre-existing native binaries beside the rank-six C++ sources. From its
repository root, install the pinned requirements in an isolated environment:

```bash
python3 tools/restore_data.py
python3 -m pip install -r supplements/rank6/requirements.txt
python3 evidence/prepublication_20261017/rank6_backend/replay_complete.py \
  --repo . --output-dir NEW_DIR --jobs 2
```

Replace `NEW_DIR` with a new directory outside `supplements/rank6`.
The wrapper uses normal Python throughout: unchanged full FLINT verification,
complete Python-backend retries of every failure, then the exact original
post-loop checks. It rejects incomplete coverage, unexpected failures, missing
retries and changed inputs. Its combined summary preserves the initial run's
actual outcome. See the [full replay guide](../evidence/prepublication_20261017/FULL_REPLAY.md#rank-six-combined-replay)
for environment details, native-cache requirements and verification limits.

The following historical component commands address individual continuation
checks. They do not replace the combined full replay:

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

For complete base-certificate coverage, use the normal-Python combined route
above. An optimized or component-only invocation is not a substitute for that
campaign, and no all-Python end-to-end result is asserted here.

The authoritative decisions and all unresolved tensors are in `data/`.
The [frontier](../supplements/rank6/research/frontier/README.md) identifies the
October 1 necessary reductions; the October 2 addendum and its portable
verifiers record subsequent progress. The model catalogue lists all realizations.

The unified October 16 revision adds the fermion Azumaya linking identity
and checks it against the rank-22 R6_4_155 witness. It also derives the forced
third indicator nu_3(T)=2 for R6_8_1660 from its two saturated modular summands.
An exact half-integral Verlinde coefficient rejects its historical rank-37 witness,
while leaving other profiles open. Both categorification questions remain unresolved. The current manuscript
sources and PDFs are bound by the [document revision](../evidence/unified_20261016/rank6/document_revision.json),
whose [research record](../evidence/unified_20261016/rank6/research_progress.json)
retains the hash-checked chain to earlier records. The frozen supplement,
archive identity and classification counts are unchanged.

`python tools/validate_release.py` checks the current document hashes, the research chain and the frozen release identities; it does not certify the new theoretical proofs.

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
0 generally open multiplicity-one cases.
See [the original evidence](../evidence/anyonwiki/README.md).

## October 2 residual update

The [17 October prepublication correction](../evidence/review_20261017/README.md) reopens **R8_2_24** because its categorical-to-linear bridge is unproved. The latest 38-case continuation retains **35 accepted decisions**: 28 proposed general exclusions and 7 unitary constructions. Three general questions remain open: R6_4_155, R6_8_1660 and R8_2_24. Together with earlier residual stages, 139 decisions remain accepted (119 exclusions and 20 constructions), subject to independent review. The [frozen 36-decision snapshot](../evidence/unified_20261016/README.md) and manuscripts remain available with dated errata and exact historical replay; their R8_2_24 exclusion is superseded.
The [earlier residual stage](../evidence/residual_20261002/README.md)
retains its own proofs and reports. Pivotal, pseudo-unitary, unitary and braided
obstructions are distinguished from general nonexistence. Replay the latest
source-bound stage in both normal and optimized Python:

```bash
python3 tools/verify_review_20261017.py --historical
python3 -O tools/verify_review_20261017.py --historical
```

The current review verifier checks the reopened record, source identities and
preservation of every other ledger entry. It restores the frozen parent files
before running the unchanged unified computational checks. The historical
R8_2_24 PASS does not reinstate the withdrawn categorical argument.
With `--historical`, the historical constructor replays run against isolated
copies of their original ledgers and model catalogues. Without that flag,
the dispatcher checks the corrected record and frozen unified stage. This does not replace a full
replay of every base-release certificate; see the
[prepublication review](PREPUBLICATION_REVIEW.md) for the separate full replays. Their original entry points
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

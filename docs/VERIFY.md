# Reproduce the data

## Fast, offline checks

From this repository root:

```bash
python3 tools/restore_data.py
python3 tools/validate_release.py
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
contains all 914 released files, including the unchanged 7-record
and 18-record continuation files and the new 12-record third continuation. Its repository mirror is restored at
`site/dist/downloads/Rank6_Categorification_M8_Revised_2026-09-29_v3.zip`.

## Rebuild from the pinned census

Check out the source commit and use its manifest:

```bash
git clone https://github.com/sebastienpalcoux/fusion-ring-census.git
git -C fusion-ring-census checkout b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726
python3 tools/generate_counts.py fusion-ring-census/results/census.json
```

The exporter requires complete, verified whole-rank bands and verifies that
every count from 1 to the declared bound exists and sums to the published
cumulative total. Rank two follows its symbolic normal form, independent of
the repository enumeration.

## Rebuild classification partitions

Unpack the attached `FusionFrontier.tar.xz` and the updated
`Rank6_Categorification_M8_Revised_2026-09-29_v3.zip` and the revised rank-five release. The
rank-four ledger is the `Rank4/.../certificates/classification.jsonl.gz` file.
The revised rank-five `data/decisions_all.json` extends the attached archive's
28,493 decisions to all 40,999 census tensors through multiplicity 20,
including general proofs for both former multiplicity-18 residuals;
rank-six decisions use the updated M8 ZIP. The command below rebuilds ranks
2–8; rank-seven and rank-eight decisions are imported from the included
frozen ledgers and audited with `tools/validate_release.py`. Their own full
certificate replays are described in `supplements/rank7/README.md` and
`supplements/rank8/README.md`.
Then run, substituting the actual extracted paths:

```bash
python3 tools/generate_classification.py \
  --bundle FusionFrontier.tar.xz \
  --rank6-bundle Rank6_Categorification_M8_Revised_2026-09-29_v3.zip \
  --census fusion-ring-census/results/census.json \
  --rank4 classification.jsonl.gz \
  --rank5 rank5-decisions_all.json \
  --rank6 rank6-decisions.json \
  --rank7 supplements/rank7/output/rank7_ledger.json \
  --rank8 supplements/rank8/data/decisions.json
```

The exporter records source checksums, checks cardinalities and agreement with
every census band. The released rows have no unassessed bands. Rank five is
complete through multiplicity 20; rank six is complete through multiplicity
three and separately at exact multiplicity seven, with 10 cases through
multiplicity eight remaining generally unresolved. The isolated seventh band
does not complete the intervening multiplicities four through six.
Rank seven has 78 open cases through
multiplicity four, and rank eight has 116 through multiplicity two. Those
figures are stored as unresolved, never as exclusions or zero positive counts.

To refresh only rank six from the revised archive while preserving every
other rank's current rows and provenance, use:

```bash
python3 tools/generate_classification.py --refresh-rank6 \
  --rank6 supplements/rank6/data/decisions.json \
  --rank6-bundle site/dist/downloads/Rank6_Categorification_M8_Revised_2026-09-29_v3.zip
python3 tools/export_grothendieck_counts.py
python3 tools/render_readme.py
python3 tools/validate_release.py
```

The incremental exporter verifies all 16,612 distinct records and each pinned
census-band total before replacing rank-six rows. Its current input hash and
bundle identity are explicit in `data/classification_status.json`; earlier
bundle entries remain as provenance. `validate_release.py` compares all eight
rank-six bands against the authoritative ledger, checks the 16,548/54/10
partition, completion through multiplicity three and at exact multiplicity
seven, and the current release summary. Export checks are separate from replaying mathematical certificates.

## Rank-six continuation evidence

The complete revised source is in `supplements/rank6/`. Restore repository
large files first, install that release's pinned requirements, then run from
its directory:

```bash
python check_manifest.py
python -O software/continuation_controls.py --jobs 3
python software/release_consistency.py
```

The three continuation files contain 7, 18 and 12 disjoint general exclusions.
The command above replays all 37 continuation certificates. The current
`verification/round3/release_replay.json` records the exact replay of the
**12 new proofs**, with assertions and numerical optimization disabled; the
unchanged first two continuations retain their previous exact replay evidence
in `verification/round2/release_replay.json`. To replay only the new proofs
and reconstruct the third-continuation ledger, use:

```bash
python -O software/round3_release.py --jobs 3
python software/release_consistency.py
```

The earlier multiplicity-three proof exhausts all module and central-induction
branches for `R6_3_215`; its 200 separating vectors do not assume that an
unknown center equals a known modular category. The third continuation
resolves `R6_4_6` by forced C4 associator twists and stabilizer rotation,
adds further general exclusions at multiplicities four through eight, and
closes both former multiplicity-seven residuals. The new criteria address the
frozen 22-residual input domain, with full-census scans and all 54 positive
models checked at the precise eligibility scopes recorded in the manuscript
and revision notes. The preceding continuation's 40-input domain remains
historical. A feasible necessary-system witness, an ineligible input or a
stopped search is not an exclusion or a categorification model.

The unchanged original 16,511-certificate campaign retains its earlier
verification. A fresh complete negative replay is available with
`python -O verify.py --jobs 2 --out verification/current/recheck_O.jsonl`;
it is not claimed to have been rerun for this publication update. Nor does
the current third-continuation replay claim a fresh replay of the unchanged
25 proofs from the first two continuations.
The current authoritative ledger and 10 residual tensors are under `data/`;
old research logs and preserved summaries are historical. The previous
`Rank6_Categorification_M8_Revised_2026-09-29_v2.zip` describes the 22-residual
snapshot; it is not the current verification input.

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

# Reproduce the data and mathematical checks

> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.

The [coverage report](PREPUBLICATION_REVIEW.md) states which computations were
actually executed. Program success checks its declared algebraic conditions;
it does not establish unproved categorical reductions or coherence.

## Restore and validate

From the repository root:

```bash
python3 tools/restore_data.py
python3 tools/validate_release.py
python3 tools/render_publication_docs.py --check
python3 tools/render_readme.py --check
```

Restoration needs only Python's standard library, works offline and checks
SHA-256 for every part and reconstructed file. `--check` verifies existing
restored files. The validation commands check publication identities, data
partitions and generated pages; they do not replay all mathematical proofs.

## Complete rank-four and rank-five checks

Rank four requires Python 3.10 or newer and a C++17 `g++` compiler:

```bash
python3 supplements/rank4/restore_certificate.py
python3 -m pip install -r supplements/rank4/requirements.txt
cd supplements/rank4
python3 verify.py --workers 4
```

Return to the repository root for the rank-five public replay. Its
[package guide](../evidence/prepublication_20261017/rank5/README.md) gives the
pinned Python dependencies and C++17 requirement.

```bash
python3 evidence/prepublication_20261017/rank5/replay.py --check-package
python3 evidence/prepublication_20261017/rank5/replay.py --jobs 2
python3 -O evidence/prepublication_20261017/rank5/replay.py --jobs 2
```

These are full checks of 889,530 rank-four classes and 40,999 rank-five classes.
The rank-five ledger is reconstructed and has its own source-bound digest.
Neither public route requires a private attachment.

## Complete rank-six route

**The portable complete-replay orchestrator has not been executed end to end.**
Its identity and rejection controls were tested. The executed campaign combines
25,355 passes in the initial full process with seven complete Python-backend
retries and two separate post-loop checks. The initial process's failed status
is preserved. This is not a single successful full run or an all-Python full
census replay. The [backend packet](../evidence/prepublication_20261017/rank6_backend/README.md)
records exact coverage, environment observations and matrix comparisons.

Use a fresh restored checkout, with no pre-existing native binaries beside
the rank-six C++ sources. In an isolated environment, from the repository root:

```bash
python3 -m pip install -r supplements/rank6/requirements.txt
python3 evidence/prepublication_20261017/rank6_backend/replay_complete.py \
  --repo . --output-dir NEW_DIR --jobs 2
```

`NEW_DIR` must be a new directory outside `supplements/rank6`. The wrapper runs
normal Python: complete FLINT verification, complete Python-backend retries
for every failure, then the original post-loop checks. It rejects incomplete
coverage, changed inputs and unexpected failures. Read the
[full replay instructions](../evidence/prepublication_20261017/FULL_REPLAY.md#rank-six-combined-replay)
for native-cache and environment details. The initial audited process did not
capture its loaded backend/version; the installed Flint version changed during
execution, so no uniform measured runtime is claimed.

## Upper-rank and continuation checks

```bash
python3 tools/verify_current_publication.py --historical
python3 -O tools/verify_current_publication.py --historical
```

The `--historical` option replays the complete dependency chain with each
source-bound program run in its isolated compatible input snapshot. Omitting
it does not execute all constructor dependencies. Both commands verify the
current accepted decision inventory and source identities. They do not replace
the original full base-certificate loops described in the
[full replay guide](../evidence/prepublication_20261017/FULL_REPLAY.md).
Use normal Python for any checker whose proof checks use `assert`.

The [current research account](../docs/RESEARCH_STATUS.md) records **35 decisions among 38 cases**: 28 proposed general exclusions and 7 unitary constructions. Three general questions remain open: `R6_4_155`, `R6_8_1660` and `R8_2_24`. The combined residual program records 139 decisions (119 exclusions and 20 constructions), all subject to independent mathematical verification.

A conditional local calculation for `R8_2_24` contributes no general exclusion.
Cited mathematical theorems remain explicit dependencies. External Normaliz
or Groebner calculations are not claimed to have been rerun.

## Individual rank-six checks

From `supplements/rank6`, the following check the named components:

```bash
python3 -O software/conformal_models.py --verify
python3 -O software/release_consistency.py
python3 -O software/replay_m9.py --jobs 2
python3 -O software/replay_m9_structure.py
python3 software/replay_m9_completion.py --output verification/m9/completion/replay_normal.json
python3 -O software/replay_m9_completion.py --output verification/m9/completion/replay_optimized.json
python3 -O research/exclusions/R6_5_1204/verify_exclusion.py
python3 -O software/frontier_replay.py --check-receipts
python3 -O software/frontier_replay.py --select R6_4_155
python3 research/frontier/new_research/replay.py
```

A receipt audit checks source hashes and completion predicates, not the
mathematics. The multiplicity-nine completion replay checks eleven standalone
certificates; all 8,809 exact-multiplicity-nine rings have general exclusions.
Necessary frontier reductions do not settle either rank-six open case.

From the repository root, replay the exact fermion and all-exponent
Minkowski certificates with:

```bash
python3 evidence/unified_20261016/rank6/verify_fermion_crossing.py --repo .
python3 evidence/rank6_laptop_20261002/all_p_minkowski/verify.py \
  --tensors supplements/rank6/data/unresolved_tensors.json
```

No timeout constitutes an exclusion. Component checks do not replace complete
base-certificate coverage.

## Census crosswalk and publication exports

```bash
git clone https://github.com/sebastienpalcoux/fusion-ring-census.git
git -C fusion-ring-census checkout 2a340871242879665fa7ba2b01fa15b8bdeaada3
python3 tools/generate_counts.py fusion-ring-census/results/census.json
```

The [tensor crosswalks](PROVENANCE.md#tensor-crosswalks) compare based-ring
isomorphism classes at rank five and exact labelled tensor lines at rank six.
Count agreement alone does not establish tensor identification.

Refresh publication indexes from the authoritative ledgers with:

```bash
python3 tools/update_upper_rank_status.py
python3 tools/export_grothendieck_counts.py
python3 tools/render_readme.py
python3 tools/render_publication_docs.py
python3 tools/validate_release.py
```

An enumerated band is not classified until every record has been addressed.
Preserve the distinction between census, partial classification and complete
classification. Do not enter incomplete-band lower bounds as exact OEIS terms.
Archive identities must be updated only after rebuilding the corresponding
bundle. Source and document integrity checks do not replace mathematical review.

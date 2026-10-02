# R6_8_1660: exact pairwise restriction lifting

This is a new, bounded laptop computation on the remaining **1,136 labelled center-restriction profiles** of R6_8_1660. It tests arbitrary low–high and high–high products using exact integers. Equal ungraded profiles are checked once: the input contains **628 distinct restriction multisets**, with all 1,136 original labels preserved.

The full scan has **not** been run in preparing this package. The category remains unresolved. A small pilot touched one profile and found 93 feasible pair tests and three budget-limited tests; it produced no obstruction.

## Run

Use Python 3.9 or newer. No external packages, internet access, or repository checkout are needed. Unzip the package, open a terminal in its directory, and run:

```sh
python verify_controls.py
python run_r1660.py --seconds 3600
```

On systems where Python is called `python3`, substitute that command. On Windows, `py -3` is another option. The main command allows one hour, at most 15 seconds and 200,000 search nodes per pair. It uses a single process and prints progress after each profile. The local checkpoint is updated after every completed pair test, so Ctrl+C safely stops the job.

To resume with the same limits, repeat the same command. To give unfinished pair tests larger limits:

```sh
python run_r1660.py --seconds 3600 --seconds-per-pair 60 --nodes-per-pair 2000000
```

Use `--retry-unknown` to retry budget-limited tests without raising their limits. A budget of zero means immediate stop or unknown; zero does **not** mean unlimited. A two-profile pilot is available with `--max-profiles 2`. One process should use a checkpoint at a time.

**Send back `r1660_results.json`.** Keep `r1660_checkpoint.sqlite3` on your laptop to resume. The JSON contains the original profile labels, progress, and complete bounded systems for candidate obstructions. It does not require sending the larger checkpoint. To refresh the JSON from the checkpoint without computing:

```sh
python run_r1660.py --summarize
```

Keep the input and runner unchanged between resumes. Their hashes are bound to the checkpoint. To use a changed runner, choose a new checkpoint with `--checkpoint new_checkpoint.sqlite3`. If Python reports a traceback, stop and send the full traceback, Python version, and exact command; do not delete the checkpoint. A hash-mismatch error should be reported, not bypassed.

## Interpret the result

| JSON status | Meaning |
|---|---|
| `profile_rejected` | Candidate obstruction: an exact bounded integer search was exhausted. The retained system must be independently replayed before using this as a mathematical exclusion. |
| `pairwise_pass` | Every selected pair admits an individual decomposition. This does not construct a center or fusion category. |
| `partial` | Some selected pairs remain unvisited or budget-limited. |
| `not_run` | No completed profile report has been recorded. Its completed pair tests may nevertheless be cached after an interruption. |

`labelled_profile_counts` counts all original labels, including aliases. The program never changes the categorification status. Excluding the original ring would require independently validating every remaining profile obstruction and the hypotheses and completeness of the preceding center-profile reduction. A partial run is useful and can be returned as it stands.

This job is ungraded: it does not choose one packet-charge witness and mistake its failure for an entire-profile obstruction. The new scope is low–high and high–high input pairs. Earlier calculations already imposed low–low product constraints and ordinary Frobenius–Schur indicator constraints; those are not advertised as new here. The future nonunit low-target generalized-indicator route is separate and is not implemented by this job.

## Contents and verification

- `run_r1660.py`: exact solver, source checks, resume, and result export.
- `r1660_profiles.json`: complete compact input and original source hashes.
- `PROOF.md`: necessity, multiplicity bounds, unit cases, and scope.
- `verify_controls.py` and `controls_receipt.json`: known categorical positive controls, integer-hole and budget controls, 120 independent small Cartesian-product checks, and a one-profile resume test.
- `verify_returned.py`: source-bound replay of candidate obstructions in a returned report.
- `INDEPENDENT_AUDIT.md` and `independent_audit.json`: independent mathematical and implementation audit, including 2,400 additional bounded-system comparisons.
- `generate_input.py`: optional reconstruction from the original repository evidence. It is not needed for the laptop run.
- `MANIFEST.json`: package file hashes.

The original source paths and SHA256 hashes are embedded in the input. To reconstruct it from the repository, use `python generate_input.py --repository /path/to/classification-repo --output regenerated.json`; its bytes should match `r1660_profiles.json`. All essential checks use explicit exceptions and remain active under `python -O`.

The search may be slow on difficult pairs. Limits affect only how much is attempted: an unfinished search is recorded as unknown, never as an obstruction. Completed feasible witnesses are checked directly. Only fully explored or exactly pruned states are cached as impossible within a search.

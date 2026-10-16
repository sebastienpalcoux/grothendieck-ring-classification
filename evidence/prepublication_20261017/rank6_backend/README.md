# Rank-six algebra backend correction — 17 October 2026

**Completed combined coverage audit: PASS.** All 25,362 unique exclusion IDs are
covered by 25,355 successful results in the original run and seven complete
successful selected replays. The original full run remains recorded as **failed
(exit 1)**. See [aggregate_summary.json](aggregate_summary.json) and the retained
[initial process result](initial_process_result.json).

The prepublication replay exposed a reproducibility defect in the frozen rank-six
checker: several saved exact Farkas rays depend on the Python rational backend's
ordering of algebraic-number strings. Selecting the Flint backend can reorder or
reverse otherwise identical equality rows. Merely installing the pinned
`python-flint==0.9.0` does not restore the saved row convention.

**Use `SYMPY_GROUND_TYPES=python` before importing SymPy for the affected selected
replays.** The proof sources and saved certificates are unchanged. The actual
audit uses an initial complete run followed by complete Python-backend replays of
every failed certificate. Initial failed receipts remain available; they are not
relabeled as a successful full run. A single complete all-Python run has not been
established by this audit.

The original full process did not record its loaded backend/version at startup.
The global python-flint installation changed from 0.8.0 to 0.9.0 while that run
was active. Existing workers may have retained 0.8.0 while later child processes
loaded 0.9.0; a uniform initial runtime version is not established. The Flint
backend is inferred from the default environment and reproduced failures, not
directly measured in that original process. The isolated diagnostics explicitly
recorded backend and version, including identical failures under Flint 0.9.0.

These results and data were generated with AI assistance. Treat them with caution:
they have not been independently verified by a human or formalized in Lean. Exact
software replay checks the implemented finite conditions; it does not by itself
verify their categorical hypotheses.

## Replay selected certificates

From the repository root, after installing
`supplements/rank6/requirements.txt` in an isolated environment:

```bash
python evidence/prepublication_20261017/rank6_backend/replay_selected.py \
  --repo . --ids R6_4_416 R6_4_427 R6_4_446 R6_5_638 R6_6_1035 R6_8_311 R6_8_3664 \
  --out /tmp/rank6-selected.jsonl
```

The adapter also accepts `--failed-receipts PATH.jsonl` in place of `--ids` and
selects every explicit `passed: false` record. Add `--list` to validate and list
the selection without executing certificates. Output paths must be new. Each
result uses the original `verify.py:worker`, including its prohibition of
floating-point optimization during checking. The adjacent summary records the
actual backend, source and input hashes, and the exact completed scope.

This adapter checks complete selected general exclusions. It does not claim to
replay the positive models, frontier reductions, other scoped structure
obstructions, or census import.

## Reproduce the complete audit workflow

The newly supplied `replay_complete.py` automates the procedure below. **This new
orchestrator has not itself been executed end to end.** Its identity, coverage,
and rejection controls were tested. The actual audit used the separately saved
original run and diagnostic replay commands.

On a fresh restored checkout, with the frozen dependencies and `g++` installed:

```bash
python evidence/prepublication_20261017/rank6_backend/replay_complete.py \
  --repo . --output-dir /tmp/rank6-fresh-campaign --jobs 2
```

The output directory must not exist. The wrapper refuses preexisting adjacent
native binaries, uses fresh temporary compiler directories, observes each child
process's actual backend/version, preserves all failures, and stops if any
certificate remains unchecked or fails its second replay. It does not modify
the frozen mathematical checker or certificate vectors.

The actual audit combines the initial unchanged full-verifier run with strict
Python-backend replays of every failed ID, then runs the two original post-loop
checks and validates complete coverage. A fresh run starts with:

```bash
cd supplements/rank6
SYMPY_GROUND_TYPES=flint python verify.py --jobs 2 --out verification/fresh-flint.jsonl
```

If this exits at the final negative-certificate failure gate, preserve the entire
receipt stream and failure log. First establish that the stream covers **all
25,362 exclusions** in ledger order; an early interruption is not a complete
replay. Then, from the repository root:

```bash
python evidence/prepublication_20261017/rank6_backend/replay_selected.py \
  --repo . --failed-receipts supplements/rank6/verification/fresh-flint.jsonl \
  --out /tmp/rank6-fresh-python.jsonl
```

Every initial failure needs a complete fresh PASS, with identical input and
source commitments. A second failure remains a failure and stops the workflow.
The two checks after the original failure gate—multiplicity-one counts and
positive-registry equality—must also be run. The separate `postloop/` receipt
records their exact original statements and both successful results.

`aggregate_replays.py` checks the archived audit's complete ordered coverage,
all source and certificate bindings, every fresh selected PASS, and the separate
post-loop checks. It explicitly preserves the original run's failed status.
The public full replay guide describes the orchestration entrypoint and its
validation limits. This two-backend workflow is the established audit procedure;
an all-Python full invocation remains a separate experiment.

To rerun the completed coverage audit without rerunning the expensive mathematics:

```bash
python evidence/prepublication_20261017/rank6_backend/aggregate_replays.py \
  --repo . \
  --initial evidence/prepublication_20261017/rank6_backend/initial_full_receipts.jsonl \
  --initial-log evidence/prepublication_20261017/rank6_backend/initial_full_replay.log \
  --replay-index evidence/prepublication_20261017/rank6_backend/selected_replays_index.json \
  --baseline evidence/prepublication_20261017/rank6_backend/baseline_identity.json \
  --postloop evidence/prepublication_20261017/rank6_backend/postloop/receipt.json \
  --out /tmp/rank6-coverage.json
```

The original proof sources and 299 explicitly bound source/input files remain
unchanged. Two freshly generated model outputs differ from their historical
copies only in run timings and the hash of a timing-bearing generated file;
`regenerated_model_outputs.json` records the exact comparison. Sibling diagnostic
packets are referenced through relative public repository paths in the selected
replay index, with their receipt and source hashes checked by the aggregate.

## Why the initial exact check failed

`software/spectral_induction.py:58,63` and
`software/augmented_spectrum.py:41,46` sort algebraic types using `key=str`.
SymPy's Python backend prints rational ANP coefficients as, for example,
`MPQ(1, 1)`, while Flint prints them as `1`. This changes lexicographic type
order. It can change both the order of balance equations and which member of a
Galois orbit is chosen first, reversing an equality's sign.

`software/modular_character_induction.py:42` appends those balance rows to the
exact system. A saved ray is a vector in that system's row coordinates. Its
inequalities need not survive a change of row coordinates unless the ray is
transported as well. This is different from an invalid mathematical separating
functional.

For the first previously failing R6_4_416 system, the Python and Flint matrices
have exactly the same augmented `[A | b]` rows and the same column order. An
explicit bijection moves 255 of 544 row positions. The unchanged saved ray has
23 negative dual coefficients under the Flint ordering. Transporting it by the
recorded row permutation restores the exact same dual vector as under Python:
minimum coefficient 0, with
`b^T y = -912954103961436122311806629120`.

The two Flint versions 0.8.0 and 0.9.0 produce identical matrices and rays in this
diagnostic. The diagnostic copy compiled native code freshly, so reuse of an old
native executable is not required to reproduce the defect.

The parallel R6_5_638 diagnosis also found row **orientation** changes (27 equality
rows reversed). Thus the general explanation is a signed row-coordinate change,
not only a permutation. The independently saved comparison receipts for the
other affected cases belong with the full prepublication audit.

For a signed permutation matrix `P`, if `A_python = P A_flint` and
`b_python = P b_flint`, then `y_flint = P^T y_python` preserves both
`A^T y` and `b^T y`. Reordering or negating an equality does not change its
solution set. The published correction instead restores the original backend
convention, so no certificate vector or mathematical condition is edited.

## Inspect this diagnostic

Run the small integer-only check:

```bash
python evidence/prepublication_20261017/rank6_backend/check_r416_coordinates.py
```

It verifies the committed captured-system hashes, exact row bijection, equality
of the two Flint systems, original failed inequalities, and the transported ray.
This is a diagnosis of **one system**, not a substitute for the complete R416
certificate replay. The complete selected replay receipts are separate.

The `python-full-r416` and `python-full-r427` receipts come from the diagnostic
harness's unchanged `stabilizer_rotation_higher.verify_general` entrypoint, which
is the ordinary dispatcher target for these certificate kinds. That harness
instruments `check_farkas` by calling the original exact checker twice, including
its original raising call; it does not remove a check. The later portable adapter
uses `verify.py:worker` directly and additionally disables SciPy optimizers.
`diagnostic_probe_used.py` preserves the historical instrumentation for inspection;
it expects the original scratch layout. Use `replay_selected.py` as the portable
public entrypoint for complete selected replays.

The six adapter controls cover a real inexpensive exclusion, an unknown ID, an
open record, duplicate IDs, output-overwrite refusal, and forcing the Python
backend despite an inherited Flint setting. Their receipts are in
`wrapper_controls/`.

This dated correction preserves the historical proofs, ledgers, and unsuccessful
replay evidence. It establishes a reproducible environment convention; it does
not establish backend-independent ordering for every future software version.

# Rank-eight local exclusion campaign

This package searches for **new exclusions** of R8_3_928, R8_3_941,
R8_3_1154 and R8_3_1768. It contains precomputed exact necessary systems,
case-specific search code, pinned mathematical inputs, exact proof checkers,
and resumable checkpoints. It does not change the public census.

## Ubuntu: install once, then search

Python 3.10 or newer is required. An internet connection is needed only to
install Python dependencies. If Ubuntu lacks venv support, first run:

```bash
sudo apt update
sudo apt install python3-venv unzip
```

Unzip the downloaded file and run:

```bash
unzip Rank8_Exclusion_Campaign.zip
cd Rank8_Exclusion_Campaign
bash install.sh
bash run.sh --hours 8
```

The eight hours are a wall-clock budget, not an estimate of the time needed
to exclude a case. The program alternates fairly between cases. It uses
one solver thread per worker and at most two workers by default, reducing
the worker count when available memory is low. To use one worker explicitly:

```bash
bash run.sh --hours 8 --jobs 1
```

You can continue later with exactly the same command. Checkpoints resume
automatically. Ctrl+C requests a controlled stop; allow up to twenty seconds
for workers to stop and the return archive to be written. A file named
`STOP` in this directory also requests a stop; delete it before resuming.
A task can overrun its numerical search budget while finishing an exact check.

At the end, send back **RANK8_RESULTS_TO_SEND.zip** from this directory.
It includes results, witnesses or proof attempts, rejection receipts,
checkpoints, logs, model identities and installed dependency versions.
If the terminal or laptop was stopped abruptly, recreate the archive with:

```bash
bash collect.sh
```

Please send the archive even if no case was excluded. Surviving necessary
data and partial exact searches guide the next theoretical step.

## What is different for each case

| Case | New search beyond the previously feasible relaxations |
| --- | --- |
| R8_3_928 | All four surviving branches; actual twist-root Galois orbits with integral per-root counts, coupled to full cyclic-rotation Fourier dimensions. |
| R8_3_941 | All fourteen surviving charge branches; the corresponding actual-orbit/rotation search with the charge and fermion constraints retained. |
| R8_3_1154 | All twenty-five pair branches; a bounded integral distinguished fusion matrix, packet commutation, forgetful intertwining, degree-five compressed moments, then exact degree-six moment and characteristic-polynomial checks. Rejected complete assignments receive replayable no-good cuts. |
| R8_3_1768 | Both remaining sector alternatives; the integer center system coupled to the surviving rational phase cone using full restriction vectors and exact character matching. Fixed variables are eliminated exactly; identical resulting systems are searched once with both branch records retained. |

For R928/R941 the precompiled models include rotation orders
3, 4, 6, 8, 9, 12 and 16. The actual twist conductor bound is derived as
1152; it is not an arbitrary numerical search cutoff. Some spectral trace
weights are rational continuous variables and remain continuous.

The package compiles all inherited branches before selecting distinct
search tasks. The exact counts and any identical projected models are in
`models/index.json`; build controls and smoke-test results are in
`build_validation.json`.

To concentrate on a single case:

```bash
bash run.sh --hours 8 --case R8_3_1154
```

Repeat `--case` to choose several cases. Keep this directory together;
do not copy checkpoint folders between different package versions.

## Reading the outcome

- `EXACT_NECESSARY_WITNESS`: the current necessary system has exact
  surviving data. This does not construct a fusion category.
- `CANDIDATE_REJECTED_EXACTLY`: a complete R1154 matrix assignment failed
  an exact mandatory invariant; only that assignment was removed.
- `INFEASIBLE_CERTIFIED`: exact checkers verified a contradiction for
  that necessary model. All branches and the mathematical prerequisites
  still require review before announcing a categorical exclusion.
- A timeout, unresolved node, numerical infeasibility report, or solver
  error is not an exclusion.

Numerical LP/MIP calculations discover candidates and proof directions.
Exact rational arithmetic checks accepted witnesses, bound cuts,
separations and integer branching. A separately implemented checker
replays exported equality-model certificates. R1154 assignment rejections
are replayed as a complete chain before a strengthened model contradiction
is accepted.

To replay stored exact outcomes locally:

```bash
.venv/bin/python verify_results.py
```

Runtime searches use the bundled files offline. The source inputs are
pinned to repository commit
`7f4aea6fb5e5a98aa9e5e5dc78a58bd46c1c92e1`.
`PACKAGE_MANIFEST.json` binds every shipped input; `tested_versions.txt`
records the tested Ubuntu build dependencies.
`METHODS.md`, `cases/R928_R941_THEORY.md`, and the bundled source proof
notes explain the reductions. Successful model closure remains
`EXCLUSION_CANDIDATE_REVIEW_REQUIRED` until that mathematical review.

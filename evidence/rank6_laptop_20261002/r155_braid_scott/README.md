# R155: a new exact laptop computation

This tests the still-open rank-six ring **R6_4_155**, through its retained
rank-26 modular candidate. It adds necessary compatibility conditions between
three braid operators, beyond the earlier 70 blocks of dimension at most four.
It does not attempt to solve the full center or associator equations.

Requirements: **Python 3.9 or later**, with no additional packages. Keep the extracted files together, including `su2_4_control.json` for the
self-test. The data are about 114 KB;
the script checks their SHA256 before using them. No internet or repository
clone is needed.

The separately included `audit_b3_su2_controls.py` records an independent
matrix check and uses SymPy. It is optional; neither the local search nor
`--self-test` needs SymPy.

## Run

First check the implementation:

```bash
python r155_braid_scott.py --self-test
```

Then allow two hours, with at most two minutes of search per block:

```bash
python r155_braid_scott.py --budget-seconds 7200 --seconds-per-block 120 --max-states 50000
```

On Windows, `py` can replace `python`. The default output is
`r155_braid_results.json` in the current directory. **Send back that complete
JSON file**, even if some blocks remain unknown.

Completed blocks are saved atomically after each block. You can interrupt
with Ctrl+C. To continue, allowing two further hours and ten minutes of search
per difficult block:

```bash
python r155_braid_scott.py --resume --budget-seconds 7200 --seconds-per-block 600 --max-states 200000
```

Blocks marked `PASS_NECESSARY` or `CANDIDATE_OBSTRUCTION` are retained.
Interrupted and `UNKNOWN` blocks restart with the new budgets. The
default memory bound is 50,000 proved-impossible search states per block;
the resume command raises it to 200,000. Setting either time limit to zero
removes that limit; a positive limit is recommended for an unattended run.
Blocks are processed in increasing dimension. The default range is 5 through 308,
so it avoids rerunning the old screen for dimensions one through four.

To reproduce one interesting block from scratch, use a fresh output name:

```bash
python r155_braid_scott.py --only 4,20 --seconds-per-block 300 --budget-seconds 360 --output one_block.json
```

Object labels in `--only a,b` are **zero-based labels of the rank-26 modular
candidate**, not labels of the original rank-six ring.

## What the output means

* `PASS_NECESSARY`: a partition of the three spectra passes the stated
  inequalities. The file contains a directly checkable partition witness.
  This constructs neither a braid representation nor a fusion category.
* `UNKNOWN`: a time or search-state budget was reached. It is not a negative
  result. Resuming retries that block with the newly supplied budgets.
* `CANDIDATE_OBSTRUCTION`: the finite partition search finished exhaustively
  and found no permitted partition. This is a potentially useful exact
  obstruction, to be independently replayed and audited before changing any
  classification claim. It has conditional scope: the retained positive-ribbon
  rank-26 modular candidate. The script does not itself upgrade it to a claim
  about every complex categorification of the original ring.
* `ERROR_REQUIRES_REVIEW`: an exact spectrum consistency check failed.
  The diagnostic is saved in the JSON. Send it back for review; the program
  does not automatically classify this as nonexistence.

The run can finish sooner than its budget. There is no prediction that it will
find an obstruction. A completed passing run would settle this additional
necessary test only.

## The new test

On `Hom(b,a^3)`, let `A=σ1`, `B=σ1σ2`, `D=σ1σ2σ1`. Then
`D=B A` and `D²=B³=(θ_b/θ_a³)I`. Their spectra are recovered exactly from
modular data and generalized Frobenius–Schur indicators using
Barter–Jones–Tucker, §4. The second-indicator data give the spectra of `A` and
`D`; an exact third-indicator calculation gives the spectrum of `B`.
All eigenvalues are represented as integer exponents modulo144.

A braid representation, even if not completely reducible, has a
Jordan–Hölder series. Its three spectra must partition into the spectra of
irreducible constituents. The program permits **every constituent dimension**
up to the block dimension. It imposes the exact determinant relation and
Scott inequalities on each proposed constituent, including the stronger
inequalities for triples of resonant eigenvalues. `PROOF.md` states them.
No restriction to constituents of dimension at most four is made.

This is stronger than a whole-block determinant check: the included negative
control has the correct determinant and central roots but no Scott partition.
The positive controls include exact modular-data reconstruction of actual
two- and three-dimensional `SU(2)_4` braid blocks, plus a reducible direct sum.

Only the controls and **one new six-dimensional R155 block** were run while
preparing this package. The full new search has deliberately been left for
your local run. The smoke-test result is in `smoke_result.json`.

Primary reference for braid spectra:
Barter, Jones and Tucker, *Eigenvalues of rotations and braids in spherical
fusion categories*, Corollary 4.1 and Proposition 4.2,
https://arxiv.org/pdf/1611.00071 .

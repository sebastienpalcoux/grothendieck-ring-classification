Exact terminal integer-system certificate

Run with Python 3:
    python3 check.py
Alternatively:
    python3 check.py /path/to/terminal_proof

Only Python standard-library modules are used. No optimizer, floating-point
arithmetic, SymPy, SciPy, NumPy, or pickle is required by the checker.
Run normally, without Python's -O flag, because verification uses assertions.

The checker starts from the 362-row base model and its initial integer bounds.
It replays 380 initial upper-bound cuts and 486 further integer cuts, then adds
266 indicator-field equations and replays 782 additional integer cuts.
Every rational bound is recomputed exactly using fractions.Fraction. Integer
rounding is checked at each step. The final 628-row, 572-variable system has a
rational covector y satisfying

    y*b - sum_j max((y*A)_j*l_j, (y*A)_j*u_j)
    = 2717541156573712541191977062303 / 359103652930042901916159999600 > 0.

This contradicts A*x=b for every x in the final interval box. Since all 1648
rounding cuts preserve integer solutions, the initial bounded integer problem
with the added field equations has no solution.

models.json contains sparse integer rows, right-hand sides, and starting
bounds, exported once from the frozen models. It also records the original
model file hashes. The mathematical derivation and coverage of this necessary
system are separate from this arithmetic certificate. This bundle verifies
the entire arithmetic contradiction without a numerical solver.

The JSON fields containing numerical discovery information are not used as
proof. The parent proof_manifest.json records repository-relative SHA-256 hashes.

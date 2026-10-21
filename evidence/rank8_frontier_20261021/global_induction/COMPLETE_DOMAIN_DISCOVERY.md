# Complete sparse cone discovery and exact replay

`complete_phase_one.py` changes the numerical discovery procedure for the
already defined central-induction cones. It introduces no additional
categorical necessary condition. In particular, it retains every column
of the requested complete frame or character-labeled atomic cone.

The matrix is accumulated in packed integer-index and floating-value
arrays, with positive row scaling. The full nonnegative feasibility
problem is proposed through the phase-I linear program

\[
  \min \mathbf 1^t(s_++s_-),\qquad
  Ax+s_+-s_-=b,\quad x,s_+,s_-\geq0.
\]

A numerical optimum near zero is only a proposal. The retained support
and values are converted to rational numbers, and the original exact
operator checks every equality and nonnegativity condition. A numerical
dual is likewise only a proposal: after undoing row scaling and changing
its sign, it is rationally reconstructed and cleared to an integer vector
\(y\). The original full-domain oracle must verify
\(y^t A\geq0\) and \(y^t b<0\). If a rounded ray fails, an exact rational
linear solve on proposed active constraints may supply another candidate;
the same whole-domain checks remain mandatory.

For high columns, the packed constructor contracts already scaled integer
modular coefficients with a common denominator for each phase-trace tuple.
Its output is compared with the original constructor on all small control
columns and a fixed spread of larger columns. This optimization only
affects numerical proposals: both saved primal and dual certificates are
replayed with the original exact cone implementation. A construction or
numerical-solver failure is recorded as incomplete, never as an exclusion.

One feasible indicator assignment yields an exact feasible relaxation.
This is survival of the stated necessary system and is neither a fusion
category construction nor a claim that every stronger system is feasible.
An exclusion requires an exact separator for every permitted indicator
assignment. Promotion from pseudo-unitary obstruction to general complex
scope additionally requires the existing complete spherical and oriented
signed-lift verification. Reusing a separator for another indicator is
allowed only after its new exact right-hand-side pairing is negative;
the matrix is unchanged and its complete column inequalities were already
checked.

`complete_queue.py` runs the finite domains serially and records discovery
outcomes and independent optimized replays. Its replaced incremental
searches remain marked as incomplete historical attempts in the coverage
inventory. Default `--verify` performs no numerical optimization and does
not require SciPy. The canonical research replay lists completed result
files explicitly; it does not rerun discovery.

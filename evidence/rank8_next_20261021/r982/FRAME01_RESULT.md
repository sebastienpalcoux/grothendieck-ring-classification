# R8_3_982: two complete distinguished frames excluded

This new evidence excludes distinguished low frames **0 and 1** of the
pseudo-unitary integer-center necessary system. It does not exclude the
fusion ring: frames 2 and 3 remain, and no reduction from arbitrary complex
categorifications to pseudo-unitary ones is asserted here.

The two frames give identical reduced necessary systems: 504 equalities,
361 nonnegative bounded integer variables, augmented rational rank 295.
Their source tensor SHA256 is
`f4a9fb77b3a78e9dcd8370ca9fa822ea331f1b71e3fad7990efdd386445fcd1c`.

The constraints are the previously defined full Gram, distinguished-S,
cubic Verlinde, individual Galois spectral multiplicities, FP fusion bounds, and source-unit norm/AMGM
constraints. No new restriction on phase weights is introduced.

## Exact finite-domain criterion

Let `Ax=b`, `x_j in D_j`, be necessary integer equalities with finite domains.
Every rational linear combination of the equalities remains necessary.
For any such row `a*x=c`, delete a proposed value `v in D_j` whenever

`c-a_j*v` does not belong to the finite sum of sets `sum_{k != j} a_k*D_k`.

Interval and gcd tests give exact inexpensive sufficient tests for deletion.
For rows with small finite sum range, integer bitset convolution computes
that sum set completely, including holes. Each deletion preserves every
integer solution. Rational row reduction and lattice reduction provide
additional short equivalent equations to which this criterion applies.

For this system, 624 verified steps delete 3,389 integer values and fix 61
variables. On the resulting interval hull, the saved integer covector gives

`y*b = 27,010,932 > 27,000,993 = sum_j max(c_j*min(D_j), c_j*max(D_j))`,

where `c_j = (y*A)_j`. The strict gap is **9,939**. Thus no integer solution
can remain. The numerical LP was used only to propose this covector; its
status is not part of the proof.

## Replay

Run from the repository root:

```sh
env SYMPY_GROUND_TYPES=flint OPENBLAS_NUM_THREADS=1 \
  python evidence/rank8_next_20261021/r982/verify_frame01.py --rebuild
```

The verifier reconstructs both necessary systems from the tensor, checks
that their coefficients, bounds, labels, shifts, and metadata equal the
saved data, verifies rational row-space inclusion, independently checks
every deleted value, and checks the strict integer separating inequality.
The deletion checker does not call the discovery propagator. Ordinary
replay without `--rebuild` checks the complete arithmetic certificate
against the cached exact systems.

Files `frame0_domains.json` and `frame0_branch.json` hold the deletion chain
and the final separator. `verified_frame01.json` records the latest replay.
The old frontier evidence is untouched.

## Additional investigations

`full_product.py` implements all 28 exact source-unit distinguished-product
identities and all 196 coordinate inequalities expressing the nonnegative
forgotten high remainder. Its first fixed-frame continuous relaxation has
no exact obstruction found so far. This observation is not a certified
feasible categorical model.

`lift_phase_cuts.py` lifts previously selected-pattern phase separators to
necessary inequalities on every high multiplicity pattern. For a covector
y nonnegative on the auxiliary phase columns, set
`c_o = min_t y*A_(o,t)`. Every compatible pattern satisfies
`sum_o c_o*m_o <= y*(b-fixed_low)` because its phase weights in orbit o sum
to m_o. Exact integer rounding gives weaker bounded coefficients while
preserving validity. This is being applied to the remaining frames 2 and 3;
its output must not be read as a ring exclusion until all relevant domains
and indicator branches are certified.

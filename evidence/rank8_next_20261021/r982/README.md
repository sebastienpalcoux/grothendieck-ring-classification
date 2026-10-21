# R8_3_982: new exact exclusions and a stronger joint survivor

**The ring remains unresolved.** This directory contains new necessary
center constraints and exact certificates. No categorical model, exclusion
of the entire ring, or general-to-pseudo-unitary reduction is asserted.
The frozen earlier evidence has not been changed.

## New exact results

1. **Distinguished frames 0 and 1 are excluded** under the pseudo-unitary
   hypothesis. Exact finite-domain propagation removes 3,389 values in 624
   justified steps; an exact bounded separator has strict gap 9,939. The two
   reduced systems are identical. An independent reviewer rebuilt both
   from the tensor and checked the complete deletion/separation proof.
2. **Frames 2 and 3 have identical mathematical systems and phase columns.**
   Lifting selected-pattern phase separators to all high multiplicity
   patterns excludes six of eight indicator branches. Every one of the
   1,348 allowed high duality orbits and all 34 phase types is included in
   the exact minimum calculation.
3. **A unique central lift G of source g is forced.** Tensoring by G gives 106
   additional mass equations. In the residual semion branches, both G and
   G composed with duality act without fixed simples; this yields 54 even
   mass conditions. These conditions exclude a seventh indicator branch,
   with strict separating gap 78,122.
4. **The last branch has an exact joint integer/phase survivor.** Its source
   indicators on indices 1 through 7 are `(0,0,0,0,+1,-1,-1)`. The necessary
   center pattern has rank 62 and 23 positive high duality orbits (31 distinct
   high restriction types). It has integral multiplicities and cubic fusion
   coefficients, both semion parity families, and exact rational phase
   weights in the complete remaining 117-orbit, 34-type domain. The joint
   equality system has 5,144 rows and 8,749 nonnegative variables, including
   variables used to express finite upper bounds.

The new rank 62 pattern also passes all 2,561 joint-Galois equalities, all 28
exact distinguished source-unit product identities, all 196 coordinate
remainder inequalities, and 28 separately certified nonnegative integer
high-remainder decompositions. Those decompositions respect the known
monodromy charges of the eight translated low objects and forbid G in a
product of two distinguished low objects.

All 406 entries of the fourth spectral product Gram are nonnegative
integers. After subtracting the eight known low outputs, both the remaining
product Gram and its Schur complement against the forgotten high
restriction Gram are positive semidefinite in exact arithmetic. All 6,435
mixed vacuum moments of the seven nonunit distinguished objects through
total degree 8 are also nonnegative integers.

These are necessary tests. The individual high-remainder decompositions
are not a mutually associative fusion table; rational phase variables are
not a choice of actual twists or an associator. The survivor is therefore
not a construction or a proof of categorifiability.

## Proofs and replay

`FRAME01_RESULT.md` proves the finite-domain criterion.
`SEMION_ACTION.md` proves the central-action and central-duality parity
criteria. The latter has an actual double-semion control with explicit
associator and braiding: all 256 pointed pentagons and 128 hexagons are
verified, along with nondegeneracy and both free involutions.

Run from the repository root:

```sh
env SYMPY_GROUND_TYPES=flint OPENBLAS_NUM_THREADS=1 \
  python evidence/rank8_next_20261021/r982/verify_frame 01.py --rebuild

env SYMPY_GROUND_TYPES=flint OPENBLAS_NUM_THREADS=1 \
  python evidence/rank8_next_20261021/r982/verify_followup.py --rebuild

python evidence/rank8_next_20261021/r982/semion_action_control.py

env SYMPY_GROUND_TYPES=flint OPENBLAS_NUM_THREADS=1 \
  python evidence/rank8_next_20261021/r982/joint_galois_check.py

python evidence/rank8_next_20261021/r982/forgetful_product_probe.py

env SYMPY_GROUND_TYPES=flint OPENBLAS_NUM_THREADS=1 \
  python evidence/rank8_next_20261021/r982/fourth_moment.py

env SYMPY_GROUND_TYPES=flint OPENBLAS_NUM_THREADS=1 \
  python evidence/rank8_next_20261021/r982/mixed_moments.py
```

The two source rebuilds call no numerical solver. They reconstruct the
necessary systems from the tensor, replay all domain deletions and strict
separators, check the full phase minima and indicator coverage, independently
reconstruct the central action and entire joint phase domain, and verify
the exact integer/phase witness. `verified_frame 01.json` and
`verified_followup.json` record successful full rebuilds.

Discovery scripts that call LP or MILP accept no numerical infeasibility
status as a proof. Only checked integer vectors, rational primal vectors,
finite-domain deletion proofs, or strict exact dual inequalities are
reported as mathematical results. Older intermediate proposals in this
directory are superseded by `joint_integer_result.json`.

## Remaining problem

A categorical construction, a full obstruction, or a completion of the
unknown center fusion data and associativity constraints remains open.
The computations narrow the pseudo-unitary problem to one common semion
branch of frames 2 and 3 and provide a joint necessary witness with which to
test further theoretical criteria.

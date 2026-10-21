# Final R982 arithmetic and phase screen

All statements here concern necessary pseudo-unitary center data. The source
fusion ring is **not excluded**, and no categorification has been constructed.

The complete distinguished-S low domain has four labeled frames. For each,
`r982.py` reconstructs the complete Gram-bounded high domain, integer
Gram/S/cubic equations, coordinatewise Galois balance, exact FP bounds and
finite box propagation. Exact modular and Hermite replays show signed
integer-lattice membership for all four. Frames 2 and 3 have saved exact
nonnegative integer witnesses. Frames 0 and 1 have numerical MILP
infeasibility proposals, which are explicitly not accepted as proofs.

`r982_joint_probe.py` verifies all 2,561 joint-Galois equations on each saved
integer witness. `r982_unit_pair_probe.py` verifies all 28 exact distinguished
source-unit product identities. Each witness has 25 positive high duality
orbits and proposed center rank 56.

`r982_phases.py` fixes those integer low and high multiplicities in the full
height-4 rotation/STS cone. Every omitted high fiber has multiplicity zero;
all trace types of each positive fiber and all rotation variables remain.
Each specialized system has 366 rows and 885 columns. Exact separators cover
all eight indicator choices for both patterns. Frame 3 has the identical
specialized column operator as frame 2, so its saved rays were transferred
and checked against its own exact right-hand sides and every column. The
interrupted redundant numerical reconstruction is retained separately as
`R8_3_982_frame3_phases_h4_initial.json`; it is not the final proof receipt.

For frames 0 and 1, `r982_remaining_linear.py` appends source-unit norm and
AM–GM equations and finite integer slacks. Its continuous search found no
exact separator. `r982_rational.py` replaces the numerical feasibility status
with exact rational primals: all original equations and all propagated bounds
are checked. The reduced systems have 504 rows and 361 variables. These
rational primals are weaker than nonnegative integer centers.

Every named script defaults to read-only exact replay. Optional numerical
discovery requires `--write`; default replay does not require SciPy. The
four-frame system and source-unit controls are covered by the independently
reviewed shared integer theorem. The final campaign ledger binds all source
tensors, receipts and canonical replay commands.

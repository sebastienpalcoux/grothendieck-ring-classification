# Fourth continuation: higher multiplicities

The new uniform necessary conditions project a center object onto a known
fusion subcategory, preserving the half-braiding and twist. This couples
restriction columns to twist support and to exact twist-resolved dimension
masses. See `papers/chapters/round4_higher.tex` and the shared projection lemma.

R6_6_49 and R6_6_1035 are now excluded with unrestricted categorical scope.
These two exclusions complete exact multiplicity six. R6_5_1204 remains
unresolved; its strongest tested necessary system survives.

| Input | Complete proof | Exact coverage | Normal / `-O` replay |
| --- | --- | --- | --- |
| R6_6_49 | `R6_6_49_general.json` | 353 low frames; one remaining frame, four character assignments, three pointed associator classes, two indicator choices; 24 rays | 255.98s / 348.96s; both passed |
| R6_6_1035 | `R6_6_1035_general.json` | 12 low frames; two remaining frame/character assignments, two indicator choices; four rays; 448 signed tables in 14 sign orbits | 367.40s / 372.93s; both passed |

Both replay scripts disable numerical optimizers before importing the proof
checker. They reconstruct the complete necessary equations and check exact
integer separating rays. The general reduction for R6_6_49 is the established
two-FP-value criterion; R6_6_1035 uses exhaustive signed reduction. Complete
receipts are `R6_6_49_replay*.json` and `R6_6_1035_replay*.json`. Reproduce with
`python research/round4/higher/replay_c3.py` and `replay_e6.py`, and repeat each
with `python -O`. The complete certificate digests are recorded in the
receipts and `summary.json`.

`round4_higher_mass.py` implements a small exact half-E6 projection system;
`round4_higher_real.py` adds real relative twist traces, full-character ST
relations, and the unique negative involution-module rotation constraints.
`round4_higher_c3.py` retains all three pointed associators and applies their
exact twist support. The final `round4_higher_e6.py` proof uses the full
conductor-60 field with projection, twist masses, joint character spectra,
Galois multiplicities and ordinary third-rotation equations. Its proof does
not depend on exploratory real-field MILP results, additional Clifford
rotation constraints or low-Verlinde inequalities.
`round4_higher_fast.py` supplies full-tensor detectors
and an exact, reconstruction-checked subfield arithmetic acceleration.

Exploratory scripts and receipts explicitly distinguish a completed exact
obstruction, surviving necessary relaxation, numerical MILP status, and
budget-incomplete exploration. None of the latter three changes a status.
The source classification of pseudo-unitary half-E6 categories has been
independently audited from Hagge–Hong arXiv:0704.0208 and Hong–Rowell–Wang
arXiv:0710.5761. The two positive half-E6 choices are covered by conjugating
the entire putative category; the integer based ring and positive dimensions
are preserved. This is an existence reduction, not an omitted branch.
Independent source, relabelling and negative-mutation audits are in
`../models/c3_independent_audit.json` and
`../models/half_e6_independent_audit.json`.

`coverage.py` exhausts the inherited ten frontier tensors and 54 realized
controls for subcategory recognition and runs a bounded half-E6 mass scan.
It also checks all cyclic-three associator/flux source twist domains exactly.
`frozen_inputs.py` selects these 64 inputs from the frozen campaign manifest
and model catalog, independent of subsequent decision changes.
`c3_controls.json` records 59 inputs without a C3 subring, three implementation
ineligibilities, one surviving positive control (R6_1_6), and the canonical
R6_6_49 exclusion. `e6_controls.json` records 62 implementation
ineligibilities, the canonical R6_6_1035 exclusion and an initial 20-second
positive-control timeout. The longer follow-up `e6_positive_retry.json`
completes that positive R6_2_127 check in 96.58 seconds, with two necessary
systems surviving. There are no false positive exclusions among the 54
realized controls. Recognition of a subring and implementation eligibility
are distinct, and ineligibility is not a mathematical conclusion.

For R6_5_1204, `R6_5_1204_ambient_h3.json` and
`probe_1204_verlinde.json` record all 39 low frames and eight admitted character
assignments across two frames. Both assignments of the first frame are
excluded. The next frame retains a necessary relaxation even after low
Verlinde and restriction-product equations (5,194 rows, 8,267 variables).
The failure of particular Morita model candidates is documented separately
in `../models/`; it is not a categorification obstruction.

The earlier timed-out full-field probes, surviving weak mass systems,
real-field MILP infeasibility reports, and unsuccessful congruence searches
remain as exploration records. The later degree-eight complex-field probe
also found four exact separating rays, but has no independent public replay
allocation; the canonical R6_6_1035 proof is the full conductor-60 certificate.

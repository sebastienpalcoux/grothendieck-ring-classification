# Research audit (not a catalogue of proofs)

The authoritative decisions are in `data/decisions.json` and the authoritative
new exact certificates are in `certificates/multiplicity_three.json` and
`certificates/structure_only.json`. They are independently checked by `verify.py`.
The positive source is reconstructed in `software/near_group_inversion.py`.
The authoritative feasible relaxation is `systems/modular_frontier_215.json`.

This directory preserves discovery scripts and logs, including unsuccessful work.
`higher/scan_summary.json` covers all 34 input residuals of multiplicities 4--6.
Its `nonexclusion` status includes ineligible full character fields; it does not
assert an exact feasible point for every such ring. Two `error` records are native
60-second low-search timeouts; three `timeout` records are outer 360-second limits.
The two pseudo-unitary exclusions are recertified by the shorter inherited
character-induction checker. Their general lifting attempts did not close.

The experimental modular-product MILP, spectral-involution and Morita searches
supply no allocated negative certificates. Floating-point infeasibility reports
are not mathematical proofs. A larger experimental rational solution is retained
for reproducibility, but only the 230-equation, 199-variable witness is part of the
release-wide verification contract. Neither solution is a category or modular datum.

Some original scripts/logs contain absolute paths to the investigation directory.
They are historical discovery records, not portable verification commands. The
supported entry points at the repository root and in `software/` use relative
paths. Scientific scope and authoritative files are described in the manuscript.

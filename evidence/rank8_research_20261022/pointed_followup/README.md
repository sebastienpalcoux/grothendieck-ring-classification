# Order-two pointed induction and Fourier fibre packing

**R8_3_1795 is excluded from general complex fusion categorification.**
All sixteen admissible second-indicator assignments are excluded by exact
separators after the new pointed phase and integer Fourier-fibre filters.
The separate, accepted general-to-Galois-pseudo-unitary gate supplies the
lift from the initially pseudo-unitary calculation.

**R8_3_1768 remains unresolved, with a new structural restriction:** every
categorification must have the nontrivial associator on its pointed C2
subcategory. All eight assignments with pointed second indicator +1 are
excluded. The -1 assignment `(-1,1,1,1,1,1,1)` has an exact rational
solution to the necessary cone. The other seven -1 assignments were not
searched in this refinement. The feasible solution is not a model.

`PROOF.md` gives the general equal-fibre-mass lemma, the finite integer
packing argument, domain completeness, and the categorical conclusions.
The complete packing test is an individual-column necessity test; a hull
of entire integral fibre configurations remains a possible stronger test.
It is not needed for the R1795 exclusion.

## Reproduction

The accepted no-argument verifier is read-only:

```sh
python evidence/rank8_research_20261022/pointed_followup/verify.py
```

It rebuilds both complete domains, checks all recorded exact separators
and the R1768 rational feasible witness, verifies full branch coverage for
each excluded parity, validates the frozen source hashes, and compares
the results with the saved receipts. All checks remain active with
`python -O`.

The individual producer replays are:

```sh
python evidence/rank8_research_20261022/pointed_followup/c2_fibres.py --ring 1768 --verify
python evidence/rank8_research_20261022/pointed_followup/c2_fibres.py --ring 1795 --verify
```

`R8_3_1768.json` and `R8_3_1795.json` are immutable terminal results.
`verification_R8_3_1768.json` and `verification_R8_3_1795.json` pin every
imported repository Python module and their respective terminal result.
`R1795_pointed_associator_obstruction.json` preserves the earlier complete
odd-parity certificate; the verifier requires equality with the odd record
in the terminal R1795 result.

The inherited complete central-induction cones are in
`../../rank8_frontier_20261021/global_induction/`. The general-to-Galois-PU
gates are in `../pivotality/`. Independent audits are in
`../r1768_r3472/`. The additional `r1795_morita/` calculation records the
intermediate subgroup-algebra investigation; it is not used by the final
R1795 exclusion.

No frozen earlier research source, repository status, manuscript, or site
file is changed by these scripts. Numerical linear programming proposes
the witnesses; every claimed conclusion is checked in exact arithmetic.

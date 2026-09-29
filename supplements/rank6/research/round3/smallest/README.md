# The forced C4 associator continuation

The tensor R6_4_6 is excluded for general complex fusion categories. The
canonical proof is `R6_4_6_certificate.json` (height four, ten low frames,
forty exact separators). `theorem.tex` gives a uniform proof that the
pointed associator is class 2, and that the uniform family parameter must
be even with a unique anti-invariant involution-module action.

`software/round3_smallest.py` recognizes the entire multiplication tensor;
it has no census identifiers among its hypotheses. Its general-scope
verifier uses the two-dimension Galois-pseudo-unitary reduction and exact
integer checks, without numerical optimization.

The full-census scan finds nine members, with family parameter 0 through 8.
Parameters 0 and 2 have established unitary models. Odd parameters have no
involution-module representation. Parameters 4, 6, 8 have the enclosed
forced-twist certificates; only parameter 4 is a new exclusion.

`coverage.json` records screening of all 16,612 tensors, the frozen 22
residual inputs, and all 54 known positive models. Of the two positive
family members, R6_2_4 survives the necessary central system; R6_1_3 is
ineligible for this implementation because its global dimension is rational.
This distinction is retained explicitly.

`final_replay.json` verifies the three canonical height-four certificates
under Python `-O` with optimizers disabled. `controls_optimized.json` records
rejection of six certificate mutations and recognition under all 120 based
relabellings. `cocycle_indicator_check.py` checks all 1024 cyclic cocycle
identities and the restriction/indicator conventions used in the proof.

From the release root:

```bash
python -O research/round3/smallest/replay.py
python -O research/round3/smallest/controls.py
python -O research/round3/smallest/cocycle_indicator_check.py
python research/round3/smallest/scan.py
```

The older height-six prototype remains as a reproducibility record;
`R6_4_6_height6.json` is superseded by the smaller canonical certificate.
Every discovery job had an explicit limit below 15 minutes.

The secondary R6_4_91 investigation imposes the exact scalar conditions
nu3(b1)=nu3(b2)=1 and the discrete Clifford values nu3(b5) in {-2,1}.
It leaves two necessary branches. Both existing rank 42 witnesses already
have all three third indicators equal to 1. The complete stronger systems
were replayed exactly, with optimizers disabled, for these two witnesses
and the two rank 36 R6_4_22 witnesses. `frontier_witness_audit.json` records
all four successful replays and their explicit 890-second job budgets.
These remain feasible necessary relaxations, not categorifications or full
modular data. No classification allocation was changed for either ring.

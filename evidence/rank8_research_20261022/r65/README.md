# R65 pointed-phase/Fourier obstruction

New result: every pointed-associator branch of `R8_3_65` is excluded by one
unified central-induction/Fourier obstruction. With the published
two-dimension Galois reduction, this completes its general complex
categorification exclusion. See `PROOF.md` for the full proof and all
dependencies. The earlier class-zero subgroup-dual theorem is not needed.

The new uniform step is to use equality in the pointed higher-indicator
trace bound *before* passing to relative traces. Fourier inversion then
gives exact dimension mass in each twist fibre. For R65 this forces every
central constituent over a pointed generator to occur once and to contain
at most eleven noninvertible source summands. These restrictions eliminate
the last odd-associator branch.

The decisive files are:

* `pointed_phase_k0_fourier.json`: two exact separators covering class 0,
  with Fourier integrality; 2413 allowed columns, 283 rows.
* `pointed_phase_k1_fourier.json`: two exact separators covering classes
  1 and 3, with Fourier integrality; 1992 allowed columns, 283 rows.
* `pointed_phase_k2.json`: two exact separators covering class 2; 2222
  allowed columns, 283 rows. Fourier integrality is not needed here.
* `pointed_phase_cone.py`: complete-domain construction, discovery, and
  exact replay; all earlier modules are imported read-only.
* `verify_all.py` / `verification.json`: source-level arithmetic checks,
  six-branch replay, and SHA256 inventory of imported repository modules
  and theorem inputs.

`pointed_phase_k1.json` retains the earlier, weaker odd-class attempt:
one exact feasible relaxation and one exact separator. The feasible
relaxation is deliberately retained to identify the genuine contribution
of the Fourier argument. `pointed_phase_k2_fourier.json` is a redundant
stronger class-2 check and is not required by the proof.

Exact replay, requiring no optimization solver:

```sh
python evidence/rank8_research_20261022/r65/verify_all.py
python -O evidence/rank8_research_20261022/r65/verify_all.py
```

Reproduce the three decisive discoveries, then replay:

```sh
python evidence/rank8_research_20261022/r65/pointed_phase_cone.py --k 0 --fourier --seconds 60
python evidence/rank8_research_20261022/r65/pointed_phase_cone.py --k 1 --fourier --seconds 60
python evidence/rank8_research_20261022/r65/pointed_phase_cone.py --k 2 --seconds 60
```

The LP solver is used only to discover rational separator candidates;
verification enumerates the entire allowed domain and checks every sign
exactly. Discovery may produce different valid separators depending on
the solver version, so the saved certificate hashes need not be preserved
by rerunning discovery. The saved replay is deterministic.

No searches for a unitary model, no assumption that pseudo-unitarity implies
unitarity, and no twist-order cutoff enter the exclusion. The inherited
finite list of relative trace types represents roots of unity of all orders.

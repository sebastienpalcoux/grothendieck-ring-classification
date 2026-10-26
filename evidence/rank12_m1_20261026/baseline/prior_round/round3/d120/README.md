# Dimension120: complete offline continuation

Three new unitary models (R12_1_142, R12_1_361, R12_1_444); twelve new general-complex exclusions; none unresolved in this family. The earlier model R12_1_25 is retained as a positive control.

Read `theory.md` for the categorical converse, both Morita reductions, forced group-subgroup pair, complete relative cohomology coverage and the coprime-twist invariance proof. Read `results.json` for the ledger changes.

`all_graph_twists.json` records all four cohomologically relevant construction outputs, including complete exact scalar/matrix actions, source maps and all tensors. The parameters `[a,b]` mean `a*(u+v)+b*(w+v)` in the notation of the proof. Nothing is inferred from a numerical associator search.

Standalone replay requires Python3 and NumPy only:

```
python verify.py
python -O verify.py
```

The replay reconstructs the Schur cover cocycle, computes the second generator by transfer, checks all12960000 transfer3cocycle equations, verifies all original and balanced bimodule identities and complete projective characters, reconstructs every fusion coefficient, and compares all16 input based rings to all four outputs. It also verifies the exact source tensor premises used in the Morita argument. Each pass takes approximately one minute.

`graph_twist.py` and `all_graph_twists.py` also run as constructive discovery scripts, overwriting their respective output JSON; they read only the local frozen source tensors. `common.py`, `group_ops.py`, `scalar_base.py` and `monomial.py` are the standalone runtime. All mathematical classification premises remain stated in the proof; this is not a proof-assistant formalization. Independent human verification is pending.

No repository or website was revised.

The separate R350 audit is in `audit_R350.md`. Its portable exact replay
requires Python 3 and SymPy and reads only `audit_R350_inputs.json` beside
the script:

```
python -O audit_R350.py
```

It independently reconstructs the complete low/high restriction domains
and all 32 indicator systems, then verifies every frozen integer Farkas
ray without importing the rank-six code or invoking an optimizer.

# Completion of exact multiplicity nine

These seven portable proof bundles exclude the eleven final multiplicity-nine
rings for general complex fusion categories. Each contains frozen full tensor
inputs, proof text, exact certificates and explicit verifiers that remain active
under `python -O`.

| Ring | Required bundles | Argument |
|---|---|---|
| R6_9_529, R6_9_2455 | involution_pair | Signed-dimension saturation and induction |
| R6_9_1060 | free_involution | Quadratic dimension descent and 128 exact Farkas rays |
| R6_9_3748 | psu25 | Sphericality and relative-center Galois constraints |
| R6_9_7018 | gauss8200, pivotal_gap | Higher-field obstruction and quadratic-sector exclusion |
| R6_9_7741, R6_9_7742 | triangle | Bounded deficit, triangle saturation and retained spherical obstructions |
| R6_9_8099, R6_9_8101 | pivotal_gap | Quartic dimension-field trace obstruction |
| R6_9_8200 | gauss8200 | Gauss-family parity obstruction |
| R6_9_8785 | gauss8200, case8785 | Higher-field obstruction and exact signed-spectrum exclusion |

From the package root, replay all required bundles once per process:

```bash
python software/replay_m9_completion.py
python -O software/replay_m9_completion.py
python software/m9_completion_controls.py
python -O software/m9_completion_controls.py
```

The campaign is `certificates/m9_completion.jsonl`. Its proof manifest and normal,
optimized and negative-control receipts are in `verification/m9/completion/`.
The manifest binds the tensor hashes, complete proof-bundle files and transitive
local Python checker imports. Child verifiers disable numerical optimizer entry
points. Fresh temporary copies prevent reuse of an unbound compiled helper.

This third campaign preserves the preceding classification and advanced campaign
bytes. Its single recorded stage receives eleven rings and excludes all eleven;
it records no unsuccessful discovery attempts. The complete census contains
25,421 rings: 25,362 excluded, 57 realized and the two historical open rings
R6_4_155 and R6_8_1660.

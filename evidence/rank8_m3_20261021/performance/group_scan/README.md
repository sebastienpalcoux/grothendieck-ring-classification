# Exhaustive ordinary finite-group model scan

This is a fresh rerun after workspace loss, using GAP 4.12.1 and SmallGrp 1.5.3.
The target set is the fixed 28 integral profiles among the 277 first-stage
survivors, not a current unresolved-status ledger. All **760** groups at the
11 required orders were visited. Every group with eight conjugacy classes and
a compatible degree vector had its complete character multiplication tensor
exported and compared under every necessary dimension-compatible unit-fixing
basis permutation.

| Order | Groups | Rank-eight groups | Tensors exported |
|---:|---:|---:|---:|
| 40 | 14 | 0 | 0 |
| 60 | 13 | 0 | 0 |
| 78 | 6 | 1 | 1 |
| 80 | 52 | 1 | 1 |
| 84 | 15 | 0 | 0 |
| 90 | 10 | 0 | 0 |
| 96 | 231 | 0 | 0 |
| 216 | 177 | 0 | 0 |
| 280 | 40 | 0 | 0 |
| 360 | 162 | 0 | 0 |
| 660 | 40 | 1 | 1 |

The only matched targets are the known controls **R8_3_342**, SmallGroup(78,1),
and **R8_3_724**, SmallGroup(660,13). No additional ordinary representation
model is found. The result does not exclude arbitrary fusion categories,
quasi-Hopf categories, or twisted group-theoretical constructions. In
particular a separate twisted model for R8_3_3342 is consistent with this result.

The [SmallGroups manual](https://docs.gap-system.org/pkg/smallgrp/doc/manual.pdf)
describes a complete irredundant list for all orders at most 2000 except 1024;
all scanned orders lie in that range. The scan relies on that catalogue and
GAP's exact character arithmetic. Package versions and downloaded package
hashes are retained in [installation.json](installation.json).

## Reproduction and CI scope

```bash
python3 prepare_scan.py
gap -q -b -T scan.g > gap_scan.jsonl 2> stderr.log
python3 summarize_scan.py
python3 -O summarize_scan.py --check
```

The read-only `--check` uses only Python's standard library. Explicit checks
remain active under `python -O`. It validates that each order starts and
finishes once, every group index appears exactly once, all dimension equations
hold, exported tensors are associative unital nonnegative rings, and the saved
per-ID outcomes reproduce by exact full-tensor comparison. It binds the script,
targets and transcript by SHA-256. It does **not** regenerate GAP's group
catalogue or character tables; label this as a transcript audit in aggregate CI.

[results.json](results.json) gives the order inventory and all attempts;
[per_id_attempts.json](per_id_attempts.json) is the directly ingestible per-ring
list. The transcript is actual newly executed GAP output, not a reconstruction
from remembered outcomes. Its stderr is empty.

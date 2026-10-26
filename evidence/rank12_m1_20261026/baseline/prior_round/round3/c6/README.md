# Order-six quadratic packet

Accepted result: **R12_1_350 is excluded from general complex categorification**.
The other four input rings remain unresolved. See `results.json` and `theory.md`.

Portable replay (standard library plus SymPy):

```sh
python -O verify.py
```

This uses only `frozen_inputs.json`, `frozen_R350.json`, and `verify_R350.py` in
this folder. It requires no repository checkout, network, SciPy, or optimization.
It raises explicit exceptions on failed checks and writes `verification.json`.

The `probe_*.py`, `*_probe.json`, and `verify_local.py` files record discovery
work. They are not the portable replay and some import the earlier project
implementation. Unseparated probes never establish existence.

The R350 proof was independently checked in `../d120/audit_R350.*` before the
independent replay was frozen here. No online content was changed.

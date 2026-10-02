# Rank-six all-p Minkowski certificates

Both remaining rank-six fusion tensors satisfy **every** Lim Corollary3.4 inequality, for all real p≥1 and all nonnegative vectors. This package proves that claim by exact finite certificates. It does not construct categories or exclude either tensor.

Run locally:

```sh
python -m pip install -r requirements.txt
python verify.py
```

Run against the repository tensors from the repository root:

```sh
python evidence/rank6_laptop_20261002/all_p_minkowski/verify.py --tensors supplements/rank6/data/unresolved_tensors.json
```

The verifier uses SymPy and the Python standard library. No SciPy, NumPy, optimizer, internet connection, or center computation is needed. The initial replay took under one second in the task environment; laptop timings depend on the installed Python and SymPy versions. Checks remain enabled under `python -O`.

Read PROOF.md for the short coupling–Minkowski argument. The verifier checks 216 triples and 23,328 marginal equations per ring. All 1,120 stored probability entries are verified in exact algebraic number fields; remaining triples get direct couplings whose equations are checked too. An external tensor file is optional but recommended when auditing a repository checkout.

The negative controls record rejection of negative probabilities, incorrect marginal values, and missing triples for each ring.

This exact result means that increasing the random-search budget for these particular finite-p inequalities cannot resolve either ring. Further computation should target a different necessary condition or model equations.

# Exact diagnosis of four rank-six replay failures

This is an AI-generated computational review, not independent human verification or Lean formalization. It checks the stated arithmetic and implementation behavior; it does not newly prove the categorical hypotheses behind these exclusions.

The fresh full replay reported failed higher-indicator Farkas checks for `R6_5_638`, `R6_6_1035`, `R6_8_311`, and `R6_8_3664`. All four failures reproduce in fresh processes, without reused worker state. Their first failed systems are mathematically unchanged between SymPy backends: the stored certificates use a different row order or row orientation from the one reconstructed with Flint's rational-number display. No ledger, frozen certificate, or frozen checker was changed during this diagnosis.

## Exact cause

Several inherited constructors order algebraic field elements by `str`. SymPy's `ANP` representation contains the representation of its ground-field coefficients. With the Python ground backend a rational coefficient is displayed as `MPQ(a,b)`; with the Flint backend it is displayed as a rational literal. Thus `sorted(..., key=str)` can change an orbit representative, the orientation of an equality, or the order of equalities. A stored positional Farkas vector must use the same row convention as the matrix it is paired with.

The relevant paths are `augmented_spectrum.AugmentedSpectrum.balance` for R638 and the coupled Galois balance construction in `round4_higher_fast.coupled_balance_cached` for R1035. The latter inherits the string convention of `round3_m4.coupled_balance`, which is also used directly by the Ising projection checker `round4_m8_ising.system` for R8311. The Fibonacci subfield checker for R83664 uses the same string convention in `spectral_induction.Spectrum.balance`.

| Case | First failed system | Exact Python/Flint difference | Unchanged ray in Python convention |
|---|---:|---|---|
| R6_5_638 | 277 rows, 531 columns | Only rows 187–213 inclusive are negated, including their right sides; all other entries agree. Indices are zero-based. | `min(Aᵀy)=0`, `bᵀy=-2504839010202541056`. |
| R6_6_1035 | 4798 rows, 6173 columns | A permutation moves 1239 rows; every integer entry and right side agrees under that permutation. No sign changes or column permutation occur. | `min(Aᵀy)=0`, with exactly the same strictly negative `bᵀy` recorded in the comparison receipt. |
| R6_8_311 | 1017 rows, 1896 columns | A permutation moves 174 rows; every integer entry and right side agrees. No sign changes or column permutation occur. | `min(Aᵀy)=0`, `bᵀy=-24525175067893939132416`. |
| R6_8_3664 | 708 rows, 2184 columns | A permutation moves 218 rows; every integer entry and right side agrees. No sign changes or column permutation occur. | `min(Aᵀy)=0`, with exactly the same strictly negative `bᵀy` recorded in the comparison receipt. |

The comparisons include the full matrix, the complete right side, and the saved ray. Candidate matches are located by a digest, then **every matched integer entry is compared directly**. None of these comparisons relies on approximate linear algebra, a floating-point tolerance, or merely matching row counts.

R638 reconstructs exactly the same failed matrix with python-flint 0.8.0 and 0.9.0. Upgrading Flint alone therefore does not correct this positional convention. The native Gram executable and relevant Python/C++ sources also agree byte-for-byte between the canonical and initial replay copies; a stale executable or reused worker state is not needed to reproduce the failures.

## Complete unchanged-certificate replay

The rigorous operational correction is to set `SYMPY_GROUND_TYPES=python` **before importing SymPy**, then run the unchanged checker against the unchanged tensor and certificate. This selects the row convention used by the saved certificates. It changes no equation, hypothesis, inequality, or certificate entry.

- R6_6_1035: **PASS**, 333.177 seconds. The full general checker verified the reduction, all 12 low frames, and all 4 trace cases.
- R6_5_638: **PASS**, 460.220 seconds. The full general checker verified its reduction, complete outer module domain, and all 200 conditional trace branches.
- R6_8_311: **PASS**, 146.087 seconds. The full general checker verified its reduction, both low frames, and all 16 trace cases.
- R6_8_3664: **PASS**, 59.561 seconds. The full general checker verified its reduction, all 13 low frames, and both trace cases.

The isolated driver forbids `scipy.optimize.linprog` and `milp`. Its diagnostic wrapper calls the existing exact Farkas predicate and retains the existing failure behavior. Full replays are distinct from the explicitly labelled selected-matrix capture. The initial failed receipts remain available and are not overwritten by the corrected-environment results.

## Evidence and reproduction

`inputs_and_commands.json` binds the first two census records, unchanged certificates, ledger/source files, and full-replay commands; `R8311_inputs_and_commands.json` and `R83664_inputs_and_commands.json` supply the additional cases. `full_replay_commitments.json` links each full invocation to its raw receipt and exact input commitments. `R638_backend_matrix_comparison.json`, `R1035_backend_matrix_comparison.json`, `R8311_backend_matrix_comparison.json`, and `R83664_backend_matrix_comparison.json` contain the exact row maps, pairings, and input-file hashes. The complete captured systems are included as deterministic `.json.gz` artifacts. `compare_systems.py` performs the entry-by-entry comparison after decompression.

The code in `reproduce.py` is an external diagnostic driver; it imports the repository's unchanged checkers. Its only early-stop option is explicitly labelled as a selected-matrix capture and never reports a complete-certificate PASS. Full checks use no early-stop option.

```sh
SYMPY_GROUND_TYPES=python python3 reproduce.py --repo /path/to/repository --id R6_5_638 --out R638_python_backend.json
SYMPY_GROUND_TYPES=python python3 reproduce.py --repo /path/to/repository --id R6_6_1035 --out R1035_python_backend.json
SYMPY_GROUND_TYPES=python python3 reproduce.py --repo /path/to/repository --id R6_8_311 --out R8311_python_backend.json
SYMPY_GROUND_TYPES=python python3 reproduce.py --repo /path/to/repository --id R6_8_3664 --out R83664_python_backend.json
```

The environment condition matters for reproducible positional certificate replay. It does not imply that the alternative backend's equations are mathematically invalid: the captured failures above are exactly equivalent equality systems with incompatible positional ray coordinates.

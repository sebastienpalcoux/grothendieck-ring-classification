# Six unresolved fusion rings: exact continuation checks

Research continuation, 29 October 2026. **0 new whole-ring exclusions; 0 new models; all 6 rings remain unresolved.** The arguments are integrated into the current GitHub manuscripts.

| Case | Current result and limit |
|---|---|
| R6_4_155 | A specified near-group construction route forces the parent group C4 × C2³. Compatible finite metric data exist; the parent category is unconstructed. |
| R6_8_1660 | A positive representative has a nonreal Morita invariant. Several construction routes are excluded; this is not a general categorification obstruction. |
| R8_3_928 | Patterns 49, 191 and 40 are excluded, leaving pattern 186. An exact rank-20 modular datum and simple fusion ring pass the stated checks. Their categorification and realization as the required center remain unproved. |
| R8_3_941 | A direct modular-source restriction and coefficient-cone obstruction apply. Transferring the R1660 invariant requires an actual Morita equivalence, which is not proved. |
| R8_3_1154 | A hypothetical algebra 1+X4 has two possible six-vertex based-module actions. One forces a specific rank-seven dual ring; neither algebra nor module associators are constructed. |
| R9_2_137 | The positive Tambara–Yamagami sign is excluded. The negative sign has a checked rational necessary-data witness, not integral center data or a categorification. |

## What each kind of result means

A **theorem or branch obstruction** rules out exactly the hypotheses stated in its proof. A branch obstruction is not a whole-ring exclusion when another branch survives.

A **conditional construction restriction** describes what must follow if an algebra, parent category, or Morita equivalence exists. A compatible tensor, based module, or fusion ring does not establish that existence.

A **witness for necessary conditions** is only a solution of the displayed relaxation. Rational multiplicities, partial modular data, indicators, and nonnegative integral fusion coefficients do not replace associators or a proof of categorification.

The positive/spherical existence reductions and complete center domains from earlier project work are explicit inherited premises. Frozen files in `prior/` document those inputs; they are not represented as fresh audits of every earlier manuscript. New assertions and their scope are in the case reports and independent audit notes. Independent agent review is not independent human review.

## Run

Requirements: Python 3.10 or later and SymPy. The optional native zero/one-spectrum replay also requires `g++` with C++17 support. No optimizer, numerical solver, network connection, or enclosing repository is required.

    python run_checks.py
    python run_checks.py --include-native --receipt ../run_receipt.json

Use ordinary Python, without `-O` or `-OO`; several verifiers deliberately use assertions. The runner verifies every shipped file against `manifest.json`, checks dependencies, makes a temporary copy, and runs all selected checks there using the same Python interpreter. It verifies again that shipped inputs and receipts were unchanged. A JSON run receipt is printed; `--receipt` may save it outside this directory. Each check has a short timeout. The native replay is optional and is clearly recorded separately.

Run order and exact file inventory are in `manifest.json`. Large JSON inputs are stored as deterministic gzip files. The runner verifies their expanded hashes and restores them only inside its temporary copy. Use the runner to preserve the shipped receipts. Receipts certify the stated finite arithmetic checks, not omitted categorical premises.

## Read

- `pair/REPORT.md`: R1660/R941 deductions and their precise scope.
- `r155/CONTINUATION.md`: the conditional parent-group restriction.
- `r1154/CONDITIONAL_RANK7_ROUTE.md`: the hypothetical algebra/module route.
- `r137/NEW_RESULTS.md`: the positive-sign obstruction and surviving rational witness.
- `r928/REPORT.md`: the current modular reductions.
- `unified/`: independent exact replays, the conjugation-parity saturation theorem, and the strict bosonic-mass bound.

Exploratory programs, optimization proposals, stale witnesses, compiled binaries, and unrelated historical notes are omitted. The old positive-TY witness retained inside the frozen R137 domain is explicitly replayed only to verify why its necessary-data relaxation is insufficient; it is not presented as a surviving candidate.


## Exact identification in The Anyon Atlas

The rank-20 modular datum is the existing record [B20-02148](https://anyonatlas.org/data/B20-02148), Galois orbit 20.167. This identifies the proposed factor B, not the full center Sem times B. A safe exact cyclotomic comparison checks all 400 S entries, 20 twists and 8000 fusion coefficients under the project-to-Atlas permutation recorded in r928/atlas/atlas_match_receipt.json. The normalization is S_Atlas=L S_project, L=D/sqrt2. No novelty of the modular datum is claimed.

On 29 October 2026 the Atlas labels it Not CS and its Known Categorifiable selector does not include it. Its displayed possible algebra 1+X7+X11+X18, of dimension D/2, may condense to semion B02-00007; the export does not guarantee this algebra. Those data are not an algebra or categorical construction. R928 remains unresolved.

Run python r928/atlas/verify_match.py from the current proof root, or run the bundled combined checker. Source: the exact JSON export from the public record, accessed 29 October 2026; hashes and the explicit permutation are in the receipt.

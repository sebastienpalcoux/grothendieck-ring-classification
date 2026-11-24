# Rank five within the sharp multiplicity and dimension bounds

This directory verifies the final finite classification in the manuscript. Its mathematical inputs are commutativity of the rank-five Grothendieck ring, the bounds

- maximum fusion multiplicity at most four;
- global Frobenius–Perron dimension at most 48 + 24√3;

and Theorem A, which provides a pseudo-unitary Galois conjugate of every complex rank-five fusion category. Galois conjugation preserves the based ring, so a necessary condition for pseudo-unitary categorifiability can exclude a complex categorification.

## Run the verifier

From this directory, run:

```bash
python3 verify.py
```

Alternatively, from the parent directory, run:

```bash
python3 verify.py --classification-only
```

Requirements are Python 3.12, SymPy, NumPy, and a C++17 `g++` compiler supporting OpenMP. Use Python with assertions enabled; the census entry point explicitly rejects `python -O`. The complete verification uses only the bundled files, requires no network access, and compiles its helpers in temporary directories. All decisions are exact; no numerical feasibility decision is accepted.

## Optional additional audits

From this directory, run `python3 verify_independent_census.py`. It regenerates the symmetry orbits and associativity equations, verifies the necessary linear-completion equations, compares the optimized census with a replay bypassing nonlinear shortcuts, and independently reconstructs the `Ad(SU(3)_4)` tensor from its Pieri graph. The results are 220 self-dual rings and 49 non-self-dual rings (47 with one dual pair and two with two dual pairs).

The replay shares the existing fraction-free linear-completion routine and basis parametrization. It is an additional reproducibility check, not a wholly independent implementation or a formal verification. It does not read the stored witness records.

Run `python3 verify_additional_audits.py` for the targeted checks. It rejects the concrete malformed subring certificate that previously falsely excluded `Rep(D14)`, verifies the repaired quadratic cutoff by exact fractions, and compares the sharp-dimension decision with exact root isolation for all 269 generated rings, including the three at equality. It also computes the relevant 864 cyclotomic moments and 19 joint trace vectors directly, compares all 14 induction/indicator cases with direct low-column enumeration, compares all 11 residual Gram cases with direct high-column enumeration, and certifies complete interval coverage and upper endpoints for the three quartic generator ranges.

The latter audit shares the ring generators, field data, certified root intervals, and construction of individual restriction-column sets. Its dimension comparison uses exact root isolation instead of shifted-polynomial coefficients. Its interval ranges are derived by Lagrange interpolation and divided differences, independently of the original fixed cutoffs and padding. It does not independently establish the categorical assumptions. Both optional commands passed; their current output is recorded in `../additional_verification_round4.txt`.

Three further optional probes are in `../audits_round4/`. Run `python3 ../audits_round4/positive_models.py` to check the relevant necessary conditions on all seventeen models and dimension divisibility on their twenty-seven proper nontrivial fusion subrings. Run `python3 ../audits_round4/dihedral_center.py` for an explicit feasible higher-trace system from `Z(Rep(D14))`, including all twenty-eight central simples and thirty-two indicator inequalities through order six. Run `python3 ../audits_round4/linear_completion.py` for the full multiplicity-four generator run with undefined-behavior sanitization and an exact rational row-reduction comparison on 659 inputs (269 generated records and 390 fixed-seed boundary/random inputs).

The new probes share model/criterion code or the native matrix construction. The row-reduction comparison is sampled outside the generated records and is not a formal proof or an independent exhaustive census. Use assertions-enabled Python; the native probe also needs the `g++` undefined-behavior sanitizer. All native binaries are temporary. These programs do not run as part of the ordinary verifier; their actual outputs are in `../additional_verification_round4.txt`.

## Exhaustive enumeration and the dimension test

The generator solves the unit, duality, Frobenius reciprocity, and associativity equations in all three rank-five duality types. With coefficients at most four, it generates 269 based rings up to isomorphism.

For a ring with fusion matrices N_i, the Casimir matrix C = Σ_i N_i N_iᵀ has the global Frobenius–Perron dimension as its largest eigenvalue. Its eigenvalues are real. For M = 48 + 24√3, the bound D ≤ M is therefore equivalent to every coefficient of det((t + M)I − C) being nonnegative. The verifier checks these signs exactly in Q(√3), including equality at the endpoint.

| Maximum multiplicity | Generated | Within the dimension bound | Excluded | Realized |
|---|---:|---:|---:|---:|
| 1 | 16 | 16 | 6 | 10 |
| 2 | 37 | 30 | 27 | 3 |
| 3 | 82 | 46 | 44 | 2 |
| 4 | 134 | 22 | 20 | 2 |
| **Total** | **269** | **114** | **97** | **17** |

Enumeration and the dimension test establish the 114-ring list before the verifier reads the stored witness records. Every witness is matched to a generated tensor, and all unit-preserving permutations of the four nonunit basis elements are allowed when testing based isomorphism.

## Exclusions and model identifications

The 97 exclusions are partitioned as follows:

| Necessary condition violated | Certificate kind | Rings |
|---|---|---:|
| Formal-codegree d-number condition | `dnumber` | 76 |
| Subcategory dimension divisibility | `subring` | 2 |
| Integrality detected by a central-dimension norm | `fp_norm` | 3 |
| Membership in the simple-dimension field | `fp_dimension_field` | 2 |
| Unit induction, Gram matrices, and second moments | `induction` | 10 |
| Higher-indicator trace constraints | `finite_indicator_traces` | 4 |
| **Total** | | **97** |

Each certificate is checked against its full fusion tensor. The induction and higher-indicator checks regenerate the admissible restriction columns and indicator assignments. Each stored separating form is checked exactly on all required columns and on the prescribed moment vector.

Subring certificates require distinct integer basis indices in the range `0 <= i < rank` before any tensor or character indexing. This rejects negative indices that Python would otherwise interpret as aliases of valid basis elements. Both stored subring certificates satisfy the corrected validation.

The seventeen positive model tensors are constructed in `criteria/model_registry.py`. The verifier checks their fusion-ring axioms and distinctness, and supplies an explicit basis permutation identifying each retained positive witness with exactly one model. The manuscript cites the unitary categorical constructions; in particular, its endpoint construction explains the C₂-equivariantization tensor directly from Izumi's symmetry formulas.

The verifier uses only the pseudo-unitary necessary conditions justified by Theorem A. There is one verification mode; no additional spherical or signed-extension stage is needed.

## File roles and sources

- `generator/`: the ring parametrizations and C++ enumeration programs.
- `dimension_test.py`: the exact sharp-dimension test.
- `data/bounded_witnesses.json`: the 114 tensors with their model identifications or exclusion certificates.
- `criteria/`: exact ring arithmetic, categorical necessary conditions, and model constructions.
- `verify.py`: regeneration, coverage checks, and verification of every decision.
- `verify_independent_census.py`: optional symbolic equation, alternative census, and Pieri-model checks.
- `verify_additional_audits.py`: optional certificate-input, exact cutoff, cyclotomic-trace, Gram-column, and generator-enclosure checks.

The generator and parametrization originate from `fusion-ring-census`, commit `942dbd9c4f4149479e51acb1224f3c71ca47a64b`. The criteria and restricted witnesses originate from `sebastienpalcoux/grothendieck-ring-classification`, commit `d35cb684d2f27cca18f89ab24c769af756c16160`, under `evidence/prepublication_20261017/rank5`. The present package retains the necessary pseudo-unitary certificates and verifies them directly. No tables or categorification decisions are downloaded from those repositories during verification.

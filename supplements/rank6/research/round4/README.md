# Fourth-continuation coverage

**Final coverage report.** The domain is the frozen ten-tensor campaign manifest and 54 distinct positive controls; the current ledger is not used to select inputs.

The canonical fourth-round file allocates **4 new general exclusions**, leaving **6** input rings unresolved. Only this canonical file supplies allocation counts.

Regenerate and independently validate the release receipts with:

```sh
python research/round4/coverage.py --require-canonical
```

The aggregator checks complete source/canonical equality, SHA-256 bindings, frozen full tensors, disjoint inherited allocations, complete input/control domains, and the optimized optimizer-disabled unified replay receipt. It does not rerun the mathematical checkers.

| Multiplicity | Frozen inputs | New canonical exclusions | Remaining |
| ---: | ---: | ---: | ---: |
| 4 | 4 | 0 | 4 |
| 5 | 1 | 0 | 1 |
| 6 | 2 | 2 | 0 |
| 7 | 0 | 0 | 0 |
| 8 | 3 | 2 | 1 |

## Criteria and application domains

Counts from different criteria overlap. Structural screens are not full exclusion runs; a timeout is inconclusive.

| Criterion | Domain | Frontier outcomes | Positive controls |
| --- | --- | --- | --- |
| Fibonacci subcategory projection and subfield traces | all 10 frozen frontier tensors and all 54 positive controls | general_proof_reported: 1; ineligible: 9 | ineligible: 51; no_exact_obstruction: 3 |
| Ising twist support and projected masses | all 10 frozen frontier tensors and all 54 positive controls | ineligible: 7; targeted_campaign: 3 | ineligible: 53; no_exact_obstruction: 1 |
| Half-E6 subcategory recognition and twist-resolved mass | all 10 frozen frontier tensors and all 54 positive controls | ineligible_no_subcategory: 9; necessary_system_survives: 1 | ineligible: 3; ineligible_no_subcategory: 46; necessary_system_survives: 5 |
| Full half-E6 projection and complex character moments | all 10 frozen frontier tensors and all 54 positive controls | covered_by_complete_exact_certificate: 1; ineligible: 9 | budget_incomplete: 1; ineligible: 53 |
| Cyclic-three associators and projected twists | all 10 frozen frontier tensors and all 54 positive controls | covered_by_complete_exact_certificate: 1; ineligible_no_C3_subcategory: 9 | ineligible: 3; ineligible_no_C3_subcategory: 50; necessary_system_survives: 1 |
| Complex low Verlinde and restriction products | all 10 frozen frontier tensors and all 54 positive controls | budget_incomplete: 8; ineligible: 2 | budget_incomplete: 7; exact_rational_survival: 18; ineligible: 27; numerical_survival: 2 |
| Fourth moments and integer-square cuts | all 10 frozen frontier tensors and all 54 positive controls | budget_incomplete: 8; ineligible: 2 | budget_incomplete: 12; exact_rational_survival: 14; ineligible: 27; numerical_survival: 1 |
| Central invertible transport | all 10 frozen frontier tensors and all 54 positive controls | budget_incomplete: 7; ineligible: 3 | budget_incomplete: 11; exact_rational_survival: 5; ineligible: 38 |
| Squared-Galois orbit trace domain | all 10 frozen frontier tensors and all 54 positive controls | eligible_domain_constructed: 1; ineligible: 9 | eligible_domain_constructed: 2; ineligible: 52 |
| Quartic full-character profile implementation eligibility | all 10 frozen frontier tensors and all 54 positive controls | eligible: 5; ineligible: 5 | eligible: 1; ineligible: 53 |
| Exact integral complex and fourth-moment survivors | one targeted input; nine exact witnesses | exact_integral_necessary_relaxation_survives: 1 | outside this domain |
| Exact squared-orbit survivors | one targeted frontier input and two selected positive controls | exact_necessary_relaxation_survives: 1 | exact_necessary_relaxation_survives: 2 |
| Exact rational Ising projected survivor | one targeted frontier input | exact_rational_necessary_relaxation_survives: 1 | outside this domain |
| Normalized squared-dimension Galois balance | one targeted frontier input | exact_augmented_necessary_relaxation_survives: 1 | outside this domain |
| Exact finite count-profile reductions | three targeted frontier inputs and one positive control; complete low-frame domains | finite_necessary_profiles_survive: 3 | finite_necessary_profiles_survive: 1 |
| Additional bounded refinements | selected frontier inputs; explicit per-experiment scope | targeted_searches_recorded: 4 | outside this domain |
| Known-model and relative-center dimension comparisons | all ten frontier tensors; 61 constructors / 54 distinct model rings | no_match_in_tested_registry: 10 | outside this domain |

## Finite reductions and exact survivors

Full low-frame reconstructions and exact trace refinements leave the following necessary count profiles. Counts identify profiles independently of their character labellings; the JSON retains every labelled branch.

| Input | Reduction | Remaining ranks | Exact necessary-system witnesses |
| --- | --- | --- | --- |
| `R6_4_22` | 93 → 3 by low products → 2 by words through degree six | 30, 36 | Rank 36; rank 30 undecided |
| `R6_4_91` | Low frame 0: 264 → 4, then all rejected by trace rays. Low frame 1: 524 → 6 → 2 by exact mod-2 constraints | 36, 42 | Both ranks |
| `R6_4_629` | 784 → 5 by low words → 3 by exact twist rays; one character labelling remains | 30, 35, 38 | Ranks 35 and 38; rank 30 undecided |

These are reductions of necessary induction profiles, not exhaustive classifications of modular data. The positive control `R6_4_322` retains 24 profiles per labelling on its surviving low frame.

`R6_4_155` has an exact integral rank-36 necessary-system point satisfying 7,764 equations in 9,982 variables, including fourth moments and central-invertible transport. The eight weaker integral witnesses and their exact optimized replays are retained. `R6_4_629` also has exact squared-orbit relaxation witnesses; `R6_8_1660` has an exact rational projected-Ising witness that satisfies 252 added normalized-dimension balance equations. None is asserted to be a fusion category.

## Frozen frontier

| Input | Canonical outcome | Recorded criterion domains |
| --- | --- | --- |
| `R6_4_22` | unresolved | 12 |
| `R6_4_91` | unresolved | 12 |
| `R6_4_155` | unresolved | 12 |
| `R6_4_629` | unresolved | 14 |
| `R6_5_1204` | unresolved | 12 |
| `R6_6_49` | general_cyclic_three_projection | 11 |
| `R6_6_1035` | general_half_e6_projection | 12 |
| `R6_8_311` | general_ising_projection_rotation | 11 |
| `R6_8_1660` | unresolved | 14 |
| `R6_8_3664` | general_fibonacci_subfield_rotation | 11 |

## Scope notes

**Fibonacci subcategory projection and subfield traces.** The 64-input batch checks implementation eligibility and bounded proof discovery; a general proof report is allocated only through the canonical file. The separate full-census screen detects a based Fibonacci subcategory only; it is not 16,612 exclusion runs.

**Ising twist support and projected masses.** targeted_campaign points to separate exact proofs or bounded searches; it is not a successful obstruction. The separate full-census screen is structural recognition only.

**Half-E6 subcategory recognition and twist-resolved mass.** Subcategory recognition and full-character implementation eligibility are distinct. necessary_system_survives is a bounded discovery outcome; no exact primal point is inferred unless a separate receipt is cited.

**Full half-E6 projection and complex character moments.** This stronger criterion includes complete complex character/twist constraints beyond the separate coarse mass screen. Numerical survival or a budget interruption does not certify a primal point; the targeted general proof is separately replayed. The eligible positive R6_2_127 survives a separate 180-second follow-up; its original 20-second timeout remains recorded.

**Cyclic-three associators and projected twists.** All three pointed associators and their flux twist domains are retained. General exclusion is allocated only after the separate signed reduction and complete exact replay.

**Complex low Verlinde and restriction products.** Per-input discovery budgets are explicit. An exact rational control point certifies its equations, not a category. The dedicated R6_4_155 exact integral follow-ups supersede its short scan timeouts but do not alter the raw scan records.

**Fourth moments and integer-square cuts.** Per-input discovery budgets are explicit. An exact rational control point certifies its equations, not a category. The dedicated R6_4_155 exact integral follow-ups supersede its short scan timeouts but do not alter the raw scan records.

**Central invertible transport.** Per-input discovery budgets are explicit. An exact rational control point certifies its equations, not a category. The dedicated R6_4_155 exact integral follow-ups supersede its short scan timeouts but do not alter the raw scan records.

**Squared-Galois orbit trace domain.** eligible_domain_constructed certifies construction of the finite trace domain only; it is not primal feasibility. This implementation requires odd dimension prime support; its two positive exact controls and target witness are separate.

**Quartic full-character profile implementation eligibility.** Eligibility requires a quartic FP field and a supported full-character cyclotomic realization of conductor at most 24. This scan constructs the eligible domain only. R6_8_1660 is eligible but its full profile enumeration was not executed; R6_8_311 is excluded by a separate criterion. Full low-frame profile certificates cover R6_4_22, R6_4_91, R6_4_629, and positive R6_4_322.

**Exact integral complex and fourth-moment survivors.** All witnesses are checked with optimizers disabled under optimized Python. They are not complete center fusion rules, modular data, or a category.

**Exact squared-orbit survivors.** These exact necessary-system points do not supply a complete modular datum or category.

**Exact rational Ising projected survivor.** The primal coordinates may be fractional. Their equations are exact; integral induction data and categorification are not asserted.

**Normalized squared-dimension Galois balance.** These additional equations are checked exactly by the discovery/follow-up script. The separate optimizer-disabled replay covers the original 1,304-equation system.

**Exact finite count-profile reductions.** Historical experiments select a low frame. The later full_low_frame_receipt includes every low frame and compatible character labelling; final_twist_refinement retains only profiles not exactly rejected by the additional trace and congruence checks. A retained profile without an exact decision is not asserted feasible. R6_4_22 rank 30 and R6_4_629 rank 30 remain in this category. The positive R6_4_322 full-profile enumeration is an exact discovery control; no separate optimizer-disabled replay of that positive control is asserted. Individual integer-solver failures without independently checked proof certificates do not allocate exclusions.

**Additional bounded refinements.** These search records are historical or exploratory even when another exact proof resolves the same tensor. resource_incomplete and budget_incomplete are not feasibility or nonexistence certificates.

**Known-model and relative-center dimension comparisons.** This is a dimension-level comparison with a specified registry, not a proof that no model exists.

The report binds 166 source files by SHA-256. Its inventory includes unsuccessful and interrupted experiments; these do not supply additional categorical allocations.


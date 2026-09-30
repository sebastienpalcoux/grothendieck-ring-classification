# Automated frontier research

The authoritative [decision ledger](../data/decisions.json) records 16,552
general exclusions, 54 realized rings and six unresolved rings. Necessary
profiles, fusion tensors and modular data do not establish categorification.

## Current finite frontier

[`round5/coverage.json`](round5/coverage.json) records the exact scope, staged
reductions, canonical replay commands and file bindings for all six frozen
inputs. The [input manifest](../verification/round5/campaign_manifest.json)
contains the full tensors and their hashes. Run
`python -O software/round5_replay.py --list` from the package root to inspect
all current replay commands; `--check-receipts` audits retained evidence
without claiming a new mathematical replay.

- [`round5/quartic_pair/`](round5/quartic_pair/) and
  [`round5/fermion/`](round5/fermion/) contain the full fusion/modular
  reconstructions and coupled word/twist reductions for `R6_4_22` and `R6_4_91`.
- [`round5/m4_155/`](round5/m4_155/) contains the complete profile reduction,
  pointed constraints and semion-centralizer fusion-action frontier.
- [`round5/m4_629/`](round5/m4_629/) contains the rank-30 and rank-38
  obstructions and the exhaustive rank-35 modular completion.
- [`round5/m5_1204/`](round5/m5_1204/) contains the complete general reduction
  to 171 necessary induction profiles.
- [`round5/m8_1660/`](round5/m8_1660/) contains both complete low-frame
  enumerations with saturated conductor support and individual-root Ising
  mass bounds. [`round5/m8_1660_conductor/`](round5/m8_1660_conductor/)
  supplies the general categorical reduction. The complete actual-root
  systems and congruence reductions are in [`round5/m8_actual48/`](round5/m8_actual48/);
  [`round5/m8_modrep/`](round5/m8_modrep/) contains the exact finite modular
  representation spectra used to refine them.
- [`round5/unification/`](round5/unification/) contains independent audits,
  exhaustive domain controls and categorical positive controls of the shared
  Gram and balancing criteria.

The exact multiplicity bands 1, 2, 3, 6 and 7 are complete. All six current
frontier rings remain unresolved. The coverage file explicitly distinguishes
complete profile domains from tests of one selected profile or factorization.

## Retained proof dependencies and provenance

Earlier criterion directories and their original receipts remain available
for exact replay. Their counts and unresolved labels describe their frozen
inputs; they do not override the current ledger.

- [`round4/`](round4/README.md) supplies inherited finite profile reductions,
  subcategory center projection, twist-resolved masses and accepted general
  exclusions. Its earlier coverage report retains its original ten inputs.
- [`round3/`](round3/README.md) contains the C4 associator, full-character
  rotation, integral Morita, local arithmetic and signed-spectrum proofs,
  with the original 22-input coverage and model controls.
- [`round2_center/`](round2_center/README.md),
  [`round2_theory/`](round2_theory/README.md),
  [`round2_literature/`](round2_literature/),
  [`round2_higher/`](round2_higher/README.md),
  [`round2_external/`](round2_external/) and
  [`round2_audit/`](round2_audit/README.md) retain the general multiplicity-three
  completion, Clifford and arithmetic criteria, imported-proof audits and
  their precisely scoped scans.
- [`new_frontier/`](new_frontier/README.md),
  [`center_continuation/`](center_continuation/README.md),
  [`module_continuation/`](module_continuation/README.md) and
  [`model_continuation/`](model_continuation/) retain the earlier Morita,
  spectral, modular and grading calculations.
- [`m8_frontier/`](m8_frontier/README.md) and [`m8_audit/`](m8_audit/)
  retain the source-matching, modular comparison and scope controls.

Accepted negatives occur in the disjoint [certificate allocations](../certificates/).
Alternative proofs and overlapping criterion scans are not additional ledger
allocations. Numerical solver outcomes, process deadlines, failed hypotheses
and surviving necessary systems never assign an existence status. The source
census remains trusted; no independent census enumeration is claimed.

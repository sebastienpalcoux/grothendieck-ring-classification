# Rank-seven multiplicity-five continuation

> **Historical 19 October stage.** The counts and frontier below describe that stage. See the [20 October continuation](../rank7_m5_20261020/README.md) for current decisions; links to current ledgers and replay receipts follow the revised edition.

AI-generated research; independent human verification and Lean formalization
remain pending. The status below records the frozen computational continuation
of 19 October 2026.

| Scope | Supplied rings | Excluded | Unitarily realized | Unresolved |
|---|---:|---:|---:|---:|
| Exact multiplicity five | 5,805 | 5,789 | 1 | 15 |
| Rank seven through multiplicity five | 10,006 | 9,961 | 30 | 15 |

Every exclusion in the current ledger concerns all complex fusion categories.
All 4,201 earlier decision records are unchanged. The supplied census contains
the earlier representatives and 5,805 additional representatives; source
coverage and identifier transport are checked exactly. Completeness of the
producer's enumeration is a supplied claim: this continuation does not
independently regenerate the complete census.

The authoritative artifacts are the
[current ledger](../../supplements/rank7/output/rank7_ledger.json),
[continuation summary](../../supplements/rank7/output/m5/summary.json), and
[source transport](../../supplements/rank7/output/m5/source_transport.json).
The summary records disjoint first-certificate counts; separate exploratory
scans below overlap and must not be added to those counts.

## Model and proof evidence

* **Known model:** `R7_5_5678` is
  `Rep(AGL(1,7)) = Rep(C7 semidirect C6)`, with faithful action and dimensions
  `1,1,1,1,1,1,6`. The [exact character checker](models/verify_frobenius42.py)
  checks all 49 character inner products and 343 tensor coefficients; its
  [receipt](models/frobenius42_match.json) gives the basis permutation. This is
  a known group representation construction. No additional new categorical
  model was established.
* **New cyclic isotypic integrality criterion:** the
  [proof](review/CYCLIC_ISOTYPIC_PROOF.md),
  [checker](review/cyclic_isotypic.py), and
  [scan certificates](review/cyclic_isotypic_results.json) extend the cyclic
  stabilizer obstruction to isotypic summands for cyclic subgroups. They give
  a general exclusion of `R7_5_4757`; the other scan successes overlap earlier
  exclusions. [Positive and corrupted-certificate controls](review/cyclic_isotypic_controls.json)
  accompany the scan.
* **New cubic Fourier module obstruction:** the
  [categorical proof](theory/cyclic3_spectral.tex),
  [exact checker](theory/cyclic3_spectral.py), and
  [certificate](theory/cyclic3_spectral_certificate.json) exclude
  `R7_5_5007`. Its required cubic trace is 15, while the exhaustive list of
  81 permitted matrices has cubic traces only -3 or 6. The proof assumes no
  pivotal structure.
* **Other exact checks:**
  [integral formal codegrees](models/integral_codegree_results.json),
  [noncyclic maximal near-group exclusion](models/maximal_near_group_result.json),
  [rank-six subring descent](theory/rank6_subring_certificates.json), and
  [spectral involution modules](theory/spectral_module_results.jsonl) supplement
  the existing certificate pipeline. The
  [criteria scope audit](review/CRITERIA_SCOPE_AUDIT.md) records hypotheses,
  references, overlapping one-spectrum witnesses, and the distinction between
  general and conditional obstructions.

## Exact replay

From the repository root, with Python 3, SymPy, NumPy, and a C++17 compiler:

```sh
python supplements/rank7/software/verify_m5.py --jobs 4
python -O supplements/rank7/software/verify_m5.py --jobs 4
```

Both modes passed all 5,789 new exclusion certificates and the positive
character model; see the [normal receipt](../../supplements/rank7/output/m5/replay_normal.json)
and [optimized receipt](../../supplements/rank7/output/m5/replay_optimized.json).
SciPy is optional for discovery and is not required for exact replay.
An additional optimized replay with all SciPy imports disabled also
[passed](../../supplements/rank7/output/m5/replay_without_scipy.json).
The verifier also checks the source, canonical tensor order, model catalog,
and preservation of the earlier records. Earlier mathematical certificates
retain their separate historical replay archives. The `--metadata-only`
option checks bindings and coverage without replaying mathematical proofs.

## Open frontier and research notes

The 15 unresolved identifiers are:

`R7_5_443`, `R7_5_1214`, `R7_5_1964`, `R7_5_3895`, `R7_5_4530`,
`R7_5_4531`, `R7_5_4569`, `R7_5_4653`, `R7_5_4982`, `R7_5_5029`,
`R7_5_5039`, `R7_5_5040`, `R7_5_5343`, `R7_5_5623`, `R7_5_5778`.

Their full tensors and status records are in
[survivors.json](../../supplements/rank7/output/m5/survivors.json).
[Model research notes](models/RESEARCH_NOTES.md) distinguish exact models from
dimension coincidences and failed obstruction attempts. The
[theory handoff](theory/THEORY_HANDOFF.md) describes additional subring proofs
and the necessary module representations found for `R7_5_4982`; those
representations do not supply categorical associators or establish existence.
Numerical profiles and finite search failures are discovery diagnostics only.
Exhausted search budgets leave a case unresolved.

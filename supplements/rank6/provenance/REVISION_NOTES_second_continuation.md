# Revision notes — second continuation, 29 September 2026

## Result

Multiplicity three is complete. The release has **16,536 general exclusions,
54 categorifiable rings and 22 unresolved rings**. Relative to the supplied
40-residual revision, **18 further rings are generally excluded**.
There are no new positive identifications. The 16,612 census tensors, all
identifiers, and the 54 established positive-model identifications are unchanged.
The first continuation's seven exclusions are retained and are not counted
again as new here.

| Exact multiplicity | Rings | Excluded | Models | Unresolved |
|---:|---:|---:|---:|---:|
| 1 | 39 | 18 | 21 | 0 |
| 2 | 154 | 132 | 22 | 0 |
| 3 | 384 | 381 | 3 | 0 |
| 4 | 872 | 863 | 2 | 7 |
| 5 | 1,582 | 1,579 | 1 | 2 |
| 6 | 2,768 | 2,762 | 3 | 3 |
| 7 | 3,814 | 3,810 | 2 | 2 |
| 8 | 6,999 | 6,991 | 0 | 8 |
| **Total** | **16,612** | **16,536** | **54** | **22** |

## New accepted general exclusions

| Tensor | General obstruction | Accepted source |
|---|---|---|
| `R6_3_215` | Clifford stabilizer rotation; complete signed Galois reduction | `certificates/stabilizer_rotation_215.json` |
| `R6_4_174` | Higher-dimensional stabilizer rotation; general reduction | `research/round2_theory/R6_4_174_general.json` |
| `R6_4_258` | Quartic cyclotomic trace and stabilizer bound; signed reduction | `research/round2_literature/R6_4_258_general.json` |
| `R6_4_325` | Quartic cyclotomic trace and stabilizer bound; signed reduction | `research/round2_literature/R6_4_325_general.json` |
| `R6_4_416` | Higher-dimensional stabilizer rotation; general reduction | `research/round2_center/R6_4_416_general.json` |
| `R6_4_427` | Higher-dimensional stabilizer rotation; general reduction | `research/round2_theory/R6_4_427_general.json` |
| `R6_7_3582` | Ramified signed reduction and central-induction obstruction | `research/round2_higher/R6_7_3582_general.json` |
| `R6_7_3812` | Ramification, codegree integrality and signed Casimir trace | `research/round2_higher/R6_7_3812_general.json` |
| `R6_7_3813` | Biquadratic dimension field, norms and Casimir parity | `certificates/biquadratic_exclusions.json` |
| `R6_8_570` | Quartic cyclotomic trace and stabilizer bound; signed reduction | `research/round2_literature/R6_8_570_general.json` |
| `R6_8_2203` | Quartic cyclotomic trace and stabilizer bound; signed reduction | `research/round2_literature/R6_8_2203_general.json` |
| `R6_8_6234` | Ramification, codegree integrality and signed Casimir trace | `research/round2_higher/R6_8_6234_general.json` |
| `R6_8_6509` | Ramification, codegree integrality and signed Casimir trace | `research/round2_higher/R6_8_6509_general.json` |
| `R6_8_6520` | Trace-ideal saturation and all-orders quadratic Gauss bound | `research/round2_external/R6_8_6520_general.json` |
| `R6_8_6940` | Biquadratic dimension field, norms and Casimir parity | `certificates/biquadratic_exclusions.json` |
| `R6_8_6973` | Biquadratic dimension field, norms and Casimir parity | `certificates/biquadratic_exclusions.json` |
| `R6_8_6997` | Formal-codegree trace ideal exceeds the signed trace bound | `research/round2_external/R6_8_6997_general.json` |
| `R6_8_6998` | Biquadratic dimension field, norms and Casimir parity | `certificates/biquadratic_exclusions.json` |

The source column locates the complete general certificate used to freeze the
new record. `certificates/continuation_round2.jsonl` is the canonical disjoint
allocation. Some rings admit several new proofs; overlapping certificates are
checked but contribute only one exclusion.

## Why the multiplicity-three argument is complete

1. Unrestricted sphericalization reconstructs 1,480 signed quotient tables and
   63 sign orbits. Every nongauge character branch is rejected, and the surviving
   dimensions have the Frobenius–Perron Galois orbit.
2. All 16 involution-module branches are reconstructed. Twelve fail exact Gram
   separation and two fail the rank bound. The two remaining branches force
   the mixed stabilizer sign -1 on both fixed simples.
3. Pair insertion on the cubic invariant space gives three anticommuting
   involutions cyclically permuted by pivotal rotation. The resulting Clifford
   representation forces the third indicator to be -1 when that space has
   dimension two and the exponent is coprime to three. The Cauchy theorem gives
   this coprimality here from the dimension norm 2^6·17.
4. Every possible central-induction branch is covered: 91 low frames, 31 frames
   with character labellings, 50 total labellings and four second-indicator
   choices give 200 exact separating vectors. Their arithmetic replay uses no
   numerical optimizer and no chosen modular datum.

The general theorem and certificate are in Section 5 and
`software/stabilizer_rotation.py`. Independent normal/optimized replays and
mutation controls are retained under `research/round2_center/` and
`research/round2_audit/`. The earlier rank-22 witness remains valid only for its
specified necessary relaxations. A separate argument now also excludes the
whole actual Grossman–Izumi cyclic-eight Morita class, without assuming that
its modular data determine all possible braided categories.

## Uniform higher-multiplicity coverage

- `verification/round2/campaign_manifest.json` freezes all 40 inherited inputs,
  including all 39 at multiplicities 4–8, with the full tensors.
- `research/round2_theory/higher_campaign.json` records the generalized
  stabilizer test and additional height-six attempts. The higher engine handles
  non-self-dual fixed simples and uses the cubic dimension N[Y,Y,Y*]. Its
  averaged bound is -n/2 ≤ Re(ν3) ≤ n/4. Ineligible domains, surviving
  relaxations, and budgets remain explicit. The quartic extension has its own
  complete records in `research/round2_literature/quartic/`.
- The ambient cyclotomic theorem gives a finite joint relative-trace domain for
  all root-of-unity orders permitted by Cauchy prime support. The all-zero type
  covers arbitrary orders outside the finite conductor box. This does not
  assume a finite exponent bound.
- `research/round2_higher/ramification_application.json` records the complete
  frozen input scan for ramification and signed Casimir criteria. Its direct
  arithmetic exclusions do not assume pseudo-unitarity.
- `research/round2_external/biquadratic_full_census_scan.json` scans all 16,612
  tensors. The criterion applies to 51 and excludes all 51, including four
  newly resolved inputs; the other 47 were already excluded.
- `research/round2_external/trace_ideal_full_census_scan.json` also scans all
  16,612 tensors. It applies to 11,241 and independently excludes 1,827. These
  overlapping confirmations are not added to the classification count. Its new
  direct exclusion is R6_8_6997. Saturation of the same trace bound reduces
  R6_8_6520 to a pseudo-unitary Galois conjugate; the new Gauss theorem then
  requires at least 4,298 roots of unity where only 590 are available.
- `research/round2_higher/gauss_census_application.json` scans the full census
  for the tensor family underlying the Gauss theorem. Its five matches, at
  multiplicities 4, 5, 6, 7 and 8, all fail the pseudo-unitary criterion. The
  three lower members were already generally excluded; new general conclusions
  use their separately verified signed reductions.
- Each applicable new engine was checked on the 54 established positive models,
  with further permutation and deliberate-corruption controls. Nonapplicability
  to a positive model is recorded as such, not called a substantive survival.
  In particular, all 54 models are outside the current quartic criterion's
  domain: its dedicated control report records zero trace systems and zero
  optimization calls, not 54 feasible LP witnesses.

The full manuscripts state the mathematical eligibility hypotheses. The
programs receive full tensors, rather than census labels, as mathematical
inputs. The classification remains partial at multiplicities four through
eight; the exact remaining tensors are exported in
`data/unresolved_tensors.json`.

## Verification and provenance

`verification/round2/release_replay.json` records the final exact replay of every
accepted record from both continuations, with assertions disabled and SciPy
optimization disabled, and the resulting certificate and ledger hashes.
`verification/release_summary.json` gives the disjoint union and totals.
Derived CSV/JSON/model exports and paper tables are checked by
`software/release_consistency.py`; final PDF compilation and cross-reference
checks are separate from mathematical evidence.

The original 16,511-certificate file and the first seven-certificate continuation
are unchanged. Their existing exact evidence is inherited; a fresh full replay
of all original certificates is available but is not claimed for this turn.
Exact checks of the new proofs, controls and allocation are repeated here.

The standalone R3582 proof was matched against the entire R6_7_3582 tensor and
integrated through generic code. The supplied B13 proof is retained as a
comparison/control outside this census, not as a new rank-six multiplicity-eight
allocation. Source copies and the exact import audit are under
`research/round2_external/sources/` and `IMPORT_AUDIT.md`.

The previous revision notes are preserved at
`provenance/REVISION_NOTES_first_continuation.md`. Old research logs are
historical evidence and may name rings that were unresolved when they ran.
For current status use the decision ledger and this revision's paper.

`SHA256SUMS` covers every archived file except itself. The ZIP is checked for
CRC integrity and complete agreement with that manifest after construction.

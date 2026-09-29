# Revision notes — third continuation, 29 September 2026

## Result

This continuation adds **12 general exclusions**, reducing the inherited
22-case frontier to **10 unresolved rings**. The complete ledger has
**16,548 general exclusions and 54 realized rings**. The exact
multiplicity bands **1, 2, 3, 7** are complete. There are no new positive
identifications and no changes to the underlying census or identifiers.

| Exact multiplicity | Rings | Excluded | Models | Unresolved |
|---:|---:|---:|---:|---:|
| 1 | 39 | 18 | 21 | 0 |
| 2 | 154 | 132 | 22 | 0 |
| 3 | 384 | 381 | 3 | 0 |
| 4 | 872 | 866 | 2 | 4 |
| 5 | 1,582 | 1,580 | 1 | 1 |
| 6 | 2,768 | 2,763 | 3 | 2 |
| 7 | 3,814 | 3,812 | 2 | 0 |
| 8 | 6,999 | 6,996 | 0 | 3 |
| **Total** | **16,612** | **16,548** | **54** | **10** |

## New accepted general exclusions

| Tensor | General obstruction | Exact proof source |
|---|---|---|
| `R6_4_6` | Forced cyclic associator and Clifford rotation | [`research/round3/smallest/R6_4_6_certificate.json`](research/round3/smallest/R6_4_6_certificate.json) |
| `R6_4_211` | Full-character cyclotomic rotation and signed Galois reduction | [`research/round3/m4/R6_4_211_general.json`](research/round3/m4/R6_4_211_general.json) |
| `R6_4_243` | Low Verlinde and restriction-product constraints; signed reduction | [`research/round3/m4/R6_4_243_general.json`](research/round3/m4/R6_4_243_general.json) |
| `R6_5_638` | Integral Morita congruences and higher Clifford rotation | [`research/round3/higher/R6_5_638_general.json`](research/round3/higher/R6_5_638_general.json) |
| `R6_6_170` | Complete signed-sector exhaustion and weighted induction | [`research/round3/noncommutative/R6_6_170_certificate.json`](research/round3/noncommutative/R6_6_170_certificate.json) |
| `R6_7_200` | Complete signed-sector exhaustion and weighted induction | [`research/round3/noncommutative/R6_7_200_certificate.json`](research/round3/noncommutative/R6_7_200_certificate.json) |
| `R6_7_1225` | Integral Morita congruences and higher Clifford rotation | [`research/round3/higher/R6_7_1225_general.json`](research/round3/higher/R6_7_1225_general.json) |
| `R6_8_491` | Complete signed-sector exhaustion and weighted induction | [`research/round3/noncommutative/R6_8_491_certificate.json`](research/round3/noncommutative/R6_8_491_certificate.json) |
| `R6_8_6524` | Local dimension-field isolation and signed-spectrum saturation | [`research/round3/arithmetic/R6_8_6524_general.json`](research/round3/arithmetic/R6_8_6524_general.json) |
| `R6_8_6525` | Local dimension-field isolation and signed-spectrum saturation | [`research/round3/arithmetic/R6_8_6525_general.json`](research/round3/arithmetic/R6_8_6525_general.json) |
| `R6_8_6526` | Different ideal, abelian field exhaustion and signed saturation | [`research/round3/arithmetic/R6_8_6526_general.json`](research/round3/arithmetic/R6_8_6526_general.json) |
| `R6_8_6999` | Local dimension-field isolation and signed-spectrum saturation | [`research/round3/arithmetic/R6_8_6999_general.json`](research/round3/arithmetic/R6_8_6999_general.json) |

The canonical disjoint allocation is
`certificates/continuation_round3.jsonl`. Alternative proofs and new
confirmations of old exclusions are retained without double counting.
The first and second continuations contain 7 and 18 earlier exclusions;
their original files are unchanged.

## Mathematical advances

- **Cyclic associators:** the uniform cyclic order-four family forces an
  even parameter and a unique anticommuting module action. A trivial pointed
  associator is impossible in the positive cases at issue; its nontrivial
  class forces fourth-indicator support. Every remaining induction branch
  of the smallest multiplicity-four case is excluded. The realized parameter
  zero and two members are preserved.
- **Full character fields:** exact relative cyclotomic traces retain the
  character information lost by projecting to the FP field. Coupled Galois
  and modular equations settle `R6_4_211`; low Verlinde positivity and
  restriction products settle `R6_4_243`. Both include complete unrestricted
  signed reductions before the general conclusion.
- **Integral Morita equations:** an exact congruence annihilating every
  integer multiplicity column but not the right-hand side rejects branches
  that are feasible over the rationals. The remaining branches are covered
  by exhaustive higher Clifford-indicator certificates.
- **Local signed spectra:** central induction puts every original formal
  codegree in the categorical dimension field. Local factorization and
  cyclotomicity isolate that field, after which exact positive codegree
  enumeration saturates the signed Casimir bound. The split quadratic case
  additionally uses the different ideal and a finite abelian-field list.
- **Noncommutative sectors:** the remaining noncommutative inputs are split
  into both possible signed algebra types. The commutative sector is
  exhausted when necessary; the other sector has type C + C + M2(C).
  Its weighted codegree identity and trace bound force magnitude saturation,
  all sign tables are original gauges, and exact weighted induction rejects
  every pseudo-unitary branch.

The formal-codegree normalization in the reusable oriented helper was
corrected for a noncommutative source: a matrix block's Casimir eigenvalue
is twice its formal codegree. The audit confirms that every inherited
noncommutative exclusion already used the correctly weighted checker;
no old allocation changes. The new sector proof explicitly uses codegree12,
not the Casimir eigenvalue24.

## Coverage and the remaining frontier

`verification/round3/campaign_manifest.json` fixes all 22 starting tensors.
`research/round3/coverage.json` records the current allocation and the exact
scope of each scan. Tensor-family and arithmetic applicability scans include
all 16,612 census records. The expensive induction and Morita campaigns test
all 22 residuals and all 54 positive models, with eligibility, survival and
budget outcomes retained. Ineligible or unfinished positive controls are
reported explicitly and are not described as feasible witnesses.

The remaining tensors are exported in `data/unresolved_tensors.json`.
Exact strengthened witnesses for the two quartic multiplicity-four cases
show that those finite necessary systems survive; they do not construct a
category. Further field and induction reductions on other cases are retained
as research progress without changing classification status.

## Verification and revised deliverables

`verification/round3/release_replay.json` records exact checking of the new
canonical allocation with optimized Python and numerical optimizers disabled.
The criterion directories retain independent arithmetic audits, positive
controls, based relabelings and rejected certificate corruptions. The original
negative campaign and the preceding continuations retain their unchanged
source-bound evidence; the entire old catalogue is not claimed to have been
replayed again.

The JSON/CSV ledgers, residual tensors, derived counts, allocation tables,
main paper, verification guide and current documentation are regenerated.
`software/release_consistency.py` checks the agreement of the derived exports
with the authoritative ledger in normal and optimized Python modes. PDF
compilation and visual checks are separate from the mathematical certificate
replay. `SHA256SUMS` covers every archived file except itself; the ZIP receives
both CRC and complete manifest verification.

The previous notes are preserved in
`provenance/REVISION_NOTES_second_continuation.md` and
`provenance/REVISION_NOTES_first_continuation.md`. Historical logs remain
historical; use the current ledger for current status.

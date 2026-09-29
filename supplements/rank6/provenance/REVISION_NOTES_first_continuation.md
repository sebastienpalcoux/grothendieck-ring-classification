# Revision of 29 September 2026

## Result and limitation

This archive replaces the manuscript, guide, classification exports, relevant
software and checksums with a coherent revised release. The original source
census and original classification campaign are preserved as provenance.

There are **16,518 general exclusions, 54 categorifiable rings and 40 unresolved
rings**. Seven of the former 47 residuals are now excluded. There is no new
positive model. General categorifiability remains completely decided through
multiplicity two only.

**R6_3_215 is still unresolved. The requested completion of multiplicity three
has not been achieved.** Neither compatibility with modular data nor a
based-ring Morita completion has been presented as a categorical construction.

## New general exclusions

| Tensor | Necessary criterion | Main proof / implementation |
|---|---|---|
| R6_4_90 | Complete general character-induction certificate | Section 4; advanced_criteria.py |
| R6_4_146 | Complete general character-induction certificate | Section 4; advanced_criteria.py |
| R6_4_162 | Forbidden rank-three C2 near-group subring | Section 5; new_rank3_subring.py |
| R6_5_100 | Order-six Morita dual and faithful C3 grading | Section 5; new_morita_order6.py |
| R6_5_408 | Order-six Morita dual and faithful C3 grading | Section 5; new_morita_order6.py |
| R6_8_2945 | Spectral and parity constraints on the anti-invariant module | Section 5; new_module_spectral.py |
| R6_8_3071 | Spectral and parity constraints on the anti-invariant module | Section 5; new_module_spectral.py |

Every identifier is only an index into the frozen full tensor. The obstruction
functions receive the tensor, check their hypotheses, and reconstruct the
finite domain. General, pivotal, spherical, pseudo-unitary and unitary fields
remain distinct in the decision ledger.

The order-six argument exhausts 60 cyclic and four nonabelian dual-ring
possibilities. The surviving cyclic cases have a faithful C3 grading whose
neutral component contains the inverse Morita algebra. This forces a grading
on the original ring, contradicting its trivial universal grading. The
pseudo-unitary formal-codegree step is justified by the two-dimension Galois
reduction on the dual category, not assumed for the original category.

## Multiplicity-three investigation

A new signed-sphericalization reduction proves that every categorification
of R6_3_215 admits a spherical structure and has a pseudo-unitary Galois
conjugate. General existence is therefore equivalent to pseudo-unitary
existence for this ring. The unrestricted enumeration contains 1,480 signed
quotients in 63 sign-gauge orbits. One orbit consists of the 32 gauges of the
original table; every other orbit is rejected by 228 zero-dimension and 43
exact norm checks. No modulo-four indicator normalization is used. This is a reduction of the outstanding
problem, not a proof of existence or nonexistence; it implies no unitary
structure. The exact certificate and checker are in
research/new_frontier/frontier_spherical_reduction.json/.py.

The full Morita-action Gram theorem couples every right action matrix through
one integral Gram identity. For the forced algebra 1+g in R6_3_215, all 16
module branches are now accounted for exactly: two violate a rank bound,
twelve have integer Farkas certificates, and each of the remaining two has a
unique full action frame. Both dual tensors are based-isomorphic to R6_3_215.
This does not establish equivalence of the categories or create a new algebra
on 1+X for a noninvertible simple.

The rank-22 center witness now extends to a complete modular fusion tensor
from the known Grossman–Izumi cyclic-eight center. Its positive unital ring
map to the residual tensor satisfies 2,904 coefficient equations. The exact
checker also verifies 10,648 spectral fusion identities, associativity,
modular relations, dimensions and all second indicators over
Z[x]/Phi_136(x). Input validation and explicit arithmetic bounds prevent
acceptance of a zero map, malformed data or machine-integer overflow.

All 55,896 ordinary cyclic-rotation multiplicities for powers 1 through 136
also pass an exact indicator audit. These are necessary compatibility data.
An algebra lift is an additional categorical requirement. A separate proof
now excludes lifting this specified restriction map from the actual known
cyclic-eight center: the forced Morita module, involution condensation and
a second small algebra give a dimension-square contradiction. The proof
retains the actual source-category and supplied-induction-data hypotheses.
It does not identify all braided categories with equal modular data or
exclude arbitrary categorifications of R6_3_215. All 4,752 generalized
rotation multiplicities through power eight also pass their exact audit,
illustrating the limit of these numerical necessary conditions. The earlier braided-spherical exclusion remains scoped to
braided spherical categories and does not decide general existence.

Additional scoped investigations and their limitations are retained in the
research directories, including the congruence branch analysis and the
order-four pointed-associator constraint.

## Application across higher multiplicities

The rank-three subring criterion was run on all 16,612 census tensors. It
applies to 257 excluded tensors, with R6_4_162 the one new residual exclusion.
The full Morita-action scan covers all 47 original residuals: 21 are eligible
and 26 are outside its implemented hypotheses; it produces no additional
whole-ring exclusion. All 54 known positive rings pass its controls.

The supplementary campaign repeats module-dual Gram, dimension-order,
character-induction, tensor-rotation and modular tests on every one of the
47 original residuals, including every residual in multiplicities 4 to 8.
Each search has an explicit process budget. The saved outcome distinguishes
an accepted exact certificate, a surviving relaxation, ineligibility and an
exhausted budget. None of the latter three proves nonexistence. The complete
campaign outcome is recorded in verification/continuation/summary.json.

A further saturation audit covers all 46 original multiplicity-4–8 residuals.
Integral module-Gram searches complete on 14 inputs, with 26 inapplicable and
six timed out. Simultaneous commuting dual-action searches complete on 18,
with 26 inapplicable and two timed out. They give no further exclusions.
Sixteen completed full-action cases force the original rank-six dual tensor.
The separate canonical E6 algebra condensation in R6_6_1035 also reconstructs
the original tensor. These exact results and their finite budgets are in
research/higher_continuation/.

The residual counts after this continuation are:

| Multiplicity | Before | After |
|---:|---:|---:|
| 3 | 1 | 1 |
| 4 | 15 | 12 |
| 5 | 4 | 2 |
| 6 | 3 | 3 |
| 7 | 5 | 5 |
| 8 | 19 | 17 |
| Total | 47 | 40 |

## Verification and reproduction

All seven newly accepted exclusions were checked in normal Python during
allocation and independently under python -O, with numerical optimization
disabled. The order-six domain and mutation controls pass in both modes.
The current ledger, CSV exports, model catalogue, classification tables and
OEIS count exports pass the release-consistency checks in both modes.
The complete center and multiplicity-three Morita records have independent
optimizer-free exact replays.

The original 16,511 accepted negative certificates are unchanged and retain
the original campaign's exact checking evidence. This continuation does not
claim a fresh full replay of those unchanged certificates. For a fresh full
check use verify.py; for the incremental check use:

```bash
python -O software/continuation_controls.py --jobs 3
python research/new_frontier/verify_frontier_full_morita.py
python research/center_continuation/exact_cyclic8_center.py
python research/model_continuation/replay_morita_order6.py
```

To refresh the accepted continuation from discovery checkpoints and rebuild:

```bash
python software/release.py --freeze-and-build
python software/build_paper_tables.py
python build_papers.py
```

The separate frozen continuation input prevents rerunning a scan on the
shrinking final residual list. PDFs are published only after all TeX passes
complete. The final SHA256SUMS records every archived file except itself.
The census is trusted at the original pinned revision; it was not enumerated
again, and no statement is made about multiplicity above eight.

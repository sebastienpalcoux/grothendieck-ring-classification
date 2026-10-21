# Further rank-eight research: a generalized Haagerup model and unified restrictions

This stage realizes **R8_3_721** by an actual inherited Q-system construction.
The exact-multiplicity-three inventory becomes **3,504 exclusions, 15 unitary
models and 8 unresolved rings**. Through multiplicity three the totals are
**4,400 exclusions, 92 unitary models and 8 unresolved rings**.

The original frontier ledger, its 25 additional exclusions, and both complete
108-check replay receipts are preserved. This directory contains a separate
stage. Reviewable arithmetic proofs and categorical arguments are distinguished
from exploratory scripts; filenames containing `probe` are not by themselves
evidence that a proposed obstruction succeeded. Consult the individual notes.

## The new model

Let C be the C2 de-equivariantization of the existing generalized Haagerup
category for C8 in Grossman--Izumi, arXiv:1501.07679v2, Example 4.4 and Section 6.
The image of its Q-system is the connected separable algebra A=1+rho. Then

    B = A-bimod(C)

is an actual unitary fusion category. A uniform conjugation argument for these
cyclic generalized Haagerup Q-systems proves that B has no nontrivial
invertible object. Complete free-bimodule Gram factorization and the known
center force rank eight. Exact rational inequalities then bound every fusion
coefficient by three, for all four possible duality choices. An exhaustive
exact scan of all 4,500 supplied tensors identifies its dimension type uniquely
as R8_3_721.

The last step uses completeness of the supplied census; the enumeration itself
was not independently rerun. This identifies the constructed category's ring
by a finite bound and census uniqueness. It does not claim to have independently
extracted its full tensor from analytic intertwiner calculations, or to have
proved novelty of the category.

- [Categorical construction and uniform lemma](models/R721_QSYSTEM_CONSTRUCTION.md)
- [Independent categorical review](review/R721_CATEGORICAL_REVIEW.md)
- [Complete bimodule rank argument](semion_fermion/construction/PROOF.md)
- [Exact coefficient certificates](models/r721_dual_multiplicity_bound.json)
- [Independent coefficient reconstruction](quadratic/r721_bound_review.json)
- [Complete census comparison](r721/census_dimension_crosswalk.json)
- [Accepted model record](models/consolidated_models.json)

## Remaining cases and what changed

| Ring | Established new progress | Remaining question |
|---|---|---|
| R8_3_65 | Complete based-module action list; a pointed-subgroup Morita obstruction excludes a trivial C4 associator and both rank-two categorical module possibilities. | A category with one of the permitted nontrivial associators, or an obstruction covering them. |
| R8_3_928 | Charged fourth-moment equations force pair-product sectors and have exact feasible completions for all ten retained allocations. | Complete center/associator coherence or a further obstruction. |
| R8_3_941 | Fermionic pair-product equations have a unique positive completion of the relevant sector, compatible with all fourteen retained allocations. | Complete center/associator coherence or a further obstruction. |
| R8_3_982 | Two induction frames are excluded exactly. The remaining common semionic branch survives a joint integral-core and rational-phase system, including the full phase domain and joint Galois constraints. | A coherent center and category, or an additional exact obstruction. |
| R8_3_1154 | Fourth moments, fusion-action reconstruction, an induction trace and a negative-diagonal obstruction reduce 292 center patterns to three. A separate Morita argument forces the pointed C2 associator to be nontrivial. | A simultaneous center-action completion and categorification, or exclusion of all three patterns. |
| R8_3_1768 | Complete connected-algebra object, internal-end and Morita-dimension-profile filters substantially reduce possible module data; specified affine Lie construction families are excluded uniformly. | Actual algebra/module coherence and a category, or a further obstruction. |
| R8_3_1795 | The same complete connected-algebra and Morita closure methods reduce candidate module data. A potential Morita comparison with R1154 is only a search direction. | Actual algebra/module coherence and a category, or a further obstruction. |
| R8_3_3472 | Complete Gram, internal-end and Morita-profile constraints reduce candidate module data, with exact action checks when forced. | Actual algebra/module coherence and a category, or a further obstruction. |

All eight remain unresolved. These are extensively investigated candidates in
the documented operational sense; this does not assert their categorifiability
or that a future realization would be new. Surviving integer or modular data
are necessary conditions, not associators.

## Proof packages

- `models/`: actual R721 construction, independent reviews, and scoped model
  searches and Morita reductions, including the R1154 rank-five dual obstruction.
- `r721/`: full modular-data analysis, exhaustive census comparison, and
  independent reviews of the R1154 action and trace obstructions.
- `r1154/`: complete finite moment enumerations, action constraints and exact
  rejected-pattern certificates. Large enumerations are compressed with receipts.
- `r982/`: exact frame certificates and surviving joint necessary-condition data.
- `quadratic/`: complete Gram and Morita closure, the R65 pointed-associator
  obstruction, and independent model verification.
- `semion_fermion/`: charged fourth-moment constraints, complete finite pair
  completions and independent quadratic-package review.
- `review/`: independent arithmetic and categorical checks performed separately
  from the producing workstreams.

The scripts use exact arithmetic for accepted contradictions and identities.
Numerical optimization proposes certificates or witnesses; acceptance requires
the specified exact reconstruction. No unsuccessful numerical search is
promoted to an exclusion. Independent expert review and formalization remain
separate from these computational checks.

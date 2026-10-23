# Rank-ten multiplicity-one: the six previously unresolved cases

Research date: 23 October 2026. This is a research package for the subsequent
repository/manuscript/website revision. No online files were changed in this
research turn. The original catalogue and earlier research are retained as
inputs; the new decisions are in `classification_updates.json`.

## Result

**Five excluded over the complex numbers; no new models; one unresolved.**

| Case | Decision | Argument |
|---|---|---|
| R10_1_114 | Excluded | Ordinary rank-four factors; the two possible swap descents have either multiplicity two or invertible group C2 x C2, whereas the input has C4. |
| R10_1_115 | Excluded | The same ordinary-factor obstruction. |
| R10_1_152 | Excluded | Pseudo rank-four factors force a forbidden odd-evaluation rank-two superfusion rule. |
| R10_1_153 | Excluded | The same pseudo-factor obstruction. |
| R10_1_179 | Excluded | The same pseudo-factor obstruction. |
| R10_1_189 | Unresolved | New pointed-associator and Morita restrictions; no valid exclusion or model. |

The five exclusions concern arbitrary complex fusion categorifications,
not only unitary or braided ones. These are new deductions in this project
using existing categorical results and the explicit input tensors.

## Uniform reduction for the five quadratic cases

Put delta=1+sqrt(2). All five rings have dimension type
1^4,(2delta)^2,(delta^2)^4. A distinguished involution h fixes the two
2delta-dimensional simples. Its stabilizer supplies the algebra 1+h.
An odd-coefficient parity argument forces the left h-action on all eight
simple right modules to be trivial. The Morita dual consequently has
sixteen simples, of dimensions 1^4,delta^8,(delta^2)^4.

The eight-dimensional module action is forced. Its rational commutant,
the Perron bound B_ij <= 33, and the sign involution determine all sixteen
dual simple action matrices. Associativity determines the remaining
ambiguous products. These are exact finite linear and integer checks,
not a numerical search for associators.

The dual's rank-eight adjoint subcategory contains two rank-four factors
sharing 1,f. A new relative-factorization argument proves that they
coherently commute: the complementary bimodule is a twisted regular
module, and its projected multiplication supplies a twisted-central
1+f whose unit summand trivializes the twist. The common f acts freely,
so this summand argument is justified. Trivial universal grading makes
the resulting relative half-braidings unique. The canonical odd
involution interchanges the factors. Their central self-braidings are
both inverse and equal, hence q^2=1.

Read, in order:

1. `new/quadratic_obstructions/MORITA_REDUCTION.md`
2. `new/quadratic_obstructions/REDUCTION_AUDIT.md`
3. `new/rank16_dual/RELATIVE_FACTORIZATION.md`

The exact tensors use the endofunctor-composition convention, opposite
to literal A-bimodule multiplication. The proofs state and handle this
convention explicitly.

## Ordinary branch: 114 and 115

The earlier exact sphericalization/Galois reduction permits passage to a
pseudo-unitary categorification. Pseudo-unitarity is preserved by Morita
equivalence, so the rank-four factors are pivotal. Etingof--Ostrik's
Theorem A.3 identifies them with quantum SO(3) categories at primitive
sixteenth roots. Relative factorization and central-algebra descent give
the diagonal-boson quotient of two equal factors.

There are exactly two possible algebra lifts of factor interchange,
given by the signs on (f,f). The plus lift produces a coefficient 2.
For the minus lift, a direct balanced tensor calculation gives invertible
group C2 x C2. Both input rings have C4. These alternatives exhaust the
possible actions, including their coherence; they are not merely two
unsuccessful model guesses.

Full proof: `new/quadratic_models/ORDINARY_FACTOR_EXCLUSION.md`.
Independent review: `new/rank16_dual/ORDINARY_DESCENT_AUDIT.md`.

## Pseudo branch: 152, 153 and 179

Here the rank-four factors have x*=fx and x^2=f+x+fx.
The q=+1 alternative would condense to the forbidden ordinary rank-two
ring W^2=1+2W. The q=-1 alternative supplies a central fermion. Its
standard associated superfusion category has two m-type simples and
the odd-evaluation rule W^2=Pi 1+(1+Pi)W.

Chang--Chen--Xu explicitly exclude this particular finite superpentagon
system, their odd family with parameters (1,1). Their separate conjecture
about unbounded rank-two superfusion classification is not used. This
published finite Groebner calculation is a literature input; it was not
independently rerun here. The categorical reduction to that exact family
and its applicability without unitarity were independently audited.

Full proof: `new/rank16_dual/PSEUDO_BRANCH_EXCLUSION.md`.
Independent source audit: `new/pseudo_psu_central_fermion_audit.md`.

## Case 189: precise remaining problem

Its normal form is

    g^5=1, gx=xg, x*=x,
    x^2=1+(g+g^2+g^3+g^4)x,   FPdim(x)=2+sqrt(5).

The new pointed-associator theorem proves that any categorification has
untwisted pointed subcategory Vec(C5). A nonzero associator would force
primitive 25th-root twists in pointed induction. Modular Galois symmetry
then forces groups of five equal restriction vectors. Seven complementary
subset patterns give a negative principal Gram minor; the eighth would
give five central lifts of the same invertible, impossible because the
universal grading is trivial.

The regular algebra sum(g^i) therefore exists. Its Morita dual must have
the same based ring, even without assuming that dual is multiplicity free:
the dimension-compatible alternatives are excluded by rank-two
categorification and exact formal-codegree field arguments. This is
based-ring self-duality, not a proved tensor equivalence. A braided model
is excluded by the existing irrational generalized-near-group theorem.

No argument here excludes the remaining nonbraided, untwisted case, and
no categorical model was constructed. Integer Gram witnesses do not
constitute models. The unresolved status must be retained.

Read `new/case189/POINTED_ASSOCIATOR.md`, `MORITA_REDUCTION.md`, and
`STRUCTURAL_PROGRESS.md`. The latter also records the finite necessary
twist-order bound and unsuccessful necessary-condition searches.

## Verification and replay

The exact module and dual computations were replayed by their author and
independently inspected. The parent reviewer additionally replayed the
five input hypotheses, all six dual tensors (including control 21), all
rank-four/swap/factorization hypotheses, the existing model-21 balanced
tensor calculation, the exact sphericalization/Galois receipts for
114,115,189, and all three case-189 verifiers. All passed.

The stored checks include 48 affine commutant systems, 256 action-product
equations and 4096 associativity equations per dual tensor. The proofs
explain why those finite checks exhaust the necessary possibilities.

For a full reconstruction, run the following in order from this directory
with Python, SymPy and NumPy installed:

    python new/quadratic_obstructions/parity_morita_reduction.py
    python new/quadratic_obstructions/module_action.py
    python new/quadratic_obstructions/commutant_candidates.py
    python new/quadratic_obstructions/dual_products.py
    python new/quadratic_obstructions/complete_dual_tensor.py
    python new/rank16_dual/verify_subcategories.py
    python new/case189/verify_structure.py
    python new/case189/verify_pointed_associator.py
    python new/case189/verify_morita_reduction.py
    python prior/rank9_rank10_m1_20261023/work/audit_new_models/verify_model21.py

The earlier general signed verifiers and their instructions are retained
under `prior/rank9_rank10_m1_20261023/work/general_signed/`.
The optional `central_filter.py` and `full_gram.py` are unsuccessful
obstruction explorations, not dependencies of the exclusions. SciPy is
needed only for the latter discovery search.

## Primary literature used at the decisive steps

- Etingof--Ostrik, *On semisimplification of tensor categories*, Appendix A,
  Theorem A.3: https://arxiv.org/abs/1801.04409 .
- Bruguières--Natale, *Exact sequences of tensor categories*, Corollary 5.6:
  https://arxiv.org/abs/1006.0569 .
- Ostrik, *Fusion categories of rank 2*:
  https://arxiv.org/abs/math/0203255 .
- Usher, *Fermionic 6j-symbols in superfusion categories*, Definition 4.9:
  https://arxiv.org/abs/1606.03466 .
- Chang--Chen--Xu, *Topological defect lines in two dimensional fermionic
  CFTs*, Section 3: https://doi.org/10.21468/SciPostPhys.15.5.216 .
  The corresponding arXiv v4 discussion is equation (3.2), page 25:
  https://arxiv.org/abs/2208.02757 .
- Schopieray, *Categorification of integral group rings extended by one
  dimension*: https://doi.org/10.1112/jlms.12789 .
- Schopieray, *Irrational braided generalized near-groups*:
  https://doi.org/10.4153/S0008439523000334 .

Further exact source locations appear in the individual proofs. Copies
of downloaded third-party papers are omitted from this package. The
2026 numerical inventory of low-rank complex categories is not used as a
completeness theorem.

## Handoff for the later online revision

Apply the five general-complex exclusions in `classification_updates.json`
to the existing ordered rank-ten census. Keep 189 unresolved and replace
its old deferred-work note with the proved necessary conditions above.
Update manuscripts, both repositories and their website sections only in
the later revision requested by the user. Preserve the established clean,
uniform rank ordering; these cases do not require a separate website section.

The old decisions inside `prior/` and `catalogue.json` are historical
snapshots. They intentionally remain unchanged; the new delta supersedes
them only for the six listed cases.

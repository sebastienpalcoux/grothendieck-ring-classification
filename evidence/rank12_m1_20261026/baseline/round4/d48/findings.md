# Dimension-48 audit and continuation

All work is offline. No prior-round files or online repositories were changed.

## Prior decisions checked

The actual category data and complete tensor identifications for R414/R531 pass a fresh replay of the prior standalone verifier with Python -O. The earlier ordinary group-theoretical models R25/R30/R417 and the relative A4xC2 models R351/R513/R428/R597 pass `audit_earlier_models.py`; their receipt records actual subgroup algebra/cocycle premises and exact source hashes. No positive-model correction was needed.

## Exhaustive conditional group-theoretical classification

The previous 23-pair necessary-condition reduction is rechecked in `audit_possible_twisted_types.g/log`. Eleven Sylow16 pairs have normal C3 and are eliminated uniformly by the argument in the round3 proof, refreshed by `audit_sylow16_checks.g/log`. For the other two Sylow16 pairs, the full 12 subgroup Schur classes are checked. The ten H4/H8 pairs have complete relative cohomology coverage, with actual cocycles, Schur representatives, and exact subgroup-triviality certificates.

All 104 admissible categorical cases are independently verified: 42 wrong-rank cases, 16 cases with an explicit multiplicity greater than one, and 46 multiplicity-one cases. The latter give exactly R30, R417, R414 and R531. See `cohomology_coverage.md`, the frozen data and the independent audit receipts referenced there. This rules out a group-theoretical model for every remaining D48 input; it does not by itself rule out general categorification.

## New categorical lemmas

- `ng24_lagrangian_lemma.md`: every C2-equivariantization of an arbitrary complex near-group category of type (D8,2) or (Q8,2) is group-theoretical. The proof uses the full unitary classification with the general-complex unitarity bridge, followed by the three-Lagrangian center argument. The near-group categories themselves exist; the old blanket conditional rejection was incorrect.
- `triality_soft_automorphisms.md`: the non-group-theoretical dimension-twelve triality categories have no nontrivial soft tensor autoequivalences; their tensor automorphism groups embed into S3. Every equivariantization by a group of order four retains a coefficient two. The complete four-dimensional F2 arithmetic is in `triality_orthogonal.py/json`; the graded-functor premise is explicitly grounded in Edie-Michell's equivalence classification.
- `triality_gt_branch.md`: the three group-theoretical categorifications of the same dimension-twelve triality ring have exactly three central Lagrangians. Every equivariantization by a 2-group is group-theoretical. Combined with the preceding lemma, any order-four equivariantization of a category with those triality rules is either group-theoretical or has multiplicity greater than one.

All twenty remaining D48 rings are now excluded from arbitrary complex categorification. The final proof is `general_complex_exclusion.md`; the per-row decisions and all56 central-involution branches are in `results.json`.

The decisive new binding checks do not assume completeness of the supplied census. `quotient_reconstruct.py` reconstructs every rank-twelve dimension24 quotient using at most three binary variables, finding only R351/R513. `rank9_reconstruct.py` reconstructs every rank-nine quotient using at most eight bounded integer variables. Four source rows have no such quotient; the two surviving quotient rings have a unique central boson and a pointed second de-equivariantization, so their outer equivariantizations are group-theoretical. The free rank-six and near-group alternatives are closed by their separate categorical lemmas. Thus every possible central quotient forces group-theoreticity, contradicting the complete conditional classification.

Both reconstruction scripts and their categorical premises have independent PASS audits. The portable frozen inputs and utilities are `quotient_inputs.json` and `ring_utils.py`. The complete proof/evidence index and hashes are in `accepted_manifest.json`. No D48 input remains unresolved, and no new model was added in this round.

## Reproduction and independent receipts

Use `python -O restriction_certificates.py`, `python -O triality_orthogonal.py`, and `python -O audit_h16.py` from any working directory. Discovery and freeze scripts use paths relative to their own files and do not write to prior rounds. Exact frozen evidence is `gt_classification_frozen.json` and `h16_all_cases.json`.

Independent receipts live in `../audit_exclusions/audit_d48_cohomology.*`, `audit_d48_groups.*`, `audit_d48_followup.md`, `audit_NG24_lagrangians.md`, and `../audit_models/d48_catalog_independent.json`, `h16_catalog_independent.json`. The independent full-Hom reconstruction does not import the discovery character-projection code.

# Rank12 quadratic families: fourth-pass audit and continuation

## Classification outcome

R12_1_332 is newly excluded from categorification by arbitrary complex fusion
categories. R12_1_561, R12_1_623 and R12_1_628 remain unresolved. No new model
is claimed. The earlier R12_1_350 exclusion is confirmed, not counted twice.

## Audit of the accepted results

The frozen, optimizer-free round3 replay was copied into audit/ and rerun with
Python -O. It passed all32 R350 Farkas cases, all exact low/high-column domain
checks, and the R623/R326 indicator controls. Neither rank6 repository imports
nor disabled assertions are used by that replay. The theoretical audit retains
the distinction between an arbitrary complex category and a pseudo-unitary
Galois conjugate; published Schopieray Lemma3.1 is the applicable theorem.
No completeness claim about unitary Haagerup categories is needed.

For R623, the accepted conclusion is nu_2(z)=-1 in the pseudo-unitary conjugate,
equivalently a nontrivial pointed associator on C2. The corresponding restriction
on the ordinary C2 cohomology class also holds in the original category: its
two cohomology classes are fixed under every Galois automorphism. This is not
an assertion that the original pivotal structure has positive dimensions.
It does not by itself exclude the ring. The positive R326 control has
nu_2(z)=+1 despite its central fermion, as required.

The existence premise for R326 was checked against Grossman-Izumi,
https://arxiv.org/html/1501.07679v2, Section2.4 and Example4.5. The two C6
Haagerup categories themselves are supplied by exact construction data in
solutions.nb; the numerical/conjectural qualification concerns their additional
center modular data. No assertion of a numerical category construction is used.

## New exclusion: R332

R332_proof.md gives an actual coherent C2 action on the neutral Haagerup-C3
category by conjugation with the existing odd invertible. Pointed associator
scalars cancel between a conjugating object and its inverse dual, so there is
no hidden untwisted-associator assumption. Every possible equivariant fusion
ambiguity is covered and yields the same rank6 ring R6_4_260.

An explicit character has formal codegree5+sqrt(5), while the equivariantized
category would have global dimension39+9sqrt(13). The required central simple
dimension has field norm13689/25, so it is not an algebraic integer. This is an
elementary contradiction independent of prior rank6 exclusion certificates.

verify_R332.py and R332_frozen.json provide a standard-library replay of full
tensor bindings, both characters and the norm obstruction. An independent
agent audit in ../audit_exclusions/audit_R332.md and audit_R332.py accepted the
categorical action, all fusion ambiguities, the scope, and the exact replay.

## Stronger necessary conditions on the three remaining rings

C3_central_lift.md proves that R561/R628 force an actual central braided C3
lift. The argument uses genuine inner C3 equivariantization, exhausts72 tiny
section refinements of its based ring, and excludes66 by exact character norms.
All six remaining sections are subgroup sections; the adjoint subcategory maps
tensor-equivalently back to the original category. Canonical central lifts from
equivariant structures then transfer to the original C3. Trivial universal
grading makes these half-braidings unique and proves braided closure.

This replaces the previous missing central-lift premise, but a Tannakian lift
has not yet been forced. The two possible nondegenerate C3 braidings remain.
The Tannakian case is excluded by the already-replayed rank4 quotient arguments.
Plain Müger splitting inside a nonbraided ambient category would be invalid;
no such step is used. The arithmetic and central-lift argument were independently
reviewed, with this isotropy gap explicitly retained.

R623_central_semion.md gives the parallel inner-C2 reduction, now with only64
sections per pointed square term and no arithmetic search. It forces a central
semion lift of z, compatible with the audited nontrivial C2 associator. A further
central-duality argument reduces its induction data to thirteen exact integer
profiles (R623_semion_profiles.md). Strong bounded trace tests did not eliminate
every profile. The ring remains unresolved.

## Attempts that were not promoted to conclusions

- The trivalent-category route to R332 was replaced by the stronger actual
  equivariantization proof. No claim that every Haagerup category is generated
  by a trivalent vertex is needed.
- Known twisted Haagerup precursors arise from near-group C9+9. Merely having
  such a precursor does not provide a required automorphism or algebra.
- Central nondegenerate pointed subcategories do not automatically split from
  nonbraided categories. Free pointed action may add a useful restriction, but
  an additional theorem is required; it has not been inserted as an assumption.
- Failed Farkas separation is not a model or a certified primal feasibility
  result. The semion probes are research records only.
- No new unitary-classification completeness claim was used to exclude a general
  complex category, and no proposed algebra was treated as existing on the
  strength of a based-ring match.

## Portable checks

All of the following passed with Python -O:

    audit/verify.py
    verify_R332.py
    verify_R623_duality.py
    verify_C3_sections.py
    verify_R623_C2.py
    verify_R623_profiles.py

The first is the complete prior accepted packet replay. The remaining scripts
check the new exact structural statements. Research probe scripts are separate
from these portable verifiers. Every file in this pass is newly written under
rank12-m1-round4-20261026/c6. No prior artifact, repository, or website was edited.

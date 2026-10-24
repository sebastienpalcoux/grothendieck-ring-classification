# Phase-three group-theoretical research: accepted results and boundaries

## Accepted results

1. R9_2_92 has the explicit unitary model
   C(S5,sign∪Schur,S3×C2,ψ), with a fully specified relative cocycle and all 729
   coefficients matched. Canonical record: `models.json`. Proof:
   `S5_RELATIVE_TWIST.md`. Independent audit:
   `../audit_models/S5_RELATIVE_TWIST_AUDIT.md`.
2. The independent structural audit accepts the general-complex exclusions
   R9_2_907, R9_2_1071, R9_2_1724, R9_2_1356, R9_2_1933. It rebuilds tensor
   hypotheses from the original compressed input and checks the categorical
   arguments and subgroup/module-category alternatives. Records are in
   `../audit_structural/`. These proofs do not use absence from the formerly
   incomplete lower-positive registry.
3. The independently constructed dimension-48 models R9_2_392 and R9_2_1246
   both pass my separate categorical, cochain, and complete tensor audits.
   Canonical ownership remains `../integral_theory/models.json`; these are not
   duplicated in this directory's model list. The audits are
   `../audit_models/D48_RELATIVE_TWIST_AUDIT.md` and
   `../audit_models/D48_EXOTIC_RELATIVE_TWIST_AUDIT.md`.

## Remaining dimension-120 targets R9_2_12 and R9_2_959

No new model or general exclusion is claimed for either target.

The successful fixed pair G=S5, H=S3×C2 cannot produce either target just by
varying the trivializing two-cochain ψ while keeping the successful ω fixed.
Indeed, H²(H,C×)=C2: the nontrivial class is the cross term between the two
abelianization characters. The Schur two-cocycle of S5 restricts to that class,
as witnessed by the nontrivial lifted commutator of the two disjoint
transpositions. Thus every two-cocycle change of ψ extends to a global
two-cocycle of G. The resulting identity-on-objects tensor autoequivalence of
Vec_G^ω identifies the two algebra/module constructions. All such ψ choices
therefore have the same based ring as R9_2_92. Also, R9_2_959 has cyclic
invertibles C4, whereas the identity double coset supplies Rep(S3×C2), whose
four invertibles form V4.

This argument does not exhaust other three-cocycle classes or other finite
groups and subgroups. In particular, no negative conclusion is inferred from
the old complete untwisted group scan. No new untwisted scan was run.

The recent primary reference Li Dai, *Frobenius property for fusion categories
of dimension 120*, Rev. UMA 68(2) (2025), 395–403, DOI
10.33044/revuma.4390, was checked. Its Lemma 3.2 gives a nontrivial symmetric
subcategory in the center because these rings contain a dimension-12 fusion
subcategory. Lemma 3.1 gives weak group-theoreticality if that symmetric
subcategory can be strengthened to a nontrivial Tannakian one. The available
argument does not justify that strengthening here: Lemma 2.5 assumes an odd
number of invertibles, while these rings have four. Consequently the paper
does not supply a missing classification or exclusion.

Primary source: https://inmabb.criba.edu.ar/revuma/pdf/v68n2/v68n2a03.pdf

## Remaining dimension-168 target R9_2_1965

No general exclusion or model is claimed. The exact ring is noncommutative,
has central invertible group C2 and trivial universal grading, and contains
the ordinary Rep(S4) based subring. The based subring alone does not establish
that an arbitrary categorification of that subcategory is tensor equivalent
to Rep(S4).

There is a useful bounded obstruction to the most immediate group-theoretical
route: neither conjugacy class of S4 subgroups in G=PSL(2,7) yields a new
relative-cocycle model for R9_2_1965.

For H=S4, restriction H³(G,C×)→H³(H,C×) is injective. To see this, use
H³(-,C×)≅H⁴(-,Z). Restriction followed by corestriction multiplies by [G:H]=7,
so its kernel is 7-primary. Restriction to a Sylow C7 is injective on the
7-primary part. Its image must be invariant under the normalizer C7⋊C3. An
order-three normalizer element acts on H⁴(C7,Z)=C7 by multiplication by 2 or
4 (the square of its action on H²), whose fixed group is zero. Thus G has no
7-primary H⁴, proving the restriction claim.

Consequently an admissible ω can be globally gauged to 1. The Schur multiplier
of H is C2, and its generator extends from G: the Schur double cover of G has
a nontrivial commutator on a commuting pair in either H. Hence every remaining
ψ also extends globally and can be removed by a tensor autoequivalence. Both
routes give the already known untwisted ring R9_2_1557, not R9_2_1965.

The small exact group check `psl168_relative_bound.g` confirms order 168,
normalizer order 21, automorphism exponents {1,2,4}, both S4 subgroup classes,
both Schur multipliers C2, and nontrivial restricted Schur commutators. The
untwisted full tensor matches for the two subgroup classes were already saved
in `../../phase2/group_models/matches.json`.

This rules out only the specified (PSL(2,7),S4) route. It neither proves all
categorifications group-theoretical nor exhausts every other possible group
presentation. In particular, a conditional solvability descent was considered
but was not promoted because the required starting solvability/central
Tannakian hypothesis was not established.

## Replay boundary

The large prior untwisted search remains recorded in
`../../phase2/group_models/search_summary.json`: all 873 groups at the selected
dimensions were scanned then. Those results are useful search bounds, never
exclusion certificates for twisted group-theoretical or arbitrary fusion
categories. The present positive cocycle constructions demonstrate why this
distinction matters. No online files or baseline classification were changed
by this research subtask.

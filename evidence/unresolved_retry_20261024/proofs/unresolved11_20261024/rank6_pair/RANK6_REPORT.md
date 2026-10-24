# Rank-six research report, 24 October 2026

Both R6_4_155 and R6_8_1660 remain unresolved. This pass establishes a new categorical extension obstruction and an exact cross-rank identification; neither is a categorification or an exclusion of either rank-six ring.

## New categorical consequence for R6_4_155

Every complex-linear tensor autoequivalence of a categorification fixes its four invertible simple classes. The reason is categorical: the pivotal structure and each invertible's central lift are unique, and the four central twists are pairwise distinct. The already published frontier proof establishes the lift/twist premise; this pass isolates its consequence for extensions.

An invertible object of a larger fusion category that normalizes this subcategory therefore centralizes its Klein-four pointed group. In particular, no faithful C2 extension of R6_4_155 can have pointed group D8. The proof, precise general scope, Galois argument covering arbitrary complex categories, and equivariantization corollary are in `POINTED_AUTOMORPHISM_OBSTRUCTION.md`. The associated ring/group checker passes. The rank-nine noncommutative investigation is checking this obstruction against a previously surviving Morita branch.

The distinction between ring and tensor automorphisms matters: the ring admits four automorphisms, two of which swap the two semionic invertibles. Those two cannot lift to tensor autoequivalences. A hypothetical coherent C2 action therefore fixes all four invertibles, giving eight invertibles in its equivariantization, rather than the four in the current rank-nine dimension type.

## Exact identification of R6_8_1660's possible rank-eight Morita dual

The published full-center/Morita theorem leaves one possible rank-eight dual after the second-indicator obstruction. This ring is exactly R8_3_941. In `dual_actions_receipt.json`, take type `III_same`, solution zero. The permutation from its basis to the census basis of R8_3_941 is

    [0, 3, 6, 7, 4, 5, 2, 1].

`verify_r941_morita_identification.py` verifies all 512 structure constants and records hashes in `r941_morita_identification_certificate.json`. This strengthens the previous unnamed rank-eight alternative to an explicit link between two current frontier cases.

The implication remains conditional: a categorification of R6_8_1660 admitting the indicated nonpointed module category would have a Morita partner categorifying R8_3_941. No argument forces that module category, and no proof identifies the existence questions themselves. The guaranteed pointed algebra of R8_3_941 gives a different rank-eight dual and does not supply this rank-six route.

## Laptop feedback audit

The supplied R6_mult4 archive contains 29 verification reports. None passes its numerical tolerance, and none supplies an exact certificate. The smallest maximum pentagon residual is 0.5052494246948446, at branch 020. The campaign state explicitly calls the run an incomplete heuristic unitary search. Accordingly it supplies neither a model nor an exclusion, including for arbitrary complex categories. The extracted summary is `laptop_campaign_summary.json`.

## Previously established restrictions retained

For R6_4_155, the complete necessary modular centralizer has rank 26; its exact modular equations, nonnegative integral Verlinde coefficients, Vafa equations, higher rotations and fermionic Clifford restrictions already pass. Direct closure of its fusion tensor yields precisely four fusion subrings, of ranks 1, 2, 16 and 26; the rank-16 one is the fermion centralizer. Thus this tensor hides no smaller excluded nonpointed fusion subring. The canonical intermediate condensation was already proved to return C tensor Rep(C2), and does not produce the desired near-group exchange action. Known near-group constructions and the recent V4-quadratic classification were checked; the latter explicitly retains R'(4).

For R6_8_1660, the current domain still consists of 640 labelled necessary phase profiles, with fully determined indicator period dividing 48. The complete necessary Morita list is the original ring, the displayed rank-six Ad(E6)-based ring, and now explicitly R8_3_941. No associators or a compatible complete center are supplied by those profiles. The Ising-containing braided route and generalized-near-group dimension routes were already excluded.

No repository or website was changed in this research pass.

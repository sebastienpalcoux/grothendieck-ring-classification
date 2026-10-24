# Rank-nine multiplicity two: fourth research continuation

Research date: 24 October 2026. Online revision is deferred.

**Nine of the eighteen previous unresolved rank-nine rings are settled:
six general-complex exclusions and three explicit unitary models.** The new
exact-multiplicity-two partition is **2,039 excluded, 35 modeled, and
9 unresolved**, out of 2,083 rings. This is substantial progress, not a
complete categorification of all eighteen. All eighteen received new analysis.

| Outcome | IDs, with prefix R9_2_ | Main argument |
|---|---|---|
| General complex exclusion | 585, 1303 | A nonsolvable dimension-60 neutral category forces every extension to be group-theoretical, contrary to nonintegral dimensions |
| General complex exclusion | 1025, 1709, 1759, 1988 | A cyclic internal-end algebra forces multiplicity-free tensor products, contradicting multiplicity two |
| Explicit unitary model | 746, 1209 | Two coherent inversion equivariantizations of a cyclic generalized Tambara–Yamagami category |
| Explicit unitary model | 1254 | An order-four cover functor descends to a coherent involution of a generalized Moore–Read category |
| Still unresolved | 12, 137, 941, 959, 1607, 1848, 1965, 1975, 1976 | Scope restrictions, Morita reductions, and construction obstructions |

The prior 142 multiplicity-one rings are unchanged. Cumulatively, rank nine
through multiplicity two has 2,225 rings: 2,141 excluded, 75 modeled, and
9 unresolved. The overall project frontier decreases from 25 to 16 cases.

## R8_3_436: a corrected proof, not a restored premise

The criticism is correct. The earlier complete-table derivation assumes
unitarity; reconstruction of categories from scalar solutions does not
parameterize every original spherical category. The exact scalar checks do
not bridge this gap. The claimed universal Galois-unitarization proposition
is therefore explicitly withdrawn.

An independent replacement proves that **R8_3_436 still has no complex
categorification**. Its hypothetical neutral near-group category admits a
coherent inversion action after cancellation of a pointed associator anomaly.
The resulting spherical equivariantization has rank five and dimension
field Q(sqrt(21)). Every possible fusion-rule branch has a formal codegree
in Q(sqrt(5)) or Q(sqrt(13)), contradicting the spherical dimension-field
theorem. This proof allows either spherical dimension root and needs no
unitary parameterization. The full proof and independent audit are in
`r8_scope/REPAIR.md` and `root_audit/R8_REPAIR_AUDIT.md`.

The old stronger claim remains withdrawn even though the exclusion
conclusion is recovered. Historical proof files must be marked superseded,
and the manuscript generator must use the replacement; the exact publication
map is in `r8_scope/PUBLICATION_HANDOFF.md`.

## Precise status of every remaining case

All nine remain unresolved for arbitrary complex fusion categories. None
admits a braided categorification. The new restrictions are:

| Case | New progress |
|---|---|
| R9_2_12 | Central Rep(S3) obstruction; braided descent; all group-theoretical categorifications excluded |
| R9_2_137 | Fixed transparent involution obstruction; all-complex character frames; quantum-group Morita route ruled out |
| R9_2_941 | Exact published open dimension-504 ring; weakly group-theoretical categorifications excluded |
| R9_2_959 | Central Rep(S3)/braided obstruction; all group-theoretical categorifications excluded |
| R9_2_1607 | Same transparent-involution obstruction and refined center analysis |
| R9_2_1848 | Exact Morita dual returns the same ring; invertible group is C6 |
| R9_2_1965 | Noncommutativity; all group-theoretical categorifications excluded |
| R9_2_1975 | Rank-twelve Morita alternatives reduced; one branch contains the existing open R6_4_155 |
| R9_2_1976 | Same transparent-involution obstruction and refined center analysis |

A braided exclusion does not imply a fusion-category exclusion. Likewise,
excluding every group-theoretical construction does not exclude an
arbitrary complex category. R9_2_941 is precisely the exotic ring asked
about in Alekseyev–Bruns–Dong–Palcoux, arXiv:2507.07023v2, Question 1.14;
its published open status is not itself a nonexistence proof.

The group-theoretical exclusions cover every finite-group presentation,
including all associator and subgroup twists. The reduction uses an
exhaustive projective-character scan followed by cohomological transfer
and exact relative-trivialization tests. A separate audit repeated the
group scan and independently decided all primitive equations. This
settles that entire construction class for the integral residuals.

For R9_2_1254, the earlier mixed Moore–Read lift ansatz is impossible
even with arbitrary complex tensorators: five equations multiply to a
contradiction. The successful model uses a different lift whose square
becomes the identity only after central condensation. Its coherent action
is certified explicitly, including the correction of the initial parity
defect. See `weak_a/MR_1254_MODEL.md` and its independent audit.

For the five other quadratic cases, the earlier general-to-pseudo-unitary
reduction is at the level of existence and can require Galois conjugation.
It does not make every original categorification pseudo-unitary.

## Verification and limitations

The new general exclusions have explicit categorical proofs and separate
reviews of their premises. A second implementation of the cyclic criterion
scanned all 2,083 exact-M2 tensors: 289 witnesses, of which four were newly
unresolved; all 32 earlier models passed as controls. All three new constructions
received an independent audit of half-braidings, central-algebra descent,
action coherence, and the decisive equivariant fusion-line sign. Each matches
all 729 source coefficients. All 35 model transports were then replayed,
checking 25,515 coefficient equalities in total.

The R8 replacement was checked against every possible rank-five branch,
with independent exact formal-codegree and field-norm calculations. The six
new braided-only exclusions have exact tensor witnesses and scope proofs.
The frontier reports distinguish exhaustive finite enumerations from bounded
or numerical investigations. Surviving necessary conditions, a solver timeout,
and unsuccessful model searches are never classified as models or exclusions.

The current research ledger is `phase4/results/ledger.json`; phase3 and
all earlier ledgers are preserved as historical snapshots. Run
`python phase4/verify.py` from the package root for the accepted finite checks.
The full categorical proofs are mathematical arguments reviewed here; they
are not formal proof-assistant certificates. This AI-assisted research
requires independent human mathematical verification before reliance or
scholarly publication.

No GitHub repository, website, or online manuscript was changed in this
research continuation. The evidence is prepared for the later revision step.

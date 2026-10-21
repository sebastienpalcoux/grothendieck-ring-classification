# Rank-eight research continuation, 22 October 2026

The pointed-induction Fourier criterion and its integer fibre-packing
refinement exclude **R8_3_65 and R8_3_1795 from general complex
categorification**. The exact-multiplicity-three ledger now has
**3,506 general exclusions, 15 unitary realizations, and six unresolved
rings** among 3,527 inputs. Through multiplicity three the totals are
**4,402 exclusions, 92 unitary realizations, and six unresolved rings**.
This stage constructs no additional model. All 4,498 prior ledger entries
outside these two decisions, and all 92 prior models, are preserved exactly.

## New results and their limits

| Cases | Accepted result | Remaining question |
| --- | --- | --- |
| R65 | General exclusion by pointed induction and Fourier integrality, covering all four pointed associator classes | None for existence |
| R1795 | General exclusion by integer Fourier-fibre packing, covering all sixteen indicator branches and both pointed associators | None for existence |
| R982, R1768, R1795, R3472 | Every categorification admits a spherical structure and has a pseudo-unitary Galois conjugate | Existence for R982, R1768 and R3472; this gate enables the R1795 exclusion |
| All eight incoming rings | A uniform tensor-image criterion excludes every braided Morita representative, using the general braided exclusions | Arbitrary unbraided constructions for the six survivors |
| R1154 and R1795 | Incompatible center dimension inventories exclude Morita equivalence between the pair | R1154 categorifiability; R1795 is subsequently excluded |
| R982 | Every indecomposable module category has rank eight; three necessary based-module types; 31 algebra candidates reduce to eight | Algebra/module associators; the nonregular route requires an algebra on 1+X5 |
| R1768 | Nontrivial pointed C2 associator; free pointed action on every module category, whose rank is even and at least four | 21 retained induction factors; 15 still lack full module actions |
| R3472 | Ten possible dual dimension spectra for one specified rank-two module branch | Categorical lifts; the other rank-two branch is outside this spectrum theorem |

The six remaining IDs are `R8_3_928`, `R8_3_941`, `R8_3_982`,
`R8_3_1154`, `R8_3_1768`, and `R8_3_3472`.
All have a general-to-spherical and Galois-pseudo-unitary reduction. The
Galois statement allows changing the category; it does not assert that the
original category is pseudo-unitary, or that a pseudo-unitary category is
unitary. Their general unbraided categorifiability remains open.

## Proof map

* [C2 Fourier-packing refinement and the R1795 exclusion](pointed_followup/PROOF.md).
  Each pointed twist fibre has dimension mass D/2. Complete finite integer
  packing removes impossible restriction columns before exact separation.
  All sixteen R1795 branches are excluded. For R1768, all eight trivial-
  associator branches are excluded; an exact witness survives only in the
  nontrivial pointed-associator relaxation. That witness is not a category.
* [Completed intermediate R1795 Morita construction attempt](pointed_followup/r1795_morita/PROOF.md).
  The odd-associator exclusion first forced the algebra 1+g. An independent
  enumeration of 2,531,250 central C2 cover choices yields 45 associative
  rings; exact obstructions eliminate 44 and leave only R1795 itself.
  This conditional same-fusion-ring result constructs neither a category nor
  a categorical self-equivalence. The complete R1795 exclusion supersedes it.
* [Dimension-block bounds and their equality cases](pointed_followup/dimension_block/PROOF.md).
  All seven incoming rings pass the scalar bounds. Equality gives additional
  linear restrictions on twist-one center objects for R928, R941, R982 and
  R1768. Every forced I(1) summand passes; no refined cone search is claimed.
* [R65: pointed induction and Fourier integrality](r65/PROOF.md).
  Indicator saturation fixes central twist powers. Fourier inversion fixes
  each fibre's dimension mass; integral restriction multiplicities then
  remove columns from the complete all-order trace cone. Six exact rational
  separators cover every pointed-associator and remaining second-indicator
  branch. The published two-dimension Galois theorem makes the exclusion
  general. No prior rank-four or R1453 exclusion is needed for this proof.
* [Four general sphericalization gates](pivotality/PROOF.md).
  Full parity enumeration modulo a justified sign gauge handles R982,
  R1768 and R1795. Positive second-indicator normalization handles R3472.
  Every ordered associativity equation is retained; commutativity of a
  signed quotient is never assumed in the enumeration.
* [Uniform obstruction to braided Morita representatives](braided_morita/PROOF.md).
  Every proper based subring is pointed and the global FP dimension is
  irrational. A braided Morita representative would yield a dominant
  equal-dimension tensor functor and hence a braiding on the source.
* [Pairwise Morita obstruction and stronger Galois constraints](r1154_r1795/PROOF.md).
  The final three R1154 center patterns contain no simple of dimension
  D/10, whereas R1795 requires four. The stronger Galois covariance test
  still admits all 25 current R1154 histograms; it gives no further exclusion.
* [R1768 module restrictions](pointed_followup/r1768_modules/PROOF.md).
  The nontrivial pointed associator forces a free action on module simples.
  Of 61 recorded induction factors, 21 remain, with possible ranks 4, 6, 8
  and 12. Three of nine previously determined full actions survive; 15
  retained factors still have undetermined actions. This is not a complete
  classification of module categories or their based actions.
* [R982 module-category restrictions](r982/MODULE_TYPES.md).
  Semion associator freeness and complete paired Gram factorization prove
  the rank and type statements. The exact center d-number and divisibility
  probes in the same folder eliminate no additional restriction column.
* [Independent R928/R941 center arguments](r928_r941/PROOF.md).
  These include a reusable fermion-centralizer rank-square obstruction.
  Their applications are also covered by the simpler tensor-image theorem.

The corrected R3472 spectrum proof and exact finite enumeration are in
`r1768_r3472/`. Its hypothesis specifies the action matrix
`[[5,7],[7,7]]`. The other action has a larger integral commutant and is
explicitly excluded from this claim. Independent review caught and corrected
the earlier overbroad draft before publication.

## Verification and publication

```sh
python3 tools/verify_rank8_research_20261022.py
python3 -O tools/verify_rank8_research_20261022.py
python3 tools/rank8_research_20261022.py --check
```

The targeted replay verifies the new mathematical certificates and independent
reconstructions. It does not rerun the earlier 108-check campaign. Separate
normal and optimized receipts record exactly which scripts ran, their source
identities and their output hashes. An assertion-based component is executed
with assertions enabled even when the outer command uses `-O`.

`accepted.json` binds the proof inputs and scoped research updates.
`per_ring_research_audit.json` retains earlier attempts and appends these
results. The new ledger is
`supplements/rank8/output/research_20261022/ledger.json`; the inherited
92-model catalogue is unchanged. The additive release archive preserves
the previous package's members, including superseded files under its
recorded historical paths. Packaging checks are distinguished from
mathematical replay.

Independent computational and mathematical audits in this directory were
performed by separate automated reviewers. They do not replace independent
human review or formal verification. Surviving necessary data, module actions
and dimension spectra do not supply associators or prove categorical novelty.

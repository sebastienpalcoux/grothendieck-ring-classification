# Rank-six pre-publication audit — 16 October 2026 (UTC)

This is a fresh AI review, not independent human verification and not a Lean formalization. No historical research, evidence, manuscript, certificate, or manifest was modified. The review deliberately did not treat earlier audit prose or `PASS` receipts as proofs.

## Outcome

I found two concrete documentation defects that should be corrected in an append-only publication erratum before public release. I did not find a counterexample or a missing categorical hypothesis invalidating the **new rank-six conclusions reviewed here**. Neither defect changes the mathematical verdict: **R6_4_155 and R6_8_1660 remain unresolved**. The rank-37 obstruction excludes one specified witness, not the source ring. Passing the fermion identities constructs no category.

This is not a claim to have independently reproved all 25,362 historical rank-six exclusions. The inspected dependency chain and sampling are itemized below, and the remaining limits are explicit.

## Findings requiring correction

### R6-DOC-1 — Wrong proposition used for the general-to-pseudo-unitary reduction

Severity: **medium; a substantive broken proof reference, with an existing valid replacement dependency**.

- `manuscripts/rank6/papers/chapters/frontier_tensor_functors.tex:105–106` invokes `prop:frontier-galois-pu` while treating R6_4_155 and R6_8_1660.
- `manuscripts/rank6/papers/chapters/dimension_block_20261016.tex:81–82` invokes the same proposition while treating R6_8_1660.
- The actual proposition, in `chapters/frontier_spherical_reduction.tex:3–9`, concerns **only R6_3_215**. It cannot prove the stated reductions for the two residual rings.

The correct R6_4_155 dependency is `prop:nonselfdual-neargroup-spherical` in `chapters/frontier_155.tex:12–51`. Its argument really starts from an arbitrary categorification, uses sphericalization, and forces a fusion-closed set of lifts by integrality of the ratio of global dimensions. I checked the two norm identities, the simultaneous quadratic conjugation, the lift closure, and the positive-root conclusion. The argument does not assume the original category pivotal or pseudo-unitary.

For R6_8_1660, the necessary reduction is asserted at `chapters/frontier_1660.tex:11–15` and actually certified in:

- `supplements/rank6/research/round4/m8/R6_8_1660_reduction.json`;
- `supplements/rank6/software/galois_pseudo_reduction.py`;
- `supplements/rank6/software/oriented_signed.py`;
- the packaged entry point `supplements/rank6/research/round5/m8_1660_conductor/replay_reduction.py`.

I read the relevant algorithms and the mathematical signed-field obstruction, then freshly replayed the certificate without executing the packaged receipt-writing entry point. It enumerates with `normalized=False`, covering all coefficient parity intervals without positive-indicator assumptions. The outcome is 640 signed quotients, 24 sign orbits, one original gauge orbit, and 58 nongauge character rejections: 28 zero dimensions, 29 norm failures, and one field-prime failure. The original characters have degrees 1, 1, 4; the two degree-one characters have zero simple dimensions, leaving precisely the FP Galois orbit. The gauge orbit supplies a spherical section by the standard sum/difference argument explicitly explained in the manuscript's earlier sphericalization section. Fresh receipt: `work/prepublic_audit/rank6_unrestricted_reduction.json`.

**Exact replacement wording for the first reference:**

> Extend to this common field the Galois conjugation supplied for R6_4_155 by Proposition `prop:nonselfdual-neargroup-spherical`, and for R6_8_1660 by the unrestricted sphericalization reduction described at the beginning of §`subsec:frontier-1660` and certified in `supplements/rank6/research/round4/m8/R6_8_1660_reduction.json`.

**Exact replacement wording for the second reference:**

> Apply the unrestricted sphericalization reduction for R6_8_1660 described in §`subsec:frontier-1660` (certificate `supplements/rank6/research/round4/m8/R6_8_1660_reduction.json`), followed by Lemma `lem:pu-tensor-functors`.

These chapters are bound by `evidence/unified_20261016/source_files.json`; do not silently edit them or replace the historical manifest. A dated erratum beside the manuscript downloads preserves the evidence history while repairing the current reading path.

### R6-DOC-2 — Nonportable replay command

Severity: **low; reproducibility documentation**.

`evidence/unified_20261016/rank6/RESEARCH.md:34` gives

```text
python work/unified/rank6_center/verify_fermion_crossing.py --repo repo
```

The documented script path does not exist in the repository snapshot. The actual standalone checker is published under the evidence directory. From the repository root the command is:

```sh
python evidence/unified_20261016/rank6/verify_fermion_crossing.py --repo .
```

Repeat with `python -O` if desired. This README is also hash-bound, so place the corrected command in the dated erratum/current verification guide rather than rewriting the frozen record.

## Categorical and arithmetic review

### Fermion Azumaya crossing

Read `chapters/fermion_azumaya_20261016.tex` in full and its application in the unified research note. Checked the actual reason alpha-induction is an equivalence: the one-generator Clifford algebra is Azumaya inside sVec, and its canonical Azumaya map remains an isomorphism after braided inclusion. This uses a genuine fermion/sVec embedding, not merely a commutative based ring. The linking-category index manipulation is consistent with `M_{i*}=M_i^T`.

The cited primary source was read directly: Davydov–Nikshych, *The Picard crossed module of a braided tensor category*, §3.2, Definition 3.5 and following paragraph, https://arxiv.org/pdf/1202.0061. It explicitly identifies the Azumaya condition with both alpha-induction equivalences. The reviewed theorem is a necessary identity; a based module satisfying it still needs coherent module associators. The manuscript states that limitation correctly.

### Dimension-block equality and the complete actual-root domain

Read `chapters/dimension_block_20261016.tex` in full, together with the saturated-conductor and universal-moment arguments in `chapters/signed_character_fields.tex:360–528`, and the actual twist-bound argument in `chapters/frontier_1660.tex:136–184`.

Read the primary theorem and its proof: Schopieray, *The dimension block of a spherical fusion category*, Lemmas 2.1, 3.1, 4.1 and Theorem 5.1, https://arxiv.org/html/2609.35287. In particular, the proof really gives the stronger compression-norm bound used in the manuscript, not only the final scalar inequality. The source derives unitarity of the canonical modular **representation**; no unitary categorical structure is required.

The conductor-equality argument is legitimate: in the induced primitive-column representation, the two norm-attaining local vectors are pullbacks from the conductor modulus. At trivial local character, equality forces invariance under both upper and lower unipotents and hence a trivial local representation. This justifies conductor support rather than an arbitrary search cutoff.

For R1660, both nontrivial saturated weights have conductors 12 and 24. The manuscript separately treats columns where both weights vanish, using Ising projection; those are not lost by the support condition. Together these yield the actual order-dividing-48 domain. In the new twist-one proposition, removing the two saturated Fourier components forces `a=3z` and `b+c=4z`; a nonzero sigma multiplicity then has primitive order-16 twist and cannot be twist one. The zero-restriction case is excluded. The proof does not infer existence from the resulting data.

### Higher-indicator refinement

Read `chapters/higher_indicators_20261016.tex`, `higher_indicators/R1660_HIGHER_INDICATOR_PROOF.md`, and the complete standard-library verifier. Checked the crucial logical step: knowing a low compression eigenvalue alone would not isolate an irreducible summand, but the entire twist-one space is known, the appropriate torus multiplicity is one, and every eligible irreducible containing that character has one-dimensional twist-fixed space. Thus projection of the unit vector to that irreducible is indeed `w_r/4`. This justifies the character-trace-to-matrix-coefficient conversion.

The checker loops over all 532 local irreducible pairs and fails explicitly on an unexpected fixed-space rank; it does not silently discard such a branch. The comparison uses the two complete low compression multisets, not a selected high profile. The source indicator equation, factor of four, rational weights, and odd-indicator linear solution are consistent. I independently recomputed the radical weights and source invariant dimensions from the full tensor, without importing the new checker. The ten possible third-rotation traces on a three-dimensional space contain the two conjugate surviving traces and exclude both mixed traces. No claim that self-dual objects have real higher indicators is used.

The categorical tensor involution was also inspected in `frontier_1660.tex:410–449`: the argument constructs the action by a central boson and de-equivariantization, including triviality of its image half-braiding and the dimension comparison. It does not infer a tensor autoequivalence solely from a ring permutation.

### Fixed rank-37 Verlinde obstruction

Read `chapters/witness_verlinde_20261016.tex` and the standalone proof note. The argument requires the exact historical restriction rows, twist fiber, and irreducible decomposition; its scope is correctly limited to that witness. Equal nonzero coordinates identify the symmetric repeated-twist line in W; the one-dimensional remaining representation identifies the antisymmetric line. Simple twist spectrum in W justifies each weighted expectation q_t. Since the spectral ratio is constant on the repeated twist fiber, the hidden line has eigenvalue -1 and the mixed term vanishes. Thus the half-integral diagonal coefficient is not a phase-choice artifact.

Independent rational arithmetic confirms that the displayed probabilities sum to one, their weighted visible expectation is 2, and `(2-1)/2=1/2`. The original 1,536 equations may still pass: those equations do not include every Verlinde integrality condition. There is no contradiction in retaining their historical PASS receipt and separately rejecting the stronger witness claim.

### Arbitrary tensor functors and pivotal scope

Read `chapters/frontier_tensor_functors.tex` in full. I checked the two nontrivial scope upgrades rather than assuming pivotal compatibility:

1. A dominant image of a pseudo-unitary category embeds by right tensor multiplication into its Morita dual; dominance gives full faithfulness of that embedding. Morita invariance of global and FP dimension makes that dual pseudo-unitary, and restriction supplies a positive spherical structure on the image.
2. The comparison of the two spherical structures is a monoidal natural automorphism of the functor. The finite-spectrum/tensor-power argument rules out non-root-of-unity eigenvalues and nontrivial Jordan blocks. Positive categorical trace then forces the comparison to be identity.

I verified the required primary statements in EGNO, *Tensor Categories*, https://math.mit.edu/~etingof/egnobookfinal.pdf: Corollary 9.1.8 (common algebraic number fields), Proposition 9.3.9 (Morita global dimension), Proposition 9.4.2 (global/FP ratio), and Proposition 9.5.1 (canonical positive spherical structure).

For R155 the remaining algebra argument uses twist-one support, connectedness after forgetting, and a nondegenerate Frobenius pairing; associativity on `Z⊗Z⊗Z*` genuinely contradicts zero multiplication on `Z⊗Z`. For R1660, every twist-one constituent restricting with unit multiplicity one leaves only the unit algebra. These conclusions concern hypothetical categories and leave both existence questions open.

### Selected older general-exclusion foundations

Read the full basic reduction chapter `03.tex`, the ambient cyclotomic trace bound, the quartic stabilizer exclusion proof, the ramification trace criterion, and the entire eleven-case multiplicity-nine completion chapter. Adversarial checks included:

- noncommutative signed quotients are not identified using arbitrary transpositions; only cyclic and dual-reflection orbits are imposed;
- self-dual original objects have self-dual lifts because the two lift dimensions are nonzero opposites;
- promotion from spherical or pseudo-unitary exclusions is accompanied by an exhaustive signed reduction or a separate dimension-field proof;
- actual-root tests are distinguished from normalized relative-trace relaxations;
- the ambient finite trace-domain argument accounts for arbitrarily large prime powers by vanishing trace, not a guessed root cutoff;
- the eleven-case multiplicity-nine proof handles quartic/sextic dimension fields, totally positive bounds, complementary formal codegrees, and the exceptional signed-table domain explicitly;
- the final thirteen-primary Galois contradiction in the PSU(2)_5 extension argument uses the actual twist action squared, allowing higher powers of thirteen, and compares it against a Gram multiplicity budget.

No new counterexample was found in these sampled older arguments. Their large enumerations, source-model identifications, and the 2.247-billion-node historical search were not independently reimplemented in this review. Root-level full replay results are separate evidence.

## Fresh local checks and limits

`work/prepublic_audit/rank6_spotchecks.py` and `.json` record independent small exact checks: the inverse global dimension, both Fourier weight vectors, twist-one restriction equations, invariant dimensions at powers 3, 5, 7, all ten possible cubic rotation traces, the displayed Verlinde expectation, and the generalized near-group norm identities. The separate unrestricted reduction receipt is noted above.

The review reads finite-group character tables through their certified interfaces; it does not construct all 532 representations from scratch. It does not prove pentagons for the two open rings, independently reconstruct every historic model, validate every source bibliographic claim, or constitute human peer review. The completed automated suite and this audit therefore support publication as **provisional AI-generated research with transparent verification scope**, not a statement that all results are human-verified or formally certified.

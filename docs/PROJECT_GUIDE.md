# Project guide

**Current classification: six unresolved cases.** R8_3_1768 is excluded over the complex numbers by pivotal conjugation parity, using the established existence and complete center-domain reductions. The current continuation adds branch exclusions and conditional constructions, including the exact identification of Anyon Atlas B20-02148. No additional categorification is claimed.

> **AI-generated research; independent human verification pending.** Exact checks establish only their stated computational scope.

## Read the project

- [Current ranks 2–5 series](../manuscripts/README.md) gives four unrestricted classifications without an initial pivotality assumption.
- [Rank-five paper](../manuscripts/rank5.pdf), [reading guide](../manuscripts/rank5/README.md) and [exact replay](../supplements/rank5/sharp/README.md) provide the current rank-five route.
- [Public Atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/) presents the current classification and case records.
- [Manuscripts](../manuscripts/README.md) gives one current paper per rank or stated band.
- [Theory and definitions](https://sebastienpalcoux.github.io/grothendieck-ring-classification/theory.html) introduces fusion rings, fusion categories and the structural filters.
- [Current research frontier](RESEARCH_STATUS.md) states exactly what remains open.
- [Verification](VERIFY.md) provides reproducible commands and their limits.

## Rank-five classification (24 November 2026)

The current series gives unrestricted classifications at ranks 2–5, without
assuming a pivotal structure. At rank five, every complex fusion category
has a pseudo-unitary Galois conjugate and admits a spherical structure.
Exactly seventeen based rings occur, each with a unitary realization; the
sharp bounds are μ ≤ 4 and FPdim ≤ 48 + 24√3.

Start with the [rank-five reading guide](../manuscripts/rank5/README.md),
[canonical paper](../manuscripts/rank5.pdf) and
[exact replay](../supplements/rank5/sharp/README.md).
The [earlier census through multiplicity twenty](../supplements/rank5/README.md)
remains separate historical evidence: 40,999 inputs, 40,982 exclusions and
17 models. Its original counts and records are preserved.

## Two complementary repositories

The [Fusion Ring Census](https://github.com/sebastienpalcoux/fusion-ring-census) enumerates based rings without a categorifiability filter. Its bounded regions contain 1,434,042 rings. This classification repository supplies categorical models and exclusions. The Atlas case directory covers the full census; detailed research profiles are supplied where available. Census-only numerical invariants are never treated as categorical models.

<a id="grothendieck-rings--known-realizations-at-each-exact-multiplicity"></a>

## Decisions and models

An exclusion is recorded at its proved scope: general complex, pivotal, spherical, pseudo-unitary or unitary. A restriction at one level is not automatically an exclusion at a broader level. A realized based ring has at least one categorical model; inequivalent associators are not counted separately. R12_1_623 is recorded as complex/pseudo-unitary with unitarity unproved.

A model must be categorically constructed and matched to the full tensor by an exact based isomorphism. Matching FP dimensions or modular spectra is insufficient. Necessary center matrices, rational witnesses and conditional algebra constructions retain unresolved status.

## Current data

[All-rank classification totals](../data/classification_summary_all_ranks.csv) · [Current publication manifest](../data/current_publication_revision.json) · [Six open tensors](../data/current_remaining_cases.py) · [Current proofs and exact replay](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/frontier/README.md)

## Construction catalogue

“New” refers only to a specific construction that has not, to our knowledge, been explicitly recorded in the literature. The constructions use known methods, with hypotheses and fusion rules checked in the project; this is not a claim of novelty up to tensor equivalence or of exoticness. Independent human verification remains pending. [New constructions](https://sebastienpalcoux.github.io/grothendieck-ring-classification/constructions.html).

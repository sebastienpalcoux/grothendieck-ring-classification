# Unrestricted rank-four Grothendieck ring classification

**[Read the main manuscript · 88 pages](papers/companion.pdf)** ·
[LaTeX source](papers/companion.tex) ·
[Exact verification package](../../supplements/rank4/unrestricted/README.md)

> **AI-generated research · independent verification pending.** The results,
> proofs, code and data require independent human verification and have not
> been formalized in Lean. Treat them as provisional; computational checks
> do not replace mathematical review.

## The general classification

**No multiplicity bound; no initial pivotality assumption.** The main
manuscript classifies the Grothendieck rings of arbitrary rank-four fusion
categories over ℂ:

- **Exactly 15 based-isomorphism classes of Grothendieck rings.**
- **Every categorification admits a spherical structure.**
- The sharp bounds are **FPdim ≤ 24 + 12√3** and **multiplicity ≤ 6**,
  attained by the near-group ring `NG(C₃,6)`.

These bounds are conclusions of the classification. They are not assumptions
on its scope. The result classifies Grothendieck rings; it does not assert
uniqueness of the fusion category realizing a ring.

The proof first establishes the theoretical bounds FPdim < 1000 and
multiplicity at most 31, then applies exact finite verification to a census
of **1,692 rings: 1,677 exclusions and 15 models**.

## Reading order

| Read | Pages | Scope |
|---|---:|---|
| **[Unrestricted classification — main paper](papers/companion.pdf)** · [TeX](papers/companion.tex) | **88** | **General rank-four classification, without a multiplicity bound** |
| [Finite-range classification companion](papers/finite.pdf) · [TeX](papers/finite.tex) | 29 | Separate census through multiplicity 128 |
| [Mathematical verification guide](papers/verification_guide.pdf) · [TeX](papers/verification_guide.tex) | 9 | Criteria, certificates and replay scope |

The primary unrestricted manuscript is stored as `papers/companion.pdf`;
its source and section files are in [the papers folder](papers/README.md).

## Proof package and related work

- [Unrestricted classification: exact replay and census](../../supplements/rank4/unrestricted/README.md)
- [Finite census through multiplicity 128: public replay](../../supplements/rank4/PUBLIC_REPLAY.md)
- [Verification scope](../../docs/PREPUBLICATION_REVIEW.md)
- [All research manuscripts](../README.md)

For the pivotal case, see Jingcheng Dong, Sébastien Palcoux and Arnaud Plessis,
[*Classifying Grothendieck rings of pivotal fusion categories of rank four*](https://arxiv.org/abs/2609.33272).
That paper assumes pivotality; the general classification above does not.

# Braided scope of the unresolved and retained cases

Braiding is a separate requirement from pivotality, sphericality,
pseudo-unitarity and unitarity. Every one of the six current unresolved cases is excluded
from braided categorification without a pivotality assumption. The three unresolved rank-eight cases have unconditional braided exclusions.
The retained four-case sphericalization gates also apply to the now generally
excluded R8_3_1768. All conclusions retain
the project's independent-review caution.

| Cases | Strongest braided exclusion recorded here |
| --- | --- |
| `R6_4_155`, `R6_8_1660` | No general braided categorification |
| `R8_3_928`, `R8_3_941`, `R8_3_1154` | No general braided categorification, and no braided Morita representative |
| `R9_2_137` | No general braided categorification; see the current center restrictions |
| `R8_3_1768` (generally excluded) | No complex categorification, by pivotal conjugation parity |
| `R8_3_982` (unitarily realized) | No general braided categorification, and no braided Morita representative |

For R9_2_137 the [current proof account](../evidence/frontier/README.md) gives the center restrictions: a braiding would lift its four source invertibles to a center with at most two invertibles. The same account proves the general exclusion of R8_3_1768; its weaker braided obstruction below is retained only as a supporting historical argument.

`R8_3_982` is now realized by the triality-zero component of the unitary
E21 category from SU(3)_21 into E7_1; see the
[source construction and exact fusion-tensor identification](../evidence/rank8_creative_20261022/r982/E21_MODEL.md).
This unbraided unitary model is consistent with the braiding obstruction
below. Its former case page retains both results and the complete research
history. Realization does not weaken or remove the universal braiding
and braided-Morita exclusions.

`R8_3_65` is now excluded from general categorification by the independent
[pointed-induction Fourier obstruction](../evidence/rank8_research_20261022/r65/PROOF.md).
Its earlier braided obstruction is retained below as a historical argument.
`R8_3_1795` is likewise excluded from general categorification by the
[complete order-two Fourier-packing argument](../evidence/rank8_research_20261022/pointed_followup/PROOF.md).
Its braided obstruction below records an earlier, weaker result.
`R8_3_3472` is now also excluded from general categorification by the
[complete center and rotation-indicator argument](../evidence/r3472_exclusion_20261022/README.md).
Its d-number obstruction below is retained as an earlier braided-only result.

## General braided exclusions

For `R6_4_155`, the existing result is stronger: no categorification is
Morita equivalent to a braided category. See Proposition
`prop:155-no-braided-morita` of
[`frontier_155.tex`](../manuscripts/rank6/papers/chapters/frontier_155.tex)
and the standalone
[`structural_reductions.md`](../supplements/rank6/research/frontier/R6_4_155/structural_reductions.md).
The established Galois pseudo-unitary reduction, the central semion and the
absence of nontrivial twist-one central invertibles yield the obstruction.
Galois transport preserves braidings and Morita contexts.

For `R6_8_1660`, a braiding makes the Ising subcategory nondegenerate, so
the category splits as its Deligne product with a rank-two category.
The coefficient `N[X,X,sigma X]=4` contradicts that factorization. See
Corollary `cor:1660-no-braiding` of
[`frontier_1660.tex`](../manuscripts/rank6/papers/chapters/frontier_1660.tex),
using DGNO, [*On braided fusion categories I*](https://arxiv.org/abs/0906.0620),
Corollary B.12 and Theorem 3.13. This needs no pivotality assumption.

For `R8_3_65`, the invertibles form C4 and act transitively on the four
noninvertibles, whose common dimension is `(11+5 sqrt(5))/2`, with minimal
polynomial `x^2-11x-1`. It is therefore an irrational generalized near-group
ring. The two possibilities in Schopieray,
[*Irrational braided generalized near-groups*, Theorem 1](https://arxiv.org/abs/2212.14009),
have noninvertible dimensions `(1+sqrt(5))/2` or `1+sqrt(2)`, incompatible
with this ring. The theorem does not require pivotality or pseudo-unitarity.
The exact fusion calculation is recorded in
[`STRUCTURAL_SCOPE.md`](../evidence/rank8_frontier_20261021/structural_models/STRUCTURAL_SCOPE.md).

For `R8_3_928`, `R8_3_941` and `R8_3_1154`, the fusion ring is
noncommutative. A braiding gives `X_i tensor X_j` isomorphic to
`X_j tensor X_i`, so all their multiplicities would agree. Each site's
scope record contains an explicit unequal coefficient pair, checked against
the canonical tensor by `check_cases.py`.

## General reduction preserving a braiding

For `R8_3_982`, `R8_3_1768`, `R8_3_1795`, and `R8_3_3472`, the new
[complete signed-sphericalization proof](../evidence/rank8_research_20261022/pivotality/PROOF.md)
shows that every general categorification admits a spherical structure and
has a pseudo-unitary Galois conjugate. Apply the same field automorphism to
the braiding matrices. Naturality and the hexagon identities remain true.
Consequently each pseudo-unitary braided obstruction below excludes
**general braided categorification**. This deduction uses the proved
four-case sphericalization result; it makes no general pivotality conjecture.

### R8_3_982: forced semion versus the adjoint category

The complete necessary pseudo-unitary center audit has four induction
frames. Frames 0 and 1 are excluded; frames 2 and 3 have the same remaining
systems. The only surviving indicator branch has `nu_2(g)=-1` for `g=X_6`
and forces a unique central invertible `G` forgetting to `g`, with
`G^2=1` and twist `+i` or `-i`. These are necessary consequences of the
complete frame and branch exclusions, not an inference from one selected
surviving witness. See
[`FINAL_SUMMARY.json`](../evidence/rank8_next_20261021/r982/FINAL_SUMMARY.json),
[`FRAME01_RESULT.md`](../evidence/rank8_next_20261021/r982/FRAME01_RESULT.md)
and [`SEMION_ACTION.md`](../evidence/rank8_next_20261021/r982/SEMION_ACTION.md).

A braiding on the source category supplies a central lift of `g`; uniqueness
identifies it with `G`. Consequently the source pointed C2 subcategory is
semionic and nondegenerate. By the nondegenerate-subcategory decomposition,
the source category would be `Semion tensor D`. Its adjoint subcategory is
contained in `Vec tensor D` and is proper. Direct closure of all `X X*`
supports in the canonical tensor instead gives the whole ring. This
contradiction excludes pseudo-unitary braided categorification, and the
preceding reduction excludes general braided categorification.

### R8_3_1768 and R8_3_3472: a simple-dimension d-number obstruction

Ostrik, [*On formal codegrees of fusion categories*, Theorem 1.8](https://arxiv.org/abs/0810.3242),
proves that squared norms of simples in a braided fusion category are
d-numbers. Under pseudo-unitarity these are squared FP dimensions.
Corollary 2.9 equates the d-number conditions for an algebraic integer and
its square. For a quadratic minimal polynomial `x^2-t x+n`, Lemma 2.7(v)
requires `n` to divide `t^2`.

* `R8_3_1768` has the simple dimension `5+sqrt(37)`, with polynomial
  `x^2-10x-12`. But `12` does not divide `100`.
* `R8_3_3472` has the simple dimension `6+5sqrt(2)`, with polynomial
  `x^2-12x-14`. But `14` does not divide `144`.

This proves the pseudo-unitary braided obstructions, hence the general
braided obstructions by the preceding reduction. One must not replace
squared norm by FP dimension for a general non-pivotal braided category;
Ostrik's Remark 1.9(i) explicitly distinguishes the two questions.

### R8_3_1795: a reduced-codegree obstruction

The canonical tensor is self-dual, has full adjoint subring, and has exactly
one proper nontrivial based subring, `{1,g}` with `g=X_1` of order two.
The action of `g` consists of the four pairs `(0,1)`, `(2,7)`, `(3,6)`,
`(4,5)`. In a braided category invertibles centralize the adjoint category,
so `g` is transparent. The whole category cannot be symmetric, since a
complex symmetric fusion category has integral FP dimensions. Its Müger
center is therefore exactly the pointed C2 subcategory, either
`Rep(C2)` or `sVec`.

Set `D=540+240sqrt(5)`. The four characters satisfying `chi(g)=1` have
full-ring formal codegrees `D`, its conjugate, `10`, `10`. Identifying the
four pairs halves those codegrees. In either possible symmetric center,
the reduced codegrees must equal `(D/2)/d_i^2` for the dimensions of the
four representatives:

* For a Tannakian center `Rep(C2)`, de-equivariantization is nondegenerate.
  Each free pair gives one simple: the endomorphism space of the free
  module on `X` is `Hom(X,(1+g) tensor X)`, of dimension one. Thus the
  modularization has rank four, dimensions `d_i`, dimension `D/2` and
  exactly the pair-quotient fusion ring. The usual modular codegree
  identity applies. The positive spherical structure descends to the
  quotient: see DGNO, Proposition 4.56(iii) and §6.3, before Theorem 6.16.
* For center `sVec`, use the reduced S-matrix on one simple per pair.
  Lacabanne, [*Slightly degenerate categories and Z-modular data*,
  Lemma 3.1 and Proposition 3.3](https://arxiv.org/abs/1807.00766), apply
  to braided pivotal categories without a unitarity assumption. In the
  present positive spherical, self-dual setting the reduced matrix obeys
  `S^2=(D/2)I`; its normalized rows give all four quotient characters.
  Their squared row norms give the same reduced-codegree identity.

Consequently a full-ring codegree `10` forces some `d_i^2=D/10`, namely
`54+24sqrt(5)`. The actual squared simple dimensions are only
`1`, `81+36sqrt(5)` and `94+42sqrt(5)`. None equals that value.
Both possible centers are excluded. This proves no pseudo-unitary braided
categorification, hence no general braided categorification.

## Morita representatives

Every proper fusion subcategory of each of the eight incoming rank-eight
rings is pointed, and each global FP dimension is irrational. The
[minimal-image Morita criterion](../evidence/rank8_research_20261022/braided_morita/PROOF.md)
therefore shows that a braided Morita representative would give a braiding
on the source category itself. The preceding exclusions rule this out.
This is a restriction on constructions through Morita equivalence; it does
not exclude the three remaining rank-eight rings from general unbraided
categorification, and it is consistent with the unitary realization of
R8_3_982.

## Replay and maintenance

`python3 site/verify_braided_scope.py` rechecks the finite tensor, dimension
and character calculations used by these braided corollaries. It does
not rerun the much larger previously published center-certificate campaign.
`python3 site/verify_scope_consequences.py` checks the earlier conditional
Galois reductions. The new general gates replay with `python3 evidence/rank8_research_20261022/pivotality/verify_general_spherical_gates.py`. The linked historical center receipts retain their original scope.

The curated `categorification_scope.json` records general braided status
separately from any conditional exclusion, with SHA-256-bound proof sources.
Rebuild with `python3 site/build_cases.py --classification .`, then run
`npm run check` from `site/`. A braided-only exclusion never changes the
general existence status or the five-level implication diagrams. In particular,
R8_3_982 has all five unbraided levels realized and still has braiding excluded.

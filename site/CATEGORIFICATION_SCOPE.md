# Categorification status and implication diagrams

The scope audit concerns complex fusion categorifications of the six current
unresolved rings, together with retained dossiers for three excluded rings and
the realized ring R8_3_982. It reports established results in the linked research
record; it is not a claim that every possible obstruction has been exhausted.

The standard implications are unitary ⇒ pseudo-unitary ⇒ spherical ⇒ pivotal
⇒ general. A case page highlights only the strongest established exclusion:
for example, excluding pivotal categorification also excludes all three stronger
structures. For an unresolved case with no established exclusion, the page
explicitly says that even unitary categorification remains open. A realized
case instead identifies the strongest constructed level. Surviving necessary conditions do not establish
existence. An excluded induction frame, pointed associator or construction
family is not an exclusion of every categorification of that structural type.

## Two kinds of implication

The first diagram concerns structures admitted by the **same category**.
“General ⇒ spherical” means that every hypothetical categorification admits a
spherical structure. “Pivotal ⇒ spherical” means that every categorification
admitting a pivotal structure admits a spherical one. Double arrows are obtained
by combining the standard implications with the case-specific proved arrows.
An absent reverse arrow means that it has not been established in this audit.

A separate diagram concerns **existence for the same fusion ring**, allowing
Galois conjugation when the proof requires it. A pseudo-unitary Galois conjugate
does not imply that the original category is pseudo-unitary, nor does
pseudo-unitarity imply unitarity. Spherical structure can be transported back
through Galois conjugation: the tensor, duality and spherical identities are
algebraic identities, and remain identities under the inverse automorphism.

## Current implications

Every current unresolved ring has the following two consequences:

| Cases | Same-category consequence | Additional existence reduction |
| --- | --- | --- |
| `R6_4_155`, `R6_8_1660` | General ⇒ spherical | Every categorification has a pseudo-unitary Galois conjugate |
| `R8_3_928`, `R8_3_941`, `R8_3_1154`, `R8_3_1768` | General ⇒ spherical | Every categorification has a pseudo-unitary Galois conjugate |

All six remain unresolved at every level in the unbraided hierarchy.
Every one is excluded from general braided categorification. Each of the
four rank-eight cases is also excluded from having a braided Morita
representative. See [the separate braided audit](BRAIDED_CATEGORIFICATION.md).

`R8_3_982` is now **unitarily realized** by the eight-object triality-zero
component of the E21 exceptional fusion category associated with
SU(3)_21 into E7_1. The [construction and exact identification](../evidence/rank8_creative_20261022/r982/E21_MODEL.md)
match all 512 fusion coefficients, and realize the algebra 1+X5 and both
nonregular based-module types. All five unbraided existence levels are
therefore realized. Its former case URL retains the model, invariants, tensor
download and research history. The universal general-to-spherical and Galois
implications proved below remain valid; the existence of one unitary model
does not assert that every categorification of this ring is unitary. Its
braided and braided-Morita exclusions also remain valid.

The earlier four-case sphericalization result is proved in
[`pivotality/PROOF.md`](../evidence/rank8_research_20261022/pivotality/PROOF.md).
For `R8_3_982`, `R8_3_1768`, and `R8_3_1795`, the full parity enumeration
modulo a justified basis-sign gauge gives respectively 3, 28 and 42 sign
classes. All classes except the original tensor are excluded by exact
spherical-dimension character obstructions. For `R8_3_3472`, choosing the
positive second-indicator lifts in sphericalization gives modulo-four
constraints; the complete oriented associativity search returns only the
original tensor. The spherical-section criterion then supplies a spherical
structure in all four cases. Complete character calculations place its
dimension character in the FP Galois orbit. These are computer-assisted
proofs, with an independently replayed enumeration and arithmetic audit.

`R8_3_65` has left the unresolved inventory: the
[new pointed-induction Fourier criterion](../evidence/rank8_research_20261022/r65/PROOF.md)
excludes every pointed associator class, and hence every general
categorification. Its earlier implication argument is retained here as
part of the proof history.

`R8_3_1795` is also excluded from general categorification: the
[order-two Fourier-packing criterion](../evidence/rank8_research_20261022/pointed_followup/PROOF.md)
excludes all sixteen indicator branches, covering both pointed associators.
The general-to-Galois-pseudo-unitary gate below is an essential part of that
exclusion. Their closed case pages and tensor downloads are retained.

`R8_3_3472` is now excluded from general categorification by the
[complete center and rotation-indicator proof](../evidence/r3472_exclusion_20261022/README.md).
The complete 372-assignment domain is excluded by exact STS constraints and
a final twist-orbit contradiction. The terminal arithmetic certificate contains
1,648 integer-bound deductions and an exact rational separating inequality.
The sphericalization and Galois gate above makes this a general exclusion.
Its earlier necessary-condition witnesses remain in the retained research
history; its case address and fusion-tensor download are unchanged.

For `R8_3_65`, the two distinct FP dimensions are 1 and
`d = (11 + 5 sqrt(5))/2`. Apply Schopieray's **published** Lemma 3.1,
[Categorification of integral group rings extended by one dimension](https://doi.org/10.1112/jlms.12789),
which gives a pseudo-unitary Galois conjugate. Transport its spherical structure
back to obtain the same-category consequence. The published statement is used
instead of the stronger wording in the original arXiv version.

For the three self-dual rings, the pivotal ⇒ spherical implication is an
immediate consequence of the dual permutation recorded in their exact tensors.
For any pivotal structure, a simple object is isomorphic to its dual, so their
pivotal dimensions agree. By additivity this holds for every object and is the
sphericality criterion in Etingof–Gelaki–Nikshych–Ostrik,
[*Tensor Categories*, Definition 4.7.14](https://math.mit.edu/~etingof/egnobookfinal.pdf).
Here, in fact, **every** pivotal structure is spherical. The new sphericalization argument above now supplies such a structure; this elementary observation alone did not do so.

For `R8_3_982`, the same implication follows even though some simples are not
self-dual. In a pivotal fusion category the slope (left dimension divided by
right dimension) defines a monoidal automorphism of the identity, and the
category is spherical exactly when every slope is 1; see Bruguières–Virelizier,
[*On the center of fusion categories*, §4.3](https://arxiv.org/html/1203.4180v2#S4.SS3).
Write `s_i` for the slope of `X_i` in the displayed zero-based tensor. Since
`X_1* = X_2`, the product
`X_1 X_2 = X_0 + X_1 + X_2 + 2 X_3 + 2 X_4 + 2 X_5`
forces `s_0 = ... = s_5 = 1`. The product
`X_1^2 = X_1 + X_2 + 2 X_3 + 2 X_4 + X_6 + 2 X_7`
then forces `s_6 = s_7 = 1`. Thus every pivotal structure is spherical.

The existing exact character table for `R8_3_982` has eight distinct characters
over `Q(zeta_24)`. Precisely four agree on dual basis elements: the rows numbered
0, 1, 6 and 7. These four are exactly the Galois orbit of the FP character.
A spherical dimension character must agree on duals, so Galois transport takes
it to FP dimensions and makes the transported category pseudo-unitary.
The finite calculations are replayed by `verify_scope_consequences.py`.
Combined with the new sphericalization gate, this proves an equivalence of **general, pivotal, spherical and pseudo-unitary existence** for this ring. The pseudo-unitary category may be a Galois conjugate of the original one.

The other three cases have the same Galois conclusion, now preceded by a general sphericalization gate. For
`R8_3_1768` and `R8_3_3472`, every character outside the FP Galois orbit vanishes
on a simple basis object. Such a character cannot be a pivotal dimension
function, since pivotal dimensions of simple objects in a fusion category are
nonzero. For `R8_3_1795`, the remaining non-FP characters have global dimension
20, 10 or 4. The dimension-4 characters have zero entries. In the other two
cases, the ratio of that dimension to the FP formal codegree has quadratic
norm `20^2/3600 = 1/9` or `10^2/3600 = 1/36`, respectively. These cannot be
norms of algebraic integers, contradicting
[Ostrik, *Pivotal fusion categories of rank 3*, Theorem 2.13 and Corollary 2.14](https://arxiv.org/abs/1309.4822).
Thus a spherical dimension character must lie in the FP Galois orbit in each
case. The verifier checks the complete exact character tables, their identities,
the FP orbit and these exclusions. Together with the new gates this establishes the general-to-pseudo-unitary existence reduction. It does not establish unitarity for a pseudo-unitary category.

## Maintenance

Update `categorification_scope.json` when a proof changes one of these statuses
or implications. Its `cases`, `closed_cases` and `realized_cases` fields keep
current unresolved profiles, retained exclusions and retained realizations
distinct. A unitary realization marks all five existence levels as realized
without adding an unsupported universal same-category implication.
Replay the conditional consequences with
`python3 site/verify_scope_consequences.py` (requires SymPy).
Then run `python3 site/build_cases.py --classification .` from
the repository root and `npm run check` from `site/`. The checks validate the
current inventory, evidence hashes, hierarchy closure, strongest-exclusion
selection, and the separation between same-category and Galois implications.

# All-Morita restrictions for R8_3_3472

`manuscript.tex` proves the following necessary statements for **every** complex
categorification of the source ring and **every** Morita partner:

* The center has no nontrivial invertibles. This follows directly from the
  source tensor: only the unit is invertible and every nonunit Xi occurs in Xi².
* The FP dimension field of every partner is Q(sqrt(2)), with all simple
  dimensions a+b sqrt(2), a,b nonnegative integers.
* Their exact moments are sum(a²)=350, sum(b²)=175, sum(ab)=245.
* The integral-dimensional subcategory is pointed of order **1 or 7**.
  Strong Lagrange and parity exclude order two. Strong Lagrange, a complete
  seven-type moment enumeration, Frobenius reciprocity and a forced impossible
  rank-ten subcategory exclude order five.
* Order seven forces the dimension profile 1^7,(7+5sqrt(2))^7.
* The previously retained seven spectra of the first conditional rank-two
  module branch reduce to four (saved indices 1,2,4,10).

No pivotal, spherical, pseudo-unitary, braided, or rank-two-module-lift
assumption is used for these all-Morita restrictions. Neither a category nor
an associator is constructed, and R8_3_3472 remains unresolved.

The order-five argument keeps **all four** arithmetic profiles after strong
Lagrange, rather than assuming only one profile. Three force a subcategory
of dimensions 1^5,(1+sqrt(2))^5. Its inversion-action ring violates the
integrality of a uniform coefficient 2/5. Its commuting-action alternatives
contain either the rank-two n=2 ring or a formal codegree with irreducible
polynomial

    f^4 - 55*f^3 + 1000*f^2 - 7250*f + 18125,

which fails the d-number test (55^4 mod 18125 = 15625).

Run from the repository root:

```sh
python3 evidence/r3472_focus_20261022/morita/verify.py
python3 -O evidence/r3472_focus_20261022/morita/verify.py
```

The standard-library verifier checks the input multiplication tensor and its
positive FP character, source hashes, exact arithmetic bounds, complete
moment enumeration, and formal-codegree obstruction. Both modes give the
same receipt. `verification.json` is the saved receipt. Mathematical arguments
remain in `manuscript.tex`; computation is not substituted for their
categorical hypotheses.

Primary references:

* M. A. Alekseyev, W. Bruns, J. Dong, S. Palcoux, *Classifying integral
  Grothendieck rings up to rank 5 and beyond*, Letters in Mathematical Physics
  116:141 (2026), Proposition 5.7 (Strong Lagrange),
  DOI 10.1007/s11005-026-02164-7.
  https://bimsa.net/doc/publication/14753.pdf
  (The earlier preprint numbered this result Proposition 4.12.)
* V. Ostrik, *Fusion categories of rank 2*, Math. Res. Lett. 10 (2003),
  177–183, Main Theorem. https://arxiv.org/abs/math/0203255
* V. Ostrik, *On formal codegrees of fusion categories*, Math. Res. Lett. 16
  (2009), 895–901, Theorem 1.2 and Lemma 2.7.
  https://arxiv.org/abs/0810.3242

The dimension-field descent lemma is proved directly. It uses the spectral
radius bound and tensor automorphisms of the identity, rather than a
classification theorem or the simplicity of the center.

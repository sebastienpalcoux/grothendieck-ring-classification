# A uniform obstruction to braided Morita representatives

## Minimal-image criterion

**Proposition.** Let C be a fusion category with nonintegral global
Frobenius–Perron dimension. Suppose that every proper fusion subcategory of C
is integral. If C is categorically Morita equivalent to a braided fusion
category, C itself admits a braiding.

**Proof.** Let M be a braided Morita representative. Its braiding supplies a
fully faithful tensor functor M → Z(M). Compose it with the braided
equivalence Z(M) ≃ Z(C) and the forgetful functor to obtain F: M → C.
Let E be its tensor image, including all direct summands. The induced functor
M → E is dominant, and tensor functors preserve Frobenius–Perron dimensions.
If E is proper, its integrality implies that every simple object of M has
integer Frobenius–Perron dimension. Then FPdim(M) is an integer, contrary to
FPdim(M) = FPdim(C). Hence E = C. A dominant tensor functor between fusion
categories of equal global Frobenius–Perron dimension is an equivalence.
Transporting the braiding along this equivalence proves the assertion. ∎

The hypothesis concerns the global dimension, not merely the presence of
nonintegral simple dimensions. No pivotal, spherical, pseudo-unitary, or
unitary structure is assumed. The standard ingredients are in Etingof–Gelaki–
Nikshych–Ostrik, *Tensor Categories*: Proposition 6.3.4 (dominance and equality
of dimension), Corollary 7.16.7 (Morita invariance of dimension), and Theorem
8.12.3 (centers and Morita equivalence). The author's final version is
[available here](https://math.mit.edu/~etingof/egnobookfinal.pdf).

## Application to the eight rank-eight cases

`verify.py` enumerates every unit-containing subset of each original based
ring, tests duality and multiplication closure, and verifies that every
proper based subring is pointed. Independently, it computes the characteristic
polynomial of the Casimir multiplication matrix and isolates its largest
real eigenvalue. In every case its irreducible factor has degree greater
than one, proving that the global Frobenius–Perron dimension is irrational.

Thus, for each of `R8_3_65`, `R8_3_928`, `R8_3_941`, `R8_3_982`,
`R8_3_1154`, `R8_3_1768`, `R8_3_1795`, and `R8_3_3472`, an exclusion of
braiding automatically excludes every braided Morita representative in
the same scope. Combining the general sphericalization reductions in
`../pivotality/PROOF.md` with `../../../site/BRAIDED_CATEGORIFICATION.md`
gives the general, unconditional application for all eight rings.

This criterion rules out constructions from braided categories by passing
to a Morita dual. It does **not** exclude arbitrary unbraided categorifications
or Morita partners that are themselves unbraided.

Replay from the repository root:

```sh
python3 evidence/rank8_research_20261022/braided_morita/verify.py
```

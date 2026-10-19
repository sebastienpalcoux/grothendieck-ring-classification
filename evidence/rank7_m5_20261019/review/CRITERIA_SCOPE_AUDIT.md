# Rank-seven multiplicity-five criteria review

This review concerns complex fusion categories. It does not promote a
pseudo-unitary obstruction to a general obstruction without a separate
reduction covering every categorification.

## One-spectrum scan

Source: Z. Liu, S. Palcoux, Y. Ren and G. Vercleyen, *Triangular Prism
Equations and Categorification*, arXiv:2203.06522v5, Theorem 6.8,
equations (6.13)--(6.18), printed page 29.

The scanner `one_spectrum.cpp` implements the six nonzero boundary
coefficients, the unique multiplicity-one spectrum, the vanished opposite
channel, and the three disjunctions forcing the three right-hand associator
entries to be nonzero. `one_spectrum.py` independently evaluates the scalar
integer formulas for each returned witness. No categorical dimensions are
used. Thus the complex application assumes neither pivotality nor a
nonzero value for any chosen categorical dimension. The paper states
broader field scope, but this release makes only the complex claim needed
for its classification.

All 5805 rings of exact multiplicity five were scanned. There are 66
witnesses; none belongs to the 178 survivors of the basic pipeline.
Consequently these witnesses provide independent confirmation but no
additional first-successful-stage exclusions. The controls test all 27
entries of the then-current positive model catalog (zero false exclusions),
recheck the 66 certificates, reject their zeroed-index corruptions, and
verify 198 equalities with the dual-rotated versions of the three scalar
conditions. See `one_spectrum_results.json`, `one_spectrum_controls.json`,
and `one_spectrum_additional.json`.

## Noncommutative maximal near-group exclusion

The remaining noncommutative basic survivor is `R7_5_4812`. In the uploaded
source labeling its invertibles are `0,1,2,3,5,6`; the other simple is `X=4`.
Its square is `[1,1,1,1,5,1,1]`, and every invertible fixes X on both sides.
Thus it is the near-group ring K(G,5), |G|=6. The products `1*3=6` and
`3*1=5` prove that G is nonabelian, hence noncyclic.

The relevant theorem is **D. Nikshych and V. Ostrik, Appendix A,
Theorem A.14(ii)** in V. Ostrik, *Pivotal fusion categories of rank 3*,
Moscow Mathematical Journal 15(2) (2015), 373--396;
arXiv:1309.4822, printed page 25. It asserts that a near-group category
C(G,n) with n=|G|-1 has cyclic G. No abelian assumption occurs in part
(ii). Appendix A explicitly starts with general semisimple rigid
near-group categories; its reduction to a pseudo-unitary Galois conjugate
is recalled in Section A.1. Therefore the conclusion excludes arbitrary
complex categorifications of this tensor.

Do not apply Siehler's original Theorem 1.2 to nonabelian G without this
replacement: Nikshych--Ostrik explicitly warn that Siehler implicitly
assumes G abelian (their Example A.1(iv)). The premise certificate and
checker are maintained in the sibling `models/` directory.

## Scope of existing reusable tests

The prime-order cyclic-stabilizer lemma was applied uniformly to the 178
basic survivors, producing 49 general exclusions (47 at p=2, one at p=3,
one at p=5). It recovers all five old manuscript examples and excludes
none of 30 known positive controls. The new cyclic isotypic-summand
integrality generalization then gives 54 exclusions on that same initial
frontier, including five order-four applications beyond the prime-order
pass. Its proof avoids projective representation classification: the
isotypic summand itself is an object of the Morita dual, so its normalized
Frobenius--Perron dimension is integral. See `CYCLIC_ISOTYPIC_PROOF.md` and
`cyclic_isotypic_controls.json`. Counts are independent scan counts and
must not be added to other stages without removing overlap.

* A zero-/one-spectrum witness and a certified excluded fusion subring
  obstruct every complex categorification.
* Formal-codegree d-number tests, cyclotomicity, and Frobenius--Perron
  subcategory dimension divisibility likewise have general scope. At rank
  seven the noncommutative Casimir argument is justified by the unique
  possible matrix block M2(C), whose scalar formal codegree is integral.
* Character dimensions, central induction, twist moments and
  Frobenius--Schur indicator inequalities normally have the spherical or
  pseudo-unitary hypotheses stated in their proofs. They become general
  exclusions only after a complete signed-sphericalization tree or an
  independently proved structural reduction eliminates all other branches.
* A finite search budget, numerical infeasibility, a candidate modular
  datum, or absence from a model registry is not a general exclusion.
* A successful fusion-tensor comparison to a proved categorical
  construction establishes existence. Dimension agreement alone does not.

Primary sources consulted on 2026-10-19:

* https://arxiv.org/pdf/2203.06522v5
* https://arxiv.org/pdf/1309.4822
* https://arxiv.org/pdf/2208.07319
* https://homepages.gac.edu/~jsiehler/Articles/near-group-categories.pdf

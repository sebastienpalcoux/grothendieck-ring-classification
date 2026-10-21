# Reproducible bounded model investigation

`model_search_audit.py` reconstructs 72 explicit rank-eight based tensors:
30 Deligne products of all 15 catalogued rank-four positive tensors with
Vec(C2) or Fibonacci; 28 crossed tensors for every unit-preserving
involutive based-ring automorphism of those rank-four rings; three
SU(2)/PSU(2) tensors; two Frobenius-group tensors; Rep(PSL(2,11)); seven
other independently certified constructions; and the twisted A6/A5 model.
Every constructed tensor is checked for unit, nonnegative integrality,
duality, reciprocity and associativity. Maximum multiplicity first rules
out impossible matches, and all remaining comparisons use the full based
tensor with an explicit unit-preserving basis map.

The 28 abstract crossed tensors are **not** automatically categorical
constructions. A based-ring automorphism need not lift to a coherent
tensor action. In particular the match to R8_3_436 is recorded only as an
abstract ring match, not a positive categorification. The other matches
recover the 14 independently certified positive models.

Every one of the 277 baseline survivors receives a source-bound record
with the following separate investigations:

* 28 integral cases have positive integer dimension characters checked
  in all 64 products. Each of the other 249 cases has a positive integer
  test vector giving strict rational Collatz–Wielandt bounds between
  consecutive integers for one simple dimension. Numerical profile data
  only suggest a test vector; the saved bounds themselves are exact.
* Noncommutativity or a verified nonintegral simple dimension rules out
  an ordinary finite-group representation ring. Integral commutative
  cases are explicitly left undecided by this elementary filter.
* Pointed and ordinary Tambara–Yamagami categories have maximum fusion
  multiplicity at most one, so cannot directly give these exact-M3 rings.
* The verifier computes the adjoint based subring and all central
  invertibles. If the adjoint subring is full and the unit is the only
  central invertible, then any categorification has no nontrivial
  invertible object in its center. Indeed an invertible central object
  forgets to a central invertible of the category, and the forgetful
  kernel is Hom(U(C),C*), trivial when the adjoint category is full.
  A nontrivial cyclic-prime extension or equivariantization supplies
  a central Rep(Cp), so none can be a Morita source in this situation.
  This filter applies to 24 of the baseline rings. It does not obstruct
  arbitrary fusion categories.
* Each record includes the numerical dimension-ratio leads from the
  independently regenerated bounded scan of 1505 classical WZW models.
  These remain explicitly heuristic leads, not tensor matches or
  categorical exclusions.

For all 24 profiles with quartic global-dimension polynomial, an extra
exact computation compares the actual source Casimir characteristic
polynomial with `x^2-480x+2304`, the minimal polynomial of the F4 level-3
dimension `240+96 sqrt(6)`. None is divisible by that polynomial.
Therefore none can have that global dimension, which is Morita invariant.
This rules out that specific proposed source. The accompanying
`psl2_11/f4_level3_attempt.py` independently computes its dimension by the
quantum Weyl formula over Q(zeta_48).

Two targeted receipts are retained with their full current proofs:
the unitary PSU(3)_7 Morita-family investigation for R8_3_65 and
R8_3_1453, and the determinant-trivial spin anchor distinguishing the
constructed mu2 A6/A5 model from R8_3_3344. Other historical targeted
attempts whose complete source receipts were unavailable after the
workspace reset are not represented as newly verified results here.

The audit is a finite model-family investigation. Failure to match any
of these constructions is not a theorem of noncategorifiability and
does not prove that every conceivable construction has been exhausted.

Replay:

    python -O evidence/rank8_m3_20261021/models/model_search_audit.py

Default execution compares every regenerated field to the saved JSON.
Use `--write` only to explicitly regenerate the receipt.

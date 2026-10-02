# Reconstruction audit, 2026-10-02

The twelve general exclusions were retained in the recovery decisions. Their
original new proof programs were pruned, so the present proofs and premise
checker were reconstructed from the source tensors and independently revisited
arguments. This receipt does not pretend that the old inaccessible source
files were recovered byte for byte.

The following points were checked explicitly rather than inherited from the
retained summary.

* The eight-prime family has two different invertible groups: R213 is C4,
  R70/R358 are V4. The corrected proof gives the immediate C4 contradiction
  after constructing the order-eight representation subcategory.
* Both second-descent dimension partitions are complete. At dimension ten,
  the pointed case is excluded using its unique invariant C2 quotient, and
  six invertibles are excluded by subcategory divisibility. At dimension 34,
  a dimension-four simple is excluded by Frobenius divisibility. The smaller
  category has no faithful grading because a prime-dimensional neutral
  subcategory would need more invertibles than exist.
* The order-five pointed Brauer–Picard possibility is checked for both
  groups of order four, after a rank-one module trivializes the pointed
  associator. Their orthogonal groups have orders four and 72.
* The dimension-five strictification retains arbitrary pointed associators
  and group-action coherence: an invariant mu5 cocycle is obtained by
  coprime averaging, and the relevant H2 groups remove tensorator and
  coherence multipliers. No projective stabilizer was silently replaced by
  an ordinary representation.
* The dimension-96 new branch counts **left module** equivalence classes.
  Repeated left classes make the relative quotient a regular module of
  rank four, contradicting the third rank-one grading component. Different
  right actions therefore cannot evade the pigeonhole argument.
* The dimension-54 argument first retains the outer tensorator class; only
  the order-two condition and odd cohomology force it to zero. Its resulting
  central -I action on the hyperbolic group cannot invert an order-three
  component class.
* The dimension-310 proof uses all closed source subrings to constrain the
  identity double coset. Sylow31 normality and the D10 commutator replace
  the earlier unnecessary Frobenius-group argument, retaining arbitrary
  outside projective multipliers.

Primary PDF statements checked during reconstruction: ENO0809.3031
Definition1.2/Proposition4.4, Theorems1.5,1.6,9.2; ENO0909.3140
Corollary1.2 and Proposition9.3; Burciu–Natale1206.6625 Corollary2.13;
DGNO0906.0620 Theorem4.18/Proposition4.19; ENOmath/0203060 Corollary8.30.
The latter, rather than an imprecise reference just to Theorem8.28, is
the prime-dimension pointed statement used here.

Normal and optimized premise checks both pass in less than one second,
including all full-tensor source bindings and the two altered-data
rejection controls. No mathematical gap requiring a status reversal was
found in this reconstruction. This is a mathematical reconstruction audit,
not an independent proof-assistant certification.

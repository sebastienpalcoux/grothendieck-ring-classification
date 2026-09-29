# Independent audit of the continuation

The following checks were performed independently of the scripts' authors.

* The unrestricted signed-sphericalization enumeration for R6_3_215 was
  repeated without modulo-four indicator constraints. It returned 1,480
  tables in 274,655 search nodes, forming 63 sign-gauge orbits. One orbit
  consists of the 32 gauges of the original ring. Every character component
  of every other orbit was rejected: 228 zero-dimension and 43 norm
  obstructions. The final frozen verifier reproduces these figures under
  `python -O`.
* The passage from a gauge-original signed quotient to sphericality was
  checked categorically: after changing lift signs, the two-lift
  multiplicity sum and difference both equal the original coefficient.
  Opposite lifts never occur in products, giving a full tensor subcategory
  whose projection is a tensor equivalence. The only everywhere-nonzero
  dimension-character orbit is the Frobenius–Perron quadratic orbit, so a
  Galois conjugate is pseudo-unitary. This establishes a reduction, not
  existence or nonexistence.
* For the actual cyclic-eight quotient, all 3,872 coefficient identities
  of the canonical central restriction and all 48 cross-Gram entries were
  checked with integers. The six-object module enumerator and small-algebra
  dimension verifier both pass under `python -O`. The s=7 to s=1 Morita
  transformation, the possible alternative lower block, and the unit
  internal-end exception are addressed explicitly in
  `cyclic8_morita_exclusion.md`. That memo retains its specified source and
  induction-data hypotheses.
* The original small-algebra list in the second-algebra argument must
  include 3d-2. Its norm is -53, so the omission does not change the
  contradiction. The exhaustive corrected list is stored separately.
* All ordinary rotation multiplicities through exponent 136 and all
  generalized central rotation multiplicities through exponent 8 pass for
  the supplied modular datum. These are necessary tests only. The actual
  source-category obstruction shows why passing them cannot establish
  a categorical lift.

The new higher-multiplicity exclusions audited earlier are
R6_4_162, R6_8_2945 and R6_8_3071. For the first, an independent scan of
all 16,612 input tensors reproduced all 257 stored rank-three subring
certificates. For the last two, the exact anti-invariant module equations,
strict Perron bound, reconstruction polynomials and final integral-matrix
contradictions were checked independently. No mathematical gap was found.

None of these audit conclusions resolves the remaining general existence
question for R6_3_215.

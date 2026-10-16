# Independent audit of the four-case dihedral reduction

I read `work/unified/two_dimension/FOUR_RANK7_DIHEDRAL_REDUCTION.md`
and independently checked the categorical logic.

- A fixed simple trivializes the C2 pointed associator. The indicated
  multiplicity-one components of XY and YY* force the three HxH
  projective classes to split. Thus the first dual has exactly eight
  invertibles and eight noninvertibles of dimension t.
- The inverse algebra is supported on the two invertible bimodules
  whose underlying object contains the original unit. The restriction
  of the Morita context to the pointed category is legitimate.
- If the order-two inverse subgroup were normal, every double coset
  would contribute two ordinary irreducibles because H²(C2,C*)=0.
  The resulting rank-eight pointed dual contradicts the integral
  rank-five subcategory. Therefore the group of eight invertibles is
  D8 and the subgroup is a reflection subgroup.
- An intersection of inverse left and right reflection stabilizers of
  order two would give dimension-t simples. Their absence forces the
  mixed automorphism to exchange the two reflection conjugacy classes.
- The general two-dimension Galois pseudo-unitarity bridge and the
  forgetful-image formal-codegree field condition correctly exclude
  the exceptional normalized ring: its quadratic Casimir factor has
  roots 48+/-16 sqrt(6), outside Q(sqrt(5)). Dividing by a representation
  degree cannot remove the field discrepancy.
- For L=<s>, phi(s)=rs, the double orbit of rho contains
  {1,s,rs,r^{-1}} rho. With a=1 it is self-dual; with a=r² duality
  exchanges this orbit and its complement. This confirms the stated
  duality distinction in the inverse rank-seven ring.

The exact enumeration was replayed to a separate output at
`work/unified/rank7_structural/d8_independent_replay.json`. It found
24 unnormalized systems and five normalized forms, with the displayed
Casimir polynomials. I inspected the coefficient constraints and basis
normalization; no completeness gap was found. The current exploratory
script should be supplemented by source-tensor binding and full fusion
identity verification before inclusion as a publication certificate.

No new classification decision follows from this reduction. It leaves
four extension families, with their actual associators and coherent
extension data still to be supplied or obstructed.

## Publication replay

The final source-bound `verify_four_case_dihedral.py` was independently run against the repository on 16 October 2026. Its receipt `four_case_dihedral_independent.json` reports PASS, all four sources, 24 raw systems, five normal forms, and four surviving extension families. Full tensor and rank-eight subring checks passed. This remains a structural reduction with no classification change.

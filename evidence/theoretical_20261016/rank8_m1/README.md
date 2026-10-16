# Multiplicity-one rank-eight frontier: research notes, 16 October 2026

No authoritative decision ledger is changed here. R8_1_9, R8_1_18, and
R8_1_49 remain unresolved by this work.

## New theoretical result

`proof.tex` proves that the nontrivial invertible of any
pseudo-unitary categorification of the 2D2 rank-four fusion rules has no
central lift. The proof treats boson, fermion, and semion possibilities
separately. The fermion case reduces to a rank-six ring and gives a direct
two-moment contradiction; it needs no unitarity classification and no
associator search. The published two-FP-dimension Galois reduction extends
the result to arbitrary complex categorifications of that ring.

`verify.py` constructs the rank-six ring exactly. Its
output agrees with census R6_4_373 via permutation
(0,1,4,3,2,5), interpreted as census label -> our representative label.
All 216 coefficients are matched against `rank6_source.json`, itself checked
against the restored original census. Its existing decision certificate is
in `supplements/rank6/data/decisions.json`; the new argument uses neither the
signed search nor the three-profile Gram enumeration in that certificate.

The first draft of the moment argument used K=12+32d from the existing
three Gram profiles. The proof now uses the weaker uniform lower bound
K>=8+32d, avoiding that enumeration entirely.

Run `python evidence/theoretical_20261016/rank8_m1/verify.py` from the
repository root. The normal and optimized receipts both pass. The script
checks tensor hashes against the unchanged rank-eight ledger, complete
associativity, the conditional orbit tensor, all six characters/formal
codegrees, the induction coefficient, and the strict moment inequality.
It does not claim to machine-verify the categorical argument.

## What this does and does not settle at rank eight

Write d=2+sqrt(5). All three rings have four invertibles acting freely and
transitively on four noninvertibles of dimension d.

| Ring | Exact fusion profile | Established obstruction | Remaining gap |
|---|---|---|---|
| R8_1_9 | C4, phi=id; self-dual rho, rho^2=1+sum(g rho) | No braided categorification. A bosonic square quotient would have 2D2 rules, whose nontrivial invertible has no central lift. | Reconstruct the claimed central lift of g^2, determine its twist, and justify any additional lift descending to the quotient. |
| R8_1_18 | C4, phi=id; all noninvertibles non-self-dual, rho^2=g+sum(g rho) | No braided categorification. Conditional on the claimed central C4, a bosonic square gives an excluded rank-four quotient. | Reconstruct the central C4 claim and eliminate the remaining primitive-eighth-root twist / fermionic square case. |
| R8_1_49 | C2 x C2, phi swaps two involutions; self-dual rho, rho^2=1+sum(g rho) | Noncommutativity excludes braiding. A bosonic fixed-involution quotient has 2D2 rules and hence no central lift of its nontrivial invertible. | Reconstruct the fixed-involution lift and its twist; no additional descended lift has been proved. |

The old retained scalar-gauge argument claims unique central lifts of
g^2 (R9), all of C4 (R18), and the phi-fixed involution (R49).
Those certificates were removed from an old workspace and have not been
reconstructed; these claims must not be treated as freshly verified.

Conditional on the R18 central-lift claim, a bosonic square g^2 gives a
rank-four non-self-dual quotient with rule rho^2=f+2rho+2f rho. That ring
is excluded by the rank-four classification. Consequently a hypothetical
central generator must have primitive eighth-root twist, and its square
must be a fermion. This is a necessary condition, not a nonexistence proof.

For R9/R49, a central boson quotient has the self-dual 2D2 fusion rules.
The new theorem rules out any *additional descended central lift* of the
quotient's nontrivial invertible. It does not itself prove that such a lift
must descend. For a central fermion one cannot use ordinary
de-equivariantization; this remains a genuine gap.

## Primary sources checked

* Izumi, The classification of 3^n subfactors and related fusion categories,
  arXiv:1609.07604, Theorem 2.2: inversion is forced only for odd-order
  groups and odd multiplicity. Its proof does not exclude order four.
* Edie-Michell--Izumi--Penneys, arXiv:2108.01564: the 2D2 uniqueness
  theorem is unitary; the paper explicitly notes the issue in extending
  its tetrahedral argument to nonunitary categories.
* Schopieray, Categorification of integral group rings extended by one
  dimension, JLMS 108 (2023), DOI 10.1112/jlms.12789, corrected published
  Lemma 3.1: Galois pseudo-unitarity for two dimension values.
* Gannon--Schopieray--Yadav, On Haagerup--Izumi fusion categories,
  arXiv:2609.25185v1: odd-order HI constructions and Q-system hypotheses
  do not cover these order-four, non-inversion cases.

The standard ingredients in the new proof are Ostrik's formal-codegree
description of I(1), the Ng--Schauenburg first/second indicator identities,
central Tannakian condensation, and the rank-two classification. These
should be cited using the main manuscript's existing bibliography.

## Why inner conjugation does not construct the three residual rings

For any categorification Q of the 2D2 rules, put P=Q_pt and form the
relative center D=Z_P(Q), the intrinsic version of equivariantization by
inner conjugation. This construction is legitimate, but it cannot
realize R8_1_9, R8_1_18, or R8_1_49. By Gelaki--Naidu--Nikshych,
*Centers of graded fusion categories*, Algebra & Number Theory 3 (2009),
Remark 2.4(i), D is Morita equivalent to P tensor Q^rev
([primary paper](https://msp.org/ant/2009/3-8/ant-v3-n8-p05-p.pdf)).
Its invertible objects are exactly those of Z(P). For either associator
on P=Vec_C2^omega, this group is C2 x C2: the two lifts of the nontrivial
group element both square to the unit, as do the two character objects.
Thus D cannot have either C4-based ring R9 or R18. This statement does not
use a Frobenius--Schur indicator or a choice of associator class.

The 2D2 rules have trivial universal grading, so the no-central-lift
theorem gives Inv Z(Q)=1. Morita invariance of the center consequently
gives exactly four invertibles in Z(D). If D had the R49 rules, its
universal grading would also be trivial, making the forgetful map
Inv Z(D) -> Inv D injective: the kernel consists of tensor
automorphisms of the identity, or characters of that grading. Both
groups have four elements, so every invertible of D would have a
central lift and commute with every simple. This contradicts the
nontrivial permutation phi in R49. This closes only this proposed
construction; it neither excludes the three rings generally nor
classifies all actions on a 2D2 category. Their ledger decisions remain
unresolved.

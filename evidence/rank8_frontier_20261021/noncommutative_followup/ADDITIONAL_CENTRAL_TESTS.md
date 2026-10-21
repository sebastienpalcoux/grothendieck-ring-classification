# Exact central frames and forced indicators for the remaining three NC rings

These calculations use the independently reviewed central-image,
full-character S-row and joint-rotation methods in `../noncommutative/`.
They are necessary conditions on the pseudo-unitary representative.
The independently verified additional spherical/Galois gate makes them
necessary for general existence after Galois transport. They do not
assume or establish unitarity.

## Complete central-image and S-symmetry domains

Every central restriction column lies in the image of the induction
Gram matrix B=MM^T. The complete weighted distinguished-frame counts
are5,1,5 for439,455,567; all pass the earlier ordinary frame checks.
The full S-row formula

    S_(A_E,Z) = D/(f_E dim(E)) * chi_E(FZ)

is applied to all four scalar characters and the two-dimensional trace
character. All equal-codegree assignments are exhausted. Symmetry leaves
one frame in each case, with two assignments per frame. This includes
the M2 row with its factor dim(E)=2.

For R567 the two nonreal scalar characters do not lie in the real FP
field. The verifier adjoins i, embeds the original FP-field data exactly,
and constructs all characters in the resulting quartic field. All
character multiplication and orthogonality identities are checked; no
nonreal character is discarded. The S-symmetry calculation is algebraic
and does not require a positive embedding of the larger complex field.

## Complete height-six joint rotation domains

For each of439 and567 the unique full-S frame is frame2 in the complete
central-image list. Its complete high restriction domain has45 columns.
The height-six root-of-unity trace reduction has19 types. Including the
joint divisor-power rotation variables gives a932-variable,182-equation
rational nonnegative system for each indicator branch.

All eight indicator tuples allowed by duality and the known odd
multiplicity constraint are tested, not merely conjugacy-invariant tuples.
Fourteen exact Farkas certificates exclude seven branches per ring. Two
exact nonnegative rational witnesses certify the remaining relaxations:

| Ring | Surviving second indicators, original objects1 through7 |
|---|---|
| R8_3_439 | (0,0,1,1,1,1,1) |
| R8_3_567 | (0,0,0,0,-1,-1,-1) |

The default verifier performs no numerical optimization. It reconstructs
every rational system, verifies complete indicator and frame coverage,
and checks each exact dual or primal identity. Both normal and optimized
Python replays pass. A feasible relaxation is not a category or a
completed center fusion ring.

## Pointed associator consequences

The three odd S3 invertibles are objects3,6,7 for439 and5,6,7 for567.
The canonical pseudo-unitary indicator of an order-two pointed simple
detects the restriction of the associator to its C2 subgroup. Thus this
restriction is trivial for439 and nontrivial for567.

For both rings the C3 subgroup fixes each noninvertible simple. The
corresponding rank-one module over the pointed C3 subcategory supplies
a trivialization of the restricted3-cocycle. For439 both restrictions
are therefore zero. Restriction followed by corestriction multiplies
a class by the subgroup index, so2[omega]=3[omega]=0. Bezout's identity
then gives[omega]=0 in H^3(S3,C^*); no untested component is omitted.
Hence the full S3 regular algebra exists for439, while the nontrivial
C2 restriction prevents that untwisted regular algebra for567.
The precise source stabilizer and construction-route implications are
bound separately by the structural-model receipts. Galois transport
preserves triviality of the cohomology class and the C2 sign.

## Primary inputs and exact replays

The full character S row is Deshpande, arXiv:1611.04486, Equation39.
The joint rotation systems reuse the source-bound exact methods and
finite order/trace proofs of `../noncommutative/README.md` and its
`full_rotation.py`; this extension adds no numerical criterion.

```
python evidence/rank8_frontier_20261021/noncommutative_followup/additional_central_constraints.py
python -O evidence/rank8_frontier_20261021/noncommutative_followup/additional_central_constraints.py
python evidence/rank8_frontier_20261021/noncommutative_followup/additional_joint_rotation.py
python -O evidence/rank8_frontier_20261021/noncommutative_followup/additional_joint_rotation.py
```

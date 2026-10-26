# Complete general-complex exclusion of the twenty remaining D48 rings

The proposed conclusion is that none of the following based rings has a
fusion-category realization over C:

    R12_1_{130,146,151,175,216,239,244,277,289,296,
           303,319,407,410,421,424,433,523,526,538}.

This conclusion uses categorical converses and complete finite checks;
failure to find a model is not an exclusion criterion. The final decision
manifest records the independent audit status of each ingredient.

## Forced first equivariantization

The full frozen source tensors have positive integral dimension character
(1^8,2²,4²), total dimension48. Their adjoint closure is the entire ring,
so every categorification C has U(C)=1. The ENO theorem for dimensions
p^a q^b makes C solvable. A solvable construction of C ends in a prime
cyclic extension or equivariantization. A nontrivial extension contradicts
U(C)=1. In an equivariantization by Cp, Rep(Cp) embeds in C, so p divides
the order8 of its invertible group. Hence p=2 and C=D^C2, FPdim(D)=24.
The nontrivial object b of this central Rep(C2) is one of the explicitly
enumerated central invertible involutions of the source ring.

The portable quotient_reconstruct.py checks every such b, including all
56 possibilities across the twenty sources. The simple-orbit formula
for C2 equivariantization gives exactly four cases:

| b-fixed source simples | Type of D | Closure argument |
|---|---|---|
| two dimension2 and two dimension4 | (1^8,2^4) | Exhaustive quotient reconstruction; integral-Lagrangian theorem |
| no simple | (1^4,2,4) | Free-rank6 triality flattening |
| two dimension2 only | (1^8,4) | Near-group odd-Lagrangian theorem |
| two dimension4 only | (1^4,2^5) | Exhaustive rank9 reconstruction; pointed flattening |

No other pattern occurs. The following arguments close EVERY possible b,
which is essential: existence of one favorable central involution would
not justify choosing it as the actual Tannakian boson.

## Rank-twelve quotient branch

The invariant-orbit tensor of D is determined by the full source tensor.
quotient_reconstruct.py reconstructs all possible quotient fusion rules
from these orbit products without assuming census completeness. The
remaining coefficient search has at most three binary variables. The
only possible based rings are R351 and R513; all source/candidate basis
maps are exact and independently checked.

Every categorification of either quotient is group-theoretical, by the
complete neutral-associator and stable-Lagrangian arguments in
../audit_models/d24_c3_pointed_extension_lemma.md and the independent
R351/R513 proof notes. Their graded pointed Morita sources have groups
Gamma=A4 times C2 or SL(2,3). The integral-Lagrangian theorem in
../root/integral_lagrangian_lemma.md proves that every integral C2
extension of either pointed source is group-theoretical, for every
associator class. Applying it to the Morita equivalent crossed product
D crossed C2 proves that C itself is group-theoretical. This additional
step is required; equivariantization does not preserve arbitrary
group-theoretical categories without hypotheses.

## The other branches

free_rank6_branch.md proves that C is an order-four equivariantization of
a dimension12 triality category. The complete ring swap lemma and
Jordan–Larson classification identify its possible categories. The
three group-theoretical trialities have three central Lagrangians, so
their 2-group equivariantizations are group-theoretical. For the three
non-group-theoretical trialities, the audited soft-automorphism argument
forces a coefficient2 in any order-four equivariantization. Since the
source is multiplicity1, C is group-theoretical in this branch.

ng24_lagrangian_lemma.md treats every possible near-group quotient. An
abelian order8 group is impossible by the integral abelian near-group
classification and total dimension. For D8 and Q8 the general-complex
solvability/unitarity bridge allows the complete Izumi classification;
its actual models have pointed S4 Morita sources with associator inflated
from S3. Their centers have exactly three Lagrangians. Every C2 action
fixes one, making C group-theoretical.

rank9_quotient_branch.md reconstructs every quotient based ring using at
most eight bounded integer variables. Two of the four orbit types have
no associative lift. Each of the other two has exactly one based ring,
with U(D)=1 and a unique central involution fixing all five noninvertibles.
A second forced C2 de-equivariantization is pointed of dimension12.
Uniqueness of the central lift allows the outer action to descend,
giving C=E^P for pointed E and |P|=4. Such an equivariantization is
Morita equivalent to a pointed crossed product and is group-theoretical.

## Final contradiction

Thus any hypothetical categorification of any of the twenty source
rings must be group-theoretical. cohomology_coverage.md, together with
the complete subgroup-pair reduction, classifies ALL group-theoretical
categories with dimension48, U=1, and multiplicity-one type (1^8,2²,4²).
It includes every admissible associator and subgroup cochain; all104
categorical cases have independently checked complete simple lists and
fusion data. The only resulting based rings are R30, R417, R414 and R531.
Each of the twenty frozen source tensors is checked not to be based-ring
isomorphic to any of these four. This contradiction proves exclusion
from arbitrary complex categorification.

The earlier conditional blanket rejection of NG(G8,2) is explicitly
corrected, not reused. The completed proof includes the existing D8/Q8
categories and their possible equivariantizations. No unproved universal
group-theoretical premise, unitary-only classification premise, quotient
census completeness assumption, or ring-level lift of a tensor action is
used.

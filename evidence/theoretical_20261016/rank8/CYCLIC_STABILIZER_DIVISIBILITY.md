# Cyclic-stabilizer divisibility and three general exclusions

**Lemma.** Let H=C_p, p prime, be a pointed subcategory with trivial associator, and A=⊕_{h∈H}h. Suppose X is fixed on the left, Y on the right, and Z on both sides by H. If FPdim(Z)/p is not an algebraic integer, then p divides N_{XY}^Z.

**Proof.** The obstruction to giving X a left A-module structure is a scalar 2-cocycle of C_p, and H²(C_p,C×)=0; similarly Y has a right A-module structure. Therefore X⊗Y is an A-bimodule. The block of A-bimodules supported on the fixed simple Z is controlled by a twisted group algebra of C_p×C_p. Its simple projective representations have either dimension1 (trivial alternating class) or dimensionp (nontrivial alternating class). In the former case the associated simple bimodule has FP dimension FPdim(Z)/p, impossible by algebraic integrality. Thus every simple bimodule in that block has underlying object pZ. Decomposing the A-bimodule X⊗Y proves the divisibility.

The pointed associator need not be assumed separately whenever at least one simple is fixed by all H: its one-element orbit is a rank-one module category over Vec_H^ω, forcing [ω]=0. The lemma applies without pivotality or unitarity.

## R8_2_260 directly

Take H={0,1,2}, p=3, and X=Y=Z=b3. Every label3,4,5,6 is fixed by H on both sides, has FP dimension d=3+2sqrt3, and Norm(d/3)=−1/3. But N_{33}^3=2, contradicting the lemma. This proof replaces the longer A4 Morita-dual proof and uses no dimension12 categorical classification.

## R8_2_380 and R8_2_673

Let g be their nontrivial invertible (label3 and label1 respectively). Each ring has a full subcategory E with dimensions(1,1,2,2) and the Rep(D10) fusion rules:

| ID | E | g | free outside orbits |
|---|---|---:|---|
| R8_2_380 | 0,3,4,5 |3|{1,2}, {6,7}|
| R8_2_673 | 0,1,6,7 |1|{2,5}, {3,4}|

The outside dimensions are x=4+sqrt6 and y=3+2sqrt6, one orbit of each dimension. Since g fixes the two dimension2 simples, A=1+g exists. The category B=A-bimod(C) contains E'=A-bimod(E), pointed with group D10 by Etingof–Gelaki–Ostrik, arXiv:math/0304194v2, Lemma6.2 and proof of Theorem6.3. Each free outside orbit has cyclic stabilizerC2 in the left-right action, hence contributes two simples of its original dimension. Thus B has ten invertibles forming D10, two x-dimensional simples, and two y-dimensional simples.

The rotation subgroup H=C5 fixes all four noninvertible labels on both sides: each equal-dimension fiber has size2, and C5 has no nontrivial action on a two-element set. Therefore its associator is trivial and the cyclic-stabilizer lemma applies. We have

    Norm(x/5)=2/5,    Norm(y/5)=−3/5,

so every noninvertible multiplicity in XX* is divisible by5 for any x-dimensional simple X. Writing FPdim(XX*)=a+bx+cy, with a,b,c nonnegative integers, gives 5|b,c. But x²=22+8sqrt6, while the sqrt6 coefficient of a+bx+cy is b+2c. Thus b+2c=8, impossible modulo5.

This proves both general exclusions. The cocycles in each bimodule block are kept arbitrary; their possible projective dimensions, not an assumed triviality, supply the obstruction.

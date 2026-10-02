# Independent audit of the four dimension-48 exclusions

Status: APPROVED for general complex fusion categories.
Auditor: restore_r8_nonintegral, independent of the proof author.
Cases: R8_2_158, R8_2_186, R8_2_579, R8_2_682.

The categorical argument has no remaining gap after the revised proof
explicitly invokes the induced-module crossed-product statement in its
last Morita step. The exact classifier originally omitted the nontrivial
C4 action: [0,1,1,0] was not a homomorphism for cyclic addition. I
independently detected this, then replayed an isolated corrected
classifier with [0,1,0,1]. It has 100 oriented candidates, six valid
tables and exactly two eligible tables, R3_V4 and R3_C4. The two added
self-dual C4 tables have equal squares containing exactly one nonunit,
and cannot admit the required involution exchanging the nonunits.
The corrected author checker now explicitly tests the group-action
homomorphism and reproduces these counts normally and under Python -O.

The first de-equivariantization follows from two-prime solvability and
trivial universal grading. Jordan--Larson arXiv:0812.1603 Theorem 1.4
applies to R3_C4 over C, with no pivotal hypothesis, and excludes it.
The remaining R3_V4 category is C3 graded over Vec_V4; its rank-one
components trivialize the pointed associator.

The odd D-module can be de-equivariantized by the central regular
algebra 1+epsilon in D. This constructs an actual E-module, independently
of any extension of epsilon's half-braiding to the ambient category.
Its rank is one if epsilon swaps the two source simples, and four if
it fixes them. Cyclic stabilizer H^2(C2,C*) vanishes, so fixed simples
have precisely two algebra-module structures. The six Vec_V4 module
classes have ranks 4,1,1,2,2,2. Galindo arXiv:1010.5283v3 Proposition
4.1 and Theorem 1.1 apply to actual submodules. The regular rank-four
class and the two distinct rank-one component classes form a C3 orbit
of total rank six. The remaining rank-two classes are fixed or form
another total-rank-six orbit. Thus a rank-one E-module is impossible;
a rank-four E-module consists of two actual fixed rank-two summands.
Each supplies a coherent E-module extension.

Galindo Theorem 1.3 concerns the dual of the induced module, and yields
a semidirect C3 product with neutral Vec_V4. Its transported action
has order three. The tensor-automorphism kernel H^2(V4,C*)=C2 cannot
contain it. Its classes are therefore a pure group action; the remaining
coherence group H^2(C3,V4-hat) is zero by coprimality. The semidirect
category is untwisted Vec_A4, including a tensor section of C3. No
uncontrolled H^3(C3,C*) twist is silently removed here.

Nikshych--Riepel arXiv:1309.5026 Proposition 7.6 and Section 8.3 give
three A4 Lagrangians in the orbit of the canonical Rep(A4), hence each
has untwisted Vec_A4 pointed Morita dual. An involution fixes at least
one of these three. Galindo Proposition 5.3 requires invariance, rather
than a coherent module extension: the dual of the induced invariant
pointed module is a C2 crossed product with pointed neutral Vec_A4.
This supplies a pointed Morita group G with normal A4 and quotient C2.
Since A4 is centerless, its two outer actions give S4 or A4 times C2.
The latter has six identity-supported central characters for every
associator. Forgetting central invertibles is injective when U(D)=1,
contradicting only four invertibles in D. Thus G=S4.

S4 has only the normal abelian subgroups 1 and V4. The previously
audited square-order stabilizer criterion therefore makes every graded
extension of D integral, contradicting odd dimension 2sqrt(3). The
argument has no pivotal, spherical, pseudo-unitary or unitary premise.

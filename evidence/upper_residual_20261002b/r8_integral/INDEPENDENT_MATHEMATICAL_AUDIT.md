# Independent audit of the integral rank-eight proofs

Audited independently of the proof producer: `PROOFS.md`,
`R694_DIM28_GRADING_PROOF.md`, and `verify_integral.py`.
The primary theorem statements were checked in the actual papers:

- Kashina, [math/0004114](https://arxiv.org/abs/math/0004114), Theorems 1.1--1.2
  and Table 1, especially row 16.
- Jordan--Larson, [0812.1603](https://arxiv.org/abs/0812.1603), Theorem 1.1.
- Etingof--Nikshych--Ostrik,
  [0809.3031](https://arxiv.org/abs/0809.3031), solvability and integral pqr
  results.

## Approved general exclusions

**R41, R86, R162.** The rank-one odd component supplies a fiber functor on
the neutral category, and invertibility of that bimodule identifies its
dual with the neutral category. Both H and H* therefore have four grouplikes.
Kashina's Table 1 row 16 is the unique possibility, HC:sigma1, with neutral
fusion ring Rep(D16). Its invertibles are V4 and all 2-dimensional simples are
self-dual. The source invariants exhibited by the checker contradict these
properties. Opposite-category conventions do not change the rank, invertible
group, or duality invariants used here.

**R140.** A rank-one left module is sufficient to reconstruct a Hopf algebra;
an invertible bimodule is not needed for this exclusion. The resulting
dimension8 Hopf dual has cyclic grouplikes of order4. Kashina's Theorem 1.1
holds for every prime-power dimension, so it forces that Hopf dual to be C[C8],
which would have eight grouplikes. The contradiction is valid generally.

**R697, R808.** Solvability and a whole adjoint category force a final prime
equivariantization. The sign action and orbit/stabilizer formula correctly
give the descent types 1^2,2^8 at dimension34 and 1^3,3^10 at dimension93.
The supplied adjoint-dimension arguments rule out every proper divisor.
Thus the next descent is pointed of prime dimension. The unique central
lifts are justified by U(E)=1: the ratio between two half-braidings on an
invertible is a tensor automorphism of the identity. The outer action
preserves this canonical central Tannakian subcategory, so successive
equivariantizations combine into a group action. Equivariantizing the
preserved central subcategory supplies the claimed Rep(H) inside the final
category. For R697 its four invertibles force H=V4; a V4 action on C17 cannot
produce dimension4 equivariant simples. For R808 the embedded representation
subcategory forces H=S3, whose action on the cyclic group C31 kills the
normal C3 and contradicts the preceding nontrivial inner action.

**R694.** The stronger dimension28 lemma has been checked case by case.
Jordan--Larson applies with p=7,q=2; its non-group-theoretical exceptions
do not occur. A group of order28 is C7 semidirect P, P=C4 or V4, with image
in Aut(C7) either trivial or inversion. The subgroup orders 1,2,4,7,14,28
exhaust the group-theoretical possibilities. Normal cyclic stabilizers
yield pointed categories. For noncentral H=C2 the index2 subgroup C7H
provides the grading. For H of order14 the grading is support modulo H;
its nonpointed neutral case is Rep(D14). For H=G, Rep(G) has adjoint category
Rep(G/Z(G))=Rep(D14).

For H=P of order4, the cohomological normalization has no omitted mixed
term: positive cohomology of C7 is 7-primary, so higher P cohomology of
these modules vanishes. The remaining P class is zero by the module-category
condition. The map H^3(C7,mu7) to H^3(C7,C*) is an isomorphism, by the cyclic
cohomology calculation (or the power-7 exact sequence). Averaging and then
raising by |P|^{-1} modulo7 gives a strictly invariant cocycle in the same
class. Inflating the residual psi from P genuinely removes it by an identity
tensor autoequivalence. The kernel C2 then acts strictly trivially and grades
the equivariantization by its two characters. Its neutral category has the
Rep(D14) fusion ring. The identities X_i^2=1+epsilon+X_(2i) generate the whole
neutral category because multiplication by2 cycles the three nonzero C7
classes modulo inversion. Consequently that neutral category is exactly
D_ad, so U(D)=C2.

The final contradiction is particularly direct and valid independently of
any sign action on the original ring. The outer involution preserves D_ad
and permutes three 2-dimensional simples. An involution has a fixed point on
a set of odd cardinality. A fixed 2-dimensional object yields two distinct
2-dimensional equivariant simples: its stabilizer is C2 and H^2(C2,C*)=0.
The target ring has only one such simple. No pivotality, braiding,
unitarity, or assumed classification of all dimension56 categories enters.

## Approved unitary models

R143, R179, R244 and R289 use literal finite-group automorphisms of untwisted
graded Hilbert spaces. These are strict unitary actions, so the corresponding
equivariantizations exist. The orbit formula in the verifier correctly counts
the zero weight as a sum of regular stabilizer representations and nonzero
weights by one representative of each free orbit.

R237 is the representation category of the actual finite group AGammaL(1,8).
Its three linear characters and two inflated degree3 characters are standard
induced characters of C7 semidirect C3. The three degree7 characters arise
from the nonzero additive-character orbit with stabilizer C3; the fixed-point
condition a*r^(2^t-1)=1 and trace term Tr(v/r) agree with the induced-character
formula. Completeness follows from the stated degree-square sum. Thus the
exact orthogonality and multiplication checks concern genuine characters,
rather than a proposed character table.

## Fresh independent replay

Normal and optimized Python replays both pass. The independent receipts are
`independent_audit_normal.json` and `independent_audit_optimized.json`. They
rebind every exclusion premise to the complete census and independently
construct and compare all 512 coefficients of each of the five models.
No mathematical gap was found in the audited decisions. The separate R575
Hopf-pairing construction is outside the scope of this audit.

# Closing specified near-group and quantum-group construction branches

These are general-complex **construction-family exclusions**, not general
noncategorification decisions for R439, R567 or R721.

## A center-invertible obstruction

Let C be any fusion category whose only invertible basis object commuting
with every simple is1, and whose adjoint subcategory is all of C. Then
Z(C) has no nontrivial invertible objects. Indeed the forgetful tensor
functor takes a central invertible to an invertible of C commuting with
every simple, hence to1. A half-braiding on1 is a tensor automorphism of
the identity functor. On each simple it is a scalar lambda_i, and
lambda_i lambda_j=lambda_k whenever N_ij^k is nonzero. In particular it
is1 on every constituent of X_i X_i*, and therefore on the adjoint
closure. Thus all lambda_i=1. This argument uses neither positivity nor
a pivotal structure.

Both source rings R439 and R567 satisfy these two hypotheses, checked
from all512 coefficients in `known_model_routes.py`. Their invertibles
form S3, only the unit commutes with all simples, and their adjoint
closure is the entire ring. Braided centers are preserved by categorical
Morita equivalence; see Etingof--Nikshych--Ostrik, arXiv0909.3140v2,
Introduction, printed p3, and its references to Mueger and Schauenburg.

A faithful C2 extension has a nontrivial central invertible over1 given
by its grading character. A C2 equivariantization has its canonical
central Rep(C2). A dimension-two Deligne factor is pointed and also
supplies a nontrivial central invertible. These statements survive any
subsequent Morita change. In particular the rank-five known Izumi
equivariantization category cannot be Morita equivalent to either
source, even though its based ring is the sole surviving possibility in
the conditional full-S3 condensation calculation. This does not exclude
other associators on that based ring.

## The complete surviving SU2 dimension branch

The separately replayed infinite-level family sieve
`../noncommutative_followup/su2_all_frontier.py` has exactly one branch
for each of R439 and R567: one factor A12, the adjoint SU(2)_10 global
dimension, with total positive integer multiplier2. No other nonrational
factor or exponent occurs. The rational adjoint dimensions in the whole
candidate-level domain are A3=1, A4=2 and A6=6; the last cannot occur
here. Full SU(2)_10 itself is a faithful C2 extension of its adjoint
subcategory. Every other realization of the retained branch by the
specified operations uses exactly one dimension-two extension,
equivariantization or Deligne factor. Morita changes at any stages
preserve the center, and there is no second nontrivial integer operation
because the total multiplier is2. The preceding center obstruction
therefore excludes **all** models in this entire dimension-compatible
SU2/adjoint product family. This covers every ADE module-category Morita
dual of SU(2)_10 at once, without a rank-only identification.

The claim includes the actual operations of extensions,
equivariantizations, integer-dimensional Deligne factors and Morita
changes. A bare numerical multiplier does not by itself define a
categorical operation. Dimension-decreasing de-equivariantization,
arbitrary algebra condensation, other Lie types, and other construction
families remain outside this statement.

## The actual near-group inversion action and crossed product

Izumi1512.04288v2, Lemma13.1 (printed p118), Example13.10
(printed pp124--125), supplies actual automorphisms of the unitary
NG(C3,6) realization. At the normalized solution (x,0), the pair
(-id,R(pi/4)) and (id,L), L=diag(1,-1), preserve the solution.
Their product (-id,U), U=R(pi/4)L, has U²=I. Taking phase omega=1
in Lemma13.1 therefore gives an actual involution, not merely an
order-two outer class. It inverts C3 and fixes the noninvertible object.
Conjugation supplies a coherent strict tensor action as in the paragraph
before Lemma13.2. This is distinct from the object-fixing phase and
reflection actions behind the known rank-eight models274/334.

Its crossed product tensor is explicitly reconstructed in
`known_model_routes.py`: (a,e)(b,f)=(a theta^e(b),e+f), expanding the
near-group multiplication rho²=sum(C3)+6rho. All4096 associativity
equations and the C2 grading are verified. It cannot match R439 or R567:
its maximum coefficient is6, whereas both target tensors have maximum3;
also its neutral NG subcategory gives a nontrivial grading, whereas the
source adjoint closure is full. Thus this actual coherent action does
not give a source model. Its other possible Morita duals are not
identified merely by matching a rank-five based ring.

## All near-group dimensions for R721, with integer multipliers

For a near-group ring with group order n and rho²=sum(G)+m rho,
write d=FPdim(rho). If the global dimension D0=n+d² is irrational,

    Tr(D0)=4n+m²,       Nm(D0)=n(4n+m²).

The source dimension is D=136+32sqrt(17), with trace272 and norm1088.
If D=t D0 for a positive integer t, then necessarily

    n=4/t,             m²=256/t.

Hence t divides4. For t=2 the proposed multiplicity squared is128,
not a square. For t=1 one has n=4,m=16, and the two possible groups
are C4 and V4. For t=4 one has n=1,m=8, the impossible rank-two rule
rho²=1+8rho by Ostrik, math/0203255, Main Theorem (printed p1).
Rational near-group dimensions cannot match the irrational target under
an integer multiplier, so there are no missing cases.

`rank5_route_bindings.py` constructs both order-four tensors and matches
all125 coefficients to R5_16_1909 and R5_16_1653 respectively, then
freshly replays the frozen exact general exclusion proofs. The archive
SHA256 and source-to-constructor basis maps are in the receipt. This
closes all near-group source orders and multiplicities for this target,
with positive integer scaling and Morita changes. It does not cover
dimension-decreasing operations or arbitrary products of multiple
nonintegral source categories.

## Replay

Run the dependency verifiers, then `known_model_routes.py`, each with
normal and optimized Python. Every default invocation is read-only.
`rank5_route_bindings.py` extracts the pinned frozen verifier into a
temporary directory and executes the six source-bound proofs. No old
proof roots are edited.

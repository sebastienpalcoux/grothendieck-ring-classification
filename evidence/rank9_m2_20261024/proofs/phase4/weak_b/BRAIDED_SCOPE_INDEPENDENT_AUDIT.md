# Independent categorical audit of the integral braided refinements

Reviewed: `../integral/BRAIDED_SCOPE_THEOREMS.md` and its exact verifier,
24 October 2026. No general-complex exclusion is inferred here.

## Verdict

The three braided exclusions R9_2_12, R9_2_959 and R9_2_941 are supported
by the stated hypotheses and categorical arguments. The distinct
weakly-group-theoretical exclusion for R9_2_941 is also supported.
General existence of these three rings remains unresolved.

## Points checked adversarially

1. In a hypothetical central Rep(S3) descent, integrality of the smaller
   category follows from the equivariant-simple dimension formula: every
   simple dimension is a rational algebraic integer. No integrality
   preservation under arbitrary dominant functors is assumed.
2. All subgroups of S3 have trivial Schur multiplier. Hence the fixed
   invertibles contribute exactly two copies of the (1,1,2) packet;
   no projective exception changes the count. The remaining three
   dimension-six simples have just the three packet partitions stated.
   These give smaller-category types 1^20; 1^8,2^3; or 1^2,3^2.
3. In the pointed case, the Sylow-5 subgroup of a group of order 20 is
   unique and characteristic. The order-three subgroup of S3 acts
   trivially on it, contradicting the stipulated two fixed points.
   The other types violate subcategory dimension divisibility and the
   strong Frobenius property, respectively.
4. If the Müger center is nonpointed, the ring hypothesis puts the
   S3 representation ring inside it. A symmetric category of this ring
   is Rep(S3), because S3 has no central involution supporting a
   nontrivial super modification. Its inclusion supplies a fully
   faithful central functor, not merely an abstract ring match.
5. If the Müger center is pointed, each transparent invertible fixes a
   simple. Balancing in the canonical positive ribbon structure forces
   its twist to be one. This explicitly eliminates a super-Tannakian
   center; it is not silently replaced by a Tannakian center.
6. After quotienting the full center, the residual category is integral
   and nondegenerate. The equivariantization group has order dividing
   four, so all orbit indices and projective degrees are powers of two.
   Any simple below a dimension-six object thus has integer dimension
   divisible by three. Its square cannot divide 120/e, whose 3-adic
   valuation is one. Pseudo-unitarity supplies the positive spherical
   structure needed to identify categorical and FP dimensions.
7. Simplicity of R941 leaves only the symmetric and nondegenerate
   braided possibilities. The symmetric possibility contradicts its
   established exotic/non-group representation ring; the nondegenerate
   possibility contradicts 49 not dividing 504. ENO Proposition 9.11
   separately excludes a nonpointed simple weakly-group-theoretical
   categorification. Neither conclusion asserts general nonexistence.

The finite verifier was inspected: it exhausts all 256 unit-containing
basis subsets and checks dual closure, so its list of fusion subrings
is exhaustive. It checks all dimension equations, the S3 multiplication,
and the required fixed points. The equivariantization packet enumeration
contains all subgroup stabilizers and all base dimensions that can occur
under an object of dimension at most six.

## Primary-source checks

EGNO, *Tensor Categories*, author's final version, was opened and the
precise statements checked: Proposition 4.15.9, Theorem 8.23.3,
Proposition 8.23.8 and Proposition 8.14.6.
https://math.mit.edu/~etingof/egnobookfinal.pdf

ENO, *Weakly group-theoretical and solvable fusion categories*,
arXiv:0809.3031v2, Proposition 9.11 and the general-scope statements used
for solvability were checked.
https://arxiv.org/pdf/0809.3031

## Attempt to upgrade R12/R959 to general exclusion

The known central-induction dimensions of I(1) for these two commutative
rings are 1,4,4,5,6,20,20,30,30. Thus I(1) does not itself exhibit the
dimension-two central object required for the proposed Rep(S3). The
three dimension-six objects restrict to rank-one modules over the
rank-three S3 subcategory, so that subcategory admits a fiber functor.
This is useful information, but it does not extend its symmetric
braiding to a central half-braiding with all objects of C. No such
extension theorem has been proved in this continuation.

Accordingly the central-Rep(S3) hypothesis remains a genuine premise;
the braided results must not be promoted to general exclusions.

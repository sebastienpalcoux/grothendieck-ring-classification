# Three additional spherical/pivotal exclusions (not general exclusions)

Source: A. Schopieray, *The dimension block of a spherical fusion category*, arXiv:2609.35287v1, Theorem 5.1 (submitted 28 September 2026).

The following rank-seven frontier rings violate the theorem for their positive FP dimension and its conjugate:

| Ring | D | Norm(D) | quadratic discriminant | (1/D-1/D')² |
|---|---|---:|---:|---:|
| R7_3_695 | 420+70 sqrt(35) | 4900 | 140 | 1/35 |
| R7_3_783 | 120+30 sqrt(15) | 900 | 60 | 1/15 |
| R7_3_1015 | 120+30 sqrt(15) | 900 | 60 | 1/15 |

The theorem requires the final column to be at most the reciprocal of the discriminant (indeed at most 1/(e² times discriminant), where e≥1). Thus these dimensions are impossible for a spherical category.

To eliminate every other spherical dimension character, use Ostrik's theorem that δ/f is an algebraic integer for each formal codegree f. In each case δ, being the codegree of the one-dimensional categorical-dimension character, is an eigenvalue of the integral regular Casimir. For R7_3_695 the rational Casimir roots are5,7 and Norm(D)=4900, giving Norm(5/D)=1/196 and Norm(7/D)=1/100. For R7_3_783 and R7_3_1015 the rational Casimir roots are6,15 and Norm(D)=900, giving Norm(6/D)=1/25 and Norm(15/D)=1/4. These nonintegral norms exclude all rational alternatives. (For the noncommutative ring it is harmless to include the root6 from the matrix block in this necessary superset.) Thus δ must be D orD', both already excluded.

These spherical exclusions are also pivotal exclusions: all source objects of R7_3_695 are self-dual. In the sqrt15 rings the three invertible dimensions are1 by gE=E; the three orbit-object dimensions are equal, and the singleton is self-dual. Hence every pivotal dimension character satisfies dim(X)=dim(X*) for every simple, which makes the pivotal structure spherical.

No argument here forces an arbitrary categorification to admit a pivotal structure. General status therefore remains unresolved for these three rings. Passing to the full sphericalization alone scales δ by2; the strict factor4 violations become equalities and do not yield a contradiction.


The scope above is the scope of this argument alone. The independent
`C3_SIGNED_GENERAL_PROOF.md` proves that categorifications of R7_3_783
and R7_3_1015 must be spherical, and hence upgrades those two to general
exclusions. The independent `R695_GENERAL_PROOF.md` upgrades R7_3_695 by a
full-induced-unit compression equality and a modulo-four contradiction.

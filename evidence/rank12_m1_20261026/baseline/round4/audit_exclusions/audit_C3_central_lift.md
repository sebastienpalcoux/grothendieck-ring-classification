# R561/R628: independent audit of the central-C3 partial theorem

I read the complete `../c6/C3_central_lift.md` proof and its standalone
`verify_C3_sections.py`, and replayed the latter with Python `-O`. The replay
checks the two frozen input tensor presentations, trivial universal grading,
all 72 possible duality-compatible sections, exact cyclotomic resultants,
and the subgroup property of every survivor. It reports 66 excluded section
refinements and six subgroup-section survivors, three for each original
ring. No original ring is excluded by this audit.

## Categorical and arithmetic checks

The general-complex scope uses the previously audited two-FP-value
Galois-pseudo-unitary theorem. The coherent inner C3 action does not require
triviality of the original pointed associator: scalar coherence defects
cancel between the two sides of conjugation. Cyclic stabilizers have trivial
H2 with C* coefficients. Therefore all original simples have three
one-dimensional equivariant structures.

The group A of the eighteen invertible equivariant objects is a central
extension of C6 by K=C3; hence it is abelian and is either C18 or C6 x C3.
Its action on the eighteen noninvertibles is free, since a stabilizer must
project to the trivial original stabilizer and a nontrivial kernel character
changes the equivariant structure. The two actions differ by an automorphism
tau fixing K and inducing the identity modulo K. Comparing the unique
invertible term of r^2 a and r(ra) gives tau^2=1. Oddness of K then implies
tau=1. Thus no noncommutative refinement is omitted.

Changing r by K normalizes the pointed term of r^2 to 1 or the unique
involution. Duality imposes exactly S^{-1}=t^{-1}S on its six-element section.
The stated 9/27 section counts in each group follow from the inverse or
twisted-inverse pairs in C6; the script enumerates this full domain.

For every group character the two extensions to the based algebra have
product of formal codegrees 18^2(4+s^2/epsilon). The duality relation makes
s^2/epsilon nonnegative real, so the roots are distinct. In a pseudo-unitary
categorification both global-dimension/codegree quotients are algebraic
integers. The global dimension 360+108 sqrt(10) has rational norm 12960,
supported only at 2,3,5. A prime outside this set in the cyclotomic norm of
4+s^2/epsilon gives a negative valuation of the product quotient, even after
passing to the compositum. All 66 certificates exhibit such a prime using
exact polynomial resultants. This is a genuine arithmetic obstruction, not
a numerical approximation or incomplete optimization.

For each survivor the section B is a subgroup complement. Its adjoint
subcategory has simples B union Br, and the forgetful functor sends these
bijectively to the original simples. A C-linear tensor functor with this
property is fully faithful and essentially surjective. Hence it gives the
actual tensor equivalence E_ad -> C used in the argument.

## Central lifts and an explicit closure justification

The inner-action equivariantization can be viewed as a relative center with
respect to the pointed H subcategory. Its equivariance map for h gives a
crossing hX -> Xh. The half-braiding compatibility is exactly equivariance
coherence, and its tensor hexagon is monoidality. The usual twisted-double
central construction supplies the lifts of h; cyclicity makes their
projective character structures one-dimensional. Tensoring by the canonical
central Rep(H) gives all three lifts of each h.

There is exactly one underlying lift of each h in E_ad. To make the braided
closure completely explicit, restrict the half-braidings to E_ad first.
For an invertible underlying object, two half-braidings differ by scalar
functions on simples satisfying the tensor-automorphism relations. Their
ratio is therefore an element of Aut_tensor(Id_Ead), equivalently a character
of U(E_ad). Here U(E_ad)=U(C)=1. Thus a half-braiding on each selected
underlying invertible is unique. The product half-braiding must equal the
selected one on the product object, proving braided closure without an
unstated choice of compatible structures. This gives an actual braided
pointed C3 in Z(C) mapping faithfully to the original H.

A braided pointed category on odd cyclic C3 has trivial ordinary associator:
its quadratic form has values among the cube roots and is represented by an
ordinary bicharacter. Hence the regular H algebra really exists. Its central
braiding, however, can be trivial or one of the two metric C3 braidings.

## Remaining gap and safe status

I have not proved that the central lift is isotropic. The three subgroup
section possibilities are compatible with the three braided C3 possibilities;
the section calculation does not distinguish the isotropic one. Trivial
universal grading proves uniqueness of a half-braiding, not symmetry. Free
action on all original simples has not yet supplied the missing isotropy
argument.

Ordinary Mueger factorization requires an ambient braided category and cannot
be applied inside the unbraided C. Likewise the existence of the regular H
algebra alone does not make its module category a rank-four tensor quotient:
commutativity for its central structure is precisely what fails in the metric
case. Any separate Morita argument has to compute its actual dual category
and cannot assume the Tannakian de-equivariantization rules.

Result: the central-C3 partial theorem passes, with the explicit closure
justification above. R561 and R628 remain unresolved unless an independent
argument removes the two metric alternatives or constructs a realization.

## Subsequent regular-algebra Morita check

I also read `../c6/C3_regular_algebra_Morita.md`. Its explicit alpha-induction
proof is valid. For A the regular H algebra, the free left module A tensor X
gets its right action by the inverse given central crossing. The same crossing
supplies a balanced strong tensorator. A left-linear map is a sum of maps
f_h:X -> h tensor Y. Naturality and right-linearity impose
(b(k,h)-1)f_h=0 for all k, where b is the actual crossing bicharacter, not
an unprovided reverse braiding. For either nontrivial C3 bicharacter this
leaves only h=1. Thus alpha induction is fully faithful and, by equality
of Morita global dimensions, a tensor equivalence.

Therefore the actual regular-H Morita dual in either metric case has the
same fusion category and ring as the original. The rank-four one-sided
module category is not a tensor quotient. This rigorously closes that
particular proposed avenue without changing the unresolved status of
R561 or R628.

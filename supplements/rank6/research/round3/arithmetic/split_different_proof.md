# Different ideals and the split quadratic case

## A general necessary theorem

Let A be the commutative signed quotient supplied by sphericalization of a
commutative self-dual fusion ring, and let K be its categorical dimension
character field. Write d_i for its basis dimensions and Delta=sum d_i^2.
Then **Delta belongs to the different ideal D_(K/Q)**.

Indeed, let e be the separability idempotent of K/Q. Under the embeddings
K tensor K -> C indexed by pairs of embeddings, character orthogonality gives

    Delta e = sum_i d_i tensor d_i.

Both sides are elements of K tensor K; the right side is in O_K tensor O_K.
If a is in the codifferent, contract the second factor by x -> Tr(a x).
Every resulting Tr(a d_i) is integral, while contraction of Delta e gives
Delta a. Hence Delta times the codifferent is contained in O_K, exactly
Delta in the different.

This theorem is independent of any pivotality assumption on the original
category. The signed quotient and dimension-field containment are obtained
from sphericalization as in the preceding chapter.

The usual local trace formula is
Tr_(L/Q_p)(P_L^k)=p^floor((k+d)/e), where d is the different exponent and e
the ramification index. Therefore every ramified odd prime divides
Tr_K(Delta): tame ramification has d=e-1 and floor(2d/e)=1. A cyclic cubic
extension of conductor 9 has e=3,d=4, and contributes 9 to this trace ideal.
These classical local facts, and the conductor-discriminant formula below,
may be cited from Serre, Local Fields, Chapters III and VI, and J.S. Milne,
Class Field Theory, Chapter V, Theorem 3.27 (the online notes are at
https://www.jmilne.org/math/CourseNotes/CFT.pdf).

## Exhaustive field list for the tensor profile

The executable hypotheses require exactly the formal codegrees
9,9,9,9 and the roots of X^2-7380X+13284, Casimir trace 7416, and modulo-two
algebra F_2^4 times F_2[epsilon]/epsilon^2. These are checked from the complete
tensor, without using an identifier. Put E=Q(sqrt(41)). Central induction
forces E contained in K, Delta/9 integral, and

    Delta/(18 sqrt(41)) integral,  738 | Tr_K(Delta),  Tr_K(Delta)<=7416.

The FP codegree is 18 sqrt(41)(32+5 sqrt(41)); its second factor has norm -1.
Cyclotomicity of the signed characters makes K/Q abelian Galois. Its degree
is 2,4, or 6. If its degree is 4 or 6, it is completely split at 2: the
four etale rank-one local factors are Q_2, and the sole remaining block has
rank two. A Galois character field using a local extension of degree two
would need respectively two or three such degree-two local components.
There is space for at most one. Ramification at 2 is excluded for the same
reason. This argument permits rational idempotents inside the non-etale
rank-two block and does not assume that the entire order is etale.

The different theorem and the bound restrict every ramified prime outside
{3,41} to 5 or 7, and exclude simultaneous 5 and 7: the extra multiplier in
lcm(738,Tr(D_K)) would be at least 35. The finite abelian field list is now
an elementary Dirichlet-character calculation:

* A biquadratic quartic K=E Q(sqrt(m)) would have m positive squarefree,
  coprime to 41, supported on {3,5,7}, and m=1 modulo 8 because 2 splits.
  Among the eight products, only 1 and 105 satisfy this congruence. The first
  gives E itself, and the second requires both 5 and 7, already excluded.
* A cyclic quartic K has a primitive quartic character whose square is the
  quadratic character of conductor 41. It is therefore a quartic character
  modulo 41 times a quadratic character of positive odd discriminant m,
  coprime to 41. The quartic character takes value -1 at 2
  (2^10=-1 modulo 41). Splitting at 2 requires m=5 modulo 8. Among the same
  eight products this leaves exactly m=5 and 21. These two fields have
  conductors 205 and 861. The trace divisibilities are 3690 and 5166, so
  the only traces are 3690,7380 in the first field and 5166 in the second.
* A degree-six abelian field is E times a cyclic cubic field L. Its possible
  ramified primes are 3 and 7: neither 5 nor 41 admits a cubic character.
  The cubic conductor is therefore 7,9, or 63 (a nontrivial cubic character
  at 3 has conductor exactly 9). The prime 2 is inert in the cubic fields
  of conductors 7 and 9, excluding them. Thus only conductor 63 remains;
  its different trace contribution includes 9 times 7, giving total trace
  5166. We need not distinguish its cubic characters: the next argument
  excludes every conductor-63 field for which 2 splits.

There are no omitted prime-power conductors: at a prime other than 2 or 3,
characters of orders dividing 4 or 6 have no nontrivial action on the
prime-power unit subgroup. Quadratic odd characters likewise have squarefree odd
conductor. Thus the list is exhaustive.

## The sextic field

The discriminants of E and L are coprime, hence
O_K=O_L tensor O_E and D_K=D_L D_E. Write

    Delta=18 sqrt(41)(a+b sqrt(41))/2,
    a,b in O_L,  a=b modulo 2.

Total positivity of Delta at both extensions of every real embedding of L
implies that b is totally positive. Its trace is 5166/(18*41)=7.
The cubic field is tamely totally ramified at 7, with different P_7^2.
Since 18 is a unit at 7, the different theorem forces b in P_7^2.
Consequently Norm(b)>=Norm(P_7^2)=49. The arithmetic-geometric mean bound
instead gives Norm(b)<=(7/3)^3=343/27<49. This is a contradiction.

## The cyclic quartic fields

For M=5 or 21 put

    alpha^2=M(41+5 sqrt(41))/2,
    beta^2=M(41-5 sqrt(41))/2, alpha beta=2M sqrt(41).

The two cyclic quartic fields above are generated by alpha; its polynomial
is X^4-41M X^2+164M^2. An integral basis is

    1, (1+sqrt(41))/2,
    (1+sqrt(41)+2 alpha)/4, (1-sqrt(41)+2 beta)/4.

The verifier checks integral multiplication and discriminant 41^3 M^2.
This is the field discriminant by the conductor-discriminant formula for
characters of conductors 41,41M,41M, proving maximality.

Set theta=Delta/(18 sqrt(41)) and expand theta in this integral basis with
integer coordinates z_j. For the trace-dual basis b_j^*,

    z_j=Tr(Delta b_j^*/(18 sqrt(41))).

For fixed positive trace T, this lies strictly between T times the smallest
and largest conjugates of b_j^*/(18 sqrt(41)). The supplied coordinate
bounds are verified by exact algebraic signs at all four isolated real
roots. Every integer point satisfying the exact trace equation is then
examined. There are respectively 28 and 216 totally positive candidates
at traces 3690 and 7380 for M=5, and 16 at trace 5166 for M=21.
All 260 fail the d-number divisibility test. Every failed coefficient is
recorded and checked; no floating-point bounds enter the certificate.

## The quadratic field and saturation

For K=E, write Delta=18(41y+x sqrt(41))/2. Then x=y modulo 2,
1<=y<=10, x^2<41y^2, and the d-number condition requires
41y^2-x^2 to divide 164y^2. Divisibility by 9 is imposed.
The four complementary signed codegrees belong to E and form a Galois-stable
multiset. Thus they are four rational integers, two rational integers and
one quadratic pair, or two quadratic pairs. All possibilities are exhausted.

Rational codegrees divide the integral content of Delta. A quadratic pair
has polynomial X^2-SX+P, with S^2-4P=41r^2, P dividing Norm(Delta), P|S^2,
both roots greater than one, and each root dividing Delta integrally in E.
The total trace bound makes the S,r searches finite. The reciprocal identity
sum(1/f)=1 is imposed exactly. Only seven Delta candidates reach the
complementary search; no quadratic complementary pair is eligible. The
only complete spectra have y=10, x=+/-64 and four rational codegrees 9.
Their total signed Casimir trace is 7416, forcing saturation.

Exact signed associativity then exhausts the sign tables. Each surviving
one is gauge-equivalent to the original tensor, and every original
non-FP dimension-character orbit is excluded arithmetically. Therefore
any categorification would have a pseudo-unitary Galois conjugate. The
existing exact global-codegree moment certificate excludes that case.
The complete general exclusion is checked by
`software/round3_split_arithmetic.py` on the full tensor.

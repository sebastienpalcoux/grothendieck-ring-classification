# Inert quadratic local factors and signed codegree saturation

This is a general complex-fusion-category necessary criterion. The categorical
input is precisely the dimension-field containment lemma already proved in
`papers/chapters/biquadratic_trace.tex`, obtained from sphericalization and
Ostrik's central-induction theorem (Pivotal fusion categories of rank 3,
Theorem 2.13, arXiv:1309.4822). Global dimensions are d-numbers by Ostrik,
On formal codegrees of fusion categories, Theorem 1.2, arXiv:0810.3242.

## Local isolation theorem

Let R be a commutative self-dual rank-six fusion ring. Suppose its reduction
modulo 2 is a product of finite fields and exactly one factor has even degree,
that degree being two. Suppose an original formal codegree generates
E=Q(sqrt(q)), with q squarefree and q=5 modulo 8. Every categorification has
signed dimension field exactly E; its other four signed formal codegrees are
rational integers.

Proof. Sphericalization gives the commutative signed integral algebra A with
A/2A=R/2R, symmetric multiplication matrices, and dimension character field K.
The containment lemma gives E contained in K. Since the special fibre is
etale and A is finite free, A tensor Z_2 is finite etale: the module of relative differentials vanishes modulo 2, so vanishes by Nakayama; finite presentation and flatness then give etaleness. Its factors are the
unramified extensions corresponding to the displayed finite residue fields.
This follows equivalently from Hensel lifting of their simple defining
polynomials and primitive idempotents; see Stacks Project, Lemma 10.153.7,
Tag 04GK, https://stacks.math.columbia.edu/tag/04GK .

Because q=5 modulo 8, E tensor Q_2 is the unramified quadratic field.
Consequently every local factor of any number field containing E has even
local degree. K, being a field quotient of A tensor Q, therefore uses only
the unique even local factor. Its dimension is two, so K=E.

Every signed formal codegree belongs to E by central induction. A codegree
outside the dimension component also lies in its own character field F. If
it were irrational, E would be contained in F, forcing every completion of F
at 2 to have even degree. The unique even local factor is already occupied
by K. Thus the remaining four codegrees are rational algebraic integers.
They exceed one: the positive signed codegrees satisfy sum(1/f)=1.
No pivotality of the original category has been assumed. QED.

## Exact finite spectrum theorem

Suppose additionally D=c sqrt(q) u, where D is the FP codegree, c is a positive
integer and u is an integral unit of norm -1. The implementation verifies
this identity from the minimal polynomial of D: its norm is c^2 q and
D/(c sqrt(q)) has integral trace and norm -1. The containment lemma implies
Delta/(c sqrt(q)) is integral. Thus

    Delta = c(qy + x sqrt(q))/2,
    x,y integers, x=y modulo 2, y>0, x^2<q y^2.

Write T for the original Casimir trace. Since the four complementary
codegrees f_i exceed one, c q y <= T-5. Let n=q y^2-x^2. The d-number
condition for Delta gives n | 4q y^2, including when Delta is rational.
Moreover

    Tr(1/Delta) = 4y/(c n),
    sum_i 1/f_i = 1 - 4y/(c n).

As Delta/f_i is integral and O_E=Z[(1+sqrt(q))/2], every f_i divides

    gcd(c(qy-x)/2, c x).

Enumerate all four-element multisets of such divisors >1 satisfying the
reciprocal identity and c q y + sum f_i <= T. Also impose Delta/f integral
for every original rational codegree, and equality modulo 2 of the complete
signed and original Casimir characteristic polynomials. This is finite and
exhaustive. Empty output proves general noncategorifiability; a lower bound
T_min for its total traces bounds the signed Casimir deficit by T-T_min.

## The two multiplicity-eight applications

For R6_8_6524 and R6_8_6525, q=149, c=9,
D=(6705+549 sqrt(149))/2, and T=6741. The local factor degrees are respectively
(2,3,1) and (2,1,1,1,1). The bound gives 1<=y<=5. The complete spectrum
search leaves only y=5, x=+/-61, and (f_1,f_2,f_3,f_4)=(9,9,9,9).
Both surviving spectra have total trace 6741. Hence every signed coefficient
has its original absolute value. Exact sign-only associativity enumeration
leaves one table up to certified sign gauges in each case (1754 and 1872
DFS nodes). Each is gauge-equivalent to R. All non-FP character orbits fail
the original codegree norm-divisibility condition at the prime 149. Therefore
every categorification would have a pseudo-unitary Galois conjugate.

That pseudo-unitary possibility has an immediate independent obstruction.
In both rings the positive dimensions are 1,u-1,u,u,u,u, with
u=(37+3 sqrt(149))/2 and u^2-37u+7=0. Thus D=183u-33. A formal-codegree-9
central simple must restrict to a nonnegative integral combination of these
dimensions, but D/9=(61u-11)/3 is not even in Z+Zu. This contradiction
completes the general exclusions. The released executable wrapper instead
uses the pre-existing exact `global_codegree_moment` certificate, independently
verified on the full tensor; both proofs avoid numerical optimization.

## Verification

`software/round3_arithmetic.py` recovers all hypotheses from the tensor,
reconstructs all finite spectra and signed tables, and checks the supplied
pseudo-unitary certificate. `verify_arithmetic.py` disables scipy's optimizers,
checks the general wrappers, tests nontrivial basis permutations, rejects
altered local factors, omitted spectra, omitted signed tables and changed
trace bounds, and applies the arithmetic criterion to all 54 realized rings.
The full-census report is `full_census_scan.json`; its exclusions overlapping
previously certified rows are confirmations, not new allocations.

## Cyclotomic cubic isolation: R6_8_6999

A second local isolation theorem also permits a non-etale local block. Suppose
R/2R is F_8 times F_2[epsilon]/epsilon^2 times F_2, and an original formal
codegree generates a real quadratic field E. All signed character fields of
a categorification are subfields of cyclotomic fields, by ENO cyclotomicity
applied to characters of sphericalization with sign object acting as -1.
They are therefore abelian Galois over Q. Primitive special-fibre idempotents
lift in the complete algebra A tensor Z_2, even though its rank-two block need
not be etale. The rank-three field block is etale, hence has generic fibre
the unramified cubic field. Let F be the global character field containing it.
Since F/Q is Galois, every completion of F at 2 has the same degree three.
Thus [F:Q] is three or six. Degree six would require a second cubic local
factor, impossible inside the two remaining separate blocks of ranks two and
one. Therefore F is cubic and occupies the entire rank-three block.
The complementary rational algebra has dimension three and contains the
signed dimension field K with E contained in K. Hence K=E and the last
component is Q. The four complementary codegrees lie in E intersect F=Q or
in Q, so all four are rational integers. The preceding finite spectrum theorem
applies without requiring that 2 be inert in E.

For R6_8_6999, q=41, c=18, D=3690+576 sqrt(41), T=7416, and 1<=y<=10.
Only y=10, x=+/-64 and four complementary codegrees 9 survive. Both spectra
have total trace 7416, so the signed coefficients saturate. The exact signed
search leaves one gauge-equivalent original table; every other original
character orbit is rejected arithmetically. The pre-existing exact
`global_codegree_moment` certificate excludes the resulting pseudo-unitary
Galois case. This is a third general exclusion.

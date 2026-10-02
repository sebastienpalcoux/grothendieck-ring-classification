# A relative-trace obstruction for arbitrary categorifications

## The criterion

Let R be a commutative fusion ring all of whose basis elements are self-dual. Let B be the trace of multiplication by its Casimir element, equivalently the sum of squares of every fusion coefficient. Suppose R has formal codegrees L and f, where L is a positive rational integer and F=Q(f). Let

    I = L O_F intersect f O_F.

If every totally positive nonzero t in I has field trace Tr_F/Q(t)>B, then R has no fusion-category categorification over C. No pivotality assumption is needed.

Indeed, sphericalize a hypothetical category and choose self-dual lifts of its simple objects. Set epsilon=-1 in its Grothendieck ring and denote the resulting signed tensor by T. Its coefficients obey |T_ij^k|<=R_ij^k. The unit and dualities are retained. All the original simples are self-dual, so cyclic trace symmetry and dual reflection make T fully symmetric, in particular commutative. The multiplication matrices are real symmetric and mutually commuting. Their Casimir is a positive definite matrix, and

    Tr(C_T) = sum_(i,j,k) (T_ij^k)^2 <= sum_(i,j,k) (R_ij^k)^2 = B.

Let d_i be the spherical dimensions of the chosen lifts, K=Q(d_i), and delta=sum_i d_i^2. Every embedding of K gives a distinct one-dimensional character of T. Its Casimir eigenvalue is the corresponding conjugate of delta. These characters are linearly independent, even when their Casimir eigenvalues coincide. Hence

    Tr_K/Q(delta) <= Tr(C_T) <= B.

In particular the conjugates of delta are positive. The full sphericalization has dimension2delta. Its original-ring epsilon=+1 sector has formal codegrees2L and2f. Ostrik's induction theorem supplies simple summands of the induced unit with categorical dimensions delta/L and delta/f. They are algebraic integers. Moreover their forgetful images are integer sums of sphericalization simples with dimensions ±d_i, so both these dimensions lie in K. Since delta is nonzero, this forces F=Q(f) to lie in K.

Now put t=Tr_K/F(delta). Relative traces of algebraic integers are algebraic integers, so t/L and t/f are in O_F. Therefore t lies in I. It is nonzero and totally positive, and the trace tower gives

    Tr_F/Q(t)=Tr_K/Q(delta)<=B,

contrary to the criterion. This argument counts all [K:Q] dimension characters, including repetitions of conjugates of delta. It does not assume K=Q(delta).

## R7_4_1417 and R7_4_1420

Both exact census rings have the quadratic formal-codegree factor

    z^2-1020z+10200,

whose roots are f=510±70sqrt(51), and both have integer formal codegree20. Thus F=Q(sqrt(51)), with O_F=Z[sqrt(51)]. The exact ordinary Casimir traces are1086 and1070 respectively.

Any totally positive t divisible by20 in O_F can be written

    t=20(x+y sqrt(51)),   x,y in Z.

Its quotient by f=510+70sqrt(51) is

    t/f=(x-7y)+(y-7x/51)sqrt(51).

Integrality forces51 to divide x, because gcd(7,51)=1. Total positivity forces x>0, so x>=51. Consequently

    Tr_F/Q(t)=40x>=2040.

This exceeds each Casimir trace bound. Therefore **R7_4_1417 and R7_4_1420 admit no general complex fusion-category categorification**. The argument does not enumerate signed tables or induction matrices.

## Sources and scope

Ostrik, *Pivotal fusion categories of rank3*, arXiv:1309.4822, Section5.1 provides the sphericalization and self-dual lifts; Theorem2.13 and Corollary2.14 provide the induced-unit formal-codegree summands and their dimensions. These are applied to the sphericalization, not to the original category. The exact census facts, Casimir polynomials and lattice arithmetic are independently recomputed by `verify_relative_trace.py`.

The integer20 suffices for both cases. The additional integer codegrees in R7_4_1420 only strengthen the lattice. This criterion also forces even character-field degree for R7_4_1212/1213, and excludes degree6 by their integer-codegree lcm180 and Casimir traces1036/1020; it does not presently exclude their remaining degree2/4 dimension characters.

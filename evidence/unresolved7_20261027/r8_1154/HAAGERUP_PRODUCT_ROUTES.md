# Three further golden-field construction families cannot produce R1154

These are obstructions to specified constructions, not to the source ring.
They address a natural new model idea suggested by the rank-ten dimension
a=3(2+sqrt(5)): combine generalized Haagerup categories with Fibonacci,
then condense a central pointed algebra.

Write phi=(1+sqrt(5))/2 and d=phi^3=2+sqrt(5). Let H be any actual complex
category with GH(C4,1) fusion rules

    g rho = rho g^{-1},       rho^2=1+sum_(g in C4) g rho.

The assertions below are conditional on actual realizations, not an
assertion that a particular cited GH presentation exists or is unique.
Let F be a Fibonacci fusion category and P any pointed fusion category
of order N, with arbitrary allowed associators. Their FP dimensions are

    Dim(H)=8 sqrt(5) phi^3,      Dim(F)=sqrt(5) phi,
    Dim(F^6)=125 phi^6,
    Dim(H tensor F^3)=200 phi^6,
    Dim(H tensor H)=320 phi^6.

The R1154 target dimension is 60 phi^6. If it arose as the fusion
category of right modules over a connected separable central commutative
algebra A in one of the three products tensored with P, the standard
dimension quotient requires the following dimensions:

| Ambient factor, before tensoring P | Dim(A) | Pointed group order |
|---|---:|---:|
| F^6 | 25N/12 | N |
| H tensor F^3 | 10N/3 | 4N |
| H tensor H | 16N/3 | 16N |

Every noninvertible simple in these products has a strictly positive
phi coefficient in its FP dimension. Thus rational-dimensional A is
supported entirely on invertibles. A connected separable algebra with
pointed support is multiplicity-free and its support is a subgroup L;
its dimension is |L|. For completeness, the regular A-module is simple,
and gA is simple for each invertible g. A nonzero map gA->A for a
summand g of A is an isomorphism. This proves both multiplicity one
and closure of the support under multiplication and inversion.

The first row exceeds the entire pointed dimension. The second requires
a subgroup of index (4N)/(10N/3)=6/5, impossible. These obstructions
hold for arbitrary pointed factors, not just P=Vec.

## The remaining index-three possibility is also impossible

In the third row, L has index three in the pointed group
J=C4 times C4 times G(P). Let K be its first C4 factor. It is central
in J, so KL is a subgroup and

    [KL:L]=[K:K intersection L]

divides both 4 and [J:L]=3. Hence K is contained in L. The subobject
A_K=sum_(g in K)g is consequently a connected separable subalgebra of A.

It is also a central subalgebra. Indeed, for every simple ambient X,
the isomorphism gX=Xh, for g in K and invertible h, determines h uniquely
and places it in K. On the first GH factor it is h=g for pointed X and
h=g^{-1} for nonpointed X; all other factors of h are the unit. Thus the
half-braiding of A preserves exactly the summands A_K. Its multiplication
and central commutativity restrict. The usual pointed-subgroup algebra
is separable in characteristic zero, including arbitrary compatible
cochain twists of its multiplication.

Free induction to modules over A_K is therefore a tensor functor. It
sends every g in K to the unit, and sends rho in the first GH factor to
a simple x: by free-module adjunction,

    End(rho A_K) = Hom(rho,rho A_K) = C,

since the right K-orbit of rho is free. Its FP dimension is d>1, and
its fusion product is forced to be

    x^2=1+4x.

Hence it would generate a rank-two fusion subcategory with those rules.
This contradicts Ostrik's complete complex rank-two classification,
*Fusion categories of rank 2*, arXiv:math/0203255: only coefficients
0 and 1 are possible in x^2=1+m x. The third construction is impossible.

The same last argument gives a reusable lemma: a GH(G,m) category with
a free pointed orbit of rho cannot have its full regular pointed
algebra as a central commutative algebra whenever m|G|>1. Such a
condensation would produce the forbidden rank-two coefficient m|G|.

These results do not prohibit noncentral bimodule Morita constructions,
different nonpointed factors, or arbitrary chains of categorical
operations. They remove three natural direct central-algebra model
families, while the classification status of R1154 remains unresolved.

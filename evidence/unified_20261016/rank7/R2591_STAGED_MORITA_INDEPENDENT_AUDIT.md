# Independent audit: staged Morita obstruction for R7_4_2591

Status: PASS for the categorical argument, conditional only on the
already independently audited initial twisted-V4 reduction and the
explicit source fusion products. No associator classification or
numerical infeasibility is used in the new argument.

Auditor: rank6_center, 2026-10-16.

Let E be the initial dual, with eight invertibles K and a free orbit
K rho of eight noninvertibles of dimension t=2+sqrt(5). Let Q be the
actual inverse algebra, the full regular object on L=V4 in K, with
possibly twisted multiplication. Write rho k=phi(k)rho and rho^2=a+N rho.

The previously derived conditions phi(L)=L and a outside L have the
following categorical basis. If phi(L) differs from L, their intersection
is C2 and the noninvertible Q-bimodules have one support orbit with two
stabilizer characters. Character twists of Q restrict surjectively to
that C2 and interchange these two simples, contradicting the source
rule that all invertibles fix Y and Z separately. Once phi(L)=L, there
are two support orbits. Since Y*=Z, the duality shift a must be outside L.

## A central fixed involution

One can prove K abelian without using the quadratic normal-form census.
The only nonabelian order-eight group containing V4 is D8. Write its
index-two V4 as L=<r^2,s>. An automorphism preserving L has
phi(r)=r^(+/-1) and phi(s)=r^(2b)s, and therefore phi^2=Id.
The quadratic relation, however, gives phi^2=Ad(a). Every element
outside L is noncentral, a contradiction. Thus K is C4 x C2 or C2^3.

Now phi^2=Id. Its restriction to the two-dimensional F2-space L has
a nonzero fixed vector delta. The involution delta is central in K
and satisfies phi(delta)=delta. The summand A=1+delta is an actual
subalgebra of Q: a connected separable pointed algebra supported on
L has nonzero twisted-group multiplication, whose restriction to
the subgroup <delta> is again a separable algebra.

Every <delta>-by-<delta> orbit on either K or K rho has size two,
because delta is central and phi-fixed. Each stabilizer is C2 and
has two one-dimensional projective representations. Therefore
E'=A-bimod(E) has eight invertibles and eight noninvertibles of
dimension t, again a free orbit (the coefficient of invertibles in
W W* is one because t^2=1+4t).

## Connectedness and the second algebra

Q is naturally an algebra B in A-bimod(E). Its multiplication factors
through Q tensor_A Q and its separability passes to this relative
tensor product. Evaluation on the unit embeds

    Hom_(A-A)(A,Q) into Hom_E(1,Q).

The latter is one-dimensional, and the inclusion A->Q supplies a
nonzero bimodule map. Hence B is connected. Its dimension in E' is
dim_E(Q)/dim_E(A)=4/2=2. Thus B=1+h for an invertible involution h;
there is no need to posit an additional algebra structure on h.

B-bimod(E') is canonically tensor equivalent to Q-bimod(E): a B action
in A-bimod(E) is exactly a Q action in E whose restricted A action is
the specified one. This is the standard associativity of relative
Morita construction, with actual algebras at every step. Therefore
the second dual is the original R2591 category.

## The forced support permutation

Let K' be the order-eight invertible group of E', H=<h>, and let
phi' describe its mixed action on the free noninvertible orbit.
The integral part of the H-bimodule dual is the source TY category,
with four invertibles and one dimension-two object. If H were normal
in K', each pointed double coset would have stabilizer C2 and yield
only invertibles. Hence H is not normal, so K'=D8 and h is a reflection.

If phi'(H) were conjugate to H, some noninvertible H-by-H support
orbit would have size two and stabilizer C2. It would yield two
simple objects of dimension t, which the source does not have.
An automorphism sends reflections to reflections, so phi'(h) is in
the opposite reflection class. Up to group automorphism, take
H=<s> and phi'(H)=<rs>.

There are exactly two noninvertible support orbits. The orbit through
rho is

    H phi'(H) rho={1,s,rs,r^3}rho.

Multiplication by the central rotation r^2 sends it to the disjoint
other orbit. Since r^2 normalizes H, the pointed double coset r^2H
has stabilizer C2 and yields invertible H-bimodules. Tensoring by
either of them multiplies noninvertible supports by r^2, so it
interchanges the two simple source objects Y and Z. This contradicts
the source fusion rules. Projective phases cannot alter this support
permutation.

Thus the staged argument is a complete theoretical obstruction once
its initial source-bound twisted-V4 reduction is included. The
argument actually needs no pseudo-unitarity after that reduction:
the support, algebra, and FP dimension statements are categorical.

## Independent exact replay

I subsequently read the full source-bound verifier
verify_R2591_staged_morita.py and ran it independently with Python -O.
It passed, including replay of the initial twisted-V4 certificate,
the exact source fixedness and TY products, all five groups of order
eight and their automorphisms, and all sixteen opposite-reflection
support configurations. The compatible initial systems were 8 for
C4 x C2, 112 for C2^3, and zero for the other three groups.
The receipt is r2591_staged_independent_optimized.json. These finite
checks faithfully replay the elementary group argument above; none
of the categorical conclusions is inferred from a numerical solver.

# A small-algebra obstruction for the new order-32 Izumi categories

Research note, 1 October 2026. This excludes one proposed construction route,
not categorifications of R6_4_155 in general. No center enumeration is used.

## Algebraic half-braiding lemma

Let C be one of the algebraic Izumi categories constructed in Radchenko--Wheeler,
*Real quadratic fields and finite quantum dilogarithms I*, arXiv:2609.21892v2,
Section 5.4. Use their strict endomorphism realization and notation. The simple
objects are alpha_g (g in a finite abelian group G) and rho. Their formulas give

    alpha_g rho = rho,
    rho alpha_g = Ad(U_g) rho,
    U_g U_h = U_(g+h),
    alpha_g(U_h) = chi(g,h) U_h,

where chi is a nondegenerate symmetric bicharacter. Also rho is a summand of
rho^2, with nonzero split inclusion T_h: rho -> rho^2.

**Lemma.** If a central object Z has multiplicity-free pointed underlying object
`F(Z) = direct_sum_(g in H) alpha_g`, every alpha_g summand separately has a
half-braiding. Its self-braiding is `chi(g,g)^(-1)`.

**Proof.** Write its half-braiding with alpha_h diagonally as scalar a(g,h)
on the alpha_g summand. This is diagonal because G is abelian and the alpha_g
are pairwise nonisomorphic. Write its half-braiding with rho in matrix form:
the entry from label g to label k is `M_(k,g) U_k`. The relevant morphism space
is one-dimensional, since Hom(rho,rho alpha_k) = C U_k.

Naturality at U_h: rho -> rho alpha_h, combined with the half-braiding hexagon,
gives, in the (k,g) entry,

    U_h M_(k,g) U_k
       = a(k,h) M_(k,g) U_k alpha_g(U_h).

Consequently `M_(k,g) != 0` implies `a(k,h) chi(g,h)=1` for every h in G.
Nondegeneracy of chi shows that each row k of M has at most one nonzero entry.
M is square and invertible, so it is monomial; let pi be its underlying
permutation of the labels H.

The hexagon says that the half-braiding with rho^2 sends label g to label
pi^2(g). On the other hand, naturality at any fixed nonzero split inclusion
T: rho -> rho^2 compares this with the half-braiding with rho, whose output
label is pi(g). The two compositions are nonzero: they are compositions of
an isomorphism and a split inclusion. Output direct-sum labels must therefore
agree. Thus pi^2(g)=pi(g), and bijectivity of pi gives pi=identity.

The half-braidings with all the tensor generators now preserve each alpha_g
summand, so these summands are central. The displayed identity gives
`a(g,h)=chi(g,h)^(-1)`; in particular the self-braiding is the claimed scalar.
No C*-structure and no existence theorem for other central lifts is used. QED.

In the positive spherical representative all invertibles have dimension one,
so their twists equal these self-braidings. Galois conjugation preserves
nondegeneracy of chi and the following arithmetic argument.

## Every dimension-eight connected etale algebra would be pointed

Now take |G|=32 and near-group multiplicity 32. Pass to a positive spherical
Galois representative using the same two-dimension reduction invoked for
near-group comparisons in the frozen release. A hypothetical etale algebra,
its multiplication, and its half-braiding transport under the same Galois
automorphism. This is not an assumption of unitarity of the RW construction.
Put

    d=4+3 sqrt(2), rho=4d=16+12 sqrt(2),
    Delta=32+rho^2=8(72+48 sqrt(2)).

The formal-codegree decomposition of I(1) has constituent dimensions

    1, rho+1, and 31 copies of rho+2.

This follows directly from the commutative near-group ring: its 31 nontrivial
group characters have formal codegree 32, and the two other characters send
rho to its two quadratic roots. In particular all nonunit constituents of
I(1) have dimension greater than eight.

Suppose A is connected etale in Z(C), with FPdim(A)=8. Its underlying object
cannot contain rho, since FPdim(rho)>8, and hence is pointed. Adjunction with
I(1), using the preceding low-dimensional bound, gives

    dim Hom_C(1,F(A)) = dim Hom_Z(C)(I(1),A) = 1.

Thus F(A) is a connected separable algebra in the pointed category Vec_G.
Its underlying object is multiplicity-free, supported on a subgroup H of
order eight. One can see this without a classification: F(A) is a simple
right module over itself because its endomorphism space is Hom_C(1,F(A)).
Each alpha_g tensor F(A) is also a simple right module. Therefore

    [F(A):alpha_g] = dim Hom_A(alpha_g tensor A,A)

is zero or one, and the nonzero labels form the stabilizer subgroup H of the
simple module A under G.

The lemma now splits A into central invertibles. Since a connected etale
algebra in a pseudo-unitary modular category is twist-free, every h in H has
chi(h,h)=1. Thus an order-eight subgroup of bosons is necessary.

## Rank-at-most-two groups of order 32 have only four bosons

The only possibilities are C32, C2 x C16, and C4 x C8. The following count
allows every nondegenerate symmetric bicharacter, not just a chosen one.

* For C32, chi(x,x)=exp(2 pi i c x^2/32), with c odd. The equation chi(x,x)=1
  is equivalent to 8 dividing x. There are exactly four solutions.
* For C2 x C16, write coordinates (a,b), a modulo 2 and b modulo 16. A
  symmetric bicharacter has diagonal parameters p/2 and q/16 and off-diagonal
  r/2. Nondegeneracy forces p=1 and q odd. Indeed if q is even then the
  character of the order-16 generator has order at most eight; if p=0 and
  q is odd then the order-two generator equals 8 times the order-16 generator
  under the pairing map when r=1, and is in the kernel when r=0. The boson
  equation is `8a+q b^2=0 mod16`; the cross term is integral. It forces a=0
  and b divisible by four. Again there are four solutions.
* For C4 x C8, write diagonal parameters p/4 and q/8 and off-diagonal r/4.
  Nondegeneracy forces p and q odd. If q is even the order-eight generator
  maps to a character of order at most four. If p is even, with q odd,
  a nonzero element `(2,4r)` is in the kernel. The boson equation is
  `2p a^2+q b^2+4r ab=0 mod8`. It first forces b even. Writing b=2c then
  forces a even, and finally c even. The bosons are precisely a=0,2 and
  b=0,4, again four elements.

Therefore none of these newly constructed order-32 Izumi categories has a
connected etale algebra of dimension eight in its center. In particular one
cannot obtain the proposed rank-52 center of R6_4_155 by a single dimension-
eight connected-etale condensation of any of these centers.

## Scope and references

This does not exclude other categorical constructions, nonintegral
condensations, products before condensation, or the unresolved near-group
type (8,16). It does not settle R6_4_155.

Primary source: D. Radchenko and C. Wheeler, arXiv:2609.21892v2, Section 5.4,
especially equation (47), the relations immediately preceding (48), and
Theorem 12 / Corollary 6. The half-braiding argument above is an independent
algebraic deduction from those displayed identities, not an invocation of
a unitary center-classification theorem.

The formal-codegree induction formula and twist-freeness of connected etale
algebras are the standard ones already used in the frozen release. The
formal-codegree values needed here are explicitly listed above.

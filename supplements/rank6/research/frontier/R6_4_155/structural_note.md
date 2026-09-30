# Structural investigation: R6_4_155 and R6_5_1204

Status: neither ring is newly excluded or constructed here. The positive result is
a uniform, short sphericality and Galois-pseudo-unitarity proof for the whole
non-self-dual V4-quadratic family. It removes the need for signed-table enumeration
in R6_4_155. All calculations below are independently checked in `check.py`.

## A uniform sphericality lemma

Let C be a complex fusion category with simples 1,h,g,hg,X,Y, where the
invertibles form V4, h fixes X,Y, g swaps X,Y, Y=X*, and

    XY = 1+h+mX+mY,    X^2 = g+hg+mX+mY.

Then C is spherical and has a pseudo-unitary Galois conjugate, for every m>=0.
This is a special case of Thornton's Theorem IV.3.6, but the following direct
proof is particularly short and does not enumerate associativity or induction
systems.

Pass to the canonical sphericalization. Choose the dimension-1 lift k+ of each
invertible k. Their products are the corresponding positive lifts. Choose X+
and put Y+=g+ X+. Write delta=dim(X+)=dim(Y+). The equality of these dimensions
also proves h+X+=X+, h+Y+=Y+, g+Y+=X+, and (X+)*=Y+.

The object X+Y+ is self-dual. Its invertible summands are exactly 1+,h+,
by Frobenius reciprocity. Hence

    X+Y+ = 1+ + h+ + s(X+ + Y+) + t(X- + Y-),   s+t=m.

Taking dimensions gives delta^2 = 2+r delta, where r=2(s-t). Simultaneously
changing both chosen noninvertible lifts changes the sign of r, so take
0<=r<=2m. The squared-norm global dimension of C is

    d_r = 4+2 delta^2 = 8+r^2 +/- r sqrt(r^2+8),

whereas its Frobenius-Perron dimension is

    D_m = 8+4m^2+2m sqrt(4m^2+8).

If m=0, s=t=0 already and tensor closure follows directly as below. Assume m>0.
The ratio d_r/D_m is an algebraic integer (ENO, Proposition 8.22). For even r,
r^2+8 cannot be a square: a putative square would give (v-r)(v+r)=8 and then
r=1. The same holds for 2m. Thus, when r>0, an automorphism of the compositum
can simultaneously negate the two square roots; for r=0 simply negate the
denominator root. Multiplying the ratio and its image gives the positive rational
algebraic integer

    (r^2+8)/(4m^2+8).

It is at most 1, hence equals 1. Therefore r=2m, s=m, and t=0. To make tensor
closure explicit, g+ commutes with X+,Y+: both orders have the same underlying
simple and the same nonzero dimension. Consequently X+^2=Y+^2=g+X+Y+, and all
these products contain only the chosen lifts. Their full fusion subcategory
maps tensor-equivalently onto C.
This gives a spherical structure. Its common noninvertible dimension is
m +/- sqrt(m^2+2); conjugating the negative root to the positive root yields
pseudo-unitarity. This also covers m=0 (r=0) directly.

Independent mathematical audit: passed. The audit explicitly verified the scope
of ENO Proposition 8.22 (arXiv:math/0203060, p. 34), the simultaneous quadratic
automorphism, and tensor closure in the sphericalization.

For R6_4_155, m=4. The only candidate r after changing sign are 0,4,8, and the
three rational norms are respectively 1/9,1/3,1. No computer enumeration is
needed for the mathematical proof.

References checked:

* Josiah Thornton, *Generalized Near-Group Categories*, 2012 dissertation,
  Theorem IV.3.6, pp. 51-52 (printed numbering):
  https://scholarsbank.uoregon.edu/server/api/core/bitstreams/5ca4d3c1-3d84-4b04-820f-985cf1826ba9/content
* Dong, *On generalized near-group fusion categories*, introduction explicitly
  cites this unconditional result: https://arxiv.org/html/1903.08791v1
* Meng--Yu, *Classification of some V4-quadratic fusion categories of rank 6*,
  https://arxiv.org/abs/2608.06064 . Their last case in Theorem 1.1 is precisely
  R'(4)=R6_4_155; their new construction is R'(2). Their Lemma 2.1 alone is not
  an unconditional sphericality reference: their Section 2.3 explicitly
  assumes sphericality in its terminology.

## What the original tensors imply structurally

R6_4_155 has precisely the three order-two pointed subrings, the full pointed
V4 subring, and the trivial/full subrings. Its adjoint subring is the whole
ring. Thus no nontrivial faithful grading can yield a smaller component.
The recorded 1+h Morita calculation returns this same based ring; repeating
that calculation would not advance its classification.

R6_5_1204 has no nontrivial proper fusion subring. In particular, it has no
half-E6 subcategory. Its dimensions are

    1, 3+2sqrt(3), 3+2sqrt(3), 7+4sqrt(3), 6+4sqrt(3), 8+4sqrt(3).

Its nontrivial Galois conjugate has global dimension 336-192sqrt(3), about
3.446. The presently checked small-global-dimension classification below
sqrt(5) does not apply. Small squared norms alone give no contradiction.

## A verified dimension match that is not a model

Edie-Michell, *Type II quantum subgroups of sl_N. I*, Theorem 5.2 and its
preceding discussion, constructs the modular category

    F = C(sl_3,9)^0_{Rep(Z3)}

of rank 9 and dimension 336+192sqrt(3). Its dimensions are

    1, 7+4sqrt(3), 8+4sqrt(3), (3+2sqrt(3)) six times.

Replacing six copies of d=3+2sqrt(3) by d,d,2d preserves the sum of squares
and produces the dimension multiset of R6_5_1204. This is only arithmetic:
it does not establish an algebra, a tensor functor, or a categorification.
Moreover, if the existing exhaustive 22--51 center-rank frontier is accepted,
C cannot be Morita equivalent to the underlying fusion category F, because
Z(F)=F boxtimes F^rev has rank 81.

Primary source: https://par.nsf.gov/servlets/purl/10423839
(Communications AMS 3 (2023), 112-165, DOI 10.1090/cams/19).

## The SU(6)_6 adjoint conformal embedding: another exact match, ruled out

The adjoint conformal embedding SU(6)_6 into SO(35)_1 gives an Ising local
module category of global dimension 4. Let A be its vacuum algebra and
B=C(sl_6,6)_A. The canonical root-lattice grading is by Z6. Its neutral
component B0 does indeed have exactly the target dimension
336+192sqrt(3): the SU(6)_6 global dimension is

    2011392+1161216sqrt(3) = 9(336+192sqrt(3))^2.

However B0 cannot categorify R1204. The simple current J of highest weight
6 omega_1 belongs to the vector branching block, not the vacuum algebra.
Indeed, in the abelian-ideal branching rule it is the sum of the five
positive roots epsilon_1-epsilon_j (j=2,...,6), and this ideal has odd
cardinality. Thus the invertible F_A(J) is nontrivial. But J has center
charge 6=0 in Z6, so this nontrivial invertible lies in B0. R1204 has no
nontrivial invertible.

There is also a small exact center-rank test against Morita equivalence.
Using Z(B)=C(sl_6,6) boxtimes Ising^rev, passage to B0 condenses the
Tannakian Z6 generated by (J,psi). Centralizing simples are the pairs
(lambda,1),(lambda,psi) with charge(lambda)=0 and (lambda,sigma) with
charge(lambda)=3. Enumerating the 462 level-six affine A5 weights gives
236 such pairs. The Z6 action has 38 orbits of length 6, two of length 2,
one of length 3, and one of length 1. Stabilizers are cyclic, hence their
projective irreducible representations are one dimensional. Fixed-point
splitting therefore gives

    rank Z(B0) = 38 + 2*3 + 2 + 6 = 52.

The existing necessary center frontier of R1204 has ranks at most 51.
Subject to that existing exhaustive certificate, B0 is not a Morita model
for R1204 either. This rejects an attractive proposed model; it is not a
categorification obstruction for R1204 itself.

`check_su6_route.py` independently enumerates all 32 abelian ideals, checks
the vacuum/vector parities and the J branching, verifies the dimension
formula symbolically, and computes all 42 diagonal orbits. It takes
less than one second; results are in `su6_route_results.json`.

Branching reference: Cellini--Kac--Moseneder Frajria--Papi,
*Decomposition rules for conformal pairs associated to symmetric spaces
and abelian subalgebras of Z2-graded Lie algebras*, Advances in Mathematics
207 (2006), 156--204, https://arxiv.org/abs/math-ph/0506043 .

## Boundaries of the conclusions

A nondegenerate semion subcategory of Z(C) splits Z(C), not automatically C.
The rank-3 near-group quotient obtained by formally identifying g with 1
is not an available tensor quotient: the forced pointed associator on g is
nontrivial. A central fermion h is not a Tannakian boson. Consequently neither
formal quotient legitimately invokes the rank-3 categorification theorem.
No new exclusion should be entered in the classification ledger on these grounds.

# Spherical reduction for R6_4_155

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

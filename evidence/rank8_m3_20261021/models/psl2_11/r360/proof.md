# A twisted alternating-group model for R8_3_3342

## Statement and scope

There is a normalized cocycle `omega: A6^3 -> {+1,-1}` and a cochain
`psi: A5^2 -> {+1,-1}` with `d psi = omega|A5` such that the unitary
group-theoretical category `C(A6,omega,A5,psi)` has precisely the based
fusion tensor **R8_3_3342**. The subgroup A5 fixes one of the six letters.
The category has simple dimensions `1,3,3,4,5,10,10,10` and dimension 360.

The proof below specifies the cocycle class by an independently checked
stable element, proves the nontrivial projective stabilizer multiplier,
and derives the entire fusion tensor. It does not identify a model merely
by its dimensions. R8_3_3344 is not the tensor of this construction; no
general exclusion of that ring is asserted here.

## 1. A finite relative cocycle certificate

Let `P = <r,s | r^4=s^2=1, srs=r^-1>` and write its elements `(i,j)=r^i s^j`.
Embed P in A6, acting on letters 0 through 5, by

    r=(0 1 2 3)(4 5),  s=(0 2)(4 5).

It is a Sylow 2-subgroup. Put

    E = {(i,j): i mod 2 = j},
    K = {(i,j): i mod 2 = 0},
    t = s.

Here E is the Klein four group fixing both 4 and 5; K is the other Klein
four subgroup of P. Let `x(i,j)=i/2`, `y(i,j)=j` on K. All calculations in
this section have coefficients F2. The verifier solves the normalized bar
equations

    dw=0,   w|E=0,   w|K = x^2 y + x y^2 + dv.

Explicitly the chosen representative of the cubic at `(a,b,c)` is
`x(a)x(b)y(c)+x(a)y(b)y(c)`. There are 343 normalized values of w and 9
normalized values of v. The 2455 equations have rank 312. The certificate
saves the entire solution, the exact equation hash, and all 512 values of w
(including normalized zero entries). The verifier checks every equation.

For each of the 360 elements g of A6 it enumerates
`P intersect g P g^-1` and solves the normalized 2-cochain equation saying
that the restriction of w equals its g-conjugate in cohomology. All these
equations are checked, and a witness cochain for every g is saved. The
intersection-order counts are

| Order | Number of elements g |
|---:|---:|
| 1 | 256 |
| 2 | 64 |
| 4 | 32 |
| 8 | 8 |

By the Cartan–Eilenberg stable-elements theorem there is a class
`c in H^3(A6,F2)` restricting to `[w]`. For the point stabilizer H=A5,
E is a Sylow 2-subgroup of odd index 15. Restriction to E is injective
on mod-2 cohomology, by restriction and transfer, so `c|H=0`.
Consequently c can be represented by a normalized global F2 cocycle
whose restriction to H vanishes identically: first choose its normalized
trivializing 2-cochain on H, then extend that cochain to A6 and gauge the
cocycle. Exponentiating by `a -> (-1)^a` gives the required mu2 data.
We use this gauge, in which `omega|H=1` and `psi=1`.

No table of the cohomology of A6 is needed for this argument. The stable
element theorem is the only general existence theorem used here.

## 2. The actual U(1) multiplier is nontrivial

The off-diagonal double coset has stabilizer
`L=H intersect tHt^-1 = A4`, the pointwise stabilizer of 4 and 5.
For a normalized cocycle trivial on H and psi=1, the stabilizer
multiplier is the one in Gelaki–Naidu, Section 5.1. On E, where a and b
are involutions, its additive F2 version is

    alpha(a,b) = w(a,b,t)
               + w(a,bt,t^-1 b t)
               + w(abt,t^-1 b t,t^-1 a t).

The verifier checks that alpha is a 2-cocycle. For `u=r^2` and `v=rs` it
proves

    alpha(u,v) + alpha(v,u) = 1.

This equality is not just tested on the chosen solution. The certificate
saves indices of original affine equations whose sum is the displayed
commutator functional plus 1. Thus it is forced for **every** normalized
cocycle vanishing on E and restricting to the specified class on K.
In particular it holds for the restriction of the globally gauged
cocycle from Section 1, even if that restriction differs from the chosen
local representative by a coboundary.

After exponentiation, the commutator is -1 on the commuting pair u,v.
Every U(1) coboundary has commutator +1 on a commuting pair. Hence the
actual multiplier on A4 is nontrivial in `H^2(A4,U(1))`.

It would be incorrect to infer this conclusion merely from the nonzero
mod-2 Dickson cubic on K: that cubic itself has zero image in
`H^3(K,U(1))`. The relative multiplier computation above is the necessary
additional step. We do not need a separate assertion about the order of
the global U(1) 3-class.

## 3. The two sectors and their projective representations

The action of A6 on six letters is doubly transitive, so H has two double
cosets. The diagonal sector is Rep(A5), with irreducible dimensions
`1,3,3,4,5`. The off-diagonal sector is the projective representation
category of A4 for the multiplier above; its simple dimensions are
multiplied by `[A5:A4]=5`.

The nontrivial mu2 extension of A4 is the binary tetrahedral group 2T.
For completeness, the extension is unique: the coprime extension
`V4 -> A4 -> C3` identifies `H^2(A4,F2)` with the invariant part of
`H^2(V4,F2)`, which is one dimensional. Its nonzero class restricts to
the quaternion extension. Equivalently the Kummer sequence identifies
`H^2(A4,mu2)` with `H^2(A4,U(1))[2]`, since squaring is bijective on
`H^1(A4,U(1))=C3`.

Let rho0 be the defining two-dimensional representation of the unit
quaternions 2T in SU(2), and let chi generate the character group C3 of
A4. The spin representations are

    rho_i = rho0 tensor chi^i,   i in Z/3.

They are irreducible and distinguished by
`det(rho_i)=chi^(2i)`. Their squared dimensions sum to 12, the dimension
of the twisted group algebra of A4, so they exhaust its simple modules.
The object rho0 is intrinsically the unique determinant-trivial spin
representation. Changing a mu2 projective gauge does not change the
determinant of a two-dimensional representation. Write X_i for the
corresponding off-sector objects, all of dimension 10.

All the X_i are self-dual. Indeed reversing the two endpoints can be
implemented by `(0 2)(4 5)`; on their A4 stabilizer it conjugates by an odd
permutation, so it inverts the character group C3. Taking a representation
dual also inverts its determinant. These two inversions cancel, and the
remaining transport scalars are in mu2 and have square one. Thus duality
preserves each determinant chi^(2i), and hence each X_i. The five A5
irreducibles are self-dual as well. A based ring with all simples
self-dual is commutative, and its structure constants are symmetric in
all three indices.

## 4. Mackey convolution and the determinant-trivial anchor

One may describe the bimodule category as twisted equivariant kernels
on ordered pairs of points of A6/A5. Composition sums over intermediate
points. At distinct fixed endpoints, the product of two off-diagonal
kernels has four possible intermediate points. Their common stabilizer
A4 acts transitively on those points, with point stabilizer C3. Therefore
off/off fusion at that endpoint pair is induction from C3 to the
projective A4 sector, with the usual cocycle transport factors.

Every mu2 multiplier on C3 has a **unique** mu2 trivialization, since
`H^1(C3,mu2)=H^2(C3,mu2)=0`. An order-three lift in 2T acts on rho0 with
eigenvalues zeta and zeta^2; for example a unit quaternion with scalar
part -1/2 has trace -1 and order three. Thus

    rho0|C3 = chi + chi^2.

This formula is unchanged by either automorphism of C3. All cocycle and
transport factors arise from mu2-valued cochains. After the unique
trivializations, an extra such factor would be a mu2-valued character
of C3 and is therefore trivial. This also follows by determinants: the
three transported copies of rho0 are determinant-trivial, whereas any
nontrivial C3-character twist has nontrivial determinant.
Frobenius reciprocity now gives the anchor

    N(X0,X0;X0) = <chi+chi^2, (chi+chi^2)^2>_C3 = 2.

More generally the restriction of each rho_i is a character translate
of `chi+chi^2`. The tensor of two such restrictions has C3-character
multiplicities 2,1,1 in some order. Pairing with the three translated
two-character restrictions gives one coefficient 2 and two coefficients
3. Thus for every pair i,j the three off-sector coefficients are a
permutation of `(2,3,3)`. This statement is independent of transport
orientations and character labeling.

Symmetry in all three indices, together with the anchor N000=2, now
uniquely fixes the off-sector tensor. The verifier enumerates all 729
assignments of the location of the coefficient 2 for the six unordered
pairs and checks these exact constraints. Only one assignment remains:

    N(X_i,X_j;X_k) = 2 if i+j+k=0 mod 3, and 3 otherwise.

For the diagonal/off-diagonal terms, restrictions from A5 to A4 are

    1 -> 1;  3a,3b -> 3;  4 -> 1+3;  5 -> chi+chi^2+3.

Since `3 tensor rho_i = rho0+rho1+rho2`, the five action matrices on
`(X0,X1,X2)` are respectively

    I, J, J, I+J, 2J-I,

where J is the 3 by 3 all-ones matrix. The off/off coefficients in the
diagonal sector are the same matrix entries, by reciprocity.

## 5. Full tensor verification and unitary scope

The verifier constructs the diagonal tensor independently from the exact
A5 character table (in Q(sqrt(5))), then appends the five action matrices,
their reciprocity coefficients, and the uniquely completed off tensor.
It verifies the dimension character and every associativity identity.
The basis order is

    [1,3a,3b,4,5,X0,X1,X2].

The model-to-census basis map is `[0,1,2,6,7,3,4,5]`; its inverse,
the source-to-model map, is `[0,1,2,5,6,7,3,4]`. All 512 coefficients
agree with R8_3_3342. The compact-JSON source SHA256 is

    964e7a672186047744b854ccf9cf3a89dd177d1efbe595f3a1fb8384d3fe238f

The verifier recomputes this hash from the authoritative census rather
than trusting the stored metadata. The category is unitary: the pointed
category has unit-modulus associators, the subgroup algebra has its
standard unitary separable algebra structure, and its bimodule category
inherits the unitary fusion structure.

For comparison R8_3_3344 has N(X_i,X_i;X_i)=3 for each of its three
dimension-10 simples, contradicting the determinant-trivial anchor of
this particular construction. This comparison is also bound to its
recomputed source hash in the certificate. It is not a nonexistence
theorem for other potential constructions of R8_3_3344.

Replay, including all exact cochain equations and the full tensor match:

    python -O evidence/rank8_m3_20261021/models/psl2_11/r360/verify_a6_twist.py

Default execution compares every recomputed certificate field with the
saved JSON; `--write` explicitly regenerates it. No assertions are used
as validation gates, so optimized Python retains every check.

## References and dependency boundaries

* H. Cartan and S. Eilenberg, *Homological Algebra*, Chapter XII,
  Section 10: stable elements. The mod-p version is also stated as
  Theorem 1.3 in A. Adem, *On the geometry and cohomology of finite simple
  groups*, [author PDF](https://personal.math.ubc.ca/~adem/simple.pdf).
  Only the stable-elements theorem and ordinary restriction/transfer
  are used, not an externally computed A6 cohomology ring.
* S. Gelaki and D. Naidu, *Some properties of group-theoretical
  categories*, [arXiv:0709.4326](https://arxiv.org/abs/0709.4326),
  Section 2.1 and Section 5.1, Theorem 5.1: bimodule construction and
  double-coset/projective-stabilizer parametrization, including the
  multiplier convention used literally by the verifier.
* All local cohomology, stable-element checks, relative multiplier signs,
  tensor completion, and source identification are independent finite
  computations in the accompanying verifier. The representation and
  Mackey arguments in Sections 3 and 4 give their categorical meaning.

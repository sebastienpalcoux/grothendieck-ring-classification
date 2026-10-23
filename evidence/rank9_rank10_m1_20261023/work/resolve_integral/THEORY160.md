# Integral dimension 160: two models and two commutativity obstructions

This note treats the four input rings `R10_1_39`, `R10_1_83`,
`R10_1_138`, and `R10_1_177`. The explicit models and finite checks have
been independently replayed. The general reduction below has passed an
independent mathematical audit, recorded in
`work/audit_new_models/INT160_AUDIT.md`. All four rings are resolved:
two unitary realizations and two exclusions over C.

## Exact affirmative witnesses

Let `V = F16_add`, where `F16 = F2[t]/(t^4+t+1)`. Put `a=t^3`, of order 5,
and let `H=D10` denote the dihedral group of order 10, with elements `(k,e)`
and multiplication `(k,e)(l,f)=(k+(-1)^e l,e+f)`. Its action on V is

`(k,e).x = a^k x^(4^e)`.

* `R10_1_39` is the representation ring of `V semidirect D10`.
  Equivalently, it is the equivariantization of `Vec(V)` by this action.
  The source-to-model basis map is `[0,1,4,8,7,6,9,5,2,3]`.
* `R10_1_138` is the equivariantization of `Vec(V)^omega` by the coherent
  action given in `verified_models160.json`. Here `omega=(-1)^W`, with W
  the C5-average of the trilinear form `x_0 y_1 z_1` in the polynomial
  basis `(1,t,t^2,t^3)`. The source-to-model map is
  `[0,4,5,6,7,1,2,3,8,9]`.

In both certificates, rotations are strict and the involution has
tensorator `i^J(x,y)` and square identification `i^q(x)`. For `(k,e)`,
the tensorator is `i^(e J)`; the compositor for `(k,e),(l,f)` is
`i^(ef q)`. The full J and q arrays are stored in the certificate.
All structural morphisms are unitary phases, so these are unitary fusion
categories.

`replay160.py` checks normalization, all 65,536 associator pentagons,
all 4,096 involution monoidality equations, the full D10 compositor
monoidality and action pentagons, and all 1,000 input fusion coefficients.
The fusion arithmetic is exact in `Q(sqrt(5),sqrt(2),i)`.

## Reduction of every possible categorification to a pointed equivariantization

Suppose C categorifies one of the four input rings, over C. No pivotal,
braided, or unitary hypothesis is imposed. Direct finite checks establish:

* `FPdim(C)=160`, with simple dimensions `(1,1,2,2,5,5,5,5,5,5)`;
* `C_ad=C`, so the universal grading is trivial;
* the nonidentity invertible g fixes the two dimension-2 simples, and
  permutes the six dimension-5 simples in three free pairs.

By Etingof--Nikshych--Ostrik's categorical Burnside theorem, C is solvable.
The prime cyclic extension/equivariantization characterization of
solvability implies that its last construction step is an equivariantization:
a nontrivial extension would give a nontrivial grading. The prime is 2,
since an equivariantization by Cp contains p invertible simples and C has
only two. Thus `C=D^{C2}`.

The orbit formula for equivariant simple objects now gives D of type
`(1^5,5^3)`: each g-fixed dimension-2 object descends to an orbit of two
invertibles, and each pair of dimension-5 objects descends to one fixed
simple of dimension 5. The invertibles of D form C5, and the C2 action
inverts them. Since C5 cannot act nontrivially on a three-element set, it
fixes each of the three dimension-5 objects Y.

Consequently every invertible occurs in `Y Y*`, and `Vec(C5)` is contained
in `D_ad`. Its possible dimension is `5+25k`, for `0<=k<=3`. Divisibility
of fusion-subcategory dimensions leaves only 5 or 80. Dimension 5 is
impossible: every universal-grading component would have dimension 5,
whereas a component containing a dimension-5 simple has dimension at
least 25. Thus `D_ad=D`. D is solvable, so the same last-step argument
forces `D=E^{C5}`. In particular there is a canonical central Tannakian
`Rep(C5)` whose underlying objects are exactly the invertibles of D.

This central lift of the pointed subcategory is unique. Two half-braidings
on a fixed invertible differ by a tensor natural automorphism of `Id_D`;
that group is `Hom(U(D),C*)`, which is trivial. Therefore the C2 action
preserves the canonical central `Rep(C5)`. Equivariantizing it gives a
central symmetric fusion subcategory of `C=D^{C2}`. Explicitly, the
half-braiding of a central equivariant object with another equivariant
object is its original half-braiding in D; equivariance follows from the
central equivariance condition. This gives the usual braided embedding
`Z(D)^{C2} -> Z(D^{C2})` on these objects.

The resulting symmetric subcategory is Tannakian: its forgetful symmetric
functor to `Rep(C5)`, followed by the usual fiber functor, is a fiber
functor. Its dimension is 10, and the inversion action gives simple
dimensions `1,1,2,2`. Hence it is `Rep(D10)`. It exhausts the four
low-dimensional simples of C.

De-equivariantization by this central `Rep(D10)` yields
`C=(E')^{D10}`, with `FPdim(E')=16`. The four simples above the tensor unit
already account for all low-dimensional simples of C. Every other simple
X of E' therefore has an equivariant lift of dimension 5. If its orbit
has size m and the relevant projective stabilizer representation has
degree r, the dimension formula is `5=m r FPdim(X)`. The last factor is
a rational algebraic integer, hence an integer. Dimension 5 is impossible
in a category of dimension 16. Thus `FPdim(X)=1` and `m r=5`. The possibility
`m=1,r=5` is impossible, since an irreducible projective representation
of a group of order at most 10 has degree at most sqrt(10). Therefore
`m=5,r=1`, and E' is pointed.

Write its group of invertibles as V, of order 16. The C5 action is free
away from the identity. The center of the 2-group V is nontrivial and
characteristic, so its size is a power of 2 greater than 1 and congruent
to 1 modulo 5. It must be 16, making V abelian. Apply the same argument
to the nontrivial characteristic subgroup `V[2]`; it too has order 16.
Hence `V=C2^4`. The order-5 action is irreducible over
F2, so it is multiplication by a primitive fifth root in F16. The
involution has form `b(x)=c x^4`, with `c^5=1`; conjugating by a power of a
makes `b(x)=x^4`. We have reduced every categorification to

`(Vec(F16_add)^omega)^{D10}`

with exactly the specified permutation action, allowing arbitrary
associator class and arbitrary coherent tensor structure on the action.

## Four associator classes suffice

The standard complete set of classes in `H^3(C2^4,C*)` has the 14 binary
trilinear representatives

`x_i y_i z_i`, `x_i y_j z_j` for `i<j`, and
`x_i y_j z_k` for `i<j<k`.

Their restrictions to cyclic subgroups are the diagonal values
`omega(x,x,x)`, represented by squarefree Boolean monomials of degrees
1, 2, and 3. Those 14 functions are independent and span the even-weight
functions on the 15 nonzero vectors. Thus the diagonal restriction is
injective on cohomology. A C5-invariant class is determined by three
orbit values with even sum. There are exactly four such classes.

C5-averages of `0`, `x_0 y_1 z_1`, `x_0 y_2 z_2`, and their sum represent
these four classes. Averaging is valid because 5 is odd. The certificate
`normal_forms160.json` provides a coherent action for each representative.
Its four diagonal orbit patterns are `(0,0,0)`, `(1,1,0)`, `(1,0,1)`,
and `(0,1,1)`. In every normal form the involution tensorator beta0 is
symmetric on `Fix(b)=F4`. The replay verifies all these statements directly,
including the rank-14 diagonal calculation.

## All coherent actions have the same fixed-space symmetry

Choose the corresponding C5-invariant associator representative for an
arbitrary action. The tensorator of the generator a is now a 2-cocycle.
Let its class be u in `H^2(V,C*)`. Coherence for `a^5=1` implies `Norm(u)=0`.
Since `H^2(V,C*)` is 2-primary, cyclic averaging gives
`H^1(C5,H^2(V,C*))=0`, so u is in the image of `a-1`. Conjugating the action
by an identity-on-objects tensor autoequivalence kills u. A tensor natural
isomorphism then makes the generator strict. All its powers may be taken
strict; the residual C5 coherence can be strictified because
`H^2(C5,V*)=0`. In fact `(V*)^{C5}=0` also removes any possible remaining
identification of the fifth power with the identity.

Let beta be the involution tensorator in this normalized action. The
categorical relation `ba=a^-1 b` says that
`beta(ax,ay)/beta(x,y)` is a 2-coboundary. It is unnecessary to make beta
itself C5-invariant. Divide beta by the corresponding explicit,
C5-invariant normal-form tensorator beta0. Their quotient gamma is a
2-cocycle whose commutator bicharacter is C5-invariant, because
2-coboundaries on an abelian group are symmetric.

There are exactly four C5-invariant alternating bicharacters on V. They
are

`B_c(x,y)=(-1)^{Tr_F16/F2(c x y^4)}`, for `c in F4`.

They all restrict trivially to `F4 x F4`, since the absolute trace of an
F4 element is zero. This can also be checked without the field formula:
the replay enumerates all 64 alternating binary forms, finds exactly four
invariant ones, and checks their vanishing on `Fix(b)`.

Therefore gamma has trivial commutator on `Fix(b)`, and beta is symmetric
there. Every reflection is C5-conjugate to b. Strict rotations and the
natural comparison maps transport this conclusion to its fixed space;
any comparison changes the tensorator only by a symmetric coboundary.
Nonidentity rotations have no nonzero fixed point. Thus, for every
`h in D10`, its tensorator `J_h` is symmetric on pairs of h-fixed vectors.
This conclusion covers every associator and every coherent action, not
only the four displayed normal forms.

## Commutativity and the two contradictions

For equivariant objects X and Y, the trace of h on the fiber of their
tensor product at an h-fixed vector z is

`sum_{x+y=z, hx=x, hy=y} chi_X(h,x) chi_Y(h,y) / J_h(x,y)`.

Only fixed pairs contribute to this trace. The fixed-space symmetry of
`J_h` makes the expression unchanged by swapping X and Y. Projective
stabilizer character projection gives identical multiplicities for every
simple summand. Hence the Grothendieck ring of every possible category
in the reduction is commutative.

Both remaining input rings are noncommutative. With zero-based input
indices, the replay records:

| Ring | Coefficient | Reversed coefficient |
|---|---:|---:|
| `R10_1_83` | `N[1][6][7]=0` | `N[6][1][7]=1` |
| `R10_1_177` | `N[1][3][5]=0` | `N[3][1][5]=1` |

These contradictions exclude their categorification over C. No assumption of unitarity,
pseudo-unitarity, or a chosen pivotal structure enters the obstruction.

## Reproduction and references

Run `python work/resolve_integral/replay160.py`. Python 3 and SymPy suffice.
For replay, the required files are `replay160.py`, `verify160.py`,
`fuse_mod4_exact.py`, `verified_models160.json`, `normal_forms160.json`, and
`dimension160_inputs.json`, all in the same directory. The replay writes
`replay160_report.json`. Its finite checks are separate from the categorical
reduction proved above; a finite search alone is not asserted to exclude
arbitrary associators.

* P. Etingof, D. Nikshych, V. Ostrik, *Weakly group-theoretical and solvable
  fusion categories*, [arXiv:0809.3031](https://arxiv.org/abs/0809.3031).
  Theorem 1.6 is the categorical Burnside theorem; Proposition 4.4 gives
  the prime cyclic construction of solvable categories; Proposition 4.5
  includes closure under relevant subcategories and quotients. Sections
  2.6, 2.11, and 2.12 discuss central Tannakian de-equivariantization and
  dimension divisibility.
* H.-L. Huang, Z. Wan, Y. Ye, *Explicit cocycle formulas on finite abelian
  groups with applications to braided linear Gr-categories and
  Dijkgraaf-Witten invariants*, [arXiv:1703.03266](https://arxiv.org/abs/1703.03266).
  Section 3.2, formula (3.1), gives the complete normalized 3-cocycle
  representatives used for the elementary abelian 2-group calculation.
* S. Burciu, S. Natale, *Fusion rules of equivariantizations of fusion
  categories*, [arXiv:1206.6625](https://arxiv.org/abs/1206.6625).
  The simple-object orbit and projective stabilizer formulas underlie
  both the dimension reduction and the exact fusion computation.

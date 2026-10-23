# Independent audit of the neutral category and C4 coefficient module

This note audits the categorical hypotheses used to exclude R11_1_153 relative
to the explicit R11_1_104 model. The complete exclusion theorem is written in
`../integral/`; the model and its independent replay are in
`../known_models/jordan_gt_model.json` and the associated verifiers.

The exact finite checks below are independently replayed by
`verify_c4_cohomology_independent.py`. They use only the original source gzip,
local `support.py`, local `verify_baseline.py`, Python and SymPy, and remain
active under `python -O`.

## 1. Exact source hypotheses

Both inputs have FP dimensions 1^4,2^7 and universal grading C4. Their adjoint
neutral ring D has dimensions 1^4,2 and is the Tambara–Yamagami ring on V4.
The three other components each have rank two. If X is a simple of degree one,
then the full source tensor gives

    X X* = 1+h_L+m,     X* X = 1+h_R+m,

where m is the unique noninvertible neutral simple and h_L,h_R are distinct
nonidentity invertibles. The exact verifier independently computes the
adjoint closure, every homogeneous multiplication, these internal-end rules,
and the two stabilizer lines. It also checks that the degree-two pair is
self-dual in R11_1_104 and consists of distinct duals in R11_1_153.

## 2. All four neutral Tambara–Yamagami forms are addressed

The classification of Tambara–Yamagami categories parametrizes the neutral
category by a nondegenerate symmetric bicharacter chi on V4 and a scalar
`tau=+1/2` or `-1/2`. Up to group isometry there are two bicharacters: an
alternating form and a nonalternating form. Thus both signs and both forms
must be considered. The category need not initially be identified with a
particular Hopf-algebra representation category.

The objects XX* and X*X carry their canonical connected separable
internal-end algebra structures. In an algebra `1+h+m` of this kind, the
multiplications `h tensor m -> m` and `m tensor h -> m` are nonzero.
Indeed the h summand comes from the isomorphism between h tensor X and X
(or its right-hand counterpart), and multiplication by that summand acts
invertibly. In a standard TY gauge the associator on `(h,m,h)` is the scalar
`chi(h,h)`. The associativity equation for this triple compares the products
of the same two nonzero scalar maps in opposite order. Hence it forces
`chi(h,h)=1`.

Applying this to the two internal-end algebras proves
`chi(h_L,h_L)=chi(h_R,h_R)=1`. A nonalternating nondegenerate symmetric form
on F2^2 has exactly one nonzero isotropic vector: in an orthonormal basis its
diagonal is the nonzero linear functional x_1+x_2. Two distinct nonzero
isotropic vectors are impossible. This excludes **both signs of the
nonalternating form**, including the Kac–Paljutkin type alternatives.

For the alternating form the two signs give Rep(D8) and Rep(Q8), respectively
(with the convention that the positive sign gives Rep(D8)). This is the
standard TY realization of these representation categories: the unique
2-dimensional irreducible has Frobenius–Schur indicator +1 for D8 and -1 for
Q8. No other alternating TY category is left by the classification.

The quaternion case is excluded directly using the C4 grading, without any
triality argument. Nikshych–Riepel §9.2 and Remark 9.4 compute
`BrPic(Rep(Q8))=S3`. Since S3 has no element of order four, a homomorphism
`C4 -> BrPic(Rep(Q8))` sends the degree-two element to the identity. Its
homogeneous component would be the regular bimodule category, which has rank
five. The actual degree-two component has rank two. Thus the negative-sign
alternating case is impossible. Every putative source categorification has
neutral category tensor-equivalent to **Rep(D8)**.

The group-theoretic order argument is stronger than merely saying that Q8
has no nonregular extension, and does not assume that the C4 generator is a
triality element. The internal-end proof likewise uses no order-three
hypothesis.

## 3. Unique Brauer–Picard homomorphism up to neutral equivalence

Nikshych–Riepel §9.1 computes `BrPic(Rep(D8))=S4`. The tensor
autoequivalences of the alternating TY category give the full S3 of
permutations of the three nontrivial invertibles. Their induction into BrPic
is injective: its kernel consists of inner tensor autoequivalences, and all
such autoequivalences are trivial for the symmetric category Rep(D8).
The induction-kernel statement is also explicitly proved in
Marshall–Nikshych, Proposition 3.1.

The subgroup stabilizing the regular left-module class is therefore S3.
One can see that it is not all of S4 either from the nonregular modules or
from Nikshych–Riepel Example 9.3. A proper subgroup of S4 containing S3 is
S3 itself. Thus its action on the four regular-module cosets is the usual
four-point permutation action, with a distinguished regular point p.

For either source, the image of a C4 generator cannot have order one or two,
since its square would give a regular degree-two component. It must therefore
be a four-cycle. All six four-cycles are conjugate under the S3 fixing p;
the exact verifier enumerates this conjugacy orbit. Consequently any two
source categorifications determine the same homomorphism to BrPic after an
allowed tensor equivalence of their neutral categories. Reversing the chosen
C4 generator does not change its degree-two subgroup.

## 4. The full coefficient module A, using the new model rather than triality

Let `A=Inv Z(Rep(D8))`. The group-double description gives

    A = Z(D8) x Hom(D8,C*) = C2^3.

There is exactly one nontrivial central invertible z whose underlying object
in Rep(D8) is the tensor unit. It is the tensor natural automorphism of the
identity which is +1 on the four invertibles and -1 on m. The regular S3
stabilizer fixes z, since it preserves the forgetful functor up to tensor
isomorphism. Therefore the orbit of z under S4 has size one or four.

The size-one alternative is impossible. Use the explicit C4 extension
realizing R11_1_104. If S4 fixed z, its degree-group C4 would fix z. In the
relative-center description of the center of a graded category, an invariant
invertible object has an equivariant lift unless its scalar obstruction in
`H^2(C4,C*)` is nonzero. This group is zero for a cyclic group. Hence z would
lift to a central invertible of the whole extension with underlying object
one. Such a lift is a tensor natural automorphism of the identity functor.

But tensor natural automorphisms of the identity of a fusion category are
characters of its universal grading group. R11_1_104 has universal grading
exactly C4 with neutral adjoint category D. Every such automorphism is
therefore trivial on D, whereas z acts as -1 on m. This contradiction proves
that the orbit of z has four distinct elements.

Call these four elements `w_0,w_1,w_2,w_3`, labeled by the four points of the
S4 action. They span A and have exactly one relation,

    w_0+w_1+w_2+w_3=0.

Indeed a relation of weight one would make a vector zero; a relation of
weight two would equate two vectors; and S4-translates of any relation of
weight three would imply a relation of weight two. Since four vectors in a
3-dimensional space are dependent, the weight-four relation is the only
possibility. This proves the **full S4-module identification**

    A = F2^4 / <(1,1,1,1)>.

This proof invokes the independently constructed R11_1_104 category only to
rule out an invariant z. It does not assume that the desired R11_1_153 model
exists, and it does not import a C3 or triality calculation. Alternatively,
under the temporary assumption that R11_1_153 exists, that category itself
gives the identical contradiction.

For a four-cycle t, choose basis w_0,w_1,w_2 and put w_3=w_0+w_1+w_2.
Then the action columns are `(2,4,7)` in binary encoding. Thus t is the
three-dimensional unipotent Jordan block over F2.

## 5. Independent cohomology check and its categorical implication

Let `N=t-1`. One has `N^3=0`, `rank N=2`, `rank N^2=1`, and
`ker N=im N^2`. The cyclic norm for C4 is zero, so

    H^2(C4,A) = ker N,
    H^2(<t^2>,A) = ker N^2 / im N^2.

Restriction in even degrees is the map induced by the identity. Hence the
restriction of every class in H^2(C4,A) is zero.

The independent verifier does not rely on that periodic-resolution formula.
It sets up all normalized inhomogeneous two-cochains on C4 with values in A:
there are 27 binary coordinates. It checks the full cocycle equation

    t^g c(h,k) + c(g+h,k) + c(g,h+k) + c(g,h) = 0

for all 64 triples. The cocycle space has dimension seven and the coboundary
space dimension six. All 128 cocycles are directly enumerated and checked.
For each, the restriction value c(2,2) is explicitly shown to lie in
`(1+t^2)A`, and an explicit normalized one-cochain on C2 is exhibited whose
coboundary equals that restriction. Thus every restricted class is zero.
The receipt stores preimages for a basis of cocycles.

ENO Theorem 1.3 classifies multiplication systems for the fixed C4
Brauer–Picard homomorphism by a torsor over H^2(C4,A). Consequently any two
such extensions, including the reference R11_1_104 extension and a putative
R11_1_153 extension, have equivalent multiplication systems on the degree-two
C2 subextension. Their associators may still differ by scalar H^3 data, but
scalar associator changes do not alter fusion coefficients or simple-object
duality. Their even fusion rings must therefore be based-isomorphic.

The reference even ring has every simple self-dual, while R11_1_153 has a
pair of distinct dual simples in degree two. These rings cannot be
based-isomorphic. Together with the accepted model replay, this proves the
claimed categorical incompatibility for R11_1_153.

## Primary sources checked

- Tambara–Yamagami, *Tensor categories with fusion rules of self-duality for
  finite abelian groups*, J. Algebra 209 (1998), 692–707: TY classification.
  ENO [arXiv:0909.3140v2](https://arxiv.org/html/0909.3140v2), §9.2,
  also recovers this classification. Gelaki–Naidu–Nikshych §4.1 displays
  the TY associator `alpha_(a,m,b)=chi(a,b) id_m` used above.
- Nikshych–Riepel,
  [arXiv:1309.5026v2](https://arxiv.org/html/1309.5026v2), §§9.1–9.2,
  Example 9.3 and Remark 9.4: the D8 and Q8 Brauer–Picard groups.
- Etingof–Nikshych–Ostrik,
  [arXiv:0909.3140v2](https://arxiv.org/html/0909.3140v2), Theorem 1.1,
  Theorem 1.3, §6 and §§7–8: central equivalence, invertible homogeneous
  components, and the multiplication/associator torsors.
- Marshall–Nikshych,
  [arXiv:1603.04318v3](https://arxiv.org/html/1603.04318v3), Proposition 3.1:
  the induction homomorphism has inner tensor autoequivalences as kernel.
- Gelaki–Naidu–Nikshych, *Centers of graded fusion categories*,
  [arXiv:0905.3117](https://arxiv.org/abs/0905.3117): relative-center
  equivariantization (Theorem 3.5) and the scalar obstruction to an equivariant lift.
- Gelaki–Nikshych, *Nilpotent fusion categories*,
  [arXiv:math/0610726](https://arxiv.org/abs/math/0610726), universal
  grading and tensor automorphisms of the identity (Proposition 3.9).

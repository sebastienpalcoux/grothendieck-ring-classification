# Five quadratic rank-ten cases: model-route audit

Status: research reduction only; no new categorification or exclusion is claimed here.

Later development: the relative-factorization gap recorded below was
subsequently addressed in the rank16_dual work. The ordinary-factor cases
114 and 115 now have a separately written and independently reviewed
exclusion proof in `ORDINARY_FACTOR_EXCLUSION.md`, using the complete
pivotal SO(3) classification of Etingof--Ostrik and central-algebra descent.
The earlier conditional discussions below are retained as a route audit;
the newer proof note supersedes their statement that no short bridge was
available. The Q-type cases require their separate semion/supercategory
argument and are not settled by this model-route audit.

## Verified source invariants

The input is `research/catalogue.json`, frozen from public commit
`81ba2b63dad3a46c6aab70c39cd4f6a28d0e58cc`.
For each of R10_1_114,115,152,153,179 the dimension profile is
`1^4,(2+2sqrt(2))^2,(3+2sqrt(2))^4`, with global dimension
`96+64sqrt(2) = FPdim(PSU(2)_6)^2`.
All have formal-codegree polynomial
`(t-16)^3 (t-8)^5 (t^2-192t+1024)`.
The first four have invertible group C4, and the last has C2 x C2.
All have nonselfdual noninvertibles; thus none is isomorphic to the previously
constructed, wholly selfdual R10_1_21.

## Ordinary PSU(2)_6 permutation construction

Write P=PSU(2)_6 with simples 1,f,x,y=fx, d(x)=d(y)=1+sqrt(2).
The established construction for R10_1_21 is
`((P boxtimes P)^swap)_(1 + (f,f)_-)`.
Its categorical fixed-point calculation proves that its four invertibles form
C2 x C2; all its simples are selfdual. Consequently the construction does not
supply any of these five cases merely by relabeling objects.
Changing a basis or using Galois-conjugate quantum-group parameters does not
change this duality obstruction in this construction.

The other equivariant lift h=(f,f)_+ is ruled out by an explicit multiplicity,
not just by dimension or duality. In W=(P boxtimes P)^swap one has
`(d_x^+)^2 = d_1^+ + d_x^+ + d_y^+ + p_1x + p_1y + p_xy`.
Induction to modules over 1+h identifies d_x^+ with d_y^+; its image b is
simple because h does not fix d_x^+. Consequently b^2 contains 2b. Thus this
second lift cannot produce any multiplicity-one case. This computation
avoids relying on an unaudited assertion about fixed-point resolution.

## Exceptional monoidal automorphism: theorem and exhausted obvious actions

Cain Edie-Michell, *The Brauer-Picard groups of the fusion categories coming
from the ADE subfactors*, arXiv:1709.04721v2, Lemma 4.10, proves
`Aut_tensor(Ad(A7)) = C2`. Its nontrivial element S exchanges x and y.
The source also computes BrPic(Ad(A7))=D8 and describes its bimodules in §6.2.
Primary source: https://arxiv.org/abs/1709.04721
Local downloaded source: `edie_article.pdf`, with extracted `edie_article.txt`.

Let B=(P boxtimes P)_(1+f boxtimes f), rank eight. It has dimensions
`1^2,d^4,(d^2)^2`. The action induced by S boxtimes S on B does have orbit
counts that would give the desired rank-ten dimension profile on equivariantization.
However, this is NOT a multiplicity-one construction: it preserves the embedded
first-factor P, and equivariantizing that subcategory gives a rank-five
near-group category. Its unique noninvertible object a has dimension 2d and
satisfies `a^2 = sum_{g in G} g + 4a` for a group G of order four.
Thus the ambient equivariantization has multiplicity at least four.
Dimension matching alone would have been misleading here.

The factor-exchange action multiplied by S boxtimes S is conjugate to ordinary
factor exchange via S boxtimes Id. When these functors descend compatibly to
the chosen central algebra, this gives no genuinely new action class.
Factor exchange multiplied by S in only one factor has square S boxtimes S,
which is nontrivial on the four small simple objects of B, so it is not a C2
action of the required orbit type.

## Pseudo PSU(2)_6 is not a plug-in replacement

The nonselfdual rank-four category Q with rules
`f^2=1`, `fx=y`, `x^2=y^2=f+x+y`, `xy=1+x+y`
exists by the subfactor construction of Liu–Morrison–Penneys,
*1-supertransitive subfactors with index at most 6+1/5*,
arXiv:1310.8566, Theorem 3.12 (two complex-conjugate examples).
Primary source: https://arxiv.org/abs/1310.8566
The recent Vercleyen–Slingerland paper independently identifies this source:
https://link.springer.com/article/10.1007/s00220-026-05705-2
The ring has trivial universal grading and a unique nonunit invertible.

Mäurer–Thiel, *Computing the center of a fusion category*,
arXiv:2406.13438v3, Table 7.1, reports that the center of each of the four
listed associator forms of Q contains a simple rank-seven fusion subcategory
of half the total dimension. If this computed datum is accepted, that
subcategory is nondegenerate: its Müger center is a fusion subcategory, hence
trivial or the whole category; the latter would make it symmetric, impossible
at nonintegral global dimension. Müger decomposition then gives a rank-two
nondegenerate pointed factor, a semion category. Trivial universal grading
makes the underlying central invertible the unique f. It therefore has
self-braiding +i or -i and nontrivial pointed associator.

Consequently the diagonal central object f boxtimes f in Q boxtimes Q is a
fermion, and `1+f boxtimes f` is NOT a central commutative algebra. In
Q boxtimes conjugate(Q) the diagonal can be bosonic, but complex conjugation
reverses the twist of the unique central invertible. Thus Q and its conjugate
are not monoidally equivalent, so the ordinary factor-swap equivariantization
cannot simply be invoked. This checks a tempting construction route; it is
not a nonexistence theorem for the five rank-ten rings.
Primary center source: https://arxiv.org/html/2406.13438v3

## Important limit on the rank-sixteen Morita reduction

For the involution h fixing the two 2d-dimensional simples, A=1+h exists:
the fixed simple supplies a rank-one module over the pointed subcategory,
trivializing the restricted associator. A separate agent proves that the
projective stabilizer cocycles on the two fixed simples are trivial, forcing
a rank-sixteen dual with dimensions `1^4,d^8,(d^2)^4`.

That profile does NOT force a Deligne square. As a control, the known model21
has a central boson s, and its corresponding Morita dual is B semidirect C2,
where B is the rank-eight category above. This dual has a faithful C2 grading,
whereas P boxtimes P has trivial universal grading. Any argument identifying
all such rank-sixteen duals with P boxtimes P solely from the dimensions would
therefore be false.

For any fusion category with this rank-sixteen dimension profile, elementary
positive-dimension arithmetic forces
`X X* = 1 + Y + Z`
for every d-dimensional simple X (allowing Y=Z until multiplicity or another
argument rules it out). In particular the invertible stabilizer of X is
trivial. The group of four invertibles therefore has two free left orbits on
the eight small simples, and two free right orbits. A product of two small
simples is either one invertible plus two small simples, or one large simple.
These restrictions are useful, but they do not by themselves establish the
needed rank-four subcategories, central lift, or categorical factorization.

No accepted case decision has been changed by this audit.

## Alternative order-two algebras in the known rank-sixteen dual

The separately reconstructed based tensors for the canonical Morita duals
of cases 21 and 114 are identical. This is a based-ring statement, and does
not identify associators or module-category structures.

For the known associator of case 21, write D=B semidirect_T C2, where T
exchanges the two P factors in B. Its four invertibles have representatives
1,f,t,ft, where f belongs to B and t to the other graded component.

The algebra 1+f, if considered, cannot give a rank-ten dual: f acts freely
on all sixteen simples of D. The left-right H x H action therefore has
eight size-two orbits with cyclic stabilizer C2. Every projective
representation of that cyclic stabilizer is equivalent to an ordinary
one, and each orbit gives two simple bimodules. Its dual has rank sixteen.

The remaining candidate 1+ft also does not supply a new rank-ten ring.
If its restricted associator is nontrivial, it is not an algebra. If it is
an algebra, ft gives a coherent C2 section of D -> C2, with conjugation
action phi=Ad_f composed with T on B. The central half-braiding of f in B
gives a monoidal isomorphism Ad_f -> Id_B, so phi is monoidally isomorphic
to T. Moreover U(B)=1: the images of the two P factors generate B, and in
each factor x^2=1+x+y forces every degree to be trivial. Hence
Aut_tensor(Id_B)=Hom(U(B),C^*)=1. The coherent C2 action structure is then
unique once the functor is fixed up to monoidal isomorphism. It follows
that the dual for 1+ft, when defined, is B^phi equivalent to B^T, the known
case 21. This exhausts the order-two pointed algebras in this particular D.

For the identity-automorphism fact, see Gelaki--Nikshych, *Nilpotent fusion
categories*, arXiv:math/0610726, Proposition 3.9 (equivalently EGNO,
*Tensor Categories*, Proposition 4.14.3).
Primary source: https://arxiv.org/abs/math/0610726

## Conditional extension uniqueness, and the precise unresolved gap

Suppose one had established that an unknown rank-sixteen dual has neutral
category categorically equivalent to this B and odd invertible bimodule
equal to the known factor-swap bimodule. Then the extension freedom is
particularly small. The forgetful map Inv Z(B) -> Inv B is injective,
because its kernel is Aut_tensor(Id_B)=1. The central fermion supplies its
nontrivial element, so Inv Z(B)=C2.

Etingof--Nikshych--Ostrik, *Fusion categories and homotopy theory*,
arXiv:0909.3140v2, Theorem 1.3, parametrizes extensions, subject to its
obstructions, by the Brauer--Picard homomorphism, an H^2 torsor with
coefficients Inv Z(B), and an H^3(C2,C^*) torsor. In this fixed-component
situation, changing the nontrivial H^2 datum replaces t^2=1 by t^2=f,
changing the invertible group from C2 x C2 to C4. The remaining H^3 sign
twist makes the associator on the section t nontrivial and forbids 1+t.
Thus the known based ring together with its canonical order-two algebra
would select the known extension, *under the categorical hypotheses just
stated*.
Primary source: https://arxiv.org/abs/0909.3140

Those hypotheses are not currently proved. In particular, a rank-eight
fusion ring generated by two rank-four subrings intersecting in Vec(C2)
does not by itself supply a relative Deligne-product equivalence or a
central half-braiding. Neither BrPic(P)=D8 nor the ordinary classification
of twisted Deligne products fills this shared-subcategory gap. Therefore
this conditional argument must not be used to mark case 114 excluded.

The recent Etingof--Nikshych--Ostrik manuscript *Twisted Deligne products
of semisimple tensor categories*, arXiv:2607.19560 (July 2026), concerns
exact factorizations / categorifications of tensor products of based
rings. Its no-grading hypothesis is promising only after the necessary
exact factorization has been established. The present two rank-four
factors intersect in Vec(C2), so it does not directly apply.
Primary identifier: https://arxiv.org/abs/2607.19560

No genuinely short remaining route to a new categorical decision has
been established by this audit. The next mathematical requirement is
classification of the rank-eight neutral categories and their relevant
tensor actions, or an independent coherent construction with exact
coefficient matching.

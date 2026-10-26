# The rank-nine quotient branch: a second pointed de-equivariantization

This proof does not infer a C3 grading from the dimension type. Indeed,
the actual surviving quotient rings below have trivial universal grading.

Let C be one of the twenty dimension-48 source rings, categorified over
C, and let b be the central boson supplied by solvability. In this branch
b fixes the two dimension4 simples and fixes neither dimension2 simple.
The quotient D in C=D^C2 has four invertibles and five dimension2 simples.
Its actual C2 action fixes each invertible and one dimension2 simple T;
it exchanges the other four in two pairs. Identifying X and bX in the
source gives its full invariant-orbit ring, of rank7 and orbit dimensions
(1,1,1,1,2,4,4).

## Exhaustive reconstruction without a census assumption

rank9_reconstruct.py reconstructs every possible full quotient ring from
these invariant-orbit products. It allows both groups of order4, every
homomorphism to S5 for the left action, every antihomomorphism for the
right action, all commuting action pairs, and every possible duality.
Frobenius reciprocity determines all coefficients involving an invertible.
The other125 coefficients are equated only by necessary reciprocity,
duality, the actual C2 action, and associativity with an invertible factor.
At most eight integer variables remain. Their exact finite upper bounds
come from the invariant-orbit coefficients and dimension equations;
no multiplicity-one assumption on D is used. An exhaustive bounded
integer recursion solves these linear equations, followed by full exact
associativity and reciprocity for each remaining tensor.

There are four invariant-orbit types. Their outcomes are:

| Source rows | Labeled associative lifts | Based-ring classes |
|---|---:|---:|
| R175 | 24 | 1, invertible group V4 |
| R216, R319 | 0 | 0 |
| R244 | 8 | 1, invertible group C4 |
| R410, R526 | 0 | 0 |

Every central involution giving this branch is bound separately in
rank9_reconstruction.json. The two surviving tensors are frozen in full.
The verifier checks that each has trivial universal grading and exactly
one nonidentity central invertible involution h; h fixes all five
noninvertible simples. It also checks that the actual outer C2 action
preserves h. This conclusion is drawn from every possible quotient table,
not merely a successful match against a supplied list.

## Categorical closure of both surviving rings

A hypothetical D is solvable because its dimension24 has two prime
factors. Since U(D)=1, its last solvable step is a prime cyclic
equivariantization, rather than a graded extension. Its invertible group
has order4, so this prime is2. The canonical boson is necessarily the
unique h just identified. Write D=E^C2, with FPdim(E)=12.

The simple-orbit formula now forces E to be pointed. D's four
invertibles, paired by h, give two fixed invertibles of E. Each of its
five h-fixed dimension2 simples forgets to a free pair of invertibles
of E. These twelve invertibles exhaust dimension12.

The central lift of h in D is unique because

    ker(Inv(Z(D))->Inv(D)) = Aut_tensor(Id_D) = Hom(U(D),C*) = 1.

The outer C2 action from C=D^C2 preserves h and therefore its unique
central lift. It preserves the resulting central Tannakian Rep(C2).
Equivariantizing this subcategory gives a central Tannakian Rep(P) in C,
where |P|=4; iterated de-equivariantization gives C=E^P. This includes
both order-four groups and all possible action coherences.

Every equivariantization of a pointed category is group-theoretical:
it is Morita equivalent to the crossed product E crossed P, whose
simple objects are all invertible. Thus C is group-theoretical for
either surviving quotient ring. The other two orbit types have no
based-ring quotient at all. This closes every rank-nine branch.

The argument needs no classification of dimension24 categories, no
unitary-only reconstruction premise, and no assertion that a general
equivariantization of a group-theoretical category is group-theoretical.

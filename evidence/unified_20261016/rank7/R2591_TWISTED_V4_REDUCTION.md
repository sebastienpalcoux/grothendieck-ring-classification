# R7_4_2591: a twisted V4 Morita reduction

This general complex-category reduction is the input to the complete exclusion
proved in `R2591_STAGED_MORITA_EXCLUSION.md`. The reduction itself does not
construct a category.
Let t=2+sqrt(5). The source ring has invertibles G=V4, a simple X of
dimension 2, and a dual pair Y,Z of dimension 2t. Every element of G fixes
X,Y,Z on both sides. Its relevant products are X²=sum G, XY=YX=2Z,
XZ=ZX=2Y, and Y²=2X+4Y+4Z.

## Projective action notation

The pointed associator is trivial, since the integral subcategory is a
Tambara–Yamagami category. Choose its standard normalization. For each
G-fixed simple W, choose isomorphisms gW→W and Wg→W. Their left and right
projective classes are denoted alpha_W,beta_W in H²(G,C*)=F2. The mixed
commutator is a 2×2 matrix B_W over F2, using values (-1)^b.
Thus the projective G×G action on the multiplicity space of a bimodule
supported on W is described by an alternating 4×4 matrix with diagonal
blocks alpha_W J,beta_W J and off-diagonal block B_W, where
J=[[0,1],[1,0]]. A matrix of rank 2r has irreducible projective
representations of dimension 2^r, and has 2^(4-2r) inequivalent such
representations.

In the standard TY normalization alpha_X=beta_X=0, and B_X=chi is the
matrix of the nondegenerate symmetric TY bicharacter. Duality gives
alpha_Z=beta_Y and beta_Z=alpha_Y. The mixed matrices for a dual pair
are transposes; only their ranks will be needed.

More generally, if W occurs with multiplicity n in U tensor V, the
left G action on U and right G action on V induce a projective G×G
action on that n-dimensional multiplicity space. Its alternating
matrix has diagonal blocks

    (alpha_U-alpha_W)J, (beta_V-beta_W)J

and mixed block B_W, up to harmless transpose and sign. Consequently,
the rank of this matrix cannot exceed 2 log_2(n).

## Multiplicity two forces the cocycle classes

Apply the rank bound to the multiplicity-two X in Y². The matrix is

    [[alpha_Y J, chi], [chi^T, beta_Y J]].

Since chi is invertible, rank at most two forces alpha_Y=beta_Y=1.
Indeed, if either diagonal block vanishes, the rank is four. If both
are J, the Schur complement vanishes because chi^T J chi=J for every
invertible 2×2 matrix over F2. Thus alpha_Z=beta_Z=1 as well.

Next use the multiplicity-two Z in XY. Its matrix is

    [[J, B_Z], [B_Z^T, 0]].

Its rank is two plus the rank of B_Z^T J B_Z, so rank at most two is
equivalent to det(B_Z)=0. Duality gives det(B_Y)=0 too.

## Twist the full regular algebra

Let beta represent the nontrivial class in H²(G,C*), and let
A_beta=sum_{g in G}g with multiplication twisted by beta. This is a
connected separable algebra. Twisting changes both diagonal cocycle
blocks by J and does not change the mixed block.

For X the twisted block is [[J,chi],[chi^T,J]], of rank two. It gives
four simple bimodules with underlying object 2X. Each has dual-category
FP dimension FPdim(2X)/FPdim(A_beta)=1.

For Y or Z the twisted block is [[0,B],[B^T,0]], of rank 2 rank(B).
We already know rank(B)≤1. If rank(B)=0, the resulting simple
bimodules would have underlying object Y or Z, and FP dimension t/2.
That is impossible: t is an algebraic unit of norm -1, so t/2 has
norm -1/4 and is not an algebraic integer. Therefore rank(B)=1 for
both Y and Z. Each block gives four simple bimodules with underlying
object 2Y or 2Z, of FP dimension t.

The pointed support gives four invertible bimodules, each with
underlying object A_beta. Thus the full Morita dual has exactly eight
invertibles and eight noninvertibles of dimension t.

For any noninvertible W in the dual, t²=1+4t implies that W W* has
exactly one invertible summand. Hence its invertible stabilizer is
trivial, and the eight invertibles act freely and transitively on the
eight noninvertibles. The dual is a free-orbit quadratic category.

## Consequence and completion by staged Morita theory

The published Galois pseudo-unitarity theorem for fusion categories
with exactly two FP dimensions applies to this dual. Global dimension
and FP dimension are preserved by Morita equivalence, and algebra
twisting commutes with Galois conjugation. Hence every complex
categorification of R7_4_2591 is Galois conjugate to a pseudo-unitary
category.

The inverse algebra is supported on a subgroup V4 of the order-eight
invertible group K of the dual. Consequently K is C4×C2, C2³, or D8.
The pointed associator of the dual need not be trivial. The staged Morita argument in `R2591_STAGED_MORITA_EXCLUSION.md` excludes
the resulting quadratic category together with this inverse V4 algebra,
without any assumption on its pointed associator. A classification of
untwisted generalized Haagerup categories alone would not have justified
that conclusion.

The source-bound verifier checks the source products, dimensions,
duality, and every finite-field rank implication used above. Its role
is to verify the small exact linear algebra, not to construct
associators.

The Galois pseudo-unitarity reference is A. Schopieray,
*Categorification of integral group rings extended by one dimension*,
J. London Math. Soc. 108 (2023), 1617–1641, published Lemma 3.1,
DOI:10.1112/jlms.12789. The projective-block calculations are independent
of a unitary or spherical structure.

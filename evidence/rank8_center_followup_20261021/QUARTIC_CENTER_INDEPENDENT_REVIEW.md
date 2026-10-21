# Independent quartic-center review for the necessary-condition addendum

This research record is outside both repositories and does not alter the
accepted 21 October publication or any frozen mathematical source.

## Formula and scope

Let a hypothetical categorification of R721 or R1154 be transported to its
pseudo-unitary Galois conjugate using the already accepted unrestricted
sphericalization gate. Write D=FPdim(C), and use the unnormalized S matrix of
Z(C), whose global dimension is D squared. For an irreducible source-algebra
representation E of degree m_E and formal codegree f_E,

    S(A_E,Z) = D/(f_E m_E) chi_E(FZ).

References: Deshpande, arXiv:1611.04486, Lemma 4.3, Corollary 4.5 and (39);
Deshpande, arXiv:1811.08447, Theorem 1.1 specialized to the ordinary modular
category, for Verlinde. These are spherical/modular statements and do not
require C-star unitarity.

The source character check chi_E(x*)=chi_E(x) gives
S(A_E*,Z)=S(A_E,Z*)=S(A_E,Z). Nondegeneracy of S therefore proves that every
distinguished A_E is self-dual. This argument does not assume that the high
central simples are self-dual and does not require analytic conjugation.

For four self-dual distinguished objects, Verlinde and Frobenius reciprocity
give the bilinear fusion-coefficient pairing

    sum_Z N(i,j;Z) N(k,l;Z)
      = D^(-2) sum_Y S(i,Y) S(j,Y) S(k,Y) S(l,Y)/dim(Y)^2.

Without self-duality, the last two S factors must use k* and l*. In particular
the unstarred formula must not be transferred to arbitrary complex-character
rows. The ordinary transpose in X^T X is justified by the integer fusion
multiplicity pairing, independently of categorical unitarity.

Subtract the unit and the four nonunit distinguished outputs from this
pairing. The resulting rational 10-by-10 matrix G is X^T X, where every row
of X represents one individual high simple, including separate rows for
different simples with identical forgetful columns. The tensor functor
equations are M X = T. The matrix-block degree m_E=2 belongs in the displayed
S normalization; it does not duplicate its distinguished central simple.

## R721 uniqueness

For each of the four complete integer restriction patterns and both allowed
character assignments, the exact minimum-norm solution X0 satisfies

    G - X0^T X0 = (2/3) h^T h,
    h = (0,0,0,0,1,1,-1,1,-1,1).

Every possible integral X is real. Orthogonality of the minimum-norm solution
to ker(M) gives X=X0+t h, Mt=0, and sum_i t_i^2=2/3. Since h has a coordinate
equal to one, integrality fixes each t_i modulo Z. The bound |t_i|<1 leaves a
finite coordinate set. The challenge's unique per-coordinate minima sum to
exactly 2/3, so every coordinate is forced; its final M X=T and X^T X=G checks
prove existence of that unique necessary matrix.

The independent script instead reconstructs X0 using M.pinv(), obtains h
from the residual Gram itself, and exhausts all permitted coordinate choices.
It re-enumerates the entire 240-point restriction Gram box, obtaining four
patterns. For each character assignment its four coordinate boxes have
sizes 1,2,2,4 and each has exactly one solution. The high-simple counts are
17,14,14,11, respectively. All ten distinguished pair decompositions are
therefore unique within each case. This does not determine products involving
arbitrary high objects or prove a unique center fusion ring or category.

## Positive control and R1154 boundary

The independent positive control derives the three ordinary S3 characters
from permutations, derives their tensor coefficients by exact character
inner products, and uses the eight actual simples of Z(Vec(S3)). All 27
cubic and 81 quartic identities pass. Its matrix-block normalization is
D/(f m)=6/(3*2)=1.

The initial challenge's R1154 calculation passes 35 scalar fourth moments for
all 1,238 retained integral restriction patterns. This initial stage does not
test simultaneous nonnegative integral pair-product Gram factorization. The
subsequent independently reviewed norm/propagation and low-action extension
are recorded in CENTER_FOLLOWUP_REVIEW.md. None of these results excludes
either source ring or constructs a category.

## Replay

With the repository supplied explicitly (the default root is the current
working directory):

    python quartic_center_independent_review.py --root /path/to/repository
    python -O quartic_center_independent_review.py --root /path/to/repository

The paired JSON receipt binds this independent script, the immediate frozen
source helpers and the frozen main publication source-manifest identity.
It is a followup research review, not an amended main-release certificate.

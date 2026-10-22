# A dimension match and its algebra obstruction

This section rules out one precisely specified construction, not the
fusion ring R8_3_1154. Let D=540+240 sqrt(5), let C=SU(3)_7, and let F
be a Fibonacci category, with nontrivial simple dimension
phi=(1+sqrt(5))/2. There is an exact and initially promising identity

    FPdim(C) = 750+330 sqrt(5),
    FPdim(F) = (5+sqrt(5))/2,
    FPdim(C tensor F) = 5D.

However, C tensor F contains no connected separable algebra of FP
dimension 5. Consequently a fusion category of dimension D cannot be
obtained as its category of modules over a connected etale algebra.
Braiding reversals do not change this obstruction.

## Positive coefficient criterion

Let K be a real number field, and suppose a Q-linear functional
ell:K→Q satisfies ell(1)=0, ell(FPdim(X))≥0 for every simple X of a
fusion category B, and equality holds precisely for invertible X.
Then every connected separable algebra in B with rational FP dimension
is supported on invertible objects. Each invertible has multiplicity at
most one in such an algebra. In particular its dimension is at most
the number of invertible simples of B.

Indeed, rationality makes ell(FPdim(A)) zero, so positivity excludes all
noninvertible summands. Regard A as a right A-module. Connectedness gives
End_A(A)=Hom_B(1,A)=C, and separability makes the module category
semisimple, so A is simple as a module. For an invertible g, g tensor A
is also simple. Free-module adjunction identifies

    Hom_B(g,A) = Hom_A(g tensor A,A).

Schur's lemma bounds this space by one. This argument needs no braiding
and no classification of algebra multiplication. It is useful whenever
a field-coordinate functional separates the noninvertible dimensions
from the rational axis.

## Complete exact dimension calculation

The 36 SU(3)_7 labels are (a,b) with a,b≥0 and a+b≤7. Their dimensions
are

    d(a,b)=[a+1][b+1][a+b+2]/[2],
    [n]=sin(n pi/10)/sin(pi/10).

The quantum Weyl formula and global-dimension convention are given in
Coquereaux, [Global dimensions for Lie groups at level k and their
conformally exceptional quantum subgroups](https://arxiv.org/abs/1003.2589),
§§2.1–2.2. The formula is evaluated here exactly: put t=[2], so
t²=(5+sqrt(5))/2, use [n+1]=t[n]−[n−1], and remove one factor t
from every even quantum integer. The numerator has either one or three
even factors, so division by [2] leaves an element of Q(sqrt(5)).

The verifier enumerates the entire 36-label alcove, then all 72 product
labels. Every dimension has nonnegative sqrt(5) coefficient, strictly
positive except at the three labels (0,0,0), (0,7,0), (7,0,0), whose
dimensions are one. Thus ell(a+b sqrt(5))=b satisfies the criterion.
A rational-dimensional connected separable algebra has dimension at
most three, contradicting the required dimension five.

For the connected etale module construction the dimension formula is
FPdim(B_A)=FPdim(B)/FPdim(A); see Davydov–Muger–Nikshych–Ostrik,
[The Witt group of non-degenerate braided fusion categories](https://arxiv.org/abs/1009.2117),
Lemma 3.11 (§3.4). We use this formula only for the stated module fusion-category
construction; a general noncommutative algebra's module category need
not itself carry this fusion-category structure.

Replay:

    python3 evidence/rank8_creative_20261022/r1154/verify_quantum_subgroup_route.py

The receipt `quantum_subgroup_route.json` includes every simple dimension,
the full dimension histogram, and the exact global-dimension identity.
This does not rule out longer constructions involving other ambient
categories, other index values, or intervening Morita equivalences.

# R8_3_928: two new necessary fusion-matrix reductions

29 October 2026. **The ring remains unresolved.** No category or associator
has been constructed, and none of the four retained center patterns is
eliminated by the calculations below.

The new result reconstructs actual necessary fusion matrices, rather than
just checking dimensions or moment constraints. It leaves a considerably
smaller modular-ring reconstruction problem in two of the patterns.

## Inputs and scope

Use the inherited pseudo-unitary existence reduction and semion splitting
Z(C)=Sem⊠B. The previous report proves B is simple, with ranks23,20,20,17
for patterns40,49,186,191. Put

    D=144+96sqrt(2)+80sqrt(3)+56sqrt(6),
    L=D/sqrt(2),        w=D/4.

Thus FPdim(B)=L². Write B0=1,B1,B2,B3 for the four Galois-unit simples,
with dimensions

    r0=1,
    r1=15+10sqrt(2)+8sqrt(3)+6sqrt(6),
    r2=21+14sqrt(2)+12sqrt(3)+8sqrt(6),
    r3=35+24sqrt(2)+20sqrt(3)+14sqrt(6).

The automorphisms sigma0,sigma1,sigma2,sigma3 act on (sqrt2,sqrt3)
by (++),(-+),(--),(+-), respectively; rσ=D/sigma(D).
Their normalized S-columns are completely determined:

    uσ(i)=rσ sigma(d_i)/L.

Indeed modular Galois symmetry gives the fusion eigenvalue
lambdaσ(i)=rσ sigma(d_i)/d_i, and S(i,Bσ)=d_i lambdaσ(i)/L.
These four real columns are orthonormal. This uses the positive modular
normalization, not a unitary associator hypothesis.

There is a fifth distinguished simple W in B, of dimension w. It is G times
the dimension-D/4, multiplicity-two constituent of the canonical algebra
in Z(C). Its source restriction is

    F(W)=2g+2X1+2X2+2X3+2X4+3X5+3X6.

It is selfdual: this dimension occurs only once in B. In the ordered basis
starting (B0,B1,B2,B3,W), its normalized S-column is

    uW=(1,1,1,1,-2,0,...,0)/(2sqrt2).

To check this formula, use the full two-dimensional source-ring character
chi, which is2 at1,-2 atg, and0 elsewhere. The distinguished-center character
formula gives S_Z(B4,Z)=chi(F(Z))/8; semion splitting multiplies this row by
sqrt2 on B. Its only nonzero columns in B are precisely the five displayed
ones. This calculation is independently bound to the previously accepted
source tensor/low-column receipt; it does not guess high S-entries.

## 1. One entire fusion matrix is forced in every pattern

**Proposition.** Multiplication by W has the unique matrix

    N_W = sum_sigma [w/rσ] uσ uσ^t - 2 uW uW^t.

Consequently it has rank5 and trace142. Every entry is fixed by the dimension
multiset of B.

**Proof.** Verlinde diagonalizes N_W by normalized S. Its eigenvalues are
w/rσ at the four Galois-unit columns,-2 at W, and0 at every other column,
by the preceding explicit W row. These five eigenvalues are nonzero. Their
sum is sum_sigma sigma(D)/4-2=142. The spectral expansion follows. QED.

All four patterns give nonnegative integer matrices, with the correct unit
row, dimension eigenvector, and symmetry. For example their common first
five rows/columns are

    [0 0 0 0  1]
    [0 3 4 7  8]
    [0 4 6 10 11]
    [0 7 10 17 18]
    [1 8 11 18 17].

The full matrices are in `spectral_reduction.json`. Passing this matrix test
does not provide the other fusion rules or an S-matrix completion.

## 2. A second whole fusion matrix is forced in patterns49 and191

Let C0=B3 (the letter C0 here denotes a simple object, not the source category),
and let lambda(i)=r3 sigma3(d_i)/d_i. Outside the four Galois-unit columns,
these eigenvalues are all±1. In patterns49,191 exactly two are+1: W and the
unique simple of dimension48+36sqrt2+28sqrt3+20sqrt6. In patterns40,186
there are five+1 eigenvalues instead.

Define the entirely known rational symmetric matrix

    M=-I + sum_sigma [lambda(Bσ)+1] uσ uσ^t.

Then N_C0=M+Q, where Q is twice the orthogonal projection onto the+1
eigenspace outside the four Galois-unit columns. In particular Q is positive
semidefinite, Q²=2Q, and its trace is4 for patterns49,191 (10 otherwise).
No unknown twist is used here.

The low4×4 block of N_C0 is fixed by the Verlinde formula from the known
four S-rows and all dimensions:

    [0 0 0 1]
    [0 3 5 7]
    [0 5 6 10]
    [1 7 10 17].

Its entries involving W are fixed by N_C0(i,W)=N_W(i,C0). Subtracting M
therefore fixes the entire leading5×5 block of Q as

    1/4 * [ 3 -1 -1  3 -2]
          [-1  3  3 -1 -2]
          [-1  3  3 -1 -2]
          [ 3 -1 -1  3 -2]
          [-2 -2 -2 -2  4].

This block already has trace4, is positive semidefinite, and squares to
twice itself. In patterns49 and191 no trace remains for any other diagonal
entry of Q. A positive-semidefinite matrix with a zero diagonal entry has
zero in its entire corresponding row and column. Thus all other rows and
columns of Q vanish, and N_C0 is uniquely forced.

The two resulting full matrices are nonnegative integral, have the correct
unit rows and dimension eigenvectors, commute with N_W, and square to the
independently computed spectral square. They therefore give a stricter
necessary target, not a contradiction. In patterns40,186 the remaining
positive projection has rank3; this argument does not uniquely reconstruct
N_C0 there.

## 3. A forced central second indicator

The new fusion matrix also gives N_WW^W=17. Because W is selfdual, the
space Hom(1,W tensor W tensor W) has this odd dimension. The main theorem
of Fuchs–Runkel–Schweigert, *A reason for fusion rules to be even*, in the
braided sovereign category B forces nu2(W)=+1: if its indicator were-1,
that space would have a nondegenerate alternating bilinear form and hence
even dimension. The primary proof is https://www.esi.ac.at/preprints/esi1099.pdf.

It follows that the original canonical summand B4=Semion tensor W has
nu2(B4)=-1. Its multiplicity in the canonical algebra is2, so this causes
no conflict with the symmetric Frobenius pairing on that algebra. This
indicator computation is a further necessary condition; it is not an
exclusion. The argument explicitly uses the braiding on B.

## 4. Further attempts and retained gap

The Galois-unit fusion spectra were computed exactly. Their first six power
traces, all distinguished triple fusion coefficients, and the forced matrices
are integral and nonnegative where required. No obstruction is obtained
from these necessary conditions. Balancing equations for the two forced
matrices reduce to systems with remaining free phase sums; they have not
produced a contradiction. Their feasible linear solutions are not asserted
to be roots of unity or modular data.

The central semion by itself cannot be removed to make an ordinary rank-four
fusion category; its pointed associator is nontrivial. Likewise the simple
modular factor has a nontrivial étale algebra, so results classifying
**completely anisotropic** simple modular categories do not apply. The known
E21 model has already been ruled out as a direct Morita source by earlier
module rigidity. Those invalid shortcuts were not used.

The precise remaining problem is a consistent completion of the necessary
fusion matrices and modular constraints, together with categorical existence,
or a universal contradiction. This note resolves neither side.

## Replay and references

Run `python verify_spectral_reduction.py` in this directory. The script uses
only the Python standard library and the prior exact quartic helper, hashes
the two source receipts, and writes all matrices and exact checks. It takes
seconds; it performs no associator or unbounded matrix search.

The general primary sources for the spectral arguments are the Verlinde
formula and modular Galois symmetry, for example Dong–Lin–Ng,
*Congruence property in conformal field theory*, arXiv:1201.6644,
https://arxiv.org/abs/1201.6644, and Ng–Wang–Zhang,
*Modular categories with transitive Galois actions*, §2,
https://arxiv.org/abs/2007.01366. No transitivity hypothesis is imposed here;
only their standard Galois identities are used. The case-specific center
character identity and exhaustive four-pattern input are inherited from the
archived project proofs, explicitly hashed by the verifier.


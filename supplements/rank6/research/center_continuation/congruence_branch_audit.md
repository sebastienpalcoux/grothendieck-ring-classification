# Independent congruence audit of the rank-22 witness

Scope: these conclusions concern the specified rank-22 positive-dimensional
central-induction witness for `R6_3_215`. They do **not** exclude all central
induction witnesses, and therefore do not by themselves exclude the ring.

Assume the twist analysis has established the following spectrum:

- six specified self-dual low objects have twist 1;
- four objects of type A have twists `z {1,-1,i,-i}`, with `z^4 = ±1`;
- eight objects of type B have the eight quadratic-nonresidue 17th roots;
- four objects of type C all have twist -1.

## Every object is self-dual

Duality preserves twists. Hence each A or B object is self-dual, since its
twist has multiplicity one, and the low objects are self-dual by hypothesis.
The negative eigenspace of charge conjugation, if nonzero, is therefore
contained in the C subspace, on which T=-I. It is invariant under S and T.
On this space, the anomaly-free center relation `(ST)^3=S^2` implies
`-S^3=S^2`, so S=-I. This contradicts S^2=-I on that space. Consequently
charge conjugation is the identity and the modular representation is even.

## The 17 and 2 parts separate

The congruence property and the Chinese remainder theorem express the
representation as a sum of tensor products `U_2 ⊗ U_17`, with levels dividing
8 and 17 (or 4 and 17 in the fourth-root branch). A nontrivial irreducible
`U_17` has a nontrivial T eigenvalue: otherwise T and its conjugates act
trivially, and these generate the group. For each nontrivial 17th-root
eigenvalue, every T eigenvalue of `U_2` would produce a corresponding mixed
global eigenvalue. The displayed spectrum contains no such mixed roots.
Thus T acts trivially on `U_2`; its conjugates generate that factor too,
so `U_2` is trivial. This proves that every summand with nontrivial 17 part
is pure level 17.

The ordinary irreducible SL(2,F_17) T spectra (Plavnik--Schopieray--Yu--Zhang,
arXiv:2111.05228, Appendix A, Table 1) leave exactly the even nine-dimensional
Weil representation with nonresidue eigenvalues, together with trivial
representations. Its T=1 space is one-dimensional; S compressed to that
line is `-1/sqrt(17)`. The odd eight-dimensional Weil representation cannot
occur in an even representation. Other nontrivial irreducibles have both
quadratic residue classes in their T spectra. The remaining representation
therefore has dimension 13 and level dividing 4 or 8.

## The fourth-root branch is impossible

For any even representation of level 4, let P project onto T=1. The
operator PSP has possible eigenvalues only `1,-1/2,0`. This follows without
an irreducible-character table: compute the operator in the regular
representation of PSL(2,Z/4Z) on the six cosets of <T>. Its characteristic
polynomial is

    x^3 (x-1) (2x+1)^2 / 4.

This regular calculation proves a universal annihilating polynomial,
because every complex representation of the finite group is a summand of
a sum of regular representations. The exact computation is in
`congruence_compression.py`.

In the fourth-root branch there is one additional T=1 object of type A.
For the specified witness, the low six-by-six normalized S block has
eigenvalues `1,1,1,-1/2,0,-1/sqrt(17)`. Its column coupling to the additional
T=1 object is

    (1,1,0,0,-1,-1)/4,

which lies in its nullspace and has norm 1/2. Consequently the remaining
two-by-two compression block is `[[0,1/2],[1/2,c]]` for some c, with
determinant -1/4. Both eigenvalues would have to belong to `1,-1/2,0`.
No pair of these numbers has product -1/4. This excludes this twist branch.

## The eighth-root branch is not excluded here

At level 8 the corresponding regular coset computation has characteristic
polynomial

    x^9 (x-1) (2x+1)^2 (8x^2-1)^6 / 1048576.

Thus the allowed compression eigenvalues are `1,-1/2,0,±sqrt(2)/4`.
The residual low-block spectrum `1,1,1,-1/2,0` is compatible with this.
More specifically, the irreducible level-8 spectrum
`{1,-1,zeta8,zeta8^3,zeta8^5,zeta8^7}` together with three trivial,
one standard two-dimensional level-2, and two sign representations has
exactly the required residual thirteen-dimensional T spectrum.

An independent exact cross-compression calculation also gives no
contradiction: on the nine-dimensional zero eigenspace of PSP in the
regular coset representation, `P S P_{-1} S P` vanishes. On that space
`P S P_i S P` has characteristic polynomial `x^6 (2x-1)^3/8`.
In particular the six-dimensional constituent with no ±i eigenvalues
does not couple its T=1 line to its T=-1 line. The observed rank-one
low-to-C block is therefore compatible with this representation.

No full modular datum, nonnegative Verlinde tensor, algebra object, or
categorification is asserted by these representation-theoretic checks.

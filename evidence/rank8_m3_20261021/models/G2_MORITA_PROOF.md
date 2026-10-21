# The conformal G2 algebra bimodule category: R8_3_458

Let C be the unitary WZW modular category C(G2,3), and A its connected
commutative Q-system from the conformal embedding G2_3 ⊂ E6_1. Such a
conformal embedding gives an actual algebra object, not merely a candidate
dimension vector. Put D = A-bimod(C), with tensor product over A. This is a
unitary fusion category Morita equivalent to C.

For the unitary assertion, see Gui, *Q-systems and extensions of completely
unitary vertex operator algebras*, [arXiv:1908.03484v3](https://arxiv.org/html/1908.03484v3),
Theorem2.21 (a unitary conformal extension supplies a standard Q-system),
Theorem2.28 and §§3.1–3.3 (its unitary bimodule tensor category), and
Corollary3.32 (complete unitarity of positive-level affine VOAs, including G2).
The compact Lie algebra conformal inclusion preserves the invariant positive
Hermitian forms, so it is a unitary extension in the sense of that paper.

Ostrik's Appendix A.4 to Calegari–Morrison–Snyder, *Cyclotomic integers,
fusion categories, and subfactors*, Comm. Math. Phys. 303 (2011), 845–896,
[primary text](https://tqft.net/papers/cyclotomic.pdf), proves that C_A has
the Izumi–Xu near-group rules for C3 with multiplicity3, and that its local
modules are C(E6,1), pointed of rank3. Write d=(3+sqrt(21))/2, so d²=3+3d.
The six dimensions of C are 1,d,d+2,d,d,d+1; they are checked against the
existing full G2_3 tensor by the verifier. Hence dim D = dim C = 21+21d.

There are fully faithful tensor functors j_+,j_- from the two opposite
tensor structures on C_A to D:
equip a right A-module with the left action induced using either braiding.
This is precisely Davydov–Müger–Nikshych–Ostrik, *The Witt group of
non-degenerate braided fusion categories*, [arXiv:1009.2117v2](https://arxiv.org/pdf/1009.2117),
§3.3, equation(16); Definition3.12 and Remark3.13 give the intersection
criterion used here. Opposite structures have the same commutative near-group
fusion rules in this case.
Naturality makes every right-module morphism a bimodule morphism in either
image. The two left actions on a simple right module agree exactly when
it is local. More generally an isomorphism between the two induced
bimodules is a right-module automorphism; for a simple module it is scalar,
so again it exists exactly when the module is local. Therefore the images
share the pointed C3 subcategory and have distinct other simples X and Y.
They satisfy, with G=1+g+g²,

    g³=1, gX=Xg=X, gY=Yg=Y, X²=G+3X, Y²=G+3Y.

In particular X and Y are self-dual of dimension d.

Rigidity gives (XY,XY)=(X²,Y²)=3. Frobenius reciprocity shows that none of
1,g,g²,X,Y occurs in XY. Thus XY is a sum of three distinct new simples.
Their dimensions sum to d²=3(d+1). Their squared dimensions are at least
3(d+1)² by Cauchy–Schwarz. The already known five objects leave exactly
3(d+1)² of the total dimension. Consequently these are all remaining
simples, all have dimension d+1, and YX is their sum as well.

The left action of g on these three objects is either trivial or a 3-cycle.
If trivial, the right action is also trivial by duality. On the span of
Y and the three new objects, left multiplication by X has matrix
[[0,1,1,1],[1,A]], where A is a symmetric nonnegative integral 3x3 matrix
with row sums3. The equation X²=G+3X gives A²+J=3I+3A. A has eigenvalue3
on the all-ones vector; on its orthogonal complement the eigenvalues are
the two conjugate roots of t²-3t-3. Rationality of the trace forces each
root to occur once. Thus tr(A)=6. But its total entry sum is9, so its
off-diagonal sum is3, contradicting symmetry and integrality. The verifier
also exhausts the finitely many possible A. Therefore g acts transitively.

Choose a self-dual member Z_0, which exists because duality permutes a set
of odd cardinality, and label Z_i=g^i Z_0. The right action of g commutes
with the left and is likewise a 3-cycle; it has one of two orientations.
Associativity and the equations above give

    XY=YX=sum_i Z_i,
    XZ_i=Z_iX=Y+sum_j Z_j,
    YZ_i=Z_iY=X+sum_j Z_j.

For example the three products XZ_i coincide since Xg=X; their sum is
X²Y=3Y+3XY, which gives the displayed rule. The other sides follow in
the same way. If the two g-actions had the same orientation, g would
commute with Z_0, hence all products would commute: Z_iZ_j=g^(i+j)Z_0².
This is impossible. Indeed, Morita invariance gives
Z(D) ≅ C ⊠ C^rev. Every simple of C is self-dual (also directly verified
in its tensor), so duality is the identity on K(Z(D)). If K(D) were
commutative, ENO, *On fusion categories*, Lemma8.49 makes the forgetful
map K(Z(D))⊗Q → K(D)⊗Q surjective, forcing duality to be the identity
on K(D). This contradicts g*=g²≠g. This is the same center argument used
in Ostrik's Appendix A.6, with a different modular center.

Thus Z_i g=g^-1 Z_i and all Z_i are self-dual. Frobenius reciprocity
determines the pointed, X and Y coefficients in every Z_iZ_j. Dimension
and translation covariance leave only

    Z_iZ_j = g^(i-j)+X+Y+sum_k c_(k-i+j) Z_k,

where indices are modulo3 and c_0,c_1,c_2 are nonnegative integers summing
to3. There are exactly ten such triples. The independent constructor
checks associativity for every quadruple of basis indices for each triple;
only (1,1,1) passes. This is a complete finite last step, not a search
through selected guesses. Therefore these formulas force the entire
bimodule fusion ring. The resulting 512 structure constants match
R8_3_458 under the recorded unit-preserving basis permutation.

Reproduce with `python -O evidence/rank8_m3_20261021/models/g2_morita.py`.
No assertion is used as an essential check; optimized Python retains all
verification gates. The construction identifies a known conformal-algebra
Morita dual in the new census; no claim that the category itself is new is made.


# Independent audit of the R155 modular reconstruction

1 October 2026. Audited the modular agent's README, exact_enumeration.py, chi_i_completion.py, trivial12.py, reconstruct.py, and reconstruction.json. No mathematical gap was found in the new modular constraints or reconstructed S candidate. This is not a categorification claim.

## Normalization and Galois fields

The normalization is correct: `sqrt(dim B)=12d` and normalized Gauss sum `tau+/sqrt(dim B)=z^21=z^-3`. Thus `s=S_B/(12d)` and `t=zT_B` satisfy `s^2=C` and `(st)^3=C`. Since t has order 24, Dong-Lin-Ng Theorem II gives level 24 and entries in Q(z). Their equations (4.3)-(4.6) and Remark 4.5 identify `G_a=sigma_a(s)s^-1` with the representation of `diag(a,a^-1)`. Every unit mod24 is self-inverse, so this is the central element aI. The Galois matrices are signed rational permutation matrices.

Primary source independently opened: https://arxiv.org/pdf/1201.6644, especially Theorem II and Section 4 (retrieval `turn451view0`, `turn451view1`).

The character eigenspaces admit rational bases. On a rational chi eigenspace the relation `sigma(s)=G_sigma s` implies entrywise `sigma(s_block)=chi(sigma)s_block`. Because Q(z24)=Q(i,sqrt2,sqrt3) has Galois group C2^3, the chi_sqrt3 eigenspace in the coefficient field is exactly sqrt3 times Q. This is stronger than membership in Q(sqrt3), and the stronger assertion used by the argument is valid.

For the M rows, `(1+2d)/(12d)=sqrt2/8` and the character value on X is `+/- i sqrt2`. Therefore their overall signed factor is chi_sqrt2 and their pair-permutation character is chi_i chi_sqrt2. On the unit/A and f/fA pairs, conjugating sqrt2 acts as negative transposition, giving a rational difference and a chi_sqrt2 sum. The pure kd normalized dimensions are rational, hence their Galois signs are positive. The fermion's rational eigenvalues ensure Galois matrices commute with its fusion permutation, justifying the tied pair characters at twists differing by a minus sign.

## The two-dimensional obstruction

The equal-norm rational pair-difference basis makes the block symmetric. Its t-eigenvalues are `t1=i,t2=iw`. Write s=[[a,b],[b,c]]. The claim b != 0 can be obtained without invoking an irreducibility classification: if b=0, s^2=I forces a,c in {+1,-1}, but the first diagonal entry of `(st)^3=I` would require `(a i)^3=1`, impossible.

Consequently s^2=I gives c=-a. The off-diagonal modular equation gives `a=1/(t1 t2 (t1-t2))=1/sqrt3`; the square equation gives b^2=2/3. Since b belongs to sqrt3 Q, `(b/sqrt3)^2=2/9` would be a rational square, a contradiction. All signs and normalizations check. The selfdual odd-2d branch is excluded and the remaining duality has 10 fixed labels in B, 20 in Semion x B.

## Enumeration and completion

The local character-table verifier is exact: it reconstructs finite groups and class algebras, checks all class-algebra characters, degrees, character orthogonality, T spectra, and central signs. Completeness follows from the number of characters and degree-square sum. The tensor-product enumeration is therefore not relying on numerically guessed characters. I replayed it independently in this directory: 718 T-spectrum decompositions, eight after Galois constraints, four after the known low-row trace. The apparent greedy pair-character selection is harmless: after subtraction of the fixed contributions, the total residual at each relevant t exponent is exactly one, so two admissible character choices cannot coexist.

I replayed the six-dimensional completion and the rational 12-dimensional block. The latter's matrix H is `V^T s V` in a rational orthogonal basis with Gram matrix N=diag(norms), not the representation matrix itself. The code correctly uses `H N^-1 H=N` and `H N^-1 t H=t^-1 H t^-1`. Reconstruction correctly divides each block entry by both basis norms. The original exact Gröbner calculation reproduced nine linear equations. I also replayed the final replacement: ordinary row reduction over Q, temporarily treating quadratic monomials as separate columns, gives the same nine linear consequences. Substitution satisfies every original equation. Thus uniqueness now needs only rational linear algebra, not a Gröbner-basis computation.

## Full-data verification

`independent_full_s_audit.py` creates Q(z24) afresh, imports the coefficient lists and integer fusion tensor, and checks:

* all integer associativity equations;
* every exact fusion eigenvector identity;
* direct Verlinde sums for every coefficient of the four fusion matrices N_2, N_8, N_12, N_23;
* nonnegativity, integer coefficients, tensor unit and duality;
* the exact positive vacuum normalization and normalized Gauss sum;
* the scalar arithmetic in the excluded two-dimensional branch.

Everything passes. The largest fusion coefficient is nine. Runtime was approximately 2.2 seconds. The direct sums use the dual label in the third S factor, and the tensor unit is frozen label 1, not label 0.

The replayed exact jobs and independent audit receipts are saved alongside this note. The verified conclusion is a unique full modular S candidate compatible with the stated categorical prerequisites, with a nonnegative integral associative Verlinde ring. Associators and a categorical realization remain unproved; matching these data to a named category would require a separate identification argument.

## Forgetful-ring compatibility and portable replay

The separate `forgetful_ring_audit.py` checks the frozen 26-by-6 multiplicity matrix against every product in the reconstructed fusion tensor. All 26 squared product identities (4,056 integer coefficients) pass exactly, and the unit is preserved. This establishes compatibility of a based-ring homomorphism; it does not construct its tensor structure.

The independently written scripts accept explicit artifact paths:

```sh
python independent_full_s_audit.py --reconstruction /path/to/reconstruction.json
python forgetful_ring_audit.py --package /path/to/Rank6_Categorification_M9 --reconstruction /path/to/reconstruction.json
```

Each writes its receipt next to itself. The copied reconstruction-stage replay scripts retain the original agent's source layout and are supplementary; the two independent scripts above have no fixed workspace path.

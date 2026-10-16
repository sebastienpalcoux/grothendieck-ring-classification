# Independent categorical audit: twisted V4 descent for R7_4_2591

Reviewed `work/unified/two_dimension/R2591_TWISTED_V4_REDUCTION.md`.
The argument proves a general-to-Galois-pseudo-unitary reduction, and does
not decide whether the ring is categorifiable.

The key multiplicity-space lemma is correct. Choose identifications
`l_U(g):gU→U`, `l_W(g):gW→W`, and similarly right identifications. On
`Hom(W,U⊗V)`, left translation is induced by left translation of U and
inverse left translation of W. Its projective class is therefore
`alpha_U−alpha_W`. The right action uses V and W and has class
`beta_V−beta_W`, up to taking the inverse class. The two outer actions on
U⊗V commute by the associativity coherence theorem; their defect after
identifying W is precisely the mixed commutator of W, up to transpose and
inverse. All these ambiguities leave the alternating-matrix ranks
unchanged over F2. The claimed rank bound follows because an irreducible
projective representation for an alternating form of rank 2r has dimension
2^r, which must divide the nonzero multiplicity-space dimension n.

For the TY simple X, the standard TY associator has trivial left and right
projective classes, with mixed form the nondegenerate bicharacter chi.
The multiplicity-two X channel in Y² therefore gives the displayed
4-by-4 alternating matrix. If either diagonal block is zero, invertibility
of chi forces rank four. If both are J, the Schur complement vanishes
because chi^T J chi=det(chi)J=J. Thus both projective classes of Y are
nontrivial; duality gives the same assertion for Z.

The multiplicity-two Z channel in XY then gives diagonal blocks J,0.
Its rank is 2+rank(B^T J B), so the mixed block has rank at most one.
The twisted full regular algebra changes both diagonal blocks and leaves
the mixed block unchanged. The simple-bimodule counts and underlying-object
multiplicities consequently agree with the proof: four invertibles over X;
and, over each of Y and Z, either sixteen objects of dimension t/2 (ruled
out by algebraic integrality) or four objects of dimension t. The pointed
support adds four invertibles. This accounts for the entire dual category.

The final two-dimension Galois reduction is valid under Morita invariance
of categorical global dimension and FP dimension. It does not presume a
unitary or pivotal structure on the original category. The inverse algebra
and the possible order-eight groups do not trivialize the pointed
associator, so the stated limitation on further GH classification is
necessary and correctly retained.

**Verdict: no categorical gap found.** Finite source and rank calculations
are delegated to the accompanying source-bound verifier and require their
own replay; this note records the independent theoretical audit.

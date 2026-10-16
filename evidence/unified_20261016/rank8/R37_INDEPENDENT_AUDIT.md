# Independent audit of the R8_2_37 construction

Verdict: PASS, as a unitary existence theorem. No claim about R8_2_170 is covered by this audit.

I read `work/unified/two_d_two/R37_CONSTRUCTION.md`, inspected the complete source-tensor verifier, replayed it, and independently checked the source statements in Grossman–Izumi–Snyder, arXiv:2201.11901, and Grossman, arXiv:1612.07185, against the available full paper texts.

Theorem 4.1 of the first source includes the known C4 Haagerup category P1, odd p=1, and z=0 or 2. Lemma 3.2 supplies character eigenvectors u,v; Lemma 3.6(2), equation (3.10), and equation (3.18) give alpha_2(u)=-u and alpha_2(v)=-v. The crossed-product definition of Q1 and its extended generators is explicitly stated in the second source, Section 4.1, printed page 38.

The crucial categorical verification is on the implementing involution lambda. Since both u and v anticommute with lambda, the two proposed endomorphism equalities hold there as well as on M. Therefore b^2 has sector g, not the identity. This avoids any unproved coherent order-two autoequivalence assumption.

I also checked that the finite list of eight sectors is closed and has no repetitions. The four invertibles have order-four generator a, because a^2=g is nontrivial. Frobenius reciprocity and the fact that rr* has only the identity as an invertible summand separate all four noninvertibles. All eight proposed sectors are irreducible, and the closed finite list inherits associativity and unitarity from the factor endomorphism category.

The multiplication in the note follows from ra=a^(-1)r and r^2=1+2r+2a^2r. The replay compares all 512 source constants under the explicit bijection (0,1,7,2,5,3,6,4), verifies the ledger tensor hash, and checks all 4,096 associativity coefficients. The tensor hash is

    1cfa463b5ec59daa44cc51752a6a58ea5378684a46ab7ee72147ab69153d5f6a

The proof constructs the associativity constraints by embedding the category in End_0(P); the finite tensor check correctly serves only to identify that constructed category with the census entry.

No correction to the R37 construction was needed.

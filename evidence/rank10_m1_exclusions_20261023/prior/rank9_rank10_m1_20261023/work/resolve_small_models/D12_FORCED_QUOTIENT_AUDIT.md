# Independent proof of the forced dimension-twelve quotient

This note audits the missing input to the dimension-24 characteristic-boson argument. It is a categorical argument, not a failure of a bounded model search.

Let B have fusion rules

- G(B)=V4, with every invertible fixing m and n;
- d(m)=2, d(n)=4;
- m^2=sum G(B), mn=nm=2n, n^2=sum G(B)+2m+2n.

The adjoint subcategory is all of B. Solvability in dimension24 therefore implies that the final step in a prime-cyclic solvable sequence is an equivariantization. Its prime is2 because Rep(C_p) embeds in B and G(B)=V4. Write B=E^{C2}; let beta denote the induced involution on simple classes of E.

For the nontrivial sign g, the tensor permutation on B has two pairs among the four invertibles and fixes m,n. The C2 equivariantization orbit formula gives

    E: 1^4,2^2,

with beta fixing two invertibles and interchanging the other two, and beta interchanging the two dimension-two simples X,Y. In particular the group G=G(E) has order4 and is abelian.

## The invertibles must fix both X and Y

Suppose instead that the left action of G on {X,Y} is transitive. Its stabilizer H has order2. Left and right actions agree: the duality permutation on the two-element set conjugates left multiplication by g^{-1} into right multiplication by g, and every permutation of this set commutes with every other permutation. The image of G has exponent2, so inversion does not change that permutation. Consequently conjugation by any g fixes X and Y. It also fixes every invertible because G is abelian.

Choose g with Y=gX. The invertible constituents of XX* are exactly H, each once. Dimension gives

    XX*=sum_{h in H}h + Z,

for exactly one Z in {X,Y}. Conjugation invariance gives

    YY*=g(XX*)g^{-1}=XX*.

On the other hand beta(X)=Y, so beta(XX*)=YY*=XX*. This is impossible because beta interchanges X and Y and the noninvertible part of XX* is precisely one of them. Hence every invertible fixes X and Y on both sides.

## The remaining fusion rules are forced

Now XX*=YY*=sum G. If both X and Y were self-dual, then XY could have no invertible constituent and, by Frobenius reciprocity, neither X nor Y could occur in XY: the relevant multiplicities are constituents of XX*=YY*=sum G. This contradicts d(XY)=4. Thus X*=Y, and

    XY=YX=sum G.

The product X^2 has no invertible constituent. Frobenius reciprocity gives N_XX^X=N_(X*X)^X=0. Therefore X^2=2Y, and similarly Y^2=2X. These are the R_{3,G} rules.

## The group G cannot be C4

The category is faithfully C3-graded with neutral pointed category Vec(G,omega), and each nonneutral component has rank1 as a left module category. A rank1 module category over Vec(G,omega) is equivalent to a fiber functor on that pointed category; the module associativity equation trivializes omega. Thus the neutral category is Vec(G).

If G=C4, then

    BrPic(Vec(C4))=O(C4⊕C4*,q),   q(x,y)=xy mod4.

This group has no element of order3. One elementary proof is reduction modulo2: the image lies in the two-element orthogonal group of q(x,y)=xy over F2, while the kernel consists of matrices I+2M and has exponent2. Thus an element whose order divides3 is the identity. Equivalently the exact matrix group consists of the two diagonal matrices diag(a,a^{-1}) and two anti-diagonal matrices with off-diagonal entries b,b^{-1}, for a,b in {1,3}.

A homomorphism C3→BrPic(Vec(C4)) is consequently trivial. Its homogeneous components would all be regular bimodule categories, of rank4. This contradicts the rank1 nonneutral components. Hence G=V4.

We have therefore derived R_{3,V4} for every possible E, and the complete Jordan–Larson classification (Theorem1.4, Lemma2.6, Proposition3.1 of arXiv:0812.1603) applies. No extra dimension-twelve fusion ring or associator family is omitted.

## Audit of the subsequent center argument

The proof in work/audit_new_models/RANK6_CENTRAL_BOSON.md then applies to every B above. Its central steps are sound: E⋊C2 has universal group S3; a central invertible has neutral degree; its restriction to Z(Vec(V4)) is triality-fixed; all nonzero triality-fixed vectors are anisotropic; the kernel consists of the two grading characters. Thus its center has exactly one nontrivial invertible boson. Braided Morita equivalence preserves the canonical positive ribbon structure. The characteristic boson in B is fixed by any further action, and its equivariantization supplies central Rep(V4) in the dimension48 category. The fully faithful forgetful embedding follows because the original central Rep(C2) has distinct underlying simple objects in B. This permits the independently classified near-group sign to be chosen.

This audit does not itself replace the independent near-group action classification or its input tensor checks.

# Connected etale algebra supports in the reconstructed rank-26 ring

This is a categorical necessary theorem conditional on the new reconstructed
fusion rules in `../r155_modular/reconstruction.json`. It is not a proof that
those modular data have a categorical realization. The frozen release is
unchanged.

Use the frozen numbering, with unit 1, fermion 0, A=23 of dimension b-1,
and L=25 of dimension b, where b=18+12 sqrt(2). The twist-one simples are
exactly

    1, 2, 5, 23, 25.

Objects 2 and 5 are a dual pair, of dimension d=4+3 sqrt(2). The full
reconstructed fusion rules give

    2 tensor 2 = 9+10+16+19,
    2 tensor 5 = 1+8+11+22.

Thus the first product has no twist-one constituent, and the second has
only the tensor unit among the twist-one constituents.

**Theorem.** In any positive ribbon categorification of these data, the
underlying object of every connected etale algebra is one of

    1,       1+A,       1+A+L.

**Proof.** Connected etale algebras in a pseudo-unitary modular category
are twist-free and have a nondegenerate Frobenius pairing. Suppose such an
algebra E contains object 2. It then contains its dual 5, with equal
multiplicity, and multiplication from the 2 and 5 isotypic components to
the unit has a nondegenerate pairing on the multiplicity spaces.

Multiplication from 2 tensor 2 is zero, since that tensor product has no
twist-one summand at all. Multiplication from 2 tensor 5 lands entirely
in the unit, since no other allowed algebra summand occurs in that
product. Choose copies of the second 2 and of 5 on which this pairing is
nonzero. The associativity equation on 2 tensor 2 tensor 5 has zero on
the side which first multiplies 2 tensor 2. The other side first contracts
the second 2 with 5 to the unit and then multiplies by the first 2; it is
nonzero. This is impossible. The same argument excludes object 5.

We are left with E=1+sA+tL, s,t nonnegative integers. Its dimension is
1-s+(s+t)b. The local-module dimension formula implies

    FPdim(E) <= sqrt(FPdim(B)) = 2 sqrt(2) b.

If s+t is at least three, the smallest possible dimension is 3b-2,
which exceeds 2 sqrt(2)b by exactly four. Hence s+t <= 2.

Besides the three displayed candidates, the only possibilities have
dimensions b+1, 2b-1, and 2b+1. Their field norms in Q(sqrt(2)) are
respectively 73,73,217. On the other hand

    Norm(FPdim(B)) = Norm(8b^2) = 82944 = 2^10 3^4.

For a connected etale algebra, FPdim(B)/FPdim(E)^2 is the global dimension
of a fusion category, hence an algebraic integer. Taking norms would
require the square of 73 or 217 to divide 82944, which is false. This
excludes the three other possibilities. QED.

When B comes from a categorification of R155, the two nontrivial listed
objects do carry canonical etale algebra structures, as explained in
`canonical_condensation_note.md`. The theorem does not prove uniqueness
of their algebra structures. The local categories of these canonical
structures are respectively ToricCode tensor Semion^rev and Semion^rev.

## Fusion subcategories and restriction functor

The exact closure computation finds precisely four fusion subcategories:

1. Vec, support {1}.
2. sVec, support {0,1}.
3. The rank-16 fermion centralizer, support
   {0,1,2,3,5,6,8,9,10,11,16,17,18,19,22,23}.
4. B itself.

Every noninvertible even simple generates the rank-16 category, and every
odd simple generates B. There is no hidden smaller nonpointed fusion
subcategory to which a rank-two or near-group classification could apply.

The same exact checker verifies all 26^2=676 restriction products for
the frozen functor matrix W:B->C. Every reconstructed product satisfies

    W(i) W(j) = sum_k N_(i,j)^k W(k)

in the original R155 fusion ring. Thus the full reconstructed fusion ring
is consistent with the original restriction functor, beyond the previously
known low multiplication matrices.

Run `python -O check_full_fusion_categorical.py`; its receipt is
`full_fusion_categorical_receipt.json`. The computation takes under one
second, uses integer arithmetic, and neither changes nor regenerates the
modular reconstruction.

The categorical ingredients are the standard Frobenius pairing for a
connected separable algebra, twist-freeness of connected etale algebras in
a pseudo-unitary braided fusion category, and the local-module dimension
formula. See Davydov--Muger--Nikshych--Ostrik, *The Witt group of
non-degenerate braided fusion categories*, arXiv:1009.2117, Section 3.

# Independent audit: the weighted third-indicator obstruction for R630

Auditor: `rank6_center`, 2026-10-16. Status: **PASS** for the categorical
argument and its independently checked source cube multiplicities.

The general-complex reduction is separately fully audited and replayed
in `work/unified/simple_global/HI6_PAIR_GALOIS_PU_INDEPENDENT_AUDIT.md`.
It proves that every hypothetical categorification has a positive
spherical Galois conjugate with the same source tensor. It does not
assume unitarity or identify this category with HI(C6).

Write q=sqrt10, D=120+36q, and source dimension coefficients

    a=(1,1,2,3,3,2,4,4), b=(0,0,1,1,1,1,1,1).

The linear functional ell=3a-10b has values

    (3,3,-4,-1,-1,-4,2,2).

For a central restriction row v with dimension z=A+Bq, ell(v) vanishes
exactly when z/D is rational. The independently audited saturated
quadratic dimension block has conductor40. Therefore every high row
with ell(v) nonzero has twist of order dividing40. Every constituent of
I(1) has twist one. The primitive-twist residue refinement is not needed.

Take a cyclotomic field containing all center twists and dimensions,
and, if necessary, enlarge it to contain zeta40. There exists an
automorphism tau whose exponent is congruent to3 modulo40: it is already
coprime to2 and5, and at each other prime dividing the full conductor
choose a nonzero residue and use the Chinese remainder theorem. In
particular a prime3 dividing the full conductor causes no problem; the
chosen exponent need not equal the integer3. The quadratic character
chi40(3)=+1, so tau fixes q and all central dimensions.

The weighted first center trace is

    sum_Z ell(v_Z) dim(Z) theta_Z = D ell(unit)=3D.

Apply tau. On high rows with rational dimension ratio the summand is
zero. On all other high rows tau(theta)=theta cubed, since their twists
have order dividing40. On low I(1) rows the twist is one. Thus the
transformed identity is precisely the weighted third center trace, with
the same right side 3D. The center indicator formula gives

    sum_{i>0} ell_i nu3(X_i)=0.

I independently loaded the original multiplicity-two census, used its
prescribed flattened lexicographic ordering, and checked the source
R630 tensor directly. Its self-duality makes
dim Hom(1,X_i cubed)=N_ii^i, and those eight values are

    (1,0,0,1,1,1,0,0).

The balance consequently becomes

    nu3(X3)+nu3(X4)+4 nu3(X5)=0.

Each displayed third indicator is the trace of the pivotal order-three
rotation on a one-dimensional vector space. It is therefore a cube root
of unity and has absolute value one. The last term has absolute value
four, while the sum of the first two has absolute value at most two.
This is impossible.

No claim that a self-dual object's higher indicator is real is used or
needed. Nor is a global center exponent bound, finite row enumeration,
linear-programming certificate, or associator search used. The only
twist-order restriction required is the theoretically saturated
conductor-forty restriction on rows not annihilated by ell.

## Final packet replay

I subsequently read the completed `SATURATED_GALOIS_INDICATOR_LEMMA.md`,
`R630_WEIGHTED_GALOIS_INDICATOR_PROOF.md`, and the complete source-bound
`verify_r630_weighted_indicator.py`. The abstract lemma correctly applies
the Galois automorphism to the weighted trace coefficients in K, uses
the one-dimensional rational kernel of ell, and cancels D after the
indicator formula. The proof of conductor-forty saturation correctly
allows both prime-power factors8 and5 and needs no residue refinement.

The independent optimized replay passed, including invocation of the
published structural sphericality gate. Its receipt is
`r630_rank6_independent_optimized.json`. It binds tensor SHA256
`4bf43a0204695223442fef2735e46289cded33126a6598118091a280cada93cb`,
reproduces the 27-variable/157-equation/195-node signed gate, and checks
the exact three weighted cubic invariant spaces and the inequality4>2.

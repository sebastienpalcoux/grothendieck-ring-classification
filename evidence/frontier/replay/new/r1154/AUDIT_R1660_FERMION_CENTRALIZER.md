# Independent audit: R1660 fermion centralizer

29 October 2026. Reviewed the candidate argument in
`../r1660_941/REPORT.md`, Section 1, with the rank-eight simplification
in Section 2. **Verdict: valid as a necessary theorem in the stated
positive representative, conditional on the explicitly inherited complete
central phase and integral-center theorems. It is not a ring exclusion.**

## Critical premise checked

The proper source Ising subcategory means that absence of a central simple
of dimension sqrt(2) alone would not justify the dominant-image step. One
must exclude *every* nonpointed central simple whose entire forgetful support
lies in {1,g,sigma}.

The accepted phase theorem does give this stronger statement. It supplies
eight central simples, each with restriction (0,0,2,2,1,3), in the four
spin-phase dual pairs. I independently computed the induction Gram entry
H_sigma,sigma=8 from the source tensor. Each displayed column contributes
one to that entry. Their eight contributions exhaust it, so no other
central simple can contain sigma. Every one of those eight already contains
X,gX,T. All remaining objects supported inside {1,g,sigma} are therefore
supported on {1,g}, and the inherited integral-center theorem leaves just
the unit and the fermion.

The small ring computation independently gives these single-generator
fusion closures:

    <g>={1,g},      <sigma>={1,g,sigma},
    <X>=<gX>=<T>=C.

Thus each nonpointed central fusion subcategory contains a simple whose
forgetful image generates C; its forgetful functor is dominant.

## Strictness, splitting, and s-simplicity

The dimension bound is actually strict: equality would make the restricted
forgetful functor a tensor equivalence. It would then have a simple preimage
of the source sigma, forcing a central simple of dimension sqrt(2), which
was just excluded. This provides an independent, shorter justification than
the candidate's correct Ising-braiding argument.

If E split as M tensor sVec, nondegeneracy of M would split the entire
center as M tensor K with FPdim(K)=4. K contains the fermion. Since the
center has no other integral simples, K has exactly two invertible simples;
the remaining squared-dimension mass is two. Every noninvertible simple has
FP dimension greater than one, so the remaining mass must be one simple of
dimension sqrt(2), contradiction.

For a proper nonpointed H in E containing sVec, the centralizer identity
would give FPdim(H) FPdim(H')=D^2. Either H'=sVec, which forces H=E, or both
H,H' are nonpointed and have dimensions strictly greater than D, impossible.
For H omitting the fermion, its join with sVec must be E. Its symmetric
Müger center is integral, hence lies in sVec; the trivial intersection makes
H nondegenerate, forcing the excluded split E=H tensor sVec. This verifies
the assertion that the only fusion subcategories of E are Vec, sVec and E.

The same four-dimensional-complement argument correctly simplifies R941's
previous nonsplitting proof. There its nonpointed source dimensions already
exceed sqrt(2), so no central simple can have that dimension.

## Scope and dependencies

The new proof does not construct the algebra 1+X, assert that R1660 and R941
are Morita equivalent, or eliminate either ring. It uses the following
inherited categorical premises, not merely numeric evidence:

1. The established spherical/Galois reduction to the chosen positive form.
2. The unique central fermion and exact integral-center classification.
3. Existence and completeness of the eight spin columns in the phase theorem.

The Gram calculation makes the needed support completeness transparent once
item 3 is supplied; it cannot prove those central objects exist on its own.
The report correctly works in the positive representative rather than
asserting pseudo-unitarity of an arbitrary original complex category.
Transport of these structural properties back to a particular original
category requires that the inherited gate actually identifies its own
Galois/Morita transport, not merely an unrelated positive existence witness.
No such additional generality is needed for the stated necessary condition.

This audit covers the centralizer theorem. It does not purport to be a new
independent audit of all earlier phase proofs or the separate cyclic-algebra
coefficient argument in Section 3.

## Addendum: specified quantum construction routes

I also reviewed `../r1660_941/quantum_routes.py` and the dimension-12
construction obstructions, then replayed the checker in normal and
optimized Python. Both passed.

The basis (1,r,s,rs,c,cr,cs,crs), where r=sqrt(2), s=sqrt(3), and
c=2cos(pi/24), is independent: Q(c) is the real cyclotomic field of
conductor 48 and degree eight, and c^2 belongs to the degree-four field
Q(r,s). The displayed multiplication c^2=2+(r+rs)/2 is correct. The exact
recurrence gives the complete 23 and 11 dimensions of SU(2)_22 and
SU(2)_10. It yields 69 dimensions in SU(2)_22 times Ad(E6), and 5819
in SU(2)_22 squared times SU(2)_10. The nonnegative coordinate cone
and the lists of four/eight rational-dimensional simples verify that
any dimension-12 algebra would be pointed-supported.

For a connected separable algebra A, its regular right module is simple;
so is gA for invertible g. The adjunction
Hom_A(gA,A)=Hom(g,A) bounds each invertible's multiplicity by one. Thus
the respective upper bounds four/eight contradict dimension twelve.
The two dimension identities in the report are checked exactly.

One terminology correction was requested: Ad(E6) is not assumed braided,
so a fusion category of full modules in the first product needs a central
commutative algebra, not an unspecified étale algebra in a braided ambient.
The underlying connected-separable-algebra dimension obstruction is valid
without a braiding and survives this correction. No claim about arbitrary
quantum groups, intermediate operations, or ordinary noncentral Morita
bimodules follows.

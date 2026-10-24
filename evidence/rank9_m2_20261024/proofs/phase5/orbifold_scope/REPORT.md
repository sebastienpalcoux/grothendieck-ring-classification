# Orbifold-scope research: proved construction, no census promotion

**The algebraic extension is proved for the explicit Radchenko–Wheeler
Leavitt realizations. This route currently resolves no additional rank-nine
case.** Independent audit: **PASS**, documented in
`../audit_orbifold_scope/REPORT.md`, with an independent exact verifier.

`ALGEBRAIC_ORBIFOLD.md` proves the isotropic-orbifold fusion rules of Izumi
Theorem 12.5 without assuming a unitary source. The proof constructs the
ordinary algebraic crossed product R=L rtimes H, extends the near-group
endomorphisms, checks the fusion decomposition on its additional generators,
computes every basic intertwiner space, and uses additive Karoubi completion
to obtain a finite semisimple rigid category. Finite Fourier projections
give the complete multiplicities. This is an existence construction for
the specific RW categories; it does not parameterize arbitrary original
spherical categories. Sphericality follows separately from the established
general theorem for quadratic categories.

For RW's matrix `[[1,4],[8,33]]`, the source group is C8 x C4. Its isotropic
order-four subgroup gives an actual rank-twelve model with invertibles
C4 x C2 and four non-self-dual objects of dimension 4+3 sqrt(2), with uniform
noninvertible product coefficient two. These invertibles differ from the
D8 group required in the outstanding rank-nine Morita-dual candidates.
Thus neither R9_2_1975 nor R9_2_137, R9_2_1607, or R9_2_1976 is promoted
by this construction.

The suggested canonical object A=1+sum sigma_eta does not yet supply a
different model. In Izumi's unitary subfactor construction, Theorem 12.3
and Remark 12.4 identify the corresponding subfactor as self-dual. The
algebraic extension proved here does not extend that Q-system theorem or
provide a separable multiplication on A. The peer's conditional induction
Gram calculation has rank twelve, and is not a construction of an algebra
or a rank-nine category. Other nonintegral algebras and other metric inputs
remain possible; their absence has not been proved.

Run `python -S verify_orbifold.py` to reproduce `orbifold_verification.json`.
It uses only Python's standard library and checks the exact RW metric
formulas, isotropy, orthogonal complement, all averaging-projection ranks,
the full rank-twelve fusion tensor, duality, dimension identities and
20,736 associativity coefficients. Its receipt explicitly separates these
finite checks from the cited quantum-dilogarithm and categorical existence
dependencies. All checks pass. Source PDFs and extracted text are retained
in this directory; no repositories or earlier-phase evidence were edited.

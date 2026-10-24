# What remains after the five accepted resolutions

The four unresolved IDs are R9_2_137, R9_2_1607, R9_2_1975 and
R9_2_1976. They all have dimensions `(1^4,2,(4+3sqrt(2))^4)`.
No further rank-nine classification follows from the auxiliary results below.

## Three commutative sources: two common necessary Morita types

For 137,1607,1976 the two different stabilizers of the nonintegral objects
force the integral TY(V4) subcategory's bicharacter to be nonalternating.
The unique isotropic involution gives an algebra whose Morita dual has
eight D8 invertibles and four dimension-(4+3sqrt(2)) objects. The complete
finite reduction initially leaves three common based-ring types.

A further categorical obstruction removes the type with nontrivial
left-right quotient action. The pointed associator is forced to have class
two on the rotation C4. A relation rX=Xs with r of order four and s of
order two would make this nonzero class vanish on a cyclic stabilizer,
which is impossible. The conclusion uses the TY-origin associator and
does not exclude arbitrary categorifications of that abstract based ring.

The remaining two types have identity quotient action and uniform
noninvertible multiplicity two; their duality shift is either zero or a
specified reflection coset. The source rings remain unresolved because
neither compatible associators nor a categorical contradiction have been
established. Constructing an arbitrary categorification of a dual based
ring would also require the appropriate inverse module to recover a source.

Proofs: quadratic_comm/REPORT.md and ty_module_subtask/ within that folder.
Independent audit: audit_quadratic_reduction/REPORT.md, PASS.
Portable exact replay: quadratic_comm/verify_packaged_records.py.

## An algebraic construction that does not reach these targets

The isotropic orbifold construction was proved for the explicit algebraic
Radchenko-Wheeler near-group realizations, without importing unitarity.
The proof uses a crossed-product algebra, complete intertwiner spaces,
finite semisimplicity, rigidity and exact Fourier projectors. It is a
construction for those sources, not a parameterization of all spherical
near-group categories.

It produces an auxiliary rank-twelve category with invertibles C4 x C2
and four non-self-dual objects of dimension 4+3sqrt(2). It has the desired
dimension scale, but the invertible group differs from the required D8.
Pointed-only Morita changes cannot overcome the relevant center obstruction.
The canonical object 1+sum X_i, even if equipped with a suitable separable
algebra structure, has twelve simple modules and cannot give a rank-nine
dual by the rank inequality. Its algebra structure has not been assumed
or inferred from its based-ring decomposition.

Proof: orbifold_scope/ALGEBRAIC_ORBIFOLD.md.
Independent audit: audit_orbifold_scope/REPORT.md, PASS.
Additional construction limits and R9_2_1975 attempts are recorded in
quadratic_noncomm/REPORT.md. These obstructions to particular routes are
not nonexistence theorems for the four remaining source rings.

Run the package's `python verify.py --frontier` for the portable exact
auxiliary replays as well as all accepted rank-nine classifications.

# The model needs only ground-state branching

The full affine branching table in `CONFORMAL_MODEL.md` can be replaced by
the following short argument. It supplies an independent theoretical
check on every branching multiplicity used in the model.

Use the conformal embedding sl4 at level6 into sl10 at level1 induced by
the ten-dimensional representation Sym²(C⁴), or its dual to match the
orientation of the published table. The two Sugawara conformal vectors
agree. The lowest conformal weight of the jth level-one sl10 module is

    h_j = j(10−j)/20,    0≤j≤9.

If an affine sl4 module of highest weight λ occurs in that module, its
conformal weight must be h_λ=h_j+n for a nonnegative integer n. At n=0,
its multiplicity is the ordinary finite-dimensional branching
multiplicity in the ground state Λʲ(C¹⁰).

For the handful of sl4 weights needed here, the inverse-Cartan formula
h_λ=(λ,λ+2ρ)/20 gives

| λ | h_λ |
|---|---|
|000|0|
|101|2/5|
|020|3/5|
|010|1/4|
|111|3/4|
|200,002|9/20|
|030|21/20|

The residues of the h_j are 0,9/20,4/5,1/20,1/5,1/4. Thus neither 101 nor
020 occurs in any of the ten branching objects. The vacuum 000 occurs
once only for j=0. This proves that the ten translates τ_j F(010) are
simple and distinct.

For the cube of v=(010), the possible constituents are

    3(010)+2(111)+(030)+(200)+(002).

The weight111 cannot occur in any branching object, by its conformal
residue. The only possible j for010 is j=5, but h_5=5/4>1/4, so010 cannot
occur either. The weights200,002 can occur only at j=1,9, and at ground
level. Their multiplicities are one, because the finite-dimensional
sl10 vector restricts as Sym²(C⁴), or its dual.

The weight030 can occur only at j=3,7, again at ground level. The ordinary
plethysm identity

    Λ³(Sym² V) = S_(4,1,1)(V) ⊕ S_(3,3)(V),   dim V=4,

gives SU(4) weights301 and030; dualizing gives103 and030. The
self-dual030 summand has multiplicity one in both cases. Consequently
the branching intersection of v³ is precisely one copy in each of
j=1,3,7,9, and zero elsewhere, exactly as required.

`verify_minimal_branching.py` verifies all conformal weights over rational
numbers and verifies the plethysm identity as a complete equality of
four-variable weight characters. It enumerates the120 exterior-cube
weights and the semistandard-tableau characters of the two Schur
functors, rather than assuming their dimensions imply the identity.

The only affine input retained is existence of the stated conformal
embedding and agreement of its conformal vectors. No assertion that a
numerical modular invariant is automatically realized is involved.

# R7_4_2053 reduces to R8_1_18 over the complex numbers

**Status: proved general-complex exclusion, using the separately proved R18 endpoint.** Every complex fusion-category categorification of R7_4_2053 would yield a complex categorification of R8_1_18. The general exclusion of R8_1_18 is proved in [R18_STS_MOMENT_PROOF.md](../rank8/R18_STS_MOMENT_PROOF.md). Consequently R7_4_2053 is excluded over the complex numbers. The main body isolates and verifies the exact structural implication.

## Existing categorical inputs and their scope

The already audited `FOUR_RANK7_DIHEDRAL_REDUCTION.md` and its exact source verifier prove a general-complex Morita reduction, without an assumed pivotal structure. The source has invertibles C4, a dimension-two simple X, and two self-dual simples Y,Z of dimension 2t, where t=2+sqrt(5). The involution h fixes X,Y,Z on both sides. The multiplicity-one relations XY=Y+Z and [YY*:X]=1 force all fixed-object H-by-H projective blocks to split. Thus the actual algebra 1+h has a Morita dual E with eight invertibles and eight freely permuted noninvertibles of dimension t.

The inverse algebra is supported on an order-two subgroup L. Its pointed Morita dual is the original integral TY(C4) subcategory, so L is nonnormal and the invertible group of E is D8. Absence of dimension-t objects on the inverse side forces the mixed automorphism to exchange reflection conjugacy classes. Complete associative coefficient enumeration leaves four normal forms after the exceptional codegree-field candidate is excluded. This last exclusion and the later indicator argument use the published two-dimension Galois pseudo-unitarity theorem. That theorem allows replacing the actual category and its existing algebra by a pseudo-unitary Galois conjugate; it does not assume the original categorification unitary or spherical.

In generators D8=<r,s | r^4=s^2=1, srs=r^-1>, the normal forms are

    rho r=r^-1 rho,   rho s=rs rho,
    rho^2=a+N rho,
    a in {1,r^2},
    N=sum rotations or sum reflections.

The inverse reflection double orbits are H g phi(H), H=<s>, each of size four with trivial stabilizer. Their dual supports are a^-1 phi(g^-1). They are individually preserved for a=1 and exchanged for a=r^2. Since the source Y and Z are self-dual, **a=1 is forced**. This conclusion concerns actual simple bimodules because each support has trivial stabilizer and hence exactly one simple bimodule; no projective-character ambiguity remains.

## The rotational branch is already excluded generally

The proved `R2053_ROTATIONAL_FS_OBSTRUCTION.md` excludes N=sum rotations. For completeness, its argument is as follows. Here rho is self-dual and rho^3 contains every rotation once. The pivotal odd-multiplicity form lemma forces nu_2(rho)=nu_2(r^2)=+1 in the positive spherical Galois conjugate. Therefore the pointed associator on C4 has even cohomology class. The integral inverse reflection dual is TY(C4); Ng--Schauenburg's exponent formula for group-theoretical categories bounds its FS exponent by eight. Shimizu's exact TY indicator formula instead gives nu_8(X)=0 for either nondegenerate bicharacter on C4 and either sign of tau, whereas exponent dividing eight would give nu_8(X)=dim(X)=2. This is a contradiction.

This argument uses only the pivotal form lemma, the actual inverse algebra, and published indicator/exponent formulas. It does not use C*-positivity, a classification of unitary realizations, or a presumed central lift.

## The surviving branch contains R8_1_18

The sole remaining normal form is

    rho^2=1+(s+rs+r^2s+r^3s)rho.

Put sigma=s rho and P=1+r+r^2+r^3. Directly from the displayed mixed rules,

    sigma r=r sigma,
    sigma^2=s phi(s) rho^2=r^3+P sigma.

Thus the full additive subcategory on

    1,r,r^2,r^3, sigma,r sigma,r^2 sigma,r^3 sigma

is closed under tensor products and duals. It is an actual fusion subcategory of E. Its fusion ring is R8_1_18. Reversing the chosen rotation generator changes the constant r^3 to r and gives the usual presentation of that census ring. Hence a categorification of R7_4_2053 necessarily gives a categorification of R8_1_18, as claimed.

The existence of this actual fusion subcategory is enough for the implication. No extension existence theorem, reconstruction of an associator, or additional Morita-invariance claim is required.

## Independent exact endpoint verification

`verify_r2053_r18_reduction.py` is standalone Python standard library. It reopens both authoritative compressed census tensors, checks their SHA-256 bindings, validates all source fusion identities, checks the source C4/TY and common-involution hypotheses, and determines the duality of the two inverse reflection orbits for both a values. It independently constructs both rank-sixteen tensors and checks every associativity and Frobenius-reciprocity identity. It recomputes the rotational cubic multiplicities and the two integer Shimizu residue sums [8,24,8,24]. Finally, it checks closure of the reflection rank-eight subcategory and matches all 512 coefficients to R8_1_18 with local-to-census map

    [0,1,7,2,4,3,6,5].

The source hashes are

- R7_4_2053: `17b7a12f7ae481ec749633f470cf33ca50e4b09c3ea168be5392cc5dfe0f1534`;
- R8_1_18: `cdd3aa4477861e8521c75ac63cb0f9e4e5d0a021073d1619aae358a0850704f2`.

The new verifier certifies the exact endpoint and the input identities of the previously proved reduction. It does not replace that reduction's categorical argument or its complete five-normal-form enumeration.

## Primary references already used by the audited parent proofs

- A. Schopieray, *Categorification of integral group rings extended by one dimension*, J. London Math. Soc. 108 (2023), 1617–1641, published Lemma 3.1, DOI 10.1112/jlms.12789.
- V. Ostrik, *On formal codegrees of fusion categories*, Math. Res. Lett. 16 (2009), 899–905, induced-unit formal-codegree theorem.
- S.-H. Ng and P. Schauenburg, *Frobenius–Schur indicators and exponents of spherical categories*, Theorem 9.2, https://arxiv.org/abs/math/0601012.
- K. Shimizu, *Frobenius–Schur indicators in Tambara–Yamagami categories*, Theorem 3.4, https://arxiv.org/abs/1005.4500.

## Final endpoint corollary

By the independently audited general-complex R8_1_18 exclusion in [the companion modular-center STS proof](../rank8/R18_STS_MOMENT_PROOF.md), R7_4_2053 has no complex fusion-category categorification. The proof is exactly the structural implication above followed by that endpoint theorem. The rank-seven criterion is `dihedral_Morita_R18_obstruction`. The endpoint theorem is a separate proof dependency; the reduction verifier does not itself certify it.

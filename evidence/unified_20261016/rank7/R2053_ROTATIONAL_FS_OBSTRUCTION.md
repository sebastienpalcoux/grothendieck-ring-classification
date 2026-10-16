# The rotational branch for R7_4_2053 is impossible

**Current classification status.** R7_4_2053 is now excluded over C by [the final R18 Morita endpoint argument](R2053_R18_MORITA_REDUCTION.md), using [the R18 STS theorem](../rank8/R18_STS_MOMENT_PROOF.md). This document proves the rotational-branch step only. Its original proof and intermediate verifier receipts are preserved below.

**Scope.** This is a necessary-condition improvement, not a complete
exclusion of R7_4_2053. In the four-case dihedral Morita reduction,
R7_4_2053 must use the reflection-support normal form. Consequently its
rank-sixteen Morita dual contains the rank-eight fusion subcategory
R8_1_18. The rotational normal form is excluded over C.

## Odd multiplicities in an odd tensor power

Let X be a self-dual simple in a pivotal fusion category over C. Write
epsilon=nu_2(X), which is +1 or -1. In a strict pivotal realization,
choose an isomorphism f:X -> X* whose pivotal transpose is epsilon f.
For odd n, the reversed dual word of X^n has the same sequence of
factors, so f tensor ... tensor f is a nondegenerate form on X^n with
pivotal transpose epsilon^n=epsilon times itself. This step does not
require a braiding: all factors and all component morphisms coincide.

If a self-dual simple S occurs with multiplicity m in X^n, the
restriction to its isotypic component is a nondegenerate multiplicity-
space form of sign epsilon/nu_2(S). A nondegenerate skew-symmetric form
has even dimension. Therefore

    m odd implies nu_2(S)=nu_2(X).

In particular, if the unit occurs oddly, nu_2(X)=+1, and every
self-dual simple occurring oddly also has indicator +1. This is a
form-theoretic statement; it makes no positivity assumption.

## Application to the rotational dihedral normal form

Assume a categorification of R7_4_2053 exists. The previously proved
dihedral reduction supplies its Morita equivalent category E with
eight invertibles D8=<r,s> and eight noninvertibles of dimension
t=2+sqrt(5). In the rotational branch, one may choose rho with

    rho*=rho, rho r=r^-1 rho, rho s=rs rho,
    rho^2=1+(1+r+r^2+r^3)rho.

Schopieray's two-dimension Galois pseudo-unitarity theorem allows
replacement by a pseudo-unitary Galois conjugate with the same fusion
rules and the same existing inverse reflection algebra. Equip it with
the canonical positive spherical structure.

Writing P=1+r+r^2+r^3 gives rho^3=P+(1+4P)rho. Thus both 1 and r^2
occur with multiplicity one. The preceding lemma gives

    nu_2(rho)=nu_2(r^2)=+1.

Let k in Z/4 be the associator class on the pointed rotation C4.
Its restriction to <r^2> is k modulo two. In the positive spherical
structure of a pointed category the order-two indicator is the sign
of that restricted class. Hence k is even, and the restriction to C4
has order at most two.

The integral subcategory of the inverse reflection dual is the
group-theoretical category C(D8,<s>,Omega,psi), and its fusion rules
are TY(C4) for source R7_4_2053. Ng--Schauenburg, Theorem 9.2, gives
its FS exponent as the least common multiple of

    |C| order(res_C[Omega])

over cyclic subgroups C of D8. On the rotation subgroup this divides
4*2=8; all other nontrivial cyclic subgroups have order two, and their
terms divide four. Therefore this integral category has FS exponent
dividing eight.

This is impossible for any TY(C4,chi,tau). Nondegeneracy gives
chi(x,y)=i^(epsilon*x*y), epsilon=+1 or -1. Shimizu, Theorem 3.4,
with k=4 gives

    nu_8(X)=1/8 sum_(a+b+c+d=0 mod4)
                        i^[epsilon*(ab+ac+ad+bc+bd+cd)].

The exponent classes 0,1,2,3 occur respectively 8,24,8,24 times,
so the sum and nu_8(X) vanish for both choices of epsilon and both
choices of tau. FS exponent dividing eight would instead give
nu_8(X)=FPdim(X)=2. This contradiction excludes the rotational branch.

## Exact replay and remaining scope

`verify_R2053_rotational_fs.py` binds the source R7_4_2053 tensor,
checks its integral C4/TY type and self-duality, constructs the
rotational dihedral tensor independently, checks the required cubic
multiplicities, and evaluates both indicator sums over the integers.
The source-independent dihedral constructor and its full fusion-axiom
validation are in the already audited four-case and R35 packets.

The reflection-support normal form has no unit summand in rho^3,
so the argument above does not exclude it. No classification count
changes on the basis of this result alone.

Primary references:

- A. Schopieray, *Categorification of integral group rings extended by
  one dimension*, JLMS 108 (2023), published Lemma 3.1,
  DOI 10.1112/jlms.12789.
- S.-H. Ng and P. Schauenburg, *Frobenius--Schur indicators and
  exponents of spherical categories*, Theorem 9.2,
  https://arxiv.org/abs/math/0601012.
- K. Shimizu, *Frobenius--Schur indicators in Tambara--Yamagami
  categories*, Theorem 3.4, https://arxiv.org/abs/1005.4500.

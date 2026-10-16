# A unified dihedral Morita reduction for four rank-seven cases

**Current classification status.** All four source cases are now decided. R7_4_35 and R7_4_2665 have unitary models; R7_4_2603 is excluded by [the two-moment theorem](R2603_CENTER_MOMENT_PROOF.md), and R7_4_2053 is excluded by [the R18 endpoint theorem](R2053_R18_MORITA_REDUCTION.md). The structural argument and its intermediate verifier receipts below retain their original narrower scope.

This is a new structural reduction, not an exclusion or a construction.
It applies over C without a pivotality or unitarity assumption to
R7_4_35, R7_4_2053, R7_4_2603, and R7_4_2665.

Write t=2+sqrt(5), so t²=1+4t. Each ring has four invertibles G,
a dimension-two simple X, and two simples Y,Z of dimension 2t.
There is an involution h in G fixing X,Y,Z on both sides. The source
rules have XY=Y+Z and N_{YY*}^X=1. Moreover X²=sum_{g in G}g.
The group G is V4 for cases 35 and 2603, and C4 for 2053 and 2665.
Y and Z are self-dual for 35 and 2053 and are a dual pair for 2603 and 2665.

## 1. All three fixed-object projective blocks split

The pointed subgroup H={1,h} has trivial associator because it fixes
X. Hence A=1+h is a connected separable algebra. Every H-fixed simple
has both a left and a right A-module structure since H²(C2,C*)=0.
For fixed simples U,V, their tensor product is an A-bimodule using the
left action on U and right action on V. Each simple isotypic component
is preserved by these actions.

An A-bimodule supported on a fixed simple W is a projective
representation of H×H on its multiplicity space. A nontrivial class
has only irreducibles of dimension two. Therefore an occurrence of W
with multiplicity one in UV forces its projective class to be trivial.
Apply this first to XY=Y+Z and then to the X summand of YY*.
Consequently X,Y,Z each support four simple A-bimodules with their
original underlying object.

The two free H-orbits of invertibles each support two simple
A-bimodules. Thus the Morita dual D has eight invertibles, four from
X and four from G, and eight noninvertibles of dimension t, four each
from Y and Z. Its two FP dimensions are 1 and t. Since t²=1+4t,
any product W W* has exactly one invertible constituent. The eight
invertibles act freely and transitively on the eight noninvertibles.

## 2. The invertible group is D8

In the inverse Morita context, the internal end of the regular right
A-module is the sum of the two invertible A-bimodules supported on H.
Call this order-two subgroup L of K=Inv(D). Indeed the multiplicity
of a simple bimodule V in the internal end is Hom_C(1,V), which is one
for exactly these two objects and zero for every other simple.

The inverse dual of the pointed category Vec_K^omega along L is the
integral rank-five subcategory of the original category, with four
invertibles and X of dimension two. If L were normal, each of the four
L-double cosets would give two one-dimensional projective stabilizer
representations, because H²(C2,C*)=0, and the dual would be pointed of
rank eight. Therefore L is not normal. Among groups of order eight,
only the dihedral group has a nonnormal subgroup of order two. Hence
K=D8, with L a reflection subgroup. No assertion that omega is trivial
is made or needed.

## 3. The mixed automorphism must exchange reflection classes

Write D8=<r,s | r^4=s²=1, srs=r^{-1}>. For a noninvertible rho,
write rho g=phi(g)rho and rho²=a+N rho, with phi an automorphism,
a in D8, N a nonnegative integral group-ring element, and sum N=4.
Associativity and duality give

    phi²=Ad(a), phi(a)=a, N g=phi(g)N, phi(N)=N,
    N*=a^{-1}N.

In the inverse L-bimodule category, a noninvertible double orbit
represented by g rho has stabilizer L intersect g phi(L) g^{-1}.
If this intersection had order two, the two one-dimensional stabilizer
representations would give noninvertibles of dimension t in the
original category. Its only noninvertible irrational dimension is 2t.
Thus L and phi(L) are not conjugate. Equivalently phi exchanges the
two conjugacy classes of reflections.

After replacing rho by b rho and changing the dihedral generators,
we may normalize

    phi(r)=r^{-1}, phi(s)=rs, a in {1,r²}.

The coefficient equations then show that N has equal coefficients A
on all four rotations and coefficients B,B,C,C on the two adjacent
pairs of reflections. Thus 4A+2B+2C=4. When a=r² the duality equation
also forces B=C. Conjugating interchanges B and C. There are exactly
five normalized candidates:

    a=1:  N=sum rotations; N=sum reflections; N=2(s+rs);
    a=r²: N=sum rotations; N=sum reflections.

For the exceptional candidate N=2(s+rs), the regular Casimir has
characteristic polynomial

    (x-16)^4 (x²-160x+1280)^2 (x²-96x+768)^4.

The last roots are 48+/-16sqrt(6). A regular Casimir eigenvalue is
(dim E) f_E, so some formal codegree is outside Q(sqrt(5)). The
published two-dimension Galois pseudo-unitarity theorem and Ostrik's
induced-unit theorem imply that every formal codegree must lie in
Q(t): D/f_E is the dimension of an actual forgotten central object,
hence lies in Q(t). Therefore this fifth candidate is excluded over C.

## 4. The four surviving ring families and the remaining issue

If N is the sum of rotations, the subcategory on C4 and C4 rho has
standard C4 Haagerup-Izumi rules when a=1 (R8_1_15), and the
non-self-dual twisted C4 rules when a=r² (R8_1_12).

If N is the sum of reflections, replace rho by sigma=s rho. Its
commutation with r becomes trivial; sigma² is r or r³ plus the sum
of the four noninvertibles. Thus the resulting rank-eight subcategory
has the commutative, entirely non-self-dual C4 rules R8_1_18.

The original four rank-seven cases are therefore controlled by a
very short list of dihedral extensions of these three rank-eight
families. The a=1 cases have self-dual inverse noninvertibles and the
a=r² cases have a dual pair. Thus 35/2053 use a=1, and 2603/2665 use a=r².

The reduction alone does not construct the required coherent extensions.
The subsequent inversion-descent proofs do so for two explicit near-group
orbifolds: the diagonal C4 orbifold of the Yu--Zhang C4² category realizes
R7_4_35, and the 4C16 orbifold of Budinski's C16 category realizes
R7_4_2665. See R35_INVERSION_CONSTRUCTION.md and
R2665_INVERSION_CONSTRUCTION.md. Their automorphisms are established
directly, including coherence. An earlier draft's claim about the absence
of an inversion action on "standard C4 Haagerup categories" was too broad
and is withdrawn: the self-dual C4 based ring alone does not identify a
category with one of the previously classified subfactor realizations.
No such identification is needed by the new construction. R7_4_2053 and
R7_4_2603, and the R8_1_18 extension input, remain unresolved by these
arguments. The subsequent odd-cube indicator argument in
R2053_ROTATIONAL_FS_OBSTRUCTION.md excludes the rotational branch of
R7_4_2053, so that case must contain R8_1_18 on its rank-sixteen Morita
side. This necessary condition does not settle the reflection branch.

## Reproducible algebra

The publication verifier verify_four_case_dihedral.py reopens the rank-seven
census, binds all four source tensors by SHA-256, and verifies all source
associativity, duality, Frobenius reciprocity and dimension identities.
It enumerates every automorphism of D8, every possible a, and every
nonnegative N of coefficient sum four, with no optimization solver.
The necessary exchange of reflection conjugacy classes leaves 24
unnormalized systems and exactly the five displayed normal forms.
For each normal form the verifier constructs all 4096 structure constants,
checks all fusion identities, and computes the regular Casimir polynomial
over the integers. The three neutral rank-eight identifications are
independently matched to the lexically indexed source census by all 512
structure constants. Normal and Python -O replays both pass.

The categorical references are A. Schopieray, *Categorification of integral
group rings extended by one dimension*, J. London Math. Soc. 108 (2023),
1617–1641, published Lemma 3.1 (DOI:10.1112/jlms.12789), and V. Ostrik,
*On formal codegrees of fusion categories*, Math. Res. Lett. 16 (2009),
899–905, for the induced-unit formal-codegree formula. The verifier
certifies the finite consequences of these results; it does not solve
the remaining associator or extension problem.

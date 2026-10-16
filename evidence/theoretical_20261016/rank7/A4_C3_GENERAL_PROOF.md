# Three general exclusions through C3 and V4 Morita duality

The rings R7_2_236, R7_4_2167, and R7_4_2716 have no complex fusion categorification. The argument imposes no pivotal, spherical, pseudo-unitary, or unitary hypothesis. R7_3_1022 is included only to record the exact limit of this reduction and remains unresolved.

The source rings are R7_2_236, R7_4_2167, R7_4_2716, R7_3_1022.
Their dimensions are 1,1,1,3,d,d,d with d^2=4+md and
m=6,12,12,8. Their integral rank-four subring has the Rep(A4) rules.
The previously recorded C3 module relaxation is exact at the ring level.

Let C be a hypothetical complex fusion categorification and A the regular
algebra of its order-three invertible subgroup. The fixed dimension-three
simple trivializes the pointed associator. The dimension-three simple's
square has coefficient2 on itself; its projective C3xC3 block must split.
Thus C_A has dimensions 1^4,d. The Morita dual D has 12 invertibles and
three d-dimensional simples. The pointed associator on its group K is
trivial: K fixes the unique d-dimensional simple of C_A, giving a rank-one
module category over Vec_K^omega.

The invertibles act transitively on the four dimension-one modules. A
stabilizer L has order3. The original integral rank-four subcategory is
the Morita dual of Vec_K with respect to L. If L were normal, its four
double cosets would each yield three simples (H^2(C3,C*)=0), giving rank12
rather than rank4. Therefore L is nonnormal. The kernel of the transitive action on four
points is a normal subgroup contained in L, and hence is trivial. Thus
K embeds into S4 with order12, so it is the unique index-two subgroup
A4; L is a Sylow3 subgroup.

The three noninvertible simples of D form a transitive K-orbit; their
stabilizer H=V4 is normal. The same holds on the right. At least one of
these three simples rho is selfdual. Its HxH stabilizer cocycle has an
alternating commutator form beta on F2^4. Duality exchanges the two H
factors and inverts the commutator; since its values are +/-1, beta is
invariant under this swap. Thus in matched bases

    beta = [bJ C; C bJ],  J=[0 1;1 0],  C=C^t.

There are two algebra structures on the object sum_{h in H} h, indexed by
H^2(H,C*)=C2. Changing this algebra cocycle adds diag(J,J) to beta. A
check of the eight symmetric 2x2 matrices C over F2 shows that the two
forms have ranks (2,4) or (4,2), except C=0, which gives (0,4).
The rank-zero case is impossible: it gives a simple bimodule with
underlying object rho and dual FP dimension d/4, whose monic minimum
polynomial has constant coefficient -1/4. Consequently one algebra
choice gives rank2 for beta. Its twisted group algebra has four simple
modules of dimension2, giving four bimodule simples per rho, of dual
FP dimension d/2. A4 conjugation preserves the unique nontrivial H^2
class, so all three rho-orbits have the same block rank.

The resulting Morita category D' has twelve invertibles and twelve
noninvertibles of dimension t=d/2, with t^2=1+(m/2)t. Its invertible group
is A4: for the untwisted H algebra the pointed Morita dual is
Vec_(Hhat semidirect C3)=Vec_A4. The nontrivial H cocycle extends to A4
through the binary tetrahedral extension Q8 semidirect C3 -> A4, so it
is carried from the untwisted H algebra by a tensor autoequivalence of
Vec_A4. This gives the same pointed dual for both algebra choices.

Thus the reduced based-ring question has 24 simples, twelve
forming A4 and twelve a free orbit of A4, with noninvertible dimension
satisfying t^2=1+k t for k=3,6,6,4. The classification and formal-codegree argument below exclude k=3 and k=6, giving the three stated general exclusions. The k=4 case remains possible at this stage, and the argument does not construct a categorification of its original rank-seven source.

Scope clarification: the original C can be recovered from D' using an
algebra supported on all twelve invertibles, not necessarily a subgroup
C3 algebra. Its three dimension-2t simples can correspond to the three
2-dimensional projective irreducible representations of A4. Therefore
orbit sizes alone do not contradict the rank-seven dimension pattern.

## Explicit justification of the first Morita step

Let g generate C3 and X be the dimension-three simple, so gX=Xg=X
and N_XX^X=2. Fixed X gives a rank-one module over the pointed C3
subcategory, hence its associator class vanishes. Since H^2(C3,C*)=0,
X admits both a left and a right A-module structure. The object X tensor X
then has a left-right A-bimodule structure. Its X-isotypic component has
underlying object 2X. A-bimodule structures supported on X are projective
representations of C3xC3. A nontrivial alternating class on C3xC3 has
only irreducible modules of dimension3. The dimension2 multiplicity space
therefore forces the trivial class. Hence X supports nine simple
A-bimodules with underlying object X, each of dual dimension3/3=1.
The orbit {1,g,g²} supports three further simple A-bimodules, each with
underlying object A and dual dimension1. Thus exactly twelve invertibles
occur in D. The remaining orbit of three d-dimensional source objects
has stabilizer C3 inside C3xC3, and H^2(C3,C*)=0, so it gives exactly
three simple bimodules of underlying dimension3d and dual dimension d.

Right A-modules consist of the free orbit A (dimension1 after dividing
underlying FP dimension by3), the three structures on X (each dimension1),
and the one free orbit of the three d-dimensional objects (dimension d).
This derives the module and dual dimensions from actual hypothetical
categories, not merely from one feasible Gram solution.

Let B be the integral rank-four fusion subcategory generated by X. The
category B_A is an indecomposable module category, and its dual consists
of exactly the twelve invertibles just described. Therefore the K action
on its four simple modules is transitive. The unique d-dimensional
simple of C_A is fixed by K; the associativity isomorphisms of this
rank-one Vec_K^omega module give a 2-cochain whose coboundary is omega,
so the entire pointed associator is trivial.

For any noninvertible Y in D, the coefficient of the unit field part
in FPdim(Y Y*)=d²=4+md shows that exactly four invertibles occur in
Y Y*: every such multiplicity is0 or1 by rigidity, and all other
summands have dimension d. Thus the left stabilizer has order4, and the
K orbit has size3. The right stabilizer similarly has order4. Both are
the unique V4 subgroup of A4.

## The symmetry and final orbit details

For rho=rho*, duality sends h tensor rho tensor k to
k tensor rho tensor h, since every h in V4 is selfdual. Applying this
contravariant equivalence to chosen stabilizer isomorphisms inverts the
projective commutator and swaps the H factors. Changing the selfduality
isomorphism changes only scalar choices, hence not the commutator class.
As all commutators have order2, inversion does not change them. This
proves the asserted swap invariance in the same H bases, without a
pivotal assumption.

The two algebra twists on H restrict on HxH to the cocycle on the left
and its inverse on the right. Their commutator forms therefore differ
by diag(J,-J)=diag(J,J) in characteristic2. Conjugation by an element
of A4 preserves the unique nontrivial class in H²(V4,C*); transporting
rho to either other noninvertible conjugates the stabilizer cocycle by
an invertible linear change of coordinates, preserving its rank.

The pointed dual is actually untwisted Vec_A4 for either algebra choice:
for H untwisted this follows by the explicit Fourier duality for the split
semidirect product H semidirect C3. For the other choice, the central
extension Q8 semidirect C3 -> H semidirect C3, with kernel{+1,-1},
provides an extending A4 2-cocycle. The identity functor of Vec_A4 with
that tensorator maps one H algebra to the other. Thus their pointed
Morita duals are tensor equivalent, including associators.

Finally any noninvertible Y in D' satisfies FPdim(Y Y*)=t²=1+kt.
Comparing rational and irrational coefficients gives exactly one
invertible summand, so its left stabilizer has order1. The twelve
invertibles therefore act freely and transitively on all twelve
noninvertibles. This proves the free-orbit hypothesis used in the
quadratic A4 ring classification.

## A shorter proof for R7_2_236

After just the first Morita step, the two simple FP dimensions are 1 and d, with d²=4+6d. Schopieray, *Categorification of integral group rings extended by one dimension*, J. London Math. Soc. 108 (2023),1617–1641, DOI https://doi.org/10.1112/jlms.12789, Proposition 3.3, proves the necessary divisibility s | r for irrational d satisfying d²=r d+s. Here 4 does not divide 6. Thus R7_2_236 is excluded before the V4 step. The longer A4 argument gives an independent proof for the same source and is needed for the two m=12 sources.

## Classification and exclusion of the reduced A4 rings

## 1. Associativity, rigidity, and the choice of rho

Right multiplication by invertibles commutes with the free left action. It is itself free: rho g=rho implies g^(-1)rho*=rho*, and the left action is free on every noninvertible. Thus it gives an automorphism phi of G=A4 such that rho g=phi(g)rho. By Frobenius reciprocity, the multiplicity of an invertible g in rho² is the multiplicity of rho* in g^(-1)rho. Exactly one such g exists, with multiplicity one. Denote it by a. Write

    rho² = a + N rho,     N = sum(n_g g),     n_g >= 0,     sum n_g=k.

Associativity of (rho²)g=rho(rho g) and rho(rho²)=(rho²)rho gives

    phi²=Ad(a),        phi(a)=a,
    N s=phi(s)N,       phi(N)=N.

The dual is rho*=a^(-1)rho, and compatibility with the involution gives

    N*=a^(-1)N.

For completeness, in comparing the two bracketings of rho³, the invertible terms give phi(N)a=Na, hence phi(N)=N; the noninvertible terms then give phi(a)=a. Taking the dual of rho² gives N=a phi(N*), equivalent to the displayed involution condition.

Use Aut(A4)=S4 and Z(A4)=1. Write phi=Ad(sigma), sigma in S4; then necessarily a=sigma². Replace rho by rho'=b rho for b in A4. The parameters become

    sigma'=b sigma,       a'=(b sigma)²,       N'=bN.

(The formula for N' follows from N b^(-1)=phi(b^(-1))N.) If sigma is even choose b=sigma^(-1). If sigma is odd choose b=tau sigma^(-1), where tau is a fixed transposition. Thus there are two normal forms:

    inner: sigma=1, phi=id, a=1;
    outer: sigma=tau, phi=Ad(tau), a=1.

In both normal forms rho is self-dual. This is a proved change of basis, not an initial self-duality assumption.

## 2. Complete enumeration of the coefficients

### Inner normal form

N is a central, self-adjoint nonnegative element of Z[A4]. The conjugacy classes have sizes 1,3,4,4, with inversion exchanging the two size-four classes. Therefore

    N = A·1 + B·sum(v in V4\{1})v + C·sum(three-cycles)g,
    k = A+3B+8C.

For k<=6, C=0. The complete possibilities (A,B) are:

| k | (A,B) |
|---|---|
| 3 | (3,0), (0,1) |
| 4 | (4,0), (1,1) |
| 6 | (6,0), (3,1), (0,2) |

### Outer normal form

M=tau N is an element of the odd coset of A4 in S4 invariant under conjugation by A4. That coset has exactly two A4-conjugacy classes: the six transpositions and the six four-cycles. Both are preserved by inversion and conjugation by tau, so all the other coefficient constraints hold automatically. Hence k=6(B+C). There is no outer ring for k=3 or 4. For k=6 there are exactly two: M is the sum of the transpositions or the sum of the four-cycles.

These choices produce based rings; the accompanying exact program independently verifies all associativity, unit, duality, and Frobenius-reciprocity identities of the complete 24×24×24 tensors. It also checks their regular Casimir characteristic polynomials against the theoretical formulas below. The program also enumerates all 24 original automorphisms before normalization: there are respectively 24, 24, and 60 unnormalized coefficient systems for k=3,4,6. It verifies the complete 24-dimensional basis change for every one, recovering exactly the 2,2,5 normal forms. Normal and optimized Python replays agree byte for byte.

## 3. A necessary formal-codegree field condition

Schopieray, *Categorification of integral group rings extended by one dimension*, J. London Math. Soc. 108 (2023), 1617–1641, p. 1628, Lemma 3.1, DOI https://doi.org/10.1112/jlms.12789, proves that a category with only two simple Frobenius–Perron dimensions is Galois conjugate to a pseudo-unitary category. The Galois conjugate has the same based ring. The claim is existence of a pseudo-unitary categorification of that ring, not pseudo-unitarity of every original categorification.

In a pseudo-unitary categorification C, put D=FPdim(C). For every irreducible representation E of its fusion ring, Ostrik's induced-unit theorem gives a simple A_E in Z(C) with

    FPdim(A_E)=D/f_E,

where f_E is the formal codegree (Ostrik, *On formal codegrees of fusion categories*, Math. Res. Lett. 16 (2009), and the induced-unit formulation in *Pivotal fusion categories of rank 3*, arXiv:1309.4822, Theorem 2.13).

The forgetful image of A_E is an actual object of C, so its dimension is an integer combination of 1 and t. Since D is also in Q(t), this implies the necessary condition

    every formal codegree f_E belongs to Q(t).

This condition applies to all the quadratic rings here by the preceding Galois reduction.

## 4. Formal codegrees and the exclusions

Let r_s^±=(s±sqrt(s²+4))/2, so r_s satisfies r_s²=1+s r_s.

In the inner case, the three one-dimensional representations of A4 have N-eigenvalue k, whereas its three-dimensional representation has N-eigenvalue ell=A−B. Each extends to two representations of R, with rho acting as r_k^± or r_ell^± respectively. Their formal codegrees are

    dimension 1: 12(1+(r_k^±)²), each sign three times;
    dimension 3:  4(1+(r_ell^±)²).

Indeed the regular Casimir is 12(1+rho²), and its scalar on E is dim(E) f_E.

When B=0, {1,rho} is the closed rank-two subring rho²=1+k rho. Ostrik's rank-two classification excludes it for k>1.

For k=3, the only remaining inner choice has ell=−1. Its three-dimensional codegrees are

    10+2sqrt(5),  10−2sqrt(5),

but Q(t)=Q(sqrt(13)). The field condition fails.

For k=6, both remaining inner choices have ell=2 or −2. Their three-dimensional codegrees are

    16+8sqrt(2),  16−8sqrt(2),

but Q(t)=Q(sqrt(10)). Again the field condition fails.

In the outer case, restrict the standard three-dimensional representation of S4 to A4 and let T represent tau. The transposition class sum acts by 2I and the four-cycle class sum acts by −2I. Since M=tau N, the matrix of N is respectively 2T or −2T. Extend to R by taking rho=r_2^± T or r_(-2)^± T. These are irreducible three-dimensional representations with the same codegrees 16±8sqrt(2). Both k=6 outer rings therefore fail the field condition as well. The other representations are two one-dimensional representations with codegrees 12(1+(r_6^±)²), and one two-dimensional representation with codegree 12; their squared dimensions sum to 24 as required.

For k=4, the surviving choice (A,B)=(1,1) has ell=0, so its three-dimensional formal codegrees are both 8. Its relations are

    rho g=g rho,       rho²=1+sum(v in V4)v rho.

They are realized by the known Haagerup–Izumi V4 category crossed with the strict cyclic order-three symmetry fixing rho and permuting the three nonidentity V4 invertibles; the resulting invertibles form V4⋊C3=A4. Grossman arXiv:1612.07185, §§2.5 and 3.2, describes this crossed product as C2. This gives existence for the based ring; no uniqueness claim about categorifications of that ring is needed or made.

## 5. Ordinary arithmetic checks and independent source matches

All nine candidate rings pass the individual formal-codegree d-number test: for c=12 or 4, f=c(1+r_s²) has trace c(s²+4) and norm c²(s²+4), so its norm divides the square of its trace. The rational codegrees pose no problem. Their character values lie in composites of quadratic fields and Q(zeta_3), so cyclotomicity alone also gives no exclusion. The stronger common-field condition is what resolves the remaining nontrivial branches.

As an independent check, the V4 quadratic subrings match these source tensors:

| (k,A,B) | Rank-eight source | Status |
|---|---|---|
| (3,0,1) | R8_1_68 | Previously excluded generally |
| (4,1,1) | R8_1_69 | HI(V4), unitarily realized |
| (6,0,2) | R8_2_480 | Previously excluded generally |

For each match the source-basis permutation is [0,1,2,7,3,6,5,4] relative to the generator's order. The replay compares all 512 coefficients and the published source digest. These historical exclusions are corroboration only; the field argument above is a separate pure proof.


## Exact evidence and scope

Run `python verify_C3_A4_reduction.py --repo REPOSITORY_ROOT`. It reopens the complete rank-seven census, binds all four tensors by their original source IDs and SHA-256, verifies all 343 coefficients through their fusion identities, checks the exact dimension and module characters, and checks all eight symmetric cross-forms over F2. It invokes `verify_A4_quadratic.py` with the same repository root. That verifier regenerates the complete nine normalized tensors, checks every coefficient of all 108 normalization maps from the 24 automorphisms, and verifies the complete Casimir characteristic polynomials. The unnormalized counts are 24,24,60 for k=3,4,6, respectively. Its rank-eight subring comparisons are corroboration; the theoretical formal-codegree field proof is independent of those historical exclusions.

Both programs use exact arithmetic and no optimizer. Normal and optimized Python replays agree. The tensor generator output is retained as `A4_quadratic_certificate.json`; concise receipts are `C3_A4_reduction_replay.json` and `A4_quadratic_replay.json`. The categorical proof, normalization, published Galois-scope theorem and field obstruction were independently audited in `C3_A4_INDEPENDENT_AUDIT.md`.

The corrected published Lemma 3.1, rather than the earlier arXiv wording, is essential: it guarantees a Galois-conjugate pseudo-unitary categorification of a two-dimension ring, and does not claim the initial category itself is pseudo-unitary. No unitary classification is used to exclude any of the three source rings.

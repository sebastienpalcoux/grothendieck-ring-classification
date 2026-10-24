# Phase five: a unitary model for R9_2_1848

**R9_2_1848 is modelled. R9_2_1975 remains unresolved.**

The new model is an application of an existing, general orbifold theorem to an
existing unitary near-group category. It does not require a new associator ansatz
or the unproved assertion that every spherical category is unitary.

## Construction and complete fusion rules

Let N be Budinski's near-group category J_18^1 of type C18+18. Its simple
objects consist of the group G=C18 and one object rho with

    rho^2 = sum_(g in C18) g + 18 rho,
    FPdim(rho) = 9 + 3 sqrt(11).

The source exists as a unitary category by the Cuntz algebra construction
described in Budinski, Theorem 3.1.1 and Table 3.1 (the four rows for n=18).
Table 3.1 displays rounded phase coordinates, but section 3.3.2 explicitly
explains the exact algebraic certification of these solutions. We use the
source's existence result as a literature dependency. This continuation does
**not** claim to independently reconstruct or replay its complete associator.

For J_18^1 the nondegenerate symmetric pairing and quadratic refinement are

    <x,y> = exp(2 pi i xy/18),
    a(x) = exp(-pi i x^2/18).

Take H={0,6,12}. Then

    H^perp = {0,3,6,9,12,15},
    H subset H^perp,  a|H=1,
    G/H = C6,  H^perp/H = C2,  G/H^perp = C3.

Apply **Izumi, Theorem 12.5**, together with the irreducible decomposition
and multiplication formulas immediately preceding it in section 12.1.
This theorem covers isotropic H; it does not require H to be Lagrangian.
The resulting unitary orbifold has six distinct invertibles indexed by G/H,
and three distinct noninvertibles indexed by G/H^perp. With g a generator
of C6 and X the distinguished component, its complete presentation is

    g^6=1,  g^3 X=X,  Xg=g^-1 X,
    X^2=1+g^3+2(X+gX+g^2X).

Here the theorem's shift g_a may be chosen to be zero because a|H=1.
Its noninvertible coefficient is |H^perp/H|=2. In particular,
FPdim(X)=3+sqrt(11), all three noninvertibles are self-dual, and the category
has rank nine and maximum fusion multiplicity two. The construction supplies
associativity at the categorical level; checking the based tensor alone would
not supply that missing premise.

The construction is a special case of the unified formula

    sigma^2 = sum_(k in H^perp/H) alpha_(k-g_a)
              + |H^perp/H| sum_(q in G/H^perp) alpha_q sigma,
    alpha_g sigma = sigma alpha_-g.

Thus the model uses a known theoretical construction and a known source
category, rather than claiming a new family of associators.

## Exact census binding

Order the model basis as

    [1,g,g^2,g^3,g^4,g^5,X,gX,g^2X].

The map into the census tensor basis is

    [0,1,4,8,3,2,5,7,6].

All **729** coefficients agree with R9_2_1848. The source tensor SHA256 is
`42681407529a88aaaf34a909975776d8d1008ee8a99b6e231263dcb1aae9ff5c`.
The self-contained record `1848_model.json` includes both tensors and the
permutation. Run

    python verify_1848_model.py

to verify the transport, the subgroup and root-of-unity exponent conditions,
associativity, duality, and the dimension identities using exact integers.
The receipt is `1848_model_verification.json`. Its scope explicitly separates
the new exact transport from the cited near-group existence theorem.

## Primary sources and scope

1. P. G. Budinski, *Exotic Fusion Categories and Their Modular Data*, master's
   thesis, University of Alberta (2021), Theorem 3.1.1, Table 3.1 (n=18),
   section 3.3.2 (exactness, printed pp.46–47).
   DOI: https://doi.org/10.7939/r3-7p7k-fg18.
   Institutional PDF:
   https://ualberta.scholaris.ca/bitstreams/3f73f320-a2a2-4184-ad81-d8708764f725/download.
2. M. Izumi, *A Cuntz algebra approach to the classification of near-group
   categories*, arXiv:1512.04288v2, section 12.1, Theorem 12.5 and the
   preceding action formulas (printed pp.107–111):
   https://arxiv.org/abs/1512.04288v2.

Source URLs and hashes are in `sources.json`. Downloaded primary papers and
extracted text are held in the local research cache; they are not included
in the verified baseline archive or the final research package. In particular,
Izumi's cached PDF and text under `sources` are URL/hash dependencies, not
bundled replay inputs. The exact tensor replays do not read these cached
papers. Later citations to the thesis in Yu's 2024 paper and
Yu–Zhang's notes support that its solutions are used as existence results,
but the proof dependency above is the primary thesis itself.

Izumi works in the unitary C* setting. That is sufficient here because the
conclusion is the existence of one unitary model. No classification theorem
for arbitrary original spherical categories is inferred.

## R9_2_1975: new avenues examined and present blockers

The phase-four reduction remains valid: a hypothetical categorification has
a rank-twelve Morita dual with eight invertibles forming D8 and four
noninvertibles of dimension d=4+3sqrt(2). The stabilizer is Z(D8)=C2.
After the existing field and lower-rank exclusions, there is one extreme
branch containing R6_4_155 and two uniform branches. These are necessary
based tensors, not categorical models.

The successful orbifold construction above suggests trying the same general
formula here. If an untwisted isotropic orbifold of a type G+|G| near-group
category had eight invertibles, four noninvertibles and stabilizer order two,
the formula would force |G|=32 and |H|=4, with source dimension
16+12sqrt(2)=4d. However, its invertible group would be the **abelian** quotient
G/H, so it cannot directly realize any of these D8 candidates.

Fresh primary literature supplies a more promising source than Budinski's
finite table: Radchenko--Wheeler, arXiv:2609.21892v1, Theorem 10 and
Corollary 4, constructs nonunitary near-group categories for every two-generator
abelian group. He--Liu--Lu--Palcoux--Ren, arXiv:2610.11652, Theorem 5.4 and
Corollary 6.6, separately supplies spherical and pseudo-unitary cyclic examples.
These are explicit reconstruction/existence statements; using them in this
direction does not require parameterizing every arbitrary spherical category.
Thus source existence at order 32 is available. The extension of Izumi's
orbifold calculation to the explicit algebraic Leavitt realization is now
proved in `../orbifold_scope/ALGEBRAIC_ORBIFOLD.md`, with independent audit
PASS in `../audit_orbifold_scope/REPORT.md`. No unitarity assertion is made
for these new order-32 sources.

There is still a structural obstacle to the immediate model route. Quotients
of two-generator abelian G have at most two cyclic generators. Every pointed
category on such a group has pointed Drinfeld center (there is no alternating
three-generator cocycle contribution). A pointed category on D8 has a
nonpointed center, already from the two-dimensional representation of D8.
Therefore a Morita change confined to the integral pointed subcategory cannot
connect these source quotients to the required D8 category. A genuinely
nonintegral algebra or a source with more generators is needed.

For a concrete order-32 datum, the Radchenko--Wheeler matrix
`[[1,4],[8,33]]` gives G=C8 x C4, pairing
`exp(2 pi i(-x1*y1/8+x2*y2/4))`, and refinement
`(-1)^(x1+x2) exp(pi i(-x1^2/8+x2^2/4))` in their convention.
Its isotropic subgroup of order four is
`H=<(4,0),(0,2)>`; the refinement restricts nontrivially to H.
The proved algebraic orbifold construction therefore gives a rank-twelve category
with invertibles C4 x C2 and four non-self-dual objects with uniform
multiplicity two. It does not identify the required D8 dual tensor.
We tested the image of the canonical source near-group algebra `1+rho`,
namely `A=1+sum X_i`, of dimension 17+12sqrt(2), conditionally on the
categorical algebra being available. Its induction Gram matrix and unique
nonnegative factor, up to permutation of columns, are

    B = [[I8,J_(8,4)], [J_(4,8),I4+8J4]],
    F = [[I8,0], [J_(4,8),I4]].

Uniqueness is immediate: the first eight rows have norm one and are
orthogonal, so they force eight distinct coordinates; subtracting their
contribution leaves I4. Thus there are exactly twelve simple A-modules.
For the two canonical Lagrangian objects in the common center, their
endomorphism dimensions are respectively 12 and the dual rank r, and
their Hom dimension is the module rank 12. Cauchy--Schwarz gives
144<=12r, so r>=12. This specific nonintegral algebra therefore cannot
produce a rank-nine Morita dual.

There is also a D8 obstruction for this direct move. The two different
module-dimension orbits have lengths eight and four. The source invertibles
act regularly on the first orbit. Every invertible dual object gives a
permutation commuting with all source actions, so its restriction to that
orbit is a translation in C4 x C2. The cross-action matrices force its
permutation on the other orbit uniquely. Consequently the dual invertible
group embeds into C4 x C2 and cannot be D8. Commuting permutations are
only candidate actions; we do not infer the existence of an invertible
dual object from a matrix alone.

The exact replay `probe_order32_canonical_algebra.py` constructs the full
rank-twelve tensor, verifies the Gram factor and all module products, and
checks the eight possible translations against all 24 permutations of
the other orbit. The receipt is `order32_canonical_algebra_probe.json`.
This is a limitation of the proposed model route, not an exclusion of any
rank-nine fusion ring. Other nonintegral algebras or repeated Morita moves
are not ruled out. Izumi's Remark 12.4 also records self-duality of the
canonical orbifold subfactor in its unitary setting, consistent with this
failure to reach a smaller rank.

We also checked the generalized near-group restrictions for a possible
shortcut. Normality of the stabilizer is satisfied, and the nonabelian
representation bound of Schopieray, Proposition 3.4, gives only
dim(psi)<=|D8/C2|=4; the relevant two-dimensional representation passes.
Neither a ring-central involution nor its fixing all noninvertibles by itself
provides a coherent central half-braiding. Thus de-equivariantization by that
involution, or replacing stabilizer actions by ordinary characters of D8,
would introduce an unproved categorical premise.

A remaining direction is the dimension-four algebra 1+h+Y in the integral
TY(V4) subcategory of R9_2_1975 (Y has dimension two). Its existence depends
on the actual TY associator and module structure, not only its underlying
object. This continuation has not established that such an algebra is forced
or that its Morita dual is excluded. It therefore does not turn the surviving
D8 alternatives into exclusions.

Consequently this continuation changes exactly one status: R9_2_1848 becomes
modelled, with a unitary model. R9_2_1975 remains unresolved.

## Final forced-associator check for R9_2_1975

`1975_FORCED_ASSOCIATOR.md` verifies that the new TY-origin D8 obstruction
also applies to this source: its left TY module has distinct stabilizers
{1,b7} and {1,b6}, so the same nonalternating bicharacter and class-2
rotation associator are forced. However, all three remaining dual types
have identity quotient action and lack the forbidden rotation/reflection
relation. The stronger check of all 64 cyclic bimodule-stabilizer relations
in each representative passes for both signs of tau. Thus there are
**zero additional exclusions**, and the three-type necessary frontier for
R9_2_1975 remains unchanged. Replay `check_1975_forced_associator.py` against
the bundled `1975_associator_inputs.json`; its receipt is
`1975_forced_associator_certificate.json`.

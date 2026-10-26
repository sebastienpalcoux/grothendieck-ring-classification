# Independent positive-model audit: rank twelve, multiplicity one

## Conclusion

I found no incorrect categorical realization among the first round's 127
positive based rings. The independent binding replay checks all 381 stored
full tensor identifications, and separately accounts for the 21 explicit
Liptrap constructions, for 402 accepted model records in total.

This conclusion does not mean that the categorical literature was formally
verified by a computer. The precise dependencies reviewed are below. The
newly identified ordinary representation model R12_1_541 corrects an omission
of the bounded model search, not a false first-round positive or exclusion.

## Deligne products and standard categories

The pointed list consists of the five groups of order twelve: C12,
C6×C2, D12, Dic3 and A4. The quantum-group entries are the standard unitary
SU(2)11 and even subcategories PSU(2)22 and PSU(2)23. The ordinary dihedral
and dicyclic entries are genuine finite-group representation categories.
TY(C11) uses its standard nondegenerate cyclic bicharacter and positive tau.
The accepted rank-two, rank-four and rank-six factors are retained from the
existing project catalogue; they are actual categories, not necessary-test
passes. In particular Haagerup H3 is the known subfactor category and the
non-self-dual Ising/SO(5) zests are established unitary constructions.

For the half even-metaplectic model R12_1_10, I checked the N=28 case against
Gustafson–Rowell–Ruan Section 3.3. The four invertibles, six X simples and
two V simples form a closed subcategory, of dimension 56. All are self-dual
in the N≡0 mod4 regime. Its two relevant order-two currents have twist ±1;
the adopted h·g current is always a boson. This is not an N≡2 mod4 formula
silently reused in the wrong regime. The odd SO(17)2 constructor agrees with
the four standard fusion formulas of Section 3.1.

## Actual equivariant actions

Pointed actions are genuine strict automorphisms of the explicit finite
group, hence strict unitary tensor actions on the untwisted pointed
category. Orthogonal TY involutions preserve every standard TY associator
coefficient. The functor has identity tensorator and squares strictly to
the identity. Either coherence on its square is permitted: +1 on all
objects, or +1 on invertibles and −1 on the TY-odd simple. The latter is a
monoidal natural automorphism because of the TY grading, and is invariant
under the involution. The action pentagon therefore holds. In the odd
choice, the two equivariant structures on m have eigenvalues ±i. The
encoded Fourier formula includes this extra phase correctly. A permutation
of the fusion rule alone has not been substituted for such an action.

This agrees with the explicit orthogonal action in Gelaki–Naidu–Nikshych,
Proposition 4.8, together with the displayed coherent square modification.

## C2 zests

The stored 138 C2-zest alternatives were checked for all grading channels,
neutrality, order two, and their specified categorical lift family.

- On braided standard bases the lift is canonical.
- On a product with an otherwise unbraided factor, the sampler restricts to
  the specified braided left-factor current. The exceptions allowed as
  fully braided right factors really are braided categories (ordinary
  representations, pointed products and the indicated quantum categories).
- On an Ising graded pullback the selected current is exactly (fermion,1).
  Restriction of its product half-braiding provides its lift even when the
  other factor is unbraided.
- On the metaplectic-character crossed product the selected current is the
  canonical Rep(C2) boson, fixed by the strict crossing action.

All these chosen order-two lifts have self-braiding +1 or −1, rather than
an unrecognized semionic value. In a compatible normalization the cocycle
is h^(ab), with scalar correction 1 in the bosonic case and i^(abc) in the
fermionic case. Its only nontrivial coboundary value is −1 at (1,1,1,1),
which cancels the fermionic crossing sign. This satisfies associative
zesting Definition 3.2 and Proposition 3.4, and preserves unitarity.

The discovery condition h²=1 was stronger than required. See NEW_MODELS.md
for the corrected general construction and its one new exact hit.

## Graded pullbacks and character crossed products

Matching C2 degrees in Ising⊠B gives a full fusion subcategory, closed under
duality, with exactly twelve simples when B has four simples in each
graded component. The twenty-four actually used rank-eight B factors were
traced to their current project constructions. The less elementary factors
R8_1_6,7,11,14,25,42 have explicit categorical constructions in rank8.tex:
bosonic all-module quotient, central square-root extension, and coherent
ordinary/pseudo-PSU flip extensions. Their unitary existence uses an actual
central lift and a unit-modulus correction of the C2 obstruction. The pseudo
flip is supported by an actual tensorator and coherent-square certificate;
it is not merely the visible x↔x* ring symmetry. The inputs of the report's
pullbacks do not include the more delicate rank-eight near-group orbifolds.

For TY(C5)^C2, multiplication of the equivariance map by −1 precisely on
the TY-odd summand is a strict tensor involution. The grading character is
monoidal, commutes with the existing action, and squares to one. It fixes
the canonical Rep(C2) subcategory and its central lift. Thus the associated
crossed product and subsequent specified bosonic zests exist categorically.

## Liptrap reconstruction and unitarity

Liptrap Theorem 4 and Lemma 5.4 reconstruct a fusion system from the
retained uberderivation. I compared the component formulas in the paper
with the code: left/right translations, involution, quasisymmetry,
biderivation, tau normalization and the gamma formula agree.

Every chi and upsilon value is a root of unity. Tau has constant modulus
1/sqrt(|H|), including the two cases R12_1_581 and R12_1_617 where its phase
varies and the modulus of the stored exponent system is 432. Consequently
all scalar recoupling matrices obtained from Lemma 5.4 have modulus one.
The only nonscalar matrices are the coset gamma matrices of Lemma 5.1.
The checker tests their complete exact cyclotomic row orthogonality,
including every coset pair and lord. With the normalization 1/sqrt(|H|)
these are unitary. Taking the decomposition bases orthonormal therefore
gives a unitary fusion category. A complex pentagon solution was not simply
declared unitary without checking its nonscalar blocks.

## Twisted C2 group-theoretical models

I independently derived the phase equations using associator omega(x,y,z)
on Vec_G^omega. They match the implementation:

L_x+L_sx+omega(s,s,x)=0,
R_x+R_xs−omega(x,s,s)=0,
L_x+R_sx−R_x−L_xs−omega(s,x,s)=0.

The balanced quotient identifies (x,y) with (xs,sy) with phase
omega(xs,s,y)+L_y−R_xs. Its left and right phases are respectively
L_x−omega(s,x,y) and omega(x,y,s)+R_y. These are exactly the encoded
formulas. All cocycle restrictions to H are trivial, all group quotients
are genuine homomorphisms, and all cocycle identities are tested. Double
cosets of size four have trivial stabilizer, while size-two cosets have
stabilizer C2 and exactly two projective characters. Thus the enumerated
simple bimodules are complete. The multiplicity trace is the normalized
character projection for L^(-1)R on the representative grade. It is not an
ad hoc fitted multiplication rule. These are duals at an actual separable
subgroup algebra in a unitary pointed category, hence unitary categories.

## Generalized Haagerup C6

Grossman–Izumi, Example 4.5 of arXiv:1501.07679v2, explicitly states the
existence of two actual C6 generalized Haagerup categories satisfying its
equations. The numerical qualification in that example concerns the
computed modular data, not the existence of the two categories. The stored
tensor is precisely the common standard generalized Haagerup tensor, and
its full twelve-object match is valid. No numerical center conjecture is
needed to realize R12_1_326.

## Verification boundaries and improvement

The first-round verify.py correctly checks tensor bindings and its stored
algebraic reconstruction identities. Some categorical premises (especially
the existence of accepted lower-rank factors and central lift families) are
documented mathematical inputs, rather than automatically derived by that
checker. The independent positive_binding_audit.json makes the 381+21
accounting explicit and checks the chosen lift families. A fully formal
verification of all cited categorical theorems remains outside its scope.

Primary references reviewed:

- https://arxiv.org/html/1002.3166v2 (Liptrap, Definition4.3, Theorem4,
  Lemmas5.1 and5.4).
- https://arxiv.org/pdf/2005.05544 (DGP, Definition3.2, Proposition3.4,
  Section3.4).
- https://arxiv.org/pdf/0905.3117 (GNN, Proposition4.1 and4.8).
- https://arxiv.org/pdf/1808.00698 (GRR, Sections3.1 and3.3).
- https://arxiv.org/html/1501.07679v2 (GI, Example4.5).
- Current project rank8.tex and its explicit central-lift/coherent-flip
  proof records, used only for their positive construction statements.

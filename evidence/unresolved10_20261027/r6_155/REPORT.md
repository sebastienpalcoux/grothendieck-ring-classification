# R6_4_155: individual theoretical retry, 27 October 2026

## Outcome

**Unresolved.** No general-complex exclusion and no categorical model were established in this pass. The rejected construction below is a rejection of a route, not of the ring. No published classification status was changed.

The source is the project at commit `6a426acf6465dd674351be92dcca41b72f371521`. Its tensor is the entry `R6_4_155` in `data/current_remaining_cases.py`, with compact-JSON SHA-256 `012ef716d19b96a2a800d7bcbb33f3ae5e99e3c6a223f6e14bcd20144d4072a3`.

## Exact structure and existing frontier

Write the basis as `1,h,g,hg,X,Y`, with invertible group V4, `hX=X`, `gX=Y`, and `X*=Y`. The nonpointed products are

\[
XY=1+h+4(X+Y),\qquad X^2=Y^2=g+hg+4(X+Y).
\]

Consequently `d=FPdim(X)=4+3sqrt(2)` and `D=FPdim(C)=72+48sqrt(2)`.

The existing sphericalization and Galois argument reduces arbitrary complex existence to a pseudo-unitary Galois representative; it does not assert unitarity. The prior center proof then forces

\[
Z(\mathcal C)\simeq \mathcal S\boxtimes\mathcal B,
\]

where S is a semion category, B is a rank-26 prime modular candidate, and the full center has rank 52 and exponent 24. The unique central lifts of h,g,hg have twists `-1,i,-i` after conjugation. Their mutual monodromy satisfies

\[
M_{h,g}=\theta_{hg}/(\theta_h\theta_g)=1.
\]

The rank-26 modular datum and all fusion coefficients have already been determined, but its categorical realization and the required algebra object have not. Ordinary/generalized indicators, odd/even cyclic Clifford constraints, low-dimensional braid-spectrum tests, and the rank-22 fermion module constraints previously passed. These are not new accomplishments of this pass. The precise old statements are in `manuscripts/rank6/papers/chapters/frontier_155*.tex`, `even_clifford_retry.tex`, and `fermion_azumaya_20261016.tex`.

## A new candidate route and its decisive obstruction

The four rank-nine targets have global dimension `2D=144+96sqrt(2)`. This suggests a fermionic relative product with an Ising category I. Let psi be its fermion. The specified central fermion h in C makes

\[
A=1\oplus(h\boxtimes\psi)
\]

a connected central Tannakian algebra in C boxtimes I, since the product of the two self-braidings is +1. Its module category E is a fusion category of dimension 2D. This is a valid conditional construction whenever C exists; it supplies no construction of C.

Its simple-object count can be obtained without any pentagon calculation. Tensoring by h boxtimes psi gives:

* four free pointed orbits, giving four objects of dimension 1;
* two free orbits from the pointed objects tensored with sigma, giving two objects of dimension sqrt(2);
* two free orbits involving X,Y and 1,psi, giving two objects of dimension d;
* the fixed objects X boxtimes sigma and Y boxtimes sigma, each splitting into two, giving four objects of dimension d/sqrt(2)=3+2sqrt(2).

The fixed-point splitting is justified by `H^2(C2,C*)=0`; the two projective stabilizer representations are one-dimensional. Thus E has rank 12. The sum of the squared displayed dimensions is 2D.

However **E cannot be Morita equivalent to any of the four rank-nine targets**. Indeed, in

\[
Z(\mathcal C\boxtimes\mathcal I)
 \simeq\mathcal S\boxtimes\mathcal B\boxtimes\mathcal I\boxtimes\mathcal I^{\rm rev},
\]

the algebra A lies entirely in B boxtimes I: h belongs to B because its monodromy with g is trivial. The center of the central quotient is the category of local A-modules in this product. The entire semion factor S is therefore unaffected and remains a nondegenerate pointed factor of Z(E). All four rank-nine targets have, by the previous pointed-center proof, at most sVec as their pointed central subcategory (the noncommutative target has only Vec). None permits a semion. Morita equivalence preserves the braided center, giving the contradiction.

This is a general pattern: a modular factor disjoint from a connected central condensation algebra survives in the center of the quotient. Dimension matching between the resulting category and a target cannot override this invariant. The argument uses standard central condensation and center formulas, as in Davydov--Muger--Nikshych--Ostrik, *The Witt group of non-degenerate braided fusion categories*, Section 3, arXiv:1009.2117.

## Applying a general obstruction to the reconstructed center

The LPR zero-spectrum criterion was applied to the **entire rank-26 reconstructed fusion ring**, rather than again to the original rank-six tensor. It found no exclusion. The complete exact scan took approximately 0.66 seconds. `zero_spectrum_receipt.json` records its input hash and the reindexing that moves the rank-26 unit from label 1 to label 0. The C++ source is the existing project implementation with its array capacity enlarged from 6 to 26; its support masks remain safe within 32-bit integers.

This extends checked coverage, but is not a categorical feasibility proof. It should not be advertised as a new theoretical criterion. The primary criterion is Liu--Palcoux--Ren, *Classification of Grothendieck rings of complex fusion categories of multiplicity one up to rank six*, arXiv:2010.10264v5, Theorem 2.14.

## Independent audit of the new rank-nine duality idea

At the root agent's request, this investigator independently checked the proposed D8 pointed-bimodule duality obstruction. Vainerman--Vallin, arXiv:1210.1732, Section 2.2.2 explicitly uses the convention `omega_op(s,t,u)=omega(s^-1,t^-1,u^-1)^-1`; after identifying the second factor via inversion, the stabilizer coboundary is precisely `p1*omega/p2*omega`. Their Section 3.1.1 gives `mu_op=(mu after swap)^-1`. Thus the swap/inverse convention in the new calculation has a primary-source justification.

A crucial finite-search issue was independently detected and corrected: restricting a cobounding 1-cochain to fourth roots is unjustified. A fourth-root-valued 2-cocycle evaluated twice on an involution can force an eighth-root value. Rechecking with eighth roots restores the rotation-duality branch. For all four H2 twists with zero D16-Schur component, precisely the two rotation representatives pass; with nonzero D16-Schur component, precisely the two representatives of the identity coset pass. Reflection shifts still fail. This agrees with the rank-nine investigator's independent correction. **The duality test alone excludes only reflection shifts.**

A subsequent independent audit accepts a different argument excluding the remaining rotation branch of R9_2_1975. Its obligatory distinguished central object restricts to `1+sum_q X_q`, while the rotation-duality condition forces the diagonal stabilizer commutator of two commuting even-V4 elements to be minus one. Their projective action requires even multiplicity for X_00, contradicting its multiplicity one. The complete audit, including the noncommutative formal-codegree normalization and the strict even-V4 check removing opposite-convention ambiguity, is in `R1975_INDEPENDENT_AUDIT.md`. Combined with the archived exhaustive source-to-Morita reductions and reflection exclusion, this excludes R9_2_1975. It does not resolve R6_4_155.

The further independent audit `GALOIS_FROBENIUS_FS2_AUDIT.md` accepts exclusions of R9_2_1607 and R9_2_1976. In their remaining zero-shift completions, the distinguished self-dual multiplicity-one summand of the canonical symmetric Frobenius algebra has restriction `1+sum_q X_q`; its symmetric pairing forces all four large indicators to be +1. The Morita-invariant weighted second indicator would then require four positive large indicators in the original source, whereas R1607 has only two self-dual large simples and R1976 has none. This successful argument is independent of the unsuccessful quadratic-sign conjecture recorded in `FS2_AUDIT.md`. R9_2_137 is not excluded by it.

## Literature check and exact remaining gap

Meng--Yu, *Classification of some Z/2Z x Z/2Z-quadratic fusion categories of rank 6*, arXiv:2608.06064v1, still includes this ring under the notation R'(4) among its remaining candidates. The arXiv record checked in this pass lists v1 (6 August 2026), and no new categorical realization or exclusion was obtained from the retrieved primary literature.

The unresolved problem is categorical: construct coherent associators for the displayed rank-six rules, or realize the forced rank-26 modular data together with the required connected algebra, or obstruct one of these structures. Matching dimensions, modular data, stabilizer cochains, or a related conditional fusion category does not fill that gap.

# Independent audit of the R928 pattern-40 obstruction

29 October 2026. The new obstruction to **pattern 40** is valid, conditional on the inherited positive-modular-factor reduction and the independently stated phase/matching premises. It does not exclude pattern 186 or the fusion ring R8_3_928.

## Scope and phase prerequisites

The six-dimensional block argument was independently checked in `audit_r928_six_dimensional_block.md`. Its selected branch has H twists zeta32^3 times (1,i,-1,-i), a bosonic vector f, and an outside-pair difference of twist zeta8^7. The known two-dimensional block on e=(B0+B1+B2+B3)/2 and W has S equal to the normalized two-by-two Hadamard matrix and twists (1,i). Its invariance follows directly from the known W column and S^2e=e; e is orthogonal to f. Thus both blocks can be removed simultaneously.

Removing these eight dimensions from the pattern-40 phase list, and normalizing t=theta/zeta24, leaves dimension15 and spectrum

    3:2, 9:2, 11:1, 12:4, 15:2, 17:1, 20:1, 23:2.

The independent checker reconstructs this subtraction from the full list. In the full representation the t=-1 eigenspace consists exactly of four A coordinates, all with S unit entry 1/(4 sqrt3). The check presupposes the established complete pattern-40 phase/matching reduction in `r928/PATTERN40_ADDENDUM.md`; it does not replace that reduction by a representation-spectrum assumption.

## Level reduction

Dong–Lin–Ng, arXiv:1201.6644v7, Theorem II(i),(ii), applies to every modular category and every modular representation; no unitarity assumption is imposed by that theorem. For the chosen lift, full t has order96, so the full representation factors through SL2(Z/96).

The complementary representation kills T^24. Under CRT, SL2(Z/96) is SL2(Z/32) times SL2(Z/3), and T^24 is (E12(24),1). Its cube is (E12(8),1). The reduction kernel from level32 to8 is

    K = {I+8M : M in Mat2(Z/4), tr(M)=0}.

It is the additive group sl2(Z/4), since 64=0 modulo32. The conjugates of E12(8) by the identity, S, and [[1,0],[1,1]] have respective directions E12, -E21, and -H+E12-E21. These form a basis of sl2(Z/4), so the normal closure contains every one of the 64 kernel elements. It is contained in K as well. Therefore the complement factors through SL2(Z/24). This argument does not infer its level merely from the order of its T matrix.

## Complete table validation and a two-line nonnegative certificate

I replayed `r155/level24/verify_level24_inputs.py`: it passes the concrete group, conjugacy-class, class-algebra, character-equation, orthogonality, T-spectrum, and central-sign checks for all30 irreducibles at level8 and all7 at level3. The 210 CRT products exhaust the level24 irreducibles. Character completeness follows because the distinct class-algebra characters exhaust its primitive one-dimensional eigenspaces; their positive degrees and unit norms fix the genuine irreducible-character normalization.

Both central signs are retained. Exactly12 irreducibles have spectra componentwise bounded by the target. Write m_(i,j) for their multiplicities using the frozen table indexing, and T_k for the target multiplicity at zeta24^k. Direct inspection of all12 spectra gives

    2 T20 - T23 - T11 + T17 = 2(m_(1,1)+m_(1,5)),
    2 T12 - T3 - T15 + T9 = 2(m_(1,2)+m_(1,5)).

For the target, the left sides are0 and6. Nonnegativity first gives m_(1,1)=m_(1,5)=0, then m_(1,2)=3. The representation (1,2) has dimension1 and t=-1; the relation (st)^3=s^2 forces s=-1. Thus there are three sign copies. This proof requires no search for irreducible decompositions. The independent checker verifies both identities separately on every compatible irreducible.

## Signed Galois contradiction and sign choices

Theorem II(iii),(iv) of Dong–Lin–Ng supplies

    G5 = sigma5(S) S^-1 = t^5 S t^77 S t^5 S^-1,

where sigma5 sends zeta96 to its fifth power and 5*77=1 modulo96. This word acts as +1 on every sign copy. Hence G5 has at least three fixed vectors in the t=-1 eigenspace.

The same theorem makes G5 a signed permutation and preserves this eigenspace. Since sigma5(sqrt3)=-sqrt3, the constant unit entries force G5=-P on its four coordinates, for some permutation P. A permutation on four elements has at most two even cycles, so -P has at most two fixed vectors. This contradicts the forced three.

The use of normalized t retains the anomaly: gamma=zeta24 and gamma^3=zeta8. Choosing this cube root is a legitimate modular lift. The opposite semion orientation is the complex conjugate branch; conjugation preserves the contradiction. No restriction on charge-conjugation signs of the complementary irreducibles has been introduced. In particular, none of the negative-central-sign summands was silently discarded.

The primary theorem was independently inspected at https://arxiv.org/pdf/1201.6644, page3, Theorem II. It supplies a modular-category obstruction. Applying the complete inherited positive-center pipeline to arbitrary complex categorifications still requires the project's separately established sphericalization/Galois gate; this new argument adds no assumption that every fusion category is pivotal or unitary.

## Replay

    python research-six/r155/level24/verify_level24_inputs.py
    python research-six/unified/audit_r928_pattern40.py

The first verifies the complete frozen tables, and the second verifies the independent block-spectrum subtraction, both linear certificates, the level-reduction kernel, and the final signed-permutation dimension bound. Neither uses an optimizer or a large computation.

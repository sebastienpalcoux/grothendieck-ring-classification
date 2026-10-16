# Sphericality and a Galois reduction for R8_2_630 and R8_2_671

**Scope:** necessary structural result only. No categorification or nonexistence decision follows from this note alone. The label HI6 refers only to the shared dimensions; the proof does not identify a hypothetical center with the center of a known HI(C6) category.

## Proposition

Every complex categorification of either source ring admits a spherical structure. Every spherical dimension character is in its Frobenius–Perron Galois orbit. In particular every categorification has a pseudo-unitary Galois conjugate.

## A spherical section

Both source tensors are self-dual. In the canonical sphericalization choose the positive-second-indicator lift of each simple object. Each lift is self-dual: duality preserves its nonzero spherical dimension, whereas the other lift has its negative. The signed quotient tensor T is consequently fully symmetric and associative, with the standard unit and duality, and

    |T_ij^k| <= N_ij^k,       T_ij^k = N_ij^k mod 2.

The odd-channel Frobenius–Schur parity theorem (Liu–Palcoux–Ren–Vercleyen, arXiv:2203.06522v5, Theorem 3.9) gives

    N_jj^i - T_jj^i = 0 mod 4.

Thus a coefficient one with a repeated label is fixed at +1; a repeated coefficient two is ±2; an all-distinct coefficient one is ±1. Every possible signed tensor is exhausted by these domains and associativity.

For R630, all coefficient-two triples have a repeated label. There are 27 Boolean signs. The complete ordered associativity equations reduce to 157 distinct integer equations in Boolean monomials. Exhaustive depth-first search visits 195 nodes and returns only the all-positive solution.

For R671, there are again 27 Boolean signs, and exactly one all-distinct coefficient-two triple. Its signed value must be one of -2,0,2. The three exhaustive branches respectively have 163,165,163 distinct associativity equations and visit 57,5,103 nodes. The first two branches have no solution; the third has only the all-positive Boolean solution.

The exact replay regenerates all domains and equations from the complete census tensors. It visits both values at every unassigned Boolean sign and rejects a branch only after an assigned associativity equation fails. It uses no numerical criterion, guessed gauge, timeout or optimizer.

Hence T=N in both cases. The selected lifts form a tensor-closed full fusion subcategory of the sphericalization, and the forgetful functor restricts to a tensor equivalence with the source category. Restriction of the spherical structure gives the asserted spherical structure.

## The dimension characters

The eight exact characters of each commutative rank-eight ring are given below in census order. Each displayed ± pair denotes two characters. The replay verifies all multiplication equations, all eight distinct characters, and the duality-aware formal codegrees. Eight distinct characters exhaust a commutative semisimple algebra of dimension eight.

For R630:

    (1,1,2±sqrt10,3±sqrt10,3±sqrt10,2±sqrt10,4±sqrt10,4±sqrt10),
    (1,-1,0,1,-1,0,0,0),
    (1,-1,1,-1,1,-1,0,0),
    (1,1,1,-1,-1,1,0,0),
    (1,-1,-2,-1,1,2,0,0),
    (1,1,0,1,1,0,-1±sqrt3,-1∓sqrt3).

For R671:

    (1,1,3±sqrt10,4±sqrt10,4±sqrt10,3±sqrt10,2±sqrt10,2±sqrt10),
    (1,-1,1,0,0,-1,0,0),
    (1,-1,-1,1,-1,1,0,0),
    (1,1,1,-1,-1,1,0,0),
    (1,-1,-1,-2,2,1,0,0),
    (1,1,-1,0,0,-1,1±sqrt3,1∓sqrt3).

In the corresponding order, the formal codegrees of either ring are

    120±36sqrt10, 4, 6, 6, 12, 12, 12.

Every character outside the first conjugate pair vanishes on a simple basis object. A spherical dimension character cannot vanish there. It therefore belongs to the FP pair. Extend the automorphism of Q(sqrt10) that makes this character positive to a field of definition of the spherical category. The resulting Galois conjugate has positive simple dimensions and is pseudo-unitary.

This last conclusion does not assert unitarizability.

## Replay

    python verify_hi6_pair_galois_pu.py --repo /absolute/path/to/repo
    python -O verify_hi6_pair_galois_pu.py --repo /absolute/path/to/repo

The script uses only the Python standard library. The source archive SHA256 is `35a8d69e9af8c873b3003890218a35b38b792abb89c19066f6705bf9c1c1d1ed`; source tensors are selected using the published multiplicity-two lexicographic ordering. Each resulting tensor digest is retained in the receipt.

# The forced central fermion of R941

The independently verified general Galois–pseudo-unitary gate allows passage to a pseudo-unitary categorification. The complete integer Gram/cubic calculation forces exactly one central simple G restricting to the source invertible g (source index 3). The central-orbit argument in `review/QUARTIC_CENTRAL_ORBITS.md` identifies G as an invertible of order two: the forgetful kernel is Vec, since the source is its own adjoint subcategory. The already verified full tensor-rotation domain forces the positive Frobenius–Schur indicator of g. Thus the pointed associator on this order-two subgroup is trivial, and the positive ribbon twist of its central lift is either +1 or -1.

If the twist were +1, this central pointed subcategory would be Tannakian Rep(C2). De-equivariantization would give a fusion category D with C=D^{C2}. The sign character acts freely on all eight source simples. For C2 equivariantization, a nonfixed base orbit has trivial stabilizer and gives a single simple fixed by the sign character; this is impossible. Every base simple is therefore fixed, has two one-dimensional projective equivariant structures (H2(C2,C*)=0), and gives precisely a pair interchanged by sign. D has rank four. Forgetting equivariant structures gives its based tensor by identifying each free g-pair and summing the source coefficients over target pairs. No braiding of C is assumed in this step.

`r941_fermionic.py` checks every choice of representatives, all associativity relations and the exact positive dimension homomorphism of that quotient. Its global dimension is

`72+48 sqrt(2)+40 sqrt(3)+28 sqrt(6)`.

This exceeds 72, whereas the pinned unrestricted rank-four theorem bounds the global dimension of every rank-four complex fusion category by `24+12 sqrt(3)<45`. The quotient also matches all 64 coefficients of the historical rank-four ring F_{6,19}; the receipt records the exact source-to-quotient permutation and source hashes. The Tannakian branch is consequently impossible. This use of the rank-four bound is confined to ordinary Tannakian de-equivariantization.

The remaining central lift has twist -1, so it is a fermion. For each distinguished object A_E in I(1), its twist is 1 and its monodromy with G equals chi_E(g)/dim(E), by the character formula for the distinguished S row. Balancing then gives

`theta(G A_E) = - chi_E(g)/dim(E)`.

The four scalar representations give +1 monodromy, while the two-dimensional representation gives -1. Exact source checks identify the translated low objects with canonical high columns 40,41,42,43,57, respectively. The first four have twist -1; the last has twist +1. Each occurs with multiplicity one in every one of the 343 complete integer Gram/cubic patterns.

`r941_rotation.py` adds these five exact twist moments and every fixed high multiplicity to the complete height-six rotation and partial STS system, for all 343 patterns. All other Frobenius–Schur indicator choices are re-excluded from the original complete exact ray receipt. Default execution only checks saved exact dual or primal certificates and never invokes a numerical optimizer. The final receipt states the exact finite-domain outcome.

No ordinary rank-four theorem is applied to the fermionic quotient. No splitting of the nonbraided source category as a Deligne product is inferred from a central pointed subcategory. A surviving finite moment system would remain necessary data, not a superfusion construction or an associator solution.

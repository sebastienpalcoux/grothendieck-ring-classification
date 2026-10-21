# The forced central fermion of R941

The independently verified general Galois–pseudo-unitary gate allows passage to a pseudo-unitary categorification. The complete integer Gram/cubic calculation forces exactly one central simple G restricting to the source invertible g (source index 3). The central-orbit argument in `review/QUARTIC_CENTRAL_ORBITS.md` identifies G as an invertible of order two: the forgetful kernel is Vec, since the source is its own adjoint subcategory. The already verified full tensor-rotation domain forces the positive Frobenius–Schur indicator of g. Thus the pointed associator on this order-two subgroup is trivial, and the positive ribbon twist of its central lift is either +1 or -1.

If the twist were +1, this central pointed subcategory would be Tannakian Rep(C2). De-equivariantization would give a fusion category D with C=D^{C2}. The sign character acts freely on all eight source simples. For C2 equivariantization, a nonfixed base orbit has trivial stabilizer and gives a single simple fixed by the sign character; this is impossible. Every base simple is therefore fixed, has two one-dimensional projective equivariant structures (H2(C2,C*)=0), and gives precisely a pair interchanged by sign. D has rank four. Forgetting equivariant structures gives its based tensor by identifying each free g-pair and summing the source coefficients over target pairs. No braiding of C is assumed in this step.

`r941_fermionic.py` checks every choice of representatives, all associativity relations and the exact positive dimension homomorphism of that quotient. Its global dimension is

`72+48 sqrt(2)+40 sqrt(3)+28 sqrt(6)`.

This exceeds 72, whereas the pinned unrestricted rank-four theorem bounds the global dimension of every rank-four complex fusion category by `24+12 sqrt(3)<45`. The quotient also matches all 64 coefficients of the historical rank-four ring F_{6,19}; the receipt records the exact source-to-quotient permutation and source hashes. The Tannakian branch is consequently impossible. This use of the rank-four bound is confined to ordinary Tannakian de-equivariantization.

The remaining central lift has twist -1, so it is a fermion. For each distinguished object A_E in I(1), its twist is 1 and its monodromy with G equals chi_E(g)/dim(E), by the character formula for the distinguished S row. Balancing then gives

`theta(G A_E) = - chi_E(g)/dim(E)`.

The four scalar representations give +1 monodromy, while the two-dimensional representation gives -1. Exact source checks identify the translated low objects with canonical high columns 40,41,42,43,57, respectively. The first four have twist -1; the last has twist +1. Each occurs with multiplicity one in every one of the 343 complete integer Gram/cubic patterns.

The initial unpaired height-six relaxation was stopped before completing its 343 fixed patterns and is explicitly superseded by the stronger correlated calculation below. Its exploratory script is not a completed certificate.

For an arbitrary central simple Z, write M_Z for its monodromy with G. Since G has order two, M_Z is +1 or -1. If M_Z=+1, balancing implies that tensoring by G exchanges two distinct simples with opposite twists. If M_Z=-1, G may fix Z, and its twist is unrestricted by this argument. For each of the fixed restriction types 0 through 39, write p_v for the number of positive-charge pairs and q_v for the number of negative-charge individual simples. Then 2p_v+q_v=m_v, with p_v,q_v nonnegative integers. No charge is assigned from the restriction vector alone. The five low objects and their five translates have charges +,+,+,+,-.

The known fermion S row is S_{G,Z}=M_Z d_Z. The distinguished row is S_{A_E,Z}=beta_E chi_E(FZ), where beta_E=D/(f_E dim(E)). Orthogonality with every distinguished row, which is different from G, yields

`sum_Z M_Z d_Z chi_E(FZ)=0`.

All relevant characters are real and distinguished objects are self-dual. Substituting q=m-2p and the known low/translated contributions gives exact linear equations in the p_v. `r941_charges.py` exhausts all 41,664 bounded charge assignments directly and independently by exact row reduction followed by 446 free-variable assignments. The two searches agree on 93 allocations supported on 68 of the original 343 patterns. These bounds are p_v between zero and floor(m_v/2), so no potential allocation is omitted.

The fermion–distinguished STS equation supplies the further identities

`sum_Z theta_Z M_Z d_Z chi_E(FZ) = -D chi_E(g)`.

Positive-charge pairs contribute zero to this odd moment, while negative-charge individuals contribute minus their ordinary twist moment. The five translated distinguished objects have the fixed twists already proved. `r941_paired_rotation.py` forms pair columns by adding the complete existing trace columns for theta and -theta, retaining every distinct pair moment type. Negative-charge simples retain the full individual trace domain. It imposes all pair and individual counts, the original joint tensor-rotation equations through height six, the distinguished partial STS equations, and all twenty rational-coordinate fermion–distinguished STS equations. Other Frobenius–Schur indicator choices are re-excluded from the original complete exact ray receipt. Every one of the 93 allocations receives an exact primal or Farkas certificate; default execution checks them without invoking a numerical optimizer. The result receipt gives the complete finite-domain outcome.

The actual categorical control `review/fermion_center_control.py/.json` uses Z(Ising)=Ising tensor Ising^rev and G=psi tensor 1. It contains both positive-charge opposite-twist pairs and negative-charge fixed simples. It verifies the full S-square and STS matrices and the three distinguished fermion-row identities in exact cyclotomic arithmetic. This controls the minus sign, dimension normalization, and distinction between fixed negative-charge simples and positive-charge pairs.

No ordinary rank-four theorem is applied to the fermionic quotient. No splitting of the nonbraided source category as a Deligne product is inferred from a central pointed subcategory. A surviving finite moment system would remain necessary data, not a superfusion construction or an associator solution.

The corrected complete paired campaign has 77 exact infeasibility certificates and 16 exact feasible nonnegative rational witnesses. The surviving allocations occur on 16 distinct original Gram patterns. It supplies no general exclusion of R941. The optional discovery accelerator selects an exact basis of augmented rows and completes rays to the universal column domain using zero-RHS count rows; every resulting certificate is replayed against the unchanged full operator by the canonical verifier.

The subsequent integer-count layer tests each of the sixteen surviving cones. Positive count equations supply finite exact upper bounds and forced-zero columns. The supported equations pass exact modular consistency tests at primes 2, 3, 5, 7, 11 and 13. A bounded integer search then produces twelve nonnegative integer witnesses, each verified against every original equation. The four remaining searches finish without an exact integer-feasibility decision; their numerical outcomes are not exclusion certificates. Default execution of `r941_integer_counts.py` repeats the exact bounds, modular tests and witness checks without running the bounded optimizer. Thus the completed attempt leaves twelve exact integer solutions of the necessary system and four unresolved integer-feasibility cases, with no categorical realization asserted.

The final additive permutation and fusion-trace gate is proved and replayed in `review/R941_FUSION_TRACE_REVIEW.md` and `verify_r941_fusion_traces.py`. The number of fixed simples of the fermion permutation must equal its spectral trace. Per-type parity and eligibility give `sum(q_j mod 2) <= P-N <= sum(q_j)`. This complete check retains 71 of the 93 charge allocations and removes allocations 4 and 86 from the sixteen correlated survivors. All 420 mixed fusion traces of distinguished degree at most six are also checked for every allocation, with an actual Z(Ising) integer-matrix control; they remove no further survivors. The final intersection has fourteen rational moment witnesses, eleven retaining exact integer witnesses, and three unresolved integer-feasibility cases. The earlier sixteen/twelve/four receipts remain valid for their explicitly weaker stages.

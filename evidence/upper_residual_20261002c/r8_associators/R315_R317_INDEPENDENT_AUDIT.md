# Independent audit: R8_2_315 and R8_2_317

Verdict: **approved, general complex fusion categories**.

The reduction to contradictory pointed associator classes is valid. Each rank-four subcategory has exactly the dimensions1 and1+sqrt(2), so the published Schopieray Lemma3.1 applies separately. The C2 cocycle classes±1 are separately Galois invariant. They concern the same ambient pointed subcategory, so separate Galois choices create no compatibility gap. The pseudo ring's negative sign was independently checked against Larson Proposition5.5 and Theorem5.8, Case1, in the preceding R312 audit.

The new ordinary-ring positive sign was independently audited as follows.

- FRS parity leaves exactly the negative-g indicator tuple(-1,+1,+1).
- Direct Python Cartesian low-column enumeration, bypassing the native Gram enumerator, reproduces precisely the three displayed low matrices.
- The high-column bounds are necessary consequences of the residual Gram factorization. All nonnegative integer restriction vectors inside its diagonal bounds are enumerated in reference Python mode. Nullspace and principal-inverse pruning are exact necessary PSD conditions. The integral quotient D/z follows because the modular formal codegree D^2/z^2 is integral. The d-number test for z follows from the modular formal-codegree d-number theorem and the fact that integrality of a square implies integrality of its square root.
- Ng–Schauenburg's spherical center identity applies to the canonical pseudo-unitary structure. The rational averages of higher indicators are bounded by their rotation-space dimensions using normalized Ramanujan sums; only orders3 and4 are used here. There is no unsupported integrality assertion for higher indicators.
- Bruillard–Ng–Rowell–Wang arXiv:1310.7050, Theorem3.9, applies to this spherical category. The global dimension8+4sqrt(2) has norm32, so its center twist orders have only prime2. The ten trace vectors cover orders1,2,4,8,16,32 and all larger powers. For orders at least64 every joint relative trace through height4 is zero. Thus32 is a finite trace box, not an assumed twist-order bound.
- Galois symmetry of the normalized modular S matrix gives a signed permutation of its columns. Applying the nontrivial field embedding to the zeroth row z/D pairs positive dimensions by z->abs(D z'/D'). The two count-balance equations therefore hold for every possible pseudo-unitary center. No assumption about its braiding beyond the standard modular center theorem is added.
- The three stored integer rays satisfy nonnegative products against every generated variable column. Their right-side products are-48,-12,-48. Fresh normal and optimized replays agree on all three system hashes and source witnesses.

The source-bound subring maps and their closure reproduce the stated common invertible7 in both census rings. Normal and optimized receipts are `psu_pointed_independent_normal.json` and `psu_pointed_independent_optimized.json`. No LP optimizer was invoked during replay. No mathematical gap remains.

Primary scope checks: published Schopieray DOI10.1112/jlms.12789 Lemma3.1; Larson arXiv:1401.1879 Proposition5.5/Theorem5.8; Ng–Schauenburg arXiv:math/0601012 (spherical center indicators and twist exponent); Bruillard–Ng–Rowell–Wang arXiv:1310.7050 Theorem3.9 and modular Galois symmetry; Ostrik arXiv:1309.4822 Section2 (induced unit and formal codegrees).

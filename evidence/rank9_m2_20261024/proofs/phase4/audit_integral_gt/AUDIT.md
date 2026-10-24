# Independent audit of the integral group-theoretical exclusions

**Verdict: PASS for the stated group-theoretical scope.** No mathematical gap was found in the completeness argument of `../integral/GROUP_THEORETICAL_OBSTRUCTIONS.md`. The new exclusions of group-theoretical categorifications of R9_2_12, R9_2_959 and R9_2_1965 are supported. The separately cited obstruction for R9_2_941 excludes even weakly group-theoretical categorifications. None of these conclusions excludes a general complex or unitary fusion categorification; all four general cases remain unresolved.

This audit reviews the categorical premises and finite-cohomological coverage, and adds independent finite checks. It is not merely a replay of previously accepted scalar data.

## 1. Completeness of the group and subgroup reduction

EGNO, Examples 9.7.2 and 9.7.4, give the required presentation of every group-theoretical category by a finite group G, a normalized associator class, and a subgroup H with a relative trivialization. Morita invariance of Frobenius–Perron dimension gives |G| equal to the dimension of the category. The identity double coset gives Rep(H); neither its character degrees nor its invertible group may be replaced by arbitrary projective data.

For a double-coset stabilizer K, all projective representation classes are obtained by the central characters of the kernel of a Schur cover. Characters with a given central character have squared degrees summing to |K|. The GAP routine uses precisely this decomposition. Choosing the classes independently for different double cosets enlarges the allowed family, so cannot lose a realizable ring. The preliminary bound |H| >= 6 is valid: [H:K] times any projective degree is at most |H|, since the degree is at most sqrt(|K|).

A fresh GAP run completed successfully. Its parsed output agrees exactly with the original output, including the full projective-profile cache:

| Group order | All groups | All subgroup conjugacy classes | Surviving presentations |
|---:|---:|---:|---:|
| 120 | 47 | 1431 | 2 |
| 168 | 57 | 1751 | 2 |

The survivors are S5 and A5×C2, each with H≅S3×C2, and the two S4 subgroup classes of PSL(2,7). No restriction to untwisted or sign-valued associators occurs in this reduction. The reliance on GAP's SmallGrp classification, exact subgroup algorithms, and Schur-cover/character algorithms is explicit; this audit does not reprove the classification of finite groups of these orders.

Artifacts: `replay_all_twist_skeleton.g`, `replay_all_twist_skeleton.log`, `replayed_all_twist_skeleton.jsonl`, and `independent_profile_and_ring_checks.json`.

## 2. Transfer coverage and the primitive test

The restriction/corestriction order is correct: corestriction after restriction on global cohomology multiplies by the subgroup index. Thus the admissible global kernel for the order-120 pairs has exponent dividing ten, and the kernel for the PSL(2,7) pair has exponent dividing seven. Restriction to a Sylow p-subgroup is injective on p-primary cohomology. A normalizer automorphism x↦x^a of Cp acts on H⁴(Cp,Z) by a². Consequently the stated C5:C4 and C7:C3 normalizer actions kill the five-primary part for S5 and the seven-primary part for PSL(2,7), respectively.

For the remaining two-torsion classes, the exact sequence with coefficient map C*→C*, z↦z², gives a lift to H³(G,F2). Alternatively one may lift the restriction to a Sylow group and then transfer: its index fifteen acts as one on a two-torsion class. This is a coverage theorem for every admissible global class, not an assumption that a chosen cocycle formula is general.

For A5×C2, conjugation by the order-three normalizer element leaves the transferred cohomology class unchanged. Therefore transfer of the norm b+n*b+n²*b equals transfer of b in F2 cohomology. Reducing the norm span modulo boundaries is sufficient; it need not retain all ten original basis vectors.

The new checker uses independent **highest-pivot** Gaussian elimination, whereas the search uses lowest-pivot elimination. It verifies the complete normalized bar-complex ranks, every selected cocycle, and independence modulo boundaries. The original basis generator is imported solely to reproduce the original class labels; its claimed dimensions and independence are not trusted.

| Sylow group | dim Z³ | dim B³ | dim H³(F2) | Norm-image dimension |
|---|---:|---:|---:|---:|
| D8 | 45 | 41 | 4 | not needed |
| C2³ | 49 | 39 | 10 | 4 |

For each group, all 216,000 Schreier identities for the 15-element coset transversal are checked, establishing the exact transfer input identities. The normalized H-cochain complex independently gives dim Z²=12 and dim B²=9, and verifies that x², xy, y² span H²(H,F2).

Most importantly, the independent checker decides all 32 relative-primitive questions directly **modulo four**, rather than rerunning the original modulo-eight solver. This is sufficient over C*: if δψ is sign-valued and H²(H,C*) has exponent two, then ψ⁴ is a coboundary; adjusting by the coboundary of a pointwise fourth root yields a μ4-valued primitive. At the mod-two stage, changing a representative by a two-coboundary can be lifted to an integral one-coboundary, so the eight H² representatives exhaust all liftability possibilities. Every successful μ4 primitive is checked on every normalized triple. All decisions agree: eight admissible S5 representatives and two admissible A5×C2 representatives.

For every retained relative pair and subgroup twist, the checker verifies the stabilizer two-cocycle identities and its projective character degrees. In the trivial V4 multiplier case it explicitly checks the even diagonal exponents needed by the constructor's integer division, and checks every one-dimensional projective character multiplication law. Thus the constructor's previously implicit even-parity condition holds for every actual retained input; there is no missing ζ16-valued character here.

Artifacts: `independent_finite_checks.py` and `independent_finite_checks.json`.

## 3. The A5×C2 five-primary part

This is a valid primary-decomposition argument, provided the word "relative" means the cohomology of the usual mapping cone. The relevant exact sequence contains

H²(G,C*) → H²(H,C*) → H³(G,H;C*) → H³(G,C*) → H³(H,C*).

These groups in the displayed positive degrees are finite here. Since H²(H,C*) has no five-primary part, the five-primary relative group maps isomorphically onto the five-primary global restriction kernel. For a fixed double-coset representative, the projective stabilizer multiplier is the usual transgression of the relative pair. Its formula is multiplicative in the associator and the relative cochain; gauge changes alter it by a two-coboundary. It therefore defines a homomorphism to H²(K,C*).

For K=V4, the target has order two. Every relative class of five-power order maps to zero. Adding a five-primary relative class consequently cannot change the projective degree packet at this double coset. Both possible H²(H,C*) choices have already been included for every two-primary relative class, and all have trivial V4 multiplier. This proves that the omitted five-primary associator representatives cannot restore the required rank-nine packet. No inference about their full fusion tensors is necessary.

This uses the general categorical multiplier, with consistent cocycle conventions. The explicit computational character formula only needs sign-valued associators for the enumerated two-primary representatives; one need not extend that particular sign-convention implementation to arbitrary fifth roots.

## 4. Remaining identifications and exclusions

For S5, the nontrivial element of H²(S3×C2,C*) extends from the Schur class of S5, detected by commuting disjoint transpositions with noncommuting lifts. A global two-cocycle changes the relative trivialization through a tensor autoequivalence of Vec_G^ω, so it does not change the based ring. Thus one subgroup-cohomology choice per global class suffices. The four rank-nine stored tensors each match all 729 source coefficients of R9_2_92 under their saved permutations. The categorical fusion-character formula used to generate them is the general formula independently derived and checked in phase three; the present audit additionally checks its new cochain and projective-character inputs.

A simple independent based-ring invariant separates this result from R9_2_12. The multisets of traces of left multiplication by basis elements are

- R9_2_12: [1,1,2,4,4,5,6,8,9];
- R9_2_92 and every rank-nine S5 output: [1,3,3,4,4,4,6,6,9].

Thus the exclusion does not depend on a potentially faulty negative result from a based-isomorphism search.

For R9_2_959, the identity-coset subcategory requires an embedded V4 of invertibles, whereas the ring's four invertibles form C4. The obstruction is immediate once the exhaustive presentation reduction is accepted.

For the two PSL(2,7) presentations, the Schur restriction is nontrivial for both S4 classes, as witnessed by commuting pairs with noncommuting lifts in the prior exact checker. Since both Schur multipliers have order two, restriction is onto, and both subgroup choices can be removed globally. The two untwisted models are R9_2_1557. Their number of self-dual basis elements is seven, whereas R9_2_1965 has five, which independently certifies nonisomorphism.

For R9_2_941, the ring has no proper nontrivial fusion subring and is nonpointed. Its exact identification with the published exotic dimension-504 ring supplies the failure to be a finite-group representation ring. ENO Proposition 9.11 applies to general complex weakly group-theoretical fusion categories, without a unitarity assumption, and excludes that class. This audit checked the theorem's precise statement; it does not introduce a new classification claim for arbitrary dimension-504 categories.

## 5. Record corrections: resolved

Both nonfatal presentation issues were corrected and independently checked on 2026-10-24:

1. In the original A5×C2 records, `psi_exponents_mod8` contains the last loop value, namely subgroup Schur twist 1, while the top-level tensor is copied from twist 0. Both tensors are preserved in `all_subgroup_twists`. This is a provenance ambiguity, not a wrong tensor or a missing case. The independent checker explicitly subtracts 4xy to recover the base cochain before checking both twists. The corrected records now explicitly set `psi_record_subgroup_Schur_twist`, `tensor_subgroup_Schur_twist`, and `base_psi_exponents_mod8`, and each model stores its own `psi_exponents_mod8`. The audit checked the complete cochain domains and the exact 4xy relation for every retained record and every subgroup twist, and checked that each top-level tensor and match list equals the twist-zero entry. The generator preserves these fields consistently.
2. The proof now explicitly distinguishes rank nine (9⁴=6,561) from rank twelve (12⁴=20,736). The implementation already checked rank⁴ equations and required no mathematical correction.

The lightweight correction receipt is `record_corrections_receipt.json`, which records current source hashes. All eight admissible S5 records and both admissible A5×C2 records pass, covering twelve per-twist models. There are no remaining record issues. Neither correction changes any mathematical conclusion. The precise accepted status is exclusion of group-theoretical categorifications for R9_2_12, R9_2_959, R9_2_1965, and exclusion of weakly group-theoretical categorifications for R9_2_941. General and unitary categorifiability remain unresolved for all four.

## Primary references checked

- Etingof–Gelaki–Nikshych–Ostrik, *Tensor Categories*, Examples 9.7.2 and 9.7.4, and the categorical Morita-equivalence discussion: https://math.mit.edu/~etingof/egnobookfinal.pdf.
- Etingof–Nikshych–Ostrik, *Weakly group-theoretical and solvable fusion categories*, Section 2.5 and Proposition 9.11: https://arxiv.org/pdf/0809.3031.
- Brown, *Cohomology of Groups*, Chapter III, for normalized bar complexes, transfer, and restriction. The restriction/corestriction and normalizer properties were also checked against Pevtsova–Swanson's primary group-cohomology lecture notes: https://courses.washington.edu/mnotes/groupcoho/notes.pdf.

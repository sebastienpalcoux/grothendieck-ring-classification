# Three commutative quadratic rank-nine cases: phase-four continuation

The ordinary complex categorifiability of `R9_2_137`, `R9_2_1607`, and `R9_2_1976` remains unresolved. This continuation proves a **new braided-only exclusion for all three** and strengthens the exact necessary-condition analysis of their centers. It produces no new ordinary categorification or general-complex exclusion.

## Accepted new scoped conclusion

`BRAIDED_OBSTRUCTION.md` proves a general criterion: a fusion ring with trivial universal grading, an involution g fixing a simple X, and nonintegral FPdim(X)/2 cannot have a braided categorification. It applies to all three rings with FPdim(X)=4+3√2. The proof works for arbitrary complex braided fusion categories, without pivotality, pseudo-unitarity, or unitarity assumptions. Its exact tensor witnesses and all 243 multiplicative dimension identities pass in `verify_braided_obstruction.py` and `braided_obstruction_certificate.json`.

| ID | General complex | Spherical | Pseudo-unitary | Unitary | Braided complex |
|---|---|---|---|---|---|
| R9_2_137 | unresolved | unresolved | unresolved | unresolved | excluded |
| R9_2_1607 | unresolved | unresolved | unresolved | unresolved | excluded |
| R9_2_1976 | unresolved | unresolved | unresolved | unresolved | excluded |

## Complete complex-character refinement

Earlier labelled S tests used only self-dual real characters in the quadratic FP field. The new `complex_low_frames.py` includes **all nine characters**, including the complex conjugate pairs of values in Q(√2,i) for 1607 and 1976. It checks every character multiplication identity exactly, and enumerates all possible restrictions of the nine distinct distinguished simples in I(1), subject to:

- the exhaustive previously audited restriction-column domain;
- exact formal-codegree dimensions;
- duality of character labels and restrictions;
- the previously proved Galois-unit restriction vector;
- every pairwise modular S-symmetry equation over Q(√2,i);
- entrywise induction-Gram bounds and the exact first Gram row.

The enumeration finishes, without a time limit being reached:

| Ring | Labelled frames | Distinct unlabelled frames |
|---|---:|---:|
| R9_2_137 | 172 | 43 |
| R9_2_1607 | 36 | 7 |
| R9_2_1976 | 108 | 19 |

A surviving frame is only a necessary-condition object. It is not a categorical model. The finite enumeration is a research refinement, not an exclusion certificate.

`frame_moment_test.py` then conditions the audited center moment system on individual low frames. For 1976 the first two frames admit exact integer separating rays, but frame 2 survives the numerical relaxation through height 6. Frame 0 of 137 and 1607 survives at height 3. In the latter statements “survives” means the numerical optimizer returned a feasible necessary-condition relaxation; no exact feasibility theorem or categorification follows. The records preserve the numerical equality residual and never promote this to classification authority.

## A tempting quantum-group model route ruled out theoretically

The common global dimension is D=144+96√2. This equals the global dimension of SU(3)_5: the usual Weyl-denominator formula gives

    3·8² / ((2 sin(π/8))⁴ (2 sin(2π/8))²)
    = 96 / (2-√2)² = 144+96√2.

This dimensional coincidence cannot give a model, even through a Morita equivalence. SU(3)_5 is modular and has the three distinct invertibles of highest weights (0,0),(5,0),(0,5). Its center is SU(3)_5 ⊠ SU(3)_5^rev and therefore has at least nine invertibles.

For any fusion category C, forgetting a central invertible gives a homomorphism Inv(Z(C))→Inv(C), whose kernel is the group of tensor automorphisms of id_C: a half-braiding on the unit is precisely such an automorphism. For these three rings U(C)=1, so this kernel is trivial. Thus Inv(Z(C)) injects into Inv(C)=V4 and cannot contain a subgroup of order nine. Morita equivalence preserves the braided center. Consequently none of the three rings is realized by a category Morita equivalent to SU(3)_5.

This is a rejection of a particular model family, not of categorifiability. It complements the braided obstruction: both the direct SU(3)_5 route and all its Morita variants fail for structural reasons.

## Limits and continuation targets

The three tensors share their dimension multiset and formal-codegree multiset but have different dualities. No based-ring isomorphism between them is asserted. Existing split-involution Morita computations lead back to each same ring on the forced branches; the other branch has repeated simple actions and does not determine a new dual ring.

A stronger argument would need, for example, a complete categorical construction with an exact tensor transport, an independently justified half-braiding/condensation theorem in the ordinary category, or an exhaustive obstruction to every surviving center branch. Based-ring commutativity, a feasible Gram frame, and a numerical relaxation do not supply those missing ingredients.

## Reproduction

Run from the research package root:

    python phase4/quadratic_comm/verify_braided_obstruction.py
    python phase4/quadratic_comm/complex_low_frames.py R9_2_137
    python phase4/quadratic_comm/complex_low_frames.py R9_2_1607
    python phase4/quadratic_comm/complex_low_frames.py R9_2_1976
    python phase4/quadratic_comm/frame_moment_test.py R9_2_137 3
    python phase4/quadratic_comm/frame_moment_test.py R9_2_1607 3
    python phase4/quadratic_comm/frame_moment_test.py R9_2_1976 6

Only new phase-four files were written. No previous evidence, ledger, manuscript, repository, or website was changed.

## Literature checked

- Drinfeld–Gelaki–Nikshych–Ostrik, *On braided fusion categories I*, arXiv:0906.0620v3. This supplies the arbitrary-category statements in the braided obstruction and the description of tensor automorphisms via universal grading. https://arxiv.org/pdf/0906.0620
- Gelaki–Nikshych, *Nilpotent fusion categories*, arXiv:math/0610726v2, Theorem 3.5, Corollary 3.7, Proposition 3.9. https://arxiv.org/pdf/math/0610726
- Coquereaux–Schieber, *Determination of quantum symmetries for higher ADE systems from the modular T matrix*, arXiv:hep-th/0203242. The SU(3) level-five exceptional quantum-symmetry route was examined; it does not overcome the center-invertible obstruction above. https://arxiv.org/pdf/hep-th/0203242
- Schopieray, *Categorification of integral group rings extended by one dimension*, arXiv:2208.07319. The two-dimension/near-group hypotheses do not apply directly: each of the present rings has three distinct FP dimensions 1,2,4+3√2. https://arxiv.org/abs/2208.07319

The former complex-exclusion count is unchanged by this branch. The only proposed ledger change is the braided scope of these three still-unresolved ordinary cases.

# Fresh pre-publication audit of the rank-eight continuation

Date: 2026-10-16 UTC (2026-10-17 in Asia/Shanghai).

This is a new AI review, not human verification and not Lean formalization. It is not a claim that every statement in the rank-eight manuscript has been independently proved. Existing evidence and manuscript files were left unchanged.

## Outcome

**Updated after the separate adversarial R24 bridge review: a concrete proof gap was identified, and the audit decision is to reopen R8_2_24.** The initial review below found no definite error and flagged the diagram bridge as uncertified. A subsequent independent index check confirms that the manuscript's cancellation of arbitrary decorated cubic phases is unsupported in its composition-dual frame. The proposed eight-slot replacement remains conditional and is not accepted as a completed repair. R24 must not be advertised as proved by either argument. This is a gap in the proof, not a counterexample to the nonexistence statement. The other reviewed cases have no definite blocker identified here.

The public presentation must describe the work as provisional AI-generated research. Neither a successful arithmetic replay nor this report establishes human verification of the new categorical arguments.

The most demanding residual review item is the paired-space diagram calculation in the R24 inner-square obstruction. Its scalar algebra and final projective argument are clear; its general pseudo-unitary scope depends on the explicitly stated pivotal-bend and tetrahedral slot identifications. The source comparisons establish compatibility, not an independent proof of every slot identification. **The extension of the particular EIP unitary identities to the manuscript's non-Hermitian paired frame remains a categorical bridge not independently certified by this audit.** Fuchs–Grøsfjeld supply an applicable general framework; they do not state this particular R24 extension. This distinction is essential: “no definite error found” does not mean “all new theorems guaranteed.”

## Material inspected

Manuscript files under `manuscripts/rank8/paper/`:

- `unified_20261016.tex`, including R37, R49, R170, HI(C6) dual, the four algebraic 2D2 exclusions, twisted half-braiding, R342, centralizer constructions, and the Fibonacci pair.
- `r24_inner_square.tex`, `r9_pointed_class2.tex`, `r18_center_trace.tex`, `r671_center_trace.tex`, `q630_weighted_indicator.tex`, and `hi6_pair_galois_pu.tex`.
- The corresponding bibliography in `rank8.tex`.

Evidence under `evidence/unified_20261016/`:

- `compression/CONDUCTOR_EQUALITY_LEMMA.md` and `compression/QUADRATIC_RESIDUE_SATURATION.md`.
- Rank-eight proof notes for R24, R37, R342, the HI(C6) dual, the pivotal odd-isotypic lemma, the signed saturated indicator lemma, the Q(sqrt(5)) arbitrary-root hull, and algebraic 2D2 rigidity.
- Code-level inspection of `verify_r24_projective_inner_square.py`, `verify_r671_center_trace.py`, `verify_r18_sts_moments.py`, `verify_hi6_pair_galois_pu.py`, `verify_fib_pair_theoretical.py`, and `verify_fib_character_parity.py`.

The parent review separately performs clean source reconstruction and normal/optimized stage replays. A subsequent coverage investigation found that the production rank-eight entrypoint dispatches to a bundled stage checker before its original 973-record loop. I therefore additionally performed the fresh full historical baseline replay described below; this is separate from the mathematical argument review.

## Fresh full baseline replay: coverage gap closed

The original complete checker is frozen in `evidence/upper_residual_20261002b/baseline_files/supplements/rank8/software/verify.py`, SHA-256 `1814a68e081e4b6e508a8a706e8e6ee9338b86550cc80b731c4749f6f5a4926e`. The current production entrypoint can return from a later-stage dispatch without reaching that full original loop. A normal/optimized stage PASS therefore did not by itself establish fresh replay of all original rank-eight certificates.

The audit reconstructed a separate scratch copy by reversing the unified, theoretical, stage-c, and stage-b transitions. Every complete parent ledger's canonical digest was checked. The pre-b rank-eight digest is `6717588bf6d1c2c9ece32e52eca2dd46fd81257b44f31d9bf3c75b854ebc415c`. The original source repository and its frozen evidence were not modified. Final overlay bytes were checked both immediately and in a later process; `write_bytes` was used after timestamp-preserving `copy2` caused the shared filesystem to restore stale content.

The external driver `work/prepublic_audit/run_rank8_full_baseline.py` imported the byte-identical original checker under a non-main module name and explicitly called its unchanged `main()`. **Normal Python was mandatory; optimization was disabled in the parent and children. No check or assertion was removed.** Instrumentation called the original tensor and certificate functions first and recorded only successful returns.

The full replay passed in 449.989 seconds:

| Baseline scope | Freshly checked |
|---|---:|
| Source tensors, in complete ledger order | 973 |
| Negative certificate applications | 832 |
| Positive records, with complete constructor tensor matches | 60 |
| Then-unresolved records, with no false decision attached | 81 |

The original signed-proof-tree and appendix subprocesses, complete counts, and exclusion-stage tally also passed. The baseline consists of 96 exact-multiplicity-one and 877 exact-multiplicity-two tensors.

Fresh receipt: `work/prepublic_audit/rank8_full_baseline/rank8_full_baseline_receipt.json`; log: `work/prepublic_audit/rank8_full_baseline/rank8_full_baseline.log`. The receipt lists all 973 successfully checked tensor IDs and the exact criterion totals.

A separate record-partition check in `work/prepublic_audit/rank8_full_baseline/current_record_coverage.json` establishes that the 892 baseline-decided records are unchanged and the 81 baseline-open records are exactly the disjoint later-stage transitions: 26 stage-b, 11 stage-c, 18 theoretical, and 26 unified. Their mathematical decisions still depend on the corresponding stage evidence and proof audit. In particular, this finite replay does **not** resolve the independently identified R24 categorical gap.

## 1. General scope: pivotality, Galois conjugation, and signs

The published Schopieray Lemma 3.1 was checked directly. Its conclusion is existence of a pseudo-unitary **Galois conjugate** for a two-dimension fusion ring. The old arXiv v1 says something stronger and is not the version to rely on. The manuscript uses the corrected published formulation, and applies the conjugation to the entire category when a subcategory, extension, or module must be transported with it.

For the HI6 pair, the sphericalization argument does not assume the desired pivotal structure on the original category. Self-duality of a chosen lift follows because duality preserves its nonzero spherical dimension, whereas the two lifts have opposite dimensions. Choosing the positive-second-indicator lift is legitimate. The signed tensor is associative and fully symmetric, with the correct absolute-value and parity bounds.

The extra repeated-index condition is justified by the odd-channel Frobenius–Schur theorem in the sphericalization: the number of negative-indicator constituents in a square has even multiplicity. Since that number is `(N-T)/2`, the condition is `N-T = 0 mod 4`. It is not an assumption that all dimension signs are positive. The Boolean solver generates all ordered associativity equations, branches on both signs, and rejects a partial assignment only after an equation is fully determined. The all-distinct coefficient two in R671 includes all three possibilities -2, 0, 2. Thus no negative or zero signed channel is silently removed from the domain.

Once T=N, the actual lifts are tensor-closed. This supplies the spherical structure rather than merely a signed based-ring character. The complete eight characters then separate the FP conjugate pair from the six characters with a zero simple value. A spherical dimension function cannot vanish on a simple, so the Galois reduction is valid.

The pivotal odd-isotypic lemma was also checked directly by taking the pivotal transpose of a palindromic tensor form. It requires no braiding. The adjoint word X Y X* has the sign of Y, because the pivotal compatibility `j_X* j_(X*)=id` cancels the outer forms. This supports the sign propagation used in R49, R9, and R671 after their pivotality gates.

## 2. Conductor equality and arbitrary twist orders

I rederived the equality refinement from the primitive-vector model in Schopieray's Lemma 4.1. For a nontrivial local character of conductor l^c, the compression has an orthogonal big-cell/small-cell decomposition. Its maximal singular subspace is generated by the stated F and G functions, both pullbacks from level l^c. An irreducible summand containing a nonzero equality vector therefore factors through that level. For a trivial local character, equality forces invariance under both upper and lower unipotents, hence the whole local group. Tensor-product singular values justify the global conductor statement. This works at the 2-primary conductor eight used in conductor forty; the proof does not silently assume an odd prime.

The primitive quadratic-residue refinement has the necessary Chinese-remainder Gauss-sum factor. Its conclusion restricts primitive-f twists; it does not incorrectly eliminate proper divisors of f.

The signed saturated-indicator identity was checked by following both Galois signs. With ell(z)=p_chi(z/D), one gets ell(z_pi)=epsilon chi ell(z), while z_pi=epsilon D/sigma(D) sigma(z). The signs cancel. Reindexing changes the twist exponent to the inverse residue, and inversion preserves a quadratic character. No involutivity of the Galois permutation is required.

The Q(sqrt(5)) two-moment hull is genuinely an arbitrary-root hull. For order 2^a 5^b m, the odd coprime factor scales both moments by mu(m)/phi(m), with the stated possible residue interchange. The remaining negative factors are included by the negative-half endpoints. Higher shared prime powers vanish in the required coordinates. For conductor forty, the nine-point unrestricted hull and seven-point saturated list distinguish rational dimension ratios from irrational ones and retain the proper-divisor twists.

## 3. R8_1_18: full STS and fourth moments

The full induction identity follows from the actual character-labelled I(1) summands, not an arbitrary assignment of formal codegrees. Set X=diag(1/f) C. The low block of STS is `X M X^t = X B^t`, and character orthogonality gives `X^(-t)=conj(C)`. The resulting `M=B^t conj(C)` is exactly the manuscript identity. The normalized S convention is consistent.

The cyclic Fourier argument uses positivity only after the pseudo-unitary reduction. The n-th trace has maximal modulus, forcing all I(a) twists to be n-th roots of the same indicator; the lower traces force mass D/n in each individual phase. For the C4 generator this gives the sharp multiplicity bound v_a<=1 by comparing the constant coefficients, uniformly over all four associator classes.

The code explicitly verifies the extra Q(zeta8) automorphism P on every source character. It includes source duality and quadratic transport in the full row orbit. A row orbit can have repeated actual central objects, but the Galois bijection equates their relative-moment histograms; using nonnegative real multiplicities is a relaxation and cannot create a false exclusion.

The Cauchy prime support is {2,5}. The thirteen moment triples are the fortieth-root triples plus zero, not an assertion that the exponent divides forty. If b>=2, an odd repeated factor survives all powers 1,2,4. If a>=4, the fourth power still has a factor four, so every relevant relative trace vanishes. This validates the all-order reduction. The fourth-indicator projection only uses rationality of the relative trace of a sum of fourth roots; it does not guess those indicators.

The low-frame enumeration preserves actual character reciprocity and duality. The high domain uses complete diagonal Gram bounds, full orbit subtraction, exact positive semidefiniteness, and the correct quadratic algebraic-integrality test via trace and norm. Classes 1 and 3 have the same allowed relative triples and are legitimately combined. I found no missing associator branch or unsupported root-order cutoff.

## 4. R8_1_9 and the conductor-forty exclusions

For R9, odd-cube signs reduce the pointed C4 associator classes to 0 and 2; the resulting fourth indicators are respectively +1 and -1. The class-two first two moments vanish on the order-eight phases. The class-zero domain retains the imaginary fourth-root phases through the (0,-1) moment. The Fourier bound concerns each actual phase and does not average those phases prematurely.

For R671, the transport `v -> v + B(A-10B/3)` is checked on the dimension pair and annihilates the other six characters. Integrality therefore forces 3|B. The positive sign choice is checked, including rejection when neither sign is nonnegative. The low frames use character reciprocity as well as dimensions; the high list subtracts the complete partner orbit before its PSD test. Because O_Q(sqrt10)=Z[sqrt10], the two coefficient divisibilities in D/z are the correct integrality condition. These are necessary conditions, not a claimed construction of a center.

For R630, the conductor-forty weighted third-indicator identity has the correct weights `(3,3,-4,-1,-1,-4,2,2)`. Only labels 3,4,5 have one-dimensional nonunit cubic invariant spaces. Thus the contradiction has coefficients 1,1,4 on three unit-modulus quantities. It does not assume third indicators are real. The inequality 4>1+1 closes that argument once the sphericality and saturation gates are supplied.

## 5. Fibonacci pair R190/R489

The lift argument genuinely treats both signed branches. When epsilon=1, duality exchanges the two signed nonconstant terms and forces their signs to agree. When epsilon=0 and the signs disagree, x has squared dimension one. The ratio from sphericalization is delta/f, because both the category dimension and the pulled-back source codegree double. The irreducible quartic and nonmonic primitive minimal polynomial exclude algebraic integrality. Hence the tensor-closed section and subsequent Galois reduction are justified.

The final obstruction uses actual character reciprocity rather than dimensions alone. The two g=-1 characters have equal codegree and dimension `1+phi*d`, forcing restriction `1+y` or `1+gy`. The third character takes equal values on both possibilities. Reciprocity then forces equal evaluation by the two first characters. The four-coordinate field independence forces equal multiplicities within both x and y pairs, whereas the y pair has total multiplicity three. The argument works with omega=i in the non-self-dual case: the codegree uses chi(b)chi(b*) and not an unjustified square.

## 6. R24 inner-square obstruction

The outer categorical reduction is valid: the odd invertible has square g, and its actual conjugation functor fixes neutral simple labels. This is an actual tensor autoequivalence with square Ad(g), not an inference of coherence from a ring automorphism.

The conductor-five identity forces the three second-indicator signs and forces the two ordinary cubic rotations to be identities. The source EIP identities are originally written in a unitary frame. Fuchs–Grøsfjeld explicitly provide the linear partial-dual/tetrahedral framework for pseudo-unitary fusion categories with their canonical spherical structure. Thus using that framework is a possible and relevant bridge; merely citing the unitary classification would not have sufficed.

I checked the paired matrices: outgoing and incoming actions must be inverse transposes, as the manuscript now says. The displayed K_H, K_J and E satisfy the respective loop/bend covariance relations and nondegeneracy forces both eigenlines. The selected diagonal EIP resolutions yield the three scalar equations when the stated dual-slot identification is substituted. The unit-channel term is 1/d. Both tube-character branches give nonzero yY and zZ. The final gauge argument is sound: an antidiagonal H action squares to a scalar; a diagonal one preserving the two nonzero coefficients has u^4=1 and again squares to a scalar. Ad(g)'s projective H action is nonscalar.

The exact verification boundary is:

| Step | What this audit establishes | What remains outside that check |
|---|---|---|
| General pivotal calculus | FG's cited hypotheses apply to the canonical spherical structure of a pseudo-unitary category, and its linear partial duals need not be Hermitian adjoints. | FG does not itself assert the particular EIP slot arrays or their simultaneous normalization here. |
| Composition-dual action | The inverse-transpose relation follows from invariance of the composition pairing. Given the displayed loop and bend matrices, their covariance identities and opposite-eigenline pairing are consistent. | A separate complete graphical derivation of the claimed defects `s_r`, `s_gr`, loop squares, and the simultaneous choice of all four bend matrices as E. |
| Tetrahedral slots | The stated index maps, zeros, sign flips, and dual-coefficient substitutions are algebraically consistent with the matrices. The manuscript's use of paired coefficients does not accidentally treat them as complex conjugates. | An independent derivation that the actual category supplies **all** these slot maps in the same frame, particularly the two D0 sign flips and cancellation of arbitrary decorated cubic phases. |
| Diagonal resolutions | The actual EIP p. 539 formulas were read. Substitution of the asserted paired slots gives the three displayed scalar identities, with the correct unit term `1/d`. Both tube branches yield the claimed nonzero products. | Derivation, using only the admitted pivotal moves, that the chosen EIP unitary contractions become exactly these composition-dual contractions with no additional phase or normalization factor. |
| Final obstruction | Conditional on those slots and resolutions, the two crossing cases force scalar square on H; the action of Ad(g) is nonscalar. This algebra is valid in both branches. | This cannot repair a missing categorical slot identity upstream. |

**Limit:** the portable verifier checks the finite substitutions after the pivotal diagrams have supplied those slots. It cannot prove their categorical origin. I compared the manuscript's explanation against the actual primary formulas and found no explicit inconsistency, but I did not independently derive the entire simultaneous diagram calculus from duality axioms. Consequently this audit supports the conditional algebra and the plausibility of the bridge, **not a claim that the bridge has been independently verified step by step**. This is a substantive review limitation, not evidence of a counterexample. Any public claim that R24's new general theorem has already received complete independent mathematical verification would exceed this audit.

**Subsequent adversarial finding, superseding the “no inconsistency found” statement above.** With right bends E on both opposite Hom spaces and outgoing decorated rotation Omega=diag(omega_0,omega_1), the paired left bends have forms E Omega and Omega^(-1) E. Thus their coefficients on outgoing k and incoming i have product `omega_k / omega_(1-i)`. The EIP primary proof's outgoing k and incoming i vertices really have opposite Hom variance. Its formula `omega_k / omega_i` is downstream of its unitary Frobenius basis with equal paired phases. At i=k the paired-frame ratio is not automatically one. Therefore the manuscript's two D0 sign flips, claimed because “i=k” and the phase is a cube, have not been justified. This is exactly the categorical origin that the finite slot verifier assumes rather than verifies.

A conditional replacement keeps all eight even D slots, with independent diagonal entries x,X,W,w, and avoids the problematic D flip entirely. Put S=xX+Ww. Direct symbolic summation of the proposed actual F-matrix column identities gives:

`2t^2+S+1/d=1`, `S+2zZ=1`, and `S+2yY=1`.

These imply `yY=zZ=t^2+1/(2d)`, nonzero for both real tube-character values of t. I independently checked those sums using the B/C index transports in EIP's main-symmetry lemma; the displayed source transports depend only on the ordinary H rotation, already equal to one, rather than the unknown J phases. The unit contraction `delta_(k,1-l)/d` was also derived directly from composition-dual bases and the two H bends, without a dagger. However, the needed simultaneous B/C transport and opposite transport were not fully verified in the proposed paired frame. In particular, EIP's crossing reverses the g-strand orientation, and compatibility with the chosen g evaluation, the surviving loop, and its contragredient factor must be established from the actual typed diagrams. The odd permutation p must not be commuted with c: the proposed inverse-coefficient calculation uses p after c, and that is a separate relation to prove. The replacement is therefore **not accepted as a complete proof**. The audit decision is to reopen R24 and retain this candidate only as conditional research material. See the separate R24 bridge audit for the typed candidate and precise remaining gate.

## 7. Morita, module, and construction arguments

R49 and R170: existence of the regular involution algebra is established before taking bimodules. R49 uses the forced positive indicator; R170 first cancels the pointed associator by the grading cocycle, which is legitimate because the indicated subgroup maps isomorphically to the grading group. The free noninvertible double orbit gives one simple of dimension 2d; the two pointed orbits give four invertibles. The resulting near-group alternatives C4+8 and C2^2+8 are exhaustive. The C4 terminal criterion is a separate rank-five dependency, referred to the parent cross-cutting audit rather than assumed newly verified here.

The four 2D2 exclusions use a particular module graph, not a classification of all abstract pseudo-unitary 2D2 categories. Schaumann's actual statements supply the module trace, double-adjoint compatibility and spherical dual. The algebraic path-space embedding uses dual bases and nondegenerate bilinear traces; no dagger is required. The polynomial-ideal argument includes both primitive rotation eigenvalues and all complex rotation-one solutions. Complex edge gauge takes them to the known self-adjoint base solution. Containment plus equality of all rooted-loop dimensions rules out additional higher-depth data. I checked the role of Morrison–Penneys Lemma 3.4 and Theorems 7.8–7.9 in that final step.

R314/R432: the label permutation becomes an actual tensor autoequivalence by transporting the right action through the regular left module equivalence. The projection of multiplication supplies the twisted half-braiding. Its support alternation contradicts naturality on r inside r^2. This argument does not smuggle in a central lift or assume F^2=id.

R342: a fixed simple forces the pointed associator to be trivial, so the algebra is actual. The reconstruction does not stop at commuting action matrices: it resolves the kernel by forced product coefficients and a spanning list of words. The general monoidal version of Kazhdan–Wenzl quoted in Feng–Ming–Rowell Theorem 5.1 has exactly the needed hypotheses. Restriction to the adjoint category removes the cocycle. The coherent-action uniqueness uses both the gauge kernel and Aut_tensor(Id)=1. Reflection uses the actual internal-end algebra 1+u. No pivotality premise is introduced. The lengthy integer reconstruction was inspected at the proof level; its exhaustive run is covered by the parent's clean replay.

R37: Grossman–Izumi–Snyder Theorem 4.1 actually gives the required known C4 graded extensions. Its character equations imply alpha_2(u)=alpha_2(v)=-1 times the corresponding unitary, so both identities extend correctly on the crossed-product implementer. The eight sectors are distinct by reciprocity and form a tensor-closed list. This establishes existence before tensor identification.

R535: the HI(C6) dual argument does not assume faithfulness of the seven-object module representation. Its three-dimensional kernel cannot contain a noncommutative matrix block, so commutativity follows. The missing character determination rules out an extra FP codegree by a Perron bound, not by uniqueness of the FP character alone. The center inventory used is the theorem-level dimension inventory for this known Morita class. Grossman–Izumi Example 4.5 labels some full modular-data entries conjectural, but the proof here does not use those conjectural entries. The published Lemma 3.5 and Theorem 3.9 supply the needed inventory. No conclusion about unrelated R630/R671 centers is inferred from it.

R820/R869: the actual near-group categories precede the centralizer construction. The Evans–Gannon statement following Conjecture 2 explicitly covers the finite odd-order cases through 13, including order five. The manuscript does not invoke the unproved arbitrary-order conjecture. The finite source identification and centralizer closure are distinct from the existence input. The published finite modular-data identification itself uses the authors' numerical/integrality argument; the project has not newly reconstructed all original associators.

## Primary sources checked directly

- Schopieray, published Lemma 3.1 and Theorem 1.1: https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/jlms.12789
- Schopieray, dimension-block Lemma 4.1 and its proof: https://arxiv.org/html/2609.35287
- Edie-Michell–Izumi–Penneys, published local generators and resolution formulas, especially pp. 539–540: https://ems.press/content/serial-article-files/51094
- Fuchs–Grøsfjeld, Lemma 3.13(ii), Proposition 3.22 and Corollary 4.9: https://arxiv.org/pdf/2106.16186
- Schaumann, Proposition 5.8, Theorem 4.5 and Proposition 5.10(iv): https://arxiv.org/pdf/1206.5716
- Morrison–Penneys, Lemma 3.4 and Theorems 7.8–7.9: https://arxiv.org/pdf/1406.3401
- Grossman–Izumi–Snyder, Theorem 4.1 and equations (3.10), (3.18): https://arxiv.org/pdf/2201.11901
- Grossman–Izumi, Lemma 3.5, Theorem 3.9, Example 4.5: https://ems.press/content/serial-article-files/36923?nt=1
- Evans–Gannon, the finite-case statement after Conjecture 2: https://arxiv.org/pdf/1208.1500
- Feng–Ming–Rowell, Theorem 5.1: https://arxiv.org/pdf/2202.00121
- Liu–Palcoux–Ren–Vercleyen, Theorem 3.9: https://arxiv.org/pdf/2203.06522

Local copies of Izumi's `3^n` paper and the EIP TeX source were also consulted to resolve formula and version numbering.

## Publication recommendation and remaining limits

Publishing corrected work as clearly identified provisional AI-generated research is consistent with this audit's outcome after R24 is reopened and all current counts and claims are adjusted. Do not describe this review, the previous independent AI passes, or the replay receipts as human verification. Do not describe the repository as Lean-formalized. Preserve the explicit open cases and the finite-band scope of every completeness claim.

The highest-priority expert-review targets are, in order:

1. **R24 Lemma `lem:2d2-no-inner-square`:** supply an independent labelled diagram derivation of the simultaneous paired frame, slot relations, and three resolutions. The conditional algebra is not the missing task; the category-to-slot bridge is.
2. **Algebraic 2D2 rigidity:** check the non-Hermitian module-trace/path-space construction and the passage from the exact low-degree ideal and complex edge gauge to equality of the full planar algebras. Polynomial exhaustion alone does not certify that categorical completeness step.
3. **R342 Morita reconstruction and coherent action:** check the faithful recovery of the dual category despite the action kernel, the applicability of the adjoint Kazhdan–Wenzl/gauge-kernel results, and the claim that the relevant coherent C2 action has a unique class. Matrix equalities alone do not establish those equivalences.
4. **The new conductor-equality and residue refinements:** this review rederived the local linear-algebra argument, but a second expert should verify the irreducible-factorization step and all prime-power edge cases. They support several ostensibly unrelated exclusions and therefore carry substantial shared dependence.
5. **General sphericalization gates for HI6 and the Fibonacci pair:** the finite signed-tensor domains were inspected, but the category-to-domain completeness and tensor-closed-section argument deserve expert attention in addition to replaying the finite solver.

These are ranked review priorities, not discovered counterexamples. They should not be silently converted into a claim of formal or human certification simply because the arithmetic suite passes.

This review concentrated on the latest rank-eight continuation and its principal dependencies. It did not independently reconstruct every older rank-eight classification decision, every original published associator, or the complete rank-five terminal obstruction. It also did not prove census completeness anew. Those are separate dependencies and should remain visible in the provenance and scope documentation.

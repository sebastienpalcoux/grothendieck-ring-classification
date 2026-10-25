# Independent audit: rank 9, 10 and 11, multiplicity one

Audit date: 2026-10-25. Repository: `grothendieck-ring-classification`, pinned commit `8014c749c17ddd2ad3d1b99a4359d49a8be921c5`. All paths below are relative to `/workspace/scratch/90f37cc83103/grothendieck-audit` unless explicitly absolute.

## Conclusion and boundary

**No confirmed false exclusion or false model was found in the material reviewed in this sub-audit.** In particular, no missing unitary-to-general-complex premise was found in the dimension-24 near-group classifications, no arbitrary-pivotality assumption was found in the late ordinary rank-10 exclusions, and the rank-10 conformal model uses an actual published conformal inclusion and algebra.

This is not a formal certification that every theorem in every imported source is correct. The distinction matters: fresh finite replays verify the specific integer/cochain/character identities, while categorical existence and impossibility continue to depend on the cited theorems and the manuscript arguments reviewed below. The final Chang–Chen–Xu superpentagon nonexistence calculation is imported from the literature and was not rerun in Mathematica/Magma. The team's rank-seven audit independently checked the inherited cyclic-isotypic and full-I(1) compression proofs; this sub-audit additionally reviewed their rank-11 adapters.

Current ledger scope: 142 rank-9 inputs (102 excluded, 40 realized), 194 rank-10 inputs (136 excluded, 58 realized), and 182 rank-11 inputs (155 excluded, 27 realized). Thus this assignment concerns 518 supplied tensors: 393 exclusions and 125 realization claims. These counts describe the supplied census, not an independently repeated enumeration of all based rings.

This sub-audit did not edit or publish source repository files. Fresh executions were made in copies under `/workspace/scratch/90f37cc83103/audit-20261025/high-m1-replay/` and `high-m1-full/`. Full package replays and the later rank-ten decisions have now been reconciled against all518 current IDs: all393 exclusions and125 realizations have passing finite-check coverage. The per-ID receipt records each route, source hash, proof-review scope and limitations.

## Findings requiring qualification, not classification changes

### A. Auxiliary R189 branching table mixes conventions

Severity: low, concrete auxiliary-data/transcription defect; **does not change categorifiability or the main model proof**. Case: `R10_1_189`.

Location: `evidence/unresolved_retry_20261024/proofs/unresolved11_retry_20261024/global/verify_r189_pieri_branching.py:32`, and its generated `r189_pieri_branching_receipt.json`.

Compared with the primary Böckenhauer–Evans table and the correct main `rank10/verify_conformal_model.py:17–28`, the independent Pieri table swaps rows1↔9 and4↔6 while leaving rows2,3,7,8 unchanged. It therefore mixes conventions instead of using a single relabeling of the cyclic generator: a generator change sending1 to9 would send2 to8, whereas this table keeps2 at2. Correct the auxiliary table to the main/primary-source convention or explicitly remove the unsupported cyclic labels.

The proof only uses the v² intersection vector `(1,0,...,0)` and v³ intersection vector supported on `{1,3,7,9}`. Both are unchanged by these particular row swaps; the actual main conformal construction and its1000-coefficient identification are unaffected. This is not a reason to withdraw the model. It is a reason to correct the auxiliary exported branching table before presenting it as independent full branching evidence.

### B. Literature computation remains an external dependency

Severity: audit limitation; no demonstrated error. Cases: `R10_1_152`, `R10_1_153`, `R10_1_179`.

Locations: `publications/rank9-rank10/paper/rank10_completion.tex:174–213`; `evidence/rank10_m1_exclusions_20261023/new/rank16_dual/PSEUDO_BRANCH_EXCLUSION.md:49–80`.

The final contradiction is the odd-evaluation, m-type rank-two superfusion rule with parity dimensions `(1,1)`. I downloaded and read the primary Chang–Chen–Xu arXiv v4 text, especially §2.2.2, §3, §3.1, and the paragraph distinguishing odd `(0,0)` solutions from physical locality. The source explicitly includes `(1,1)` in its finite superpentagon calculation and states that the only surviving odd-evaluation family is `(0,0)`. This is not an application of its conjectural unbounded classification. The F-symbol equations use complex gauge changes, include negative-dimensional solutions, and do not impose a unitary matrix condition as a replacement for the pentagon. I did not find the unitary/pivotal scope failure raised elsewhere by the user.

Nevertheless, no independent Gröbner calculation or explicit Nullstellensatz certificate is supplied by this audit. The manuscript already discloses this correctly at lines 210–213. Keep that disclosure. A successful project replay does not newly prove the external polynomial-system nonexistence theorem.

### C. New rank-11 scans inherit older proof obligations

Severity: cross-audit dependency; no demonstrated error.

Locations: `evidence/rank11_m1_20261023/work/rank11/criteria_audit/CRITERIA_AUDIT.md`, `run_compression.py`, `verify_cyclic_independent.py`.

The cyclic criterion has 66 witnesses and adds `R11_1_13`, `R11_1_71` beyond the initial arithmetic exclusions. Its finite checker verifies invertibility/order, the four left/right fixedness conditions, multiplicity, an exact Perron factor, and nonintegrality of the scaled dimension. That verifies the numerical hypothesis; it does not prove the inherited categorical cyclic-isotypic theorem. This theorem was handed to the rank-seven audit, which independently confirmed the actual separable cyclic algebra, stable isotypic bimodule, integral dual dimension, and Bézout step without a pivotal/PU premise.

The compression adapter's three hits (`R11_1_29`, `R11_1_47`, `R11_1_144`) already have arithmetic exclusions. It keeps the weaker sphericalization bound separate from the stronger bound, whose gate is weak integrality or a transitive invertible action proving two FP values. It does not reuse a rank-eight Wedderburn guard at rank eleven. The inherited full-I(1) theorem was independently reviewed by the rank-seven audit, including distinct induction constituents, cancellation of the representation-degree factor and the general sphericalization bound. Its removal would not change these three current statuses because of their overlapping arithmetic certificates. See the rank-seven report for that independent proof coverage; it was not performed twice here.

### D. Independent review is not the same as an independent implementation of every line

Severity: reporting limitation; all cases.

The fresh executions below rerun the repository's independently written checkers in a clean copy. They are new executions, but I did not write a third full implementation of each categorical constructor. The new negative-control scripts do independently invoke the exclusion functions against all current positive cases. No claim should say that all historical proof files or every external source has been formally verified, or that all 518 categorical decisions were established without trusting any literature theorem.

## Main manuscript and proof-unit coverage

The following table inventories all substantive units of the two current main publications, including their included files. “Reviewed” means mathematical reading and checking the indicated reasoning, not formal proof verification. Numerical checks are listed separately below.

| Unit and source location | Cases / scope | Review result and remaining dependency |
|---|---|---|
| `publications/rank9-rank10/paper/rank9-rank10.tex:44–110` | Scope and baseline criteria | Reviewed general-complex versus integral/spherical/PU distinctions. Casimir eigenvalues are representation-degree multiples of codegrees; rational scaling does not change the d-number property. Comm/noncomm distinction is explicit. Zero/one-spectrum and earlier criteria retain their external/lower-rank theorem dependencies. |
| Same, `:112–155` | Central restriction, Gram and S-reciprocity | Reviewed required unit multiplicity `dim(E)`, dimension `D/f_E`, Gram residual positivity, and the degree normalization of character reciprocity. Scalar specialization is used where degree is one. |
| Same, `:157–180` | Integral dimension-60 exclusions | Re-derived the first/second-moment Cauchy inequality and its positive-dimension hypotheses. It yields the stated bound on twist-one mass, not an unsupported finite conductor cutoff. |
| Same, `:182–209`; `work/rank9_bridge/proof.tex`; `work/general_signed/` | Signed sphericalization including `R9_1_41` | Reviewed oriented cyclic/dual sign orbits, dual-compatible gauge, triangle-equality deductions, exhaustive residual signs and scalar dimension inventories. Gauge-original tables give a spherical tensor section, rather than assuming the pivotality conjecture. For `R9_1_41`, the residual associativity equality forces all signs positive, after which all dimension candidates are excluded by exact codegree ratios/norms. |
| `publications/rank9-rank10/paper/structural_sections.tex:1–40` | `R10_1_72`, `R10_1_127` | Reviewed dimension-20 integral subcategory, involution algebra, pointed Morita reduction and nonabelian GTY stabilizer contradiction. Does not infer categorification from a module matrix. |
| Same, `:41–107` | `R10_1_83`, `R10_1_177` | Reviewed successive solvability/equivariantization reductions and the arbitrary-associator/coherence argument forcing commutativity. Exact finite cohomology classification remains a computational component. |
| Same, `:108–end`; `work/literature/gty_proof.md` | 14 GTY cases; excludes 118,122,180 | Reviewed Liptrap reduction. Positive phase solutions are accompanied by unitary Fourier blocks. Negative cases use integer relations valid for arbitrary nonzero complex variables, not failure of a root-of-unity search. All bicharacter pairs are covered. |
| `publications/rank9-rank10/paper/models_section.tex:1–end` | Established families; pointed actions; `R9_1_92`, `R9_1_117` | Reviewed distinction between known categories, action/algebra coherence, and full tensor identification. In particular the triality construction uses an existing nonregular extension and exact finite fusion completion. Baseline operation theorems are inherited, not reproved here. |
| `work/resolve_rank10_quadratic/model21.tex:1–end` | `R10_1_21` | Reviewed actual transparent boson and balanced tensor quotient. The sign in the left action matters. Re-derived that the split invertible squares to the unit, giving V4 rather than C4. |
| `work/resolve_small_models/triality_equivariant.tex`; `work/resolve_integral/TRIALITY_ACTIONS.md:1–301` | `R9_1_12`, `R9_1_108`; exclusion branch for62,87 | Reviewed neutral TY classification, isotropic stabilizers, rejection of Rep(Q8), S4 Brauer–Picard action, H2/H3 action data, coherent projective-module transport, and direct inner modification. The two positive actions have actual coherence; the exclusion argument covers associator twists instead of only strict label permutations. |
| `work/resolve_rank9_neargroup/NG_ACTIONS.tex:1–end` | Complete dimension-24 near-group branch | Reviewed the path from solvability to unitarizability before applying Izumi. The normalization argument includes tensorators; the ±W ambiguity is naturally trivial. D8 and Q8 square coherences give different large-simple duality. Primary source scopes checked as described below. |
| `work/resolve_rank9_integral/D48_EXCLUSIONS.tex:1–end` | `R9_1_62`, `R9_1_87` | Reviewed all three quotient profiles, the argument that the rank-nine quotient is multiplicity-free, exhaustive quotient completion, rank-six reduction, orthogonal-group obstruction, and characteristic central boson allowing return to the exhaustive near-group branch. No absence-from-catalogue inference is used. |
| `publications/rank9-rank10/paper/rank10_completion.tex:1–94`; `new/quadratic_obstructions/MORITA_REDUCTION.md` | 114,115,152,153,179 and positive control21 | Reviewed parity proof that h fixes each split module; complete module action; dimension bound33; four actual-entry parameters; all dual matrix candidates; associative completion of remaining16 products. The result is a necessary based ring, never treated as existence by itself. |
| Same, `:95–173`; `new/rank16_dual/RELATIVE_FACTORIZATION.md` | Shared-invertible relative factorization | Reviewed twisted regular bimodule argument. The unit summand of the twisted-central `1+f` object survives because f acts freely; uniqueness follows from trivial universal grading and simple cross products. This is a supplied argument for nontrivial factor intersection, not an invalid direct use of disjoint exact factorization. |
| Same, `:174–213` | Pseudo branch152,153,179 | Reviewed central order-two lift, inverse self-braidings, bosonic rank-two contradiction, and fermionic associated-superfusion reduction. Final published superpentagon computation remains external, as Finding B explains. |
| Same, `:215–305`; `new/rank16_dual/ORDINARY_DESCENT_AUDIT.md` | Ordinary branch114,115 | Reviewed spherical/Galois→PU→Morita-dual pivotal bridge before EO A.3. Reviewed lift of factor-swapping action to the product, descent through `1+(f,f)`, both algebra signs, and absence of additional coherence when U(B)=1. One sign gives multiplicity2, the other gives V4, ruling out both C4 targets. |
| Same, `:307–end` | Structural propositions on189 | Reviewed pointed associator/Galois-cycle argument and regular-algebra dual ring. These are necessary structural assertions and are not incorrectly used to exclude189. |
| `publications/rank9-rank10/paper/rank10_conformal_model.tex:1–end` | `R10_1_189`, accompanying rank14 category | Reviewed theorem, minimal-branching lemma and rank14 proposition. The vacuum algebra exists from the actual SU(4)6⊂SU(10)1 inclusion. Pieri products, conformal energies and ground-state branching give the needed Hom dimensions; FP dimension closes the product. The rank14 corollary uses an actual subalgebra and centralizer. Primary vacuum block checked. |
| `publications/rank11/paper/rank11.tex:41–203` | Rank11 statement and baseline inventory | Reviewed scope and per-input count boundary. Noncommutative cyclotomicity is tested on character traces through a separating center element, not arbitrary eigenvalues. Earlier theorem dependencies remain explicit. |
| Same, `:204–335` |25 standard/coherent models | Reviewed V4 Tannakian zesting, SU(2)6 spin-current tensorators and square coherence, cyclic twisted pointed actions, TY actions. No claim that a ring automorphism alone defines an action. |
| Same, `:336–377` | `R11_1_104` | Reviewed actual pointed 3-cocycle and subgroup algebra construction. Independent balanced-bimodule implementation rebuilt all1331 coefficients in a fresh execution. |
| Same, `:378–496` |59 nonintegral signed/scalar inventories | Reviewed completeness and general-to-spherical bridge. Six mixed-dimension40 branches are retained, not silently discarded by PU reduction. |
| Same, `:497–602` |34 lattice exclusions | Reviewed integer-span necessary condition for every spherical dimension character and exact separating linear functional. Negative dimensions do not invalidate the additive-group argument. |
| Same, `:603–677` |3,52,142,149 | Reviewed forced two restrictions and S reciprocity contradiction; directly checked algebra `(3+2sqrt2)(4-2sqrt2)=4+2sqrt2`. |
| Same, `:679–817` | `R11_1_179` | Reviewed integral Q8 Izumi tuple, quaternionic W, covariance on all Cuntz generators and W cubed=1. Does not invoke an irrational-only automorphism theorem. All fusion channels/duality accounted for. |
| Same, `:856–1040` |40,82, dimension120 | Reviewed forced central Rep(D10), de-equivariantization, C5 grading, every possible Rep(A4)-ring neutral category, arbitrary twisted Vec(A4) Morita class, and no5-torsion via Lagrangian orbit/stabilizer. The proof does not apply an untwisted BrPic computation to arbitrary twist. |
| Same, `:1041–1200` |153, using realized104 | Reviewed TY neutrality, S4 four-cycle orbit, coefficient module, vanishing H2 restriction and comparison of even-part duality. H3 changes associators rather than fusion multiplicities; reference104 has an actual model. |
| Counts, assignment, remaining, status index |518 input claims | Read as data/coverage statements. Independently reconciled every current source hash and status with fresh complete replays and the six late rank-ten transitions; no independent ring-enumeration claim is made here. |

## Fresh execution results

All listed fresh executions completed with exit code0. These include complete package replays and additional focused checks, separately from the parent's aggregate suite.

The clean rank9/10 package replay passed all27 stages in71.35 seconds and preserved all336 predecessor status/hash mappings. It covers233 predecessor exclusions and97 models; the five late rank-ten exclusions and the R189 construction were freshly checked separately, giving the current238 exclusions and98 models at ranks9/10. The clean rank11 normal-mode replay passed all25 stages in370.11 seconds and preserved all182 mappings, covering155 exclusions and27 models. A fresh per-ID reconciliation verifies that the only six rank9/10 changes are114,115,152,153,179 becoming excluded and189 becoming realized. Thus no current high-m1 ID is omitted.

The exact518-row coverage file is `/workspace/scratch/90f37cc83103/audit-20261025/high_m1-case-coverage.json`, generated by `high_m1_audit_checks.py --controls --coverage`. Raw complete replay reports are `high-m1-full/rank9_rank10_m1_20261023/verification_report.json` and `high-m1-full/rank11_m1_20261023/work/rank11/replay_logs/replay_report.json`. Replay completion itself does not discharge the external dependency in Finding B or remove the auxiliary defect in Finding A.

1. Rank11 selected constructors: 25 inputs, all1331 coefficients each. Independent `arithmetic/model_audit.py`: 68 construction records covering the25 selected inputs. Spin actions:1664 nonzero F equations and16 zero entries per action; twisted C16 actions:65,536 cocycle and4096 functor equations each; complete square coherence, units, object-orbit labels and tensor maps.
2. `R11_1_179`: quaternionic matrix/coherence checks, independent C3 character averaging,1331 coefficients and14,641 associativity equations.
3. `R11_1_104`: independent actual bimodules and balanced quotients;1,048,576 cocycle equations;29,440 bimodule-axiom triples;1452 intertwiner systems;1331 coefficients. This is materially stronger than a matched dimension profile or a guessed fusion tensor.
4. Rank11 signed/scalar replay:59 sign records,12 alternative signed-character inventories,59 original scalar inventories. All admissible signed tables gauge-original. The six mixed branches are exactly36,86,95,135,136,170. Four originals have no spherical character:2,51,124,147.
5. Rank11 lattice/reciprocity:34 records,44 separating functionals; all four two-character cases.
6. Dimension120 hypotheses for40 and82. C4 reduction, all128 normalized H2 cocycles and all6 four-cycle conjugacy cases; actual104 receipt required by153 checker.
7. `R10_1_189`: conformal-model verifier, independent Pieri/branching verifier and rank14 WZW verifier. All1000 input coefficients agree.
8. `R10_1_21`: exact balanced fixed-point calculation, all196 permutation-equivariant source products, full1000 coefficient map.
9. D8/Q8 near-group actions: all8/24 group automorphisms enumerated;2/6 eligible involutions respectively; exact Gaussian matrices, square coherence and complete tensors. Only12/108 occur. Triality equivariantization, subgroup audit, H2(S3,A), and dimension48 quotient/orthogonal checks pass.
10. Forced rank16 duals: regenerated module actions and12-dimensional commutants for21,114,115,152,153,179; re-enumerated bounded matrix candidates;240 products uniquely forced and16 completed by associativity in each case; all256 action identities and4096 associativity equations; relative-factorization input hypotheses checked on all6 tensors.
11. Additional pointed-action/bimodule checkers: C2 actions for rank9 cases1,47,63,98; S3 actions for rank10 cases10,61,76,84,106,109,133,158; S4 bimodule cases rank9_72 and92. Complete cochain/action/Hom-space/tensor checks pass. Dimension160 normal-form audit independently checks all four H3 invariant classes,65,536 pentagons and4096 reflection equations per class, together with source hypotheses for83,177.
12. GTY checks: all11 positive witnesses,1152 quasisymmetry/biderivation identities and8 nontrivial unitary F blocks per ring; negative witnesses cover all16/4/4 bicharacter pairs for118/122/180 over arbitrary complex unknowns.

### Known-realized negative controls

A new audit driver applied seven baseline exclusion functions to every currently realized rank9/10/11 m1 tensor: d-number, commutative cyclotomic, integral center divisibility, near-group, generalized-near-group, noncommutative integral center, and primitive codegree. The noncommutative function was applied only to noncommutative inputs; other functions retain their own documented guards.

Results: **125 realized rings,768 applicable criterion calls, zero false exclusions** (98 rank9/10 rings with605 calls;27 rank11 rings with163 calls). This is a useful regression control, not a proof of soundness for arbitrary input rings or every criterion family.

Machine receipts:

- `/workspace/scratch/90f37cc83103/audit-20261025/high_m1_positive_controls.json`
- `/workspace/scratch/90f37cc83103/audit-20261025/high_m1_rank9_rank10_positive_controls.json`
- `/workspace/scratch/90f37cc83103/audit-20261025/high_m1_all_positive_controls.json`
- `/workspace/scratch/90f37cc83103/audit-20261025/high_m1-case-coverage.json`
- `/workspace/scratch/90f37cc83103/audit-20261025/high_m1_commutant.log`
- `/workspace/scratch/90f37cc83103/audit-20261025/high_m1_subcategories.log`

## Primary literature checks performed directly

Downloaded primary PDFs and inspected the actual relevant statements and local proof context:

- Chang–Chen–Xu, arXiv:2208.02757v4: §3 finite odd-evaluation exclusion, general complex gauge equations, separation from conjectural global classification and physical locality. Final elimination not independently reproduced.
- Galindo–Hong–Rowell, arXiv:1105.5048: Theorem5.20 explicitly covers weakly group-theoretical fusion categories. This supplies unitarizability in the integral dimension24/48 branches after solvability.
- Reutter, arXiv:1906.09710v2: Theorems1–2 and Corollary3 cover tensor equivalences and natural-isomorphism coherence, not merely equivalence of underlying categories.
- Izumi, arXiv:1512.04288v2: Theorems1.1,4.9,6.1, Definition4.8 and Lemma6.13 cover the actual integral D8/Q8 tuples. The manuscript avoids the inapplicable irrational-only automorphism section. Checked the normal-form generator construction against the displayed absorption/Sg formulas.
- Nikshych–Riepel, arXiv:1309.5026: §9.1, Example9.3 and Remark9.4 support S4 BrPic for D8 and the absence of nonregular Q8 extension classes needed here.
- Etingof–Ostrik, arXiv:1801.04409: TheoremA.3 has the pivotal hypothesis and l>2; rank4 corresponds to l=3 and primitive16th-root parameter. The manuscript supplies pivotality first.
- Böckenhauer–Evans, arXiv:math/0006114: the displayed SU(4)6⊂SU(10)1 branching table gives vacuum000+060+202+222 and an actual conformal inclusion subfactor. It agrees with the main conformal verifier's branch convention. The independent Pieri verifier has the auxiliary mixed-convention defect documented in Finding A; all intersections used in the proof remain the same.

Primary PDFs/text extracts are in the audit output directory. Other standard theorems (ENO/EGNO, Ostrik induction and rank-two classification, Liptrap reconstruction, general extension theory, twisted Lagrangian classification, zesting) were reviewed as dependencies/application hypotheses, not reproved in full from their original papers in this sub-audit. No claim of a complete proof audit of those entire external manuscripts is justified.

## Code scrutiny and limitations

Read the key rank11 sign verifier and scalar verifier, including oriented support completeness, full gauge rank, associativity-derived deductions, all residual assignments, and scalar-character completeness via the common commutator kernel. Reviewed the distinction between scalar codegrees and noncommutative block degrees. Read model-audit spin, cyclic, TY, and V4-zest branches: units, actual tensorators, finite action coherence and complete invariant fusion-space labels are tested.

Read rank10 module-action/commutant/completion implementations against their proof: parameters are actual nonnegative integer entries, bound33 is justified by Perron dimensions rather than a search budget, propagation is a necessary upper/lower bound, and all remaining candidate tuples are enumerated. The rank16 tensor convention is the opposite bimodule convention and is explicitly preserved in later arguments.

Fresh constructor passes do not check each theorem about WZW categories, semisimple tensor reconstruction, or central condensation from scratch. No full pentagon solver was run on each positive ring. No independent enumeration of the source census was run. These are explicit boundaries, not evidence that a particular classification is wrong.

Recommended disposition for this portion of the audit: no status changes justified by this sub-audit; correct the concrete auxiliary branching-table defect in Finding A, retain the existing external-verification caveats, and do not advertise the result as a formal or exhaustive independent verification of every proof in the entire project. The shared cyclic/compression proof dependency has been reviewed by the rank-seven teammate.

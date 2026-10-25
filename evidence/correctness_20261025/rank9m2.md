# Independent rank-nine multiplicity-two audit

Audit target: `grothendieck-audit` at `8014c749`; current evidence is `evidence/rank9_m2_20261024`, current authority inside its archive is `phase5/results/ledger.json`. This audit does not edit the repository or publish results.

## Present conclusion

No incorrectly excluded or incorrectly modelled rank-nine M2 ring has been established by this review. This is **not an unconditional all-clear**: the finite replay had material coverage/packaging defects, some external existence computations remain literature dependencies, and the independent eight-bit R920 replay exceeded available memory (the exact pseudo-Boolean replay passed). The all-group GAP enumeration and cohomology calculations were ultimately repeated successfully. The current partition is 2,043 exclusions, 36 unitary models, four unresolved.

### Finding R9-A: the advertised replay overstates its scope (moderate, verification/documentation)

`evidence/rank9_m2_20261024/README.md:9` says `python3 verify.py` checks “Every accepted finite calculation”. In the archive, root `verify.py` runs only phase five by default; `--baseline` adds **only phase four**. `tools/research_continuation_20261024.py:99–111` runs phase four and root `verify.py --frontier`; thus the publication verifier does not recursively replay phases one through three. Phase-four `integral/verify_GT_records.py:1–7` expressly describes a stored-record replay; its assertions verify saved counts, dimension profiles and tensor transports, not a fresh all-group subgroup enumeration or fresh cohomology/relative-primitives search. This affects the advertised assurance for all accepted rows, and particularly the group-theoretical dependency of R9_2_12,959,1965.

This is not evidence those mathematical decisions are false. The narrower docstring in `tools/verify_research_revision.py:2–5` correctly disclaims fresh verification of every categorical exclusion.

### Finding R9-B: two required negative-subring certificates are omitted (moderate, reproducibility)

`phase3/audit_small_subrings/verify.py:41` loads `cert2.jsonl` and `cert3.jsonl`, but neither exists in the distributed replay archive. A clean `python3 phase3/verify_audit.py --fresh` stops with `FileNotFoundError: cert2.jsonl`. The omitted proofs cover these 12 rank-nine transfers:

- `R9_2_773,774,778,779,780,781,782,783,1260,1457` (small_subring_2).
- `R9_2_849,850` (small_subring_3).

The other 12 small-subring transfers use the included cert1.json. These are transfer dependencies, not necessarily each ring's only exclusion. Importantly, both omitted certificates were reconstructed successfully from the packaged source tensors and packaged rank-five engine in scratch: cert2 uses `pseudo_gate`, cert3 uses `signed_extension_positive`; discovery itself calls the exact verifier. The entire phase-three fresh suite then passed. Therefore this omission does **not** currently justify withdrawing these exclusions; package the two certificates and fix full replay wiring.

### Historical invalid proof is correctly withdrawn

The historical phase-one `work/verify_results.py` branch `excluded_lower_subring` checks closure/transport and absence from the positive registry, which cannot establish a negative categorical theorem. This is the already acknowledged half-E6 defect, not a newly discovered current exclusion error. The current rank-nine ledger has no `work/structural.json` accepted certificate and phase-three reconstructs an explicit negative registry excluding half-E6. All 26 historical withdrawn claims were checked by the fresh phase-three replay. Do not cite an unfiltered historical phase-one PASS as proof of current general exclusions.

## Fresh executions completed

1. **All 1,817 current exclusions whose first accepted certificate is in `work/`: PASS, zero failures, 131.5 seconds.** A separate audit driver replaces old first-proof bindings with the current ledger before calling the exact checker; eleven first bindings differ from the historical corpus. This avoids validating a withdrawn historical proof instead of the currently accepted alternative. Artifacts: `rank9-baseline-current.py`, `rank9-current-baseline-ids.json`, `rank9-current-baseline-results.json`, `rank9-current-baseline.log` in this audit directory.
2. **Phase three fresh suite after reconstructing cert2/3: PASS.** Checks 568 explicit-negative-subring transports, 23,328 coefficients of 32 phase-three models, new categorical premises' finite certificates, and withdrawal of 26 historical claims. Log: `r9phase3fresh/replay-after-reconstruction.log`. Original clean failure remains `r9phase3fresh/replay.log`.
3. **Additional phase-two scripts omitted by its main fresh dispatcher: PASS.** `verify_prime_descent.py`, `frobenius52.py`, `audit_morita48_anti.py`, `audit_neutral.py`. Log: `rank9m2-replay/additional-checks.log`.
4. **Phase-two signed exclusion verifier:** all nine signed nonzero-product exclusions passed independent completeness replays. Its sequential `--gates` run passed the first twelve gates, then was SIGKILLed entering R920. This is an interrupted computation, not a mathematical counterexample or successful replay. All remaining phase-two checks subsequently passed; R920 passed with the exact pseudo-Boolean backend. See execution updates.
5. Root reports current publication verifier PASS, including phase-four/five and auxiliary frontier. This child inspected the dispatch and checker scope; that root execution is not represented as an independent child rerun.

Current first-certificate inventory (disjoint baseline subtotal): 1,531 Casimir d-number; 55 integral Drinfeld; 119 complete oriented sphericalization; 48 cyclic integrality; five subring index; 19 zero/one-spectrum; three small-m near-group; three involution-module; six cyclotomic; eight low-induction; 13 finite involution-module; four noncommutative integral Drinfeld; three weighted induction. Total 1,817. A further 171 current first decisions use phase-three corrected subring transfer; the complete 568 transfer witnesses overlap other exclusions.

## Mathematical proof coverage

The main `publications/rank9-m2/paper/rank9-m2.tex` was reviewed throughout, together with the current model/exclusion tables. The substantive continuation claims were checked against their readable proof files; repeated historical audit prose was used as a dependency guide, not as independent proof. Review priorities were whether the construction exists, whether every necessary obstruction applies to arbitrary complex categories, and whether finite success is incorrectly promoted to categorical existence.

| Result/family | Concrete proof scope reviewed | Outcome/remaining dependency |
|---|---|---|
| Formal codegrees and noncommutative Drinfeld restrictions | Main §§2; baseline checker; representation-degree factor in Casimir eigenvalues and central multiplicities | No degree-one assumption incorrectly imposed on noncommutative cases found; current 1,817 first-proof replay passed |
| Complete signed reduction and Galois pseudo-unitarity gates | Phase2 signed THEOREM; real-character audit; quotient basis/duality, nonzero products, Galois global-dimension gate | General-to-positive reduction is explicit, not inferred solely from quadratic FP dimensions; all gates replayed, with the stated R920 backend limitation |
| Integral/quadratic center and neutral-block rays | Main induction discussion; phase3 center/Morita audit; phase2 theorem statements | Arithmetic d-number restriction derives from squared norms plus integral closure; discarded neutral blocks are a necessary relaxation; full phase2 center calculations passed |
| Galois-unit restriction: 114,128,1487,1635,1636,1959 | Main theorem and exact central-character/S-symmetry deduction | No extra source braiding assumed; independent phase3 algebraic replay passed |
| Forced symmetric category: 516 | Main proof; phase3 structural argument | Tannakian conclusion uses positive dimensions and twist-one central simples; phase3 finite replay passed |
| Folded SO(3): 920 | Complete phase2 R920_PROOF, including local presentation, odd-boundary retract, negligible ideal, central fermion contradiction | Specifically checked that morphism generation is not assumed. Primary MPS/Fendley–Krushkal/Goodman–Wenzl statements fetched and agree. General signed gate is essential |
| Prime descent: 907 | Complete prime_descent proof | Unique central lift and sequential equivariantization justified by trivial universal grading; fresh premise checker passed |
| Dimension52 rank-two component:1071,1724 | Complete frobenius52 proof | Neutral Rep(C13⋊C4) identification includes associator invariance and action cohomology, followed by complete rank-two module obstruction; fresh check passed |
| Solvable central invertibles:1356,1933 | Complete dimension96 reduction proof | General complex scope from p^a q^b solvability; no braiding assumed |
| Morita module obstructions:396,1265 | Full foundation discussion in phase3 center/Morita audit; independent finite anti-module checker | Rank-one pointed-module existence forces subgroup associator trivial; anti-module gauge domain finite and independently enumerated; extra anti-module replay passed |
| Hopf20:1225,1673 exclusion and965 model | Main proof and complete phase3 Hopf20 construction | Rank-one module forces a fiber functor; full semisimple Hopf20 classification is external. Model includes symmetric pairing, dual-Hopf convention, DR coherence and unitary Fourier transform; phase3 finite checks passed |
| Cyclic internal end:1025,1709,1759,1988 | Complete phase4 theorem/continuation | Actual internal end supplies algebra; cyclic stabilizer projective irreps are one dimensional; general complex scope |
| Dimension120 neutral A5:585,1303 | Main continuation/phase4 argument | Solvability contradiction, dimension60 WGT theorem, pointed Morita representative and pointedness of extensions all stated |
| Dimension120:12,959 | Complete phase5 THEORY | Fermion case treated via parity and slightly-degenerate theorem; WGT forced before all-twists GT exclusion used; dimension30 and solvable descents checked conceptually |
| Dimension504:941 | Complete phase5 EXCLUSION_THEOREM | Seven-row congruence reduction, Gram bounds and parity force dimension9 central simple. LPR simple-center theorem and ENO prime-power theorem checked directly in primary papers; no unitarity premise |
| Dimension168:1965 | Complete phase5 GENERAL_EXCLUSION | Central-C2 quotient independently obstructed by explicit negative Gram minor; scalar characters force central symmetric Rep(G); perfect order argument forces Lagrangian. GT all-twists finite dependencies were freshly replayed successfully |
| All-twists GT120/168 | Complete phase4 GROUP_THEORETICAL_OBSTRUCTIONS and source dispatcher | Exhaustive projective-degree relaxation, restriction/corestriction bounds, relative-cochain choices and odd-primary noncontribution reviewed. Saved-record check alone does not rerun these finite searches |
| Four unresolved rings:137,1607,1975,1976 | Main frontier and quadratic_frontier.tex | Scope remains unresolved; feasible rational necessary systems are not labelled categories. Lower-rank transfer and newer Clifford/cohomology dependencies require parent cross-audit |

## All 36 model existence inputs checked at construction-family level

- Ordinary finite-group models:369,812,813,936,2083. Existence is elementary; tensor identities are separate exact checks.
- Untwisted group-theoretical bimodules:1016,1557; actual subgroup algebra is separable, and bimodules require no central algebra premise.
- Izumi extraspecial near-group:1979. Primary arXiv:1512.04288 Theorem6.1 directly states unitary existence for extraspecial Q8 with multiplicity2; no converse extrapolation was used.
- D16 even part:1374 and Asaeda–Haagerup AH3:1372. Existence relies on their specified published categories, with exact tensors transported. Ancillary source data were not freshly redownloaded here.
- Products with half-E6:71,79,499,2020; fermionic zest:1218. Actual unitary half-E6 seed is used.
- Half-E6 shear:96,1266. Complete action construction reviewed: F² has tensorator (-1)^(hk), square coherences ±i are monoidal, and central-fermion anticommutation gives both duality variants. Fresh phase3 construction and independent checks passed.
- Relative-cocycle models:92,392,1246. Main formulas and relative-trivialization conditions reviewed; full phase3 regenerated construction/independent checks passed.
- Parity TY models:21,748,1211; Fib permutation pullback:1373. Coherent actions, not mere ring automorphisms, are specified.
- Central fermion quotient:515; generalized Moore–Read orbifold:389; ordinary half-E6 swap quotient:1983. Central lift/algebra hypotheses and actual action coherence are retained. Phase2 constructor replay passed.
- Pullback models:1396,1397. Complete PULLBACK_MODELS proof reviewed: solvability yields actual central descent of the LPR seed, uniqueness of central lifts preserves the action, and pulling back the resulting S3 action is legitimate. Projective traces are inherited from the known seed, not freely chosen.
- D4 triality:1857 and triality after Tannakian zest:2029. Actual Dynkin action and equivariant Tannakian gauge are specified; Schur–Zassenhaus supplies the latter. The primary zesting theorem was checked directly (2311.17255 Prop4.2).
- Cyclic TY orbifolds:746,1209. Complete central C3 condensation and inversion tensorator/square coherence reviewed; no vanishing-H4 shortcut supplies existence.
- Moore–Read order-four descent:1254. Complete explicit cover action, central algebra preservation, F²-to-K identification, and H³(C2,C8_3)=0/exact coherence correction reviewed. This is an actual action construction.
- Isotropic orbifold:1848. Izumi's construction hypotheses reduce correctly to C18 and H=C3; unitary near-group precursor existence is cited to Budinski2021. The external C18 polynomial/root-isolation computation is not packaged or freshly reconstructed. The primary thesis was subsequently recovered by the rank-eight auditor and inspected locally (printed pp.40–47): C18 has four listed solutions, n<=20 completeness/exactness is expressly asserted, and the polynomial/conjugate norm certification method is explained. This confirms the cited existence claim, but is not an independent replay of the omitted C18 polynomial/root-isolation certificates.

## External primary sources directly checked in this audit

- Izumi1512.04288v2: Theorem6.1 (unitary extraspecial near-group existence) and orbifold section located.
- MPS1501.06869v3: local Lemma2.2, Proposition7.1 and SO(3) presentation discussion. The ambient-generation gap is explicitly handled by the project's additional presentation argument.
- Fendley–Krushkal0806.3484v3: Lemma7.1 injectivity at the parameter, rather than a generic-only statement.
- Goodman–Wenzl math/0206301: Proposition2.1 negligible ideal generator. The project's even-parity argument is necessary because their Corollary3.4 is stated for odd ell.
- LPR2102.01663v4: Theorem5.1 applies to arbitrary nonpointed simple complex fusion categories.
- ENO0809.3031v2: Corollary7.2 has exactly the integral nondegenerate/prime-power hypothesis used for941.
- Galindo–Mora–Rowell2311.17255v2: Proposition4.2 supplies associative Tannakian zesting data.

## Commands and limitations

A complete accepted dependency replay needs a current-ledger baseline selection (provided audit driver), phase2 fresh criteria plus constructors and separately omitted prime/Frobenius/Morita-neutral checks, phase3 fresh after restoring the missing certs, phase4, phase5 and current frontier. Historical stages must be kept in separate clean extractions because their initial manifest check precedes regeneration and their old ledger counts are not current authority.

The mathematically substantive project arguments listed above were read/reasoned through; this is not a formal proof-assistant validation, fresh reconstruction of every cited category, or proof of correctness of all third-party solvers. Primary-source inspections and finite replay scopes are explicitly distinguished. No current status change is recommended solely from the packaging and replay-coverage findings.

## Execution/source update 1

- All remaining phase-two center, quadratic center, theory, swap, R920 source-tensor, extra model, neutral, dimension96, and Morita checks passed. All **14 phase-two constructors** were regenerated and their complete tensor identifications passed. See `r9phase2fresh/remaining-checks.log`.
- The independent 8-bit R920 gate also suffered SIGKILL in an isolated run. Parent confirmed cgroup OOM kills; this is a resource limitation, not a failed mathematical assertion. At this checkpoint a separate exact pseudo-Boolean replay was being attempted; its successful final outcome is recorded below and remains distinct from independent 8-bit completeness.
- Fresh S5 and A5xC2 cohomology-transfer searches and the distinct high-pivot independent finite checker passed: dimensions4 and10, respectively, and8/2 relative-admissible classes. The full GAP all-group run initially stopped due to missing `transgrp`, despite GAP returning0; completion-count assertions correctly caught it. The package was subsequently supplied; the completed final run is recorded below. Logs in `r9gtfresh/full-gt-replay.log`.
- Budinski primary source now inspected directly via `primary/budinski.txt`: printed pp.40–41 expressly include C18 in the exact n<=20 claim; pp.46–47 explain algebraic polynomial roots and conjugate-norm certification. No extension of a unitary classification to arbitrary original categories is used by model1848.

## Execution/source update 2

All 20 Galois-positive gates now freshly replayed: 19 passed the independent eight-bit associativity encoding; R920 passed exact pseudo-Boolean associativity completeness plus all algebraic branch checks in 3.0 seconds. That fallback uses the discovery encoding, so its receipt's inherited field `independent_completeness` must not be interpreted as an independent implementation. The receipt explicitly labels the backend distinction: `r9phase2fresh/gate-920-pb.json`. The other seven gates omitted after the interrupted run are in `r9phase2fresh/remaining-gates.json`; all pass.

The current accepted finite decisions now have a fresh route across baseline, phase-two, phase-three and root phase-four/five. Independent checking of all original categorical existence inputs remains distinct from replaying their finite tensor consequences. The relative-cocycle and ordinary-swap detailed module/action formulas were additionally read against their categorical arguments and freshly passing phase-three/phase-two tensor constructors; no sign/convention mismatch was identified.

## Final execution update

The full GAP enumeration completed after installing and explicitly loading TransGrp. Fresh totals agree exactly: all47 groups and1,431 subgroup conjugacy classes of order120 give two candidate presentations; all57 groups and1,751 subgroup classes of order168 give two. Full S5/A5xC2 relative-transfer searches and the independent high-pivot primitive checker passed. `verify_GT_records.py` then passed against these regenerated files. Final logs: `r9gtfresh/gap-transgrp-retry.log`, `r9gtfresh/full-gt-replay.log` (also preserves the initial dependency failure), `r9gtfresh/final-GT-check.log`. There is no longer an outstanding fresh GAP coverage limitation.

All seven baseline model tensors were also regenerated directly from their specified constructors; every source transport matched all729 coefficients. Evidence: `rank9m2-replay/baseline-models.json` and `.log`. Additionally, independent GAP ordinary-character multiplication on the actual groups PGL(2,7), PSL(2,8) and C19⋊C3 reproduced models369,936,2083; see `r9gtfresh/group-char-control-verification.json`.

Disjoint current decision coverage is **1,817 baseline +171 corrected subring first certificates +36 phase-two exclusions +9 phase-three exclusions +6 phase-four exclusions +4 phase-five exclusions =2,043**. Parent owns the current phase-four/five replay; this child supplied the broader dependencies and proof review. Model constructor coverage is **7 baseline +14 phase-two +11 phase-three +3 phase-four +1 phase-five =36**, alongside all current exact transports. This establishes the reported fresh computation coverage, not independent reconstruction of every literature seed's associators.

The review found no current general-complex exclusion using a unitary classification without a justified reduction, and no accepted model justified solely by an associative integer tensor or feasible numerical relaxation. It did find the two concrete reproducibility/documentation defects R9-A/B. Neither defect presently yields a counterexample to a current classification; B was repaired and replayed in scratch, and A was addressed by broader explicit auditing. The one resource-limited independent backend is R920; exact necessary-equation completeness itself passed under the alternative pseudo-Boolean encoding. No repository files were changed.

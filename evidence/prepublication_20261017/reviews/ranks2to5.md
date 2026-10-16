# Pre-publication audit: ranks 2–5 and shared foundations

Audit date: 2026-10-16. Audited repository baseline: `e6a36a6f247b2db05f5468ffd4be1752ff42f157` in `sebastienpalcoux/grothendieck-ring-classification`. This report records an adversarial AI review of the arguments and selected checker implementations. It is not human peer review, Lean formalization, or a proof that all possible errors have been eliminated.

## Outcome and release conditions

No substantive mathematical contradiction or missing hypothesis was found in the reviewed rank-two through rank-five core arguments. In particular, the review examined the unrestricted rank-three sphericality argument, the general signed/sphericalization reductions, rank-five inert-prime parity rigidity, and the cyclic-order-four near-group exclusion used again at rank eight. This conclusion is an assessment of the reviewed proofs, not a fresh full replay of every lower-rank certificate.

Two editorial errors were found in the rank-three manuscript. A more consequential publication/reproducibility mismatch was found in the compact rank-five supplement: its current dispatcher and main verifier still implement the former two-case frontier, while its README and reports describe the completed classification. Missing large replay inputs are explicitly disclosed by the rank-four and rank-five READMEs, but a public reader still needs an accessible, hash-identified way to obtain those inputs. These publication issues should be resolved or described prominently before presenting the public repository as a complete, directly reproducible release.

The parent audit is separately recovering full archives and arranging fresh full replays. Rank-four replay is assigned to `audit_rank6_public`; rank-five reconstruction/replay is assigned to `audit_rank7_public`. Their eventual reports must be consulted for those results. This document does not pre-empt them with an inferred PASS.

## Provenance and inspection coverage

The local `repo/` checkout initially contained only a partial lower-rank snapshot; the lower manuscript sources were present in the remote repository. The audit therefore fetched pinned copies into `work/prepublic_audit/lower_sources/`, preserving their repository paths. The absence of these files in the initial local mirror was not treated as their absence from GitHub. No frozen source or historical PDF was edited by this audit.

Substantive mathematical reading covered:

- `manuscripts/rank2.tex` and `manuscripts/rank3.tex` in full.
- Rank-four finite-paper sections on arithmetic, induction, signs, adjoint parity, signed cover, twist sectors, quadratic families, conductor-40 root length, nonselfdual cases, applications, and the statement/certification framework.
- Rank-four companion sections on two FP dimensions, nonselfdual pivotal categories, proper subrings, fixed invertibles, near-`S3` families, Fibonacci subrings, determinant/codegree bounds, quadratic characters, repeated and distinct quadratic factors, cubic codegrees and differences, uniform discriminant/root conclusions, and higher moments.
- Rank-five sections on the census contract, known criteria, quadratic parity, inert parity, finite relative traces, cyclic-four central support, automatic application, positive models, and the verification guide.
- Selected implementations: rank-four `proofs.py`, `signed.py`, `global_signed.py`, and `induction.py`; rank-five `proofs.py`, `signed.py`, `induction.py`, `quadratic_parity.py`, `inert_parity.py`, `higher_traces.py`, `cyclic_four.py`, and the current compact `unified.py`/`verify.py`.

An independent short integer enumeration reproduced the five tuples in the rank-three `b<50` reduction. Its result is saved as `work/prepublic_audit/rank3_arithmetic_check.json`. The exhaustive signed-cover enumeration, all low/high induction branches, the complete certificate streams, every positive associator, and census completeness proofs were not independently reconstructed by this subagent. The parent’s replay work addresses some of these computational limitations; categorical existence continues to depend on the cited constructions.

## Findings requiring action

### R3-E1 — Incorrect unit multiplicity in a displayed induction identity

Location: `manuscripts/rank3.tex:691`, Proposition `prop:near-group`, immediately before equation `eq:near-I1`.

Current text:

```tex
$FI(\one)=2\one\oplus Y\oplus mX$
```

Correct text:

```tex
$FI(\one)=3\one\oplus Y\oplus mX$
```

For the near-group fusion rules, the underlying object is
`1^2 + Y^2 + X^2 = 1 + 1 + (1+Y+mX)`. The subsequent restrictions `F(A)=1+tX` and `F(B)=1+Y+tX` in lines 694–696 already have the correct total of three units when the unit summand of `I(1)` is included. The downstream argument uses that correct decomposition. This is an editorial typo, not a reason to retract the exclusion.

### R3-E2 — Incorrect section reference for the indicator formula

Location: `manuscripts/rank3.tex:711`, same proposition. The text refers to the Ng–Schauenburg formula “in Section~3”. The relevant central moment formula is `eq:moments` in Section 4. Replace the hard-coded section reference with `\eqref{eq:moments}` (or the correct section reference). This has no mathematical effect.

### R5-R1 — Compact verifier remains at the former frontier

Locations in the pinned baseline:

- `supplements/rank5/software/unified.py:5` imports `cyclic_four, quadratic_parity`, without `inert_parity`.
- `unified.py:31–44` has no `inert_parity_spherical` branch; unsupported kinds fall to `verify_general`.
- `supplements/rank5/verify.py:77` records the two frontier tensors as `general='unresolved'`, with criterion `spherical_only`.
- `verify.py:85` requires exactly two frontier records at multiplicity 18.
- `verify.py:102` emits `complete_general_bound:17` and `first_general_frontier_multiplicity:18`.
- In contrast, `supplements/rank5/README.md` and the latest manuscript verification guide claim all 40,999 rings through multiplicity 20 have decisions, including general exclusions for both former frontier tensors.

The compact README already says large raw inputs are omitted; that disclosure alone does not explain that the exposed dispatcher itself predates the completed inert-prime integration. A fresh user cannot reproduce the completed claim by adding only the large tensor/certificate files to this code. Synchronize the compact scripts with the completed release and replay them, or label the code explicitly as a legacy excerpt and provide the complete current executable release. Do not manufacture a new PASS receipt from the old one.

This is a reproducibility/publication blocker if the repository is advertised as a complete runnable verifier. It does not by itself refute the mathematical inert-prime argument, nor demonstrate that the original complete ZIP was incorrect.

### R4/R5-R2 — Public accessibility of archival replay inputs

The rank-four README omits the 75,825,461-byte compressed certificate stream from its compact bundle and points to a user-supplied original archive. The rank-five README similarly names a full ZIP but omits the raw tensors/certificates from the compact supplement. Before public release, the user-facing page should identify which files are directly reproducible from GitHub and give a public retrieval route for the complete inputs, or clearly state that the full replay package is not included.

The original rank-four README also explicitly states that a fresh 889,530-record replay had not been carried out after its editorial/dispatcher revision. That historical statement must not be silently converted into a current verification claim: attach the new dated replay result once actually obtained.

## Mathematical audit details

### Shared categorical foundations and scope

The review paid particular attention to arguments that start with an arbitrary complex fusion category and later use positive dimensions. The manuscripts do not generally assume the unresolved universal pivotality conjecture. They pass to sphericalization and signed quotients, or prove the particular sphericality/positive-Galois reduction they need. The distinction between existence of a unitary categorification of a ring and every categorification being unitary is maintained.

Bartlett’s canonical sphericalization construction was checked against the primary paper: its simple lifts have dimensions with opposite signs, and the signed tensor coefficients are differences of lift multiplicities while the original coefficients are sums. The section argument is valid when a sign gauge makes the signed coefficients equal to the unsigned coefficients: the opposite lifts then have multiplicity zero, so the selected lifts form a tensor-equivalent spherical subcategory.

The formal-codegree divisibility applied to nonspherical categories is supported by Ostrik’s general Corollary 2.14; the field-of-dimensions inclusion is used only after passing to a spherical category, as required by Corollary 2.15. Center induction multiplicity statements use the appropriate commutative/one-dimensional-character conditions. The spherical Ng–Schauenburg indicator formula does not require pseudo-unitarity. Positivity arguments are obtained either from positive FP dimensions after a justified conjugation, or from squared real dimensions in the general signed argument.

The Cauchy theorem used to restrict primes in twist orders has the required spherical hypothesis. Applying it to the center does not change the relevant prime support because its global dimension is the square of that of the spherical category. The finite relative-trace method bounds the nonzero trace types needed at a fixed moment height; it does not incorrectly bound all possible twist orders by that height.

### Rank two

The signed sphericalization/norm comparison was read completely. The integrality comparison forces equality of the two quadratic norm expressions under the coefficient bound, yielding a spherical section. The remaining central-induction/Gauss-mass inequality rules out multiplicity at least two. The argument does not need a blanket pivotality theorem and does not improperly extend its complex characteristic-zero scope to arbitrary positive characteristic. No defect was found.

### Rank three: unrestricted sphericality and classification

The signed quotient is an orthonormal integral based `*`-algebra, so its Frobenius trace and character identities have the stated form. The codegree field argument forces the cubic case to be cyclic/Galois; the cubic dimension field is disjoint from `Q(zeta_120)` because their degrees are 3 and 32. Consequently the six indicated even Frobenius–Schur indicators are fixed by the cubic embeddings.

The positive central measure used in the cubic argument has squared dimension weights, so the proof does not assume that a general sphericalization has all positive simple dimensions. Its total mass is 3 and the six moments are 1. The forced squared-twist sector from induction of the unit and central sign gives the stated atom lower bound. The degree-six Fejér polynomial then yields the upper bound on the sum of reciprocal-codegree squares, leading to `c <= 7b/2`. Combining it with `c >= 4b-8` gives `b <= 16`. The final signed associativity/gauge calculation for `K(1,1,1,0)` produces a section of the given categorification, not merely the existence of another spherical category.

The rational and quadratic cases were checked for the norm-ratio alternatives and divisibility steps. The normalization before the quadratic parity/descent argument is present. The final integer-factor descent eliminates the nontrivial quadratic norm alternatives as claimed. The proof does not use the rank-three classification theorem as a hidden oracle for its general sphericality result.

For reducible rings, the Gauss bound is applied only after the needed positive dimension reduction. The `b<50` tuple table was independently reproduced with integer arithmetic. The `B=1` and `B=3` reductions correctly distinguish reducible from irreducible Pell-type possibilities; the small `c-4b` bound alone is not wrongly treated as a classification. The uniform near-group exclusion has the correct low induction matrices and first two moment equations after correction R3-E1. The exceptional `K(2,1,2,1)` induction contradiction was also inspected. No substantive error was found.

### Rank four: finite classification and unrestricted companion

For the finite classification, the arithmetic necessary conditions, low Gram matrix reconstruction, dimension bounds, principal-minor pruning, and two-moment inequalities were checked at the proof level. The signed quotient remains commutative in rank four because a four-dimensional semisimple algebra with a one-dimensional FP character cannot have a noncommutative matrix block. The sign-central-object arguments keep the twist and dimension signs separate correctly.

The adjoint parity proof uses the alternating pairing on the relevant multiplicity space, and the mod-four constraints are tied to a consistent second-indicator assignment. The global signed argument uses squared dimensions, which is essential outside the pseudo-unitary setting. Its finite covering and normalized sign gauges were reviewed, but the millions of table/orbit instances were not regenerated by this subagent.

The special-family reductions were checked as parameterized arguments. In particular: the `S(m)` low-induction inequality excludes `m>=2`; the residual-involution treatment is a tensor criterion rather than an exact-label oracle; the quadratic family's conductor/root-length reduction has the needed trace constraints; and the conductor-40 equality case produces the stated contradiction. No mathematically invalid general-versus-spherical inference was found.

The companion maintains a more limited unrestricted scope than the finite classification: it does not claim all unrestricted general rank-four categorifications are classified. Its two-FP-dimension and nonselfdual pivotal reductions use Galois pseudo-unitarity only after proving or citing the correct hypothesis. The quadratic/rational codegree cutoff, repeated-quadratic exception, distinct-quadratic factor estimate, and cubic difference/support reductions were reviewed. The stated cubic leftovers are not falsely eliminated by a finite support bound.

The fixed-invertible and Fibonacci-subring reductions were inspected, including the central boson/de-equivariantization structure and finite parameter bounds. The subgroup and positive model existence inputs still rely on cited categorical results; this audit did not reconstruct their associators or every auxiliary literature proof. The unrestricted companion’s finite parameter computations were not separately replayed here.

### Rank five: parity and the two former general residuals

The rank-five commutativity argument handles the only potential noncommutative semisimple decomposition: its formal-codegree relation would force a nonintegral rational codegree, contradicting integrality. The dimension-field spectral bound uses the full orbit polynomial with its multiplicity, and does not assume without proof that the global dimension generates the entire dimension field. The signed Casimir polynomial is correctly compared modulo two.

For the ordinary quadratic parity theorem, dividing by the common coefficient gcd before reducing modulo two is necessary and is done. The one-dimensional square-row kernel forces nonzero quadratic coefficients; positivity bounds and the exact quadratic norm identity saturate the coordinate bounds. Perron irreducibility then forces equality in the signed coefficient triangle inequalities, giving the spherical section.

For the inert-prime theorem (`inert_parity.tex`, Theorem `thm:inert-parity`), the spectral multiplicity restricts the dimension field to the specified quadratic field. Divisibility of the intrinsic dimension by the ordinary codegrees then places the signed global dimension in `2 O_K`. With `q=5 mod 8`, the residue field is `F4`, and the finite character condition forces the relevant residues to lie in `F2`. The proof correctly uses this to return to integer `a_i+b_i sqrt(q)` coordinates rather than assuming those coordinates for all algebraic integers at the outset.

The odd-gcd alternative is excluded by combining the three-one residue pattern with orthogonality modulo four. In the even-gcd alternative, all nontrivial quadratic coefficients have absolute value at least two; the exact sum-of-squares identity saturates the available FP bounds, yielding coefficientwise equality and a spherical section. The two formerly unresolved tensors then need only their already established exact spherical-character exclusions. This composition is a valid general exclusion, provided both component certificates are freshly recomputed from the actual full tensors.

The `inert_parity.py` implementation was inspected: multiplication in `F4`, exhaustive normalized residue-character enumeration, square-row kernel check, radicand constraints, full tensor dimension equations, Casimir polynomial reduction, connectedness, and certificate regeneration are present. No index-specific assumption was found in the criterion. The agent reconstructing rank five has been told to replay the composed certificates, not merely trust this inspection.

### Rank five: cyclic-four central support and rank-eight dependency

The cyclic-four theorem in `cyclic_support.tex:198` is a **general complex categorification** obstruction because Thornton’s near-group theorem supplies a pseudo-unitary Galois conjugate without a braided hypothesis. The manuscript’s use of it for `K(C4,4k)` is within that scope.

The mixed-support proof forces six pairs and eight singles, their multiplicities, and the twist-sector budgets. The zero-coefficient subgroup cases `h=1,2,4` are included. When `h>=2`, the central involution splits the pure sector and pairs its negative twists, making the odd moments vanish there.

The delicate balanced branch (`cyclic_support.tex:137`, Lemma `lem:ng-galois`) was checked separately. Uniqueness of the central simple of dimension `t` identifies the Galois image of the unit row. Signed Galois symmetry of the normalized modular matrix gives the stated eigenvalue ratios. Subtracting the unit coefficient in Verlinde’s formula leaves the two exceptional columns and gives `N_AA^Z - delta_Z,1 = (k/4)b_Z`; the balanced single coefficient requires `k^2/8` to be integral. In particular, this rules out the balanced `k=2,h=1` branch. The other branches still need exact separating certificates.

The parameterized software enumerates the support/indicator branches, reconstructs relative trace types, and verifies separating rays with exact arithmetic. Its `k=2` applicability is therefore not limited to unitarity and can support the rank-eight induced-subring exclusions, subject to the separately checked tensor embedding and fresh certificate replay. No scope gap was found.

### Finite trace and separating certificates

The relative Ramanujan/Gauss trace formulas and joint conductor box were inspected. The all-zero type is retained for larger conductors, which is necessary for sound finite-height truncation. Higher indicator rationality is imposed only when the quadratic field does not occur in the cyclotomic indicator field; the available rational lower bounds have the stated sign and denominator. Low and high Gram vector pruning uses necessary conditions. The certificate contract reconstructs an integer system and checks `A^T y >= 0` and `b^T y < 0`, so floating-point LP discovery is not treated as proof.

### Positive models and the equivariantization action

The positive classification is at the ring level; the code matches exact fusion tensors while literature supplies categorical constructions. For the potentially delicate rank-five `C3+6` equivariantization, Izumi’s Example 13.10 identifies `(-1,R(pi/4))` and `(id,L)` as elements of the actual group `Aut_{rho,0}(O9)`, not only its quotient by natural equivalence. Their product is an actual involution, fixes the unit inclusion, and acts on the six-dimensional multiplicity space as inversion tensored with a trace-zero reflection. This supports the two three-dimensional eigenspaces and the displayed self-dual rank-five fusion rules. No coherence-of-action gap was found in this construction.

## Primary-literature hypothesis checks

The following primary sources were opened and the relevant statements checked. These checks concern hypothesis matching, not an independent reproof of the cited papers.

| Source | Checked point |
|---|---|
| [Ostrik, *Pivotal fusion categories of rank 3*, arXiv:1309.4822](https://arxiv.org/pdf/1309.4822), Theorem 2.13, Corollaries 2.14–2.15 | Spherical induction/codegree relation; general intrinsic-dimension divisibility; spherical dimension-field inclusion. |
| [Thornton, *On braided near-group categories*, arXiv:1102.4640](https://arxiv.org/pdf/1102.4640), Theorem 1.3 | The near-group spherical and Galois pseudo-unitary conclusion is not restricted to braided categories despite the title. |
| [Schopieray, *Categorification of integral group rings extended by one dimension*, final JLMS article](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/jlms.12789), Lemma 3.1 and Theorem 1.1 | Two FP dimensions give a **Galois conjugate** pseudo-unitary category; elementary-abelian 2-group near-group classification has the needed general scope. The older arXiv v1 has stronger unqualified wording in Lemma 3.1; use the final published statement. |
| [Bruillard–Ng–Rowell–Wang, *Rank-finiteness for modular categories*, arXiv:1310.7050](https://arxiv.org/pdf/1310.7050), Theorem 3.9 and equation (2.13) | Spherical Cauchy theorem and signed Galois symmetry of normalized modular data. |
| [Edie-Michell–Izumi–Penneys, *Classification of Z2-quadratic unitary fusion categories*, arXiv:2108.01564](https://arxiv.org/pdf/2108.01564), Theorem 2.4 | The particular rank-four restriction used is stated for pseudo-unitary categories, so the paper title does not make the manuscript’s application too broad. |
| [Larson, *Pseudo-unitary non-self-dual fusion categories of rank 4*, arXiv:1401.1879](https://arxiv.org/pdf/1401.1879), Theorem 1.1 | The cited nonselfdual restriction requires pseudo-unitarity; the manuscript first makes the appropriate reduction. |
| [Bartlett, *Fusion categories via string diagrams*, arXiv:1502.02882v2](https://arxiv.org/pdf/1502.02882), Section 5.3, Lemma 5.14, Corollary 5.15 | Canonical sphericalization and opposite-sign lifts. |
| [Ng–Schauenburg, *Frobenius–Schur Indicators and Exponents of Spherical Categories*, arXiv:math/0601012](https://arxiv.org/pdf/math/0601012), Theorem 4.1 | Central-twist formula in the spherical, not necessarily pseudo-unitary, setting. |
| [Ng–Schauenburg, *Higher Frobenius–Schur Indicators for Pivotal Categories*, arXiv:math/0503167](https://arxiv.org/pdf/math/0503167), Theorem 5.1 | Finite rotation order and cyclotomic field of the indicator. |
| [Izumi, *A Cuntz algebra approach to the classification of near-group categories*, arXiv:1512.04288v2](https://arxiv.org/pdf/1512.04288), Theorem 13.3 and Example 13.10 | Actual automorphism group needed for the rank-five equivariantization, including the two generating pairs. |

## Full replay handoff and recorded provenance

These are archived descriptions/measurements, not fresh results of this subagent.

### Rank four

Run the complete `verify.py --workers 4` after restoring the original stream to `certificates/classification.jsonl.gz`. The archive member is:

```text
Rank4/Rank4_Dong_Palcoux_Through128/Rank4_Through128/certificates/classification.jsonl.gz
```

Compressed size: 75,825,461 bytes. SHA-256:

```text
969a2a5a84b794a3da1d9cd3978f92324d631760f503f5d208011923a723920f
```

Requirements include Python >=3.10, a C++17 compiler, SymPy 1.14.0, and python-flint 0.8.0. Archived runtime was approximately 1,031 seconds on four workers; global signed regeneration/verification accounted for about 827 seconds. Target totals are 889,530 rings, 15 realized and 889,515 excluded. The global signed cover records 6,470,006 orbits and 30,207 retained objects. The parent reported recovering the full original archive and assigned a fresh replay separately.

### Rank five

The compact README names `Rank5_Complete_Through20_InertParity_2026-09-23.zip`, a 113-entry package, with SHA-256:

```text
6981c0ade02db714e38076ff30b3119712ce6b137ac376c2a8ae474a01bb9f49
```

The full-release commands described in the manuscript are:

```bash
python verify.py --jobs 2
python software/verify_extension.py --jobs 2
python -O verify.py --jobs 2
python -O software/verify_extension.py --jobs 2
```

The verification guide requires Python 3.11 or later, SymPy, NumPy, and a C++17 compiler with OpenMP and `__int128`; SciPy is needed only for certificate discovery. Recorded package versions include SymPy 1.14.0, NumPy 2.3.5 and SciPy 1.17.0. Normal verification does not call LP. Archived through-18 runs were approximately 364 seconds normal and 372 seconds optimized on two workers; the 19–20 extension was approximately 130 seconds.

Expected accounting: through 18, 28,493 = 17 realized + 28,476 excluded; extension 19–20, 12,506 excluded; overall 40,999 = 17 + 40,982. The pinned census commit is `b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726`, with tables SHA-256 `4542c0871498337ef38ce3903407933289699a5ff06c85ad0f6c2bd57da823fb`. The stated complete decision-ledger SHA-256 is `9261917451d469ece9929a1756f505924cf84adf34e79a0d2e6f68fed43f55cf`.

The parent’s rank-five auditor is reconstructing a complete replay from the recovered original frontier archive, the 19–20 extension, and the inert-prime module. Such a reconstruction should have its own dated provenance and hashes; it must not be represented as the historical ZIP merely because the decisions agree.

## Residual limitations

This review reduces several concrete risks but cannot establish the absence of all mathematical or software defects. It did not formally verify a compiler, the algebra libraries, the categorical theorems, or all proof text; it did not independently enumerate the external censuses; and its primary-source checks were targeted to the highest-risk scope transitions. A complete replay validates applications of the implemented necessary conditions and exact tensor matches, not every categorical proof or associator construction. Public wording should preserve these distinctions and the requested explicit notice that the results and data were AI-generated and remain unverified by humans and unformalized in Lean.

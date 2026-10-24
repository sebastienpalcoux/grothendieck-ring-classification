# Corrected rank-nine multiplicity-two audit and continuation

The current audited partition is **2,033 excluded, 32 with unitary models,
18 unresolved**, out of **2,083 exact-multiplicity-two fusion rings**.
The input also contains 142 multiplicity-one rings, whose prior IDs and
explicit basis transports are unchanged. Research on the residual cases
continues; no repository or website has been changed.

The current classification is `phase3/results/ledger.json`. The earlier
`results/` and `phase2/results/` ledgers are historical snapshots and contain
the superseded exclusions described below. They must not be used as the
current classification.

## A substantive error, and its complete correction

The original structural pass treated absence from a lower-rank positive
registry as noncategorifiability. That registry omitted the known unitary
half-E6 ring, with basis 1,f,x and rules f²=1, fx=x,
x²=1+f+2x. This invalidated 26 subring claims: ten primary proofs and sixteen
secondary proofs. All 26 claims have been withdrawn.

Reassessment of the ten primary cases gives:

| IDs (prefix R9_2_) | Corrected conclusion | Reason |
|---|---|---|
| 71 | Unitary model | half-E6 × Ising |
| 79 | Unitary model | half-E6 × Rep(S3) |
| 499 | Unitary model | half-E6 × PSU(2)_5 |
| 2020 | Unitary model | half-E6 × Vec(C3) |
| 1218 | Unitary model | Fermionic associative zest of half-E6 × Ising |
| 96, 1266 | Unitary models | The two central-fermion shear equivariantizations of half-E6 × Vec(C2) |
| 97, 98, 1489 | Excluded, by replacement proofs | Each contains NG(V4,2), forbidden by the established near-group criterion |

Thus seven formerly excluded rings are categorifiable. The three other
exclusion conclusions survive, but their original proofs do not. All seven
models have categorical existence proofs and exact full-tensor matches;
the two shear models also have an independent reconstruction and categorical
audit. Their constructions are in `models_restored/`; the independent shear
audit is in `audit_exotic_models/SHEAR_AUDIT.md`.

The corrected `structural_checked.py` accepts a subring transfer only with
an explicit negative tensor and a proof dependency. It never infers an
exclusion from absence in a positive catalog. It rescans all 2,083 rings
and verifies that none of the seven restored positive rings is excluded.

## What the audit checked

* All 2,225 input tensors are distinct and satisfy the fusion-ring axioms.
  A fresh replay of all 2,083 baseline records completed. Its original
  registry check was logically insufficient, which is why the additional
  dependency audit was essential.
* All 588 original structural uses were audited. Apart from the 26 invalid
  half-E6 claims, the remaining 562 have explicit negative lower-rank
  bindings or direct proofs. All 454 rank-six through rank-eight transfers
  match explicit excluded lower tensors coefficient by coefficient. All
  166 stored direct witnesses replay. Three fresh small-rank certificates
  cover the 24 rank-four/rank-five uses that lacked direct witnesses.
* All original 21 positive models passed categorical existence review and
  all 15,309 tensor-coefficient comparisons. The five delicate constructions
  389, 515, 1857, 1983 and 2029 received another independent reconstruction.
* All 36 phase-two exclusions passed renewed scope/proof review. The center
  and Morita audit independently rebuilt finite domains, checked exact
  separating rays, tested positive controls, and handled noncommutative
  representation-degree weights explicitly. The signed audit checked the
  sphericalization and Galois-reduction foundations. The five structural
  exclusions received independent primary-source and tensor checks.
* The original multiplicity-one crosswalk passes all 103,518 coefficient
  equalities. There are 128 identity basis maps and 14 explicit nonidentity
  maps; retaining IDs does not mean every basis is literally unchanged.

Two smaller issues were also corrected. The delivered fresh-replay script
had a Python syntax error (`else120000`); inserting the missing space fixes
execution without changing a mathematical condition. The folded SO(3)
presentation proof omitted an explicit argument for odd boundary count:
splitting a boundary strand and retracting with the normalized bigon fills
that gap. The proof now contains the argument. The center d-number proof now
also spells out the passage from Ostrik's braided squared-norm theorem to
simple dimensions using pseudo-unitarity and integral closure.

Detailed reports are in `audit_baseline/`, `audit_models/`,
`audit_exotic_models/`, `audit_signed_so3/`, `audit_center_morita/`,
`audit_structural/`, and `audit_small_subrings/`.

## Thirteen newly settled cases from the earlier unresolved list

| ID (prefix R9_2_) | Conclusion | Argument |
|---|---|---|
| 92 | Unitary model | The relative-cocycle category C(S5, omega, S3×C2, psi), with omega the sign cup an explicit Schur cocycle |
| 516 | Excluded | Forced central Rep(S3), descent to an impossible rank-three category; an independent labelled-S certificate gives a second proof |
| 392, 1246 | Unitary models | Two explicit relative-cocycle constructions on S4×C2 with the same V4 subgroup |
| 965 | Unitary model | A coherent unitary rank-one extension of the Gelaki dimension-20 Hopf algebra A1 |
| 114, 128, 1487, 1635, 1636, 1959 | Excluded | One Galois restriction criterion forces nonintegral coefficients in a central simple's restriction |
| 1225, 1673 | Excluded | A rank-one odd component forces a fiber functor on the dimension-20 neutral category; the exhaustive Hopf-algebra list has commutative character rings, whereas these neutral rings do not |

For 92, an independent implementation reconstructed S5, verified every
120³ two-cocycle identity and every 12³ relative algebra identity, derived
the twisted fusion formula directly from the bimodule axioms, and matched
all 729 coefficients. The cochains take unit-modulus values, and the
construction is unitary. See `group_models/S5_RELATIVE_TWIST.md` and
`audit_models/S5_RELATIVE_TWIST_AUDIT.md`.

For 392 and 1246, the same subgroup V4 in S4×C2 and two explicit pointed
associators produce the two rings. The second associator reuses a fully
copied lower-rank cocycle, whose identities are checked afresh; no earlier
classification is assumed. Independent checks reconstruct the group and
all 48⁴ cocycle equations, the subgroup algebra, projective characters,
and all 729 coefficients for each ring. See
`integral_theory/D48_RELATIVE_MODELS.md` and both dimension-48 audit reports.

For the six quadratic exclusions, write D for the global dimension and
sigma for the nontrivial automorphism of the quadratic dimension field.
Let B be the distinguished central simple associated to sigma(FP).
Symmetry of the S-matrix gives, for every scalar character chi_h,

`chi_h(F(B)) = f_h / sigma(f_h)`.

The characters determine F(B) uniquely. Rational functional calculus on
the fusion Casimir reconstructs it exactly, and each of the six cases has
coefficients 1/2. Restriction multiplicities must be integers: this is the
contradiction. The independent implementation reconstructs the polynomial
by a different exact method, checks the full operator identity, and invokes
the previously audited Galois-to-pseudo-unitarity gates to obtain general
complex scope. All eleven applicable positive models pass the condition.
See `quadratic_s_symmetry/GALOIS_UNIT_THEOREM.md` and
`audit_quadratic_symmetry/GALOIS_UNIT_AUDIT.md`.

For 516, the distinguished central object of dimension two forces a central
Rep(S3). Condensing its sign object and using the residual C3 grading yields
a rank-three category with dimensions 1, 1+sqrt(3), 2+sqrt(3). Its forced
twist-one contribution in the induction of a nontrivial simple exceeds half
the total dimension, contradicting the vanishing first twist moment.
Every descent step has a separate categorical audit. An exact labelled-S
certificate, independently reconstructed against all 14,128 columns,
provides another proof. See `quadratic_s_symmetry/R516_STRUCTURAL.md` and
`audit_quadratic_symmetry/STRUCTURAL516_AUDIT.md`.

The two dimension-40 exclusions are a unified theoretical application of
Tannaka reconstruction and the classified semisimple Hopf algebras of
dimension 20. The commutativity of both exceptional character rings is
proved directly from their coproducts and independently replayed over
Q(zeta20). No spherical, pseudo-unitary, braided, or Hopf self-duality
assumption is required. See `hopf20/README.md` and `audit_hopf20/AUDIT.md`.

For 965, an explicit symmetric Hopf pairing and normalized Haar cointegral
satisfy the Davydov–Runkel extension theorem in its copairing formulation.
The construction produces a rank-one odd component over Rep(A1), and all
associator maps are unitary. Independent review caught and resolved a dual
Hopf-algebra convention before acceptance: the antipodes in the self-duality
map and the associator definition cancel. The retained proof states this
explicitly and checks the theorem's copairing identities directly. See
`audit_hopf20/MODEL_965_AUDIT.md`.

## Continued research, with unresolved status preserved

The residual list is in `results/unresolved.json`. It includes four integral,
nine strictly weakly integral and five non-weakly-integral cases:

| Type | IDs (prefix R9_2_) |
|---|---|
| Integral | 12, 941, 959, 1965 |
| Strictly weakly integral | 585, 746, 1025, 1209, 1254, 1303, 1709, 1759, 1988 |
| Other quadratic | 137, 1607, 1848, 1975, 1976 |

R9_2_941 matches, in all 729 coefficients, the dimension-504 rank-nine ring
in Alekseyev–Bruns–Dong–Palcoux, *Classifying integral Grothendieck rings up
to rank 5 and beyond*, arXiv:2507.07023v2, Section 1.5, Question 1.14.
The paper explicitly asks for its categorification. This identification is
recorded in `audit_models/published_504_tensor.json`; it does not settle the
question.

The split-involution anti-module and Morita tests were extended with
the correct multiplication orientation to noncommutative rings. They leave
feasible necessary branches for 1225, 1673 and 1848 and therefore give no
exclusion; the first two are instead settled by the Hopf argument above.
The remaining quadratic cases pass the exact Galois restriction tests.
Bounded labelled-S/duality searches on the three commutative cases produce
no certified contradiction; several reach their time limits. This is not
an exact feasibility certificate. A degree-correct noncommutative
implementation leaves 1848 and 1975 undecided. The weak/integral real-character sweep checks all fifteen
then-residual cases and 103 dual-invariant characters, without another
exclusion. Two exact mixed Moore–Read action searches are inconsistent at
the tested phase orders; that excludes only those construction ansatzes.

Group-model search limits, coherent versus unfinished construction attempts,
and the current literature check are recorded in
`group_models/BOUNDED_SEARCH_SUMMARY.md`,
`integral_theory/continuation_attempts.json`,
`weak_integral_attempt_manifest.json`, and `rank6_literature_check.md`.
The exact limits of the final quadratic searches are recorded in
`quadratic_s_symmetry/SUMMARY.md` and `noncomm1975/README.md`.
The newly posted rank-six weakly integral classification has no direct
application: all four rank-six subrings of the nine weak residuals are
integral. A questionable intermediate lemma was not used.

Files describing candidates or feasible constraints are research records,
not classification authority. Only `accepted.json` and the explicit corrected
subring proof pass change the current ledger. No complete classification of
the eighteen residual rings is claimed.

This is a checked research package, not a formal proof-assistant development.
The reports distinguish categorical arguments from finite certificate replay
and do not treat an unsuccessful search as a nonexistence theorem.

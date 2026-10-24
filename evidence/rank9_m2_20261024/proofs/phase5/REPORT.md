# Fifth continuation: four general exclusions and one unitary model

Research date: 24 October 2026. This continuation investigates all nine
rank-nine, exact-multiplicity-two cases left by phase four. Five are now
settled after independent categorical review and exact arithmetic replay.

| Ring | Result | Main argument |
|---|---|---|
| R9_2_12 | Excluded over C | Fermion parity forces a Tannakian center; weak group-theoreticality and dimension-60 descents contradict the complete group-theoretical obstruction. |
| R9_2_941 | Excluded over C | Odd central-dimension restrictions force a dimension-nine simple in a center that must be simple. |
| R9_2_959 | Excluded over C | The same dimension-120 theorem as R9_2_12. |
| R9_2_1848 | Unitary model | Isotropic C3 orbifold of an existing unitary near-group category NG(C18,18). |
| R9_2_1965 | Excluded over C | Two scalar characters force a symmetric central subcategory; a dimension-84 Gram obstruction makes it Lagrangian. |

The four unresolved rings are **R9_2_137, R9_2_1607, R9_2_1975 and
R9_2_1976**. They all have dimension type
`(1^4,2,(4+3sqrt(2))^4)` and global dimension `144+96sqrt(2)`.
Their braided categorifications are already excluded, but their general
categorifiability remains open in this research.

## Classification counts

| Scope | Total | Excluded | Modelled | Unresolved |
|---|---:|---:|---:|---:|
| Rank 9, exact multiplicity 2 | 2083 | 2043 | 36 | 4 |
| Rank 9, multiplicity at most 2 | 2225 | 2145 | 76 | 4 |

The second row retains the previous 142 multiplicity-one decisions.
Relative to the accepted phase-four research baseline, seven earlier-rank
cases are unchanged and the project-wide unresolved frontier decreases
from 16 to 11. These are research-lineage counts; independent corrections
made by the other agent performing the online audit must be reconciled
before publication.

## The theoretical content

The dimension-120 argument gives a reusable criterion: in an integral
commutative category whose dimension is divisible by four, if the
multiplicity-free induction of the unit has exactly one odd nonunit
constituent, of odd prime-power dimension, then its center has a
nontrivial Tannakian subcategory. The possible fermionic exception is
handled by the S-matrix eigenvector identity for I(1), followed by parity.
The full proof conservatively assumes trivial universal grading, which
also permits an independent relative-center derivation.

The dimension-504 argument classifies only the possible odd-dimensional
central restrictions. It reduces the difficult dimension-63 case to two
congruences and seven aggregate possibilities. Two dimension identities
modulo two then force a central prime-power object. A large center
enumeration or numerical infeasibility claim is unnecessary.

The dimension-168 argument constructs a Tannakian subcategory from two
central dimension-three objects using the scalar-character S identity.
It excludes a central involution through a strictly negative two-by-two
induction-Gram minor in its forced dimension-84 quotient. The Tannaka
group is then perfect of order dividing 168, so the subcategory is
Lagrangian. The previously audited all-cocycle group-theoretical theorem
supplies the contradiction.

The R9_2_1848 model uses Izumi's published isotropic orbifold theorem and
Budinski's exact unitary NG(C18,18) existence result. The construction
supplies coherent associativity; a fresh implementation independently
matches every one of the 729 census coefficients. This does not claim a
fresh reconstruction of the source near-group associator or a universal
parameterization of arbitrary spherical categories.

## Evidence and scope

Proofs and independent audits:

| Cases | Proof | Independent audit |
|---|---|---|
| 12,959 | `integral120/THEORY.md` | `audit_integral120/REPORT.md` |
| 941 | `case941/EXCLUSION_THEOREM.md` | `root/AUDIT_941.md` |
| 1965 | `integral168/GENERAL_EXCLUSION.md` | `audit_integral168/REPORT.md` |
| 1848 | `quadratic_noncomm/REPORT.md` | `audit_model1848/REPORT.md` |

The current authority is `results/ledger.json`, generated from the
immutable phase-four snapshot by `build_results.py`. `accepted.json`
lists the five changes. `verify.py` replays the accepted finite evidence,
checks all 2083 source identities, and compares all **26244** structure
constants of the 36 model transports. These finite checks accompany
separate categorical audits; they are not formal proofs in a proof assistant.

The four residual cases receive further structural reduction and model
investigation in `quadratic_comm/` and `quadratic_noncomm/`. Necessary
Morita-ring completions are not categorical models, and a failed
construction is not a nonexistence theorem. Any scope limitations in
those reports are retained in the classification.

The independent replacement exclusion of R8_3_436 from phase four is
unchanged. Its withdrawn universal unitary-table premise remains
withdrawn; no claim made here reinstates it.

## Publication boundary

No GitHub repository or website was modified. The user paused this
agent's online work because another agent is revising after an audit.
These results are prepared as separate research evidence for a later
coordinated revision. Earlier research snapshots are preserved, including
their supersession notices and the repaired rank-eight proof.

# Third-round higher-multiplicity continuation

**R6_5_638 and R6_7_1225 are excluded from categorification over C without
additional categorical hypotheses.** Their final certificates are
`R6_5_638_general.json` and `R6_7_1225_general.json`; `summary.json` records
the exact coverage, hashes, and replay reports.

The new necessary criterion retains the integrality of the unknown simple-
object multiplicities in the full Morita Gram equations. An integral row
vector with yA=0 and yb≠0 modulo 2 excludes a module branch even when the
rational nonnegative relaxation is feasible. The proof is in
`integral_morita_proof.md` and `../../../papers/chapters/round3_integral_morita.tex`.
The tensor-parametric public verifier is
`../../../software/round3_integral_morita.py`.

For each tensor, two of the 16 module branches fail the Morita rank bound,
twelve fail the new congruence test, and two force negative stabilizers on
the same two simple objects. The completed height-six Clifford/center
calculation checks 91 low frames, 50 character labellings, and all four
second-indicator choices: 200 exact separating systems per tensor. The
unrestricted signed reductions supply general categorical scope.

## Exact replay

From the package root:

```sh
python -O research/round3/higher/verify_higher.py R6_5_638 --integral --conditional 0
python -O research/round3/higher/verify_higher.py R6_5_638 --integral --outer
python -O research/round3/higher/verify_higher.py R6_7_1225 --integral --conditional 0
python -O research/round3/higher/verify_higher.py R6_7_1225 --integral --outer
```

Each job has an 890-second limit. Conditional replay invokes the unmodified
public `stabilizer_rotation_higher.verify_conditional` and disables all
optimizer entry points. The outer replay reconstructs the signed domain
and all module actions, and checks that the conditional checkpoint belongs
to the exact source certificate SHA-256. The measured conditional times
were 511.38 s and 531.20 s; the remaining exact general replay took 31.98 s
and 109.32 s. The public entry point
`round3_integral_morita.verify_general(R,c)` can also replay the whole proof
without these checkpoints.

The discovery records retain the label `discovered_unverified` to describe
their state when first written. They are immutable inputs to the hash-bound
replay; the final `*_general.json` records supersede that discovery status.
No numerical infeasibility status is accepted as a certificate.

## Uniform application and controls

`integral_scan.json` records 76 completed inputs: all 22 inherited residuals
and all 54 inherited realized models. Among the latter, 27 are eligible and
27 lie outside the module domain. There are no timeouts or false
exclusions. The modulo-two test alone leaves a branch on each inherited
residual; the new exclusions use the forced-indicator continuation.

`integral_audit.json` records all 24 modular branch checks, five corruption
controls per input, and nontrivial basis relabellings which independently
recover two rank obstructions, twelve modular obstructions, and two
surviving branches. `independent_scope_audit.md` records the separate review
of the categorical and integral-multiplicity reasoning.

`positive_controls.json` is a distinct, older-engine height-six discovery
scan: 43 inputs lack its local rotation hypothesis, four lack its trace
domain, six complete without an exclusion, and R6_6_345 reaches its 120-second
budget. That timeout is not an exclusion and does not affect the completed
54-model audit of the new congruence criterion.

## Exploratory records retained

The earlier height-six run for R6_5_638 completes without an obstruction;
it exposes precisely why integral Gram multiplicities are needed. The
R6_7_1225 run already produces a larger proof with three separate Clifford
conditionals; the final integral certificate uses only one.

`rotation_all22.json` is a 45-second-per-input exploratory scan of the
inherited quadratic center engine. A null result can mean ineligibility or
a surviving relaxation; a timeout is explicitly incomplete. Its four
multiplicity-eight pseudo-unitary candidates were passed to the independent
arithmetic workstream for general-scope treatment. In particular,
`R6_8_6524_induction.json` is a fully verified elementary pseudo-unitary
codegree-moment obstruction, independently confirming that component.

The family scans include the tensors with dense parameter p=1,3,5,7 at
multiplicities 2,4,6,8. These scans do not give a new obstruction: p=1 is the
realized Izumi C4 dual even part, while the other three are already excluded
by inherited general certificates. They are not counted as new exclusions.

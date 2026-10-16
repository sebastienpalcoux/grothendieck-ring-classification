# Mathematical review and verification scope

> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.

The current manuscripts give one account of the classification and its open
questions. This guide states what the supporting review and computations
establish, and where mathematical verification is still needed.

## Mathematical scope

The [current research account](../docs/RESEARCH_STATUS.md) records **35 decisions among 38 cases**: 28 proposed general exclusions and 7 unitary constructions. Three general questions remain open: `R6_4_155`, `R6_8_1660` and `R8_2_24`. The combined residual program records 139 decisions (119 exclusions and 20 constructions), all subject to independent mathematical verification.

| Open ring | Established necessary restrictions | Remaining question |
|---|---|---|
| `R6_4_155` | A unique rank-26 semion-centralizer modular candidate; a rank-22 based module satisfies the fermion Azumaya linking identities. | Coherent associators and module-category structures, or a general obstruction. |
| `R6_8_1660` | One relative-center based ring, three possible Morita-dual rings and a bounded center-profile domain; saturated traces force `nu_3(T)=2`. | A categorification or an obstruction covering every possible profile. |
| `R8_2_24` | A rank-four neutral component and a required tensor autoequivalence whose square is the indicated inner action. | A general categorical obstruction or construction; the mixed transport identities in the proposed local approach are unproved. |

For `R8_2_24`, an eight-slot local calculation is conditional on mixed
categorical transport identities. Verifying its algebra does not prove those
identities. In particular, the incoming left-bend uses the complementary index;
a diagonal condition alone does not establish decorated-phase cancellation.
No general exclusion is counted for this case.

The review examines general versus pivotal or pseudo-unitary scope, cited
hypotheses, sphericalization and Galois reductions, Morita constructions,
indicator constraints and root-order completeness. Further expert review
should especially examine coherence of inverse-Morita constructions, the
algebraic 2D2 arguments and the conductor-equality reductions. An AI review
cannot certify that every mathematical step is correct.

## Computational coverage

| Check | Executed scope | Result and limit |
|---|---|---|
| Rank three | Bounded near-group enumeration, `b<50` | Five reduced tuples; categorical proof reviewed separately. |
| Rank four | Two complete 889,530-ring replays, each regenerating 6,470,006 signed orbits; separate unsigned recount | Passed: 15 models and 889,515 exclusions. |
| Rank five | All 40,999 classes, 17 models and 40,982 exclusion certificates in normal and optimized Python | Passed; complete reconstructed ledgers are byte-identical. |
| Rank six | Model/import pipeline and all 25,362 exclusion certificates, followed by the two post-loop checks | Combined coverage passed; the initial full process failed on seven certificates, each of which passed a separate complete Python-backend replay. |
| Rank seven base certificates | 4,201 records: 4,116 exclusions, 26 models and 59 cases deferred to continuation proofs | Passed in normal Python. |
| Rank eight base certificates | 973 records: 832 exclusions, 60 models and 81 cases deferred to continuation proofs | Passed in normal Python, including signed proof trees. |
| Continuation chain and current inventory | Source identities, accepted decisions and dependency replays in normal and optimized Python | Passed within each program's stated scope; does not prove categorical coherence. |

The [full replay guide](../evidence/prepublication_20261017/FULL_REPLAY.md),
[coverage audit](../evidence/prepublication_20261017/reviews/verification_coverage.md)
and [current inventory receipts](../evidence/prepublication_20261017/current_history/receipt.json)
identify the exact inputs and executed programs. Continuation checks supplement
the base loops; they do not rerun every base certificate. An optimized run alone
cannot check assertions removed by Python's `-O` option.

## Rank-six environment and coverage

The [complete packet](../evidence/prepublication_20261017/rank6_backend/README.md)
records **25,355 initial passes plus seven complete Python-backend passes**,
exactly covering 25,362 distinct certificates. It also records the separately
executed post-loop counts and model registry and binds 299 source/input files.
This was a **combined verification campaign, not a successful single full run**.

The affected Galois-balance systems order some algebraic tuples by their string
representations. SymPy's Python and Flint backends can reorder or reverse these
equations, invalidating a positional Farkas vector for the other ordering.
Exact matrix comparisons establish equivalence; complete retries use the
unchanged checker with `SYMPY_GROUND_TYPES=python` set before importing SymPy.
The initial failed status and receipts remain in the packet. No inequality is
relaxed and a failed check is not counted as a pass.

The initial process did not record its loaded backend/version. The installed
Flint version changed from 0.8.0 to 0.9.0 during execution; no uniform measured
runtime is claimed. The portable complete-replay orchestrator has **not itself
been executed end to end**. Its identity, coverage and rejection controls were
tested. No all-Python full-census pass is claimed.

## Public reproducibility

The [rank-four replay](../supplements/rank4/PUBLIC_REPLAY.md) uses checksummed
public certificate parts. The [rank-five package](../evidence/prepublication_20261017/rank5/README.md)
reconstructs every class from recovered proof sources and pinned tensors;
the unavailable archive's ledger is not represented as recovered. Normal and
optimized replays independently produce the recorded reconstructed digest.
No private attachment is required for either public replay.

[Verification instructions](VERIFY.md) give executable commands.
[Provenance](PROVENANCE.md) records the exact ledger and archive identities.

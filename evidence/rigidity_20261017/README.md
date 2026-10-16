# Inner-square rigidity · rank-eight completion

**AI-generated research · independent verification pending.** The proofs and data have not been independently human-verified or Lean-formalized. Automated checks establish only their explicitly stated arithmetic, source-identity, and bookkeeping claims.

The [inner-square torus theorem](rank8/R24_TORUS_RIGIDITY_PROOF.md) excludes a complex fusion-category categorification of **R8_2_24**. A forced rank-four subcategory would admit a label-fixing tensor autoequivalence whose square is conjugation by a particular invertible object. The pivotal signs force a nontrivial projective inner action. All associator entries have short even gauge weights; a putative square root would then produce infinitely many inequivalent tensor functors, contradicting tensor-functor rigidity.

| Scope | General exclusions | Realized rings | Unresolved |
|---|---:|---:|---:|
| Rank 7 through multiplicity 4 | 4,172 | 29 | 0 |
| Rank 8 through multiplicity 2 | 896 | 77 | 0 |
| The 38-case continuation | 29 | 7 | 2 |

The combined residual program records **140 decisions: 120 general exclusions and 20 unitary constructions**. The two remaining general questions are **R6_4_155** and **R6_8_1660**.

## Proof and independent reviews

- [Complete theoretical proof](rank8/R24_TORUS_RIGIDITY_PROOF.md).
- [Source, Galois reduction, conductor equality, and indicator audit](rank8/final_prerequisite_audit.md).
- [Local pivotal signs, common chart, and actual inner-square audit](rank8/final_structural_audit.md).
- [All associator weights, tensorators, and natural-equivalence audit](rank8/final_torus_audit.md).
- [Typed local derivation](rank8/R24_TYPED_INNER_DUALITY_AUDIT.md).

The three independent reviews above were performed within the AI workflow. They are mathematical research audits, not independent human verification. The proof uses the published tensor-functor finiteness theorem of Etingof–Nikshych–Ostrik and the published Galois-conjugacy formulation of Schopieray's two-dimension lemma; the proof and prerequisite audit give precise references.

## Data and replay

- [36 accepted continuation decisions](decisions.json), [all 38 cases](all_cases.json), [remaining IDs](remaining_ids.json), and [rank totals](expected_totals.json).
- [The source-bound R24 decision](new_decisions.json).
- [Four finite checkers and their normal/optimized receipts](checker_receipts.json).
- [Source manifest](source_files.json).

The existing 35 continuation records retain their references relative to `evidence/unified_20261016/`. The R24 record specifies its own `proof_source` explicitly. No other rank-eight ledger record is changed. The complete parent ledger is retained byte-for-byte for isolated replay of the preceding stage.

```bash
python3 tools/verify_rigidity_20261017.py --metadata-only
python3 tools/verify_rigidity_20261017.py
python3 -O tools/verify_rigidity_20261017.py
```

Metadata verification binds the full proof and audit files, source tensor, parent ledger, exact single-record change, and complete current partitions. The normal commands additionally replay four finite checkers and compare their outputs with the retained receipts. The checkers do **not** certify categorical coherence, the conductor-equality theorem, or the tensor-functor-rigidity proof. Full historical replay is dispatched by `tools/verify_current_publication.py --historical` in an isolated copy.

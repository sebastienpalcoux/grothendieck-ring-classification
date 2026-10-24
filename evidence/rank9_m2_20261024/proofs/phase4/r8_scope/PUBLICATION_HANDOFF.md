# R8_3_436 publication correction map

This is a plan for the user's later online-revision step. No repository file
was edited in this task.

The accepted replacement is `REPAIR.md`, with exact source `source.json`
and replay `verify_equivariantization.py` / `equivariantization_certificate.json`.
The invalid general near-group unitarization assertion must be withdrawn
explicitly even though the independent replacement proves the same ultimate
noncategorifiability conclusion.

## Active mathematical text

1. Replace the subsection titled “A general inversion obstruction from the
   C3+3 TPE” in the rank8 manuscript with the independent spherical
   equivariantization/formal-codegree proof. Local paths include
   `supplements/rank8/paper/m3_frontier.tex` and
   `manuscripts/rank8/paper/m3_frontier.tex`.
2. Update the generator `tools/build_rank8_m3_article.py`, whose source list
   currently includes `structural_models/r436_general_tpe.tex`. Otherwise
   regeneration will restore the invalid proof.
3. Add the new proof and receipt under a fresh dated evidence directory;
   the new decision should name the criterion
   `spherical_equivariantization_formal_codegree_field` and general-complex
   scope, with source SHA binding.
4. Update the effective current rank8 ledger overlay, the R8_3_436 case
   proof link, theoretical-evidence record, source manifests, and verifier
   registry to use the new proof. Current table counts need not change
   from the previously excluded status once the replacement is accepted.
   If a separate audit revision temporarily reopened the case, re-exclude
   it by the replacement proof and retain that correction history.
5. Rebuild rank8 PDF, mirrored website PDF, document/publication manifests,
   and current website datasets from the generators; do not hand-edit the
   same case independently in multiple derived JSON files.

## Historical evidence

Keep historical artifacts as historical evidence, with a prominent withdrawal
notice linking the replacement. In particular:

- `evidence/rank8_frontier_20261021/structural_models/R436_GENERAL_TPE.md`;
- companion `.tex`, `r436_general_tpe.py`, and `r436_general_tpe.json`;
- that release's `accepted.json`, `verifier_registry.json`, replay receipts,
  release/source manifests, and subsequent historical rank8 ledgers.

A scalar replay may still be described as passing its stated polynomial
identities. It must no longer be used as a verifier of general categorical
exclusion or universal Galois unitarization. Preserve immutable archives and
hashes; use an external supersession/withdrawal record rather than silently
rewriting an archived mathematical history.

The earlier unitary-only proof
`evidence/rank8_m3_20261021/models/R436_INVERSION_PROOF.md` is valid and
may remain an independent secondary proof. Its own warning that it does
not prove general exclusion remains historically accurate for that argument.

## Dependencies and secondary validation

The original rank8 tensor contains multiplicity3. No fusion subring of a
maximum-multiplicity1 or2 tensor can equal it. Thus no rank9 M2 exclusion,
or rank10/rank11 M1 exclusion, can depend on transferring this rank8 tensor
as a fusion subring. Changes to global counts arise only if a temporary
status restoration is being superseded, not from the proof replacement itself.

The two possible rank5 equivariantization rings also match existing lower-rank
excluded tensors coefficient by coefficient:

| Parameters | Existing source | Basis map |
|---|---|---|
| a=0,b=3 | R5_3_38 | identity |
| a=1,b=2 | R5_2_13 | identity |

The explicit archived certificates use norm obstructions at primes13 and5,
respectively. `rank5_crosscheck.json` records this corroboration. The new
proof independently derives the obstruction and does not use those archived
rank5 decisions as premises.

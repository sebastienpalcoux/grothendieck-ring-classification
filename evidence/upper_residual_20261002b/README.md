# Upper-rank categorical update, 2 October 2026

This verified update adds **30 general complex exclusions and 13 unitary models** to commit `7c78b88486d5412adeed10d77275e3eaa2de0b7d`. It resolves 43 of that commit's 140 upper-rank open records. It does not complete the classification.

| Rank | Census scope | Excluded over ℂ | Unitary models | General existence open |
|---|---|---:|---:|---:|
| 7 | Exact multiplicities 1–4 | 4,132 | 27 | 42 |
| 8 | Exact multiplicities 1–2 | 846 | 72 | 55 |

Rank-six decisions and its October 1 archive are preserved: 25,362 excluded, 57 models and two open cases. The user's laptop runs are not reported as completed.

The [decision inventory](decisions.json) binds each new result to its full original multiplication tensor, exact source fingerprint, proof and checker. [Remaining IDs](remaining_ids.json) are the complete current general frontier. No absence of a model is used as an exclusion.

## Proofs and models

- [Rank-seven integral families](r7_integral/README.md): 12 general exclusions by prime descent, orbit restrictions, rank-one module categories and group-theoretical obstructions. R7_2_213 has invertible group C4; this corrects the earlier retained V4 description and preserves its exclusion.
- [Rank-seven signed exclusions](r7_nonintegral/SIGNED_GENERAL_PROOF.md): exhaustive oriented signed tables exclude R1036, R1044, R2510 and R2706 generally. [The D12 category](r7_nonintegral/R240_D12_PROOF.md) realizes R240 unitarily and modularly.
- [Rank-eight integral proofs](r8_integral/PROOFS.md): seven general exclusions and five independent unitary constructors. [R694](r8_integral/R694_DIM28_GRADING_PROOF.md) uses the dimension-28 descent; [R575](r8_integral/r575/PROOF.md) uses explicit semisimple Hopf16 self-duality, cointegral data and the Davydov–Runkel construction.
- [Dimension-96 criterion](r8_integral/D96_TWO_DIMENSION_ORBIT_PROOF.md): type `1^4,2,4,6^2` forces a nontrivial universal grading. Two equivariantization descents and invariant square coefficients exclude R404, R418, R604 and R692 over ℂ. Every possible sign is checked.
- [R68 in dimension108](r8_integral/r68/PROOF.md): relative-center coprime lifting produces an actual central boson, and the combined C4 action cannot exchange the two required rank-one module classes. This generally excludes the last integral rank-eight residual.
- [Other rank-eight constructions](r8_nonintegral/NONINTEGRAL_PROOFS.md): six unitary models and two general exclusions, including the [actual unitary HI(C7) Q-dual](r8_nonintegral/R868_HI7_DUAL_PROOF.md).

Every positive result has an independent constructor and full coefficient comparison. An associative tensor alone is not an existence proof: the cited category construction supplies the associator and rigidity. Separate mathematical audits check those construction hypotheses.

## Scoped results

The four rank-seven cases R1212, R1213, R1417 and R1420 have no pivotal categorification; they remain generally open. The [rank-eight scope report](r8_nonintegral/SCOPED_RESULTS.md) records the narrower unitary and pseudo-unitary obstructions. R8_1_9, R8_1_18 and R8_1_49 have no braided categorification. Their general/pivotal/spherical/pseudo-unitary **existence questions are equivalent** by the published Galois-conjugation lemma; this does not say every realization is pseudo-unitary. A retained unreplayed central-lift observation is not promoted to a bosonicity or general nonexistence theorem.

The earlier [October 2 results](../residual_20261002/README.md) and [AnyonWiki import](../anyonwiki/README.md) retain their original evidence and scopes. Recovery notes record historical research, not additional current decisions.

## Reproduction

With Python 3.12, SymPy 1.14.0 and NumPy 2.2.6, run from the repository root:

```sh
python3 tools/verify_upper_residual_20261002b.py
python3 -O tools/verify_upper_residual_20261002b.py
python3 tools/validate_release.py
```

The exact checkers use explicit exceptions rather than optional Python assertions. The source manifest is pinned in the release verifier. The preservation manifest restores every replaced record and checks the complete historical ledgers and all unaffected fields. Historical October 2 and AnyonWiki replays run in an isolated temporary copy with the original source bytes. Current published ledgers are never temporarily rolled back.

Both rank-seven and rank-eight archives embed a `verification-repository` with the dependencies for the same replay. The archive entrypoints dispatch to that copy. The normal and optimized whole-update receipts are `verification_normal.json` and `verification_optimized.json`.

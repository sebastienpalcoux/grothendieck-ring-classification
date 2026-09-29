# Final publication audit gates

This is the independent mathematical workstream's checklist, based on the
actual release files and generators. A listed gate is not a claim that the
root agent has already completed it. No global ledger or website file was
edited by this workstream.

1. Freeze `verification/round4/proof_sources.json` only after every listed
   general certificate has passed its exact replay. Every kind must be
   dispatched by `software/check.py` and registered in
   `software/round4_release.py`. In particular any accepted half-E6 proof
   needs both registrations; it must not be included merely as a
   pseudo-unitary research result.
2. `python -O software/round4_release.py --jobs 3` must reconstruct every
   selected proof with optimizers disabled, compare all ten frozen tensors
   with the census, require disjointness from earlier campaigns, and verify
   that each source file kept its hash during replay. Its canonical output
   is `certificates/continuation_round4.jsonl`, with receipt
   `verification/round4/release_replay.json`.
3. Keep earlier certificate campaigns and historical reports intact. The
   new receipt states honestly that the complete inherited catalogue was
   not replayed again. Check the prior source hashes rather than assigning
   a new timestamp to old results.
4. Regenerate and cross-check `data/decisions.json`, `decisions.csv`,
   `classification_counts.json`, `unresolved_tensors.json`, the model
   catalogue, `verification/release_summary.json`, and `papers/generated_*`.
   Run `software/release_consistency.py` normally and with `-O`. All five
   existence fields must agree. The 54 model IDs and 61 constructors remain
   unchanged unless a separately proved positive model is added.
5. Require `research/round4/coverage.py --require-canonical` to cover all ten
   frozen inputs and to separate eligibility, exact exclusion, exact
   surviving witness, solver result and incomplete work. A new theorem's
   applicability screen is not a replay on all eligible census tensors.
6. Reconcile `README.md`, `REVISION_NOTES.md`, `research/round4/README.md`,
   the case-directory guides, `verification/README.md`, both TeX documents,
   and website totals with the accepted ledger. Retain the already complete
   multiplicity-three classification. Do not count finite restriction
   profiles, integer witnesses, or modular-data candidates as models.
7. Include the projection proof, Fourier mass corollary, relevant source
   tables, full general reductions, and exact branch/ray totals in the
   manuscript. Keep the two-FP-value result in its published Galois-conjugacy
   form. Include all half-E6 positive branches and all three C3 associators.
   The Ising merged phase mass is D*sqrt(2)/2, while its individual-twist
   mass is D*sqrt(2)/4.
8. Verify all links and cited certificate paths after the final names are
   settled. Rebuild `papers/manuscript.pdf` and `verification_guide.pdf`;
   inspect rendered pages with new theorems, tables, final totals and long
   filenames. Record document QA independently from mathematical replay.
9. Include the model-scope audit, exact receipts, mutation checks and
   independent replay files under `research/round4/models/`. Their specific
   known-Morita-model exclusions must not be presented as general negative
   classifications.
10. Regenerate `SHA256SUMS` after all files are frozen. `check_manifest.py`
    checks listed digests; additionally compare its path set with the
    complete intended archive path set and validate every ZIP member.
    Ensure no stale process writes to a source-bound certificate or report
    after this step. Repository, delivered ZIP and website downloads should
    use these same accepted source files and totals.

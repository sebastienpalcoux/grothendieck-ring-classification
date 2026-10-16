# R24 reopened after categorical proof review

Review date: 2026-10-17. Disposition: **R8_2_24 is unresolved; the previous general exclusion is not retained.**

The frozen proof in `../../unified_20261016/rank8/R24_PROJECTIVE_INNER_SQUARE_PROOF.md` has an unsupported decorated-phase cancellation. The incoming left-bend phase has a complemented index, so the asserted cancellation does not follow from the stated hypotheses. This finding was independently checked by two reviewers. It is a proof gap, not a construction of the ring.

- `R24_BRIDGE_PREPUBLICATION_AUDIT.md` gives the concrete issue and source locations.
- `CONDITIONAL_EIGHT_SLOT_REPAIR.md` gives a possible replacement argument that avoids the disputed decorated flips. Its categorical B/C transport remains unproved; it is retained as conditional research only.
- `verify_eight_slot_algebra.py` checks the finite algebra of that candidate argument.
- `eight_slot_normal.json` and `eight_slot_optimized.json` record the normal and optimized runs. Both have zero classification decisions and explicitly say that categorical transport is not certified.
- `MANIFEST.json` binds the unchanged frozen proof, the inspected primary-source files, and this review packet's files.

Replay from this directory:

```sh
python verify_eight_slot_algebra.py --output eight_slot_normal.json
python -O verify_eight_slot_algebra.py --output eight_slot_optimized.json
```

The candidate algebra does not authorize an exclusion. A general exclusion would require a new independently checked categorical proof.

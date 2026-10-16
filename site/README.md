# Fusion & Grothendieck Ring Atlas

Private research site with two clearly distinguished populations. Its main table counts **confirmed realized Grothendieck rings**, omitting rows that contain only zeros. Partial bands display ≥: the known positive count is a lower bound while unresolved fusion rings remain. The fusion-ring census counts **all** based rings and is linked directly. The categorification ledger keeps exclusions, positive models, and general unresolved cases apart. Multiplicity is the exact maximum structure constant. Only ranks with a classification manuscript and assessed bands are included; counts alone never imply categorifiability.

## Regenerate

Run these commands from this Site checkout, passing the private classification repository as input:

    python3 build_snapshot.py --classification /path/to/classification-repository --classification-commit FULL_RELEASE_COMMIT_SHA
    python3 build_realized.py --classification /path/to/classification-repository
    npm run check
    npm run dev

`build_snapshot.py` rejects missing census bands, cumulative mismatches, and status partitions that do not sum to census counts. `build_realized.py` checks every catalogued tensor's rank, unit, duality and associativity. It derives exact dual and invertibility data and approximate Perron dimensions. For commutative rings it supplies exact codegree polynomials and an exact primitive-root character presentation. For noncommutative models it derives numerical irreducible trace characters from the exact center kernel, checks block dimensions and orthogonality, and attaches exact individual codegree polynomials using the central Casimir and the validated numerical block matching. Numerical values are marked approximations. `smoke_test.py` compares each band’s positive count against the exact model records and requires rank five to be complete through multiplicity twenty. The static site serves only `dist/` and uses no credentials or runtime APIs.

## Contents

- dist/index.html, styles.css, app.js: responsive count explorer, explicit ring cards, full fusion-matrix profiles, character tables, formal codegrees, model references, paper shelf.
- dist/data/atlas.json, grothendieck_counts.csv: generated positive count table and classified census-band snapshot.
- dist/data/realized_rings.json: exact tensors, selected algebraic invariants, and per-model source pointers.
- dist/data/counts.csv: classified fusion-ring census bands with provenance.
- dist/data/classification_status.json: exact per-band classification ledger, copied from the repository.
- dist/papers/: revised manuscripts and guides.
- dev-preview.mjs: dependency-free local preview for QA.

## Private publication

The source and associated GitHub classification repository remain private. The Site uses owner-only access unless the owner invites a viewer through **Share**. Preserve that audience when publishing revised versions.

The rank-three manuscript proves unrestricted five-ring necessity directly, together with sphericality. Its classification-status ledger marks every displayed rank-three multiplicity as complete. By default an individual ring profile shows one fusion matrix at a time and offers a full tensor download. The character page distinguishes exact primitive-root formulas from approximate numerical tables.

## Rank-six classification

The classification counts come from the current release ledger; categorical
models, exact fusion tensors and references come from the model catalogue.
The residual summary starts with the dated rank-six release and applies the
October 2, October 11 and October 16 research overlays in order, checking each exact
previous-source path and checksum and unchanged classification totals. The
latest overlay is `evidence/unified_20261016/rank6/research_progress.json`.
It identifies the complete twist-one support for R6_8_1660 and retains tensor-functor
rigidity for both hypothetical categories. Both categorification cases remain unresolved.

The frozen October 1 archive, release identity, ledger and per-band counts are
validated independently of the current manuscript. The current
`evidence/unified_20261016/rank6/document_revision.json` binds the latest
research overlay to every rank-six paper TEX/PDF by checksum and byte size.
The site publishes this manifest as `dist/data/rank6_document_revision.json`,
along with the current manuscript and verification-guide PDFs. It retains the
October 2 PDF addendum and the complete research-summary provenance chain.
Validation compares displayed counts with the classification ledger and model
catalogue, checks the exact frozen archive, and checks current PDFs against
their document revision rather than the historical archive's document hashes.

## 16 October unified theoretical continuation

The current notice and proof table come from
`evidence/unified_20261016/decisions.json`. The continuation resolves 36 of the
38 cases open at the preceding release: 29 general exclusions and 7 unitary
constructions. Rank seven is complete through multiplicity four, and rank eight
through multiplicity two. The two rank-six questions remain open.

The snapshot builder checks every changed case against its current ledger,
remaining IDs and totals, the proof bundle, and the current manuscript hashes.
Scoped results and necessary-condition witnesses do not enter general decision
counts. `ALL38_COVERAGE.md` accounts for every original case.

Build the current bundle in the classification repository with
`python3 tools/build_unified_20261016_archive.py`. It replays its verifier from
a clean extraction before replacing `unified-update-2026-10-16.zip`. The dated
earlier archives remain historical snapshots with unchanged names and hashes.
Regenerate the snapshot after the archive and status export are ready, then
supply the immutable classification commit so proof links identify this release.

The Site audience remains owner-only. Local revisions do not deploy or change
access. On managed Linux, run browser preview only when the supported
`control-browser` skill is available; otherwise run the static and data checks
and report the visual-QA limitation.


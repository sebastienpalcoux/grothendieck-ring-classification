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
latest overlay is `evidence/theoretical_20261016/rank6/research_progress.json`.
It identifies the complete twist-one support for R6_8_1660 and retains tensor-functor
rigidity for both hypothetical categories. Both categorification cases remain unresolved.

The frozen October 1 archive, release identity, ledger and per-band counts are
validated independently of the current manuscript. The current
`evidence/theoretical_20261016/rank6/document_revision.json` binds the latest
research overlay to every rank-six paper TEX/PDF by checksum and byte size.
The site publishes this manifest as `dist/data/rank6_document_revision.json`,
along with the current manuscript and verification-guide PDFs. It retains the
October 2 PDF addendum and the complete research-summary provenance chain.
Validation compares displayed counts with the classification ledger and model
catalogue, checks the exact frozen archive, and checks current PDFs against
their document revision rather than the historical archive's document hashes.

## 16 October theoretical update

The dated notice and proof table are generated from
`evidence/theoretical_20261016/decisions.json`; the number of new general
exclusions is derived from those records. The snapshot builder checks each
changed case against its current ledger, checks remaining-case IDs and totals,
and rejects a stale classification-status export. Scoped pivotal and unitary
results do not enter the general-exclusion count.

The proof bundle is `dist/downloads/theoretical-update-2026-10-16.zip`. Its
byte size and SHA-256 are displayed beside links to the decision records,
remaining-case inventory, and each theoretical proof. The frozen rank-six,
rank-seven and rank-eight supplements retain their existing names and hashes.
After freezing the proof manifest and current manuscripts, create the archive
from the classification repository with
`python3 tools/build_theoretical_20261016_archive.py`. That command checks the
frozen inputs and replays the default verifier from a clean extraction before
replacing the download. The extracted bundle documents which optional modes
need the full repository.
Run the snapshot builder only after the update archive and current status export
are ready. Supply the final immutable classification commit before publication
so all new proof and source links point to the verified release.

The Site audience remains owner-only. Local revisions do not deploy or change
access. On managed Linux, run browser preview only when the supported
`control-browser` skill is available; otherwise run the static and data checks
and report the visual-QA limitation.

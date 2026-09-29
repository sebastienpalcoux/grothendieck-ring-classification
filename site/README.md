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

## Rank-six revision · 29 September 2026

The complete 1345-file revised archive records **16,552 general exclusions,
54 realized rings and 6 unresolved cases** through multiplicity eight.
General classification is complete through multiplicity three; exact
completed bands are **1, 2, 3, 6, 7**. The fourth continuation adds 4 exclusions
and substantial exact finite-profile reductions at multiplicity four.

The site uses the authoritative rank-six ledger, current residual tensors,
revised paper and verification guide. Its validation checks archive and PDF
hashes and matches all counts to the release summary. The research source
and every earlier accepted certificate remain available in the revised ZIP.

Archive: `Rank6_Categorification_M8_Revised_2026-09-29_v4.zip`. SHA-256:
`e8ca671cbb20ab8f1b980d28e7cbd696b6f52cbfc5d36b0d09a2665a35df728b`.

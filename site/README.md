# Fusion & Grothendieck Ring Atlas

### [Explore the public atlas →](https://sebastienpalcoux.github.io/grothendieck-ring-classification/)

An interactive companion to the classification repository: filter the count
tables, inspect individual rings, read the current manuscripts and follow
the underlying evidence. GitHub Pages publishes the static `dist/` directory.

> [!IMPORTANT]
> **AI-generated research · independent verification pending.**
> The results, proofs, code and data have not yet been independently
> verified by human experts or formalized in Lean. Treat them as
> provisional and use them with caution. Automated checks establish only
> their stated computational scope.
> [Research status](../docs/RESEARCH_STATUS.md) ·
> [Verification guide](../docs/VERIFY.md).

## Reading the atlas

The main table counts rings with recorded categorical realizations. Partial
bands display **≥**: the recorded positive count is a lower bound while
unresolved fusion rings remain. The fusion-ring census counts all based
rings; counts alone never imply categorifiability. Multiplicity is the exact
maximum structure constant.

“Complete” describes the project's recorded coverage within the stated
range, subject to the research caution. Individual ring profiles show one
fusion matrix at a time and offer the full tensor for download. Character
data distinguish exact primitive-root formulas from numerical approximations.

The continuation records **35 decisions among 38 cases**: 28 proposed general
exclusions and 7 unitary constructions. General complex categorifiability
remains open for **R6_4_155, R6_8_1660 and R8_2_24**. Rank seven is complete
through multiplicity four. Rank eight records **895 exclusions, 77 models
and one open case** through multiplicity two; its complete contiguous range
ends at multiplicity one.

## Build and check locally

From the classification repository root:

```bash
python3 tools/restore_data.py
cd site
npm run check
npm run dev
```

To regenerate the website after the current manuscripts, document manifest,
classification export and proof bundle are ready:

```bash
python3 build_snapshot.py --classification ..
python3 build_realized.py --classification ..
npm run check
```

An optional `--classification-commit FULL_RELEASE_COMMIT_SHA` binds source
links to an immutable commit containing all referenced files. Without it,
source links follow the repository's main branch.

`build_snapshot.py` checks census coverage, classification partitions,
current PDF hashes, decision records and the proof bundle. It copies every
website PDF from the canonical source named by
`data/current_document_revision.json`. The manuscript shelf and ring
profiles link those current PDFs directly.

`build_realized.py` checks each catalogued tensor's rank, unit, duality and
associativity. It derives exact dual and invertibility data, approximate
Perron dimensions, and character information with its precision stated.
`smoke_test.py` checks count/model consistency, the three open cases,
canonical PDF copies, bundle identity and local page links.

## Publication

The repository's Pages workflow restores the bundled downloads, checks the
site and deploys `site/dist/` at:

**https://sebastienpalcoux.github.io/grothendieck-ring-classification/**

Relative links keep the atlas usable under this project path. The
[research-status page](dist/review.html) explains the remaining questions and
verification limits. The manuscripts and the download labelled **Proofs &
verification** present the current account.

Rebuild the portable bundle with
`python3 tools/build_review_20261017_archive.py`, then regenerate the snapshot
so its archive size and checksum match the downloadable bytes. Large
archives are stored as manifest-bound binary parts; `tools/restore_data.py`
reconstructs them before deployment.

## Source guide

| Path | Contents |
|---|---|
| `dist/index.html`, `styles.css`, `app.js` | Explorer, ring profiles, character tables and manuscript shelf. |
| `dist/review.html` | Current research status and verification scope. |
| `dist/data/atlas.json`, `grothendieck_counts.csv` | Positive counts and classification snapshot. |
| `dist/data/realized_rings.json` | Exact tensors, invariants and model sources. |
| `dist/data/counts.csv`, `classification_status.json` | Census bands and classification ledger. |
| `dist/data/current_document_revision.json` | Canonical manuscript sources and exact PDF checksums. |
| `dist/papers/`, `dist/downloads/` | Manuscripts, guides and reproducible proof materials. |
| `dev-preview.mjs` | Dependency-free local preview. |

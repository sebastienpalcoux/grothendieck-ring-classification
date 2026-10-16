# Fusion & Grothendieck Ring Atlas

### [Explore the public atlas →](https://sebastienpalcoux.github.io/grothendieck-ring-classification/)

An interactive companion to the classification repository: filter the count
tables, inspect individual rings, read the manuscripts and follow the
underlying evidence. The website is a static GitHub Pages publication of
`dist/`, with no credentials or runtime APIs.

> [!IMPORTANT]
> **AI-generated research · independent verification pending.**
> The results, proofs, code and data have not yet been independently
> verified by human experts or formalized in Lean. Treat them as
> provisional and use them with caution. Automated checks establish only
> their stated computational scope.
> [Research-status notice](../docs/RESEARCH_STATUS.md) ·
> [Prepublication review and dated errata](../docs/PREPUBLICATION_REVIEW.md).

## Reading the atlas

The main table counts rings with recorded categorical realizations. Partial
bands display **≥**: the recorded positive count is a lower bound while
unresolved fusion rings remain. The separate fusion-ring census counts
**all** based rings; counts alone never imply categorifiability. The ledger
keeps exclusions, positive models and general unresolved cases distinct.
Multiplicity is the exact maximum structure constant.

Only ranks with a classification manuscript and assessed bands are included.
“Complete” describes the current recorded coverage, subject to the research
notice and errata; it does not mean human verification or formal proof.
Individual ring profiles show one fusion matrix at a time and offer a full
tensor download. Character data distinguish exact primitive-root formulas
from approximate numerical tables.

## Build and check locally

From the classification repository root, restore the published datasets and
enter the site directory:

```bash
python3 tools/restore_data.py
cd site
npm run check
npm run dev
```

To regenerate the scientific snapshot from a reviewed repository checkout,
run from `site/`, replacing `FULL_RELEASE_COMMIT_SHA` with the immutable
commit that contains that research release:

```bash
python3 build_snapshot.py --classification .. --classification-commit FULL_RELEASE_COMMIT_SHA
python3 build_realized.py --classification ..
npm run check
```

`build_snapshot.py` rejects missing census bands, cumulative mismatches and
status partitions that do not sum to census counts. `build_realized.py`
checks each catalogued tensor's rank, unit, duality and associativity. It
derives exact dual and invertibility data and approximate Perron dimensions.
For commutative rings it supplies exact codegree polynomials and an exact
primitive-root character presentation. For noncommutative models it derives
numerical irreducible trace characters from the exact center kernel, checks
block dimensions and orthogonality, and attaches exact individual codegree
polynomials using the central Casimir and the numerical block matching.
Numerical values are marked as approximations. `smoke_test.py` checks count
and model consistency and the provenance of the current research snapshot.

## Public publication

GitHub Pages serves the contents of `site/dist/` at:

**https://sebastienpalcoux.github.io/grothendieck-ring-classification/**

The repository's Pages workflow restores the bundled downloads, checks the
static site and deploys the artifact. Relative asset and download links keep
the website usable under this project path. Presentation changes do not
require regenerating the scientific data or changing an immutable research
commit. The live website updates after a successful deployment; committed source is
public in the repository.

The earlier owner-only working website is a separate deployment. The GitHub
Pages address above is the public destination linked from this repository.

## Source guide

| Path | Contents |
|---|---|
| `dist/index.html`, `styles.css`, `app.js` | Responsive explorer, ring profiles, character tables, references and manuscript shelf. |
| `dist/data/atlas.json`, `grothendieck_counts.csv` | Generated positive counts and classified census-band snapshot. |
| `dist/data/realized_rings.json` | Exact tensors, selected invariants and model source pointers. |
| `dist/data/counts.csv`, `classification_status.json` | Census bands, provenance and the per-band classification ledger. |
| `dist/papers/`, `dist/downloads/` | Manuscripts, guides and reproducible research bundles. |
| `dev-preview.mjs` | Dependency-free local preview. |

## Current research snapshot

The classification counts come from the current release ledger; models,
exact fusion tensors and references come from the model catalogue. The
rank-six residual summary applies the October 2, October 11 and October 16
research overlays in order, checking each previous-source path and checksum
and unchanged classification totals. Its latest overlay is
`evidence/unified_20261016/rank6/research_progress.json`.
`R6_4_155` and `R6_8_1660` remain unresolved.

The frozen October 1 archive, release identity, ledger and per-band counts
are checked separately from the current manuscript. The current
`evidence/unified_20261016/rank6/document_revision.json` binds the latest
research overlay to each rank-six paper's TeX/PDF checksum and byte size.
The site publishes that manifest as `dist/data/rank6_document_revision.json`,
together with the current manuscript and verification-guide PDFs. It retains
the October 2 PDF addendum and the research-summary provenance chain. The
checks compare current PDFs with their document revision, rather than the
historical archive's document hashes.

The [17 October correction](../evidence/review_20261017/README.md) reopens
`R8_2_24` because its proposed categorical-to-linear bridge is unproved.
The latest continuation retains 35 accepted decisions among 38 former
residuals: 28 proposed exclusions and 7 unitary constructions. Rank seven
is complete through multiplicity four; rank eight is complete through one,
with 895 exclusions, 77 models and one open case through multiplicity two.
The three general open questions are `R6_4_155`, `R6_8_1660`, and `R8_2_24`.
The current review-stage `ALL38_COVERAGE.md` accounts for every original case.
The frozen unified36 snapshot and manuscripts remain historical and must
be read alongside the dated errata.

The snapshot builder compares changed cases with their current ledgers,
remaining IDs, totals, proof bundle and manuscript hashes. Build the current
bundle from the repository root with
`python3 tools/build_review_20261017_archive.py`; it checks the current
correction and preserved parent files before replacing `review-update-2026-10-17.zip`.
The unified archive must remain the unchanged historical36 snapshot.
The review bundle includes the dated errata, corrected reading edition when
available, audit receipts and public replay instructions. For a ZIP larger
than 12 MiB, its builder updates `data/large_files_manifest.json` with raw
6 MiB parts and ignores the generated ZIP in Git. Publish those parts and
the manifest; API-based upload inventories must also omit the direct ZIP.
`tools/restore_data.py` reconstructs the download before the Pages build.
Refresh the site snapshot after rebuilding the archive so its size and hash
match the downloadable bytes.
Earlier dated archives remain historical snapshots with unchanged names and
hashes. Regenerate the snapshot only after the archive and status export are
ready, and supply the immutable classification commit so source links identify
the research release.

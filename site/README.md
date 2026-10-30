# Fusion & Grothendieck Ring Atlas

[Explore the public Atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/) · [Theory and definitions](dist/theory.html) · [Current manuscripts](../manuscripts/README.md)

**Complete census directory.** Every one of the **1,434,042** released census rings at ranks 3–12 has an individual record. The **3,462** existing detailed profiles remain available, including two rank-two realizations outside this finite census. [Coverage, exact basis maps, structural filters and deployment checks](FULL_CENSUS.md).

> **AI-generated research · independent verification pending.** Automated checks and agent audits establish only their stated scope. Independent human verification and formalization remain pending.

## Browse the mathematics

All ranks through twelve use the same [record directory](https://sebastienpalcoux.github.io/grothendieck-ring-classification/records.html), model catalogue, manuscript shelf and [open-case list](https://sebastienpalcoux.github.io/grothendieck-ring-classification/unresolved.html). Choose the full census or detailed profiles. Records are ordered by rank, exact multiplicity and identifier; the directory shows 24 per page and loads tensors only on request.

The shared selectors cover integral, weakly integral, simple, perfect, pointed, commutative, self-dual and multiplicity-free rings. Their flags cover the entire census and are derived from exact tensors. The [theory page](dist/theory.html) states definitions and mainstream references. Aggregate count tables retain their full recorded populations. Missing detailed documentation never means unresolved categorification.

A case page presents its current categorical status, precise research scope, invariants and one fusion matrix at a time. Every tensor is downloadable as a Python list; the convention is `N[i][j][k] = [X_i X_j:X_k]`, with unit `X_0`. Model existence means at least one categorification, not a classification of associators.

Six cases remain unresolved: R6_4_155, R6_8_1660, R8_3_928, R8_3_941, R8_3_1154 and R9_2_137. R8_3_1768 is generally excluded by pivotal conjugation parity and the complete necessary indicator system. The [current proof account](../evidence/frontier/README.md) states the inherited general-complex gate, exact replay and remaining categorical gaps. The latest continuation excludes three R928 center patterns and the positive TY branch of R137. R928’s surviving positive spherical center must have rank 40 and split as Sem⁻ ⊠ B, with B of rank 20 (or the conjugate orientation). [Anyon Atlas B20-02148](https://anyonatlas.org/data/B20-02148) supplies exact candidate modular data for B; uniqueness of the full data is unproved, and no category or required algebra is constructed. All 28 current finite checks passed. Necessary-condition witnesses are not models.

The [“New” constructions catalogue](https://sebastienpalcoux.github.io/grothendieck-ring-classification/constructions.html) collects the project’s documented shortlist, ordered by rank, multiplicity and identifier. “New” means only that a specific construction has not, to our knowledge, been explicitly recorded in the literature; it does not claim novelty up to tensor equivalence or exoticness. Each entry credits its known ingredients and links to its construction proof and complete case record.

## Build and verify

The [current proof and publication account](../evidence/frontier/README.md) gives the accepted source bindings and replay commands. After selecting that publication and generating its data, consolidate the reader presentation and version the local assets:

```bash
python3 site/current_presentation.py
python3 site/version_assets.py
```

`current_presentation.py` is also called by `build_snapshot.py`. Run it after any retained historical synchronizer: it presents the current classification once and does not change accepted decisions. The canonical manuscripts, website copies, page counts and SHA-256 bindings are recorded in `data/current_publication_revision.json`. Current reproducibility materials are linked through `evidence/frontier/README.md` and the stable download `Fusion-Ring-Frontier-Proofs-and-Checks.zip`.

`dist/data/constructions.json` curates the construction examples. After updating it or the linked catalogue records, run `python3 site/build_constructions.py` from the repository root. The `--check` mode checks accepted model status, tensor-bound property flags, proof-source paths and the generated HTML. All entries remain readable without JavaScript; the shared filters are an enhancement.

For the local viewer:

```bash
python3 site/build_full_census.py
python3 site/version_assets.py
cd site
npm run check
npm run dev
```

The complete-census builder needs a C++17 compiler and Boost headers. Its pinned source downloads are cached; it indexes existing data without running an enumeration. `npm run census:check` independently roundtrips every source tensor and checks sampled properties and browser data queries. [Full design and checks](FULL_CENSUS.md).

`build_ring_properties.py` recomputes exact property flags after catalogue sources change. `check_cases.py`, the high-rank checks and `smoke_test.py` validate tensors, counts, source bindings and current PDF copies. `verify_current_publication.py` also validates the accepted research transitions; historical replays remain separately scoped.

## Publication

The GitHub Pages workflow restores checksummed payloads, runs the publication checks and deploys `site/dist/` to the public Atlas. Relative links work under the project path. The former private Atlas is not a publication target.

| Path | Contents |
|---|---|
| `dist/index.html`, `app.js` | Shared explorer, counts, model catalogue and manuscript shelf. |
| `dist/catalogue.js`, `records.html` | Common record loading and ordered filters for all ranks. |
| `dist/census.js`, `census.css`, `data/full-census/` | Complete census browsing, exact filters, bounded tensor chunks and individual profile loading. |
| `dist/case.html`, `cases.js` | Case status, research, fusion matrices and curated sources. |
| `dist/constructions.html`, `constructions.js`, `constructions.css` | Curated construction examples, their limited novelty scope, and filters. |
| `dist/unresolved.html` | Current open cases with shareable rank and multiplicity filters. |
| `dist/review.html`, `theory.html` | Research scope, definitions and references. |
| `dist/data/`, `dist/papers/`, `dist/downloads/` | Exact records, canonical manuscripts and verification materials. |

## Rank-twelve extension

Run `python tools/sync_rank12_publication.py`, `python site/build_ring_properties.py`, and `python site/build_constructions.py` after selecting the canonical rank-twelve PDF. The standard shared catalogue integrates `rank12_m1.json` alongside the other ranks; there is no separate rank-twelve interface. `python site/check_rank12.py` validates all 632 records and the complete proof archive. Status `pseudo_unitarily_realized` is a realized complex ring with a pseudo-unitary model, with unitarity unproved. It belongs to all-realizations filters but not unitary-only filters.

After rebuilding case data and exact flags, run `python site/version_catalogue.py` before publication. It versions all mutually bound JSON fetches together, then versions the catalogue asset in every shared page. CI checks this fingerprint to prevent stale mixed snapshots.

Publication helpers have [explicit version bindings](../evidence/frontier/publication_replacements.json), with their original implementations preserved as proof-checkpoint inputs. Updating display metadata does not change the frozen categorical decisions or mathematical checks.

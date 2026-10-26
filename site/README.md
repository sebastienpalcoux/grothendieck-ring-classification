# Fusion & Grothendieck Ring Atlas

[Explore the public Atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/) · [Theory and definitions](dist/theory.html) · [Current manuscripts](../manuscripts/README.md)

**24 October 2026:** rank ten is complete at multiplicity one: **136 general exclusions and 58 unitary models**. R10_1_189 is recognized inside the classical SU(4)_6 conformal-embedding module category. Ten rings remain open at ranks six, eight and nine. [Current proofs and precise scope](../evidence/unresolved_retry_20261024/README.md).

> **AI-generated research · independent verification pending.** Automated checks and agent audits establish only their stated scope. Independent human verification and formalization remain pending.

## Browse the mathematics

All ranks through eleven use the same [record directory](https://sebastienpalcoux.github.io/grothendieck-ring-classification/records.html), model catalogue, manuscript shelf and [open-case list](https://sebastienpalcoux.github.io/grothendieck-ring-classification/unresolved.html). Records are ordered by rank, exact multiplicity and identifier; the directory shows 24 per page.

The shared selectors cover integral, weakly integral, simple, perfect, pointed, commutative, self-dual and multiplicity-free rings. Their flags are derived from exact tensors. The [theory page](dist/theory.html) states definitions and mainstream references. Aggregate count tables retain their full recorded populations.

A case page presents its current categorical status, precise research scope, invariants and one fusion matrix at a time. Every tensor is downloadable as a Python list; the convention is `N[i][j][k] = [X_i X_j:X_k]`, with unit `X_0`. Model existence means at least one categorification, not a classification of associators.

The ten open cases retain their general unresolved status. R928 has categorical Morita rigidity. The actual twisted GH(C6,2) precursor for R1768 still requires an algebra 1+sigma. The new rank-nine center and Clifford restrictions do not give further ring exclusions. The repaired R436 exclusion uses an independent spherical-equivariantization proof; its old TPE completeness premise remains withdrawn.

The [“New” constructions catalogue](https://sebastienpalcoux.github.io/grothendieck-ring-classification/constructions.html) collects the project’s documented shortlist, ordered by rank, multiplicity and identifier. “New” means only that a specific construction has not, to our knowledge, been explicitly recorded in the literature; it does not claim novelty up to tensor equivalence or exoticness. Each entry credits its known ingredients and links to its construction proof and complete case record.

## Build and verify

From the repository root, restore manifest-bound files and synchronize the current accepted publication:

```bash
python3 tools/restore_data.py
python3 tools/sync_research_revision.py
python3 tools/render_publication_docs.py
python3 tools/render_readme.py
python3 tools/verify_unresolved_retry.py
```

The synchronization validates accepted tensor-bound decisions. It does not discover a categorification by passing necessary numerical tests. Earlier campaign builders recreate their historical stages; the current synchronization must follow them.

The usual manuscripts are the canonical sources in `data/current_publication_revision.json`. Their website PDF copies, page counts and SHA-256 bindings are refreshed together. The focused [current proof archive](../evidence/unresolved_retry_20261024/replay.zip) contains the portable exact checks; earlier archives retain their dated scope.

`dist/data/constructions.json` curates the construction examples. After updating it or the linked catalogue records, run `python3 site/build_constructions.py` from the repository root. The `--check` mode checks accepted model status, tensor-bound property flags, proof-source paths and the generated HTML. All entries remain readable without JavaScript; the shared filters are an enhancement.

For the local viewer:

```bash
cd site
npm run check
npm run dev
```

`build_ring_properties.py` recomputes exact property flags after catalogue sources change. `check_cases.py`, the high-rank checks and `smoke_test.py` validate tensors, counts, source bindings and current PDF copies. `verify_current_publication.py` also validates the accepted research transitions; historical replays remain separately scoped.

## Publication

The GitHub Pages workflow restores checksummed payloads, runs the publication checks and deploys `site/dist/` to the public Atlas. Relative links work under the project path. The former private Atlas is not a publication target.

| Path | Contents |
|---|---|
| `dist/index.html`, `app.js` | Shared explorer, counts, model catalogue and manuscript shelf. |
| `dist/catalogue.js`, `records.html` | Common record loading and ordered filters for all ranks. |
| `dist/case.html`, `cases.js` | Case status, research, fusion matrices and curated sources. |
| `dist/constructions.html`, `constructions.js`, `constructions.css` | Curated construction examples, their limited novelty scope, and filters. |
| `dist/unresolved.html` | Current open cases with shareable rank and multiplicity filters. |
| `dist/review.html`, `theory.html` | Research scope, definitions and references. |
| `dist/data/`, `dist/papers/`, `dist/downloads/` | Exact records, canonical manuscripts and verification materials. |

## Rank-twelve extension

Run `python tools/sync_rank12_publication.py`, `python site/build_ring_properties.py`, and `python site/build_constructions.py` after selecting the canonical rank-twelve PDF. The standard shared catalogue integrates `rank12_m1.json` alongside the other ranks; there is no separate rank-twelve interface. `python site/check_rank12.py` validates all 632 records and the complete proof archive. Status `pseudo_unitarily_realized` is a realized complex ring with a pseudo-unitary model, with unitarity unproved. It belongs to all-realizations filters but not unitary-only filters.

After rebuilding case data and exact flags, run `python site/version_catalogue.py` before publication. It versions all mutually bound JSON fetches together, then versions the catalogue asset in every shared page. CI checks this fingerprint to prevent stale mixed snapshots.

# Fusion & Grothendieck Ring Atlas

[Explore the public Atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/) · [Theory and definitions](dist/theory.html) · [Current manuscripts](../manuscripts/README.md)

**24 October 2026:** rank ten is complete at multiplicity one: **136 general exclusions and 58 unitary models**. R10_1_189 is recognized inside the classical SU(4)_6 conformal-embedding module category. Ten rings remain open at ranks six, eight and nine. [Current proofs and precise scope](../evidence/unresolved_retry_20261024/README.md).

> **AI-generated research · independent verification pending.** Automated checks and agent audits establish only their stated scope. Independent human verification and formalization remain pending.

## Browse the mathematics

All ranks through eleven use the same [record directory](https://sebastienpalcoux.github.io/grothendieck-ring-classification/records.html), model catalogue, manuscript shelf and [open-case list](https://sebastienpalcoux.github.io/grothendieck-ring-classification/unresolved.html). Records are ordered by rank, exact multiplicity and identifier; the directory shows 24 per page.

The shared selectors cover integral, weakly integral, simple, perfect, pointed, commutative, self-dual and multiplicity-free rings. Their flags are derived from exact tensors. The [theory page](dist/theory.html) states definitions and mainstream references. Aggregate count tables retain their full recorded populations.

A case page presents its current categorical status, precise research scope, invariants and one fusion matrix at a time. Every tensor is downloadable as a Python list; the convention is `N[i][j][k] = [X_i X_j:X_k]`, with unit `X_0`. Model existence means at least one categorification, not a classification of associators.

The ten open cases retain their general unresolved status. R928 has categorical Morita rigidity. The actual twisted GH(C6,2) precursor for R1768 still requires an algebra 1+sigma. The new rank-nine center and Clifford restrictions do not give further ring exclusions. The repaired R436 exclusion uses an independent spherical-equivariantization proof; its old TPE completeness premise remains withdrawn.

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
| `dist/unresolved.html` | Current open cases with shareable rank and multiplicity filters. |
| `dist/review.html`, `theory.html` | Research scope, definitions and references. |
| `dist/data/`, `dist/papers/`, `dist/downloads/` | Exact records, canonical manuscripts and verification materials. |

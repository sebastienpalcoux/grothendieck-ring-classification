# Complete census records

The [case directory](https://sebastienpalcoux.github.io/grothendieck-ring-classification/records.html)
provides a permanent record for all **1,434,042** released based-isomorphism
classes at ranks 3–12. It preserves the **3,462** existing research profiles:
3,460 identify census classes, and two are the separate rank-two realizations.
There is no categorifiability filter on census membership.

The source snapshot and all compressed and uncompressed tensor hashes are in
[`census_sources.json`](census_sources.json). The mathematical classification
snapshot is pinned separately. This change transports existing decisions; it
introduces no new categorical models or exclusions.

## Identifiers, basis and classification

`C{rank}_{multiplicity}_{index}` identifies the one-based position **within the
exact-multiplicity band in the pinned census export**. The source line in the
whole-rank file is also displayed. The original tensor basis is retained.

Existing `R…` and `F_{…}` identifiers keep their previous meanings and URLs.
They are research-catalogue identifiers, which must not be assigned to new
census entries by assuming identical numbering. Every profile is connected to
exactly one census class by a unit-fixing permutation `p` satisfying
`source[i][j][k] == profile[p[i]][p[j]][p[k]]` for **all** coefficients.
Both tensor hashes and the permutation are exported in `profile_bindings.json`.
No profile is matched using counts, dimensions, numerical tolerance or a
non-exhaustive invariant alone.

The accepted modeled and unresolved classes are all identified exactly. The
remaining census classes carry the exclusion status of their published band
classification. Every band is checked against the accepted summary for its
total, exclusions, models and unresolved cases. A basic record cites that band
classification and the rank manuscript; it does not invent a case-specific
criterion or claim that its exclusion route was rerun during this build.

Missing detailed documentation is distinct from an unresolved decision. The
full census has 1,433,502 exclusions, 530 modeled classes and 10 unresolved
classes. The 530 models retain their original scope: 528 have unitary models,
one has the recorded non-pseudo-unitary model, and R12_1_623 has a pseudo-unitary
model with unitarity unproved. The two rank-two realizations are outside these
finite-census totals.

These identifiers are frozen to this source snapshot. A future larger census
must preserve this registry and its basis maps or introduce an explicitly
versioned namespace. Reordering a new export must never silently recycle an
existing C identifier.

## Exact structural properties

All eight property filters cover the **entire census**, independently of its
categorical status. `census_properties.cpp` checks the unit, duality and
Frobenius-reciprocity identities while reading the already verified input.

Pointedness and perfectness use exact products with the dual. Commutativity,
self-duality and multiplicity freedom use direct coefficient tests. Simplicity
means that every nonunit generator and its dual generate the whole based ring;
closure is computed using finite support bitsets.

The dimension tests use exact bounds, not rounded eigenvalues. For any
nonnegative matrix `A` and positive rational vector `v`, the Perron root lies
between the minimum and maximum of `(Av)_j/v_j`. Integer arithmetic computes
the possible integers in this interval. A floating iteration of the positive
sum of the fusion matrices only **proposes** `v`; its accuracy is never an
acceptance criterion. Exact integer power vectors provide a bounded fallback.

For integrality, an empty integer interval for any fusion matrix proves
nonintegrality. If every interval contains a unique integer `d_i`, the code
checks positivity, `d_0=1` and every identity
`sum_k N[i][j][k] d_k = d_i d_j`. Passing gives the positive dimension character;
failing rules out the only possible integral one in these bounds.

For weak integrality, Frobenius reciprocity gives `N_i^T = N_{i*}`. The
nonnegative symmetric Casimir matrix `Omega = sum_i N_i N_i^T` has the positive
dimension vector as eigenvector and Perron eigenvalue `sum_i d_i^2`. If its
interval has one integer candidate `D`, the code checks exactly that
`D I - Omega` is positive semidefinite and singular. Fraction-free symmetric
elimination uses arbitrary-precision integers, verifies every division, and
handles zero pivots by requiring the remaining pivot row to vanish. This
decides whether `D` is the largest eigenvalue. Empty integer intervals prove
nonintegrality of the global dimension. An undecided bound fails the build;
it is never encoded as “No”.

The native implementation was compared with the independent symbolic
characteristic-polynomial/root-isolation implementation on **all 3,462 existing
profiles**. Publication checks additionally compare deterministic samples
throughout every rank, including the large-multiplicity census regions.
These checks establish their stated computational scope; independent human
verification and formalization remain pending.

## Static hosting and phone behavior

One shared HTML template serves every individual URL. No million-page HTML
tree or database server is needed. The generated Pages artifact contains:

| Data | Loading policy |
|---|---|
| Manifest and compressed profile index | Counts, band histograms and search metadata; no tensors. |
| Band indexes | Requested bands only; gzip-compressed; each decoded row stores a source line and exact flags in six bytes. |
| Tensor hash indexes | Only the rank of an opened/downloaded census record. |
| Tensor chunks | Gzip-compressed, at most **32,768 decoded bytes**; little-endian unsigned 16-bit coefficients. The current largest network payload is 8,323 bytes. |
| Detailed JSON profiles | Individually compressed; only the requested profile is loaded, preserving its original data and evidence. |

The browser verifies the byte length and SHA-256 of every fetched index, tensor
chunk and detailed profile before decoding, then checks the decoded length.
The pinned MIT-licensed fflate 0.8.2 decoder and its license are bundled locally;
its official npm package integrity and source SHA-256 are recorded in the
source configuration. No browser-specific decompression API is required.
Compressed binary payloads use `.bin` filenames with their encoding declared
in the manifest. All payload URLs are hash-versioned. The manifest
version is bound to the pinned configuration, current mathematical inputs and
indexer source. Stale or corrupt data produces a visible error, never a record
from mixed snapshots. A small bounded cache avoids retaining the census in
browser memory.

Histograms give complete filter counts and allow pagination to skip unloaded
bands. At most 24 cards are displayed. Every property and status selector has
the same meaning in the full census and detailed-profile views. Text searches
cover documented model/criterion metadata; exact C identifiers locate any
census ring. Unreleased multiplicity bands are explicitly distinguished from
zero counts. Shareable URLs preserve filters and page number. Phone controls
wrap, targets remain touch-sized, and wide fusion matrices scroll locally.

The artifact builder rejects sites larger than 950 MB, below the current
[GitHub Pages 1 GB published-site limit](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits).
Generated data are excluded from Git and recreated from checksummed released
exports during deployment. The complete new browsing data occupy approximately
46 MB compressed; the full site, including all retained older downloads,
occupies approximately 906 MB. Visitors never download that artifact as a whole.

## Build and verify

Requirements: Python 3.12, g++ with C++17, Boost headers; SymPy 1.14.0 for
independent sampled property checks. On Ubuntu the header package is
`libboost-dev`. No census search is run.

```bash
python tools/restore_data.py
python site/build_full_census.py
python site/version_assets.py
python site/check_full_census.py --full --property-samples
node site/tests/check_full_census.mjs
```

The complete roundtrip audit independently parses all **1,434,042** original
source lines using Python's JSON parser, compares every coefficient with the
published binary chunks, checks every band and file hash, and verifies every
profile basis map. Browser tests check broad and combined filters, first/last
pages, profile aliases, bounded requests, invalid addresses, retained model
scope and phone layout. `--check` on the builder regenerates the artifact and
requires the committed browser fingerprint to match.

After an authorized mathematical-data update, review the pinned source and
summary hashes, preserve existing C identifiers, rebuild this artifact and
refresh asset fingerprints. A change in classification input must not bypass
the snapshot or transport checks.

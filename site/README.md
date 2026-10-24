# Fusion & Grothendieck Ring Atlas

<!-- current-audit-correction -->
**24 October audit correction.** R8_3_436 is unresolved for general complex
categorification; its unitary exclusion is retained. Rank eight through
multiplicity three now has 4,402 general exclusions, 93 models and five open
cases. With the rank-nine M2 continuation, the current project-wide total is
26 open cases. Earlier dated ledgers and replay receipts keep their historical
scope. [Correction and precise hypotheses](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/audit_20261024/README.md).
<!-- /current-audit-correction -->

**Rank ten, multiplicity one:** 136 general complex exclusions, 57 unitary models and one unresolved ring, R10_1_189. The five quadratic exclusions and the proved cyclic restrictions use the common case directory. [Current proof package](../evidence/rank10_m1_exclusions_20261023/README.md).

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

All ranks through 11 use the same explorer, model catalogue, manuscript shelf
and [case directory](https://sebastienpalcoux.github.io/grothendieck-ring-classification/records.html).
The directory orders profiles by rank, exact multiplicity and identifier, with
24 records per page and shared status/search filters. Source datasets stay
separately checksummed; they do not create separate rank-specific views.
Previously shared release-directory URLs redirect to this common directory.

The main table counts rings with recorded categorical realizations. Partial
bands display **≥**: the recorded positive count is a lower bound while
unresolved fusion rings remain. The fusion-ring census counts all based
rings; counts alone never imply categorifiability. Multiplicity is the exact
maximum structure constant.

“Complete” describes the project's recorded coverage within the stated
range, subject to the research caution. Individual ring profiles show one
fusion matrix at a time and offer the full tensor for download. Character
data distinguish exact primitive-root formulas from numerical approximations.

Unresolved counts link to a dedicated case list, scoped to the selected rank
and exact multiplicity or cumulative bound. The [unresolved directory](https://sebastienpalcoux.github.io/grothendieck-ring-classification/unresolved.html)
also lists every current open case. Each identifier opens a separate profile
with its fusion matrices, exact and approximate invariants, recorded research
results, and evidence sources. Use `unresolved.html?rank=8&m=3` for an exact
band or `unresolved.html?rank=8&max_m=3` for a cumulative bound.

Each unresolved profile highlights the strongest recorded obstruction among
pivotal, spherical, pseudo-unitary and unitary categorification. Its implication
diagram distinguishes structures admitted by the same category from existence
after Galois conjugation. Double arrows include proved reverse implications for
that ring, with supporting arguments linked below. The audited source is
[`categorification_scope.json`](categorification_scope.json); see
[`CATEGORIFICATION_SCOPE.md`](CATEGORIFICATION_SCOPE.md) for the conventions.

A separate braided-categorification panel records exclusions that apply
without a pivotality assumption, or the weakest additional assumption needed
for a conditional obstruction. All six earlier rank-six and rank-eight unresolved cases exclude
general braided categorification; the four rank-eight cases also exclude every
braided Morita representative. These exclusions also remain valid for the
newly realized R8_3_982.
See [`BRAIDED_CATEGORIFICATION.md`](BRAIDED_CATEGORIFICATION.md) for the proofs
and exact replay. These restrictions do not resolve general categorification
without requiring a braiding.

Every unresolved profile and realized model offers a `.txt` download containing
only a Python list of lists of lists of integers. In the displayed basis,
`N[i][j][k]` is the coefficient of `X_k` in `X_i * X_j`, and `X_0` is the unit.
Load the file with `ast.literal_eval`; no executable Python is needed.

The historical 38-case continuation records 36 decisions: 29 proposed general exclusions and seven unitary constructions. Its two rank-six questions, `R6_4_155` and `R6_8_1660`, remain open.

The rank-seven multiplicity-five continuation addresses all 5,805 supplied exact-multiplicity-five rings: 5,804 general exclusions, 1 realization and 0 unresolved cases. The classification of the supplied census is complete through multiplicity 5. The new realization R7_5_5678 is Rep(AGL(1,7)).

The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,506 general exclusions, 16 models and 5 unresolved cases. Every recorded model admits a unitary realization. The remaining rings retain unresolved status for general complex categorification; R8_3_436 retains its unitary exclusion.

The rank-eight candidate audit distinguishes completed necessary-condition tests, unsuccessful model searches, ineligible tests and time limits. Scoped unitary obstructions preserve the general complex question; these candidates are not asserted fusion categories or established exotic examples.

Canonical normal and optimized frontier replays each passed all 108 checks. These receipts cover the historical frontier stage. Fresh replay after extraction from the publication archive is deferred.

The separate center-pattern addendum passed all eight checks in canonical normal and optimized Python, including independent arithmetic reconstructions and positive controls. Fresh replay after extraction from the publication archive is deferred.

R8_3_3472 admits no fusion categorification over the complex numbers. The sphericalization and Galois reduction covers general complex categories; complete center-frame and twist-orbit domains reduce the remaining case to 628 exact equations in 572 integer variables. A certificate of 1648 rational bound deductions and a final strictly positive separating gap proves infeasibility, with two independent exact checkers. The proof and reproducible certificate are in evidence/r3472_exclusion_20261022/. This complete obstruction supersedes the earlier feasible necessary systems and conditional Morita restrictions for R3472. R8_3_982 remains unitarily realized by the neutral triality component of the exceptional E21 chiral fusion category, with all 512 canonical fusion coefficients identified exactly. Apart from R8_3_436, four rank-eight general categorification questions remain: R8_3_928, R8_3_941, R8_3_1154 and R8_3_1768. Every hypothetical categorification of these four rings admits a spherical structure and has a pseudo-unitary Galois conjugate; none has a braided Morita representative. The R928 phase refinement leaves four of ten necessary center patterns, all fourteen R941 allocations survive the stated refinements, and R1154 retains its forced semionic data. R1768 has 39 of 40 necessary Gram/indicator branches excluded, while its final cone survives. These necessary data do not construct categories or settle the four remaining questions.

Ranks two, three and four have unrestricted complex classifications. The
rank-four manuscript proves that exactly 15 rings occur and every
categorification admits a spherical structure. Its theoretical reduction
to FPdim < 1000 and multiplicity at most 31 is followed by an exact
1,692-ring census. The sharp bounds are FPdim ≤ 24+12√3 and multiplicity ≤ 6.
For the pivotal case, see Dong, Palcoux and Plessis,
[Classifying Grothendieck rings of pivotal fusion categories of rank four](https://arxiv.org/abs/2609.33272).

## Exact structural filters and mathematical introduction

The model catalogue, common record directory and unresolved list share eight
independent selectors: integral, weakly integral, simple, perfect, pointed,
commutative, self-dual and multiplicity-free. “Any / Yes / No” supports
intersections and complements. Selected properties are retained in shareable
URLs. Aggregate count tables retain their full census populations.

[Theory and definitions](dist/theory.html) introduces the objects, dimensions,
filter conventions and categorical existence statuses, with standard references.

`build_ring_properties.py` derives the flags from exact tensors. Integrality uses
rational isolation of the largest real roots of integral fusion and Casimir
polynomials; it never rounds numerical dimensions. Simplicity uses complete
generated dual-closed based-subring closures. The output binds every source JSON
and tensor digest. Run `python3 site/build_ring_properties.py` from the repository
root after rebuilding any catalogue source. Tests include Fibonacci, Ising,
Rep(S3), a pointed prime-order ring and misleading integer eigenvalue controls.

To refresh the audited current publication, run from the repository root:

```bash
python3 tools/reader_resources.py
python3 tools/build_current_document_revision.py
python3 tools/sync_audit_revision.py
python3 tools/verify_audit_revision.py
```

The audit synchronizer preserves the later rank-nine M2 data. Earlier campaign
builders recreate their historical stage; they must be followed by this current
synchronization. Old proof archives keep their literal historical scope; current
PDFs and corrected decision records are linked separately.

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
python3 build_cases.py --classification ..
python3 build_rank9_10.py --classification ..
python3 build_rank11.py --classification ..
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
`build_cases.py` assembles current unresolved profiles from the canonical
tensors and case-specific research records and writes individual Python-list
text downloads for both unresolved and realized rings. Formerly unresolved
pages remain available after exclusion or realization, with their historical
research records and current status. Regenerate it after
the snapshot and realized catalogue whenever the classification changes.
`smoke_test.py` checks count/model consistency, the complete current open-case inventory,
canonical PDF copies, bundle identity and local page links. Its case checks
also parse every tensor download and compare its entries and digest with
the published records.

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
| `dist/catalogue.js`, `dist/records.html` | Shared case loading and filtered directory for all ranks. |
| `dist/review.html` | Current research status and verification scope. |
| `dist/data/atlas.json`, `grothendieck_counts.csv` | Positive counts and classification snapshot. |
| `dist/data/realized_rings.json` | Exact tensors, invariants and model sources. |
| `dist/data/counts.csv`, `classification_status.json` | Census bands and classification ledger. |
| `dist/data/current_document_revision.json` | Canonical manuscript sources and exact PDF checksums. |
| `dist/papers/`, `dist/downloads/` | Manuscripts, guides and reproducible proof materials. |
| `dev-preview.mjs` | Dependency-free local preview. |

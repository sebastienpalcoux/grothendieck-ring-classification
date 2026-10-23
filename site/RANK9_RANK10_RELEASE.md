# Rank-nine and rank-ten release

This additive publication preserves the existing rank-two through rank-eight
JSON records byte for byte. The browser combines the new release with the old
atlas, realized catalogue and unresolved directory. Each new identifier has a
permanent `case.html?id=R9_1_…` or `case.html?id=R10_1_…` profile and a Python-list
TXT tensor download, including excluded and deferred cases.

Ranks nine and ten use the common atlas table, model catalogue and manuscript
shelf. The shared `records.html` directory filters every rank by rank, exact
multiplicity, status and search text; the former release-directory URL redirects
to this common view.
Individual profiles reuse the existing ordered case renderer: current findings,
invariants, characters, fusion data, then evidence. Supporting reports and the
searchable evidence catalogue remain folded by default.

## Canonical source

Place the portable research package at
`evidence/rank9_rank10_m1_20261023/`, retaining its relative paths:
`README.md`, `verify.py`, `manifest.json`, `inputs/`, `work/`, and `deliverable/`.
The builder reads `deliverable/ledger.json` and
`work/input_audit/tensors.json`; it never infers a categorical decision from a
tensor or a successful numerical test. Counts are derived from all individual
records and checked against the ledger totals.

An optional `deliverable/case_notes.json` maps identifiers to `summary`,
`deferred`, `evidence` (relative file paths), `research` (paragraph strings or title/source/data objects), and
an independently audited `categorification_scope`. Deferred records must remain
`unresolved`. For the six specifically audited deferred identifiers, the builder renders the
signed-sphericalization and Galois-existence reductions as distinct diagrams,
citing the independent replay and dimension-character receipts. If no note is
supplied, the profile makes no additional claims.

## Build order

Run the existing snapshot, realized and case builders first, if rebuilding them.
Then run the additive builder last: the legacy case builder intentionally prunes
tensor downloads outside its historical inventory.

```bash
python3 site/build_rank9_10.py --release evidence/rank9_rank10_m1_20261023
python3 site/check_rank9_10.py
python3 -O site/check_rank9_10.py
node --check site/dist/catalogue.js
node site/check_cases.mjs
```

For staging, `--source /absolute/package/root` reads a package outside the repo;
all public evidence URLs still use the canonical `--release` path. `--ref SHA`
binds links to an immutable publication commit. Re-run the builder against the
final accepted ledger immediately before publication.

The extension does not rewrite legacy aggregates or historical receipt scopes.
`rank9_rank10_m1_build.json` records their pre-build hashes, and the checker
verifies that they remain unchanged. The existing site smoke tests remain in
force; the additional checker covers the 336 new records and every TXT download.

## Integration checkpoint

Prepared from canonical `main` at
`7f4aea6fb5e5a98aa9e5e5dc78a58bd46c1c92e1` on 23 October 2026.
The dedicated local branch is `codex/rank9-10-publication`.
No publication push is part of this staging work.

## Coordinated publication

After the coordinator supplies the final package, copy it into the canonical
evidence directory and run the commands above. Commit the reviewed changes on
`codex/rank9-10-publication`; because the checkout is sparse, add the evidence
directory with `git add --sparse`. Push only that branch after coordination.
The coordinator publishes by updating `main` with its previously verified head
as `expected_sha`; a changed head requires review before retrying.
The publication branch runs the same restored-data validation in GitHub Actions;
the Pages deploy job runs only on `main`. Check that branch run before advancing
the public ref.

If terminal Git transport is unavailable, prepare GitHub Git-data requests:

```bash
python3 site/prepare_rank9_10_publication.py --output /absolute/staging/git-upload
```

The output must be outside the checkout. `manifest.json` records every changed
path, content size, Git blob SHA and SHA-256, grouped as text, binary or deleted.
Its accompanying JSON files contain the UTF-8 tree requests and base64 binary
blob requests. Nothing is uploaded and no reference is changed by this script.
Re-run it after the final package and compare the final remote tree with the
reviewed local commit before advancing a branch.

## Independent fusion census view

The Fusion rings table loads the current certified count manifest from the separate census repository. It never copies those additional ranks into the categorification scope, model catalogue, case inventory or classification ledger. Bands without classification data display “Categorification not assessed”. Network failure retains the bundled count snapshot with an explicit notice.

# Rank-eleven publication

The canonical classification package is `evidence/rank11_m1_20261023/`.
Its 182 source-bound ledger entries give 155 general complex exclusions and
27 unitary realizations, with no unresolved cases. Physical line identifiers,
original basis order and both tensor hashes are unchanged.

The current paper is `publications/rank11/paper/rank11.pdf` and its self-contained
TeX source. `data/current_publication_revision.json` selects the current PDFs
for ranks 2–11, binds the two new high-rank ledgers and lists all seven open cases.
The earlier `current_document_revision.json` and eight-paper page inventory
remain frozen inputs to the historical rank-two through rank-eight proof
archives. The current ten-paper inventory is
`data/current_manuscript_page_counts.json`.

Run additive builders last when rebuilding older snapshots, because the
historical tensor exporter prunes files outside its original inventory:

```bash
python3 site/build_rank9_10.py
python3 site/build_rank11.py
python3 site/check_rank9_10.py
python3 site/check_rank11.py
python3 -O site/check_rank11.py
node site/check_cases.mjs
```

The rank-eleven builder verifies every full tensor against the original hash,
all fusion axioms, the exact classification partition and every evidence path.
The checker verifies all 182 downloads, all linked proof hashes and every ZIP
member. The UI checker covers all 182 case renderings, the 182-ring fusion view,
27-model Grothendieck view, ordered pagination and status/search filters.

Rank eleven uses the same atlas table, model catalogue, manuscript shelf and
`records.html` case directory as every other rank. There is no separate
rank-eleven navigation item or front-page release panel. Previously shared
rank-eleven directory links redirect to the common directory with rank 11
selected. Source payloads remain independently checksummed.

Current findings precede invariants and fusion data. Research records and the
grouped, searchable evidence catalogue remain folded by default. Earlier
updates are retained behind expandable sections. No rank-ten status changes
are part of this publication.

The complete mathematical replay, independently of the UI, is:

```bash
cd evidence/rank11_m1_20261023
python3 -m pip install -r requirements.txt
python3 work/rank11/replay_all.py
```

Both ordinary and optimized Python cover all 25 accepted verification stages.
The archived receipts retain the research-stage context; publication changes
the report disclosure and reader projections, leaving decisions and proof
implementations unchanged. Exact automated checks do not replace independent
human mathematical review.

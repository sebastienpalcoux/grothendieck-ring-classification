#!/usr/bin/env python3
"""Render the front-page count matrix from the checked machine-readable data."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
counts=json.loads((ROOT/'data/counts.json').read_text())
status=json.loads((ROOT/'data/classification_status.json').read_text())
by={(x['rank'],x['multiplicity']):x['rings'] for x in counts['rows']}
state={(x['rank'],x['multiplicity']):x for x in status['rows']}

lines=['''# Grothendieck ring classification

### Which low-rank fusion rings admit fusion categories over ℂ?

An atlas of **exact based-ring counts**, **categorification decisions** and the
proofs behind those decisions. The census and classification have different
bounds. A ring counted by the census is not thereby categorifiable.

**[Browse all counts](data/counts.csv)** · **[Classification outcomes](data/classification_status.csv)** · **[Provenance](docs/PROVENANCE.md)** · **[Verify the data](docs/VERIFY.md)** · **[Manuscripts](manuscripts/README.md)**

> **Scope.** Multiplicity is the maximum fusion coefficient. Each cell below
> counts based-isomorphism classes with *exactly* that multiplicity. A dash
> means the whole rank/multiplicity band has not been enumerated; it never
> means zero. The symbolic rank-two sequence continues beyond this table.

## Census · rings at each exact multiplicity

| Multiplicity | Rank 2 | Rank 3 | Rank 4 | Rank 5 | Rank 6 | Rank 7 | Rank 8 |
|---:|---:|---:|---:|---:|---:|---:|---:|''']
for m in range(1,21):
    row=[str(m)]+[f'{by[(r,m)]:,}' if (r,m) in by else '—' for r in range(2,9)]
    lines.append('| '+' | '.join(row)+' |')

lines.append('''
Full data: [JSON](data/counts.json) · [CSV](data/counts.csv). The source
[fusion-ring-census](https://github.com/sebastienpalcoux/fusion-ring-census)
contains the tensors and enumerator. The table here is pinned to its commit
`b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726`. Rank-two counts follow
directly from the normal form `X² = 1 + nX` for `n ≥ 0`: two rings at
multiplicity 1, then one at every multiplicity `m ≥ 2`.

## Classification · what is decided?

| Rank | Full census | General classification | Current conclusion |
|---:|---:|---:|---|
| 2 | Symbolic, all multiplicities | All multiplicities over ℂ | Exactly the rings `n = 0, 1` are realized; revised proof in preparation. |
| 3 | Through 1,000 | Unrestricted theorem | See the short rank-three sphericality and classification manuscript. |
| 4 | Through 128 | **Complete through 128** | 15 realized rings, 889,515 general exclusions. |
| 5 | Through 20 | **Complete through 17** | 17 realized rings. At 18, 5,078 excluded and two generally unresolved. At 19–20, the census is available but no classification ledger is supplied. |
| 6 | Through 8 | **Complete through 2** | Through 7: 9,530 excluded, 54 realized, 29 unresolved. Multiplicity 8 is census-only. |
| 7 | Through 4 | No manuscript classification ledger | Census counts only. |
| 8 | Through 2 | No manuscript classification ledger | Census counts only. |

Rank-six realization counts through multiplicity 7 split into **53 unitary
models** and **one spherical model whose ring has no pseudo-unitary
categorification**. “Realized” means that at least one categorification is
constructed; it does not assert that every categorification of that ring is
unitary. The rank-five two residual rings have spherical exclusions but their
general categorification status remains unresolved.

### The classification boundary, band by band

| Multiplicity | Rank 4 | Rank 5 | Rank 6 |
|---:|---:|---:|---:|''')
def cell(rank,m):
    s=state.get((rank,m))
    if s is None:return '—'
    if s['classification_coverage']=='census_only':return f"{s['rings']:,} census; analysis pending"
    realized=(s['realized_unitary']+s['realized_other_or_unspecified']+
              s['realized_spherical_nonpseudounitary'])
    val=f"{s['excluded_general']:,} excluded · {realized:,} realized"
    if s['unresolved_general']:val+=f" · **{s['unresolved_general']:,} open**"
    return val
for m in range(1,21):
    lines.append('| '+str(m)+' | '+' | '.join(cell(r,m) for r in (4,5,6))+' |')

lines.append('''
Full decision bands: [JSON](data/classification_status.json) ·
[CSV](data/classification_status.csv). Statuses come from the attached
rank-four, rank-five and rank-six certificate ledgers; their SHA-256 hashes,
row checks and scope appear in [the provenance record](docs/PROVENANCE.md).

## Read the mathematics

The [manuscripts](manuscripts/README.md) are kept as TeX/PDF pairs. The
classification programs proceed rank by rank: general necessary criteria,
exact automated applications, positive model matches, and explicit residual
frontiers. Rank three takes a separate, unrestricted route through the
sphericality theorem. The papers and computation records remain research in
progress; [the evidence guide](docs/VERIFY.md) identifies exactly what the
stored checks establish.

## Structure

```text
data/         Pinned census matrix and classification-status tables
docs/         Provenance, terminology and verification paths
manuscripts/  Revised TeX and PDF pairs, as released
site/         Static atlas source and private-preview assets
tools/        Deterministic count/status export and crosswalk checks
```

**Source of truth:** the [fusion-ring-census repository](https://github.com/sebastienpalcoux/fusion-ring-census)
owns the based-ring census and raw tensor files. This repository records the
classification, proofs and models; it does not recompute the census. Changes
to a source census cell are imported only from a named commit and rechecked
against classification ledgers.
''')
(ROOT/'README.md').write_text('\n'.join(lines))
print('Rendered README.md')

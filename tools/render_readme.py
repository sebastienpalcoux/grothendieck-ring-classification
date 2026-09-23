#!/usr/bin/env python3
"""Render the front-page Grothendieck ring matrix from status evidence."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
status=json.loads((ROOT/'data/classification_status.json').read_text())
state={(x['rank'],x['multiplicity']):x for x in status['rows']}
ranks=sorted({r for r,m in state if 2 <= r <= 8})

def realized(s):
    return (s['realized_unitary'] + s['realized_other_or_unspecified'] +
            s['realized_spherical_nonpseudounitary'])

def outcome(rank, m):
    s=state.get((rank,m))
    if not s or s['classification_coverage']=='census_only':
        return '—'
    n=realized(s)
    return ('≥' if s['unresolved_general'] or s['unassessed'] else '')+str(n)

lines=['''# Grothendieck ring classification

### Which low-rank fusion rings admit fusion categories over ℂ?

An atlas of **realized Grothendieck rings**, **categorification decisions** and
the proofs behind those decisions. The fusion-ring census and classification
have different bounds. A ring counted by the census is not thereby
categorifiable.

**[Grothendieck ring counts](data/grothendieck_counts.csv)** · **[Fusion-ring census](https://github.com/sebastienpalcoux/fusion-ring-census#readme)** · **[Classification outcomes](data/classification_status.csv)** · **[Provenance](docs/PROVENANCE.md)** · **[Verify the data](docs/VERIFY.md)** · **[Manuscripts](manuscripts/README.md)** · **[OEIS drafts](oeis/README.md)**

[**Private working atlas (owner-only)**](https://grothendieck-ring-atlas.sebastien-palcoux.chatgpt.site) · [Atlas source and snapshot](site/)

> **Scope.** Multiplicity is the maximum fusion coefficient. Each cell below
> counts known categorifiable based-isomorphism classes with *exactly* that
> multiplicity. A plain number is exact where classification is complete;
> `≥n` is a certified lower bound where general cases remain unresolved.
> A dash denotes a band not analyzed here. Rows with no known realizations
> are omitted; omission makes no assertion about unresolved cases.

## Grothendieck rings · known realizations at each exact multiplicity
''']
lines.append('| Multiplicity | '+' | '.join(f'Rank {rank}' for rank in ranks)+' |')
lines.append('|---:|'+'---:|'*len(ranks))
for m in range(1,max(k[1] for k in state)+1):
    if not any(realized(state[(r,m)]) for r in ranks if (r,m) in state):
        continue
    row=[str(m)]+[outcome(r,m) for r in ranks]
    lines.append('| '+' | '.join(row)+' |')

lines.append('''
Full realized-count data, including zero and unresolved bands:
[JSON](data/grothendieck_counts.json) · [CSV](data/grothendieck_counts.csv).
The [fusion-ring-census repository](https://github.com/sebastienpalcoux/fusion-ring-census)
contains the separate table of **all fusion rings** and its enumerator;
[this repository's pinned census import](data/counts.csv) supports the
classification cross-check. Rank-two realized counts follow directly from
`X² = 1+nX`: both categorifiable rings occur at multiplicity 1.

## Classification · what is decided?

| Rank | Full census | General classification | Current conclusion |
|---:|---:|---:|---|
| 2 | Symbolic, all multiplicities | All multiplicities over ℂ | Exactly the rings `n = 0, 1` are realized; see the revised proof. |
| 3 | Through 1,000 | Unrestricted theorem | Five realized rings: four at multiplicity 1 and one at 2; see the standalone sphericality and ring-classification proof. |
| 4 | Through 128 | **Complete through 128** | 15 realized rings, 889,515 general exclusions. |
| 5 | Through 20 | **Complete through 17, and separately at 19–20** | 17 realized rings. At 18, 5,078 excluded and two generally unresolved; all 12,506 rings at 19–20 are excluded. |
| 6 | Through 8 | **Complete through 2** | Through 8: 16,511 excluded, 54 realized, 47 unresolved; 19 of those residuals occur at multiplicity 8. |

Rank-six realization counts through multiplicity 8 split into **53 unitary
models** and **one spherical model whose ring has no pseudo-unitary
categorification**. “Realized” means that at least one categorification is
constructed; it does not assert that every categorification of that ring is
unitary. The rank-five two residual rings at multiplicity 18 have spherical
exclusions but their general categorification status remains unresolved.

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

### When did the current criterion repertoire stabilize?

| Rank | Last first use of a mathematical criterion family | Checked range afterward |
|---:|---:|---|
| 4 | Multiplicity 18 | The same criterion families suffice for the allocated exclusions at 19–128. |
| 5 | Multiplicity 8 | The same theoretical families suffice at 9–20; a combined executable certificate type first appears at 12. Two rings at 18 remain unresolved. |
| 6 | Multiplicity 8 | Dimension-order and character-induction exclusions first succeed at 8; 47 general cases remain unresolved. No later multiplicity is covered. |

This records **first use in the chosen certificate allocation**, not an
optimal ordering theorem or a claim that the criteria settle higher
multiplicities. Rank-four nested signed cyclotomicity first succeeds at 95,
using a general cyclotomicity theorem already used at 9. The ordered
step-by-step exclusion tables and proof dependencies are in the manuscripts.

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
supplements/  Proof software, compact certificates and verification reports
site/         Static atlas source and private-preview assets
tools/        Deterministic count/status export and crosswalk checks
oeis/         Sequence drafts, pending an OEIS submission
```

**Source of truth:** the [fusion-ring-census repository](https://github.com/sebastienpalcoux/fusion-ring-census)
owns the based-ring census and raw tensor files. This repository records the
classification, proofs and models; it does not recompute the census. Changes
to a source census cell are imported only from a named commit and rechecked
against classification ledgers.
''')
(ROOT/'README.md').write_text('\n'.join(lines))
print('Rendered README.md')

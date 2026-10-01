#!/usr/bin/env python3
"""Render the front-page Grothendieck ring matrix from status evidence."""
import json
import argparse
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--identity',type=Path,default=ROOT/'data/rank6_release_identity.json')
parser.add_argument('--output',type=Path,default=ROOT/'README.md')
args=parser.parse_args()
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

rank6=sorted((s for (r,m),s in state.items() if r==6),key=lambda s:s['multiplicity'])
rank6_bound=max(s['multiplicity'] for s in rank6)
rank6_excluded=sum(x['excluded_general'] for x in rank6)
rank6_realized=sum(realized(x) for x in rank6)
rank6_open=sum(x['unresolved_general'] for x in rank6)
rank6_complete=next((x['multiplicity']-1 for x in rank6 if x['unresolved_general']),rank6_bound)
rank6_summary=(f'| 6 | Through {rank6_bound} | **Complete through {rank6_complete}** | '
               f'Through {rank6_bound}: {rank6_excluded:,} excluded, {rank6_realized} realized, '
               f'{rank6_open} unresolved. |')
identity=json.loads(args.identity.read_text())
release=identity['summary']
complete_bands=', '.join(str(s['multiplicity']) for s in rank6 if s['unresolved_general']==0)
from rank6_publication import continuation_text
rank6_continuation = continuation_text(identity)
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
| 5 | Through 20 | **Complete through 20** | 17 realized rings and 40,982 generally excluded. The two former multiplicity-18 residuals are now excluded by inert-prime parity and exact induction. |
__RANK6_SUMMARY__
| 7 | Through 4 | Partial at every band | Through 4: 4,107 excluded, 16 realized, 78 unresolved; full normal and optimized certificate replays passed. |
| 8 | Through 2 | Partial at both bands | Through 2: 824 excluded, 33 realized, 116 unresolved; positive tensors and transferred certificates verified. |

Rank-six realization counts through multiplicity __RANK6_BOUND__ split into **56 unitary
models** and **one spherical model whose ring has no pseudo-unitary
categorification**. “Realized” means that at least one categorification is
constructed; it does not assert that every categorification of that ring is
unitary. Rank five has no unresolved ring through multiplicity 20.

__RANK6_CONTINUATION__

### The classification boundary, band by band

| Multiplicity | Rank 4 | Rank 5 | Rank 6 | Rank 7 | Rank 8 |
|---:|---:|---:|---:|---:|---:|''')
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
    lines.append('| '+str(m)+' | '+' | '.join(cell(r,m) for r in (4,5,6,7,8))+' |')

lines.append('''
Full decision bands: [JSON](data/classification_status.json) ·
[CSV](data/classification_status.csv). Statuses come from the attached
rank-four through rank-eight certificate ledgers; their SHA-256 hashes,
row checks and scope appear in [the provenance record](docs/PROVENANCE.md).

### When did the current criterion repertoire stabilize?

| Rank | Last first use of a mathematical criterion family | Checked range afterward |
|---:|---:|---|
| 4 | Multiplicity 18 | The same criterion families suffice for the allocated exclusions at 19–128. |
| 5 | Multiplicity 18 | Inert-prime quadratic parity first closes two cases at 18; no new criterion family is needed at 19–20. |
| 6 | See the allocation ledger | The current criteria include stabilizer, cyclotomic-trace and signed arithmetic obstructions. Every new multiplicity-nine tensor is processed separately from the preserved earlier campaign; __RANK6_OPEN__ general cases remain unresolved through multiplicity __RANK6_BOUND__. |
| 7 | Multiplicity 2 | Signed sphericalization first contributes at 1; the last first successful application of a listed family occurs at 2. There are 78 open rings through 4, so no stabilization conclusion follows. |
| 8 | Multiplicity 2 | Signed obstructions first contribute at 1; the last first successful application of a listed family occurs at 2. There are 116 open rings through 2, so no stabilization conclusion follows. |

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

After cloning, restore the large datasets with one offline command:

```bash
python3 tools/restore_data.py
```

The repository stores those datasets as small compressed parts. The command
checks every part and reconstructed file against its released SHA-256 hash;
it requires only Python's standard library. See [verification instructions](docs/VERIFY.md).

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
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text('\n'.join(lines).replace('__RANK6_SUMMARY__',rank6_summary)
                              .replace('__RANK6_OPEN__',str(rank6_open))
                              .replace('__RANK6_BOUND__',str(rank6_bound))
                              .replace('__RANK6_CONTINUATION__',rank6_continuation))
print('Rendered README.md')

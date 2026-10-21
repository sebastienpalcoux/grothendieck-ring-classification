#!/usr/bin/env python3
"""Render the front-page Grothendieck ring matrix from status evidence."""
import json
import argparse
from pathlib import Path
from publication_stages import load_stages, overview
from rank7_publication import summary as rank7_extension_summary, remaining_ids
from rank8_publication import summary as rank8_extension_summary, active as rank8_active

ROOT=Path(__file__).resolve().parents[1]
PUBLIC_ATLAS='https://sebastienpalcoux.github.io/grothendieck-ring-classification/'
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--identity',type=Path,default=ROOT/'data/rank6_release_identity.json')
parser.add_argument('--output',type=Path,default=ROOT/'README.md')
parser.add_argument('--check',action='store_true')
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
upper={rank:status['inputs'][f'rank{rank}']['status_totals'] for rank in (7,8)}
stage=load_stages(ROOT,status)
def upper_summary(rank):
    t=upper[rank];bound=status['inputs'][f'rank{rank}']['classified_through']
    complete=next((m-1 for m in range(1,bound+1) if state[(rank,m)]['unresolved_general'] or state[(rank,m)]['unassessed']),bound)
    scope=f'**Complete through {complete}**' if complete else 'Partial at both bands'
    if complete < bound: scope += (f"; multiplicity {bound} partial" if complete+1==bound else f"; multiplicities {complete+1}–{bound} partial")
    return (f'| {rank} | Through {bound} | {scope} | Through {bound}: '
            f"{t['excluded']:,} excluded, {t['unitarily_realized']} realized, {t['unresolved']} unresolved. |")
def upper_open_phrase(rank):
    count=upper[rank]['unresolved']
    return f"There {'is' if count==1 else 'are'} {count} generally open {'ring' if count==1 else 'rings'}"
identity=json.loads(args.identity.read_text())
release=identity['summary']
complete_bands=', '.join(str(s['multiplicity']) for s in rank6 if s['unresolved_general']==0)
from rank6_publication import continuation_text,require
rank6_continuation = continuation_text(identity).replace(
    'https://grothendieck-ring-atlas.sebastien-palcoux.chatgpt.site/', PUBLIC_ATLAS)
require([[s[k] for k in ('rings','excluded_general','realized_unitary',
                         'realized_spherical_nonpseudounitary','unresolved_general')]
         for s in rank6]==identity['counts'],'Refresh rank-six status rows before rendering the README')
lines=['''# Grothendieck ring classification

**Which low-rank fusion rings admit fusion categories over ℂ?**

Explore realized Grothendieck rings, proposed categorification arguments and
the exact data behind them. The public atlas connects interactive tables,
individual ring profiles, manuscripts and reproducible computation records.

**Companion repository:** [Fusion Ring Census](https://github.com/sebastienpalcoux/fusion-ring-census)
enumerates all based fusion rings; this repository classifies which admit
categorifications over ℂ.

### [Open the interactive atlas →](https://sebastienpalcoux.github.io/grothendieck-ring-classification/)

> [!IMPORTANT]
> **AI-generated research · independent verification pending.**
> The results, proofs, code and data in this project are AI-generated and
> have not yet been independently verified by human experts or formalized
> in Lean. Treat them as provisional and use them with caution. Automated
> checks establish only their stated computational scope; they do not
> replace mathematical review or formal proof.
> [Research-status notice](docs/RESEARCH_STATUS.md) ·
> [Verification scope and review](docs/PREPUBLICATION_REVIEW.md).

> [!NOTE]
> **[Research announcement · 5 pages](announcements/hexagon-2026-10/Low_rank_Grothendieck_rings_announcement.pdf)**
> Historical October announcement: classification scope, seven construction candidates, and the two rank-six open problems.
> [TeX source and Hexagon submission package](announcements/hexagon-2026-10/).
> **[Read the announcement on Hexagon · 2610.00300v1](https://hexagonmath.org/2610.00300?version=1)**.

> [!TIP]
> **[Potentially new tensor categories and open cases (PDF)](docs/New_category_candidates_and_open_cases.pdf)**
> Seven provisional construction candidates, the known `Rep(AGL(1,7))` model, and all __OPEN_CASE_COUNT__ current open cases.
> Novelty up to tensor equivalence remains subject to independent verification.

| Start here | What you will find |
|---|---|
| [Explore the atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/) | Filter counts, inspect fusion rules and character data, and follow source links. |
| **[Unrestricted rank-four classification](manuscripts/rank4/README.md)** | **[Main paper · 88 pages](manuscripts/rank4/papers/companion.pdf)** · [LaTeX](manuscripts/rank4/papers/companion.tex). No multiplicity bound or initial pivotality assumption. |
| [Read the manuscripts](manuscripts/README.md) | TeX sources and PDFs, organized by rank. |
| [Inspect the data](data/classification_status.csv) | Classification outcomes, [realized counts](data/grothendieck_counts.csv) and the separate [fusion-ring census](https://github.com/sebastienpalcoux/fusion-ring-census#readme). |
| [Reproduce the checks](docs/VERIFY.md) | Replay instructions, [provenance](docs/PROVENANCE.md) and the limits of each check. |

**Current research account.** The 38-case continuation records **36 decisions**:
29 proposed general exclusions and 7 unitary constructions. **Two general
cases from that historical study remain open:** `R6_4_155` and `R6_8_1660`. Rank eight is complete
through multiplicity two, with 896 exclusions and 77 unitary models.
The exclusion of `R8_2_24` follows from an inner-square obstruction using
pivotal duality, short associator weights and tensor-functor rigidity.
__RANK7_EXTENSION__
__RANK8_EXTENSION__

The tables below report the project's classification claims; “complete” and
“certified” do not imply independent human verification or Lean formalization.

[Realized counts](#grothendieck-rings--known-realizations-at-each-exact-multiplicity) · [Classification](#classification--what-is-decided) · [Manuscripts](#read-the-mathematics) · [Repository guide](#structure) · [OEIS drafts](oeis/README.md)

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

These are the recorded outcomes of the current research program, subject to
the verification notice and [verification scope](docs/PREPUBLICATION_REVIEW.md).
Census bounds describe enumeration coverage; classification scope is stated separately.

| Rank | Full census | General classification | Current conclusion |
|---:|---:|---:|---|
| 2 | Symbolic, all multiplicities | **Unrestricted theorem** | Exactly the rings `n = 0, 1` are realized. |
| 3 | Through 1,000 | **Unrestricted theorem** | Five realized rings: four at multiplicity 1 and one at 2; see the standalone sphericality and ring-classification proof. |
| 4 | Through 128 | **Unrestricted theorem** | Exactly 15 realized rings; every categorification is spherical; multiplicity at most 6. |
| 5 | Through 20 | **Complete through 20** | Through 20: 40,982 excluded, 17 realized, 0 unresolved. |
__RANK6_SUMMARY__
__RANK7_SUMMARY__
__RANK8_SUMMARY__

The [rank-four unrestricted proof](manuscripts/rank4/papers/companion.pdf) gives the sharp bound FPdim ≤ 24+12√3, attained only by the near-group ring `NG(C₃,6)`. Its theoretical reduction gives FPdim < 1000 and multiplicity at most 31; an independent exact census then checks 1,692 rings, with 1,677 exclusions and 15 models. The separate multiplicity-128 census contains 889,530 rings and 889,515 exclusions.

Related work on the pivotal case: Jingcheng Dong, Sébastien Palcoux and Arnaud Plessis, [Classifying Grothendieck rings of pivotal fusion categories of rank four](https://arxiv.org/abs/2609.33272), arXiv:2609.33272. Its hypothesis is pivotality.

Rank-six realization counts through multiplicity __RANK6_BOUND__ split into **56 unitary
models** and **one spherical model whose ring has no pseudo-unitary
categorification**. “Realized” means that at least one categorification is
constructed; it does not assert that every categorification of that ring is
unitary. Rank five has no unresolved ring through multiplicity 20;
inert-prime parity and exact induction cover multiplicity 18.

__RANK6_CONTINUATION__

__UPPER_RESIDUAL_OVERVIEW__
The [proof inventory](docs/VERIFY.md) gives the replay paths.
Scope-specific obstructions retain their stated assumptions and do not change
a ring's general unresolved status.

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
| 6 | See the allocation ledger | The current criteria include stabilizer, cyclotomic-trace and signed arithmetic obstructions. All 8,809 exact-multiplicity-nine rings have general exclusion certificates; __RANK6_OPEN__ earlier cases remain unresolved through multiplicity __RANK6_BOUND__. |
| 7 | See the allocation ledger | The multiplicity-five extension adds cyclic-module, quadratic compression, signed sphericalization, center-trace and Morita-descent arguments. __RANK7_OPEN_PHRASE__ in the analyzed range; both have braided-only exclusions. Higher multiplicities are not classified here. |
| 8 | Multiplicity 2 | Graded Brauer-Picard, fiber-functor and inner-square rigidity obstructions give the complete classification through 2. __RANK8_OPEN_PHRASE__ in the analyzed range; higher multiplicities are not classified here. |

This records **first use in the chosen certificate allocation**, not an
optimal ordering theorem or a claim that the criteria settle higher
multiplicities. Rank-four nested signed cyclotomicity first succeeds at 95,
using a general cyclotomicity theorem already used at 9. The ordered
step-by-step exclusion tables and proof dependencies are in the manuscripts.

## Read the mathematics

The [manuscripts](manuscripts/README.md) are kept as TeX/PDF pairs. The
classification programs proceed rank by rank: general necessary criteria,
exact automated applications, positive model matches, and explicit residual
frontiers. Ranks two, three and four have unrestricted classification
theorems. The rank-four article supplies the complete theoretical reduction
and exact finite verification. The papers and computation records remain research in
progress; [the evidence guide](docs/VERIFY.md) identifies exactly what the
stored checks establish. Each manuscript states its current classification scope
and the remaining questions directly; [rank eight](manuscripts/rank8/paper/rank8.pdf)
proves the complete classification through multiplicity two.

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
manuscripts/  Current TeX and PDF pairs
supplements/  Proof software, compact certificates and verification reports
site/         Public GitHub Pages atlas, source and reproducible snapshots
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
from sync_rank8_m3_publication import center_scope, center_replay_scope, frontier_replay_scope
center_note = center_scope(ROOT)
rank8_extension_text = rank8_extension_summary(ROOT) if rank8_active(ROOT) else ''
if rank8_active(ROOT) and (ROOT/'evidence/rank8_frontier_20261021/publication').is_dir():
    rank8_extension_text += '\n\n'+frontier_replay_scope(ROOT)
if center_note:
    rank8_extension_text += ('\n\n'+center_note+'\n\n'
        '[Separately verified center-pattern addendum](evidence/rank8_center_followup_20261021/README.md).\n\n'+center_replay_scope())
rendered=('\n'.join(lines).replace('__RANK7_EXTENSION__',rank7_extension_summary(ROOT))
                              .replace('__RANK8_EXTENSION__',rank8_extension_text)
                              .replace('__OPEN_CASE_COUNT__',str(len(remaining_ids(ROOT))))
                              .replace('__RANK6_SUMMARY__',rank6_summary)
                              .replace('__RANK7_SUMMARY__',upper_summary(7))
                              .replace('__RANK8_SUMMARY__',upper_summary(8))
                              .replace('__RANK7_OPEN_PHRASE__',upper_open_phrase(7))
                              .replace('__RANK8_OPEN_PHRASE__',upper_open_phrase(8))
                              .replace('__RANK6_OPEN__',str(rank6_open))
                              .replace('__RANK6_BOUND__',str(rank6_bound))
                              .replace('__RANK6_CONTINUATION__',rank6_continuation)
                              .replace('__UPPER_RESIDUAL_OVERVIEW__',overview(stage))
                              .replace('__RANK8_READING__','manuscripts/rank8/paper/rank8-reviewed.pdf' if (ROOT/'manuscripts/rank8/paper/rank8-reviewed.pdf').is_file() else 'docs/PREPUBLICATION_REVIEW.md'))
if rank8_active(ROOT):
    rendered=rendered.replace('| 8 | Multiplicity 2 | Graded Brauer-Picard, fiber-functor and inner-square rigidity obstructions give the complete classification through 2.', '| 8 | Multiplicity 3 | Quadratic-compositum compression, convex central induction, split-module polynomials and Morita transport extend the classification through multiplicity three.')
    rendered=rendered.replace('proves the complete classification through multiplicity two.', 'records exclusions, explicit unitary models and individually investigated unresolved candidates through multiplicity three.')
    rendered=rendered.replace('in the analyzed range; both have braided-only exclusions.', 'in the analyzed range.')
if args.check:
    if not args.output.is_file() or args.output.read_text()!=rendered:
        raise ValueError('Regenerate '+str(args.output))
else:
    args.output.write_text(rendered)
print(('Checked' if args.check else 'Rendered')+' README.md')

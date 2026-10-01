#!/usr/bin/env python3
"""Render current rank-six publication indexes while preserving other ranks."""
import argparse,json,re
from pathlib import Path
from rank6_publication import validate_identity,archive_url,completed_bands,progress_table
ROOT=Path(__file__).resolve().parents[1]
def section(text,start,end,replacement):
    a=text.index(start);b=text.index(end,a);return text[:a]+replacement+text[b:]
def render(repo,i):
    validate_identity(i);out={};a=i['archive'];s=i['summary'];bands=completed_bands(i);bound=len(i['counts']);total=sum(r[0] for r in i['counts']);read=lambda n:(repo/n).read_text()
    text=read('docs/PROVENANCE.md')
    text=re.sub(r'\[`[0-9a-f]{40}`\]\(https://github.com/sebastienpalcoux/fusion-ring-census/tree/[0-9a-f]{40}\)',f"[`{i['census_commit']}`](https://github.com/sebastienpalcoux/fusion-ring-census/tree/{i['census_commit']})",text,count=1)
    if 'The updated rank-six source ' in text:
        text=section(text,'The updated rank-six source ','The current rank-six release is','')
    text=section(text,'The current rank-six release is','The verified rank-seven release through',f'''The current rank-six release is `{a['name']}` (SHA-256
`{a['sha256']}`). The [complete archive]({archive_url(i)}) contains
{a['files']:,} files and the pinned census, proof certificates and exact constructors.
The partition is **{s['excluded']:,} excluded, {s['positive']} realized and {s['unresolved']} unresolved**.
There are 56 unitary models and one spherical model with no pseudo-unitary
categorification. All 8,809 rings of exact multiplicity nine are generally excluded.
The final eleven cases have portable proof bundles and exact completion replays
in normal and optimized Python. Only the two earlier frontier rings remain open.
The release identity binds the completion certificates, both replay reports,
every completion proof file, and the manuscript and verification-guide sources and PDFs.

The current ledger is `supplements/rank6/data/decisions.json`, SHA-256
`{i['ledger_sha256']}`. The unchanged earlier negative proofs retain their
original exact verification evidence; this release does not claim a fresh
replay of every earlier proof. See [verification instructions](VERIFY.md).

{progress_table(i)}

''')
    lines=text.splitlines()
    for n,line in enumerate(lines):
        if line.startswith('| 6 | `results/rank6/'):
            lines[n]=f'| 6 | `results/rank6/tables.txt.gz` | {bound} | `supplements/rank6/data/decisions.json` | Complete through 3; exact bands {bands}; {s["unresolved"]} unresolved through {bound} |'
        elif line.startswith('| 6 | `') and 'results/rank6/' not in line:
            lines[n]=f"| 6 | `{i['ledger_sha256']}` | {total:,} | {s['excluded']:,} excluded; 56 unitary; 1 spherical non-pseudo-unitary; {s['unresolved']} unresolved |"
    text='\n'.join(lines)+'\n'
    text=section(text,'* Rank six:','\nThe crosswalk scripts',f'''* Rank six: [`rank6_crosswalk.json`](../data/rank6_crosswalk.json) compares
  all {total:,} full tensor lines through multiplicity {bound} with the pinned
  source export, and verifies identical compressed-file checksums. The import
  separately checks every tensor against all 120 unit-fixing basis permutations
  and preserves all 16,612 earlier representatives and identifiers.
''')
    out['docs/PROVENANCE.md']=text
    text=read('docs/VERIFY.md');text=re.sub(r'Rank6_Categorification_M[0-9]+_(?:Revised_[0-9-]+_v\d+|(?:Complete|Frontier)_[0-9-]+)\.zip',a['name'],text)
    text=re.sub(r'git -C fusion-ring-census checkout [0-9a-f]{40}',f"git -C fusion-ring-census checkout {i['census_commit']}",text)
    text=text.replace('rank-six decisions use the updated M8 ZIP.','rank-six decisions use the current M9 ZIP.')
    text=re.sub(r'The incremental exporter verifies all [0-9,]+ distinct records',f'The incremental exporter verifies all {total:,} distinct records',text)
    text=section(text,'The exporter records source checksums','Rank seven has 78 open cases',f'''The exporter records source checksums and verifies cardinalities against
every census band. The released rows have no unassessed bands. Rank five is
complete through multiplicity 20. Rank six is complete through multiplicity
three, with exact completed bands {bands} and {s['unresolved']} cases through
multiplicity {bound} generally unresolved. Isolated completed bands do not
complete intervening unresolved bands.
''')
    text=section(text,'The incremental exporter verifies all ','\n## Rank-six continuation evidence',f'''The incremental exporter verifies all {total:,} distinct records and each pinned
census-band total before replacing rank-six rows. Its input hash and current
bundle are explicit in `data/classification_status.json`. Other ranks' rows
and provenance are preserved. `validate_release.py` compares all {bound}
rank-six bands with the authoritative ledger, checks the
{s['excluded']:,}/{s['positive']}/{s['unresolved']} excluded/realized/unresolved
partition, every completed band and the release summary. These export checks
are separate from mathematical certificate replay.
''')
    text=section(text,'contains all ','\n## Rebuild from the pinned census',f"contains all {a['files']:,} current release files. It is restored at\n`site/dist/downloads/{a['name']}`.\n")
    text=section(text,'## Rank-six continuation evidence','\n## Tensor crosswalks','''## Rank-six continuation evidence

From the complete mirrored release:

```bash
cd supplements/rank6
python check_manifest.py
python -O software/conformal_models.py --verify
python -O software/release_consistency.py
python -O software/replay_m9.py --jobs 2
python -O software/replay_m9_structure.py
python software/replay_m9_completion.py --output verification/m9/completion/replay_normal.json
python -O software/replay_m9_completion.py --output verification/m9/completion/replay_optimized.json
python -O research/exclusions/R6_5_1204/verify_exclusion.py
python -O software/frontier_replay.py --check-receipts
python -O software/frontier_replay.py --list
python research/frontier/new_research/replay.py
```

The conformal-model command freshly reconstructs the three unitary models.
The frontier receipt audit checks hashes and completion predicates, not the
mathematics. To replay a necessary reduction, select one current ring, for
example `python -O software/frontier_replay.py --select R6_4_155`.
The current research replay checks the completed R6_4_155 modular-data candidate,
finite indicator tests, and the R6_8_1660 module/Morita and 1,669-profile reductions.
Its exact scope and receipts are in `research/frontier/new_research/`. These are
necessary conditions; both categorification questions remain unresolved.
Each command has a 15-minute deadline. A timeout establishes no exclusion.

The completion replay checks all eleven final multiplicity-nine exclusions
against the frozen tensors and portable proof bundles. Its normal and optimized
reports, input and proof manifests, and negative controls are recorded in
`verification/m9/completion/`. The release identity hashes these records and
every file in `research/exclusions/m9_completion/`. All 8,809 rings at exact
multiplicity nine are excluded; the two remaining open rings have lower multiplicity.

A complete fresh replay of every accepted certificate is:

```bash
python -O verify.py --jobs 2 --out verification/current/recheck_O.jsonl
```

The authoritative decisions and all unresolved tensors are in `data/`.
The [frontier](../supplements/rank6/research/frontier/README.md) identifies the
current necessary reductions, and the model catalogue lists all realizations.
''');out['docs/VERIFY.md']=text
    text=read('manuscripts/README.md');lines=text.splitlines()
    for n,line in enumerate(lines):
        if line.startswith('| Rank six |'):lines[n]=f'| Rank six | [TeX](rank6/papers/manuscript.tex) | [PDF](rank6/papers/manuscript.pdf) | Complete through 3; exact bands {bands}; {s["positive"]} realized and {s["unresolved"]} unresolved through {bound} |'
        elif line.startswith('| Rank six, verification guide |'):lines[n]='| Rank six, verification guide | [TeX](rank6/papers/verification_guide.tex) | [PDF](rank6/papers/verification_guide.pdf) | Exact models, exclusion certificates and unresolved rings |'
    text='\n'.join(lines)+'\n';text=text[:text.index('The current rank-six paper')]+f'''The current rank-six paper contains {s['excluded']:,} general exclusions, {s['positive']} realizations
and {s['unresolved']} unresolved rings through multiplicity {bound}. All 8,809 exact-multiplicity-nine
rings are excluded, including the final eleven cases proved in the completion chapter.
A unified conformal-embedding section constructs
R6_4_22, R6_4_91 and R6_4_629. Superseded necessary-center searches have been
removed. The [current frontier](../supplements/rank6/research/frontier/README.md)
and [verification instructions](../docs/VERIFY.md) give the retained evidence.
''';out['manuscripts/README.md']=text
    text=read('supplements/README.md');text=re.sub(r'all four accepted exclusion continuations and the round-five refinements','accepted exclusion certificates and conformal constructions',text);lines=text.splitlines()
    for n,line in enumerate(lines):
        if line.startswith('| 6 |'):lines[n]=f'| 6 | [`rank6/software/`](rank6/software/) and [`verify.py`](rank6/verify.py) | Complete release; {s["excluded"]:,} excluded, {s["positive"]} realized, {s["unresolved"]} unresolved; complete through 3 and exact bands {bands} |'
    text='\n'.join(lines)+'\n';text=text[:text.index('For the rank-six update')]+f'''For the rank-six update, start with its [README](rank6/README.md),
[models](rank6/data/model_catalog.csv) and [current frontier](rank6/research/frontier/README.md).
The authoritative ledger is `rank6/data/decisions.json`. The archive is
`{a['name']}`. Source-bound certificates retain their internal paths.
''';out['supplements/README.md']=text
    text=read('oeis/README.md');out['oeis/README.md']=section(text,'Rank-six general classification','No zero beyond a proven finite',f'''Rank-six general classification is complete at exact multiplicities
**{bands}**, contiguously through **3**. The unresolved rings are recorded in the current frontier.
The rank-six fusion-ring census draft is separately extended by a(9)=8809;
it counts all based rings, regardless of categorifiability. The exporter proposes only the rank-four and
rank-five drafts listed above; no incomplete band is an exact sequence term.
''')
    return out
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,default=ROOT);p.add_argument('--identity',type=Path);p.add_argument('--output-dir',type=Path);p.add_argument('--check',action='store_true');a=p.parse_args();i=json.loads((a.identity or a.repo/'data/rank6_release_identity.json').read_text());files=render(a.repo,i)
    for name,text in files.items():
        target=(a.output_dir or a.repo)/name
        if a.check:
            if not target.is_file() or target.read_text()!=text:raise ValueError('Regenerate '+name)
        else:target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
    print(('Checked' if a.check else 'Rendered'),len(files),'publication documents')
if __name__=='__main__':main()

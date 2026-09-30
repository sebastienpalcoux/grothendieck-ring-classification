#!/usr/bin/env python3
"""Render current rank-six publication indexes while preserving other ranks."""
import argparse,json,re
from pathlib import Path
from rank6_publication import validate_identity,archive_url,completed_bands,progress_table
ROOT=Path(__file__).resolve().parents[1]
def section(text,start,end,replacement):
    a=text.index(start);b=text.index(end,a);return text[:a]+replacement+text[b:]
def render(repo,i):
    validate_identity(i);out={};a=i['archive'];s=i['summary'];bands=completed_bands(i);read=lambda n:(repo/n).read_text()
    text=read('docs/PROVENANCE.md')
    text=section(text,'The current rank-six release is','The verified rank-seven release through',f'''The current rank-six release is `{a['name']}` (SHA-256
`{a['sha256']}`). The [complete archive]({archive_url(i)}) contains
{a['files']:,} files and the pinned census, proof certificates and exact constructors.
The partition is **16,553 excluded, 57 realized and 2 unresolved**.
There are 56 unitary models and one spherical model with no pseudo-unitary
categorification. The source census is unchanged. A new exact certificate excludes R6_5_1204.
Three conformal-embedding constructions settle R6_4_22, R6_4_91 and R6_4_629.

The current ledger is `supplements/rank6/data/decisions.json`, SHA-256
`{i['ledger_sha256']}`. Fresh exact checks reconstruct all 216 tensor
coefficients of each new model. The unchanged negative proofs retain their
original exact verification evidence; this release does not claim a fresh
replay of every earlier proof. See [verification instructions](VERIFY.md).

{progress_table(i)}

''')
    lines=text.splitlines()
    for n,line in enumerate(lines):
        if line.startswith('| 6 | `results/rank6/'):
            lines[n]=f'| 6 | `results/rank6/tables.txt.gz` | 8 | `supplements/rank6/data/decisions.json` | Complete through 3; exact bands {bands}; two unresolved through 8 |'
        elif line.startswith('| 6 | `') and '| 16,612 |' in line:
            lines[n]=f"| 6 | `{i['ledger_sha256']}` | 16,612 | 16,553 excluded; 56 unitary; 1 spherical non-pseudo-unitary; 2 unresolved |"
    out['docs/PROVENANCE.md']='\n'.join(lines)+'\n'
    text=read('docs/VERIFY.md');text=re.sub(r'Rank6_Categorification_M8_Revised_[0-9-]+_v\d+\.zip',a['name'],text)
    text=section(text,'contains all ','\n## Rebuild from the pinned census',f"contains all {a['files']:,} current release files. It is restored at\n`site/dist/downloads/{a['name']}`.\n")
    text=section(text,'## Rank-six continuation evidence','\n## Tensor crosswalks','''## Rank-six continuation evidence

From the complete mirrored release:

```bash
cd supplements/rank6
python check_manifest.py
python -O software/conformal_models.py --verify
python -O software/release_consistency.py
python -O research/exclusions/R6_5_1204/verify_exclusion.py
python -O software/frontier_replay.py --check-receipts
python -O software/frontier_replay.py --list
```

The conformal-model command freshly reconstructs the three unitary models.
The frontier receipt audit checks hashes and completion predicates, not the
mathematics. To replay a necessary reduction, select one current ring, for
example `python -O software/frontier_replay.py --select R6_4_155`.
Each command has a 15-minute deadline. A timeout establishes no exclusion.

The new exclusion is independently replayed with exact integer arithmetic. A complete fresh replay is:

```bash
python -O verify.py --jobs 2 --out verification/current/recheck_O.jsonl
```

The authoritative decisions and two unresolved tensors are in `data/`.
The [frontier](../supplements/rank6/research/frontier/README.md) identifies the
current necessary reductions, and the model catalogue lists all realizations.
''');out['docs/VERIFY.md']=text
    text=read('manuscripts/README.md');lines=text.splitlines()
    for n,line in enumerate(lines):
        if line.startswith('| Rank six |'):lines[n]=f'| Rank six | [TeX](rank6/papers/manuscript.tex) | [PDF](rank6/papers/manuscript.pdf) | Complete through 3; exact bands {bands}; 57 realized and 2 unresolved through 8 |'
        elif line.startswith('| Rank six, verification guide |'):lines[n]='| Rank six, verification guide | [TeX](rank6/papers/verification_guide.tex) | [PDF](rank6/papers/verification_guide.pdf) | Exact models, exclusion certificates and two unresolved rings |'
    text='\n'.join(lines)+'\n';text=text[:text.index('The current rank-six paper')]+'''The current rank-six paper contains 16,553 general exclusions, 57 realizations
and two unresolved rings. A unified conformal-embedding section constructs
R6_4_22, R6_4_91 and R6_4_629. Superseded necessary-center searches have been
removed. The [current frontier](../supplements/rank6/research/frontier/README.md)
and [verification instructions](../docs/VERIFY.md) give the retained evidence.
''';out['manuscripts/README.md']=text
    text=read('supplements/README.md');text=re.sub(r'all four accepted exclusion continuations and the round-five refinements','accepted exclusion certificates and conformal constructions',text);lines=text.splitlines()
    for n,line in enumerate(lines):
        if line.startswith('| 6 |'):lines[n]=f'| 6 | [`rank6/software/`](rank6/software/) and [`verify.py`](rank6/verify.py) | Complete release; 16,553 excluded, 57 realized, 2 unresolved; complete through 3 and exact bands {bands} |'
    text='\n'.join(lines)+'\n';text=text[:text.index('For the rank-six update')]+f'''For the rank-six update, start with its [README](rank6/README.md),
[models](rank6/data/model_catalog.csv) and [current frontier](rank6/research/frontier/README.md).
The authoritative ledger is `rank6/data/decisions.json`. The archive is
`{a['name']}`. Source-bound certificates retain their internal paths.
''';out['supplements/README.md']=text
    text=read('oeis/README.md');out['oeis/README.md']=section(text,'Rank-six general classification','No zero beyond a proven finite',f'''Rank-six general classification is complete at exact multiplicities
**{bands}**, contiguously through **3**. The two unresolved rings occur
at multiplicities 4 and 8. The new models raise the multiplicity-four
realized lower bound to five. The exporter proposes only the rank-four and
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

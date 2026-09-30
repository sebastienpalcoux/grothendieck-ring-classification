#!/usr/bin/env python3
"""Render every cross-repository rank-six publication index from one identity.

No manuscript, supplement payload or website file is modified. Use --check
after integration, or --output-dir to review the proposed documents elsewhere.
"""
import argparse
import json
from pathlib import Path
from rank6_publication import validate_identity, archive_url, completed_bands, progress_table

ROOT = Path(__file__).resolve().parents[1]

def replace_section(text, start, end, replacement):
    a = text.index(start)
    b = text.index(end, a)
    return text[:a] + replacement + text[b:]

def render(repo, identity):
    validate_identity(identity)
    a, s = identity['archive'], identity['summary']
    ex, pos, op = (s[k] for k in ('excluded', 'positive', 'unresolved'))
    bands = completed_bands(identity)
    files = a['files']
    read = lambda name: (repo / name).read_text()
    out = {}
    previous = identity['previous_release']['archive']
    provenance = f"""The current rank-six release is
`{a['name']}`, SHA-256
`{a['sha256']}`.
The [complete {files:,}-file archive]({archive_url(identity)}) is reconstructed
from repository parts by `tools/restore_data.py`. Revision `round5`, dated
2026-09-30, adds **zero categorical exclusions**. The partition remains
**{ex:,} excluded, {pos} realized and {op} unresolved** among 16,612 tensors.
General categorifiability is complete through multiplicity three; the exact
completed bands are **{bands}**. Isolated higher completed bands do not
complete intervening unresolved bands.

The preceding v4 archive `{previous['name']}` had SHA-256
`{previous['sha256']}` and contained {previous['files']:,} files. That fourth
continuation added four exclusions, reducing ten residuals to six. The v3
archive had SHA-256
`853820839d767224c810f232e479a768ee9b16150876f10848aba07be3d578df`
and contained 914 files; its twelve exclusions reduced 22 residuals to ten.
The first two continuations added seven and eighteen exclusions, including
the final multiplicity-three case. All 577 rings through multiplicity three
remain classified: 531 excluded and 46 realized, including 45 unitary models.

The census tensors, identifiers, categorical decisions and 54 positive-model
identifications are unchanged. The [revision notes](../supplements/rank6/REVISION_NOTES.md)
and [round-five research inventory](../supplements/rank6/research/round5/coverage.json)
record the new unified necessary criteria and the exact finite reductions:

{progress_table(identity)}

No surviving necessary datum is promoted to a category. The joint word-pattern candidate for `R6_8_1660` and its twist witness are
separate necessary results.
The fourth exclusion file retains SHA-256
`{identity['fourth_certificate_sha256']}`; the third retains
`{identity['third_certificate_sha256']}`. All four accepted continuation
files, containing 7, 18, 12 and 4 exclusions, retain their proof provenance.

The new [replay orchestrator](../supplements/rank6/software/round5_replay.py)
and source-bound receipts distinguish the round-five exact computations from
the inherited profile enumerations, prior 41 continuation exclusions and
original 16,511-certificate campaign. The current update does not claim a
fresh replay of every earlier campaign. See [verification instructions](VERIFY.md)
for the recorded scopes and the commands for additional reconstruction.
The [current summary](../supplements/rank6/verification/release_summary.json)
and authoritative ledger retain the {ex}/{pos}/{op} partition.

"""
    text = replace_section(read('docs/PROVENANCE.md'), 'The current rank-six release is',
                           'The verified rank-seven release through', provenance)
    lines = text.splitlines()
    for n, line in enumerate(lines):
        if line.startswith('| 6 | `results/rank6/'):
            lines[n] = f'| 6 | `results/rank6/tables.txt.gz` | 8 | `supplements/rank6/data/decisions.json` | Complete through 3; exact bands {bands}; six general residuals through 8 |'
        elif line.startswith('| 6 | `') and '| 16,612 |' in line:
            lines[n] = f"| 6 | `{identity['ledger_sha256']}` | 16,612 | {ex:,} excluded; 53 unitary models; 1 spherical model with no pseudo-unitary categorification; six generally unresolved |"
    out['docs/PROVENANCE.md'] = '\n'.join(lines) + '\n'

    text = read('docs/VERIFY.md')
    text = text.replace('python3 tools/validate_release.py\npython3 tools/render_readme.py',
        'python3 tools/validate_release.py\npython3 tools/render_publication_docs.py --check\npython3 tools/render_readme.py')
    import re
    text = re.sub(r'Rank6_Categorification_M8_Revised_[0-9-]+_v[2345]\.zip', a['name'], text)
    text = replace_section(text, 'contains all ', '\n## Rebuild from the pinned census',
                           f"contains all {files:,} released files and the four unchanged exclusion\ncontinuations with 7, 18, 12 and 4 records. Round five adds no categorical\nexclusion; it contains the new exact necessary-profile and modular-data\nreductions. The archive is restored at `site/dist/downloads/{a['name']}`.\n")
    text = replace_section(text, '## Rank-six continuation evidence', '\n## Tensor crosswalks', f"""## Rank-six continuation evidence

From the complete mirrored release:

```bash
cd supplements/rank6
python check_manifest.py
python -O software/round5_replay.py --list
python -O software/round5_replay.py --check-receipts
python software/release_consistency.py
```

The first command checks the shipped bytes; receipt checking verifies the
recorded sources and their stated scope. Neither is a new mathematical
reconstruction. To rerun selected round-five criteria with numerical
optimizers disabled and assertions removed, use:

```bash
python -O software/round5_replay.py --select R6_4_629 --jobs 1
```

Omit `--select` to run the complete listed round-five suite, or choose its
`controls` entry. The [coverage inventory](../supplements/rank6/research/round5/coverage.json)
identifies each criterion's eligible cases, controls, exact outputs and
replay receipts. Read each entry's scope: inherited complete profile
enumerations are distinct from newly computed refinements. These tests
retain six unresolved rings, not six categorical constructions.

The joint restriction-word Gram and bounded integer criteria narrow the
finite profiles. Modular-word closure and finite representation enumeration
determine necessary modular completions for the retained branches.
`R6_4_629` includes an independent rational-arithmetic verification of the
rank-38 obstruction; its surviving rank-35 datum remains unresolved.
For `R6_8_1660`, the joint word patterns and twist witness are separate tests.

The unchanged accepted continuation files contain **7, 18, 12 and 4**
disjoint general exclusions. Their prior verification records are retained,
including `verification/round4/release_replay.json`. They and the original
16,511-certificate campaign are not relabelled as new round-five results.
A fresh full negative replay remains available with:

```bash
python -O verify.py --jobs 2 --out verification/current/recheck_O.jsonl
```

The authoritative ledger and six residual tensors are under `data/`.
Earlier summaries and discovery logs are historical evidence, while the
current release summary and round-five inventory state the present scope.
""")
    out['docs/VERIFY.md'] = text

    text = read('manuscripts/README.md')
    lines = text.splitlines()
    for n, line in enumerate(lines):
        if line.startswith('| Rank six |'):
            lines[n] = f'| Rank six | [TeX](rank6/papers/manuscript.tex) | [PDF](rank6/papers/manuscript.pdf) | Complete through 3; exact completed bands {bands}; six unresolved rings through 8 |'
        elif line.startswith('| Rank six, verification guide |'):
            lines[n] = '| Rank six, verification guide | [TeX](rank6/papers/verification_guide.tex) | [PDF](rank6/papers/verification_guide.pdf) | Four unchanged exclusion continuations and the new round-five necessary-data reductions, replay scopes and controls |'
    text = '\n'.join(lines) + '\n'
    start = text.index('The current rank-six paper')
    out['manuscripts/README.md'] = text[:start] + f"""The current rank-six paper retains the completed multiplicity-three proof
and all four accepted exclusion continuations. The fifth continuation adds
no categorical decisions: **{ex:,} exclusions, 54 realizations and six
unresolved rings** remain among 16,612 tensors. It unifies joint Gram,
rotation and modular-completion criteria and gives exact finite reductions
for every residual case. Necessary modular and fusion data are explicitly
distinguished from categorical models. See the
[revision notes](../supplements/rank6/REVISION_NOTES.md),
[research inventory](../supplements/rank6/research/round5/coverage.json) and
[verification instructions](../docs/VERIFY.md) for the complete current scope.
Previous papers and audit records retain their historical proof provenance.
"""

    text = read('supplements/README.md').replace('all three continuations', 'all four accepted exclusion continuations and the round-five refinements')
    lines = text.splitlines()
    for n, line in enumerate(lines):
        if line.startswith('| 6 |'):
            lines[n] = f'| 6 | [`rank6/software/`](rank6/software/) and [`verify.py`](rank6/verify.py) | Complete release included here; {ex:,} excluded, 54 realized, six unresolved; complete through multiplicity 3, with exact completed bands {bands} |'
    text = '\n'.join(lines) + '\n'; start = text.index('For the rank-six update')
    out['supplements/README.md'] = text[:start] + f"""For the rank-six update, start with its [README](rank6/README.md),
[revision notes](rank6/REVISION_NOTES.md),
[current release summary](rank6/verification/release_summary.json) and
[round-five coverage inventory](rank6/research/round5/coverage.json).
The original campaign and four exclusion continuations are kept separately;
the current decisions come from `rank6/data/decisions.json`. Round five makes
no categorical decision and supplies new finite necessary-data reductions
for all six residual rings. Use `python -O software/round5_replay.py --list`
inside `rank6/` to see the replay commands and their exact scopes. Earlier
accepted certificates and verification records retain their provenance.
The current archive is `{a['name']}`.
"""

    text = read('docs/history/rank6/README.md'); start = text.index('The current release is under')
    out['docs/history/rank6/README.md'] = text[:start] + f"""The current release is under [supplements/rank6](../../../supplements/rank6/),
with {ex:,} exclusions, 54 realized rings and six unresolved cases. General
classification is complete through multiplicity three; exact completed
bands are {bands}. Revision `round5` adds no categorical decisions. Its
finite profile and modular-data reductions are recorded in
`research/round5/coverage.json`, separately from the unchanged exclusion
certificates and their earlier replay records.

The files in this directory are preserved historical publication audits;
they do not define current totals. Current paper sources and PDFs are
retained in the manuscript mirror.
"""
    text = read('oeis/README.md')
    out['oeis/README.md'] = replace_section(text, 'Rank-six general classification',
        'No zero beyond a proven finite', f"""Rank-six general classification is complete at exact multiplicities
**{bands}**, with contiguous completion through multiplicity **3**.
Multiplicities 4, 5 and 8 remain partial, with six unresolved rings in total.
Round five adds necessary-data reductions but no categorical decisions, so
it changes no exact counting term. Isolated higher completed bands do not
extend the initial classification range or fill its intervening gaps.
Rank seven and eight have unresolved cases even in their first analyzed
bands. The exporter emits only the rank-four and rank-five drafts listed
above; no rank-six, rank-seven or rank-eight sequence file is proposed here.
""")
    return out

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT)
    parser.add_argument('--identity', type=Path)
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    identity = json.loads((args.identity or args.repo/'data/rank6_release_identity.json').read_text())
    files = render(args.repo, identity)
    destination = args.output_dir or args.repo
    for name, text in files.items():
        target = destination / name
        if args.check:
            if not target.is_file() or target.read_text() != text:
                raise ValueError('Publication document needs regeneration: ' + name)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
    print(('Checked' if args.check else 'Rendered') + f' {len(files)} publication documents')

if __name__ == '__main__':
    main()

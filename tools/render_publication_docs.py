#!/usr/bin/env python3
"""Render publication indexes from the frozen rank-six identity and upper-rank ledgers."""
import argparse,json,re
from pathlib import Path
from rank6_publication import (validate_identity,archive_url,completed_bands,
                              progress_table,validate_document_revision)
from publication_stages import load_stages,overview,replay_commands
ROOT=Path(__file__).resolve().parents[1]
def section(text,start,end,replacement):
    a=text.index(start);b=text.index(end,a);return text[:a]+replacement+text[b:]
def render(repo,i):
    validate_identity(i);out={};a=i['archive'];s=i['summary'];bands=completed_bands(i);bound=len(i['counts']);total=sum(r[0] for r in i['counts']);read=lambda n:(repo/n).read_text()
    revision=validate_document_revision(i,repo)
    revision_note=('''The October 11 theoretical revision proves that every dominant tensor
functor from either remaining rank-six category would be an equivalence,
without a pivotality assumption on the functor. Both categorification questions
remain unresolved. The current manuscript sources and PDFs are bound by the
[document revision](../evidence/rank6_theoretical_20261011/document_revision.json),
whose [research record](../evidence/rank6_theoretical_20261011/research_progress.json)
retains a hash-checked chain to the October 2 and frozen October 1 records.
The frozen supplement, archive identity and classification counts are unchanged.
''' if revision is not None else '')
    status=json.loads(read('data/classification_status.json'))
    upper={r:status['inputs'][f'rank{r}']for r in (7,8)}
    stage=load_stages(repo,status)
    latest=stage['decisions'];latest_models=stage['models'];latest_exclusions=stage['exclusions']
    bundles={b['name']:b['sha256']for b in status['bundles']}
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

{progress_table(i,repo)}

{revision_note}

''')
    lines=text.splitlines()
    for n,line in enumerate(lines):
        if line.startswith('| 6 | `results/rank6/'):
            lines[n]=f'| 6 | `results/rank6/tables.txt.gz` | {bound} | `supplements/rank6/data/decisions.json` | Complete through 3; exact bands {bands}; {s["unresolved"]} unresolved through {bound} |'
        elif line.startswith('| 6 | `') and 'results/rank6/' not in line:
            lines[n]=f"| 6 | `{i['ledger_sha256']}` | {total:,} | {s['excluded']:,} excluded; 56 unitary; 1 spherical non-pseudo-unitary; {s['unresolved']} unresolved |"
    text='\n'.join(lines)+'\n'
    text=section(text,'The verified rank-seven release through','\n| Rank | Census source',f'''The verified rank-seven release through
multiplicity four has SHA-256 `{bundles['rank7-certified-through-m4.zip']}`.
Multiplicity one is complete with thirteen realized rings. The rank-eight
release through multiplicity two has SHA-256
`{bundles['rank8-verified-supplement.zip']}`.
{overview(stage,'../')}
These proofs supplement the earlier
[46-decision stage](../evidence/residual_20261002/README.md).
The current general frontier has {upper[7]['status_totals']['unresolved']}
rank-seven and {upper[8]['status_totals']['unresolved']} rank-eight rings.
All positive tensors and negative source hypotheses are independently checked;
earlier unaffected records retain their exact preservation evidence.
Scope-specific obstructions do not change the general partition.
The [AnyonWiki evidence](../evidence/anyonwiki/README.md) retains the exact
associator and full-tensor checks supporting earlier positive constructions.
''')
    lines=text.splitlines()
    for n,line in enumerate(lines):
        for rank in (7,8):
            totals=upper[rank]['status_totals']
            if line.startswith(f'| {rank} | `results/rank{rank}/'):
                scope='Complete at multiplicity one; higher bands partial'if rank==7 else'Partial at both bands'
                ledger=upper[rank]['file']
                lines[n]=f'| {rank} | `results/rank{rank}/tables.txt.gz` | {upper[rank]["classified_through"]} | `{ledger}` | {scope}; {totals["unresolved"]} unresolved |'
            elif line.startswith(f'| {rank} | `'):
                count=sum(totals.values())
                lines[n]=f'| {rank} | `{upper[rank]["sha256"]}` | {count:,} | {totals["excluded"]:,} excluded; {totals["unitarily_realized"]} unitary models; {totals["unresolved"]} unresolved |'
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
    text=section(text,'The exporter records source checksums','Rank seven has ',f'''The exporter records source checksums and verifies cardinalities against
every census band. The released rows have no unassessed bands. Rank five is
complete through multiplicity 20. Rank six is complete through multiplicity
three, with exact completed bands {bands} and {s['unresolved']} cases through
multiplicity {bound} generally unresolved. Isolated completed bands do not
complete intervening unresolved bands.
''')
    text=section(text,'Rank seven has ','\nTo refresh only rank six',f'''Rank seven has {upper[7]['status_totals']['unresolved']} open cases through
multiplicity four, and rank eight has {upper[8]['status_totals']['unresolved']} through multiplicity two.
These are general categorification questions. Separate unitary-only obstructions
never change the general partition.
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
The dated October 1 research replay checks the completed R6_4_155 modular-data candidate,
finite indicator tests, and the R6_8_1660 module/Morita and 1,669-profile reductions.
Its exact scope and receipts are in `research/frontier/new_research/`. The October 2
[addendum](../evidence/residual_20261002/rank6/research_addendum.pdf) reduces the
second frontier further to 1,136 profiles and proves a pivotal tensor-quotient
obstruction. It also excludes braided Morita representatives and nontrivial
finite-group extensions or equivariantizations in either Morita class. These are
necessary conditions; both categorification questions remain unresolved.
Exact probability couplings also prove every Lim Corollary 3.4 inequality on
both six-element fusion bases, for every real exponent p >= 1 and nonnegative
input vector. Replay the source-bound certificates with
`python evidence/rank6_laptop_20261002/all_p_minkowski/verify.py --tensors supplements/rank6/data/unresolved_tensors.json`
from the repository root.
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
October 1 necessary reductions; the October 2 addendum and its portable
verifiers record subsequent progress. The model catalogue lists all realizations.
''')
    if revision_note:
        text=text.replace('\n## Tensor crosswalks','\n'+revision_note+
                          '\n`python tools/validate_release.py` checks the current document hashes, '
                          'the research chain and the frozen release identities; it does not '
                          'certify the new theoretical proofs.\n\n## Tensor crosswalks',1)
    upper_start=text.index('The upper-rank bundles retain') if 'The upper-rank bundles retain' in text else text.index('The rank-seven bundle includes')
    upper_end=text.index('The revised rank-five proof',upper_start)
    text=text[:upper_start]+'''The upper-rank bundles retain the earlier full-certificate runs, including the
rank-seven normal and optimized replays and the rank-eight exhaustive signed
proofs. Subsequent finite updates have separate reports that check new models,
new theoretical obstructions and exact preservation of earlier unaffected
records. Published upstream lemmas remain explicit citation dependencies;
external Normaliz or Groebner calculations are not claimed to have been rerun.

'''+text[upper_end:]
    text=text[:text.index('## AnyonWiki positive update')]+f'''## AnyonWiki positive update

Run `python tools/verify_anyonwiki_import.py` from the repository root. It checks
all 139 multiplicity-one tensor matches, the added model permutations, and three
published associators over exact cyclotomic fields. Its historical preservation
checks account explicitly for the separately certified October 2 changes.
Multiplicity one at rank seven is complete; rank eight currently has
{next(row['unresolved_general'] for row in status['rows'] if row['rank']==8 and row['multiplicity']==1)} generally open multiplicity-one cases.
See [the original evidence](../evidence/anyonwiki/README.md).

## October 2 residual update

{overview(stage,'../')}
The [earlier residual stage](../evidence/residual_20261002/README.md)
retains its own proofs and reports. Pivotal, pseudo-unitary, unitary and braided
obstructions are distinguished from general nonexistence. Replay the latest
source-bound stage in both normal and optimized Python:

```bash
{replay_commands(stage)}
```

The verifier checks all latest source identities, model tensors and certificates,
as well as preservation of earlier decisions.
The historical constructor replays run automatically against isolated copies
of their original ledgers and model catalogues. Their original entry points
are retained for provenance; they must not be run directly against an expanded
current catalogue without restoring the corresponding historical snapshot.

To refresh the upper-rank status and publication indexes from their ledgers:

```bash
python3 tools/update_upper_rank_status.py
python3 tools/export_grothendieck_counts.py
python3 tools/render_readme.py
python3 tools/render_publication_docs.py
python3 tools/validate_release.py
python3 tools/render_publication_docs.py --check
```

The upper-rank exporter preserves every lower-rank status row and input identity.
Archive checksums must be refreshed only after the corresponding bundle is rebuilt.
'''
    out['docs/VERIFY.md']=text
    text=read('manuscripts/README.md');lines=text.splitlines()
    for n,line in enumerate(lines):
        if line.startswith('| Rank six |'):lines[n]=f'| Rank six | [TeX](rank6/papers/manuscript.tex) | [PDF](rank6/papers/manuscript.pdf) | Complete through 3; exact bands {bands}; {s["positive"]} realized and {s["unresolved"]} unresolved through {bound} |'
        elif line.startswith('| Rank six, verification guide |'):lines[n]='| Rank six, verification guide | [TeX](rank6/papers/verification_guide.tex) | [PDF](rank6/papers/verification_guide.pdf) | Exact models, exclusion certificates and unresolved rings |'
        elif line.startswith('| Rank seven |'):lines[n]=f'| Rank seven | [TeX](rank7/papers/manuscript.tex) | [PDF](rank7/papers/manuscript.pdf) | Complete at multiplicity 1; {upper[7]["status_totals"]["unitarily_realized"]} realized and {upper[7]["status_totals"]["unresolved"]} unresolved through multiplicity 4 |'
        elif line.startswith('| Rank eight |'):lines[n]=f'| Rank eight | [TeX](rank8/paper/rank8.tex) | [PDF](rank8/paper/rank8.pdf) | Partial through multiplicity 2; {upper[8]["status_totals"]["unitarily_realized"]} realized and {upper[8]["status_totals"]["unresolved"]} generally unresolved |'
    text='\n'.join(lines)+'\n';text=text[:text.index('The current rank-six paper')]+f'''The current rank-six paper contains {s['excluded']:,} general exclusions, {s['positive']} realizations
and {s['unresolved']} unresolved rings through multiplicity {bound}. All 8,809 exact-multiplicity-nine
rings are excluded, including the final eleven cases proved in the completion chapter.
A unified conformal-embedding section constructs
R6_4_22, R6_4_91 and R6_4_629. Superseded necessary-center searches have been
removed. The [current frontier](../supplements/rank6/research/frontier/README.md)
and [verification instructions](../docs/VERIFY.md) give the retained evidence.
'''
    text+='\nThe dated [October 2 rank-six research addendum](../evidence/residual_20261002/rank6/research_addendum.pdf) records subsequent necessary reductions while preserving the October 1 release and its two unresolved categorification questions.\n'
    if revision_note:text+='\n'+revision_note
    text+=f"\n{overview(stage,'../')} The current frontier has {upper[7]['status_totals']['unresolved']} rank-seven and {upper[8]['status_totals']['unresolved']} rank-eight cases generally unresolved.\n"
    out['manuscripts/README.md']=text
    text=read('supplements/README.md');text=re.sub(r'all four accepted exclusion continuations and the round-five refinements','accepted exclusion certificates and conformal constructions',text);lines=text.splitlines()
    for n,line in enumerate(lines):
        if line.startswith('| 6 |'):lines[n]=f'| 6 | [`rank6/software/`](rank6/software/) and [`verify.py`](rank6/verify.py) | Complete release; {s["excluded"]:,} excluded, {s["positive"]} realized, {s["unresolved"]} unresolved; complete through 3 and exact bands {bands} |'
    for rank in (7,8):
        totals=upper[rank]['status_totals']
        row=f'| {rank} | [`rank{rank}/`](rank{rank}/) | Complete census through {upper[rank]["classified_through"]}; {totals["excluded"]:,} generally excluded, {totals["unitarily_realized"]} realized, {totals["unresolved"]} generally unresolved |'
        index=next((n for n,line in enumerate(lines) if line.startswith(f'| {rank} |')),None)
        if index is None:
            index=max(n for n,line in enumerate(lines) if line.startswith('| '))+1
            lines.insert(index,row)
        else:lines[index]=row
    text='\n'.join(lines)+'\n';text=text[:text.index('For the rank-six update')]+f'''For the rank-six update, start with its [README](rank6/README.md),
[models](rank6/data/model_catalog.csv) and [current frontier](rank6/research/frontier/README.md).
The authoritative ledger is `rank6/data/decisions.json`. The archive is
`{a['name']}`. Source-bound certificates retain their internal paths.
'''
    text+=f"\n{overview(stage,'../')} From the repository root, run `python3 {stage['verifier']}` and its optimized-Python counterpart.\n"
    out['supplements/README.md']=text
    text=read('oeis/README.md');out['oeis/README.md']=section(text,'Rank-six general classification','No zero beyond a proven finite',f'''Rank-six general classification is complete at exact multiplicities
**{bands}**, contiguously through **3**. The unresolved rings are recorded in the current frontier.
The rank-six fusion-ring census draft is separately extended by a(9)=8809;
it counts all based rings, regardless of categorifiability. The exporter proposes only the rank-four and
rank-five drafts listed above; no incomplete band is an exact sequence term.
''')
    rows={(r['rank'],r['multiplicity']):r for r in status['rows']}
    bounds7=[rows[(7,m)]['realized_unitary'] for m in (2,3,4)]
    open7=[rows[(7,m)]['unresolved_general'] for m in (2,3,4)]
    bounds8=[rows[(8,m)]['realized_unitary'] for m in (1,2)]
    open8=[rows[(8,m)]['unresolved_general'] for m in (1,2)]
    out['oeis/update_2026-10-02.txt']=f"""Suggested comment update (2 October 2026):

Counts refer to based-isomorphism classes of fusion rings admitting a fusion-category realization over the complex numbers, at exact multiplicity m. At rank seven, the multiplicity-one count is exactly 13. The confirmed lower bounds at multiplicities 2, 3 and 4 are {bounds7[0]}, {bounds7[1]} and {bounds7[2]}; respectively {open7[0]}, {open7[1]} and {open7[2]} general categorification questions remain unresolved. At rank eight, the confirmed lower bounds at multiplicities 1 and 2 are {bounds8[0]} and {bounds8[1]}; respectively {open8[0]} and {open8[1]} cases remain generally unresolved. These lower bounds are not exact sequence terms.

The combined October 2 upper-rank update resolves {len(latest)} further cases: {latest_exclusions} general exclusions and {latest_models} unitary models.{(f' Its {len(stage["continuation_ids"])}-decision continuation generally excludes '+', '.join(stage['continuation_ids'])+'.') if stage['continuation'] else ''} Across ranks seven and eight, the current partitions are respectively {upper[7]['status_totals']['excluded']} excluded, {upper[7]['status_totals']['unitarily_realized']} realized, {upper[7]['status_totals']['unresolved']} unresolved, and {upper[8]['status_totals']['excluded']} excluded, {upper[8]['status_totals']['unitarily_realized']} realized, {upper[8]['status_totals']['unresolved']} unresolved. General exclusion means no fusion-category categorification over the complex field, without an initial pivotality, sphericality or unitarity assumption. Scoped pivotal, pseudo-unitary, unitary or braided obstructions are not counted as general exclusions.

Rank six retains two unresolved cases through multiplicity 9, R6_4_155 and R6_8_1660. All 8809 fusion rings of exact multiplicity 9 are generally excluded. No count is changed by a necessary-condition reduction for an unresolved case.

Reference / link:
S. Palcoux, Grothendieck-ring classification, manuscripts and exact certificates, https://github.com/sebastienpalcoux/grothendieck-ring-classification/tree/main/evidence/{stage['latest']} .

This is a draft comment, not a submission. Preserve the target entry's existing indexing and definition. The number 8809 counts all fusion rings, not realized Grothendieck rings. Do not enter any incomplete-band lower bound as an exact sequence term.
"""
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


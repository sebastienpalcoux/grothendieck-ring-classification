"""Current rank-six publication text, derived from one release identity."""
from pathlib import PurePosixPath
DATE='2026-10-01'
REVISION='m9-frontier-v3'
ARCHIVE='Rank6_Categorification_M9_Frontier_2026-10-01.zip'
FRONTIER={'R6_4_155','R6_8_1660'}
COMPLETION_ROOT='research/exclusions/m9_completion'
COMPLETION_BUNDLES=('free_involution','involution_pair','gauss8200','pivotal_gap','psu25','case8785','triangle')
COMPLETION_FILES=(
    'certificates/m9_completion.jsonl',
    'software/m9_completion.py',
    'software/replay_m9_completion.py',
    *(f'verification/m9/completion/{name}' for name in
      ('input_manifest.json','summary.json','attempts.jsonl','replay_normal.json',
       'replay_optimized.json','proof_manifest.json','negative_controls.json')),
)
def require(test,message):
    if not test:raise ValueError(message)
def completion_files(package):
    """Inventory all completion evidence, including every portable proof file."""
    files=set(COMPLETION_FILES)
    for name in COMPLETION_BUNDLES:
        directory=package/COMPLETION_ROOT/name
        bundle={f.relative_to(package).as_posix() for f in directory.rglob('*')
                if f.is_file() and '__pycache__' not in f.parts}
        require(bundle,'Missing completion proof bundle: '+name)
        files.update(bundle)
    files.update(f.relative_to(package).as_posix()
                 for f in (package/COMPLETION_ROOT).rglob('*')
                 if f.is_file() and '__pycache__' not in f.parts)
    files.update(f.relative_to(package).as_posix()
                 for f in (package/'software').glob('*m9_completion*.py'))
    for name in files:require((package/name).is_file(),'Missing completion evidence: '+name)
    return sorted(files)
def valid_digest(digest):
    return isinstance(digest,str) and len(digest)==64 and all(c in '0123456789abcdef' for c in digest)
def valid_relative(name):
    path=PurePosixPath(name)
    return bool(name) and not path.is_absolute() and '..' not in path.parts and path.as_posix()==name
def validate_identity(identity):
    require(identity['revision']==REVISION and identity['date']==DATE,'Incorrect rank-six release identity')
    counts=identity['counts'];s=identity['summary']
    require(len(counts)==9 and sum(r[0] for r in counts)==25421 and counts[-1][0]==8809,'Incorrect source census')
    require(all(sum(r[1:])==r[0] for r in counts),'Incorrect band partition')
    require(s['excluded']==sum(r[1] for r in counts) and s['positive']==sum(r[2]+r[3] for r in counts) and s['unresolved']==sum(r[4] for r in counts),'Incorrect rank-six totals')
    require((s['excluded'],s['positive'],s['unresolved'])==(25362,57,2),'Incomplete multiplicity-nine release')
    require(counts[-1]==[8809,8809,0,0,0],'Multiplicity nine is not completely excluded')
    require(identity['new_exclusions']==counts[-1][1],'Incorrect multiplicity-nine exclusions')
    require(len(identity['research_progress'])==2 and {x['id'] for x in identity['research_progress']}==FRONTIER,'Incorrect unresolved frontier')
    require(set(identity['conformal_models'])=={'R6_4_22','R6_4_91','R6_4_629'},'Missing conformal realizations')
    require(len(identity['census_commit'])==40,'Missing pinned census revision')
    require(identity['archive']['name']==ARCHIVE,'Incorrect completed-release archive name')
    evidence=identity.get('completion_files_sha256',{})
    require(set(COMPLETION_FILES)<=set(evidence),'Incomplete completion evidence identity')
    require(all(any(name.startswith(COMPLETION_ROOT+'/'+bundle+'/') for name in evidence)
                for bundle in COMPLETION_BUNDLES),'Missing completion proof bundle identity')
    require(all(valid_relative(name) and valid_digest(digest) for name,digest in evidence.items()),'Invalid completion evidence hash')
    require('data/frontier_research_progress.json' in identity.get('research_files_sha256',{}),'Missing current frontier overlay identity')
    documents=identity.get('documents',{})
    require({'manuscript.tex','manuscript.pdf','verification_guide.tex','verification_guide.pdf'}<=set(documents),'Missing publication source or PDF identity')
    require(all(valid_relative(name) and item['path']=='papers/'+name and valid_digest(item['sha256']) and item['bytes']>0
                for name,item in documents.items()),'Invalid publication document identity')
def archive_url(identity):
    return 'https://grothendieck-ring-atlas.sebastien-palcoux.chatgpt.site/downloads/'+identity['archive']['name']
def completed_bands(identity):
    return ', '.join(str(m) for m,row in enumerate(identity['counts'],1) if row[-1]==0)
def progress_table(identity):
    return '\n'.join(['| Unresolved ring | Necessary reduction |','|---|---|']+[f"| `{x['id']}` | {x['result']} |" for x in identity['research_progress']])
def continuation_text(identity):
    validate_identity(identity);s=identity['summary'];last=identity['counts'][-1]
    return f'''The rank-six release covers **25,421 fusion rings through multiplicity 9**:
**{s['excluded']:,} excluded, {s['positive']} realized and {s['unresolved']} unresolved**.
All **8,809 rings of exact multiplicity nine are generally excluded**.
The completion certificates settle the final eleven cases; the two remaining
unresolved rings belong to earlier bands. Previous representatives and proof
certificates are preserved.

The positive catalogue includes the three neutral module categories from
`(B2)_7 ⊂ (D7)_1`, `(C3)_4 ⊂ (B10)_1`, and `(B2)_12 ⊂ (E8)_1`, with full tensor identifications.

{progress_table(identity)}

[Manuscript](manuscripts/rank6/papers/manuscript.pdf) ·
[Completion proofs](supplements/rank6/research/exclusions/m9_completion/) ·
[Completion replay](supplements/rank6/verification/m9/completion/) ·
[Current frontier](supplements/rank6/research/frontier/README.md) ·
[Complete release]({archive_url(identity)})
'''

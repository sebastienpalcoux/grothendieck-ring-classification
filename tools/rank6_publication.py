"""Current rank-six publication text, derived from one release identity."""
from pathlib import PurePosixPath, Path
import hashlib, json
DATE='2026-10-01'
REVISION='m9-frontier-v3'
ARCHIVE='Rank6_Categorification_M9_Frontier_2026-10-01.zip'
FRONTIER={'R6_4_155','R6_8_1660'}
RESEARCH_UPDATES=(
    'evidence/residual_20261002/rank6/research_progress.json',
    'evidence/rank6_theoretical_20261011/research_progress.json',
    'evidence/theoretical_20261016/rank6/research_progress.json',
)
DOCUMENT_REVISION='evidence/theoretical_20261016/rank6/document_revision.json'
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
def current_research(identity,repo=None):
    """Validate the dated research chain without changing the frozen release."""
    repo=Path(repo) if repo is not None else Path(__file__).resolve().parents[1]
    previous='supplements/rank6/data/frontier_research_progress.json'
    digest=identity['research_files_sha256']['data/frontier_research_progress.json']
    expected={'total':sum(row[0] for row in identity['counts']),
              'excluded':identity['summary']['excluded'],
              'realized':identity['summary']['positive'],
              'unresolved':identity['summary']['unresolved']}
    result=None
    for relative in RESEARCH_UPDATES:
        path=repo/relative
        if not path.is_file():
            continue
        raw=path.read_bytes();research=json.loads(raw)
        require(research['previous_coverage']==previous and
                research['previous_coverage_sha256']==digest,
                'Rank-six research update has a different prior source: '+relative)
        require(hashlib.sha256((repo/previous).read_bytes()).hexdigest()==digest,
                'Rank-six prior research source changed: '+previous)
        require(research['classification_counts']==expected,
                'Research update changes frozen classification counts: '+relative)
        require(len(research['cases'])==2 and
                {x['id'] for x in research['cases']}==FRONTIER and
                all(x['categorical_status']=='unresolved' and
                    isinstance(x['public_summary'],str) and x['public_summary'].strip()
                    for x in research['cases']),
                'Research update must preserve the unresolved frontier: '+relative)
        previous=relative;digest=hashlib.sha256(raw).hexdigest();result=research
    return result
def validate_document_revision(identity,repo=None):
    """Bind the current sources/PDFs separately from the frozen archive copies."""
    repo=Path(repo) if repo is not None else Path(__file__).resolve().parents[1]
    path=repo/DOCUMENT_REVISION
    if not path.is_file():
        require(not (repo/RESEARCH_UPDATES[-1]).is_file(),
                'Current theoretical research is missing its document revision')
        return None
    revision=json.loads(path.read_text())
    research=current_research(identity,repo)
    require(research is not None and revision['date']==research['date']=='2026-10-16',
            'Publication revision and current research dates differ')
    require(revision['research_progress']==RESEARCH_UPDATES[-1] and
            valid_digest(revision['research_progress_sha256']) and
            hashlib.sha256((repo/RESEARCH_UPDATES[-1]).read_bytes()).hexdigest()==revision['research_progress_sha256'],
            'Publication revision has a different research source')
    previous=revision.get('previous_document_revision')
    require(valid_relative(previous or '') and valid_digest(revision.get('previous_document_revision_sha256')) and
            hashlib.sha256((repo/previous).read_bytes()).hexdigest()==revision['previous_document_revision_sha256'],
            'Prior publication revision identity changed')
    documents=revision['documents'];prefix='manuscripts/rank6/papers/'
    current_files={f.relative_to(repo).as_posix() for f in (repo/prefix).rglob('*')
                   if f.is_file() and f.suffix in ('.tex','.pdf')}
    require(isinstance(documents,dict) and
            {name for name in documents if name.startswith(prefix)}==current_files,
            'Current manuscript source/PDF inventory differs from the revision')
    require({prefix+name for name in identity['documents']}<=set(documents),
            'Publication revision omits an existing source or PDF')
    for relative,item in documents.items():
        require(valid_relative(relative) and not relative.startswith('supplements/') and
                PurePosixPath(relative).suffix in ('.tex','.pdf') and
                valid_digest(item['sha256']) and type(item['bytes']) is int and item['bytes']>0,
                'Invalid current publication document identity: '+relative)
        raw=(repo/relative).read_bytes()
        require(len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256'],
                'Current publication document changed: '+relative)
    return revision
def progress_table(identity,repo=None):
    progress=identity['research_progress']
    research=current_research(identity,repo)
    if research is not None:
        progress=[{'id':x['id'],'result':x['public_summary']} for x in research['cases']]
    return '\n'.join(['| Unresolved ring | Necessary reduction |','|---|---|']+[f"| `{x['id']}` | {x['result']} |" for x in progress])
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

The October 16 revision identifies the entire twist-one support in the center
of a positive Galois representative of R6_8_1660 and retains tensor-functor
rigidity for both residual rings. Both categorification questions remain open.
The current source/PDF hashes are recorded separately from the frozen release.

[Manuscript](manuscripts/rank6/papers/manuscript.pdf) ·
[16 October theoretical update](evidence/theoretical_20261016/README.md) ·
[11 October theoretical revision](evidence/rank6_theoretical_20261011/README.md) ·
[Completion proofs](supplements/rank6/research/exclusions/m9_completion/) ·
[Completion replay](supplements/rank6/verification/m9/completion/) ·
[2 October research addendum](evidence/residual_20261002/rank6/research_addendum.pdf) ·
[Frozen 1 October release]({archive_url(identity)})
'''


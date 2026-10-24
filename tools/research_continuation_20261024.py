"""Accepted post-audit research; historical audit and proof scopes stay frozen."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
import hashlib,json,re,subprocess,sys,tempfile,zipfile
ROOT=Path(__file__).resolve().parents[1]
EVIDENCE='evidence/research_20261024'
LEDGER='supplements/rank8/output/research_20261024/ledger.json'
AUDIT=EVIDENCE+'/rank8_research_audit.json'
R8_PROOF='evidence/r436_repair_20261024'
R9='evidence/rank9_m2_20261024'
REMAINING_IDS=['R8_3_928','R8_3_941','R8_3_1154','R8_3_1768']
R9_REMAINING=['R9_2_137','R9_2_1607','R9_2_1975','R9_2_1976']
COUNTS={'excluded':2043,'unitarily_realized':36,'unresolved':4}
def active(repo=ROOT):return (Path(repo)/EVIDENCE/'accepted.json').is_file()
def read(repo,name):return json.loads((Path(repo)/name).read_text())
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def need(c,m):
    if not c:raise ValueError(m)
def validate(repo=ROOT):
    repo=Path(repo);a=read(repo,EVIDENCE+'/accepted.json')
    for name,h in a['source_sha256'].items():need(sha(repo/name)==h,'Research source changed: '+name)
    # The conservative audit remains valid as a historical, one-record decision.
    from audit_corrections_20261024 import validate as audit_validate
    audit_validate(repo)
    before=read(repo,a['rank8_baseline']);after=read(repo,LEDGER)
    need(len(before)==len(after)==4500,'Rank-eight coverage')
    for x,y in zip(before,after):
        need(x['id']==y['id'],'Rank-eight identity')
        if x['id']=='R8_3_436':
            need(x['status']=='unresolved' and y['status']=='excluded' and y['criterion']=='spherical_equivariantization_formal_codegree_field','R436 transition')
        else:need(x==y,'Unrelated rank-eight decision changed: '+x['id'])
    need(Counter(x['status'] for x in after)==Counter(excluded=4403,unitarily_realized=93,unresolved=4),'Rank-eight partition')
    before=read(repo,EVIDENCE+'/predecessor_rank9_ledger.json');after=read(repo,R9+'/ledger.json');actual=[]
    need(len(before)==len(after)==2083,'Rank-nine coverage')
    for x,y in zip(before,after):
        need(x['id']==y['id'] and x['tensor_sha256']==y['tensor_sha256'],'Rank-nine tensor identity')
        if x['status']!=y['status']:
            need(x['status']=='unresolved','Only residual cases may be settled')
            actual.append({'id':y['id'],'before':x['status'],'after':y['status']})
        else:need(x['exclusion_certificates']==y['exclusion_certificates'] and x['models']==y['models'],'Unrelated rank-nine evidence changed')
    need(actual==a['rank9_changes'] and len(actual)==14,'Rank-nine accepted transitions')
    need(Counter(x['status'] for x in after)==Counter(COUNTS),'Rank-nine partition')
    need([x['id'] for x in after if x['status']=='unresolved']==R9_REMAINING,'Rank-nine frontier')
    need([x['id'] for x in read(repo,R9+'/unresolved.json')]==R9_REMAINING,'Open metadata projection')
    return {'status':'PASS','date':'2026-10-24','rank8':{'excluded':3507,'unitarily_realized':16,'unresolved':4},'rank8_cumulative':{'excluded':4403,'unitarily_realized':93,'unresolved':4},'rank9':COUNTS,'remaining_ids_rank8':REMAINING_IDS,'remaining_ids_rank9':R9_REMAINING,'current_open_cases':11,'old_TPE_completeness_premise':'withdrawn','accepted':EVIDENCE+'/accepted.json'}
def publication_extension(repo=ROOT):
    repo=Path(repo)
    item=deepcopy(read(repo,'evidence/audit_20261024/predecessor_publication.json'))
    for key in ('metadata_path','metadata_sha256','attempts'):item.pop(key,None)
    item.update(date='2026-10-24',excluded=3507,unresolved=4,remaining_ids=REMAINING_IDS,unitary_excluded_ids=[],ledger=LEDGER,ledger_sha256=sha(repo/LEDGER),evidence=EVIDENCE,attempts_source=AUDIT,
        independent_R436_replacement={'proof':R8_PROOF+'/REPAIR.md','certificate':R8_PROOF+'/equivariantization_certificate.json','criterion':'spherical_equivariantization_formal_codegree_field'},
        historical_metadata_checkpoint='evidence/audit_20261024/predecessor_publication.json',historical_metadata_scope='Frozen pre-audit release; the audit and independent replacement are separate accepted steps.')
    return item
def revise_generated_tex(name,text,repo=ROOT):
    if name=='m3_frontier.tex':
        pattern=r'\\subsection\{A (?:conditional|general) inversion obstruction[^\n]*\n.*?(?=\\subsection|\Z)'
        text,n=re.subn(pattern,lambda _: (Path(repo)/R8_PROOF/'proof.tex').read_text()+'\n',text,count=1,flags=re.S)
        need(n==1 or 'thm:r436-equivariantization'in text,'Missing R436 proof replacement anchor')
        text=text.replace('These arithmetic tests exclude the listed routes except the general R436 branch. That branch requires the additional scalar-table completeness hypothesis; the unitary obstruction is retained. The uniform general exclusion of all five routes for all 34 tensors is not established.',
            'The arithmetic tests and the independent spherical-equivariantization exclusion of $\\sha{R8_3_436}$ exclude all five specified single-operation routes for the original frontier. No universal near-group unitarization theorem is used.')
    text=text.replace('The generally open case $\\sha{R8_3_436}$ retains its unitary exclusion. The other four open cases admit sphericality and Galois pseudo-unitarity reductions and have no braided Morita representatives.',
        'The four remaining open cases admit sphericality and Galois pseudo-unitarity reductions and have no braided Morita representatives. The separate spherical-equivariantization proof excludes $\\sha{R8_3_436}$ in general.')
    text=text.replace('the R436 claim is now conditional and is withheld from the current general ledger.',
        'the old R436 TPE premise was withdrawn, and its general exclusion now follows from an independent spherical-equivariantization proof.')
    return text
def revise_publication_document(name,text,repo=ROOT):
    text=re.sub(r'<!-- current-audit-correction -->.*?<!-- /current-audit-correction -->\n*','',text,flags=re.S)
    text=re.sub(r'<!-- current-research-continuation -->.*?<!-- /current-research-continuation -->\n*','',text,flags=re.S)
    text=text.replace('supplements/rank8/output/audited_20261024/ledger.json',LEDGER)
    replacements={
        'five current rank-eight questions':'four current rank-eight questions',
        'Two rank-six and five rank-eight categorification questions remain open.':'Two rank-six and four rank-eight categorification questions remain open.',
        'Apart from R8_3_436, four rank-eight general categorification questions remain:':'Four rank-eight general categorification questions remain:',
        'The remaining rings retain unresolved status for general complex categorification; R8_3_436 retains its unitary exclusion.':'The four remaining rings retain unresolved status for general complex categorification. R8_3_436 has an independent general exclusion.',
        'all 26 current open tensors':'all 11 current open tensors','all 26 present questions':'all 11 present questions','all 26 open tensors':'all 11 open tensors',
        'a conditional near-group TPE scalar-table reduction':'an independent spherical-equivariantization and formal-codegree obstruction',
        '4,402 general exclusions, 93 unitary models and five unresolved rings':'4,403 general exclusions, 93 unitary models and four unresolved rings',
        '3,506 exclusions, 16 models and five unresolved rings':'3,507 exclusions, 16 models and four unresolved rings',
        'R8_3_436 remains excluded in the unitary setting.':'R8_3_436 is excluded generally by the independent replacement proof.',
    }
    for a,b in replacements.items():text=text.replace(a,b)
    text=text.replace('The first command reconciles the single R436 correction, checks current','The first command reconciles the frozen audit and the new research, checks current')
    text=text.replace('Neither mode is a fresh replay of every categorical exclusion.','Full mode also freshly replays the accepted rank-nine continuations and the R436 replacement. Neither mode repeats every earlier categorical exclusion.')
    if name.startswith('docs/') or name in ('manuscripts/README.md','site/README.md'):
        notice='''<!-- current-research-continuation -->
**Current results · 24 October 2026.** Rank-nine exact multiplicity two has
2,043 general exclusions, 36 unitary models and four unresolved rings.
R8_3_436 is generally excluded by an independent spherical-equivariantization
proof; the old TPE completeness premise remains withdrawn. The project has
11 open cases. [Proofs, precise scope and replay](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/research_20261024/README.md).
<!-- /current-research-continuation -->'''
        at=text.find('\n\n');text=text[:at]+'\n\n'+notice+text[at:]
    text=re.sub(r'Current classification through rank eleven: \d+ unresolved rings', 'Current classification through rank eleven: 11 unresolved rings',text)
    text=text.replace('**Rank 9:** through multiplicity two, 2,135 general exclusions, 72 unitary models and 18 unresolved. Exact multiplicity two contributes 2,033 exclusions and 32 models.',
        '**Rank 9:** through multiplicity two, 2,145 general exclusions, 76 unitary models and four unresolved. Exact multiplicity two contributes 2,043 exclusions and 36 models.')
    return text
def replay(repo=ROOT):
    repo=Path(repo);logs=[]
    with tempfile.TemporaryDirectory(prefix='rank9-current-replay-') as d:
        with zipfile.ZipFile(repo/R9/'replay.zip') as z:z.extractall(d)
        root=Path(d)/'Rank9_M2_Theoretical_Continuation_20261023'
        for script,args in [('phase4/verify.py',[]),('verify.py',['--frontier'])]:
            r=subprocess.run([sys.executable,str(root/script),*args],cwd=root,text=True,capture_output=True)
            need(r.returncode==0,'Accepted finite replay failed '+script+'\n'+r.stdout+r.stderr)
            logs.append({'script':script,'status':'PASS','assertions_enabled':True})
    r=subprocess.run([sys.executable,str(repo/R8_PROOF/'verify_equivariantization.py')],cwd=repo,text=True,capture_output=True)
    need(r.returncode==0,'R436 exact replay failed\n'+r.stdout+r.stderr)
    logs.append({'script':R8_PROOF+'/verify_equivariantization.py','status':'PASS'})
    return logs

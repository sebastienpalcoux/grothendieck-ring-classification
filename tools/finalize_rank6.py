#!/usr/bin/env python3
"""Freeze a verified rank-six package, archive and repository identity."""
import argparse,hashlib,json,shutil,zipfile
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--package',type=Path,required=True);p.add_argument('--archive',type=Path,required=True);a=p.parse_args();P=a.package.resolve();repo=Path(__file__).resolve().parents[1];out=a.archive.resolve()
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
for f in list(P.rglob('__pycache__')):
    if f.is_dir():shutil.rmtree(f)
for f in (P/'software').iterdir():
    if f.is_file() and f.suffix=='':f.unlink()
files=sorted(f for f in P.rglob('*') if f.is_file() and f.name!='SHA256SUMS')
(P/'SHA256SUMS').write_text(''.join(sha(f)+'  '+str(f.relative_to(P))+'\n' for f in files))
out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for f in sorted(P.rglob('*')):
        if f.is_file():z.write(f,P.name+'/'+str(f.relative_to(P)))
summary=json.loads((P/'verification/release_summary.json').read_text());counts=json.loads((P/'data/classification_counts.json').read_text());front=json.loads((P/'data/frontier_summary.json').read_text());constructors=json.loads((P/'data/conformal_positive_models.json').read_text())
identity={'schema':'rank6-release-identity/v1','date':'2026-09-30','revision':'v7','new_exclusions':1,'new_exclusion_ids':['R6_5_1204'],'new_realizations':[r['id'] for r in constructors],'research_summary':'Three unitary conformal-embedding models are constructed and matched in all 216 fusion coefficients. Exact center rotation integrality excludes R6_5_1204. Two rings remain unresolved. Fermion traces and Gauss sums leave one rank-52 center profile for R6_4_155. Fermion orbits and second-indicator congruences leave 1727 center profiles for R6_8_1660.','research_progress':[{'id':r['id'],'result':r['public_summary']} for r in front['cases']],'archive':{'name':out.name,'sha256':sha(out),'bytes':out.stat().st_size,'files':len(files)+1},'ledger_sha256':sha(P/'data/decisions.json'),'summary':{k:summary[k] for k in ['excluded','positive','unresolved','first_unresolved','complete_through_multiplicity','third_continuation_excluded','fourth_continuation_excluded']},'counts':[[c[k] for k in ['classes','excluded','unitarily_realized','spherically_realized_nonpseudounitary','unresolved']] for c in counts],'third_certificate_sha256':sha(P/'certificates/continuation_round3.jsonl'),'fourth_certificate_sha256':sha(P/'certificates/continuation_round4.jsonl'),'research_files_sha256':{f:sha(P/f) for f in ['data/conformal_positive_models.json','data/frontier_summary.json','research/frontier/coverage.json','research/frontier/R6_4_155/center_cuts_certificate.json','research/frontier/R6_4_155/forced_twists_certificate.json','research/frontier/R6_4_155/verify_center_cuts.py','research/frontier/R6_8_1660/fermion_profiles/fermion_profiles_certificate.json','research/frontier/R6_8_1660/relative_center/relative_reduction_certificate.json','software/conformal_models.py','software/center_integrality.py','certificates/structural_exclusions.jsonl','research/exclusions/R6_5_1204/exact_trace_h6.json','research/exclusions/R6_5_1204/forced_W.json','research/exclusions/R6_5_1204/verify_exclusion.py','research/frontier/R6_8_1660/relative_center/structural_cuts_certificate.json']}}
identity['documents']={name:{'path':'papers/'+name,'sha256':sha(P/'papers'/name),'bytes':(P/'papers'/name).stat().st_size} for name in ('manuscript.pdf','verification_guide.pdf')}
(repo/'data/rank6_release_identity.json').write_text(json.dumps(identity,indent=2)+'\n')
for source,target in [(P,repo/'supplements/rank6'),(P/'papers',repo/'manuscripts/rank6/papers')]:
    if target.exists():shutil.rmtree(target)
    shutil.copytree(source,target)
download=repo/'site/dist/downloads'/out.name;download.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(out,download)
manifest=repo/'data/large_files_manifest.json';m=json.loads(manifest.read_text());kept=[]
for record in m['files']:
    removed=(record['path'].startswith('supplements/rank6/') and not (repo/record['path']).exists()) or record['path'].startswith('site/dist/downloads/Rank6_Categorification_M8_')
    if removed:
        for part in record.get('parts',[]):
            path=repo/part['path']
            if path.exists():path.unlink()
    else:kept.append(record)
kept.append({'path':str(download.relative_to(repo)),'encoding':'raw','parts':[]});m['files']=kept;manifest.write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps(identity['archive'],indent=2))

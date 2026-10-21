#!/usr/bin/env python3
"""Package accepted rank-eight M3 evidence with repository-relative paths."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import zipfile
from rank8_publication import extension, summary, LEDGER, MODELS, TABLES, ARCHIVE, EVIDENCE
ROOT=Path(__file__).resolve().parents[1]
SUFFIXES={'.py','.cpp','.h','.hpp','.json','.jsonl','.gz','.txt','.md','.tex','.pdf','.csv','.sage'}
def require(value,message):
    if not value:raise ValueError(message)
def digest(raw):return hashlib.sha256(raw).hexdigest()
def collect(root):
    current=extension(root);require(current is not None,'Accepted M3 publication ledger required')
    receipt=json.loads((root/EVIDENCE/'pipeline/continuation_replay.json').read_text())
    optimized=json.loads((root/EVIDENCE/'pipeline/continuation_replay_optimized_invocation.json').read_text())
    require(receipt.get('status')=='PASS','Complete mathematical replay required')
    require(optimized.get('status')=='PASS' and optimized['ledger_digest']==receipt['ledger_digest'],'Matching optimized replay required')
    require(optimized['source_manifests_sha256']==receipt['source_manifests_sha256'] and optimized['proof_source_sha256']==receipt['proof_source_sha256'],'Normal and optimized sources differ')
    paths={LEDGER,MODELS,TABLES,'tools/rank8_publication.py','tools/rank7_publication.py','tools/build_rank8_m3_release.py','tools/audit_rank8_manuscript.py','supplements/rank7/requirements-m5.txt'}
    paths.update(receipt['proof_source_sha256']);paths.update(receipt['source_manifests_sha256'])
    for replay in (receipt,optimized):paths.update(section['log'] for section in replay['sections'])
    for folder in (EVIDENCE,'supplements/rank8/software','supplements/rank8/experimental_signed','supplements/rank8/data','supplements/rank8/output/m3','supplements/rank6/software','supplements/rank6/data','supplements/rank7/software','supplements/rank7/data','manuscripts/rank8/paper'):
        paths.update(p.relative_to(root).as_posix() for p in (root/folder).rglob('*') if p.is_file() and p.name!='release_manifest.json' and p.suffix in SUFFIXES and '__pycache__' not in p.parts and not any(part.startswith('.') for part in p.relative_to(root).parts))
    paths.update(('supplements/rank7/output/rank7_ledger.json','supplements/rank7/analyze.py','supplements/rank7/zero_spectrum7.cpp'))
    files={p:(root/p).read_bytes() for p in sorted(paths)}
    for field in ('proof_source_sha256','source_manifests_sha256'):
        for relative,sha in receipt[field].items():require(digest(files[relative])==sha,'Frozen input changed: '+relative)
    for replay in (receipt,optimized):
        for section in replay['sections']:require(digest(files[section['log']])==section['log_sha256'],'Replay log changed: '+section['log'])
    files['README.md']=(
        '# Rank-eight continuation through multiplicity three\n\n'+summary(root)+'\n\n'
        'The 973 historical records and input files are preserved. All 3,527 new source tensors are covered; complete enumeration remains a producer claim. Every recorded M3 model admits a unitary realization.\n\n'
        'From this directory, with Python 3.12 and a C++17 compiler:\n\n```sh\n'
        'python -m pip install -r supplements/rank7/requirements-m5.txt\n'
        'python supplements/rank8/software/verify_m3_continuation.py\n'
        'python -O supplements/rank8/software/verify_m3_continuation.py\n```\n\n'
        'The optimized invocation launches inherited assertion-based checks in a fresh unoptimized interpreter. '
        '`--metadata-only` checks source identities and full-replay bindings without redoing the mathematics. '
        'Transferred lower-rank exclusions retain their published theorem and exact decision/tensor binding; full historical lower-rank replays remain separately available in the repository.\n\n'
        'Current article: `manuscripts/rank8/paper/rank8.pdf`. Residual tensors and attempts: `evidence/rank8_m3_20261021/pipeline/`. Passing necessary conditions does not construct coherent associators.\n\n'
        'AI-generated research; independent human verification and Lean formalization remain pending.\n').encode()
    files['SHA256SUMS.json']=(json.dumps({p:digest(raw) for p,raw in files.items()},indent=2)+'\n').encode()
    return files,current

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,default=ROOT);p.add_argument('--output',type=Path)
    args=p.parse_args();root=args.repo.resolve();files,current=collect(root)
    with tempfile.TemporaryDirectory(prefix='rank8-m3-package-') as directory:
        test=Path(directory)
        for name,raw in files.items():
            target=test/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
        run=subprocess.run([sys.executable,str(test/'supplements/rank8/software/verify_m3_continuation.py'),'--metadata-only','--output',str(test/'metadata.json')],cwd=test,text=True,capture_output=True)
        require(run.returncode==0,'Standalone metadata check failed:\n'+run.stdout+run.stderr)
        require(json.loads((test/'metadata.json').read_text())['status']=='METADATA_PASS','Standalone receipt missing')
    output=(args.output or root/ARCHIVE).resolve();output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,raw in sorted(files.items()):
            info=zipfile.ZipInfo('rank8-certified-through-m3/'+name,date_time=(2026,10,21,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            z.writestr(info,raw,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    manifest={'date':'2026-10-21','classification':current,'files_sha256':{p:digest(raw) for p,raw in sorted(files.items())},'standalone_metadata_check':'PASS','archive_sha256':digest(output.read_bytes())}
    (root/'supplements/rank8/output/m3/release_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'output':str(output),'files':len(files),'bytes':output.stat().st_size,'sha256':manifest['archive_sha256'],'standalone_metadata_check':'PASS'},indent=2))
if __name__=='__main__':main()

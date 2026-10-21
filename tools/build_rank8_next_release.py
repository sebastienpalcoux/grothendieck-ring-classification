#!/usr/bin/env python3
"""Build a distinct source-bound continuation over the immutable frontier ZIP.

Every baseline member is retained byte-for-byte, either at its original path
or, for superseded publication tools/papers, under baseline_members. This
builder performs extracted metadata checks only: targeted new mathematical
verifications are documented by their separate receipts. It never launches
the full historical replay campaign.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import zipfile

ROOT=Path(__file__).resolve().parents[1]
BASELINE_ARCHIVE='supplements/rank8/release/rank8-certified-frontier-20261021.zip'
BASELINE_SHA256='9ceca7868f88e9b2394c56d72c15e4b06afaa8a2c9a60bcf27133487d674f59a'
BASELINE_PREFIX='rank8-certified-frontier-20261021/'
ARCHIVE='supplements/rank8/release/rank8-certified-next-20261021.zip'
ARCHIVE_PREFIX='rank8-certified-next-20261021/'
EVIDENCE='evidence/rank8_next_20261021'
PUBLICATION=EVIDENCE+'/publication'
OUTPUT='supplements/rank8/output/next_20261021'
SUFFIXES={'.py','.cpp','.h','.hpp','.json','.jsonl','.gz','.txt','.md','.tex',
          '.pdf','.csv','.sage','.g','.log','.bib'}

def need(ok,message):
    if not ok:raise ValueError(message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def safe_path(name):
    p=PurePosixPath(name)
    return bool(name)and not p.is_absolute()and'..'not in p.parts and p.as_posix()==name
def json_bytes(value):return(json.dumps(value,indent=2,sort_keys=True)+'\n').encode()
def helper(repo):
    p=repo/'tools/rank8_next.py';need(p.is_file(),'Missing current ledger helper')
    spec=importlib.util.spec_from_file_location('rank8_next_package_helper',p)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def read_baseline(repo):
    path=repo/BASELINE_ARCHIVE
    need(sha(path.read_bytes())==BASELINE_SHA256,'Immutable frontier archive changed')
    files={}
    with zipfile.ZipFile(path)as archive:
        for item in archive.infolist():
            need(not item.is_dir()and item.filename.startswith(BASELINE_PREFIX),'Unexpected baseline member')
            name=item.filename[len(BASELINE_PREFIX):]
            need(safe_path(name)and name not in files,'Unsafe/duplicate baseline path')
            need((item.external_attr>>16)&0o170000!=0o120000,'Baseline symlink rejected')
            files[name]=archive.read(item)
    checks=json.loads(files['SHA256SUMS.json'])
    need(set(checks)==set(files)-{'SHA256SUMS.json'},'Complete baseline checksum coverage')
    need(all(sha(files[name])==value for name,value in checks.items()),'Baseline member checksum mismatch')
    return files

def overlay_inputs(repo):
    h=helper(repo);summary=h.validate_ledger(repo);inventory=h.source_inventory(repo)
    manifest=PUBLICATION+'/source_manifest.json'
    target=repo/manifest;target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(json_bytes(inventory))
    paths=set(inventory)|{manifest,'tools/build_rank8_next_release.py'}
    # The earlier ZIP predates completion of its optimized replay lane. Carry
    # those already completed, immutable receipts and their bound logs forward
    # so the extracted historical metadata verifier can check both lanes.
    frontier_publication='evidence/rank8_frontier_20261021/publication'
    for lane in('normal','optimized'):
        receipt=f'{frontier_publication}/replay_{lane}.json'
        report=json.loads((repo/receipt).read_text())
        need(report.get('status')=='PASS'and report.get('mathematical_replay_performed')is True,
             'Missing completed historical replay: '+lane)
        paths.add(receipt)
        for section in report['sections']:
            log=section['log']
            need(safe_path(log)and sha((repo/log).read_bytes())==section['log_sha256'],
                 'Historical replay log mismatch: '+log)
            paths.add(log)
    for folder in(EVIDENCE,OUTPUT,'tools','manuscripts/rank8/paper'):
        for path in(repo/folder).rglob('*'):
            rel=path.relative_to(repo);name=rel.as_posix()
            if(not path.is_file()or path.is_symlink()or'__pycache__'in rel.parts
               or any(t.startswith('.')for t in rel.parts)or path.suffix not in SUFFIXES):continue
            if(name in{PUBLICATION+'/release_manifest.json',PUBLICATION+'/package_manifest.json'}
               or name.startswith(PUBLICATION+'/baseline_members/')):continue
            paths.add(name)
    for name in paths:need(safe_path(name)and(repo/name).is_file(),'Missing/unsafe overlay input: '+name)
    return paths,summary,inventory

def collect(repo):
    baseline=read_baseline(repo);paths,summary,inventory=overlay_inputs(repo)
    files=dict(baseline);replacements={};preserved={}
    for name in sorted(paths):
        raw=(repo/name).read_bytes()
        if name in baseline and raw!=baseline[name]:
            need(name.startswith(('tools/','manuscripts/rank8/paper/')),
                 'Refusing to change historical evidence/data: '+name)
            historical=PUBLICATION+'/baseline_members/'+name
            need(historical not in files,'Historical replacement path collision')
            files[historical]=baseline[name]
            replacements[name]={'historical_path':historical,'baseline_sha256':sha(baseline[name]),'current_sha256':sha(raw)}
        files[name]=raw
    for name in('README.md','SHA256SUMS.json'):
        files[PUBLICATION+'/baseline_members/'+name]=baseline[name]
    for name,raw in baseline.items():
        historical=(PUBLICATION+'/baseline_members/'+name if name in('README.md','SHA256SUMS.json')
                    else replacements.get(name,{}).get('historical_path',name))
        need(files[historical]==raw,'Baseline byte preservation failed: '+name)
        preserved[name]={'path':historical,'sha256':sha(raw)}
    files['README.md']=(
        '# Rank-eight certified continuation, 21 October 2026\n\n'
        'This separate release preserves every member of the prior frontier archive byte-for-byte. '
        'It adds the unitary realization of R8_3_721 and separately scoped necessary-condition '
        'research on the remaining rank-eight cases. Current decisions and models are in '
        f'`{OUTPUT}/ledger.json` and `{OUTPUT}/model_catalog.json`. '
        'The current article is `manuscripts/rank8/paper/rank8.pdf`.\n\n'
        'The R721 construction uses the actual inherited Q-system 1+rho in the C2 '
        'de-equivariantization of the known C8 generalized-Haagerup category. A proved rank '
        'and multiplicity bound, followed by uniqueness in the supplied complete census, '
        'identifies its Morita dual. The explicit associator of that dual is not independently '
        'extracted. Numerical feasibility, modular data, and remaining integer-center witnesses '
        'are not represented as categorical models.\n\n'
        'Current metadata check:\n\n'
        '```sh\npython tools/rank8_next.py --check\n'
        'python -O tools/rank8_next.py --check\n```\n\n'
        'Targeted mathematical verification commands and source-bound receipts are listed in '
        f'`{PUBLICATION}/source_manifest.json` and the current evidence tree. '
        'The packaging check verifies extracted metadata and checksums; it does not rerun '
        'the full historical mathematical campaign. The original completed replay receipts '
        'remain intact. Superseded tools, papers, and archive metadata are retained under '
        f'`{PUBLICATION}/baseline_members/`. `{PUBLICATION}/package_manifest.json` records the exact '
        'location and digest of every preserved baseline member.\n'
    ).encode()
    package={'schema':'rank8-next-package/v1','date':'2026-10-21',
        'baseline_archive':BASELINE_ARCHIVE,'baseline_archive_sha256':BASELINE_SHA256,
        'baseline_members':len(baseline),'baseline_byte_preservation':preserved,
        'publication_replacements':replacements,'current_summary':summary,
        'new_source_manifest_sha256':sha(files[PUBLICATION+'/source_manifest.json']),
        'overlay_input_sha256':{name:sha(files[name])for name in sorted(paths)},
        'publication_mode':'targeted_proof_receipts_and_extracted_metadata',
        'full_historical_mathematical_replay_performed':False,
        'packaging_mathematical_replay_performed':False}
    files[PUBLICATION+'/package_manifest.json']=json_bytes(package)
    files['SHA256SUMS.json']=json_bytes({name:sha(raw)for name,raw in sorted(files.items())if name!='SHA256SUMS.json'})
    return files,package,inventory

def extracted_checks(files):
    checks=[]
    with tempfile.TemporaryDirectory(prefix='rank8-next-package-')as directory:
        repo=Path(directory)
        for name,raw in files.items():
            need(safe_path(name),'Unsafe extracted member')
            path=repo/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
        expected=json.loads(files['SHA256SUMS.json'])
        need(all(sha((repo/p).read_bytes())==v for p,v in expected.items()),'Extracted checksum mismatch')
        for script in('supplements/rank8/software/verify_m3_continuation.py',
                      'tools/verify_rank8_frontier.py','tools/rank8_next.py'):
            need((repo/script).is_file(),'Missing extracted metadata verifier: '+script)
            for optimized in(False,True):
                command=[sys.executable]+(['-O']if optimized else[])+[script,'--check'if script=='tools/rank8_next.py'else'--metadata-only']
                env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None)
                env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
                run=subprocess.run(command,cwd=repo,env=env,text=True,capture_output=True)
                need(run.returncode==0,'Extracted metadata failed: '+script+'\n'+run.stdout+run.stderr)
                report=json.loads(run.stdout)
                if script=='tools/rank8_next.py':
                    need(report.get('resolved_ids')==['R8_3_721']and report.get('ledger')==OUTPUT+'/ledger.json','Unexpected current ledger validation')
                    status='METADATA_PASS'
                else:
                    status=report.get('status');need(status in('METADATA_PASS','SOURCE_METADATA_PASS'),'Unexpected metadata status: '+script)
                checks.append({'script':script,'optimized_python':optimized,'status':status,
                               'report_sha256':sha(run.stdout.encode()),'mathematical_replay_performed':False})
        need(all(sha((repo/p).read_bytes())==v for p,v in expected.items()),'Metadata check changed a packaged input')
    return checks

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=ROOT)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--collect-only',action='store_true',help='Validate inputs and report inventory without writing an archive')
    args=parser.parse_args();repo=args.repo.resolve();output=(args.output or repo/ARCHIVE).resolve()
    need(output!=(repo/BASELINE_ARCHIVE).resolve(),'Cannot overwrite the immutable frontier archive')
    need(not output.is_relative_to(repo/EVIDENCE),'Archive must not be written inside its evidence inputs')
    files,package,inventory=collect(repo)
    if args.collect_only:
        print(json.dumps({'status':'COLLECT_PASS','members':len(files),'baseline_preserved':package['baseline_members'],
                          'overlay_members':len(package['overlay_input_sha256']),'current_summary':package['current_summary']},indent=2));return
    package['extracted_metadata_checks']=extracted_checks(files)
    files[PUBLICATION+'/package_manifest.json']=json_bytes(package)
    files['SHA256SUMS.json']=json_bytes({name:sha(raw)for name,raw in sorted(files.items())if name!='SHA256SUMS.json'})
    need(sha((repo/BASELINE_ARCHIVE).read_bytes())==BASELINE_SHA256,'Baseline archive changed during packaging')
    need(helper(repo).source_inventory(repo)==inventory,'Current proof sources changed during packaging')
    for name,digest in package['overlay_input_sha256'].items():
        need(sha((repo/name).read_bytes())==digest,'Overlay input changed during packaging: '+name)
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(prefix=output.name+'.',suffix='.tmp',dir=output.parent,delete=False)as handle:temporary=Path(handle.name)
    try:
        with zipfile.ZipFile(temporary,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as archive:
            for name,raw in sorted(files.items()):
                info=zipfile.ZipInfo(ARCHIVE_PREFIX+name,date_time=(2026,10,21,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
                archive.writestr(info,raw,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
        temporary.replace(output)
    finally:temporary.unlink(missing_ok=True)
    manifest={**package,'files_sha256':{name:sha(raw)for name,raw in sorted(files.items())},'archive_sha256':sha(output.read_bytes())}
    target=repo/PUBLICATION/'release_manifest.json';target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(json_bytes(manifest))
    print(json.dumps({'status':'PASS','archive':str(output),'bytes':output.stat().st_size,
                      'sha256':manifest['archive_sha256'],'members':len(files),
                      'baseline_members_preserved':len(package['baseline_byte_preservation']),
                      'extracted_metadata_checks':package['extracted_metadata_checks'],
                      'full_historical_mathematical_replay_performed':False},indent=2))

if __name__=='__main__':main()

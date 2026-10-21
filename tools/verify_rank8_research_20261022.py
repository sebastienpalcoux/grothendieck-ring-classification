#!/usr/bin/env python3
"""Source-bound targeted replay of the accepted 22 October rank-eight stage.

Normal and -O invocations produce separate receipts. Every mathematical
child runs with assertions enabled, including transitive historical imports.
This does not rerun the full historical classification campaign.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse
import ast
import json
import os
import subprocess
import sys
import time
from rank8_research_20261022 import (
    ROOT, PUBLICATION, commands, need, safe_path, sha, source_inventory,
    validate_ledger,
)


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True)+'\n').encode()


def check_reports(repo, summary, inventory):
    pub=repo/PUBLICATION
    manifest=pub/'source_manifest.json'
    need(json.loads(manifest.read_text())==inventory,'Accepted research source inventory changed; prepare and replay again')
    manifest_sha=sha(manifest.read_bytes())
    required=commands(repo)
    need(required and len(set(required))==len(required),'Accepted targeted mathematical checks must be nonempty and distinct')
    receipts=[]
    for flag,lane in [(False,'normal'),(True,'optimized')]:
        path=pub/f'replay_{lane}.json';report=json.loads(path.read_text())
        need(report['status']=='PASS' and report['mathematical_replay_performed'] is True,
             'Missing full targeted replay: '+lane)
        need(report['optimized_python_requested']==flag and
             report['all_mathematical_children_assertions_enabled'] is True,
             'Wrong or unsafe replay lane: '+lane)
        need(report['source_manifest_sha256']==manifest_sha and
             report['ledger_sha256']==summary['ledger_sha256'] and
             report['accepted_sha256']==summary['accepted_sha256'],'Replay belongs to different accepted sources')
        need([r['script']for r in report['sections']]==required,'Incomplete targeted replay coverage')
        for item in report['sections']:
            need(item['returncode']==0 and item['python_optimization']==0 and
                 item['assertions_enabled'] is True,'Unsafe mathematical child')
            name=item['log'];need(safe_path(name),'Unsafe replay log path')
            need(sha((repo/name).read_bytes())==item['log_sha256'],'Replay log changed: '+name)
        receipts.append(sha(path.read_bytes()))
    return manifest_sha,receipts


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=ROOT)
    parser.add_argument('--prepare',action='store_true')
    parser.add_argument('--metadata-only',action='store_true')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--jobs',type=int,default=2)
    args=parser.parse_args();repo=args.repo.resolve();pub=repo/PUBLICATION
    need(not(args.prepare and args.metadata_only),'Choose preparation or metadata verification')
    need(1<=args.jobs<=4,'Use between one and four parallel targeted checks')
    summary=validate_ledger(repo);inventory=source_inventory(repo)
    manifest=pub/'source_manifest.json'
    required=commands(repo)
    need(required and len(set(required))==len(required),'Accepted targeted checks must be nonempty and distinct')
    need(all(p in inventory for p in required),'A targeted verifier is not source-bound')
    if args.prepare:
        pub.mkdir(parents=True,exist_ok=True);manifest.write_bytes(json_bytes(inventory))
        print(json.dumps({'status':'PREPARED_NOT_REPLAYED','targeted_scripts':len(required),
                          'source_files':len(inventory),**summary},indent=2));return
    need(json.loads(manifest.read_text())==inventory,'Research source inventory changed; prepare and replay again')
    protected={pub/'replay_normal.json',pub/'replay_optimized.json'}
    if args.metadata_only:
        digest,receipts=check_reports(repo,summary,inventory)
        result={'status':'METADATA_PASS','mathematical_replay_performed':False,
                'targeted_scripts':len(required),'source_manifest_sha256':digest,
                'full_replay_sha256':receipts,**summary}
        if args.output:
            need(args.output.resolve()not in{p.resolve()for p in protected},'Metadata cannot overwrite a replay receipt')
            args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(json_bytes(result))
        print(json.dumps(result,indent=2));return
    optimized=bool(sys.flags.optimize)
    lane='optimized'if optimized else'normal'
    default=pub/f'replay_{lane}.json';output=(args.output or default).resolve()
    need(output not in{p.resolve()for p in protected}or output==default.resolve(),'Wrong replay lane output')
    logroot=output.parent/(output.stem+'_logs');logroot.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None)
    env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    started=time.monotonic()
    def run(item):
        index,script=item;tic=time.monotonic()
        print('REPLAY',lane,index+1,script,flush=True)
        # Intentionally no -O: assertions in imported historical modules must
        # remain active even when this outer coordinator was invoked with -O.
        command=[sys.executable,str(repo/script)]
        result=subprocess.run(command,cwd=repo,env=env,capture_output=True,text=True)
        log=logroot/f'{index+1:02d}_{Path(script).stem}.log'
        log.write_text(result.stdout+result.stderr)
        need(result.returncode==0,'Targeted replay failed: '+script+'\n'+result.stdout+result.stderr)
        print('PASS',lane,index+1,script,flush=True)
        return {'script':script,'returncode':result.returncode,
                'seconds':round(time.monotonic()-tic,6),'python_optimization':0,
                'assertions_enabled':True,
                'direct_assert_statements':sum(isinstance(n,ast.Assert)for n in ast.walk(ast.parse((repo/script).read_text()))),
                'log':log.relative_to(repo).as_posix()if log.is_relative_to(repo)else str(log),
                'log_sha256':sha(log.read_bytes())}
    with ThreadPoolExecutor(max_workers=args.jobs)as pool:
        sections=list(pool.map(run,enumerate(required)))
    need(source_inventory(repo)==inventory,'Accepted sources changed during targeted replay')
    need(validate_ledger(repo)==summary,'Research ledger changed during targeted replay')
    result={'status':'PASS','mathematical_replay_performed':True,
            'optimized_python_requested':optimized,
            'all_mathematical_children_assertions_enabled':True,
            'child_policy':'All mathematical children run unoptimized, protecting direct and transitive inherited assertions.',
            'source_manifest_sha256':sha(manifest.read_bytes()),'sections':sections,
            'targeted_scripts':len(required),'seconds':round(time.monotonic()-started,6),
            'full_historical_mathematical_replay_performed':False,
            'scope':'All accepted targeted mathematical checks. Scoped necessary conditions are not models; historical evidence remains separately certified.',
            **summary}
    output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(json_bytes(result))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()

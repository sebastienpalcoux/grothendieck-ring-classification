#!/usr/bin/env python3
"""Replay the accepted R3472 proof with every mathematical assertion enabled.

Normal and optimized outer invocations have separate source-bound receipts.
The optional historical lane explicitly repairs a missing archived helper in
an isolated copy and records that repair; the published archive is unchanged.
"""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import time
from rank8_exclusion_20261022 import (ROOT, PUBLICATION, commands, historical_identity,
    json_bytes, need, safe_path, sha, source_inventory, validate_ledger)


def check_reports(repo, summary, inventory):
    repo = Path(repo)
    manifest = repo/PUBLICATION/'source_manifest.json'
    need(json.loads(manifest.read_text()) == inventory, 'Exclusion source inventory changed; prepare and replay again')
    manifest_sha = sha(manifest.read_bytes())
    required = commands(repo)
    receipts = []
    for optimized,lane in ((False,'normal'),(True,'optimized')):
        path = repo/PUBLICATION/f'replay_{lane}.json'
        report = json.loads(path.read_text())
        need(report.get('status') == 'PASS' and report.get('mathematical_replay_performed') is True,
             'Missing complete R3472 replay: '+lane)
        need(report['optimized_python_requested'] == optimized and
             report['all_mathematical_children_assertions_enabled'] is True, 'Unsafe replay lane: '+lane)
        need(report['source_manifest_sha256'] == manifest_sha and
             report['ledger_sha256'] == summary['ledger_sha256'] and
             report['accepted_sha256'] == summary['accepted_sha256'], 'Replay identity mismatch: '+lane)
        need([r['script'] for r in report['sections']] == required, 'Incomplete accepted proof replay')
        for section in report['sections']:
            need(section['returncode'] == 0 and section['python_optimization'] == 0 and
                 section['assertions_enabled'] is True, 'Unsafe mathematical child')
            need(safe_path(section['log']), 'Unsafe proof replay log')
            need(sha((repo/section['log']).read_bytes()) == section['log_sha256'], 'Changed proof replay log')
        receipts.append(sha(path.read_bytes()))
    return manifest_sha,receipts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=ROOT)
    parser.add_argument('--prepare',action='store_true')
    parser.add_argument('--metadata-only',action='store_true')
    parser.add_argument('--historical',action='store_true')
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve(); pub = repo/PUBLICATION
    need(not(args.prepare and args.metadata_only), 'Choose preparation or metadata verification')
    need(not(args.metadata_only and args.historical), 'Historical replay is not metadata-only')
    summary = validate_ledger(repo); inventory = source_inventory(repo)
    identity = historical_identity(repo)
    required = commands(repo)
    need(required and len(set(required)) == len(required) and all(p in inventory for p in required),
         'Accepted proof verifiers must be distinct and source-bound')
    manifest = pub/'source_manifest.json'
    if args.prepare:
        pub.mkdir(parents=True,exist_ok=True)
        manifest.write_bytes(json_bytes(inventory))
        print(json.dumps({'status':'PREPARED_NOT_REPLAYED','source_files':len(inventory),**summary},indent=2))
        return
    need(json.loads(manifest.read_text()) == inventory, 'Sources changed; run --prepare and replay again')
    protected = {pub/'replay_normal.json',pub/'replay_optimized.json'}
    sources = {(repo/p).resolve() for p in inventory} | {manifest.resolve()}
    if args.output:
        need(args.output.resolve() not in sources, 'Replay output cannot replace an input')
    if args.metadata_only:
        manifest_sha,receipts = check_reports(repo,summary,inventory)
        report = {'status':'METADATA_PASS','mathematical_replay_performed':False,
                  'source_manifest_sha256':manifest_sha,'full_replay_sha256':receipts,
                  'historical_archive':identity,**summary}
        if args.output:
            need(args.output.resolve() not in {p.resolve() for p in protected},
                 'Metadata verification cannot replace a mathematical receipt')
            args.output.parent.mkdir(parents=True,exist_ok=True)
            args.output.write_bytes(json_bytes(report))
        print(json.dumps(report,indent=2)); return
    optimized = bool(sys.flags.optimize); lane = 'optimized' if optimized else 'normal'
    default = pub/f'replay_{lane}.json'; output = (args.output or default).resolve()
    need(output not in {p.resolve() for p in protected} or output == default.resolve(), 'Wrong replay lane output')
    logroot = output.parent/(output.stem+'_logs'); logroot.mkdir(parents=True,exist_ok=True)
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE',None); env.pop('PYTHONPATH',None)
    env.update(PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
    started = time.monotonic(); sections = []
    for index,script in enumerate(required):
        tic = time.monotonic(); print('REPLAY',lane,script,flush=True)
        child = subprocess.run([sys.executable,str(repo/script)],cwd=repo,env=env,capture_output=True,text=True)
        log = logroot/f'{index+1:02d}_{Path(script).stem}.log'
        need(log.resolve() not in sources, 'Log would replace a source')
        log.write_text(child.stdout+child.stderr)
        need(child.returncode == 0, 'R3472 proof replay failed: '+script+'\n'+child.stdout+child.stderr)
        sections.append({'script':script,'returncode':0,'python_optimization':0,'assertions_enabled':True,
                         'seconds':round(time.monotonic()-tic,6),
                         'log':log.relative_to(repo).as_posix() if log.is_relative_to(repo) else str(log),
                         'log_sha256':sha(log.read_bytes())})
    history = None
    if args.historical:
        from current_publication import replay_rank8_exclusion_history
        history = replay_rank8_exclusion_history(repo,logroot/'historical',optimized=optimized)
    need(source_inventory(repo) == inventory and validate_ledger(repo) == summary,
         'Accepted proof sources or ledger changed during replay')
    need(json.loads(manifest.read_text()) == inventory, 'Source manifest changed during replay')
    report = {'status':'PASS','mathematical_replay_performed':True,
              'optimized_python_requested':optimized,'all_mathematical_children_assertions_enabled':True,
              'child_policy':'Every mathematical child runs without -O and with PYTHONOPTIMIZE removed.',
              'source_manifest_sha256':sha(manifest.read_bytes()),'sections':sections,
              'targeted_scripts':len(required),'seconds':round(time.monotonic()-started,6),
              'historical_archive':identity,'historical_replay':history,
              'full_historical_mathematical_replay_performed':bool(args.historical),
              'scope':'Complete accepted R3472 exclusion: general reduction, complete domains and frame coverage, exact source-derived rotation model and rational integer contradiction.',
              **summary}
    output.parent.mkdir(parents=True,exist_ok=True); output.write_bytes(json_bytes(report))
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()

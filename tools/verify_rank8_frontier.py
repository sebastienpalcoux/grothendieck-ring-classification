#!/usr/bin/env python3
"""Replay the accepted frontier proofs without modifying the earlier M3 release.

--prepare derives a new ledger and binds the current frontier sources. It does
not certify mathematics. Full replay produces separately named normal/-O
receipts. Metadata-only checks require both matching full receipts.
"""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import time
from rank8_frontier import (ROOT, LEDGER, PUBLICATION, accepted, commands, need,
                            reconcile, sha, source_inventory, validate_ledger)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT)
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--metadata-only', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    pub = repo / PUBLICATION
    manifest_path = pub / 'source_manifest.json'
    need(not (args.prepare and args.metadata_only), 'Choose preparation or metadata check')
    if args.prepare:
        rows, summary = reconcile(repo)
        target = repo / LEDGER
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(rows, separators=(',', ':')) + '\n')
        pub.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(source_inventory(repo), indent=2) + '\n')
        print(json.dumps({'status': 'PREPARED_NOT_REPLAYED', **summary}, indent=2))
        return
    summary = validate_ledger(repo)
    current = source_inventory(repo)
    need(current == json.loads(manifest_path.read_text()), 'Frontier source inventory changed; prepare and replay again')
    manifest_sha = sha(manifest_path.read_bytes())
    required = commands(repo)
    normal = pub / 'replay_normal.json'
    optimized = pub / 'replay_optimized.json'
    if args.metadata_only:
        reports = [json.loads(p.read_text()) for p in (normal, optimized)]
        for report, flag in zip(reports, (False, True)):
            need(report['status'] == 'PASS' and report['mathematical_replay_performed'] is True and report['optimized_python'] == flag,
                 'Both full replay lanes are required')
            need(report['source_manifest_sha256'] == manifest_sha and report['ledger_sha256'] == summary['ledger_sha256'],
                 'Full frontier replay belongs to different sources or ledger')
            need([r['script'] for r in report['sections']] == required and
                 all(r['returncode'] == 0 for r in report['sections']), 'Full frontier proof coverage')
            for item in report['sections']:
                need(sha((repo / item['log']).read_bytes()) == item['log_sha256'], 'Frontier replay log changed')
        result = {'status': 'METADATA_PASS', 'mathematical_replay_performed': False,
                  **summary, 'source_manifest_sha256': manifest_sha,
                  'full_replay_sha256': [sha(p.read_bytes()) for p in (normal, optimized)]}
    else:
        output = args.output or (optimized if sys.flags.optimize else normal)
        need(output.resolve() not in {normal.resolve(), optimized.resolve()} or
             output.resolve() == (optimized if sys.flags.optimize else normal).resolve(), 'Wrong replay lane output')
        logroot = output.parent / (output.stem + '_logs')
        logroot.mkdir(parents=True, exist_ok=True)
        sections = []
        started = time.monotonic()
        env = dict(os.environ)
        env.pop('PYTHONOPTIMIZE', None)
        env.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
        for i, script in enumerate(required):
            command = [sys.executable] + (['-O'] if sys.flags.optimize else []) + [str(repo / script)]
            before = time.monotonic()
            run = subprocess.run(command, cwd=repo, env=env, capture_output=True, text=True)
            log = logroot / (str(i + 1).zfill(2) + '_' + Path(script).stem + '.log')
            log.write_text(run.stdout + run.stderr)
            need(run.returncode == 0, 'Frontier proof replay failed: ' + script + '\n' + run.stdout + run.stderr)
            log_path = log.resolve()
            sections.append({'script': script, 'returncode': run.returncode,
                             'seconds': round(time.monotonic() - before, 6),
                             'log': str(log_path.relative_to(repo)) if log_path.is_relative_to(repo) else str(log_path),
                             'log_sha256': sha(log.read_bytes())})
        need(source_inventory(repo) == current, 'Frontier sources changed during replay')
        result = {'status': 'PASS', 'mathematical_replay_performed': True,
                  'optimized_python': bool(sys.flags.optimize), **summary,
                  'source_manifest_sha256': manifest_sha, 'sections': sections,
                  'seconds': round(time.monotonic() - started, 6),
                  'scope': 'New accepted exclusion computations and explicitly scoped necessary-condition and construction-family research checks. The immutable M3 baseline is replayed separately. Feasible relaxations are not models; no independent human or Lean verification is asserted.'}
    output = args.output or (None if args.metadata_only else (optimized if sys.flags.optimize else normal))
    if output:
        need(not args.metadata_only or output.resolve() not in {normal.resolve(), optimized.resolve()},
             'Metadata cannot overwrite a full replay receipt')
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

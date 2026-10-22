#!/usr/bin/env python3
"""Replay the unchanged publication verifier in its frozen proof context.

The GitHub checkout retains three later discovery files inside a recursively
inventoried historical directory. They are not inputs of the accepted release.
This launcher preserves the checkout, checks every accepted source, and moves
only those exact files outside a temporary copy before invoking the original
verifier. Unknown additions and all changes to accepted inputs remain errors.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = 'supplements/rank8/release/rank8-certified-research-20261022.zip'
ARCHIVE_SHA256 = '7c3b35b94e683db34a2247edf9e4247e1424be71c72ad8379e4d503c2267319a'
PREFIX = 'rank8-certified-research-20261022/'
STAGES = {
    'rank8_frontier_20261021': (1445, 'af80f1de878472bf6d789061c9c64c591f21eb4cbc61eaca5eead94d529a57a3'),
    'rank8_next_20261021': (1697, 'c7c8be9af58cf47fd54014b98c6f659d541ec1f0256a19267ec05747f3dc9718'),
    'rank8_research_20261022': (1785, '67f00e4b4ba0ddbd3586ea308f7cc56e04589f7851338f015a009992ac1c2b09'),
}
DISCOVERY = {
    'evidence/rank8_frontier_20261021/quadratic/final_atomic_integer.py':
        'e0a9a3fa9a13bb0423270bf2000ec412cd66da43d26e84c18ac6ba776e43c666',
    'evidence/rank8_frontier_20261021/quadratic/final_atomic_integer_65_results.json':
        '3f6eb9ae9765d4ce0508fe993a6634da7cb2ec2c75d1f1e1f2a78886ea928c42',
    'evidence/rank8_frontier_20261021/quartic_integer_center/r941_rotation.py':
        'acd0a82876809c9c45868f8e16023c095aaef2b998886787241e5a3fc8ee99ab',
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def safe_path(name):
    path = PurePosixPath(name)
    return bool(name) and not path.is_absolute() and '..' not in path.parts and path.as_posix() == name


def frozen_inputs(repo):
    """Validate the immutable archive and live accepted bytes before copying."""
    raw = (repo / ARCHIVE).read_bytes()
    need(sha(raw) == ARCHIVE_SHA256, 'The pinned scientific release changed')
    manifests = {}
    with zipfile.ZipFile(repo / ARCHIVE) as archive:
        names = archive.namelist()
        need(len(names) == len(set(names)), 'Duplicate archive members')
        need(all(n.startswith(PREFIX) and safe_path(n[len(PREFIX):]) for n in names),
             'Unsafe scientific archive path')
        checks = json.loads(archive.read(PREFIX + 'SHA256SUMS.json'))
        need(set(checks) == {n[len(PREFIX):] for n in names} - {'SHA256SUMS.json'},
             'Incomplete scientific archive checksums')
        for stage, (count, digest) in STAGES.items():
            name = f'evidence/{stage}/publication/source_manifest.json'
            published = archive.read(PREFIX + name)
            need(sha(published) == digest == checks[name], 'Frozen manifest identity: ' + stage)
            need((repo / name).read_bytes() == published, 'Live frozen manifest changed: ' + stage)
            manifest = json.loads(published)
            need(len(manifest) == count, 'Frozen manifest coverage: ' + stage)
            need(all(safe_path(p) and checks.get(p) == h for p, h in manifest.items()),
                 'Manifest differs from the pinned archive: ' + stage)
            manifests[stage] = manifest
        accepted = manifests['rank8_research_20261022']
        need(not set(DISCOVERY) & set(accepted), 'Discovery exception overlaps accepted sources')
        for name, digest in accepted.items():
            path = repo / name
            need(path.is_file() and not path.is_symlink() and sha(path.read_bytes()) == digest,
                 'Accepted source changed: ' + name)
        # Receipts and logs are unchanged released evidence, not regenerated CI outputs.
        for stage in STAGES:
            for lane in ('normal', 'optimized'):
                name = f'evidence/{stage}/publication/replay_{lane}.json'
                if PREFIX + name not in names:
                    continue  # The next stage records per-check receipts rather than aggregate lanes.
                published = archive.read(PREFIX + name)
                need((repo / name).read_bytes() == published, 'Published replay receipt changed: ' + name)
                for section in json.loads(published)['sections']:
                    log = section['log']
                    need(safe_path(log) and checks.get(log) == section['log_sha256'] and
                         sha((repo / log).read_bytes()) == section['log_sha256'],
                         'Published replay log changed: ' + log)
    discovery = {}
    for name, digest in DISCOVERY.items():
        path = repo / name
        if path.exists():
            need(path.is_file() and not path.is_symlink() and sha(path.read_bytes()) == digest,
                 'Unrecognized discovery bytes: ' + name)
            discovery[name] = digest
    return manifests, discovery


def check_context(repo, manifests, discovery):
    import rank8_frontier
    import rank8_next
    import rank8_research_20261022
    from verify_rank8_research_20261022 import check_reports
    modules = (rank8_frontier, rank8_next, rank8_research_20261022)
    summaries = {}
    for module in modules:
        stage = module.EVIDENCE.split('/')[-1]
        expected = {**manifests[stage], **discovery}
        actual = module.source_inventory(repo)
        need(actual == expected, 'Unexpected proof inventory additions, omissions or changes: ' + stage)
        summaries[stage] = module.validate_ledger(repo)
    check_reports(repo, summaries['rank8_research_20261022'], manifests['rank8_research_20261022'])
    return summaries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT)
    parser.add_argument('--metadata-only', action='store_true')
    parser.add_argument('--historical', action='store_true')
    parser.add_argument('--plan', action='store_true', help='Validate the isolated context and print dispatch without running proofs')
    args = parser.parse_args()
    need(not (args.metadata_only and args.historical), 'Choose metadata-only or full historical replay')
    repo = args.repo.resolve()
    # The E21 continuation has its own current router/source manifest. Its
    # verifier replays the entire older rank-eight chain from the pinned
    # scientific archive, preserving the three unbound discovery files and
    # the older router bytes without applying historical checks to new code.
    from rank8_creative_20261022 import active as creative_active, validate_ledger as validate_creative
    if creative_active(repo):
        from rank8_creative_history import baseline
        identity = baseline(repo)
        validate_creative(repo)
        command = [sys.executable] + (['-O'] if sys.flags.optimize else [])
        command += [str(repo / 'tools/verify_current_publication.py'), '--repo', str(repo)]
        if args.metadata_only:
            command.append('--metadata-only')
        if args.historical:
            command.append('--historical')
        print(json.dumps({'status':'CURRENT_CREATIVE_CONTEXT', 'historical_archive':identity,
                          'command':command, 'plan_only':args.plan},indent=2),flush=True)
        if not args.plan:
            env = dict(os.environ)
            env.pop('PYTHONOPTIMIZE',None)
            env.pop('PYTHONPATH',None)
            env['PYTHONDONTWRITEBYTECODE'] = '1'
            result = subprocess.run(command,cwd=repo,env=env)
            need(result.returncode == 0,'Current E21 publication verification failed')
            need(baseline(repo) == identity,'Historical inputs changed during current replay')
        return
    manifests, discovery = frozen_inputs(repo)
    initial = check_context(repo, manifests, discovery)
    with tempfile.TemporaryDirectory(prefix='grc-frozen-ci-') as directory:
        target = Path(directory) / 'repo'
        shutil.copytree(repo, target, copy_function=shutil.copy2,
                        ignore=shutil.ignore_patterns('.git', 'node_modules', '__pycache__', 'work'))
        for name, digest in discovery.items():
            source = target / name
            retained = Path(directory) / 'unbound_discovery' / name
            retained.parent.mkdir(parents=True, exist_ok=True)
            source.replace(retained)
            need(sha(retained.read_bytes()) == digest, 'Temporary discovery bytes changed')
        need(check_context(target, manifests, {}) == initial, 'Projection changed accepted ledger/model bindings')
        command = [sys.executable] + (['-O'] if sys.flags.optimize else [])
        command += [str(target / 'tools/verify_current_publication.py'), '--repo', str(target)]
        if args.metadata_only:
            command.append('--metadata-only')
        if args.historical:
            command.append('--historical')
        print(json.dumps({'status': 'ISOLATED_CONTEXT_PASS', 'scientific_archive_sha256': ARCHIVE_SHA256,
                          'frozen_source_counts': {stage: len(value) for stage, value in manifests.items()},
                          'discovery_files_retained_outside_proof_context': discovery,
                          'original_checkout_modified': False, 'command': command,
                          'mathematical_replay_performed': False, 'plan_only': args.plan}, indent=2), flush=True)
        if not args.plan:
            env = dict(os.environ)
            env.pop('PYTHONOPTIMIZE', None)
            env.pop('PYTHONPATH', None)
            env['PYTHONDONTWRITEBYTECODE'] = '1'
            result = subprocess.run(command, cwd=target, env=env)
            need(result.returncode == 0, 'The unchanged publication verifier failed in the isolated context')
            need(check_context(target, manifests, {}) == initial, 'Replay changed accepted inputs')
        need(frozen_inputs(repo) == (manifests, discovery), 'Original published inputs changed during replay')
    print('PASS: frozen proof context; original published sources and receipts preserved.', flush=True)


if __name__ == '__main__':
    main()

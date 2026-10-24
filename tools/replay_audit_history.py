#!/usr/bin/env python3
"""Replay historical proofs in the exact pre-audit Git snapshot.

The historical R436 scalar calculation does not establish its withdrawn
general categorical premise. This command never changes the current checkout.
The nested historical dispatchers require substantial temporary disk space.
"""
from pathlib import Path, PurePosixPath
import argparse
import json
import shutil
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PREDECESSOR = '111137a3e3ddf93be340b39c8a7c7b6ea94b844c'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def replay(repo=ROOT, plan_only=False):
    repo = Path(repo).resolve()
    identity = subprocess.run(
        ['git', 'rev-parse', '--verify', PREDECESSOR + '^{commit}'],
        cwd=repo, capture_output=True, text=True)
    need(identity.returncode == 0 and identity.stdout.strip() == PREDECESSOR,
         'The pinned historical commit is absent. In a Git checkout, first run: '
         'git fetch --no-tags origin ' + PREDECESSOR)
    tree = subprocess.check_output(
        ['git', 'rev-parse', PREDECESSOR + '^{tree}'], cwd=repo, text=True).strip()
    python = [sys.executable] + (['-O'] if sys.flags.optimize else [])
    command = python + ['tools/replay_current_publication_ci.py', '--historical']
    report = {
        'historical_commit': PREDECESSOR,
        'historical_tree': tree,
        'current_checkout_modified': False,
        'restore_command': [sys.executable, 'tools/restore_data.py'],
        'historical_command': command,
        'plan_only': plan_only,
        'scope': ('Historical computational replay only. A passing R436 scalar '
                  'calculation does not restore the withdrawn general premise.'),
    }
    print(json.dumps(report, indent=2), flush=True)
    if plan_only:
        return report
    # Check current identities separately; the old program runs exclusively on
    # old bytes, without audit overlays or rewritten historical hash manifests.
    subprocess.run(python + ['tools/verify_audit_revision.py', '--metadata-only'],
                   cwd=repo, check=True)
    with tempfile.TemporaryDirectory(prefix='grc-pre-audit-history-') as folder:
        target = Path(folder) / 'repo'
        target.mkdir()
        process = subprocess.Popen(
            ['git', 'archive', '--format=tar', PREDECESSOR],
            cwd=repo, stdout=subprocess.PIPE)
        try:
            with tarfile.open(fileobj=process.stdout, mode='r|') as archive:
                for member in archive:
                    name = PurePosixPath(member.name)
                    need(not name.is_absolute() and '..' not in name.parts,
                         'Unsafe historical archive member: ' + member.name)
                    path = target.joinpath(*name.parts)
                    if member.isdir():
                        path.mkdir(parents=True, exist_ok=True)
                    else:
                        need(member.isfile(), 'Nonregular historical archive member')
                        path.parent.mkdir(parents=True, exist_ok=True)
                        with archive.extractfile(member) as source, path.open('wb') as output:
                            shutil.copyfileobj(source, output)
                        path.chmod(member.mode & 0o777)
            need(process.wait() == 0, 'Cannot export the pinned historical snapshot')
        finally:
            if process.poll() is None:
                process.terminate()
                process.wait()
        subprocess.run(report['restore_command'], cwd=target, check=True)
        subprocess.run(command, cwd=target, check=True)
    report['status'] = 'HISTORICAL_COMPUTATIONS_PASS'
    print(json.dumps(report, indent=2), flush=True)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT)
    parser.add_argument('--plan', action='store_true')
    args = parser.parse_args()
    replay(args.repo, args.plan)

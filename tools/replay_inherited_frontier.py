#!/usr/bin/env python3
"""Run the frozen fourteen checks with a current, status-independent tensor lookup."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
ACCEPTED = 'evidence/frontier_20261027/accepted.json'
ACCEPTED_SHA256 = 'a9ef88bf0f02920925b400b999cd69bf36984f302fab9b1d4b74c44c4f20c4d1'
RUNNER = 'tools/replay_frontier_20261027.py'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def current_lookup():
    records = {}
    lookup_rows = {}
    payloads = {}
    for name in ('unresolved_cases.json', 'resolved_cases.json', 'rank9_m2.json'):
        payload = json.loads((ROOT/'site/dist/data'/name).read_text())
        payloads[name] = payload
        for row in payload['cases']:
            rid = row['id']
            tensor_hash = hashlib.sha256(json.dumps(
                row['fusion_tensor'], separators=(',', ':')).encode()).hexdigest()
            require(tensor_hash == row['tensor_sha256'], 'Current tensor digest: ' + rid)
            if rid in records:
                require(records[rid]['fusion_tensor'] == row['fusion_tensor'] and
                        records[rid]['status'] == row['status'],
                        'Inconsistent current duplicate: ' + rid)
            records[rid] = row
            if name != 'rank9_m2.json':
                lookup_rows[rid] = row
    # The historical runner searches only its unresolved and rank-nine indexes.
    # R1768 has since moved to resolved; this temporary lookup retains its status.
    lookup = dict(payloads['unresolved_cases.json'])
    lookup['cases'] = list(lookup_rows.values())
    return lookup


def main(output=None):
    require(digest(ROOT/ACCEPTED) == ACCEPTED_SHA256, 'Frozen acceptance identity')
    accepted = json.loads((ROOT/ACCEPTED).read_text())
    sources = (RUNNER, 'tools/frontier_20261027.py')
    for name in sources:
        require(digest(ROOT/name) == accepted['source_sha256'][name],
                'Frozen runner source: ' + name)
    archive = accepted['replay_archive']
    require(digest(ROOT/archive['path']) == archive['sha256'], 'Frozen archive identity')
    lookup = current_lookup()
    with tempfile.TemporaryDirectory(prefix='inherited-frontier-inputs-') as directory:
        staged = Path(directory)
        for name in (*sources, ACCEPTED, archive['path'], 'site/dist/data/rank9_m2.json'):
            target = staged/name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT/name, target)
        index = staged/'site/dist/data/unresolved_cases.json'
        index.write_text(json.dumps(lookup, ensure_ascii=False, separators=(',', ':')) + '\n')
        command = [sys.executable, str(staged/RUNNER)]
        if output:
            command += ['--output', str(Path(output).resolve())]
        env = dict(os.environ)
        env.pop('PYTHONOPTIMIZE', None)
        # Execute the original source unchanged, including its archive checks,
        # ten exact tensor comparisons and all fourteen mathematical replays.
        subprocess.run(command, cwd=staged, env=env, check=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    main(parser.parse_args().output)

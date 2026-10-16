#!/usr/bin/env python3
"""Validate the packaged rank-five proof inputs and replay all 40,999 decisions."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rank5_status(document):
    source = document['inputs']['rank5']
    records = []
    for row in document['rows']:
        if row['rank'] == 5 and row['multiplicity'] <= 20:
            records.append((row['multiplicity'], row['rings'], row['excluded_general'],
                            row['realized_unitary'] + row['realized_other_or_unspecified'],
                            row['unresolved_general'], row['unassessed']))
    return {'historical_ledger_sha256': source['sha256'],
            'classified_through': source['classified_through'],
            'status_totals': source['status_totals'], 'rows': sorted(records)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=2)
    parser.add_argument('--output-dir', type=Path, default=Path.cwd() / 'rank5-replay-output')
    parser.add_argument('--classification-status', type=Path,
                        help='override the repository classification-status file')
    parser.add_argument('--check-package', action='store_true',
                        help='check every packaged byte and the published status binding, without repeating the full proof replay')
    args = parser.parse_args()
    require(1 <= args.jobs <= 16, 'jobs must lie in 1..16')
    status_file = args.classification_status or ROOT.parents[2] / 'data/classification_status.json'
    manifest = json.loads((ROOT / 'package.json').read_text())
    require(manifest['entrypoint'] in manifest['members'] and manifest['classification_status'] in manifest['members'],
            'package entry point or publication snapshot missing')
    archive = ROOT / manifest['archive']
    raw = archive.read_bytes()
    require(len(raw) == manifest['bytes'], 'package size mismatch')
    require(hashlib.sha256(raw).hexdigest() == manifest['sha256'], 'package SHA-256 mismatch')
    mode = 'optimized' if sys.flags.optimize else 'normal'
    with tempfile.TemporaryDirectory(prefix='rank5-current-') as temporary:
        directory = Path(temporary)
        with zipfile.ZipFile(archive) as source:
            names = source.namelist()
            require(len(names) == len(set(names)) and set(names) == set(manifest['members']),
                    'package member coverage mismatch')
            for name in names:
                parts = PurePosixPath(name)
                require(not parts.is_absolute() and '..' not in parts.parts, 'unsafe package member')
                data = source.read(name)
                expected = manifest['members'][name]
                require(len(data) == expected['bytes'], 'member size mismatch: ' + name)
                require(hashlib.sha256(data).hexdigest() == expected['sha256'], 'member hash mismatch: ' + name)
                target = directory.joinpath(*parts.parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
        packaged_status = directory / manifest['classification_status']
        live_status_bytes = status_file.read_bytes()
        live_status = json.loads(live_status_bytes)
        require(rank5_status(json.loads(packaged_status.read_text())) == rank5_status(live_status),
                'live rank-five publication differs from the replayed decisions')
        print(f'PASS package SHA-256 and all {len(names)} extracted member hashes; published rank-five scope matches.', flush=True)
        if args.check_package:
            return
        # The core checks the actual current status file, after this launcher
        # has established its rank-five agreement with the archived snapshot.
        packaged_status.write_bytes(live_status_bytes)
        destination = args.output_dir.resolve()
        destination.mkdir(parents=True, exist_ok=True)
        command = [sys.executable] + (['-O'] if sys.flags.optimize else [])
        command += [str(directory / manifest['entrypoint']), '--jobs', str(args.jobs),
                    '--output', str(destination / f'current_{mode}.json'),
                    '--ledger-output', str(destination / f'current_decisions_{mode}.json')]
        subprocess.run(command, check=True)
        print('Fresh replay artifacts: ' + str(destination), flush=True)


if __name__ == '__main__':
    main()

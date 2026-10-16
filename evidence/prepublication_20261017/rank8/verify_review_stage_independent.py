#!/usr/bin/env python3
"""Bounded independent checks of the current R24 review stage; no historical replay.

Uses the unmodified review checker, then injects in-memory bad JSON values to
confirm decision-critical checks reject them. No source/evidence files change.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    verifier = repo / 'tools/verify_review_20261017.py'
    spec = importlib.util.spec_from_file_location('review_under_independent_check', verifier)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    reports = {}
    for name, flags in [('normal', []), ('optimized', ['-O'])]:
        result = subprocess.run([sys.executable, *flags, str(verifier), '--repo', str(repo), '--metadata-only'],
                                text=True, capture_output=True)
        require(result.returncode == 0, name + ' metadata check failed: ' + result.stderr)
        reports[name] = json.loads(result.stdout)
    require(reports['normal'] == reports['optimized'], 'Normal and optimized reports differ')
    require(reports['normal']['restored_parent_files'] == 26, 'Parent restoration inventory')
    source_read = module.read
    ledger = repo / 'supplements/rank8/data/decisions.json'
    accepted = repo / 'evidence/review_20261017/decisions.json'
    unified = source_read(repo / 'evidence/unified_20261016/decisions.json')
    negative = []

    def rejects(label, target, change, expected_message):
        def altered_read(path):
            result = source_read(path)
            if Path(path).resolve() == target.resolve():
                result = copy.deepcopy(result)
                change(result)
            return result
        module.read = altered_read
        try:
            module.verify_current(repo)
        except ValueError as error:
            require(str(error) == expected_message, label + ': unexpected rejection: ' + str(error))
            negative.append({'case': label, 'status': 'REJECTED', 'reason': str(error)})
        else:
            raise RuntimeError(label + ': invalid state was accepted')
        finally:
            module.read = source_read

    def reinstate(rows):
        next(r for r in rows if r['id'] == 'R8_2_24')['status'] = 'excluded'

    def alter_other(rows):
        next(r for r in rows if r['id'] != 'R8_2_24')['tensor_sha256'] = '0' * 64

    def reaccept(rows):
        rows.append(next(r for r in unified if r['id'] == 'R8_2_24'))

    rejects('reinstate withdrawn current exclusion', ledger, reinstate, 'Exact reopened current record')
    rejects('change another rank8 tensor identity', ledger, alter_other, 'Current complete ledger hash')
    rejects('reinsert withdrawn accepted continuation', accepted, reaccept,
            '35 accepted decisions are the unchanged historical decisions except R8_2_24')
    for label, destination in [('restore over source', repo), ('restore inside source', repo / 'audit-forbidden')]:
        try:
            module.restore_parent_files(repo, destination)
        except ValueError as error:
            require(str(error) == 'Historical restoration requires a separate directory outside the source',
                    label + ': unexpected rejection')
            negative.append({'case': label, 'status': 'REJECTED', 'reason': str(error)})
        else:
            raise RuntimeError(label + ': unsafe restoration was accepted')
    invalid = subprocess.run([sys.executable, str(verifier), '--repo', str(repo), '--metadata-only', '--historical'],
                             text=True, capture_output=True)
    require(invalid.returncode != 0 and 'Choose historical replay or metadata-only' in invalid.stderr,
            'Conflicting replay modes were not rejected')
    negative.append({'case': 'combine metadata-only and historical', 'status': 'REJECTED',
                     'reason': 'Choose historical replay or metadata-only'})
    report = {
        'status': 'PASS',
        'scope': 'Metadata, byte-bound parent restoration, and negative controls; no historical replay or mathematical proof certification.',
        'python_optimized': not __debug__,
        'checked_files_sha256': {str(path.relative_to(repo)): digest(path) for path in
            [verifier, repo / 'evidence/review_20261017/source_files.json',
             repo / 'evidence/review_20261017/parent_files.json',
             repo / 'evidence/review_20261017/review.json',
             repo / 'evidence/review_20261017/all_cases.json']},
        'metadata_reports': reports,
        'negative_controls': negative,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'negative_controls': len(negative),
                      'output': str(args.output), 'python_optimized': not __debug__}, indent=2))


if __name__ == '__main__':
    main()

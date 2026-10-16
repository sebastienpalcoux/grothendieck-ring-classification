#!/usr/bin/env python3
"""Invoke the unmodified frozen full rank-eight checker in an isolated copy.

The production verify.py entrypoint can dispatch to a later stage before its
973-record main loop. This driver imports the b-stage frozen original checker
under a non-__main__ name, then explicitly invokes its original main(). No
assertion or criterion is removed. Instrumentation delegates to the original
tensor/certificate functions and records only successfully returned checks.
Normal Python is mandatory because this historical checker uses assertions.
"""
from pathlib import Path
import argparse
import collections
import hashlib
import importlib.util
import json
import os
import sys
import time


def need(value, message):
    if not value:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Tee:
    def __init__(self, *targets):
        self.targets = targets

    def write(self, value):
        for target in self.targets:
            target.write(value)
            target.flush()
        return len(value)

    def flush(self):
        for target in self.targets:
            target.flush()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--original-repo', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root, original = args.repo.resolve(), args.original_repo.resolve()
    output = args.output.resolve()
    need(root != original, 'Run only on an isolated historical copy')
    need(not (original in root.parents), 'Historical copy must be outside the source repository')
    need(sys.flags.optimize == 0 and __debug__, 'Normal Python with assertions is mandatory')
    need(os.environ.get('PYTHONOPTIMIZE', '') in ('', '0'), 'Child assertion checks must remain enabled')
    output.mkdir(parents=True, exist_ok=True)
    source = root / 'supplements/rank8/software/verify.py'
    frozen = original / 'evidence/upper_residual_20261002b/baseline_files/supplements/rank8/software/verify.py'
    need(source.read_bytes() == frozen.read_bytes(), 'Checker must be byte-identical to the frozen full original')
    ledger_path = root / 'supplements/rank8/data/decisions.json'
    ledger = json.loads(ledger_path.read_text())
    need(len(ledger) == len({x['id'] for x in ledger}) == 973, 'Full 973-record baseline required')
    expected = {'excluded': 832, 'unitarily_realized': 60, 'unresolved': 81}
    need(dict(collections.Counter(x['status'] for x in ledger)) == expected, 'Unexpected historical stage')
    by_hash = {x['tensor_sha256']: x for x in ledger}
    need(len(by_hash) == 973, 'Distinct labelled source tensors required')
    sys.path.insert(0, str(source.parent))
    spec = importlib.util.spec_from_file_location('rank8_full_baseline', source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    need(module.ROOT.resolve() == root / 'supplements/rank8', 'Checker escaped isolated historical copy')
    checked_tensors = []
    checked_certificates = []
    original_tensor_check = module.assert_fusion_tensor
    original_certificate_check = module.verify_certificate

    def recorded_tensor_check(tensor):
        result = original_tensor_check(tensor)
        checked_tensors.append(by_hash[module.fp(tensor)]['id'])
        return result

    def recorded_certificate_check(tensor, certificate, *registries):
        result = original_certificate_check(tensor, certificate, *registries)
        checked_certificates.append((by_hash[module.fp(tensor)]['id'], certificate['kind']))
        return result

    module.assert_fusion_tensor = recorded_tensor_check
    module.verify_certificate = recorded_certificate_check
    started = time.monotonic()
    with (output / 'rank8_full_baseline.log').open('w') as log:
        stdout = sys.stdout
        sys.stdout = Tee(stdout, log)
        try:
            print('FULL BASELINE START: original main(), normal Python, all assertions active', flush=True)
            module.main()
        finally:
            sys.stdout = stdout
    need(checked_tensors == [x['id'] for x in ledger], 'Every tensor must be checked once in ledger order')
    expected_excluded = [(x['id'], x['certificate']['kind']) for x in ledger if x['status'] == 'excluded']
    need(checked_certificates == expected_excluded, 'Every baseline negative criterion must return successfully')
    final_report_path = module.ROOT / 'verification/report.json'
    final_report = json.loads(final_report_path.read_text())
    need(final_report.get('fully_checked') is True and final_report['census_size'] == 973, 'Original checker did not complete')
    receipt = {
        'status': 'PASS',
        'python': sys.version,
        'python_optimized': False,
        'assertions_enabled_in_parent_and_children': True,
        'historical_stage': 'pre-upper_residual_20261002b; after residual_20261002',
        'checker': str(source),
        'checker_sha256': sha(source),
        'frozen_source_checker_sha256': sha(frozen),
        'baseline_ledger_sha256': sha(ledger_path),
        'driver_sha256': sha(Path(__file__).resolve()),
        'invocation': 'Import frozen original under a non-main name, explicitly call original main()',
        'checks_disabled_or_removed': [],
        'tensor_checks_completed': len(checked_tensors),
        'negative_certificate_checks_completed': len(checked_certificates),
        'baseline_totals': expected,
        'original_checker_report': final_report,
        'elapsed_seconds': round(time.monotonic() - started, 3),
        'records': [{
            'id': row['id'],
            'status': row['status'],
            'tensor_sha256': row['tensor_sha256'],
            'certificate_kind': row.get('certificate', {}).get('kind'),
        } for row in ledger],
        'scope': 'Fresh full finite replay of all 973 historical source records. Later changed records require their separate stage replays. This is not independent proof of cited categorical theorems or census exhaustiveness.',
    }
    destination = output / 'rank8_full_baseline_receipt.json'
    destination.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: receipt[k] for k in ('status', 'python_optimized', 'tensor_checks_completed', 'negative_certificate_checks_completed', 'baseline_totals', 'elapsed_seconds')}, indent=2))
    print('Receipt:', destination)


if __name__ == '__main__':
    main()

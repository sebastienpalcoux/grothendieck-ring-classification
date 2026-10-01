#!/usr/bin/env python3
"""Require rejection of a zeroed Farkas ray, normally and with python -O."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', required=True)
    parser.add_argument('--report', type=Path, default=P/'audit/mutated_ray.json')
    args = parser.parse_args()
    original = json.loads((P/'certificate.json').read_text())
    first = original['branches'][0]['cases'][0]
    first['y'] = [0]*len(first['y'])
    receipts = []
    with tempfile.TemporaryDirectory(prefix='r6_9_1060_bad_ray_') as folder:
        corrupted = Path(folder)/'corrupted_certificate.json'
        corrupted.write_text(json.dumps(original))
        for optimize in (False, True):
            command = [sys.executable] + (['-O'] if optimize else []) + [
                str(P/'verify.py'), '--source-root', args.source_root,
                '--certificate', str(corrupted)]
            start = time.monotonic()
            result = subprocess.run(command, capture_output=True, text=True, timeout=240)
            require(result.returncode == 2, 'mutated certificate was not rejected')
            require('higher-indicator Farkas certificate fails' in result.stderr,
                    'mutation did not reach the exact Farkas gate')
            receipts.append({'python_optimization_level': int(optimize),
                             'returncode': result.returncode,
                             'stderr': result.stderr.strip(),
                             'seconds': time.monotonic()-start})
            print('REJECTED corrupted ray, optimize='+str(int(optimize)), flush=True)
    report = {'status': 'passed', 'mutation': 'replace the first full Farkas ray by zeros',
              'reason_expected': 'y^T b is not negative', 'receipts': receipts}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2)+'\n')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

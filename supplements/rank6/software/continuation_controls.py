"""Replay every newly accepted proof without an optimizer.

This is an incremental release check. It does not claim to repeat the
unchanged original campaign's 16,511 accepted negative certificates.
"""
import os
for variable in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[variable] = '1'
import argparse
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
from pathlib import Path
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'software'))


def worker(task):
    row, record = task
    start = time.monotonic()
    try:
        import scipy.optimize
        def forbidden(*args, **kwargs):
            raise RuntimeError('optimizer forbidden during certificate replay')
        scipy.optimize.linprog = scipy.optimize.milp = forbidden
        from check import verify
        verify(row['N'], record['certificate'])
        return dict(id=row['id'], kind=record['certificate']['kind'],
                    passed=True, seconds=time.monotonic()-start)
    except Exception as error:
        return dict(id=row['id'], passed=False, error=str(error),
                    traceback=traceback.format_exc(), seconds=time.monotonic()-start)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=3)
    parser.add_argument('--out', default=None)
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error('--jobs must be positive')
    from exact import require
    from existence import verify_ledger
    from import_repository import verify_source
    rows = json.loads((ROOT/'data/census.json').read_text())
    source = verify_source(rows)
    ledger = json.loads((ROOT/'data/decisions.json').read_text())
    verify_ledger(ledger)
    by_id = {row['id']: row for row in rows}
    decisions = {row['id']: row for row in ledger}
    from release import CONTINUATION_PATHS
    paths = [p for p in CONTINUATION_PATHS if p.exists()]
    records = [json.loads(line) for path in paths for line in path.read_text().splitlines()]
    require(len({record['id'] for record in records}) == len(records),
            'duplicate continuation records')
    for record in records:
        decision = decisions[record['id']]
        require(decision['status'] == 'excluded' and
                decision['certificate'] == record['certificate'],
                'continuation does not match the current ledger')
    start = time.monotonic()
    results = []
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        tasks = [(by_id[record['id']], record) for record in records]
        for result in executor.map(worker, tasks):
            results.append(result)
            print(json.dumps(result), flush=True)
    report = dict(passed=all(result['passed'] for result in results),
                  optimized_python=not __debug__, source=source,
                  count=len(results), results=results,
                  seconds=time.monotonic()-start,
                  ledger_sha256=hashlib.sha256((ROOT/'data/decisions.json').read_bytes()).hexdigest(),
                  certificates_sha256={str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},
                  scope='Every continuation certificate; original unchanged campaign is not replayed.')
    out = ROOT/(args.out or ('verification/continuation/replay_optimized.json'
                            if not __debug__ else 'verification/continuation/replay_normal.json'))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2)+'\n')
    require(report['passed'], 'continuation replay failed')
    print('ALL CONTINUATION CERTIFICATES VERIFIED', flush=True)


if __name__ == '__main__':
    main()

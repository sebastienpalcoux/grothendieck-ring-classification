"""Run current source, certificate, model and presentation consistency controls.

No test generates a new census. Each subprocess result and its complete log
are recorded, including timeouts and unexpected failures. These regression
controls supplement, and do not replace, verify.py's complete certificate check.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
SUITES = (
    'automation_controls',
    'watchdog_controls',
    'certificate_controls',
    'module_rotation_controls',
    'model_controls',
    'literature_controls',
    'morita_controls',
    'character_controls',
    'categorical_scope_controls',
    'component_controls',
    'signed_trace_controls',
    'reconstruction_controls',
    'release_consistency',
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--suites', nargs='+', choices=SUITES, default=list(SUITES))
    parser.add_argument('--mode', choices=('both', 'normal', 'optimized'), default='both')
    parser.add_argument('--timeout', type=int, default=900,
                        help='maximum seconds for each independent control process')
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    if len(set(args.suites)) != len(args.suites):
        parser.error('duplicate suites are not allowed')
    destination = ROOT / 'verification/current'
    destination.mkdir(parents=True, exist_ok=True)
    environment = dict(os.environ)
    # Exact Farkas vectors are row-indexed; pin the SymPy backend used when
    # the archived systems were generated, even if python-flint is installed.
    environment['SYMPY_GROUND_TYPES'] = 'python'
    for variable in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
        environment[variable] = '1'
    modes = ('normal', 'optimized') if args.mode == 'both' else (args.mode,)
    results = []
    started = time.monotonic()
    for suite in args.suites:
        for mode in modes:
            command = [sys.executable, *(['-O'] if mode == 'optimized' else []),
                       f'software/{suite}.py']
            log_path = destination / f'{suite}_{mode}.log'
            start = time.monotonic()
            timed_out = False
            error = None
            code = None
            with log_path.open('w') as log:
                try:
                    result = subprocess.run(command, cwd=ROOT, env=environment,
                                            stdout=log, stderr=subprocess.STDOUT,
                                            timeout=args.timeout)
                    code = result.returncode
                except subprocess.TimeoutExpired:
                    timed_out = True
                    error = f'control exceeded its {args.timeout}-second process limit'
                except OSError as exc:
                    error = str(exc)
            record = dict(suite=suite, mode=mode, command=command,
                          returncode=code, timed_out=timed_out, error=error,
                          passed=code == 0 and not timed_out,
                          seconds=time.monotonic()-start,
                          log=str(log_path.relative_to(ROOT)))
            results.append(record)
            complete = len(results) == len(args.suites) * len(modes)
            summary = dict(complete=complete,
                           passed=complete and all(r['passed'] for r in results),
                           seconds=time.monotonic()-started,
                           census_recomputed=False,
                           requested_suites=args.suites, requested_modes=list(modes),
                           all_suites_in_both_modes=set(args.suites)==set(SUITES) and args.mode=='both',
                           results=results)
            (destination/'regression_process_results.json').write_text(
                json.dumps(summary, indent=2)+'\n')
            print(json.dumps(record), flush=True)
    return int(any(not record['passed'] for record in results))


if __name__ == '__main__':
    raise SystemExit(main())

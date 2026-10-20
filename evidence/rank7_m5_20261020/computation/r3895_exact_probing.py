"""Exact failed-branch probing; incomplete chains are never exclusions.

Numerical LP solutions choose candidate integer splits. Each discarded side
must have an exact integer Farkas certificate. The remaining bounds are
therefore necessary for every integer solution of the original system.
"""
import os
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[key] = '1'
import argparse
import hashlib
import json
import math
from pathlib import Path
import signal
import time
import numpy as np
from scipy.optimize import linprog
from r3895_c8_tree import build
from exact_branch_bound import bound_system, exact_ray, check_farkas

HERE = Path(__file__).resolve().parent


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def child(bounds, j, k, side):
    lo, hi = bounds.get(j, (0, None))
    if not (lo <= k and (hi is None or k < hi)):
        raise ValueError('split is not a complete nontrivial integer partition')
    result = dict(bounds)
    result[j] = (lo, k) if side == 0 else (k + 1, hi)
    return result


def replay_steps(A, b, steps):
    bounds = {}
    for step in steps:
        j, k, bad = (step[key] for key in ('variable', 'floor', 'discarded_side'))
        if type(j) is not int or not 0 <= j < len(A[0]) or type(k) is not int or bad not in (0, 1):
            raise ValueError('invalid exact probing step')
        matrix, target = bound_system(A, b, child(bounds, j, k, bad))
        check_farkas(matrix, target, step['y'])
        bounds = child(bounds, j, k, 1 - bad)
    return bounds


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', type=int, default=0)
    parser.add_argument('--branch', type=int, default=0)
    parser.add_argument('--r', type=int, default=5)
    parser.add_argument('--s', type=int, default=1)
    parser.add_argument('--seconds', type=int, default=300)
    parser.add_argument('--proposals', type=Path)
    parser.add_argument('--replay', action='store_true')
    args = parser.parse_args()
    A, b, kept, phase_count, bindings, capacities = build(args.case, args.branch, args.r, args.s)
    matrix_digest = digest([A, b])
    path = HERE / f'R7_5_3895_c8_case{args.case}_phi{args.branch}_r{args.r}_s{args.s}_exact_probing.json'
    record = {'id': 'R7_5_3895', 'case': args.case, 'branch': args.branch,
              'r': args.r, 's': args.s, 'source_hashes': bindings,
              'matrix_sha256': matrix_digest, 'capacities': capacities,
              'status': 'partial_necessary_bounds', 'steps': [],
              'scope': 'Conditional exact probing only; a partial chain is not an exclusion.'}
    if path.exists():
        record = json.loads(path.read_text())
        if record['source_hashes'] != bindings or record['matrix_sha256'] != matrix_digest or record['capacities'] != capacities:
            raise ValueError('changed probing inputs')
    steps = record['steps']
    bounds = replay_steps(A, b, steps)
    if record.get('terminal_y') is not None:
        matrix, target = bound_system(A, b, bounds)
        check_farkas(matrix, target, record['terminal_y'])
        if record['status'] != 'complete_conditional_exclusion':
            raise ValueError('terminal status')
    if args.replay or record.get('terminal_y') is not None:
        print(json.dumps({'status': 'PASS', 'chain_status': record['status'],
                          'steps': len(steps), 'optimized_python': not __debug__}), flush=True)
        return
    started = time.monotonic()
    aa = np.array(A, dtype=float)
    bb = np.array(b, dtype=float)
    scale = np.maximum(1, np.maximum(np.max(abs(aa), axis=1), abs(bb)))
    aa /= scale[:, None]
    bb /= scale
    objective = np.array([1 if j < len(kept) and kept[j] < phase_count else 0 for j in range(len(A[0]))], dtype=float)
    pending = []
    if args.proposals:
        source = json.loads(args.proposals.read_text())
        if any(source[key] != getattr(args, key) for key in ('case', 'branch', 'r', 's')):
            raise ValueError('proposal branch mismatch')
        pending = [(row['variable'], row['floor'], side) for row in source['results'] for side, status in enumerate(row['statuses']) if status == 2]
    tried = set()

    def checkpoint():
        record['seconds_last_run'] = time.monotonic() - started
        record['forced_bounds'] = {str(k): v for k, v in sorted(bounds.items())}
        temporary = path.with_suffix('.tmp')
        temporary.write_text(json.dumps(record, separators=(',', ':')) + '\n')
        temporary.replace(path)

    def timed_ray(trial):
        matrix, target = bound_system(A, b, trial)
        def timeout(signum, frame):
            raise TimeoutError('bounded exact-ray recovery')
        previous = signal.signal(signal.SIGALRM, timeout)
        signal.alarm(40)
        try:
            from r3895_sparse_terminal import reduce_bounds, lift_ray
            reduced, rhs, metadata = reduce_bounds(A, b, trial)
            candidate = exact_ray(reduced, rhs)
            if candidate is not None:
                ray = lift_ray(A, b, trial, candidate, metadata)
                check_farkas(matrix, target, ray)
                if sum(x*y for x,y in zip(rhs,candidate)) != sum(x*y for x,y in zip(target,ray)):
                    raise ValueError('reduced Farkas target changed during lifting')
                return ray
            return exact_ray(matrix, target)
        except TimeoutError:
            return None
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, previous)

    round_number = 0
    while time.monotonic() - started < args.seconds:
        for j, k, side in pending:
            if time.monotonic() - started >= args.seconds:
                break
            lo, hi = bounds.get(j, (0, None))
            if not (lo <= k and (hi is None or k < hi)):
                continue
            key = (len(steps), j, k, side)
            if key in tried:
                continue
            tried.add(key)
            ray = timed_ray(child(bounds, j, k, side))
            if ray is None:
                continue
            steps.append({'variable': j, 'original': kept[j] if j < len(kept) else None,
                          'floor': k, 'discarded_side': side, 'y': ray})
            bounds = child(bounds, j, k, 1 - side)
            checkpoint()
            print(json.dumps({'event': 'exact_forced_bound', 'steps': len(steps),
                              'variable': j, 'bound': bounds[j], 'seconds': time.monotonic() - started}), flush=True)
        pending = []
        options = [bounds.get(j, (0, None)) for j in range(len(A[0]))]
        lp = linprog(objective, A_eq=aa, b_eq=bb, bounds=options, method='highs')
        if not lp.success:
            for method in ('highs-ds', 'highs-ipm'):
                retry = linprog(objective, A_eq=aa, b_eq=bb, bounds=options,
                                method=method, options={'presolve': False, 'time_limit': 20})
                if retry.success:
                    lp = retry
                    break
        if not lp.success:
            ray = timed_ray(bounds)
            if ray is not None:
                record['terminal_y'] = ray
                record['status'] = 'complete_conditional_exclusion'
                checkpoint()
                print(json.dumps({'event': record['status'], 'steps': len(steps)}), flush=True)
                return
            record['remaining_lp_status'] = int(lp.status)
            break
        candidates = sorted(((min(x - math.floor(x), math.ceil(x) - x), j, math.floor(x))
                             for j, x in enumerate(lp.x) if abs(x - round(x)) > 1e-6), reverse=True)
        for _, j, k in candidates[:100]:
            if time.monotonic() - started >= args.seconds:
                break
            for side in (0, 1):
                key = (len(steps), j, k, side)
                if key in tried:
                    continue
                trial = child(bounds, j, k, side)
                result = linprog(np.zeros(len(A[0])), A_eq=aa, b_eq=bb,
                                 bounds=[trial.get(q, (0, None)) for q in range(len(A[0]))], method='highs')
                if result.status == 2:
                    pending.append((j, k, side))
                else:
                    tried.add(key)
        round_number += 1
        print(json.dumps({'event': 'probe_round', 'round': round_number, 'proposals': len(pending),
                          'steps': len(steps), 'seconds': time.monotonic() - started}), flush=True)
        if not pending:
            break
    checkpoint()
    replay_steps(A, b, steps)
    print(json.dumps({'status': record['status'], 'steps': len(steps),
                      'seconds': time.monotonic() - started}), flush=True)


if __name__ == '__main__':
    main()

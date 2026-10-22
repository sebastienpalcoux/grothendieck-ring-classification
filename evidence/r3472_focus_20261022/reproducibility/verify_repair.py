#!/usr/bin/env python3
"""Independently audit the omitted R3472 counting dependency and its repair.

The original source-bound mathematical verifier remains unchanged. This check
compares every old/new receipt field, permits changes only in the documented
cache-state diagnostics, recounts by a separate iterative algorithm, and runs
that original verifier under both normal and optimized Python.
"""
from copy import deepcopy
from functools import lru_cache
from math import isqrt
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PREFIX = 'evidence/rank8_creative_20261022/'
CASE = PREFIX+'r3472/'


def need(ok, why):
    if not ok:
        raise ValueError(why)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def independent_count(h):
    """Extract a generating-function coefficient by descending-type layers.

    This uses no helper import or recursion over positive-u types. Layer values
    are coefficients, and each next layer explicitly multiplies by the entire
    finite geometric series for one type. Square partitions use a separate
    largest-square recursion, instead of the helper's ascending coin DP.
    """
    U, V, W = 35-h, 70, 175
    types = sorted([(u*u, u*t, t*t)
                    for u in range(1, isqrt(U)+1)
                    for t in range(1, isqrt(W)+1) if u*t <= V], reverse=True)
    layer = {(U, V, W): 1}
    for a, b, c in types:
        nxt = {}
        for (u, v, w), coefficient in layer.items():
            for n in range(min(u//a, v//b, w//c)+1):
                uu, vv, ww = u-n*a, v-n*b, w-n*c
                if vv*vv > uu*ww:
                    continue
                key = (uu, vv, ww)
                nxt[key] = nxt.get(key, 0)+coefficient
        layer = nxt

    @lru_cache(None)
    def squareparts(w, t):
        if w == 0:
            return 1
        if t == 0:
            return 0
        if t*t > w:
            return squareparts(w, t-1)
        return squareparts(w, t-1)+squareparts(w-t*t, t)

    return sum(coefficient*squareparts(w, isqrt(w))
               for (u, v, w), coefficient in layer.items() if u == v == 0)


def report():
    old = json.loads((HERE/'original_verification.json').read_text())
    new = json.loads((ROOT/CASE/'verification.json').read_text())
    original_accepted = json.loads((HERE/'original_accepted.json').read_text())
    original_manifest = json.loads((HERE/'original_source_manifest.json').read_text())
    accepted = json.loads((ROOT/PREFIX/'accepted.json').read_text())
    need(sha(HERE/'original_accepted.json') == original_manifest[PREFIX+'accepted.json'],
         'Archived original acceptance file changed')
    need(sha(HERE/'original_verification.json') ==
         original_accepted['source_sha256'][CASE+'verification.json'] ==
         original_manifest[CASE+'verification.json'],
         'Archived original mathematical receipt changed')
    helper = CASE+'second_branch_count.py'
    need(helper not in original_accepted['source_sha256'] and helper not in original_manifest,
         'The archived source inventories no longer document the omission')
    for name in ('verify.py', 'product_equations.py', 'exact_integer.py'):
        need(sha(ROOT/CASE/name) == original_accepted['source_sha256'][CASE+name],
             'An original mathematical verifier was modified: '+name)
    for path in (helper, CASE+'verification.json'):
        need(accepted['source_sha256'][path] == sha(ROOT/path),
             'Repaired source is missing its acceptance binding: '+path)

    diagnostics = []
    restored = deepcopy(new)
    for index, (a, b) in enumerate(zip(old['second_branch_arithmetic_counts'],
                                      new['second_branch_arithmetic_counts'])):
        need(a['integral_global_dimension'] == b['integral_global_dimension'],
             'Count ordering changed')
        diagnostics.append({'h': a['integral_global_dimension'],
                            'historical_cache_states': a['states'],
                            'reconstructed_cache_states': b['states']})
        restored['second_branch_arithmetic_counts'][index]['states'] = a['states']
    need(restored == old, 'A mathematical receipt field changed')
    hs = [1, 2, 5, 7]
    independent = [independent_count(h) for h in hs]
    need(independent == [272348, 124228, 3900, 2] ==
         [r['nonintegral_multisets'] for r in new['second_branch_arithmetic_counts']],
         'Independent generating-function count disagrees')
    need(new['general_categorification_status'] == 'unresolved' and
         new['new_model_constructed'] is False, 'Repair changed mathematical scope')

    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env.pop('PYTHONPATH', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    lanes = []
    for flag, lane in (([], 'normal'), (['-O'], 'optimized')):
        child = subprocess.run([sys.executable, *flag, str(ROOT/CASE/'verify.py')],
                               cwd=ROOT, env=env, capture_output=True, text=True)
        need(child.returncode == 0, lane+' original verifier failed: '+child.stderr)
        need(json.loads(child.stdout) == new, lane+' replay differs from repaired receipt')
        log = HERE/('replay_'+lane+'.log')
        log.write_text(child.stdout+child.stderr)
        lanes.append({'lane': lane, 'returncode': 0,
                      'original_verifier_unchanged': True,
                      'log': str(log.relative_to(ROOT)), 'log_sha256': sha(log)})
    sources = [HERE/'original_accepted.json', HERE/'original_verification.json',
               HERE/'original_source_manifest.json',
               *(ROOT/CASE/n for n in ('verify.py', 'product_equations.py',
                                       'exact_integer.py', 'verification.json',
                                       'second_branch_count.py'))]
    return {'schema': 'r3472-reproducibility-repair/v1', 'status': 'PASS',
            'baseline_commit': 'ebaeb62',
            'defect': 'Missing imported second_branch_count.py, also absent from accepted source inventories',
            'repair': 'Reconstructed exact counter; unchanged original verifier; regenerated honest execution diagnostics',
            'historical_mathematical_receipt_preserved': True,
            'changed_receipt_fields': ['second_branch_arithmetic_counts.'+str(i)+'.states'
                                       for i in range(4)],
            'cache_state_diagnostics': diagnostics,
            'independent_exact_counts': [{'h': h, 'count': n}
                                         for h, n in zip(hs, independent)],
            'independent_count_total': sum(independent),
            'legacy_verifier_replays': lanes,
            'general_categorification_status': 'unresolved',
            'new_model_constructed': False,
            'source_sha256': {str(p.relative_to(ROOT)): sha(p) for p in sources}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = report()
    path = HERE/'repair_verification.json'
    if args.write:
        path.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    else:
        need(json.loads(path.read_text()) == result, 'Saved repair verification differs')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Regenerate the complementary degree-six lists and verify every exclusion.

Requires Python 3.10 or later, NumPy and SymPy. No optimizer is used.
Run python verify_complement.py; optional --jobs sets the worker count.
The three supplied JSON files contain integer dual weights. All other
numerical lists are built from scratch in a temporary directory.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

SOURCES = ('sextic_conductor_sieve.py', 'proper_subfield_ratios.py',
           'sextic13_descent.py', 'sextic_lattice.py', 'positive_dnumber_squares.py',
           'sextic_trace_systems.py', 'sextic_matrix_bound.py', 'sextic_polytope.py')
WEIGHTS = ('sextic_5_7_polytope.json', 'sextic_8_13_polytope.json',
           'sextic_8_13_matrix_bound.json')


def verify(workspace, jobs):
    base = Path(__file__).resolve().parent
    for name in SOURCES + WEIGHTS:
        shutil.copyfile(base / name, workspace / name)
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    env.pop('PYTHONOPTIMIZE', None)

    def run(args):
        command = [sys.executable, str(workspace / args[0]), *map(str, args[1:])]
        result = subprocess.run(command, cwd=workspace, env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        if result.returncode:
            raise RuntimeError(' '.join(command) + '\n' + result.stdout)
        print('PASS', *args, flush=True)

    def data(name):
        return json.loads((workspace / name).read_text())

    def batch(commands):
        with ThreadPoolExecutor(max_workers=jobs) as pool:
            list(pool.map(run, commands))

    batch([('sextic_conductor_sieve.py',), ('proper_subfield_ratios.py',),
           ('sextic13_descent.py',), ('sextic_matrix_bound.py', 8, 13, '--verify')])
    table = {(r['quadratic_conductor'], r['cubic_conductor']): r
             for r in data('sextic_trace_bounds.json')}
    expected = set()
    for aa, bb in (((5, 8), (7, 9, 13, 19, 31, 37, 43)),
                   ((13, 17), (7, 9, 13)), ((29, 37, 40, 41), (7, 9)),
                   ((65, 104), (7, 13)), ((53, 61, 73, 85, 89, 97, 101, 109, 136), (7,))):
        expected.update((a, b) for a in aa for b in bb)
    assert len(expected) == 41 and expected == set(table)
    relative = {(37, 9), (41, 9)} | {(a, 7) for a in (73, 85, 89, 97, 101, 104, 109, 136)}
    for a, b in relative:
        row = table[a, b]
        cap, c = row['alpha_trace_bound'], row['sextic_conductor']
        assert (cap * cap - 36)**3 * b * b < 729 * a * c * c
    unit = {(5, 7): (1037, 12273947, 8360, 8007),
            (5, 9): (86, 5207, 163, 128), (8, 13): (160, 5973, 76, 46)}
    regular = set(table) - relative - set(unit) - {(13, 13), (8, 7), (8, 9)}
    assert len(regular) == 25
    assert table[5, 7]['alpha_trace_bound'] == 1037 and table[5, 9]['alpha_trace_bound'] == 86
    commands = [('sextic_lattice.py', a, b, table[a, b]['alpha_trace_bound'], '--exact')
                for a, b in sorted(regular, key=lambda k: -table[k]['alpha_trace_bound'])]
    batch([('positive_dnumber_squares.py', a, b, unit[a, b][0]) for a, b in unit] + commands)
    vector_total, survivors = 0, {}
    for a, b in regular:
        row = data(f'sextic_{a}_{b}_exact.json')
        assert row['status'] == 'EXACT_INTEGER_ENUMERATION'
        assert row['Amax'] == table[a, b]['alpha_trace_bound']
        vector_total += row['lattice_vectors']
        count = sum(x['degree'] == 6 for x in row['candidates'])
        if count:
            survivors[a, b] = count
    assert vector_total == 4903735 and survivors == {(5, 13): 27, (13, 7): 7, (29, 7): 1}
    for (a, b), (cap, vectors, ratios, primitive) in unit.items():
        row = data(f'sextic_{a}_{b}_squares.json')
        assert row['Amax'] == cap and row['status'] == 'EXACT_UNIT_SQUARE_ENUMERATION'
        assert len(row['candidates']) == ratios and sum(r['vectors'] for r in row['counts']) == vectors
        assert sum(x['degree'] == 6 for x in row['candidates']) == primitive
    survivors[5, 9] = unit[5, 9][3]
    batch([('sextic_trace_systems.py', a, b) for a, b in survivors]
          + [('sextic_polytope.py', a, b, '--verify') for a, b in ((5, 7), (8, 13))])
    for (a, b), count in survivors.items():
        rows = data(f'sextic_{a}_{b}_trace_exact.json')
        assert len(rows) == count and all(r['fourier_survivors'] == 0 for r in rows)
        if (a, b) == (5, 9):
            assert sum(r.get('trace_vectors', 0) for r in rows) == 37988587
    for a, b in ((5, 7), (8, 13)):
        weights = data(f'sextic_{a}_{b}_polytope.json')
        assert not weights['survivors'] and len(weights['certificates']) == unit[a, b][3]
    print('PASS: all 39 complementary fields. The separate height-200 proof treats the other two.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=2)
    args = parser.parse_args()
    if args.jobs < 1 or not __debug__:
        parser.error('use unoptimized Python and a positive worker count')
    with tempfile.TemporaryDirectory() as directory:
        verify(Path(directory), args.jobs)

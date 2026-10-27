#!/usr/bin/env python3
"""Independent exact certificate arithmetic; no optimizer is called.

The center-system builder is shared and explicitly an inherited input.
This checker independently verifies completeness, integral dual certificates,
and nonnegative rational primal witnesses for both new discrete stages.
"""
from fractions import Fraction
from pathlib import Path
import hashlib
import importlib.util
import itertools
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'r8_1154'
spec = importlib.util.spec_from_file_location('r1154_system', SOURCE / 'build_odd_rotation_system.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def require(condition, message):
    if not condition:
        raise ValueError(message)

stages = [
    ((4, 5), 'odd_rotation_probe_h3.json', list(itertools.product((-1, 2), repeat=2))),
    ((1, 4, 5, 6), 'odd_rotation_discrete_h3.json',
     [(x, 2, 2, y) for x, y in itertools.product((Fraction(-1), Fraction(1, 2), Fraction(2)), repeat=2)]),
]
output = []
for objects, filename, choices in stages:
    A, base, constants, domain, meta = module.build(objects)
    tensor_hash = hashlib.sha256(json.dumps(meta['source_tensor'], separators=(',', ':')).encode()).hexdigest()
    require(tensor_hash == 'c399505be76a64c8aba65feaf2cd55125dc7132f5894b74e58b64473d1387e25', 'Wrong source tensor')
    records = json.loads((SOURCE / filename).read_text())['results']
    expected = {(p, tuple(map(Fraction, values))) for p in (6971, 8766, 8772) for values in choices}
    observed = set()
    for record in records:
        pattern = record['pattern']
        values = tuple(map(Fraction, record['projected_third_indicators']))
        require((pattern, values) not in observed, 'Duplicate branch')
        observed.add((pattern, values))
        tail = [d * values[k // 2] - low for k, (d, low) in enumerate(constants)]
        require(all(Fraction(v).denominator == 1 for v in tail), 'Nonintegral scaled RHS')
        b = base + domain['completions'][pattern] + list(map(int, tail))
        require(len(A) == len(b), 'Matrix/RHS dimension mismatch')
        summary = {'objects': list(objects), 'pattern': pattern, 'values': list(map(str, values))}
        if 'exact_primal' in record:
            support = record['exact_primal']
            x = {int(j): Fraction(v) for j, v in support}
            require(len(x) == len(support), 'Repeated support column')
            require(all(0 <= j < len(A[0]) and value >= 0 for j, value in x.items()), 'Invalid primal domain')
            require(all(sum(row[j] * value for j, value in x.items()) == target for row, target in zip(A, b)), 'Failed exact primal equation')
            require(all(v == 2 for v in values), 'Unexpected feasible branch')
            summary.update(kind='feasible', support=len(x))
        else:
            y = record['exact_ray']
            require(len(y) == len(b) and all(type(v) is int for v in y), 'Invalid dual domain')
            dot = sum(v * w for v, w in zip(y, b))
            transpose = [sum(row[j] * v for row, v in zip(A, y)) for j in range(len(A[0]))]
            require(dot < 0 and min(transpose) >= 0, 'Failed exact Farkas certificate')
            summary.update(kind='infeasible', bTy=dot, min_ATy=min(transpose))
        output.append(summary)
    require(observed == expected, 'Incomplete discrete branch coverage')

receipt = {'status': 'PASS', 'checks': output, 'infeasible': sum(r['kind'] == 'infeasible' for r in output),
           'feasible': sum(r['kind'] == 'feasible' for r in output),
           'scope': 'Exact necessary-system certificate audit, not a category exclusion or construction.'}
(HERE / 'r1154_odd_rotation_full_independent_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(f"PASS: {receipt['infeasible']} exact dual certificates and {receipt['feasible']} exact primal witnesses")

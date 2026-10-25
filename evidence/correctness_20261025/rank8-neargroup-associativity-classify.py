import os
#!/usr/bin/env python3
"""Conditional finite classification using partial S-derived fusion matrices.
No assertion of the categorical partial-S premises is encoded here.
Allows all three duality cycle types on the four equal-dimensional D objects.
"""

def require(condition, message):
    if not condition:
        raise RuntimeError(message)
import collections, importlib.util, itertools, json, time
from pathlib import Path
import numpy as np
ROOT = Path(os.environ.get('FUSION_CLASSIFICATION_REPO',Path(__file__).resolve().parents[2])).resolve()
OUT = Path(__file__).resolve().parent
s = importlib.util.spec_from_file_location('ng', ROOT / 'evidence/unified_20261016/rank8/verify_neargroup_centralizer.py')
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
BASE = np.array(m.model(820), dtype=np.int64)
OTHER = np.array(m.model(869), dtype=np.int64)
require(np.array_equal(BASE[:4], OTHER[:4]), 'rank8-neargroup-associativity-classify: required invariant from original line 15')
TRIPLES = list(itertools.combinations_with_replacement(range(4), 3))
PAIRS = list(itertools.combinations_with_replacement(range(4), 2))

def canonical(N):
    best = None
    for p in itertools.permutations(range(4, 8)):
        inds = [0, 1, 2, 3] + list(p)
        z = tuple((int(x) for x in N[np.ix_(inds, inds, inds)].flat))
        if best is None or z < best:
            best = z
    return best
CAN = {canonical(BASE): 820, canonical(OTHER): 869}
start = time.time()
report = {'status': 'PASS', 'scope': 'conditional on displayed partial fusion rules, not a center identification proof', 'classes': []}
for star in [(0, 1, 2, 3), (1, 0, 2, 3), (1, 0, 3, 2)]:
    reps = {t: min(t, tuple(sorted((star[i] for i in t)))) for t in TRIPLES}
    variables = sorted(set(reps.values()))
    vi = {t: i for i, t in enumerate(variables)}
    A = [[0] * len(variables) for pair in PAIRS]
    target = []
    for r, (i, j) in enumerate(PAIRS):
        target.append(2 + int(j == star[i]))
        for k in range(4):
            A[r][vi[reps[tuple(sorted((i, j, k)))]]] += 1
    rows = [[r for r in range(len(A)) if A[r][v]] for v in range(len(variables))]
    linear_count = 0
    assoc_count = 0
    classes = {}
    nodes = 0

    def visit(values, residual, unassigned):
        global linear_count, assoc_count, nodes
        nodes += 1
        if not unassigned:
            if any(residual):
                return
            linear_count += 1
            N = BASE.copy()
            for i, j in itertools.product(range(4), repeat=2):
                N[4 + i, 4 + j, 0] = int(j == star[i])
                N[4 + i, 4 + j, 1] = int(j != star[i])
                for k in range(4):
                    N[4 + i, 4 + j, 4 + k] = values[vi[reps[tuple(sorted((i, j, star[k])))]]]
            if any((not np.array_equal(N[i] @ N[j], N[j] @ N[i]) for i in range(8) for j in range(i + 1, 8))):
                return
            L = np.einsum('ijx,xkl->ijkl', N, N)
            R = np.einsum('jkx,ixl->ijkl', N, N)
            require(np.array_equal(L, R), 'rank8-neargroup-associativity-classify: required invariant from original line 51')
            star8 = [0, 1, 2, 3] + [4 + x for x in star]
            require(all((N[i, j, 0] == int(j == star8[i]) for i, j in itertools.product(range(8), repeat=2))), 'rank8-neargroup-associativity-classify: required invariant from original line 53')
            require(all((N[i, j, k] == N[j, i, k] == N[star8[i], star8[j], star8[k]] == N[i, star8[k], star8[j]] for i, j, k in itertools.product(range(8), repeat=3))), 'rank8-neargroup-associativity-classify: required invariant from original line 54')
            assoc_count += 1
            key = canonical(N)
            if key not in classes:
                classes[key] = {'star': star, 'variable_representatives': variables, 'values': values.copy(), 'tensor': N.tolist(), 'labelled_count': 0, 'known_candidate': CAN.get(key)}
            classes[key]['labelled_count'] += 1
            return
        for r, left in enumerate(residual):
            if left < 0 or (left and (not any((A[r][v] for v in unassigned)))):
                return
        upper = {v: min((residual[r] // A[r][v] for r in rows[v])) for v in unassigned}
        for r, left in enumerate(residual):
            if left > sum((A[r][v] * upper[v] for v in unassigned)):
                return
        v = min(unassigned, key=lambda v: (upper[v], -len(rows[v]), v))
        remaining = tuple((w for w in unassigned if w != v))
        for x in range(upper[v] + 1):
            values[v] = x
            visit(values, [left - A[r][v] * x for r, left in enumerate(residual)], remaining)
    visit([None] * len(variables), target, tuple(range(len(variables))))
    row = {'star': star, 'variables': len(variables), 'search_nodes': nodes, 'row_sum_solutions': linear_count, 'associative_labelled_solutions': assoc_count, 'isomorphism_classes': len(classes), 'classes': list(classes.values())}
    report['classes'].append(row)
    print(json.dumps({k: v for k, v in row.items() if k != 'classes'}), flush=True)
report['elapsed_seconds'] = time.time() - start
(OUT / 'rank8-neargroup-associativity-classify.json').write_text(json.dumps(report, indent=2) + '\n')
print('elapsed', report['elapsed_seconds'], flush=True)

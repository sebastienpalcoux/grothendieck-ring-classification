"""Independent exact certificate for R6_9_8785; no imported census algorithms.
Requires only Python standard library and SymPy. No floating point decisions.
Usage: python verify_8785.py [unresolved_tensors.json]
"""
import hashlib, itertools, json, sys
from pathlib import Path
import sympy as s
def need(condition, message):
    if not condition:
        raise ValueError(message)

SOURCE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name('tensor_8785.json')
R = next((x['N'] for x in json.loads(SOURCE.read_text()) if x['id'] == 'R6_9_8785'))
need(hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest() == '7897af45c48cb1d416710f37ea9c4c11226490421317d193c85e3cc5022b3da8', "hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest() == '7897af45c48cb1d416710f37ea9c4c11226490421317d193c85e3cc5022b3da8'")

def add(x, y):
    return (x[0] + y[0], x[1] + y[1])

def mul(x, y):
    return (x[0] * y[0] + x[1] * y[1], x[0] * y[1] + x[1] * y[0] + x[1] * y[1])

def scale(n, x):
    return (n * x[0], n * x[1])

def dot(c, v):
    return (sum((a * n for (a, b), n in zip(c, v))), sum((b * n for (a, b), n in zip(c, v))))

def norm(x):
    return x[0] ** 2 + x[0] * x[1] - x[1] ** 2
C = [[(1, 0), (8, 13), (7, 13), (7, 13), (9, 13), (9, 13)], [(1, 0), (21, -13), (20, -13), (20, -13), (22, -13), (22, -13)], [(1, 0), (1, 2), (-1, -1), (1, 0), (0, 1), (-1, -2)], [(1, 0), (1, 2), (1, 0), (-1, -1), (-1, -2), (0, 1)], [(1, 0), (3, -2), (-2, 1), (1, 0), (1, -1), (-3, 2)], [(1, 0), (3, -2), (1, 0), (-2, 1), (-3, 2), (1, -1)]]
need(len(set(map(tuple, C))) == 6, 'len(set(map(tuple, C))) == 6')
for c in C:
    for i, j in itertools.product(range(6), repeat=2):
        need(mul(c[i], c[j]) == dot(c, R[i][j]), 'mul(c[i], c[j]) == dot(c, R[i][j])')
need(all((R[i][j][0] == int(i == j) for i, j in itertools.product(range(6), repeat=2))), 'all((R[i][j][0] == int(i == j) for i, j in itertools.product(range(6), repeat=2)))')
need(all((a > 0 or (a == 0 and b > 0) for a, b in C[0])), 'all((a > 0 or (a == 0 and b > 0) for a, b in C[0]))')
f = [dot([mul(x, x) for x in c], [1] * 6) for c in C]
D = f[0]
t = C[0][1]
need(D == (1170, 1885) and norm(D) == 21125, 'D == (1170, 1885) and norm(D) == 21125')
need(all((norm(x) == 125 for x in f[2:])), 'all((norm(x) == 125 for x in f[2:]))')
need(C[1] == [(a + b, -b) for a, b in C[0]], 'C[1] == [(a + b, -b) for a, b in C[0]]')
beta = [(1, 0), (233, 377), (26, 39), (26, 39), (442, 715), (442, 715)]
need(all((mul(fj, b) == D for fj, b in zip(f, beta))), 'all((mul(fj, b) == D for fj, b in zip(f, beta)))')
small = []
for tail in itertools.product(range(4), repeat=5):
    v = (1,) + tail
    if dot(C[0], v) == beta[2]:
        small.append(v)
need(len(small) == 8, 'len(small) == 8')
rows = [(1, 0, 0, 0, 0, 0)]
for row in [C[0], [mul(beta[2], x) for x in C[2]], [mul(beta[3], x) for x in C[3]]]:
    rows.extend([[z[h] for z in row] for h in range(2)])
A = s.Matrix(rows)
need(A.rank() == 6, 'A.rank() == 6')
branches = []
for v2, v3 in itertools.product(small, repeat=2):
    if dot(C[2], v3) != dot(C[3], v2):
        continue
    low = [(1, 0, 0, 0, 0, 0), None, v2, v3, None, None]
    for j in [1, 4, 5]:
        rhs = [1, *beta[j], *mul(beta[j], dot(C[j], v2)), *mul(beta[j], dot(C[j], v3))]
        try:
            sol, params = A.gauss_jordan_solve(s.Matrix(rhs))
        except ValueError:
            break
        need(params.rows == 0, 'params.rows == 0')
        if any((x.q != 1 or x < 0 for x in sol)):
            break
        low[j] = tuple(map(int, sol))
    else:
        N = [s.Matrix(x) for x in R]
        B = sum((M * M.T for M in N), s.zeros(6))
        need(tuple((sum((v[i] for v in low)) for i in range(6))) == tuple(B[0, :]), 'tuple((sum((v[i] for v in low)) for i in range(6))) == tuple(B[0, :])')
        need(all((mul(beta[i], dot(C[i], low[j])) == mul(beta[j], dot(C[j], low[i])) for i, j in itertools.combinations(range(6), 2))), 'all((mul(beta[i], dot(C[i], low[j])) == mul(beta[j], dot(C[j], low[i])) for i, j in itertools.combinations(range(6), 2)))')
        ell = dot(beta, [v[1] for v in low])
        gap = add(mul(add(scale(3, t), (1, 0)), ell), scale(-1, mul(mul(D, t), add(t, (1, 0)))))
        need(gap[0] > 0 and gap[1] > 0, 'gap[0] > 0 and gap[1] > 0')
        branches.append({'small_columns': [v2, v3], 'columns': low, 'ell': ell, 'positive_gap': gap})
need(len(branches) == 10, 'len(branches) == 10')
need(sorted(set((tuple(v['positive_gap']) for v in branches))) == [(110756, 179192), (184284, 298168), (257812, 417144)], "sorted(set((tuple(v['positive_gap']) for v in branches))) == [(110756, 179192), (184284, 298168), (257812, 417144)]")
print(json.dumps({'id': 'R6_9_8785', 'verified': True, 'small_columns': len(small), 'ordered_pairs': len(small) ** 2, 'complete_labeled_frames': len(branches), 'existence': {'general': 'unknown', 'pivotal': 'no', 'spherical': 'no', 'pseudo_unitary': 'no', 'unitary': 'no'}, 'branches': branches}, indent=2))

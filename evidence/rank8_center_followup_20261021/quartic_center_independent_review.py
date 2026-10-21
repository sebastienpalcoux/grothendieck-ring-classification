"""Independent quartic/Gram reconstruction; external scratch research only.

No functions from quartic_center_challenge.py are imported. Frozen source
character arithmetic and the existing complete restriction-column domain are
reused. Normal mode compares a saved scratch receipt; --write creates it.
No repository files are written, and checks remain active under python -O.
"""
import argparse
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root', type=Path, default=Path.cwd())
parser.add_argument('--write', action='store_true')
args = parser.parse_args()
root = args.root.resolve()
p = root / 'evidence/rank8_frontier_20261021/noncommutative'
sys.path.insert(0, str(p))
import central_support as c
import character_modular as md
import rotation_search as base

base.install()
s = c.s


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rational(z):
    values = list(map(s.Rational, c.ec(z)))
    need(len(values) <= 1, 'Required rational value')
    return values[0] if values else s.S.Zero


def check_721():
    record = next(x for x in json.loads((c.OLD.parent / 'pipeline/census_m3.json').read_text()) if x['id'] == 'R8_3_721')
    R = record['tensor']
    need(hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest() == record['tensor_sha256'], 'Source tensor identity')
    a = c.w.data(R)
    K = a['K']
    cols = a['lows'][10]
    chars = md.characters(R, a)
    need(all(ch[i] == ch[a['du'][i]] for ch in chars for i in range(8)), 'Self-dual distinguished characters')
    perms = md.assignments(a, chars, cols)
    L = s.Matrix.hstack(*map(s.Matrix, cols))
    Q, high = md.full.base.grams.high_columns(a, L)

    # Independently exhaust the full 7x7 integer Gram system, using all entries.
    A = s.Matrix([[v[i] * v[j] for v, z in high] for i, j in itertools.product(range(7), repeat=2)])
    b = s.Matrix(list(Q))
    rr, piv = A.row_join(b).rref()
    need(len(high) not in piv, 'Consistent Gram equations')
    free = [j for j in range(len(high)) if j not in piv]
    bounds = [min(int(Q[i, i]) // (v[i] * v[i]) for i in range(7) if v[i]) for v, z in high]
    counts = []
    for choice in itertools.product(*(range(bounds[i] + 1) for i in free)):
        x = [s.S.Zero] * len(high)
        for i, z in zip(free, choice):
            x[i] = s.Integer(z)
        for row, j in enumerate(piv):
            x[j] = rr[row, len(high)] - sum(rr[row, k] * x[k] for k in free)
        if all(z.q == 1 and 0 <= z <= bounds[i] for i, z in enumerate(x)):
            need(A * s.Matrix(x) == b, 'Complete Gram solution')
            counts.append(tuple(map(int, x)))
    need(len(counts) == 4 and len(perms) == 2, 'Eight-case domain')
    saved = json.loads((p / 'verlinde_low_721.json').read_text())
    need(sorted((tuple(case['permutation']), tuple(case['multiplicities'])) for case in saved['cases']) == sorted(itertools.product(perms, counts)), 'Saved eight-case coverage')

    pairs = list(itertools.combinations_with_replacement(range(1, 5), 2))
    summaries = []
    for perm, cs in itertools.product(perms, counts):
        types = [j for j, m in enumerate(cs) for _ in range(m)]
        allcols = list(map(tuple, cols)) + [(0,) + tuple(v) for (v, z), m in zip(high, cs) for _ in range(m)]
        dims = [sum((K(n) * d for n, d in zip(v, a['ds'])), K.zero) for v in allcols]
        sv = [[a['D'] / a['codegrees'][perm.index(i)] / K(a['multiplicities'][perm.index(i)]) * md.value(chars[perm.index(i)], v, K) for v in allcols] for i in range(5)]
        need(all(sv[0][z] == dims[z] for z in range(len(dims))), 'FP row normalization')
        C = {(i, j, k): rational(sum((sv[i][z] * sv[j][z] * sv[k][z] / dims[z] for z in range(len(dims))), K.zero) / a['D'] ** 2) for i, j, k in itertools.product(range(1, 5), repeat=3)}
        need(all(v.q == 1 and v >= 0 for v in C.values()), 'Integral nonnegative cubic coefficients')
        # Every central simple occurs once; m_E is already present in its S row.
        G = s.Matrix(10, 10, lambda u, v: rational(sum((sv[pairs[u][0]][z] * sv[pairs[u][1]][z] * sv[pairs[v][0]][z] * sv[pairs[v][1]][z] / dims[z] ** 2 for z in range(len(dims))), K.zero) / a['D'] ** 2)
                     - int(pairs[u][0] == pairs[u][1]) * int(pairs[v][0] == pairs[v][1])
                     - sum(C[pairs[u] + (e,)] * C[pairs[v] + (e,)] for e in range(1, 5)))
        T = s.Matrix(8, 10, lambda k, u: sum(cols[pairs[u][0]][i] * cols[pairs[u][1]][j] * R[i][j][k] for i, j in itertools.product(range(8), repeat=2))
                     - int(pairs[u][0] == pairs[u][1] and k == 0)
                     - sum(C[pairs[u] + (e,)] * cols[e][k] for e in range(1, 5)))
        M = s.Matrix.hstack(*(s.Matrix(v) for v in allcols[5:]))
        # Different reconstruction from the producer's independent-row formula.
        X0 = M.pinv() * T
        need(M * X0 == T, 'Moore-Penrose solution')
        H = G - X0.T * X0
        need(H.rank() == 1, 'Residual Gram rank')
        k = next(i for i in range(10) if H[i, i])
        h = H[k, :] / H[k, k]
        norm = H[k, k]
        need(H == norm * h.T * h and norm == s.Rational(2, 3), 'Rank-one Gram factor')
        choices = []
        for row in range(M.cols):
            candidates = [s.Integer(n) - X0[row, k] for n in range(math.floor(X0[row, k]) - 1, math.floor(X0[row, k]) + 3)]
            choices.append([x for x in candidates if x * x <= norm and all((X0[row, j] + x * h[j]).q == 1 and X0[row, j] + x * h[j] >= 0 for j in range(10))])
        # Exhaust every coordinate choice, rather than only choosing its minimum.
        hits = []

        def visit(i, ts, squared_norm):
            if squared_norm > norm:
                return
            if i == M.cols:
                if squared_norm == norm and M * s.Matrix(ts) == s.zeros(8, 1):
                    hits.append(ts)
                return
            for x in choices[i]:
                visit(i + 1, ts + [x], squared_norm + x * x)

        visit(0, [], s.S.Zero)
        need(len(hits) == 1, 'Independent exhaustive uniqueness')
        X = X0 + s.Matrix(hits[0]) * h
        need(M * X == T and X.T * X == G, 'Unique nonnegative integer witness')
        summaries.append({'permutation': list(perm), 'multiplicities': list(cs), 'high_simple_count': M.cols,
                          'coordinate_box': math.prod(map(len, choices)), 'integer_gram_solutions': len(hits),
                          'ranks': {'M': M.rank(), 'G': G.rank(), 'residual': H.rank()},
                          'high_types': types, 'unique_high_pair_coefficients': [list(map(int, row)) for row in X.tolist()]})
    return {'tensor_sha256': record['tensor_sha256'], 'complete_integer_Gram_box': math.prod(bounds[i] + 1 for i in free),
            'pair_order': list(map(list, pairs)), 'cases': summaries}


def check_s3():
    # Ordinary S3 characters derived from permutation actions, not a supplied N.
    group = list(itertools.permutations(range(3)))

    def character(g):
        return (1, (-1) ** sum(g[i] > g[j] for i in range(3) for j in range(i + 1, 3)), sum(g[i] == i for i in range(3)) - 1)

    ct = [character(g) for g in group]
    N = {}
    for i, j, k in itertools.product(range(3), repeat=3):
        numerator = sum(q[i] * q[j] * q[k] for q in ct)
        need(numerator % 6 == 0, 'S3 character decomposition integrality')
        N[i, j, k] = numerator // 6
    for q in ct:
        for i, j in itertools.product(range(3), repeat=2):
            need(q[i] * q[j] == sum(N[i, j, k] * q[k] for k in range(3)), 'S3 tensor-character identity')
    flux = [(0, 1, 2)] * 3 + [(1, 0, 2)] * 2 + [(1, 2, 0)] * 3
    dims = [1, 1, 2, 3, 3, 2, 2, 2]
    S = [[s.Integer(dims[z]) * character(flux[z])[i] for z in range(8)] for i in range(3)]
    for i, j, k in itertools.product(range(3), repeat=3):
        need(sum(S[i][z] * S[j][z] * S[k][z] / dims[z] for z in range(8)) / 36 == N[i, j, k], 'S3 cubic')
    for i, j, k, l in itertools.product(range(3), repeat=4):
        need(sum(S[i][z] * S[j][z] * S[k][z] * S[l][z] / dims[z] ** 2 for z in range(8)) / 36 == sum(N[i, j, x] * N[k, l, x] for x in range(3)), 'S3 fourth moment')
    return {'status': 'PASS', 'cubics': 27, 'quartics': 81, 'matrix_block_beta': '6/(3*2)=1'}


dependencies = ['central_support.py', 'character_modular.py', 'rotation_search.py', 'verlinde_low_721.json']
result = {'status': 'PASS', 'scope': 'Unique necessary high coefficients for the ten distinguished pairs in each of eight R721 cases; no center fusion ring, category, or exclusion is claimed.',
          'R721': check_721(), 'S3_control': check_s3(),
          'source_sha256': {str((p / name).relative_to(root)): sha(p / name) for name in dependencies},
          'frozen_main_source_manifest_sha256': sha(root / 'evidence/rank8_frontier_20261021/publication/source_manifest.json'),
          'reviewer_sha256': sha(Path(__file__))}
target = HERE / 'quartic_center_independent_review.json'
if args.write:
    target.write_text(json.dumps(result, indent=2) + '\n')
else:
    need(json.loads(target.read_text()) == result, 'Independent scratch receipt differs')
print(json.dumps({'status': 'PASS', 'cases': len(result['R721']['cases']), 'Gram_box': result['R721']['complete_integer_Gram_box'],
                  'S3_control': result['S3_control'], 'receipt': target.name}, indent=2))

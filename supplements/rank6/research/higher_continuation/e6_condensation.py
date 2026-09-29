"""Exact surviving E6 condensation for R6_6_1035; not an exclusion.

All Gram decompositions are exhausted. The forced dual ring is isomorphic to
the input. Hagge--Hong Theorem 1, arXiv:0704.0208, gives four Galois-conjugate
categorifications of the E6 rank-three subring. Its standard 1+x algebra is
therefore available for every categorification of that subring.
"""
import itertools
import json
import math
from pathlib import Path
import sys

P = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(P / 'software'))
import sympy as s
from exact import require
from integer_gram import frames
from rings import permute


def factors(G):
    n = G.rows
    cols = []
    for v in itertools.product(*(range(math.isqrt(int(G[i, i])) + 1)
                                 for i in range(n))):
        if any(v) and all(v[i] * v[j] <= G[i, j]
                          for i in range(n) for j in range(n)):
            cols.append((v, 0))
    ff = frames(G, cols, 30)
    return [s.Matrix.hstack(*(s.Matrix(v) for (v, _), c in zip(cols, fr)
                             for _ in range(c))) for fr in ff]


def run():
    rows = json.load(open(P / 'data/census.json'))
    R = next(r['N'] for r in rows if r['id'] == 'R6_6_1035')
    n, x, g = 6, 4, 1
    eye = s.eye(n)
    require(R[g][g] == [1, 0, 0, 0, 0, 0], 'wrong E6 involution')
    require(R[g][x] == R[x][g] == [0, 0, 0, 0, 1, 0], 'wrong E6 action')
    require(R[x][x] == [1, 1, 0, 0, 2, 0], 'wrong E6 square')
    G = eye + s.Matrix(R[x])
    Bs = factors(G)
    require(len(Bs) == 1, 'free module Gram is not unique')
    B = Bs[0]
    require(B.shape == (n, n) and B.det() != 0 and B * B.T == G,
            'free module factor is not invertible')
    Ms = [B.inv() * s.Matrix(R[i]).T * B for i in range(n)]
    require(all(t.q == 1 and t >= 0 for M in Ms for t in M),
            'module action is not nonnegative integral')
    require(all(M == M.T for M in Ms), 'module transpose relation')
    require(all(Ms[i] * Ms[j] == sum((R[i][j][k] * Ms[k]
                                    for k in range(n)), s.zeros(n))
                for i in range(n) for j in range(n)), 'module product relation')
    u = next(j for j in range(n) if B[0, j] == 1)
    require(sum(B[0, j] for j in range(n)) == 1, 'algebra module not simple')
    H = eye + Ms[x]
    Cs = factors(H)
    require(len(Cs) == 1, 'dual free module Gram is not unique')
    C = Cs[0]
    require(C.shape == (n, n) and C.det() != 0 and C * C.T == H,
            'dual free module factor is not invertible')
    V = s.Matrix.hstack(*(M[:, u] for M in Ms))
    require(V.det() != 0, 'unit evaluation is not faithful')
    Xs = []
    for j in range(n):
        coeff = V.inv() * C[:, j]
        Xs.append(sum((coeff[i] * Ms[i] for i in range(n)), s.zeros(n)))
    require(all(t.q == 1 and t >= 0 for X in Xs for t in X),
            'dual action is not nonnegative integral')
    require(all(X * M == M * X for X in Xs for M in Ms),
            'left and right module actions do not commute')
    W = s.Matrix.hstack(*(s.Matrix(list(X)) for X in Xs))
    require(W.rank() == n, 'dual action not faithful')
    S = []
    for X in Xs:
        row = []
        for Y in Xs:
            z, params = W.gauss_jordan_solve(s.Matrix(list(X * Y)))
            require(not params and all(t.q == 1 and t >= 0 for t in z),
                    'dual product is not based')
            row.append([int(t) for t in z])
        S.append(row)
    unit = next(i for i, X in enumerate(Xs) if X == eye)
    order = [unit] + [i for i in range(n) if i != unit]
    S = permute(S, order)
    maps = [list((0,) + p) for p in itertools.permutations(range(1, n))
            if permute(S, (0,) + p) == R]
    require(maps, 'dual ring is not the input ring')
    report = {'id': 'R6_6_1035', 'conclusion': 'survives; forced dual ring is isomorphic to input',
              'categorical_scope': 'general', 'E6_subring': [0, g, x],
              'algebra': [1, 0, 0, 0, 1, 0],
              'reference': 'Hagge--Hong, Some non-braided fusion categories of rank 3, Theorem 1',
              'reference_url': 'https://arxiv.org/pdf/0704.0208',
              'free_gram_factors': len(Bs), 'free_factor': B.tolist(),
              'module_matrices': [M.tolist() for M in Ms],
              'dual_gram_factors': len(Cs), 'dual_factor': C.tolist(),
              'dual_tensor': S, 'isomorphisms_to_input': maps}
    target = Path(__file__).with_suffix('.json')
    target.write_text(json.dumps(report, indent=2, default=int) + '\n')
    print(report['conclusion'])


if __name__ == '__main__':
    run()

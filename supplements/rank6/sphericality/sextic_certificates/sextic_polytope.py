#!/usr/bin/env python3
"""Rational outer-polytope certificates for a fixed sextic ratio.

Floating linear programming only proposes nonnegative dual weights.  A
rejection is accepted only after its separating inequality is verified over
the integers, using outward rational embedding and square-root bounds.
"""
from pathlib import Path
from itertools import product
from math import gcd, isqrt, lcm
import json, sys
import numpy as np
from sextic_lattice import field, embedding_bounds


SCALE = 10**12


def sqrt_upper(n, d):
    return (isqrt(n*d*SCALE*SCALE)+d-1)//d + 1


def constraints(a, b, v, G, ML, MU):
    vp, vn = np.maximum(v, 0), np.minimum(v, 0)
    lo = ML@vp+MU@vn
    hi = MU@vp+ML@vn
    assert all(hi[0] < lo[i] or np.array_equal(np.linalg.matrix_power(G, i)@v, v)
               for i in range(1, 6))
    rows, rhs = [], []

    def add_pq(wp, wq, bound):
        row = [int(x)*(int(lo[i]) if x >= 0 else int(hi[i]))
               + int(wq[i])*SCALE for i, x in enumerate(wp)]
        rows.append(row); rhs.append(int(bound))

    z = [0]*6
    for i in range(1, 6):
        w = z.copy(); w[0] = 1; w[i] = -1
        add_pq(z, w, 0)  # q_0 is minimal.
        add_pq(w, z, 0)  # p_0 is minimal.
    add_pq([1]*6, z, SCALE)
    add_pq([-1]*6, z, -SCALE)
    vv = v.copy()
    for _ in range(1, 6):
        vv = G@vv
        p, n = np.maximum(vv, 0), np.minimum(vv, 0)
        upper = MU@p+ML@n
        rows.append([-int(x) for x in upper]); rhs.append(-SCALE)

    directions = [(A, B) for A in range(-4, 5) for B in range(-4, 5)
                  if gcd(A, B) == 1]
    for C, S, c in [([2, 1, -1, -2, -1, 1], [0, 1, 1, 0, -1, -1], lcm(a, b)),
                    ([2, -1, -1, 2, -1, -1], [0, 1, -1, 0, 1, -1], b)]:
        C, S = np.array(C), np.array(S)
        for A, B in directions:
            w = A*C+B*S
            for ordinary in (False, True):
                cap = gcd(c, 2 if ordinary else 4)
                bound = sqrt_upper(4*cap*(3*A*A+B*B), 3*c)
                add_pq(w if ordinary else z, z if ordinary else w, bound)
        for Ap, Bp, Aq, Bq in product([-1, 0, 1], repeat=4):
            if not (Ap or Bp or Aq or Bq):
                continue
            wp, wq = Ap*C+Bp*S, Aq*C+Bq*S
            bound = sqrt_upper(8*(3*Ap*Ap+Bp*Bp+6*Aq*Aq+2*Bq*Bq), 3*c)
            add_pq(wp, wq, bound)
    C = np.array([1, -1, 1, -1, 1, -1])
    for sign in (-1, 1):
        add_pq(sign*C, z, sqrt_upper(gcd(a, 2), a))
        add_pq(z, sign*C, sqrt_upper(gcd(a, 4), a))
    for Ap, Aq in directions:
        add_pq(Ap*C, Aq*C, sqrt_upper(2*Ap*Ap+4*Aq*Aq, a))
    return rows, rhs


def orient(v, G, ML, MU):
    for _ in range(6):
        vp, vn = np.maximum(v, 0), np.minimum(v, 0)
        lo, hi = ML@vp+MU@vn, MU@vp+ML@vn
        if all(hi[0] < lo[i] or np.array_equal(np.linalg.matrix_power(G, i)@v, v)
               for i in range(1, 6)):
            return v
        v = G@v
    raise AssertionError('No unique least embedding')


def certificate(rows, rhs, weights):
    assert all(w >= 0 for _, w in weights)
    lower = min(sum(rows[j][i]*w for j, w in weights) for i in range(6))
    upper = sum(rhs[j]*w for j, w in weights)
    return int(lower-upper)


def run(a, b):
    from scipy.optimize import linprog
    base = Path(__file__).parent
    source = base/f'sextic_{a}_{b}_squares.json'
    data = json.loads(source.read_text())
    one, mul, E, G, matrices, t, H = field(a, b)
    ML, MU, scale = embedding_bounds(a, b)
    assert scale == SCALE
    records, survivors = [], []
    for ci, cand in enumerate(data['candidates']):
        if cand['degree'] != 6:
            continue
        v = orient(np.array(cand['coefficients'], dtype=np.int64), G, ML, MU)
        rows, rhs = constraints(a, b, v, G, ML, MU)
        A = np.asarray(rows, dtype=float)/SCALE
        bb = np.asarray(rhs, dtype=float)/SCALE
        res = linprog([0]*6+[1], A_ub=np.column_stack([A, -np.ones(len(A))]),
                      b_ub=bb, A_eq=[[1]*6+[0]], b_eq=[1],
                      bounds=[(0, None)]*7, method='highs')
        assert res.success, res.message
        rejected = False
        if res.fun > 1e-9:
            for precision in (10**6, 10**9, 10**12):
                weights = [(j, int(round(-x*precision)))
                           for j, x in enumerate(res.ineqlin.marginals) if x < -1e-14]
                gap = certificate(rows, rhs, weights)
                if gap > 0:
                    records.append(dict(index=ci, trace=cand['trace'],
                                        weights=weights, gap=str(gap)))
                    rejected = True
                    break
        if not rejected:
            survivors.append(dict(index=ci, trace=cand['trace'], phase1=float(res.fun)))
        if ci % 100 == 0:
            print(a, b, ci, 'excluded', len(records), 'remaining', len(survivors), flush=True)
    output = dict(a=a, b=b, constraint_version=1, scale=SCALE,
                  certificates=records, survivors=survivors)
    (base/f'sextic_{a}_{b}_polytope.json').write_text(json.dumps(output, indent=2)+'\n')
    print(a, b, 'FINAL excluded', len(records), 'remaining', len(survivors),
          'max trace', max((r['trace'] for r in survivors), default=0), flush=True)


def verify(a, b):
    """Check stored certificates without running a numerical optimizer."""
    base = Path(__file__).parent
    data = json.loads((base/f'sextic_{a}_{b}_squares.json').read_text())
    output = json.loads((base/f'sextic_{a}_{b}_polytope.json').read_text())
    assert output['constraint_version'] == 1 and output['scale'] == SCALE
    one, mul, E, G, matrices, t, H = field(a, b)
    ML, MU, scale = embedding_bounds(a, b)
    assert scale == SCALE
    indices = set()
    for row in output['certificates']:
        ci = row['index']
        assert ci not in indices
        indices.add(ci)
        cand = data['candidates'][ci]
        assert cand['degree'] == 6 and cand['trace'] == row['trace']
        v = orient(np.array(cand['coefficients'], dtype=np.int64), G, ML, MU)
        rows, rhs = constraints(a, b, v, G, ML, MU)
        gap = certificate(rows, rhs, row['weights'])
        assert gap > 0 and str(gap) == row['gap']
    residual = {i for i, cand in enumerate(data['candidates']) if cand['degree'] == 6} - indices
    assert residual == {r['index'] for r in output['survivors']}
    print(a, b, 'exact dual certificates verified:', len(indices),
          '; uncovered full-degree ratios:', len(residual))


if __name__ == '__main__':
    if sys.argv[-1] == '--verify':
        verify(*map(int, sys.argv[1:-1]))
    else:
        run(*map(int, sys.argv[1:]))

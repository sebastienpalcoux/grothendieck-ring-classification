"""Exact hypotheses for the dimension-220 descent obstruction.

The categorical and group-theoretical argument is in dimension220_proof.md.
This file certifies its input tensor premises, not the cited theorems.
"""
import hashlib
import itertools
import json
from pathlib import Path
import sys
import sympy as s


def require(condition, message):
    if not condition:
        raise ValueError(message)


def certificate(N):
    n = len(N)
    if n != 7 or any(N[i][j] != N[j][i] for i, j in itertools.product(range(n), repeat=2)):
        return None
    d = [1, 1, 1, 4, 10, 10, 1]
    if not all(sum(N[i][j][k]*d[k] for k in range(n)) == d[i]*d[j]
               for i, j in itertools.product(range(n), repeat=2)):
        return None
    inv = [0, 1, 2, 6]
    h = 6
    action = [6, 2, 1, 3, 4, 5, 0]
    if not all(N[h][i] == N[i][h] == [int(j == action[i]) for j in range(n)] for i in range(n)):
        return None
    # The element labelled 1 generates the pointed group C4.
    powers = [0]
    for _ in range(4):
        row = N[powers[-1]][1]
        require(sum(row) == 1, 'invertible multiplication')
        powers.append(row.index(1))
    if powers != [0, 1, 6, 2, 0]:
        return None
    dual = []
    for i in range(n):
        js = [j for j in range(n) if N[i][j][0]]
        require(len(js) == 1 and N[i][js[0]][0] == 1, 'dual')
        dual.append(js[0])
    adj = {0}
    for i in range(n):
        adj.update(k for k in range(n) if N[i][dual[i]][k])
    while True:
        before = set(adj)
        for i, j in itertools.product(before, repeat=2):
            adj.update(k for k in range(n) if N[i][j][k])
        if before == adj:
            break
    if adj != set(range(n)):
        return None
    mats = [s.Matrix(A) for A in N]
    t = s.Symbol('t')
    casimir = sum((M*M.T for M in mats), s.zeros(n))
    p = casimir.charpoly(t).as_poly()
    expected = s.Poly((t-220)*(t-44)**2*(t-5)*(t-4)**3, t)
    if p != expected:
        return None
    fs = [220, 5, 44, 44, 4, 4, 4]
    a = [220//f for f in fs]
    require(a == [1, 44, 5, 5, 55, 55, 55] and sum(a) == 220, 'induced unit dimensions')
    halves = [list(S) for k in range(7) for S in itertools.combinations(range(1, 7), k)
              if sum(a[i] for i in S) == 110]
    require(halves == [[4, 5], [4, 6], [5, 6]], 'all half partitions')
    require(all(2 not in S and 3 not in S for S in halves), 'odd-prime dimensions centralize fermion')
    return {'kind': 'dimension220_half_partition_descent',
            'scope': 'general_complex_fusion_category',
            'dimensions': d, 'global_dimension': 220,
            'formal_codegrees': fs, 'codegree_polynomial': [int(x) for x in p.all_coeffs()],
            'induced_unit_dimensions': a, 'negative_half_subsets': halves,
            'invertible_labels': inv, 'generator_powers': powers,
            'involution': h, 'involution_action': action,
            'adjoint_closure': sorted(adj),
            'forced_descent_dimensions': [1, 1, 2, 2, 5, 5, 5, 5],
            'forced_descent_global_dimension': 110,
            'tensor_sha256': hashlib.sha256(json.dumps(N, separators=(',', ':')).encode()).hexdigest(),
            'proof': 'evidence/rank7_m5_20261019/models/dimension220_proof.md'}


def verify(N, cert):
    require(cert is not None and cert == certificate(N), 'dimension220 certificate mismatch')
    return True


def main():
    rows = json.loads(Path(sys.argv[1]).read_text())
    records = []
    for row in rows:
        cert = certificate(row['tensor'])
        if cert is not None:
            verify(row['tensor'], cert)
            records.append({'id': row['id'], 'status': 'excluded', 'exact_checked': True, 'certificate': cert})
    require([r['id'] for r in records] == ['R7_5_4757'], 'dimension220 exclusion inventory')
    Path(__file__).with_name('dimension220_result.json').write_text(json.dumps(records, indent=2)+'\n')
    print(json.dumps(records))


if __name__ == '__main__':
    main()

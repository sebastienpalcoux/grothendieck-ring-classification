"""Exact premise certificate for Nikshych--Ostrik's maximal near-group theorem.

Nikshych--Ostrik, Appendix to Ostrik, Pivotal fusion
categories of rank 3, arXiv:1309.4822, Theorem A.14(ii):
if |G|=m+1>1, categorifiability of NG(G,m) requires G to be cyclic.
This checker uses only the necessary cyclicity, not prime-power testing.
"""
import itertools
import json
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def certificate(N):
    n = len(N)
    require(all(len(A) == n and all(len(row) == n for row in A) for A in N), 'tensor shape')
    unit = [1]+[0]*(n-1)
    dual = []
    for i in range(n):
        js = [j for j in range(n) if N[i][j][0] == 1]
        require(len(js) == 1, 'unique dual')
        dual.append(js[0])
    invertibles = [i for i in range(n) if N[i][dual[i]] == unit]
    if len(invertibles) != n-1:
        return None
    x = next(i for i in range(n) if i not in invertibles)
    if dual[x] != x or not all(N[x][x][g] == 1 for g in invertibles):
        return None
    for g in invertibles:
        expected = [int(k == x) for k in range(n)]
        if N[g][x] != expected or N[x][g] != expected:
            return None
    m = N[x][x][x]
    if len(invertibles) != m+1 or m == 0:
        return None
    products = {}
    for g, h in itertools.product(invertibles, repeat=2):
        support = [i for i, v in enumerate(N[g][h]) if v]
        require(len(support) == 1 and N[g][h][support[0]] == 1 and support[0] in invertibles, 'invertible closure')
        products[g, h] = support[0]
    orders = {}
    for g in invertibles:
        h = 0
        for k in range(1, len(invertibles)+1):
            h = products[h, g]
            if h == 0:
                orders[g] = k
                break
        require(g in orders, 'finite group element order')
    if len(invertibles) in orders.values():
        return None
    witness = next(((g, h, products[g, h], products[h, g])
                    for g, h in itertools.product(invertibles, repeat=2)
                    if products[g, h] != products[h, g]), None)
    return {'kind': 'noncyclic_maximal_near_group', 'invertibles': invertibles,
            'noninvertible': x, 'level': m, 'element_orders': [[g, orders[g]] for g in invertibles],
            'noncommutativity_witness': list(witness) if witness else None,
            'theorem': 'Nikshych--Ostrik, Appendix, Theorem A.14(ii)',
            'reference': 'https://arxiv.org/abs/1309.4822',
            'scope': 'general_complex_fusion_category'}


def verify(N, cert):
    require(cert == certificate(N), 'maximal near-group premise certificate mismatch')
    require(cert is not None, 'no noncyclic maximal near-group obstruction')
    return True


def main():
    rows = json.loads(Path(sys.argv[1]).read_text())
    records = []
    for row in rows:
        cert = certificate(row['tensor'])
        if cert is not None:
            verify(row['tensor'], cert)
            records.append({'id': row['id'], 'certificate': cert,
                            'status': 'excluded', 'exact_checked': True})
    require([r['id'] for r in records] == ['R7_5_4812'], 'expected single maximal near-group exclusion')
    Path(__file__).with_name('maximal_near_group_result.json').write_text(json.dumps(records, indent=2)+'\n')
    print(json.dumps(records))


if __name__ == '__main__':
    main()

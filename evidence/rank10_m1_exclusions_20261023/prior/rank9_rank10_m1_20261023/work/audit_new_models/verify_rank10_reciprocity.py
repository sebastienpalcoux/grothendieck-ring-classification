"""Independent exact scalar-character/Gram/reciprocity exclusion replay.

Only standard-library arithmetic is used. Candidate columns are regenerated
from their dimensions, not trusted from the search receipts. No completeness
of the scalar-character inventory or equality of the first Gram row is
needed: any distinct subset of scalar characters gives necessary constraints.
"""
from fractions import Fraction as Q
from itertools import product
from math import isqrt, lcm
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
IDS = [65, 89, 90, 91, 120, 143, 144, 147, 162, 182]
ZERO = (Q(0),) * 4
ONE = (Q(1), Q(0), Q(0), Q(0))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def add(x, y):
    return tuple(a+b for a, b in zip(x, y))


def scale(n, x):
    return tuple(n*a for a in x)


def mul(x, y):
    a, b, c, d = x
    e, f, g, h = y
    return (a*e+2*b*f-c*g-2*d*h, a*f+b*e-c*h-d*g,
            a*g+c*e+2*b*h+2*d*f, a*h+d*e+b*g+c*f)


def total(xs):
    out = ZERO
    for x in xs:
        out = add(out, x)
    return out


def decode(coefficients):
    # The receipt generator is sqrt(2)+i, satisfying t^4-2t^2+9.
    t = (Q(0), Q(1), Q(1), Q(0))
    out = ZERO
    for c in coefficients:
        out = add(mul(out, t), scale(Q(c), ONE))
    return out


def candidate_columns(B, dims, beta):
    require(beta[2:] == (0, 0) and all(x.denominator == 1 for x in beta[:2]),
            'real integral dimension coordinates')
    a, b = map(int, beta[:2])
    bounds = [min(B[0][i], isqrt(B[i][i])) for i in range(len(dims))]
    out = []

    def extend(v, aa, bb):
        i = len(v)
        if i == len(dims):
            if aa == bb == 0:
                out.append(tuple(v))
            return
        da, db = dims[i]
        bound = min(bounds[i], aa//da)
        if db:
            bound = min(bound, bb//db)
        for x in range(bound+1):
            extend(v+[x], aa-x*da, bb-x*db)

    extend([1], a-1, b)
    return out


def solve_one(ident, N, receipt):
    n = len(N)
    require(receipt['field_polynomial'] == ['1','0','-2','0','9'],
            'specified algebraic field')
    require(all(d == 1 for d in receipt['degrees']), 'scalar characters only')
    rows = [[decode(c) for c in row] for row in receipt['characters']]
    require(len({tuple(row) for row in rows}) == len(rows), 'distinct characters')
    dual = [next(j for j in range(n) if N[i][j][0]) for i in range(n)]
    for row in rows:
        require(row[0] == ONE, 'normalized character')
        require(all(mul(row[i], row[j]) == total(
            scale(N[i][j][k], row[k]) for k in range(n))
            for i, j in product(range(n), repeat=2)), 'exact ring homomorphism')
    ds = rows[receipt['fp']]
    allowed = {(Q(1),Q(0),Q(0),Q(0)),
               (Q(2),Q(2),Q(0),Q(0)), (Q(3),Q(2),Q(0),Q(0))}
    require(all(d in allowed for d in ds), 'strictly positive FP dimensions')
    dims = [tuple(map(int, d[:2])) for d in ds]
    D = total(mul(d, d) for d in ds)
    require(D == (96,64,0,0), 'global FP dimension')
    fs = [total(mul(row[i], row[dual[i]]) for i in range(n)) for row in rows]
    require(fs == list(map(decode, receipt['formal_codegrees'])),
            'formal codegrees recomputed')
    betas = list(map(decode, receipt['dimensions']))
    require(all(mul(f, b) == D for f, b in zip(fs, betas)), 'central dimensions D/f')
    B = [[sum(N[a][j][k]*N[k][dual[a]][i] for a, k in product(range(n), repeat=2))
          for i in range(n)] for j in range(n)]
    require(all(B[i][j] == B[j][i] for i, j in product(range(n), repeat=2)),
            'adjunction Gram symmetry')
    cols = [candidate_columns(B, dims, b) for b in betas]
    require(all(set(cs) == set(map(tuple, rs)) for cs, rs in zip(cols, receipt['column_sets'])),
            'independently exhaustive column sets agree')
    m = len(rows)
    weights = [[mul(betas[j], x) for x in rows[j]] for j in range(m)]
    denominator = lcm(*(q.denominator for row in weights for x in row for q in x))
    weights = [[[int(q*denominator) for q in x] for x in row] for row in weights]
    # values[h][a][j] = beta_j chi_j(v_h,a).
    values = [[[tuple(sum(v[i]*weights[j][i][r] for i in range(n)) for r in range(4))
                for j in range(m)] for v in cs] for h, cs in enumerate(cols)]
    outer = [[[ [v[i]*v[j] for j in range(n)] for i in range(n)] for v in cs]
             for cs in cols]
    visits, leaves = 0, 0
    rejection_counts = dict(gram_entry=0, gram_minor=0, reciprocity=0)

    def dfs(domains, gram, selected):
        nonlocal visits, leaves
        visits += 1
        if len(selected) == m:
            leaves += 1
            return
        h = min((h for h in range(m) if h not in selected),
                key=lambda h: len(domains[h]))
        for choice in domains[h]:
            gram2 = [[gram[i][j]-outer[h][choice][i][j] for j in range(n)]
                     for i in range(n)]
            if any(x < 0 for row in gram2 for x in row):
                rejection_counts['gram_entry'] += 1
                continue
            if any(gram2[i][j]**2 > gram2[i][i]*gram2[j][j]
                   for i in range(n) for j in range(i)):
                rejection_counts['gram_minor'] += 1
                continue
            next_domains = list(domains)
            failed = False
            for j in range(m):
                if j in selected or j == h:
                    continue
                next_domains[j] = [b for b in domains[j]
                                   if values[h][choice][j] == values[j][b][h]]
                if not next_domains[j]:
                    failed = True
                    rejection_counts['reciprocity'] += 1
                    break
            if not failed:
                dfs(next_domains, gram2, selected | {h})

    dfs([list(range(len(cs))) for cs in cols], B, set())
    require(leaves == 0, ident + ': all necessary assignments excluded')
    return dict(id=ident, status='PASS', scalar_characters=m,
                column_counts=list(map(len, cols)), dfs_nodes=visits,
                surviving_assignments=leaves, rejected=rejection_counts,
                used_first_row_equality=False)


def main():
    T = json.loads((ROOT/'work/input_audit/tensors.json').read_text())
    results = []
    for number in IDS:
        ident = 'R10_1_'+str(number)
        suffix = '_reciprocal.json' if number in (89,147) else '_partial_reciprocal.json'
        receipt = json.loads((ROOT/'work/resolve_rank10_quadratic'/(ident+suffix)).read_text())
        result = solve_one(ident, T[ident], receipt)
        print(ident, 'PASS', result['dfs_nodes'], 'nodes', flush=True)
        results.append(result)
    (OUT/'rank10_reciprocity_audit.json').write_text(json.dumps(results, indent=2)+'\n')


if __name__ == '__main__':
    main()

"""General categorical exclusion by a rank-three C2 near-group subring.

Ostrik, Pivotal fusion categories of rank 3, Theorem 4.1 (arXiv:1309.4822)
explicitly assumes only categorifiability of K(1,0,m,0) and proves m <= 2.
The theorem itself has no pivotality hypothesis: its proof invokes the
Galois-pseudounitary reduction for near-group categories.

A full dual-closed based subring of a Grothendieck ring is realized by a
fusion subcategory. The scan below checks the complete 3x3 product table
in the ambient tensor, including every vanishing coefficient off the subring.
No floating point or discovery optimizer is involved.
"""
import argparse
import json
from pathlib import Path
from exact import require


def basis(n, i):
    return [int(j == i) for j in range(n)]


def certificate(R):
    n = len(R)
    for g in range(1, n):
        if R[g][g] != basis(n, 0):
            continue
        for x in range(1, n):
            if x == g:
                continue
            m = R[x][x][x]
            if m <= 2:
                continue
            target = basis(n, 0)
            target[g] = 1
            target[x] = m
            if (R[g][x] == R[x][g] == basis(n, x)
                    and R[x][x] == target
                    and all(R[0][i] == R[i][0] == basis(n, i)
                            for i in (0, g, x))):
                return {'kind': 'rank3_c2_neargroup_subring',
                        'basis': [0, g, x], 'near_group_parameter': m,
                        'scope': 'general_complex_fusion_categories',
                        'source': 'Ostrik3, Theorem 4.1'}
    return None


def verify(R, c):
    require(c['kind'] == 'rank3_c2_neargroup_subring', 'incorrect certificate kind')
    zero, g, x = c['basis']
    require(zero == 0 and 0 < g < len(R) and 0 < x < len(R) and g != x, 'invalid subring labels')
    m = c['near_group_parameter']
    require(type(m) is int and m > 2, 'near-group parameter is not excluded')
    expected = [[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                [[0, 1, 0], [1, 0, 0], [0, 0, 1]],
                [[0, 0, 1], [0, 0, 1], [1, 1, m]]]
    B = [0, g, x]
    # Independent exact verification of all coefficients in all nine products.
    for i in range(3):
        for j in range(3):
            v = [0] * len(R)
            for k in range(3):
                v[B[k]] = expected[i][j][k]
            require(R[B[i]][B[j]] == v, 'ambient product does not match the forbidden subring')
    require(c['scope'] == 'general_complex_fusion_categories', 'incorrect scope')
    require(c['source'] == 'Ostrik3, Theorem 4.1', 'incorrect source')
    return True


def run():
    P = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--verify', action='store_true')
    args = ap.parse_args()
    rows = json.load(open(P / 'data/census.json'))
    manifest = P / 'verification/continuation/campaign_manifest.json'
    if manifest.exists():
        residuals = set(json.load(open(manifest))['input_ids'])
    else:
        residuals = {r['id'] for r in json.load(open(P / 'data/unresolved_tensors.json'))}
    path = P / 'certificates/new_rank3_subring.json'
    if args.verify:
        report = json.load(open(path))
        by_id = {r['id']: r for r in rows}
        for rec in report['certificates']:
            verify(by_id[rec['id']]['N'], rec['certificate'])
        print('Verified', len(report['certificates']), 'general-scope exclusions')
        return
    found = []
    for row in rows:
        c = certificate(row['N'])
        if c:
            verify(row['N'], c)
            found.append({'id': row['id'], 'multiplicity': row['m'],
                          'previously_unresolved': row['id'] in residuals,
                          'certificate': c})
    # Independent model-based checks on the admitted m=0,1,2 near-group rings.
    controls = []
    for m in range(3):
        R = [[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
             [[0, 1, 0], [1, 0, 0], [0, 0, 1]],
             [[0, 0, 1], [0, 0, 1], [1, 1, m]]]
        require(certificate(R) is None, 'positive control was excluded')
        controls.append({'near_group_parameter': m, 'excluded': False})
    report = {'criterion': 'Rank-three C2 near-group subring descent',
              'reference_url': 'https://arxiv.org/pdf/1309.4822',
              'reference_theorem': '4.1', 'scope': 'general',
              'checked_tensors': len(rows), 'residuals_checked': len(residuals),
              'new_exclusions': [x['id'] for x in found if x['previously_unresolved']],
              'positive_controls': controls, 'certificates': found}
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'certificates'}, indent=2))
    print('All applicable census exclusions:', len(found))

if __name__ == '__main__':
    run()

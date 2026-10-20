"""Exact quadratic Casimir compression obstruction, including sphericalization.

The theorem and its scope are in QUADRATIC_COMPRESSION_PROOF.md.  This code
does not infer a general exclusion from the stronger spherical bound.
"""
import argparse
import copy
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
x = s.Symbol('x')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def tensor_hash(R):
    return hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest()


def analyze(R):
    n = len(R)
    require(n > 0 and all(len(M) == n and all(len(row) == n for row in M) for M in R), 'tensor shape')
    require(all(type(v) is int and v >= 0 for M in R for row in M for v in row), 'tensor coefficients')
    N = [s.Matrix(M) for M in R]
    B = sum((M * M.T for M in N), s.zeros(n))
    poly = B.charpoly(x).as_poly()
    factors = s.factor_list(poly)[1]
    groups = defaultdict(list)
    factor_receipt = []
    for p, m in factors:
        coefficients = list(map(int, p.all_coeffs()))
        factor_receipt.append({'coefficients': coefficients, 'multiplicity': m})
        if p.degree() != 2:
            continue
        a, b, c = p.all_coeffs()
        require(a == 1, 'monic Casimir factor')
        disc = b * b - 4 * c
        require(disc > 0, 'positive quadratic discriminant')
        squarefree = s.prod(prime for prime, exponent in s.factorint(disc).items() if exponent % 2)
        require(squarefree > 1, 'irreducible quadratic factor')
        q = squarefree if squarefree % 4 == 1 else 4 * squarefree
        groups[int(q)].append({'coefficients': coefficients, 'multiplicity': m,
                               'discriminant': int(disc),
                               'contribution': str(q * m * disc / c ** 2)})
    checks = []
    for q, items in sorted(groups.items()):
        Q = sum((s.Rational(item['contribution']) for item in items), s.S.Zero)
        checks.append({'field_discriminant': q, 'factors': items, 'Q': str(Q),
                       'general_bound': 4, 'general_violation': bool(Q > 4),
                       'spherical_bound': 1, 'spherical_violation': bool(Q > 1)})
    return {'tensor_sha256': tensor_hash(R), 'casimir_characteristic_polynomial': list(map(int, poly.all_coeffs())),
            'casimir_factors': factor_receipt, 'quadratic_checks': checks}


def certificate(R):
    result = analyze(R)
    if not any(check['general_violation'] for check in result['quadratic_checks']):
        return None
    return {'kind': 'quadratic_casimir_compression', 'scope': 'general_complex', **result}


def verify(R, cert):
    require(cert.get('kind') == 'quadratic_casimir_compression', 'certificate kind')
    require(cert.get('scope') == 'general_complex', 'certificate scope')
    computed = certificate(R)
    require(computed is not None, 'the general compression bound is not violated')
    require(cert == computed, 'certificate differs from independently recomputed exact values')
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default=str(HERE.parent / 'computation/source_frontier.json'))
    parser.add_argument('--output', default=str(HERE / 'quadratic_compression_results.json'))
    parser.add_argument('--replay', action='store_true')
    args = parser.parse_args()
    rows = json.loads(Path(args.source).read_text())
    if args.replay:
        report = json.loads(Path(args.output).read_text())
        byid = {row['id']: row['tensor'] for row in rows}
        for row in report['certificates']:
            verify(byid[row['id']], row['certificate'])
        print(json.dumps({'status': 'PASS', 'replayed_general_certificates': len(report['certificates'])}))
        return
    receipts = []
    certificates = []
    for row in rows:
        receipts.append({'id': row['id'], **analyze(row['tensor'])})
        cert = certificate(row['tensor'])
        if cert:
            verify(row['tensor'], cert)
            certificates.append({'id': row['id'], 'certificate': cert})
    controls = json.loads((ROOT / 'supplements/rank7/data/model_catalog.json').read_text())
    positive_receipts = [{'id': row['id'], **analyze(row['tensor'])} for row in controls]
    require(all(not check['spherical_violation'] for row in positive_receipts for check in row['quadratic_checks']), 'positive control')
    rejected = 0
    byid = {row['id']: row['tensor'] for row in rows}
    for row in certificates:
        bad = copy.deepcopy(row['certificate'])
        bad['quadratic_checks'][0]['Q'] = '0'
        try:
            verify(byid[row['id']], bad)
        except ValueError:
            rejected += 1
    require(rejected == len(certificates), 'corrupted Q rejected')
    # R4569 violates only the spherical bound. Its exclusion must be refused.
    conditional = next((row for row in rows if row['id'] == 'R7_5_4569'), None)
    if conditional:
        require(certificate(conditional['tensor']) is None, 'spherical-only result promoted')
    result = {'status': 'PASS', 'tested': len(rows), 'general_exclusions': len(certificates),
              'certificates': certificates, 'receipts': receipts,
              'controls': {'positive_models': len(controls), 'spherical_false_positives': 0,
                           'corrupted_certificates_rejected': rejected,
                           'spherical_only_R4569_not_promoted': conditional is not None,
                           'positive_receipts': positive_receipts}}
    Path(args.output).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('status', 'tested', 'general_exclusions')}))


if __name__ == '__main__':
    main()

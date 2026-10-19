"""Exact integral formal-codegree obstruction; no numerical exclusions.

For a commutative integral fusion category C, every formal codegree is a
positive integer dividing FPdim(C). Indeed C is pseudo-unitary (ENO), and
Ostrik's central induction theorem supplies a center simple of dimension
FPdim(C)/f. Its forgetful image in integral C has integral FP dimension.
Thus f is rational; since f is an algebraic integer, f is integral.

The dimension vectors below were discovered numerically but are verified
against all 49 dimension equations using integer arithmetic. Eigenvalue
computations do not occur in this verifier.
"""
import hashlib
import itertools
import json
from pathlib import Path
import sys
import sympy as s

VECTORS = {
    'R7_5_1390': [1, 1, 7, 7, 2, 2, 2],
    'R7_5_1404': [1, 1, 9, 9, 2, 6, 6],
    'R7_5_2454': [1, 1, 14, 16, 17, 18, 19],
    'R7_5_2865': [1, 1, 14, 16, 17, 18, 19],
    'R7_5_4695': [1, 1, 1, 10, 4, 10, 1],
    'R7_5_4757': [1, 1, 1, 4, 10, 10, 1],
    'R7_5_4812': [1, 1, 1, 1, 6, 1, 1],
    'R7_5_4982': [1, 1, 1, 3, 12, 12, 12],
    'R7_5_5007': [1, 1, 1, 9, 9, 9, 12],
    'R7_5_5187': [1, 6, 6, 1, 2, 3, 3],
    'R7_5_5678': [1, 1, 1, 1, 1, 6, 1],
    'R7_5_5759': [1, 3, 3, 6, 6, 1, 2],
}
EXPECTED_EXCLUDED = ['R7_5_1390', 'R7_5_1404', 'R7_5_2454',
                     'R7_5_4695', 'R7_5_5187', 'R7_5_5759']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def tensor_digest(N):
    return hashlib.sha256(json.dumps(N, separators=(',', ':')).encode()).hexdigest()


def certificate(N, dimensions):
    n = len(N)
    require(len(dimensions) == n and dimensions[0] == 1 and
            all(type(x) is int and x > 0 for x in dimensions), 'positive integer dimensions')
    require(all(sum(N[i][j][k]*dimensions[k] for k in range(n)) == dimensions[i]*dimensions[j]
                for i, j in itertools.product(range(n), repeat=2)), 'dimension equations')
    if any(N[i][j] != N[j][i] for i, j in itertools.product(range(n), repeat=2)):
        return None
    D = sum(x*x for x in dimensions)
    mats = [s.Matrix(A) for A in N]
    C = sum((M*M.T for M in mats), s.zeros(n))
    t = s.Symbol('t')
    polynomial = C.charpoly(t).as_poly()
    factors = polynomial.factor_list()[1]
    for f, multiplicity in factors:
        co = [int(x) for x in f.all_coeffs()]
        if f.degree() > 1:
            reason = 'nonrational formal codegree in an integral category'
        elif (-co[1] <= 0) or D % (-co[1]):
            reason = 'integral formal codegree does not divide global dimension'
        else:
            continue
        return {'kind': 'integral_formal_codegree', 'dimensions': dimensions,
                'global_dimension': D, 'codegree_polynomial': [int(x) for x in polynomial.all_coeffs()],
                'irreducible_factor': co, 'factor_multiplicity': multiplicity,
                'reason': reason, 'tensor_sha256': tensor_digest(N),
                'scope': 'general_complex_fusion_category'}
    return None


def verify(N, cert):
    require(cert is not None and certificate(N, cert['dimensions']) == cert,
            'integral codegree certificate mismatch')
    return True


def main():
    rows = {r['id']: r for r in json.loads(Path(sys.argv[1]).read_text())}
    records = []
    profiles = []
    for rid, d in VECTORS.items():
        N = rows[rid]['tensor']
        cert = certificate(N, d)
        profiles.append({'id': rid, 'dimensions': d, 'global_dimension': sum(x*x for x in d),
                         'tensor_sha256': tensor_digest(N), 'excluded_by_this_criterion': cert is not None})
        if cert is not None:
            verify(N, cert)
            records.append({'id': rid, 'status': 'excluded', 'exact_checked': True, 'certificate': cert})
    require([r['id'] for r in records] == EXPECTED_EXCLUDED, 'expected integral exclusion inventory')
    here = Path(__file__).parent
    (here/'integral_codegree_results.json').write_text(json.dumps(records, indent=2)+'\n')
    (here/'integral_profiles.json').write_text(json.dumps(profiles, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'integral_profiles_checked': len(profiles),
                      'exclusions': [{'id': r['id'], 'factor': r['certificate']['irreducible_factor']}
                                     for r in records]}))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Unbounded NG(C_n,n) dimension and one-operation construction-family audit."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sympy as sp

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
IDS = [65,436,439,455,567,721,731,901,903,921,925,926,928,941,982,985,
       1055,1154,1203,1350,1463,1615,1617,1660,1661,1739,1768,1795,
       2842,2885,3258,3344,3413,3472]


def require(test, message):
    if not test:
        raise ValueError(message)


def fp_polynomial(R):
    """Casimir Perron root is FPdim; isolate its irreducible factor exactly."""
    matrices = [sp.Matrix(M) for M in R]
    dual = [next(j for j in range(8) if R[i][j][0]) for i in range(8)]
    require(all(matrices[dual[i]] == matrices[i].T for i in range(8)),
            'Frobenius reciprocity matrix convention')
    casimir = sum((M*M.T for M in matrices), sp.zeros(8))
    require(casimir == casimir.T and all(v >= 0 for v in casimir), 'Casimir positivity')
    characteristic = casimir.charpoly().as_poly()
    factors = sp.factor_list(characteristic)[1]
    roots = []
    for polynomial, multiplicity in factors:
        intervals = polynomial.intervals(eps=sp.Rational(1, 10000))
        require(sum(m for _, m in intervals) == polynomial.degree(), 'Casimir nonreal root')
        for interval, root_multiplicity in intervals:
            roots.append((interval, polynomial, multiplicity*root_multiplicity))
    roots.sort(key=lambda x: x[0][0])
    interval, polynomial, _ = roots[-1]
    require(all(a[0][1] < interval[0] for a in roots[:-1]), 'Perron root interval overlap')
    return ([str(v) for v in polynomial.monic().all_coeffs()],
            [str(v) for v in interval])


def source_data(row):
    R = row['tensor']
    sha = hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest()
    require(sha == row['tensor_sha256'], 'source SHA mismatch')
    polynomial, interval = fp_polynomial(R)
    dual = [next(j for j in range(8) if R[i][j][0]) for i in range(8)]
    inv = [i for i in range(8) if sum(R[i][dual[i]]) == 1]
    abelian = all(R[g][h] == R[h][g] for g in inv for h in inv)
    return {'id': row['id'], 'tensor_sha256': sha,
            'FP_global_dimension_minimal_polynomial': polynomial,
            'largest_real_root_isolating_interval': interval,
            'invertible_count': len(inv), 'invertibles_abelian': abelian,
            'general_complex_exclusion_claimed_by_this_audit': False}


def analyze(row):
    out = source_data(row)
    polynomial = [sp.Rational(v) for v in out['FP_global_dimension_minimal_polynomial']]
    degree = len(polynomial)-1
    routes = {'direct_or_Morita_equivalent_to_NG': 'excluded',
              'group_extension_of_NG': 'excluded',
              'equivariantization_of_NG': 'excluded',
              'neutral_component_of_nontrivially_graded_NG': 'excluded',
              'deequivariantization_of_NG': 'excluded'}
    out['routes'] = routes
    if degree != 2:
        out['rational_scaling_outcome'] = 'impossible_by_minimal_polynomial_degree'
        return out
    trace, norm = -polynomial[1], polynomial[2]
    n = sp.cancel(trace**2/norm-4)
    out.update({'quadratic_trace': str(trace), 'quadratic_norm': str(norm),
                'only_possible_group_order_n': str(n)})
    if not n.is_Integer or n <= 0:
        out['rational_scaling_outcome'] = 'impossible_n_not_positive_integer'
        return out
    scale = sp.cancel(trace/(n*(n+4)))
    require(scale > 0, 'nonpositive FP scaling')
    require(sp.cancel(scale**2*n**2*(n+4)-norm) == 0, 'scaled norm')
    require([sp.Integer(1), -scale*n*(n+4), scale**2*n**2*(n+4)] == polynomial,
            'scaled minimal polynomial')
    k = sp.cancel(1/scale)
    out.update({'rational_scaling_outcome': 'unique_n_and_scale',
                'scale_target_over_NG': str(scale), 'reciprocal_scale': str(k),
                'NG_minimal_polynomial': ['1',str(-n*(n+4)),str(n*n*(n+4))]})
    if scale == 1:
        routes['direct_or_Morita_equivalent_to_NG'] = 'not_excluded_by_dimension'
    if scale.is_Integer:
        # In this baseline only the independently generally excluded R436 remains.
        require(row['id'] == 'R8_3_436' and scale == 2 and n == 3,
                'new positive-integer scaling requires categorical analysis')
        routes['group_extension_of_NG'] = 'excluded_by_independent_R436_general_TPE_proof'
        routes['equivariantization_of_NG'] = 'excluded_by_independent_R436_general_TPE_proof'
        out['independent_proof'] = 'r436_general_tpe.json'
    if k.is_Integer:
        require(k > 1, 'unexpected same-dimension case')
        details = {'required_group_order': int(k), 'required_cyclic_group': True,
                   'order_divides_n': n % k == 0}
        out['deequivariantization_constraints'] = details
        if n % k != 0:
            details['obstruction'] = 'cyclic_Tannakian_order_does_not_divide_n'
        else:
            rank = n//k+k
            invertibles = n//k
            details.update({'required_rank': int(rank),
                            'required_invertible_count': int(invertibles),
                            'required_invertible_group': 'cyclic'})
            if rank != 8:
                details['obstruction'] = 'rank_mismatch'
            elif invertibles != out['invertible_count']:
                details['obstruction'] = 'invertible_count_mismatch'
            elif not out['invertibles_abelian']:
                details['obstruction'] = 'cyclic_invertibles_required_but_source_nonabelian'
            else:
                raise ValueError('New surviving deequivariantization route requires further work')
    require(all(value.startswith('excluded') for value in routes.values()),
            'a route survived the stated audit')
    return out


def record():
    rows = json.loads((REPO/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())
    sources = {row['id']: row for row in rows}
    ledger = json.loads((REPO/'supplements/rank8/output/m3/ledger.json').read_text())
    expected = {f'R8_3_{i}' for i in IDS}
    baseline = {r['id'] for r in ledger if r['multiplicity'] == 3 and r['status'] == 'unresolved'}
    require(baseline == expected, 'published baseline34 changed')
    # Recheck the separate categorical exclusion used in the sole upward-scaling row.
    spec = importlib.util.spec_from_file_location('frontier_r436_tpe', HERE/'r436_general_tpe.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    require(module.record() == json.loads((HERE/'r436_general_tpe.json').read_text()),
            'independent R436 general proof receipt')
    return {'schema': 'rank8-frontier-infinite-near-group-family-v1',
            'proof': 'NEAR_GROUP_SCALING.md',
            'family': 'all complex NG(C_n,n), all positive integers n; includes the cyclic TPE construction',
            'parameter_bound': None,
            'scope': 'direct/Morita dimension and the five listed single-operation routes only; no arbitrary chains',
            'certificates': [analyze(sources[f'R8_3_{i}']) for i in IDS]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    actual = record()
    target = HERE/'near_group_scaling.json'
    if args.write:
        target.write_text(json.dumps(actual, indent=2)+'\n')
    else:
        require(actual == json.loads(target.read_text()), 'saved near-group audit differs')
    print('PASS: all34 baseline tensors; unbounded NG(C_n,n) dimension and five one-operation routes excluded.')


if __name__ == '__main__':
    main()

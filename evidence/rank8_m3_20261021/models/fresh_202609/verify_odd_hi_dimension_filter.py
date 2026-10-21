"""Exact family-specific Morita filters for the September 2026 HI papers.

Default: regenerate in memory and compare the deterministic receipt read-only.
--write: explicitly replace the receipt. No categorification status is changed.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sympy as s

HERE = Path(__file__).resolve().parent
PIPELINE = HERE.parent.parent / 'pipeline'
RECEIPT = HERE / 'odd_hi_dimension_filter.json'
X = s.Symbol('x')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def tensor_sha(tensor):
    return hashlib.sha256(json.dumps(tensor, separators=(',', ':')).encode()).hexdigest()


def coefficients(polynomial):
    return [int(a) for a in polynomial.all_coeffs()]


def derive():
    census = {r['id']: r for r in json.loads((PIPELINE / 'census_m3.json').read_text())}
    profiles = json.loads((PIPELINE / 'survivor_profiles.json').read_text())
    require(len(profiles) == 277 and len({r['id'] for r in profiles}) == 277,
            'expected the frozen 277 baseline survivors')
    records = []
    exceptional_spectral_matches = []
    for profile in profiles:
        row = census[profile['id']]
        R = row['tensor']
        require(tensor_sha(R) == row['tensor_sha256'] == profile['tensor_sha256'],
                'source tensor binding: ' + row['id'])
        require(len(R) == 8 and all(len(a) == 8 and all(len(b) == 8 for b in a) for a in R),
                'rank-eight tensor shape')
        dual = []
        for i in range(8):
            candidates = [j for j in range(8) if R[i][j][0]]
            require(len(candidates) == 1, 'unique dual')
            dual.append(candidates[0])
        require(all(R[i][j][0] == int(j == dual[i]) for i in range(8) for j in range(8)),
                'dual coefficient normalization')
        matrices = [s.Matrix(a) for a in R]
        require(all(matrices[dual[i]] == matrices[i].T for i in range(8)),
                'based-ring transpose identity')
        C = sum((matrices[i] * matrices[dual[i]] for i in range(8)), s.zeros(8))
        require(C == C.T and all(v >= 0 for v in C), 'nonnegative symmetric Casimir')
        cp = C.charpoly(X).as_poly()
        upper = int(max(sum(C[i, j] for j in range(8)) for i in range(8)))
        lower = int(max(C[i, i] for i in range(8)))
        families = []
        for family, power in [('odd_Haagerup_Izumi_and_all_Morita_duals', 3),
                              ('specified_near_group_and_all_Morita_duals', 4)]:
            tests = []
            n = 3
            while n ** power < upper:
                scale = 1 if power == 3 else n
                trace = scale * n * (n * n + 4)
                norm = scale * scale * n * n * (n * n + 4)
                p = s.Poly(X * X - trace * X + norm, X)
                require(p.is_irreducible, 'irreducible target dimension polynomial')
                rem = cp.rem(p)
                test = {'odd_order': n, 'dimension_polynomial': coefficients(p),
                        'casimir_remainder': coefficients(rem)}
                if not rem.is_zero:
                    test['witness'] = 'target_dimension_is_not_a_Casimir_eigenvalue'
                else:
                    # Both target roots are positive, hence the target FPdim is
                    # strictly below their sum. A symmetric matrix has spectral
                    # radius at least any diagonal entry. This detects the one
                    # lower-eigenvalue coincidence without numerical roots.
                    require(lower >= trace, 'unresolved possible family match: ' + row['id'])
                    test.update(witness='Casimir_spectral_radius_exceeds_target_dimension',
                                source_diagonal_lower_bound=lower,
                                strict_target_upper_bound=trace)
                    exceptional_spectral_matches.append({'id': row['id'], 'family': family,
                                                         'odd_order': n})
                tests.append(test)
                n += 2
            require(n ** power >= upper, 'infinite-tail dimension bound')
            families.append({'family': family, 'outcome': 'specific_family_Morita_model_excluded',
                             'tested_odd_orders': tests,
                             'all_larger_odd_orders': {'first_order': n,
                                 'strict_target_lower_bound': n ** power,
                                 'source_upper_bound': upper}})
        records.append({'id': row['id'], 'tensor_sha256': row['tensor_sha256'],
                        'scope': 'specific_model_families_only_not_categorification_exclusion',
                        'outcome': 'no_model_from_either_tested_family',
                        'source_dual': dual, 'casimir_matrix': [[int(v) for v in C.row(i)] for i in range(8)],
                        'casimir_characteristic_polynomial': coefficients(cp),
                        'global_dimension_upper_bound': upper,
                        'global_dimension_diagonal_lower_bound': lower,
                        'families': families})
    # Rank-eight candidate in the classified unitary Q-system HI Morita class:
    # subgroup duals have rank 2N; the Q-dual has rank N+1. N is odd >=3.
    r = 3
    N_eta = s.zeros(8)
    N_eta[0, 1] = N_eta[1, 0] = 1
    N_eta[1, 1] = 1
    for i in range(2, 8):
        N_eta[1, i] = N_eta[i, 1] = 1
    for i in range(r):
        for j in range(r):
            N_eta[2+i, 2+j] = 1 - int(i == j)
            N_eta[2+i, 5+j] = N_eta[5+j, 2+i] = 1
            N_eta[5+i, 5+j] = 1 + int(i == j)
    d = (7 + s.sqrt(53)) / 2
    dims = s.Matrix([1, d] + [d-1]*3 + [d+1]*3)
    require(all(s.simplify(v) == 0 for v in N_eta*dims-d*dims), 'order-seven dimension eigenvector')
    D = s.expand(sum(v*v for v in dims))
    require(s.simplify(D-(371+49*s.sqrt(53))/2) == 0, 'order-seven global dimension')
    return {'schema': 'odd_hi_family_dimension_audit_v1',
            'result': 'PASS', 'baseline_records': len(records),
            'source_theorems': [
                {'url': 'https://arxiv.org/html/2609.15986v1', 'author': 'Tzu-Chen Huang',
                 'theorem': 'Theorem 2.1', 'scope': 'spherical and pseudo-unitary existence; universal unitarity not established'},
                {'url': 'https://arxiv.org/html/2609.25185v1',
                 'authors': 'Terry Gannon, Andrew Schopieray, Harshit Yadav',
                 'theorems': 'Theorem A(1),(3); Theorem 4.4; Theorem 6.3',
                 'Morita_classification_hypotheses': 'complex unitary cyclic untwisted HI category of Q-system type'}],
            'formulas': {'d_equation': 'd^2=N*d+1',
                         'HI_global_dimension': 'D=N*(1+d^2)',
                         'HI_dimension_minimal_polynomial': 'x^2-N*(N^2+4)*x+N^2*(N^2+4)',
                         'near_group_global_dimension': 'N*D',
                         'near_group_dimension_minimal_polynomial': 'x^2-N^2*(N^2+4)*x+N^4*(N^2+4)',
                         'tail_proof': 'D>N^3 and N*D>N^4 for every N>=3; source FPdim<=maximum Casimir row sum'},
            'classified_Morita_ranks': {'subgroup_dual_fusion_category': '2*N',
                                        'Q_dual_fusion_category': 'N+1',
                                        'subgroup_module_category_do_not_confuse_with_dual': '2*[G:H]'},
            'rank8_classified_Q_dual': {'odd_order': 7,
                'dimensions': ['1','d','d-1','d-1','d-1','d+1','d+1','d+1'],
                'd': '(7+sqrt(53))/2', 'global_dimension': '(371+49*sqrt(53))/2',
                'global_dimension_minimal_polynomial': [1,-371,2597],
                'eta_fusion_matrix': [[int(v) for v in N_eta.row(i)] for i in range(8)]},
            'lower_spectral_coincidences_not_models': exceptional_spectral_matches,
            'scope': 'No baseline tensor is Morita equivalent to either specified family; no general nonexistence conclusion, and no assertion about extensions, equivariantizations beyond the specified near-group construction, or other HI-like categories.',
            'records': records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    data = derive()
    if args.write:
        RECEIPT.write_text(json.dumps(data, indent=2) + '\n')
    else:
        require(data == json.loads(RECEIPT.read_text()), 'receipt differs from exact recomputation')
    print(json.dumps({'result': 'PASS', 'baseline_records': data['baseline_records'],
                      'families_per_record': 2, 'model_matches': 0,
                      'mode': 'write' if args.write else 'read_only_replay'}))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Exact bounded structural-family obstructions; no general exclusion."""
from pathlib import Path
import argparse
import hashlib
import itertools
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SHAS = {
65: 'fb2d70fa36311b2092190eb1ecd5e3e82fd4ab7ff646b11aa7c7e518d261a1c4',
439: 'dd40ef78c0af51291aedd91134123f7177c18cc9de9c9d3b039a6308bb340791',
567: '0efab5b3d7571872f46dd6ccc95c4b228123b252062d758318ee51834288ef4d',
901: 'db5e92bdf7d58c0fcdb4517e6f2201db1937ec33ea6a2f371a8e257dd2fa6472',
1463: '47d803231764fd5ec1f470d927188f71904f5b80938aa3aef8e53b6d08202844',
}

def require(test, message):
    if not test:
        raise ValueError(message)

def digest(R):
    return hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest()

def closure(R, subset):
    S = set(subset) | {0}
    while True:
        T = S | {k for i in S for j in S for k, c in enumerate(R[i][j]) if c}
        if T == S:
            return sorted(S)
        S = T

def analyze(ident, R):
    require(digest(R) == SHAS[ident], 'source hash mismatch')
    dual = [next(j for j in range(8) if R[i][j][0]) for i in range(8)]
    inv = [i for i in range(8) if sum(R[i][dual[i]]) == 1]
    adjoint = closure(R, {k for i in range(8) for k, c in enumerate(R[i][dual[i]]) if c})
    require(adjoint == list(range(8)), 'unexpected proper adjoint subcategory')
    out = {'id': f'R8_3_{ident}', 'tensor_sha256': digest(R),
           'general_complex_outcome': 'unresolved',
           'invertibles': inv, 'duality': dual,
           'adjoint_closure': adjoint,
           'nontrivial_faithful_group_extension': 'excluded_by_trivial_universal_grading'}
    if ident in (901, 1463):
        fib = [i for i in range(1, 8) if R[i][i] == [int(k in (0, i)) for k in range(8)]]
        require(len(fib) == 1, 'Fibonacci generator is not unique')
        x = fib[0]
        low = [i for i in range(8) if R[x][i][i] == 0]
        require(len(low) == 4, 'unexpected Fibonacci module rank')
        pairs = []
        for i in low:
            require(sum(R[x][i]) == 1, 'lower member not mapped to a single simple')
            j = R[x][i].index(1)
            require(R[x][j] == [int(k in (i, j)) for k in range(8)], 'not a regular Fib pair')
            pairs.append([i, j])
        require(sorted(sum(pairs, [])) == list(range(8)), 'Fib pairs do not partition basis')
        witnesses = [[i, j, k, R[i][j][k]] for i in low for j in low
                     for k in range(8) if k not in low and R[i][j][k]]
        require(witnesses, 'the proposed complementary basis is closed')
        out.update({'fibonacci_generator': x, 'fibonacci_regular_pairs': pairs,
                    'unique_possible_factor_complement': low,
                    'complement_not_closed_witness': witnesses[0],
                    'plain_fibonacci_deligne_factor': 'excluded',
                    'braided_categorification': 'excluded',
                    'general_factorization_assumed': False})
    else:
        noninv = sorted(set(range(8))-set(inv))
        orbit = sorted({R[g][noninv[0]].index(1) for g in inv})
        require(orbit == noninv, 'not generalized near-group')
        stabilizer = [g for g in inv if R[g][noninv[0]][noninv[0]] == 1]
        table = [[R[g][h].index(1) for h in inv] for g in inv]
        abelian = all(R[g][h] == R[h][g] for g in inv for h in inv)
        out.update({'noninvertibles': noninv, 'invertible_multiplication_table': table,
                    'invertible_action_transitive': True, 'stabilizer': stabilizer,
                    'invertibles_abelian': abelian, 'braided_categorification': 'excluded'})
        if ident in (439, 567):
            require(len(inv) == 6 and len(noninv) == 2 and not abelian, 'wrong S3 profile')
            require(len(stabilizer) == 3, 'wrong C3 stabilizer')
            out['C2_equivariantization_of_any_C3_plus6_category'] = 'excluded_by_orbit_and_invertible_group_counts'
            out['all_order_two_based_actions_on_C3_plus6'] = [
                {'action_on_C3': 'identity', 'equivariantization_rank': 8,
                 'invertibles': 6, 'invertible_group': 'abelian central extension of C3 by C2'},
                {'action_on_C3': 'inversion', 'equivariantization_rank': 5,
                 'invertibles': 2, 'other_dimensions': ['2', 'd', 'd']}]
        else:
            require(len(inv) == 4 and len(noninv) == 4 and abelian and stabilizer == [0],
                    'wrong C4 free-action profile')
            g, rho = 1, 5
            powers = [0]
            for _ in range(3):
                powers.append(R[g][powers[-1]].index(1))
            require(len(set(powers)) == 4, 'invertible group is not C4')
            rho_orbit = [R[h][rho].index(1) for h in powers]
            require([R[rho][rho][i] for i in rho_orbit] == [3, 3, 2, 3], 'wrong quadratic rule')
            require(R[rho][rho][0] == 1 and sum(R[rho][rho]) == 12, 'wrong rho square')
            out.update({'C4_powers': powers, 'rho': rho, 'rho_orbit': rho_orbit,
                        'rho_square_coefficients': [3, 3, 2, 3],
                        'noninvertible_FP_polynomial': [1, -11, -1],
                        'braided_dimension_polynomials_required_by_classification': [[1, -1, -1], [1, -2, -1]],
                        'braided_exclusion_reference': 'Schopieray2212.14009 Theorem1'})
    return out

def record():
    rows = json.loads((REPO/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())
    data = {int(r['id'].rsplit('_',1)[1]):r['tensor'] for r in rows}
    return {'schema': 'rank8-frontier-scoped-structural-v1',
            'proof': 'evidence/rank8_frontier_20261021/structural_models/STRUCTURAL_SCOPE.md',
            'certificates': [analyze(i, data[i]) for i in sorted(SHAS)],
            'scope': 'construction_families_and_braided_only; no_general_exclusion'}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    actual = record()
    target = HERE/'structural_scope.json'
    if args.write:
        target.write_text(json.dumps(actual, indent=2)+'\n')
    else:
        require(actual == json.loads(target.read_text()), 'saved scope receipt differs')
    print('PASS: five exact source-bound structural audits; all remain general-complex unresolved.')

if __name__ == '__main__':
    main()

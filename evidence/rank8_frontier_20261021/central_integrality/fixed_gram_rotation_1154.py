"""Exact joint rotation and STS tests on every filtered integral R1154 Gram.

All patterns share one matrix. Exact primal affine families and Farkas rays
may certify many right hand sides at once. Numerical solver outputs alone
are never accepted. Feasibility is only a necessary-condition result.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'noncommutative'))
import character_modular as modular
import certified_lp
import integral_gram

c = modular.c
s = c.s


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def setup(height):
    modular.full.base.install()
    domain = json.loads((HERE / 'integer_gram_1154.json').read_text())
    filtered = json.loads((c.HERE / 'central_integral_filters_1154.json').read_text())
    source = next(r for r in json.loads((c.OLD.parent / 'pipeline/census_m3.json').read_text())
                  if r['id'] == domain['id'])
    need(source['tensor_sha256'] == domain['tensor_sha256'] == filtered['tensor_sha256'], 'Tensor binding')
    R = source['tensor']
    a = c.w.data(R)
    cols = a['lows'][31]
    need([list(v) for v in cols] == domain['low_columns'], 'Low frame identity')
    indicators = (0, 0, -1, 1, 1, 1, 1)
    need(indicators in list(map(tuple, modular.full.h.indicator_choices(R))), 'Allowed full indicator assignment')
    permutation = (0, 1, 2, 3, 4)
    need(modular.assignments(a, modular.characters(R, a), cols) == [permutation], 'Complete character assignment')
    L = s.Matrix.hstack(*map(s.Matrix, cols))
    high = modular.full.base.grams.high_columns(a, L)[1]
    need([list(v) for v, dimension in high] == domain['high_columns'], 'Ordered high restriction domain identity')
    A, b, meta = modular.full.system(R, a, L, indicators, height)
    A, b, meta = modular.append_sts(R, a, cols, permutation, A, b, meta, height)
    count_rows = len(domain['high_columns'])
    A, unused = integral_gram.append_multiplicities(A, b, [0] * count_rows, meta['trace_types'])
    ids = filtered['combined_survivor_indices']
    counts = {i: domain['completions'][i] for i in ids}
    base = ids[0]
    difference = s.Matrix.hstack(*(s.Matrix(counts[i]) - s.Matrix(counts[base]) for i in ids[1:]))
    pivot_columns = list(difference.rref()[1])
    affine_ids = [ids[j + 1] for j in pivot_columns]
    basis = difference[:, pivot_columns]
    rows = list(basis.T.rref()[1])
    inverse = basis[rows, :].inv()
    coordinates = {i: list(inverse * (s.Matrix(counts[i]) - s.Matrix(counts[base]))[rows, :]) for i in ids}
    for i in ids:
        need(s.Matrix(counts[base]) + basis * s.Matrix(coordinates[i]) == s.Matrix(counts[i]), 'Complete affine Gram coordinates')
    B = s.Matrix.hstack(s.Matrix(b + counts[base]),
                        *(s.Matrix([0] * len(b) + [counts[i][j] - counts[base][j] for j in range(count_rows)])
                          for i in affine_ids))
    metadata = {'id': source['id'], 'tensor_sha256': source['tensor_sha256'], 'height': height,
                'low_index': 31, 'indicators': list(indicators), 'character_assignment': list(permutation),
                'system': meta, 'matrix_sha256': digest(A), 'constant_rhs_sha256': digest(b),
                'gram_domain_sha256': digest(domain), 'filtered_domain_sha256': digest(filtered),
                'pattern_indices': ids, 'affine_base_index': base, 'affine_basis_indices': affine_ids,
                'affine_rank': len(affine_ids), 'scope': 'pseudo_unitary_necessary_conditions'}
    return A, b, counts, coordinates, B, metadata


def family_weights(matrix, coordinates):
    return matrix[:, 0] + matrix[:, 1:] * s.Matrix(coordinates)


def verify_case(A, b, counts, coordinates, B, case):
    ids = case['pattern_indices']
    need(ids and len(ids) == len(set(ids)), 'Nonempty unique case domain')
    if case['kind'] == 'farkas_family':
        y = case['ray']
        need(len(y) == len(A) and all(isinstance(v, int) for v in y), 'Integer full Farkas ray')
        need(all(sum(row[j] * value for row, value in zip(A, y)) >= 0 for j in range(len(A[0]))), 'Common matrix separator')
        for i in ids:
            need(sum(x * z for x, z in zip(b + counts[i], y)) < 0, 'Family strict separation')
    elif case['kind'] == 'primal_affine_family':
        support = case['support']
        need(len(support) == len(set(support)) and all(0 <= j < len(A[0]) for j in support), 'Valid support')
        matrix = s.Matrix([[s.Rational(v) for v in row] for row in case['affine_weights']])
        C = s.Matrix([[row[j] for j in support] for row in A])
        residual = C * matrix - B
        for i in ids:
            need(all(v >= 0 for v in family_weights(matrix, coordinates[i])), 'Nonnegative family primal')
            need(not any(family_weights(residual, coordinates[i])), 'Exact affine primal equations for each pattern')
    elif case['kind'] == 'individual_primal':
        need(len(ids) == 1, 'Individual primal domain')
        certified_lp.verify(A, b + counts[ids[0]], case['decision'])
        need(case['decision']['status'] == 'exact_feasible_relaxation', 'Actual exact primal required')
    else:
        raise ValueError('Unknown family certificate')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--height', type=int, default=6)
    args = parser.parse_args()
    A, b, counts, coordinates, B, meta = setup(args.height)
    path = HERE / ('fixed_gram_rotation_1154_h' + str(args.height) + '.json')
    if not args.write:
        saved = json.loads(path.read_text())
        need(saved['metadata'] == meta, 'Complete system and domain identity')
        covered = []
        for case in saved['cases']:
            verify_case(A, b, counts, coordinates, B, case)
            covered.extend(case['pattern_indices'])
        need(len(covered) == len(set(covered)), 'Disjoint coverage')
        need(sorted(covered + saved['unresolved_indices']) == meta['pattern_indices'], 'Complete pattern accounting')
        need(saved['complete'] == (not saved['unresolved_indices']), 'Honest completion status')
        print('PASS R1154 fixed Gram joint rotation/STS:', len(covered), 'certified;', len(saved['unresolved_indices']), 'unresolved')
        return
    remaining = set(meta['pattern_indices'])
    out = {'metadata': meta, 'cases': [], 'complete': False,
           'unresolved_indices': sorted(remaining), 'conclusion': 'Necessary constraints only; no model or exclusion asserted.'}
    if path.exists():
        old = json.loads(path.read_text())
        need(old['metadata'] == meta, 'Resume domain unchanged')
        for case in old['cases']:
            verify_case(A, b, counts, coordinates, B, case)
            need(set(case['pattern_indices']) <= remaining, 'Disjoint resumed cases')
            remaining.difference_update(case['pattern_indices'])
        out = old
    def save():
        out['unresolved_indices'] = sorted(remaining)
        out['complete'] = not remaining
        path.write_text(json.dumps(out, indent=2) + '\n')
    save()
    while remaining:
        i = min(remaining)
        decision = certified_lp.decide(A, b + counts[i])
        if decision['status'] == 'exact_infeasible_relaxation':
            y = decision['ray']
            covered = sorted(j for j in remaining if sum(x * z for x, z in zip(b + counts[j], y)) < 0)
            case = {'kind': 'farkas_family', 'pattern_indices': covered, 'ray': y}
        elif decision['status'] == 'exact_feasible_relaxation':
            support = [j for j, value in decision['primal']]
            C = s.Matrix([[row[j] for j in support] for row in A])
            family = None
            independent_rows = list(C.T.rref()[1])
            if len(independent_rows) == len(support):
                family = C[independent_rows, :].inv() * B[independent_rows, :]
            residual = C * family - B if family is not None else None
            covered = sorted(j for j in remaining
                             if not any(family_weights(residual, coordinates[j]))
                             and all(v >= 0 for v in family_weights(family, coordinates[j]))) if family is not None else []
            if covered:
                case = {'kind': 'primal_affine_family', 'pattern_indices': covered,
                        'support': support, 'affine_weights': [[str(x) for x in row] for row in family.tolist()]}
            else:
                case = {'kind': 'individual_primal', 'pattern_indices': [i], 'decision': decision}
        else:
            out['stopped_decision'] = decision
            save()
            print('INCOMPLETE:', i, decision['status'], flush=True)
            return
        verify_case(A, b, counts, coordinates, B, case)
        out['cases'].append(case)
        remaining.difference_update(case['pattern_indices'])
        save()
        print('R1154', case['kind'], 'covered', len(case['pattern_indices']), 'remaining', len(remaining), flush=True)
    print('COMPLETE R1154 fixed Gram joint rotation/STS', len(out['cases']), 'exact families', flush=True)


if __name__ == '__main__':
    main()

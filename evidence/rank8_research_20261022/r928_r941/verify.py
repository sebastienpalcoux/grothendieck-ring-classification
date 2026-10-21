#!/usr/bin/env python3
"""Exact small audit for the semion/fermion braided-Morita obstructions.

This rechecks arithmetic and counts; the frozen source completeness and the
general Galois-PU reduction are dependencies, not rerun here.
"""
import argparse
import hashlib
import json
from fractions import Fraction as F
from math import isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FRONT = Path('evidence/rank8_frontier_20261021')
ZERO = (F(0),) * 4
ONE = (F(1), F(0), F(0), F(0))
EXPECTED_HASHES = {
    'R8_3_928': '94dfb90235dbb3ba95864a1be23437943ea3b1316ec82ca44baf419262890614',
    'R8_3_941': '8ae4007492dee167ab8b3f4f16310ee368482da03696e20ed7cceea34bec64e6',
}
FINAL_ALLOCATIONS = [8, 19, 21, 31, 34, 43, 45, 56, 60, 72, 73, 77, 79, 85]


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(c, a):
    return tuple(c * x for x in a)


def mul(a, b):
    # Basis: 1,sqrt(2),sqrt(3),sqrt(6); xor multiplies squarefree parts.
    out = list(ZERO)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i ^ j] += x * y * (2 if i & j & 1 else 1) * (3 if i & j & 2 else 1)
    return tuple(out)


def field_sum(values):
    out = ZERO
    for a in values:
        out = add(out, a)
    return out


def polynomial_and_norm(d):
    conjugates = [tuple(x * (-1 if (mask & i).bit_count() % 2 else 1)
                        for i, x in enumerate(d)) for mask in range(4)]
    need(len(set(conjugates)) == 4, 'global dimension must have degree four')
    coefficients = [ONE]  # descending coefficients
    for value in conjugates:
        result = [ZERO] * (len(coefficients) + 1)
        for i, coefficient in enumerate(coefficients):
            result[i] = add(result[i], coefficient)
            result[i + 1] = add(result[i + 1], scale(-1, mul(coefficient, value)))
        coefficients = result
    need(all(c[1:] == ZERO[1:] and c[0].denominator == 1 for c in coefficients),
         'Galois product must be a rational integral polynomial')
    integers = [int(c[0]) for c in coefficients]
    return integers, integers[-1]


def ring_audit(row, orbit, gram):
    tensor = row['tensor']
    n = len(tensor)
    digest = hashlib.sha256(json.dumps(tensor, separators=(',', ':')).encode()).hexdigest()
    need(digest == row['tensor_sha256'] == EXPECTED_HASHES[row['id']], 'tensor binding')
    dims = [tuple(F(x) for x in v) for v in row['full_characters'][0]]
    need(all(all(x >= 0 for x in d) and any(x > 0 for x in d) for d in dims),
         'positive dimension character')
    for i in range(n):
        for j in range(n):
            need(mul(dims[i], dims[j]) == field_sum(scale(tensor[i][j][k], dims[k])
                                                  for k in range(n)), 'dimension character')
    dual = []
    for i in range(n):
        partners = [j for j in range(n) if tensor[i][j][0]]
        need(len(partners) == 1 and tensor[i][partners[0]][0] == 1, 'simple dual')
        dual.append(partners[0])
    unit = [1] + [0] * (n - 1)
    invertibles = [i for i in range(n) if tensor[i][dual[i]] == unit]
    need(invertibles == [i for i, d in enumerate(dims) if d == ONE], 'dimension-one criterion')
    need(invertibles == [0, orbit['source_g']], 'two source invertibles')
    adjoint = {0} | {k for i in range(n) for k, a in enumerate(tensor[i][dual[i]]) if a}
    while True:
        enlarged = adjoint | {dual[i] for i in adjoint}
        enlarged |= {k for i in adjoint for j in adjoint for k, a in enumerate(tensor[i][j]) if a}
        if enlarged == adjoint:
            break
        adjoint = enlarged
    need(adjoint == set(range(n)), 'full adjoint subring')
    # Independently locate and count pure-g restrictions in all 343 patterns.
    high = [[0] + v for v in row['canonical_high_vectors']]
    g_vector = [int(i == orbit['source_g']) for i in range(n)]
    g_indices = [i for i, v in enumerate(high) if v == g_vector]
    need(g_indices == [40], 'unique high restriction of the source invertible')
    need(all(pattern[40] == 1 for pattern in gram['patterns']), 'one central g in every pattern')
    need([i for i, v in enumerate(row['low_columns']) if v == unit] == [0], 'unique low pure unit')
    need(all(v[0] == 0 for v in high), 'high columns have zero unit coefficient')
    need(orbit['central_g_multiplicity'] == 1 and orbit['kernel_pure_unit_only'], 'frozen lift receipt')
    translated = []
    for low in row['low_columns']:
        gv = [sum(low[j] * tensor[orbit['source_g']][j][k] for j in range(n)) for k in range(n)]
        matches = [i for i, h in enumerate(high) if h == gv]
        need(len(matches) == 1, 'unique translated low column')
        translated.append(matches[0])
    need(translated == orbit['low_translated_high_indices'] == [40, 41, 42, 43, 57], 'translations')
    need(all(all(p[i] == 1 for i in translated) for p in gram['patterns']), 'known translated simples')
    d = field_sum(mul(x, x) for x in dims)
    polynomial, norm = polynomial_and_norm(d)
    need(d == tuple(map(F, [144, 96, 80, 56])), 'global dimension')
    need(polynomial == [1, -576, 11520, -73728, 147456], 'minimal polynomial')
    proper_closed = []
    for bits in range(1 << (n - 1)):
        subset = {0} | {i for i in range(1, n) if bits & (1 << (i - 1))}
        if len(subset) == n or any(dual[i] not in subset for i in subset):
            continue
        if all(not tensor[i][j][k] for i in subset for j in subset for k in range(n) if k not in subset):
            proper_closed.append(sorted(subset))
    need(all(set(s) <= set(invertibles) for s in proper_closed), 'every proper subring pointed')
    return {
        'id': row['id'], 'tensor_sha256': digest, 'source_invertibles': invertibles,
        'source_adjoint_indices': sorted(adjoint), 'proper_closed_subrings': proper_closed,
        'global_dimension_basis_1_sqrt2_sqrt3_sqrt6': list(map(int, d)),
        'global_dimension_minimal_polynomial': polynomial, 'global_dimension_norm': norm,
        'pure_g_column': 40, 'central_g_count_in_each_of_343_patterns': 1,
        'translated_low_columns': translated,
    }


def run():
    hashes = {}

    def read(path):
        path = Path(path)
        data = (ROOT / path).read_bytes()
        hashes[str(path)] = hashlib.sha256(data).hexdigest()
        return json.loads(data)

    source = read(FRONT / 'quartic_integer_center/source.json')
    census = read('evidence/rank8_m3_20261021/pipeline/census_m3.json')
    census = {x['id']: x for x in census if x['id'] in EXPECTED_HASHES}
    gates = {x['id']: x for x in read(FRONT / 'noncommutative_followup/general_galois_pu_gate.json')}
    orbit_receipt = read(FRONT / 'review/quartic_central_orbits.json')
    orbits = {x['id']: x for x in orbit_receipt['records']}
    gram = read(FRONT / 'quartic_integer_center/gram_cubic.json')
    fermion = read(FRONT / 'quartic_integer_center/r941_fermionic.json')
    charge = read(FRONT / 'quartic_integer_center/r941_charges.json')
    traces = read(FRONT / 'review/r941_fusion_traces.json')
    need(len(gram['patterns']) == gram['complete_joint_pattern_count'] == 343, 'complete Gram audit')
    rows = []
    for row in source['records']:
        name = row['id']
        need(row['tensor'] == census[name]['tensor'], 'match canonical census tensor')
        need(gates[name]['outcome'] == 'Galois_pseudo_unitary_reduction', 'general reduction outcome')
        need(gates[name]['scope'] == 'general_complex_fusion_category', 'general reduction scope')
        need(gates[name]['tensor_sha256'] == row['tensor_sha256'] == orbits[name]['tensor_sha256'], 'gate bindings')
        rows.append(ring_audit(row, orbits[name], gram))
    need(orbits['R8_3_928']['central_twist_squared'] == -1, 'semionic lift')
    need(orbits['R8_3_941']['central_twist_squared'] == 1, 'R941 lift self-monodromy')
    need(fermion['tensor_sha256'] == EXPECTED_HASHES['R8_3_941'], 'fermion tensor binding')
    need(fermion['bosonic_branch']['outcome'] == 'excluded_by_unrestricted_rank_four_bound', 'boson exclusion dependency')
    need(fermion['fermionic_branch']['outcome'] == 'necessary_central_lift_has_twist_minus_one', 'fermionic lift')
    for dep in fermion['bosonic_branch']['dependencies']:
        p = Path(dep['path'])
        digest = hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
        need(digest == dep['sha256'], 'rank-four dependency changed: ' + str(p))
        hashes[str(p)] = digest
    need(traces['paired_surviving_allocations'] == FINAL_ALLOCATIONS, 'frozen survivor list')
    need(len(charge['solutions']) == charge['complete_charge_allocation_count'] == 93, 'complete charge list')
    charges = orbits['R8_3_941']['low_monodromy_charges']
    need(charges == [1, 1, 1, 1, -1], 'known low monodromy charges')
    # The fermion has trivial self-monodromy, so translating preserves charges.
    known_positive = 2 * charges.count(1)
    known_negative = 2 * charges.count(-1)
    allocations = []
    for index in FINAL_ALLOCATIONS:
        solution = charge['solutions'][index]
        pattern = gram['patterns'][solution['pattern_index']]
        plus, minus = solution['plus_pairs'], solution['minus_individuals']
        need(len(plus) == len(minus) == 40, 'charge coordinate count')
        need(all(isinstance(v, int) and v >= 0 for v in plus + minus), 'nonnegative integral counts')
        need([2 * p + m for p, m in zip(plus, minus)] == pattern[:40], 'complete high counts')
        p_rank = known_positive + 2 * sum(plus)
        n_rank = known_negative + sum(minus)
        need(p_rank + n_rank == 5 + sum(pattern), 'complete center rank')
        frozen = traces['cases'][index]
        need(frozen['allocation_index'] == index and frozen['pattern_index'] == solution['pattern_index'], 'allocation indices')
        need(frozen['positive_charge_count'] == p_rank and frozen['negative_charge_count'] == n_rank, 'independent rank check')
        need(p_rank == 22 and isqrt(2 * p_rank) ** 2 != 2 * p_rank, 'rank-square contradiction')
        allocations.append({'allocation_index': index, 'pattern_index': solution['pattern_index'],
                            'known_positive_count': known_positive, 'positive_pair_count': sum(plus),
                            'centralizer_rank': p_rank, 'other_charge_rank': n_rank})
    norm = rows[1]['global_dimension_norm']
    m_values = [m for m in range(1, isqrt(isqrt(norm)) + 1) if norm % m ** 4 == 0]
    need(m_values == [1, 2, 4, 8] and norm == 2 ** 14 * 3 ** 2, 'symmetric-center norm candidates')
    # Actual pointed modular control: Z(sVec) = toric code on C2 x C2.
    group = [(i, j) for i in range(2) for j in range(2)]
    twist = {(i, j): (-1) ** (i * j) for i, j in group}
    f = (1, 1)
    centralizer = [x for x in group if twist[(x[0] ^ f[0], x[1] ^ f[1])] == twist[x] * twist[f]]
    need(centralizer == [(0, 0), (1, 1)] and 2 * len(centralizer) == 2 ** 2, 'actual sVec-center control')
    # Double semion twists 1,i,-i,1 show why the no-boson hypothesis matters.
    double_semion_twists = [[1, 0], [0, 1], [0, -1], [1, 0]]
    need(sum(q == [1, 0] for q in double_semion_twists) == 2, 'double-semion boson control')
    hashes[str(Path(__file__).resolve().relative_to(ROOT))] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return {
        'kind': 'exact_braided_Morita_semion_and_fermion_rank_obstruction_audit',
        'scope': 'no braided Morita representative; general categorification remains unresolved',
        'frozen_completeness_dependency': 'Galois-PU gate and complete center audits are bound, not rerun',
        'source_rings': rows,
        'r941_all_remaining_allocations': allocations,
        'r941_symmetric_center_order_norm_candidates': m_values,
        'r941_required_braided_representative_rank_squared': 44,
        'r941_rank_square_obstruction': True,
        'controls': {'sVec_rank': 2, 'Z_sVec_fermion_centralizer_rank': len(centralizer),
                     'double_semion_nonidentity_twist_one_invertibles': 1},
        'dependencies_sha256': dict(sorted(hashes.items())),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='write the deterministic receipt')
    args = parser.parse_args()
    result = run()
    path = HERE / 'verification.json'
    if args.write:
        path.write_text(json.dumps(result, indent=2) + '\n')
    else:
        need(result == json.loads(path.read_text()), 'verification receipt differs')
    print('PASS: both source rings; 343 central-lift counts; all 14 R941 centralizer ranks 22; rank-square obstruction; controls.')


if __name__ == '__main__':
    main()

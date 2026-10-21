"""Independent R455 integer-pattern and explicit joint-separator audit.

The established restriction-domain and joint-operator constructors are
shared. Integer multiplicities are enumerated independently by dynamic
programming; cubic coefficients use the direct S-matrix formula; the full
separator is checked without the producer's LP verifier or solver.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import sys

HERE = Path(__file__).resolve().parent
PRODUCER = HERE.parent / 'r455_center_integer'
sys.path.insert(0, str(PRODUCER))
import joint_rotation as joint


def need(value, message):
    if not value:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def patterns(Q, high):
    """Coefficient extraction of finite outer-product generating functions."""
    coordinate_blocks = ((0, 2), (3, 4))
    domains = []
    covered = []
    for coordinates in coordinate_blocks:
        first, second = coordinates
        block = [i for i, (v, z) in enumerate(high)
                 if (v[first] or v[second]) and
                 not any(v[j] for j in (coordinate_blocks[1] if coordinates == coordinate_blocks[0]
                                       else coordinate_blocks[0]))]
        covered.extend(block)
        target = (int(Q[first + 1, first + 1]), int(Q[first + 1, second + 1]),
                  int(Q[second + 1, second + 1]))
        states = {(0, 0, 0): [()]}
        for index in block:
            v = high[index][0]
            form = (v[first] ** 2, v[first] * v[second], v[second] ** 2)
            bound = min(goal // coefficient for goal, coefficient in zip(target, form)
                        if coefficient)
            next_states = {}
            for state, prefixes in states.items():
                for multiplicity in range(bound + 1):
                    destination = tuple(x + multiplicity * y for x, y in zip(state, form))
                    if any(x > y for x, y in zip(destination, target)):
                        continue
                    next_states.setdefault(destination, []).extend(
                        prefix + (multiplicity,) for prefix in prefixes)
            states = next_states
        domains.append((block, states.get(target, [])))
    need(sorted(covered) == list(range(len(high))), 'complete disjoint high blocks')
    answers = []
    for left, right in itertools.product(domains[0][1], domains[1][1]):
        counts = [0] * len(high)
        for (block, _), values in zip(domains, (left, right)):
            for index, value in zip(block, values):
                counts[index] = value
        need(all(sum(counts[k] * high[k][0][i] * high[k][0][j]
                     for k in range(len(high))) == Q[i + 1, j + 1]
                 for i in range(7) for j in range(7)), 'full residual Gram')
        answers.append(tuple(counts))
    need(len(answers) == len(set(answers)) == 812, 'complete independent integer count')
    return sorted(answers), [len(values) for block, values in domains]


def compute():
    data = joint.setup()
    R, a, chars, cols, Q, high, basis, coordinates, dimensions, D = data
    K = a['K']
    saved = json.loads((PRODUCER / 'results.json').read_text())
    target = json.loads((PRODUCER / 'joint_rotation.json').read_text())
    need(digest(R) == saved['source']['tensor_sha256'], 'complete tensor binding')
    need(chars[0] == a['ds'], 'FP character explicitly labels the unit')
    need(a['codegrees'][0] == a['codegrees'][1] == a['D'] and
         a['multiplicities'][0] == a['multiplicities'][1] == 1,
         'equal-codegree reordering preserves all normalizations')
    need(cols[0] == cols[1] == (1, 0, 0, 0, 0, 0, 0, 0),
         'nontrivial distinguished invertible forgets to the unit')
    need(sum(tuple(col) == tuple(cols[0]) for col in cols) == 2,
         'precisely two simples in the invertible forgetful kernel')
    need(all(ch[i] == ch[a['du'][i]] for ch in chars for i in range(8)),
         'all distinguished character labels are self-dual')
    integer, block_counts = patterns(Q, high)
    need(integer == [tuple(row['multiplicities']) for row in saved['patterns']],
         'all ordered producer integer patterns independently recovered')
    all_columns = list(cols) + [(0,) + tuple(v) for v, z in high]
    dims = [sum((K(n) * d for n, d in zip(v, a['ds'])), K.zero) for v in all_columns]
    S = [[a['D'] / a['codegrees'][E] / K(a['multiplicities'][E]) *
          sum((K(n) * ch for n, ch in zip(v, chars[E])), K.zero)
          for v in all_columns] for E in range(5)]
    need(S[0] == dims and S[0][0] == K.one, 'direct unit S row normalization')
    need(all(S[E][0] == a['D'] / a['codegrees'][E] for E in range(5)),
         'distinguished central FP dimensions')
    triples = list(itertools.combinations_with_replacement(range(1, 5), 3))
    coefficients = [[S[E][j] * S[F][j] * S[G][j] / dims[j] / a['D'] ** 2
                     for j in range(len(all_columns))] for E, F, G in triples]
    charges = [S[1][j] / dims[j] for j in range(5, len(all_columns))]
    need(all(x in (K.one, -K.one) for x in charges), 'all high monodromy charges')
    negative = [i for i, charge in enumerate(charges) if charge == -K.one]
    cubic_survivors, parity_survivors = [], []
    cubic_digest = hashlib.sha256()
    for index, counts in enumerate(integer):
        weights = [1] * 5 + list(counts)
        values = [sum((K(n) * coefficient for n, coefficient in zip(weights, row)), K.zero)
                  for row in coefficients]
        cubic_digest.update((repr([joint.base.c.ec(x) for x in values]) + '\n').encode())
        good = all(len(x.to_list()) <= 1 and
                   (not x.to_list() or (x.to_list()[0].denominator == 1 and x.to_list()[0] >= 0))
                   for x in values)
        if good:
            cubic_survivors.append(index)
            if all(counts[i] % 2 == 0 for i in negative):
                parity_survivors.append(index)
    need(cubic_survivors == saved['cubic_survivors'] and len(cubic_survivors) == 24,
         'all independent cubic tests')
    need(parity_survivors == saved['all_tests_survivors'] and len(parity_survivors) == 12,
         'complete parity survivors; no spectral rejection needed for this proof')
    need(negative == saved['negative_monodromy_high_indices'], 'complete monodromy parity domain')
    print('PASS independent R455 DP and direct cubic/parity domain: 812 -> 24 -> 12', flush=True)
    indicators = list(joint.base.rotation.h.indicator_choices(R))
    expected = [(index, tuple(ep)) for index in parity_survivors for ep in indicators]
    actual = [(case['pattern_index'], tuple(case['metadata']['indicators'])) for case in target['cases']]
    need(actual == expected and len(expected) == 48, 'complete Cartesian branch coverage')
    common_matrix, common_ray = None, None
    column_minimum, score_hash = None, None
    right_sides = []
    for case in target['cases']:
        index, ep = case['pattern_index'], case['metadata']['indicators']
        A, b, metadata = joint.build(data, integer[index], ep)
        need(metadata == case['metadata'], 'fresh complete joint operator and RHS binding')
        decision = case['decision']
        need(decision['status'] == 'exact_infeasible_relaxation', 'full branch has no exact separator')
        ray = decision['ray']
        need(len(ray) == len(A), 'complete ray dimension')
        if common_matrix is None:
            common_matrix, common_ray = A, ray
            scores = [sum(y * row[j] for y, row in zip(ray, A)) for j in range(len(A[0]))]
            need(all(value >= 0 for value in scores), 'direct full-column Farkas inequalities')
            column_minimum, score_hash = min(scores), digest(scores)
        else:
            need(A == common_matrix and ray == common_ray, 'every branch uses the same checked matrix and ray')
        pairing = sum(y * value for y, value in zip(ray, b))
        need(pairing < 0, 'strict branch-specific exact separation')
        right_sides.append({'pattern': index, 'indicators': ep, 'rhs_pairing': pairing})
    return {'result': 'PASS', 'id': 'R8_3_455', 'scope':
            'complete integer/cubic/parity domain and all joint separators; categorical and trace-domain scope reviewed separately',
            'tensor_sha256': digest(R), 'independent_block_counts': block_counts,
            'integer_patterns': len(integer), 'cubic_survivors': cubic_survivors,
            'parity_survivors': parity_survivors, 'cubic_values_sha256': cubic_digest.hexdigest(),
            'negative_monodromy_indices': negative, 'joint_cases': len(right_sides),
            'joint_rows': len(common_matrix), 'joint_columns': len(common_matrix[0]),
            'minimum_column_pairing': column_minimum, 'all_column_pairings_sha256': score_hash,
            'right_side_checks': right_sides,
            'shared_restriction_and_joint_constructors': True,
            'producer_LP_verifier_used': False,
            'source_sha256': {str(p.relative_to(HERE.parents[2])):
                hashlib.sha256(p.read_bytes()).hexdigest() for p in
                [PRODUCER / name for name in ('verify.py', 'results.json', 'joint_rotation.py', 'joint_rotation.json')]}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    actual = compute()
    path = HERE / 'direct.json'
    if args.write:
        path.write_text(json.dumps(actual, indent=2) + '\n')
    else:
        need(actual == json.loads(path.read_text()), 'independent review receipt differs')
    print('PASS R455 independent integer-domain and full-column audit', flush=True)


if __name__ == '__main__':
    main()

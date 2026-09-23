"""Exact joint low-product Gram test on an existing central-induction witness.

This verifies a stronger necessary-condition witness, NOT a categorification.
The algorithm is independent of the chosen census identifier. It accepts a
complete positive-dimensional character table and a frozen induction witness.
No census enumeration, numerical optimizer, or manual tensor calculations.
"""
import argparse
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'software'))
import sympy as s
import modular_character_induction as induction
from augmented_spectrum import AugmentedSpectrum
from exact import require
from modular_frontier import verify_record


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def integer(z, field, context):
    x = field.to_sympy(z)
    require(x.is_Integer is True and x >= 0, context + ' is not a nonnegative integer')
    return int(x)


def compute(ring, witness):
    # Reconstruct and exactly verify all inherited induction equations first.
    inherited = verify_record(ring, witness)
    data, table = induction.reciprocity_data(ring)
    K = table.K
    n = len(ring)
    low = list(map(tuple, witness['columns']))
    require(len(low) == n and len(set(low)) == n,
            'this implementation requires distinct low restriction vectors')
    require(all(ring[i][i][0] == 1 for i in range(n)),
            'this implementation requires a self-dual input basis')
    # Real character rows imply real S rows for these low central objects.
    # S_{a*,W}=conj(S_{a,W}) and invertibility of S then imply low self-duality.
    require(all(K.to_sympy(z).is_real is True for row in table.rows for z in row),
            'real low-character rows required')
    L = s.Matrix.hstack(*map(s.Matrix, low))
    _, high_domain = induction.high_columns(data, L)
    spectrum = AugmentedSpectrum(table, low, high_domain)
    A, _, meta = induction.system_rotation(ring, data, L, witness['indicators'],
                                           witness['height'])
    labels = meta['labels']
    forbidden = set(map(tuple, spectrum.forbidden))
    keep = [j for j in range(len(A[0]))
            if j >= len(labels) or tuple(labels[j][0]) not in forbidden]
    counts = {v: 1 for v in low}
    for j, k in enumerate(keep):
        z = Fraction(witness['solution'][j])
        if k < len(labels) and z:
            require(z.denominator == 1 and z > 0, 'high multiplicity not a positive integer')
            v = (0,) + tuple(labels[k][0])
            counts[v] = counts.get(v, 0) + z.numerator
    types = dict(zip(spectrum.vectors, spectrum.types))
    labelling = witness['labelling']
    pairs = list(itertools.combinations_with_replacement(range(1, n), 2))

    def moment(objects):
        return sum((K(count) * math.prod(types[v][labelling[a]] for a in objects)
                    * table.dims[v] ** 2 / table.D ** 2
                    for v, count in counts.items()), K.zero)

    # Orthogonality independently checks the unit coefficient in each product.
    require(all(moment((a, b)) == K(int(a == b)) and
                moment((a, b, 0)) == K(int(a == b)) for a, b in pairs),
            'low-row orthogonality or unit Verlinde coefficient fails')
    # These are the predicted coefficients of each low simple in each product.
    low_products = [[int(a == b)] + [integer(moment((a, b, c)), K, 'low Verlinde coefficient')
                                     for c in range(1, n)] for a, b in pairs]
    gram = s.Matrix([[integer(moment(p + q) - K(sum(x * y for x, y in zip(lp, lq))),
                              K, 'residual fourth moment')
                      for q, lq in zip(pairs, low_products)]
                     for p, lp in zip(pairs, low_products)])
    high = [v for v in counts if v not in low]
    multiplicities = [counts[v] for v in high]
    V = s.Matrix.hstack(*map(s.Matrix, high))
    require(V.rank() == len(high), 'restriction types not independent; a general Gram solver is required')
    residual_products = []
    totals = []
    coefficients = []
    for (a, b), lp in zip(pairs, low_products):
        residual = s.Matrix([sum(low[a][i] * low[b][j] * ring[i][j][k]
                                 for i in range(n) for j in range(n))
                             - sum(lp[e] * low[e][k] for e in range(n))
                             for k in range(n)])
        total, free = V.gauss_jordan_solve(residual)
        require(not free.rows, 'unexpected nonunique restriction totals')
        require(all(z.is_Integer is True and z >= 0 for z in total),
                'restriction totals are not nonnegative integers')
        row = [total[k] / multiplicities[k] for k in range(len(high))]
        require(all(z.is_Integer is True and z >= 0 for z in row),
                'constant-type integral completion unavailable')
        residual_products.append(list(map(int, residual)))
        totals.append(list(map(int, total)))
        coefficients.append(list(map(int, row)))
    B = s.Matrix(coefficients)
    require(B * s.diag(*multiplicities) * B.T == gram,
            'constant-type products fail the joint Gram constraint')
    # Expand one actual integer vector per formal high simple and check both
    # equations, rather than accepting only an aggregated moment identity.
    expanded = s.Matrix.hstack(*(B[:, k] for k, count in enumerate(multiplicities)
                                for _ in range(count)))
    V_expanded = s.Matrix.hstack(*(s.Matrix(v) for v, count in zip(high, multiplicities)
                                  for _ in range(count)))
    require(expanded * expanded.T == gram, 'expanded integer Gram identity fails')
    require(V_expanded * expanded.T == s.Matrix(residual_products).T,
            'expanded restriction identities fail')
    return {
        'id': witness['id'],
        'kind': 'joint_low_product_gram_feasible',
        'outcome': 'necessary_conditions_feasible_not_a_category',
        'scope': 'Positive-dimensional center; low central objects are self-dual. No general or pseudo-unitary exclusion is claimed.',
        'inherited_verification': inherited,
        'dimensions': [str(K.to_sympy(x)) for x in table.ds],
        'global_dimension': str(K.to_sympy(table.D)),
        'pairs': [list(x) for x in pairs],
        'low_products': low_products,
        'high_restriction_types': [list(v) for v in high],
        'high_multiplicities': multiplicities,
        'high_restriction_rank': V.rank(),
        'residual_restrictions': residual_products,
        'type_totals': totals,
        'per_simple_high_coefficients': coefficients,
        'gram': [list(map(int, row)) for row in gram.tolist()],
        'gram_rank': gram.rank(),
        'formal_central_rank': n + sum(multiplicities),
        'new_general_exclusions': 0,
        'not_supplied': ['full center fusion tensor', 'individual twists', 'associators',
                         'algebra multiplication or categorification'],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ring', default='R6_3_215')
    parser.add_argument('--witness', type=Path, default=ROOT / 'systems/integral_frontier_215.json')
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('low_product_gram_certificate.json'))
    parser.add_argument('--check', action='store_true', help='recompute and compare with the frozen certificate')
    args = parser.parse_args()
    row = next(r for r in json.loads((ROOT / 'data/census.json').read_text()) if r['id'] == args.ring)
    witness = json.loads(args.witness.read_text())
    require(witness['id'] == args.ring, 'witness and requested ring differ')
    report = compute(row['N'], witness)
    report['tensor_sha256'] = hashlib.sha256(json.dumps(row['N'], separators=(',', ':')).encode()).hexdigest()
    report['witness_sha256'] = sha(args.witness)
    if args.check:
        require(json.loads(args.output.read_text()) == report, 'frozen Gram certificate differs')
    else:
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ('id', 'outcome', 'gram_rank', 'high_restriction_rank',
                                           'high_multiplicities', 'formal_central_rank', 'new_general_exclusions')}, indent=2))


if __name__ == '__main__':
    main()

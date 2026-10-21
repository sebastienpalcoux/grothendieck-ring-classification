"""Independent joint-spectrum control using a separating integer matrix.

No producer joint-tuple, row-building, or support-filter function is called.
The actual 64 central simples are listed directly from Fib x Vec(C4).
"""
from pathlib import Path
from collections import Counter
import argparse, hashlib, json, sys
import sympy as s
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'quadratic'))
from quartic_complex_character_table import QuarticComplexTable
from atomic_galois_balance import automorphisms, coordinates, st, need


def verify():
    R = [[[0] * 8 for _ in range(8)] for _ in range(8)]
    for i in range(8):
        for j in range(8):
            a, g = divmod(i, 4)
            b, h = divmod(j, 4)
            for c in ([0, 1] if a == b == 1 else [a + b]):
                R[i][j][4 * c + (g + h) % 4] += 1
    T = QuarticComplexTable(R, {'q': 5, 'dimensions': [[1, 0]] * 4 +
        [[s.Rational(1, 2), s.Rational(1, 2)]] * 4, 'global_dimension': [10, 2]})
    K = T.K
    fp = T.characters.index(tuple(T.ds))
    labels = [E for E in range(8) if E != fp]
    actual = []
    for g in range(4):
        for a, b, count in ((1, 0, 4), (0, 1, 8), (1, 1, 4)):
            v = [0] * 8
            v[g], v[g + 4] = a, b
            actual.extend([tuple(v)] * count)
    need(len(actual) == 64, 'actual center must contain 64 simples')
    values = []
    for v in actual:
        dimension = sum((K(n) * d for n, d in zip(v, T.ds)), K.zero)
        values.append(tuple(T.beta[E] * sum((K(n) * x for n, x in zip(v, T.characters[E])),
            K.zero) / dimension for E in labels))
    counts = Counter(values)
    maps, field = automorphisms(T)
    coordinate_counts = Counter(tuple(coordinates(x, T.degree) for x in row) for row in values)
    for M in maps:
        transformed = Counter()
        for row, count in coordinate_counts.items():
            image = tuple(tuple(sum(x[j] * M[j][k] for j in range(T.degree))
                for k in range(T.degree)) for x in row)
            transformed[image] += count
        need(transformed == coordinate_counts, 'actual full-tuple Galois multiplicities differ')
    base = None
    for trial in range(2, 100):
        scalars = {sum((K(trial ** j) * value for j, value in enumerate(row)), K.zero)
                   for row in counts}
        if len(scalars) == len(counts):
            base = trial
            break
    need(base is not None, 'no separating integer linear combination in control range')
    polynomial = [K.one]
    for row in values:
        root = sum((K(base ** j) * value for j, value in enumerate(row)), K.zero)
        new = [K.zero] * (len(polynomial) + 1)
        for j, coefficient in enumerate(polynomial):
            new[j] -= root * coefficient
            new[j + 1] += coefficient
        polynomial = new
    integral = []
    for coefficient in polynomial:
        terms = coefficient.to_list()
        need(len(terms) <= 1, 'separating integer combination characteristic polynomial not rational')
        value = s.Rational(str(terms[0])) if terms else s.Integer(0)
        need(value.q == 1, 'separating combination characteristic polynomial not integral')
        integral.append(int(value))
    need(len(integral) == 65 and integral[-1] == 1, 'characteristic polynomial has wrong degree')
    return {'model': 'Fibonacci tensor Vec(C4)', 'central_simples': 64,
            'distinguished_nonunit_matrices': 7, 'distinct_joint_tuples': len(counts),
            'field': field, 'full_tuple_Galois_multiplicities_equal': True,
            'separating_integer_base': base, 'degree_64_integral_characteristic_polynomial': integral,
            'joint_tuple_multiplicities_sha256': st.digest(coordinate_counts),
            'producer_joint_functions_imported': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    out = st.encode(verify())
    path = HERE / 'review_joint_control.json'
    if args.write:
        path.write_text(json.dumps(out, indent=2) + '\n')
    else:
        need(out == json.loads(path.read_text()), 'independent joint control differs')
    print('PASS independent 64-simple joint Galois tuples and separating integral matrix', flush=True)

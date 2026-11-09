#!/usr/bin/env python3
"""Independent exact checks for the fourth-indicator criterion and R2.

Checks both Laurent polynomials, the spectral integer used by the floor,
the R2 dimension/low-row argument, and every recorded R2 fourth witness.
Also retains symbolic character/codegree and third-indicator identities for
the related family. No production routines are imported. The categorical
indicator and positive central-moment theorems remain mathematical inputs.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

import sympy as s


def require(test, message='independent fourth-indicator check failed'):
    if not test:
        raise RuntimeError(message)


def laurent_square(coefficients):
    """Multiply a real polynomial by its reciprocal independently of SymPy."""
    result = Counter()
    for i, a in enumerate(coefficients):
        for j, b in enumerate(coefficients):
            result[i-j] += a*b
    return dict(result)


plus = laurent_square([1, 2, 2, 2, 1])
minus = laurent_square([3, 1, 0, -1, -3])
plus_expected = {0: 14, 1: 12, 2: 8, 3: 4, 4: 1}
minus_expected = {0: 20, 1: 6, 2: -1, 3: -6, 4: -9}
for degree in range(-4, 5):
    require(plus[degree] == plus_expected[abs(degree)], 'wrong Pplus coefficient')
    require(minus[degree] == minus_expected[abs(degree)], 'wrong Pminus coefficient')
require(sum(plus.values()) == 64 and sum(minus.values()) == 0,
        'wrong value of a polynomial at one')
t = s.Symbol('t', real=True)
require(s.expand(10+6*t-s.chebyshevt(2, t)-6*s.chebyshevt(3, t)
                 -9*s.chebyshevt(4, t)-2*(1-t*t)*(6*t+1)**2) == 0,
        'Pminus nonnegative factorization failed')

# Order-three and order-four rotations are diagonalizable in characteristic
# zero. Their eigenvalue multiplicities are arbitrary nonnegative integers.
u0, u1, u2 = s.symbols('u0 u1 u2', nonnegative=True, integer=True)
v0, v1, v2, v3 = s.symbols('v0 v1 v2 v3', nonnegative=True, integer=True)
epsilon = s.Symbol('epsilon', integer=True)
third_real = u0-s.Rational(1, 2)*(u1+u2)
fourth_real = v0-v2
J = s.expand(8*epsilon+4*third_real+fourth_real)
require(s.Poly(J, epsilon, u0, u1, u2, v0, v1, v2, v3).domain == s.ZZ,
        'spectral combination is not an integer polynomial')
d, a, selfdual = s.symbols('d a selfdual', real=True)
fourth_bound = (10*d-epsilon-6*third_real)/9
require(s.expand(9*(8*epsilon+4*third_real+fourth_bound)
                 -(10*d+71*epsilon+30*third_real)) == 0,
        'fourth-indicator elimination identity failed')
require(s.expand((10*d+71*selfdual+30*a)
                 -(10*d+71*epsilon+30*third_real))
        == 71*selfdual-71*epsilon+30*a-30*third_real,
        'indicator upper-bound substitution failed')

n = s.Symbol('n', integer=True)
x = s.Symbol('x')
delta = s.Symbol('delta')
relation = delta**2-3*n*delta-1


def reduce_delta(expr):
    return s.rem(s.expand(expr), relation, delta).expand()


R = [
    s.eye(4),
    s.Matrix([[0, 1, 0, 0], [1, n-1, n-1, n],
              [0, n-1, n, n], [0, n, n, n]]),
    s.Matrix([[0, 0, 1, 0], [0, n-1, n, n],
              [1, n, n, n], [0, n, n, n+1]]),
    s.Matrix([[0, 0, 0, 1], [0, n, n, n],
              [0, n, n, n+1], [1, n, n+1, n+1]]),
]
for A, C in itertools.combinations(R, 2):
    require((A*C-C*A).applyfunc(s.expand) == s.zeros(4),
            'fusion matrices do not commute')
B = sum((A*A.T for A in R), s.zeros(4))
expected = (x-3)**2*(x*x-(12+27*n*n)*x+36+81*n*n)
require(s.expand(B.charpoly(x).as_expr()-expected) == 0,
        'wrong formal-codegree polynomial')
dvec = s.Matrix([1, delta-1, delta, delta+1])
delta_conj = 3*n-delta
characters = [dvec, dvec.subs(delta, delta_conj),
              s.Matrix([1, 0, 1, -1]), s.Matrix([1, 1, -1, 0])]
for character in characters:
    for A, dimension in zip(R, character):
        require(all(reduce_delta(entry) == 0
                    for entry in A*character-dimension*character),
                'character identity failed')
D = 6+9*n*delta
Dconj = 6+9*n*delta_conj
require(reduce_delta(D*Dconj) == 36+81*n*n, 'wrong global-dimension norm')
require(reduce_delta(D-delta**2*Dconj) == 0, 'wrong conjugate-codegree ratio')
require(reduce_delta(D/3-(1+delta**2)) == 0, 'wrong rational-codegree ratio')
low_dims = [1+3*n*delta, 2+3*n*delta, 2+3*n*delta]
require(s.expand(sum(low_dims)-(D-1)) == 0, 'wrong sum of nonunit low dimensions')
summed_gap = reduce_delta(108*n*(D-1)-D*(30*delta+24+6*n))
expected_gap = 18*(13*n-8+(6*n*n-12*n-10)*delta)
require(s.expand(summed_gap-expected_gap) == 0, 'wrong third-indicator gap')
k = s.Symbol('k', nonnegative=True, integer=True)
require(s.expand((13*n-8).subs(n, k+3)) == 13*k+31,
        'constant-coefficient positivity failed')
require(s.expand((6*n*n-12*n-10).subs(n, k+3)) == 6*k*k+24*k+8,
        'delta-coefficient positivity failed')

R2 = [A.subs(n, 2) for A in R]
B2 = B.subs(n, 2)
require(list(B2[:, 0]) == [4, 5, 6, 7], 'wrong R2 first column')
require(list(R2[1][:, 1]) == [1, 1, 1, 2], 'wrong R2 square decomposition')
require(sum(v*v for v in R2[1][:, 1]) == 7, 'wrong fourth tensor-power multiplicity')

# For low dimensions 1+6delta, 2+6delta, 2+6delta the nonunit
# multiplicities are respectively (a,6-2a,a) and (b,5-2b,b+1).
# The first-column identity gives a+b+c=5, whence W_X=10-a+30delta.
# Nonnegativity gives a<=3, without imposing any residual-Gram condition.
low_choices = [(a0, b0, c0) for a0, b0, c0 in itertools.product(range(4), range(3), range(3))
               if a0+b0+c0 == 5]
require(len(low_choices) == 6, 'wrong unquotiented R2 low-row count')
for a0, b0, c0 in low_choices:
    low_weight = a0*low_dims[0]+(b0+c0)*low_dims[1]
    require(s.expand(low_weight.subs(n, 2)-(10-a0+30*delta)) == 0,
            'R2 low-row dimension identity failed')
    require(10-a0 >= 7, 'R2 low-row lower bound failed')

d2 = 3+s.sqrt(10)
D2 = 6+18*d2
bound2 = (10*(d2-1)+71+30)/9
# sqrt(10) is between 3 and 19/6; these rational checks certify floor 16.
require(3**2 < 10 < s.Rational(19, 6)**2, 'wrong sqrt(10) enclosure')
require(s.Rational(10*(3+3)+91, 9) > 16 and
        (10*(3+s.Rational(19, 6))+91)/9 < 17,
        'R2 floor enclosure failed')
require(s.simplify(32*(7+30*d2)-D2*(7*(d2-1)+16)) == 44,
        'R2 fourth-indicator contradiction is not 44')


def canonical(tensor):
    return min(tuple(tensor[p[i]][p[j]][p[h]]
                     for i, j, h in itertools.product(range(4), repeat=3))
               for p in [(0,)+v for v in itertools.permutations(range(1, 4))])


def contains_kind(obj, kind):
    if isinstance(obj, dict):
        return obj.get('kind') == kind or any(contains_kind(v, kind) for v in obj.values())
    if isinstance(obj, list):
        return any(contains_kind(v, kind) for v in obj)
    return False


def quadratic_sign(value):
    """Exact sign in Q(sqrt(10)); no floating-point approximation."""
    value = s.expand(s.simplify(value))
    b0 = value.coeff(s.sqrt(10))
    a0 = s.simplify(value-b0*s.sqrt(10))
    require(a0.is_Rational and b0.is_Rational, 'element is not in Q(sqrt(10))')
    if b0 == 0:
        return s.sign(a0)
    if a0 == 0 or s.sign(a0) == s.sign(b0):
        return s.sign(b0)
    comparison = s.sign(a0*a0-10*b0*b0)
    require(comparison != 0, 'unexpected rational square root of ten')
    return s.sign(a0)*comparison


def check_r2_record(row, record):
    """Replay R2 using explicit characters, rather than production field code."""
    tensor = row['tensor']
    standard = [A.tolist() for A in R2]
    permutations = [(0,)+p for p in itertools.permutations(range(1, 4))]
    p = next((p for p in permutations if all(
        tensor[p[i]][p[j]][p[h]] == standard[i][j][h]
        for i, j, h in itertools.product(range(4), repeat=3))), None)
    require(p is not None, 'R2 basis is not identified')
    dimensions = [None]*4
    for i in range(4):
        dimensions[p[i]] = dvec[i].subs(delta, d2)
    c = record['certificate']
    require(record['stage'] == 'central_induction' and c['kind'] == 'spherical',
            'R2 does not have a central-induction certificate')
    pseudo = c['pseudo']
    require(pseudo['kind'] == 'induction' and pseudo['generator'] == c['generator'],
            'wrong R2 central certificate')
    generator = c['generator']
    require(type(generator) is int, 'invalid R2 character generator')
    alpha = 1+dimensions[1]+generator*dimensions[2]+generator**2*dimensions[3]

    def decode(coefficients):
        require(isinstance(coefficients, list) and len(coefficients) <= 2,
                'invalid R2 field vector')
        value = s.S.Zero
        for coefficient in coefficients:
            value = value*alpha+s.Rational(coefficient)
        return s.expand(value)

    factor = s.Poly.from_list(list(map(s.Rational, pseudo['fp_factor'])), x, domain=s.QQ)
    require(factor.degree() == 2 and factor.is_irreducible
            and s.simplify(factor.as_expr().subs(x, alpha)) == 0,
            'R2 character field factor mismatch')
    require(any(branch['factor'] == pseudo['fp_factor'] for branch in c['characters']),
            'missing R2 positive character branch')
    roots = [decode(value) for value in pseudo['roots']]
    expected_roots = [D2, 6+18*(3-s.sqrt(10)), s.Integer(3), s.Integer(3)]
    for expected_root in expected_roots:
        match = next((j for j, root in enumerate(roots)
                      if s.simplify(root-expected_root) == 0), None)
        require(match is not None, 'missing R2 formal codegree')
        roots.pop(match)
    require(not roots, 'extra R2 formal codegrees')

    matrices = list(map(s.Matrix, tensor))
    gram_budget = sum((A*A.T for A in matrices), s.zeros(4))
    # Enumerate the prescribed low rows in full integer boxes, then quotient
    # only the two equal-codegree row positions in the recorded root order.
    ordered_roots = [decode(value) for value in pseudo['roots']]
    unit_root = next(j for j, root in enumerate(ordered_roots)
                     if s.simplify(root-D2) == 0)
    ordered_roots.pop(unit_root)
    row_sets = []
    for root in ordered_roots:
        target = s.simplify(D2/root)
        candidates = []
        for values in itertools.product(*(range(int(gram_budget[0, j])+1)
                                          for j in range(1, 4))):
            low_row = (1,)+values
            if s.simplify(sum(low_row[j]*dimensions[j] for j in range(4))-target) == 0:
                candidates.append(low_row)
        row_sets.append(candidates)
    require(list(map(len, row_sets)) == pseudo['column_counts'], 'wrong R2 candidate-row counts')
    low = []
    for rows in itertools.product(*row_sets):
        cols = ((1, 0, 0, 0),)+rows
        if any(sum(low_row[j] for low_row in cols) != gram_budget[0, j] for j in range(4)):
            continue
        if any(s.simplify(ordered_roots[i]-ordered_roots[j]) == 0 and rows[i] > rows[j]
               for i in range(3) for j in range(i+1, 3)):
            continue
        low.append(cols)
    failures = pseudo['failures']
    recorded = {tuple(map(tuple, branch['columns'])): branch['obstruction'] for branch in failures}
    require(set(low) == set(recorded) and len(low) == len(recorded) == pseudo['low_count']
            == len(failures), 'incomplete R2 low-row coverage')
    checked = Counter()
    fourth_witnesses = []
    for cols in low:
        why = recorded[cols]
        i = why['object']
        require(type(i) is int and 1 <= i < 4, 'invalid R2 local object')
        G = s.Matrix(cols).T*s.Matrix(cols)
        W = s.expand(sum(G[i, j]*dimensions[j] for j in range(4)))
        require(quadratic_sign(sum(G[p[1], j]*dimensions[j] for j in range(4))
                               -(7+30*d2)) >= 0, 'R2 low-row lower bound violated')
        if why['kind'] == 'fourth_indicator_row':
            floor = why.get('floor')
            require(type(floor) is int, 'invalid recorded fourth-indicator floor')
            bound = (10*dimensions[i]+71+30*tensor[i][i][i])/9
            require(quadratic_sign(bound-floor) >= 0 and quadratic_sign(floor+1-bound) > 0,
                    'recorded fourth-indicator floor is false')
            gap = s.expand(32*W-D2*(7*dimensions[i]+floor))
            fourth_witnesses.append({'object': i, 'floor': floor,
                                     'gap': str(s.simplify(gap))})
        elif why['kind'] == 'polynomial_row':
            require(why['nonselfdual'] is False, 'wrong R2 duality claim')
            gap = s.expand(9*W-D2*(3*dimensions[i]+2))
        elif why['kind'] == 'third_indicator_row':
            gap = s.expand(36*W-D2*(10*dimensions[i]+8+2*tensor[i][i][i]))
        else:
            raise RuntimeError('unexpected R2 local witness: '+why['kind'])
        require(quadratic_sign(gap) > 0 and s.simplify(gap-decode(why['gap'])) == 0,
                'R2 recorded local gap is false')
        checked[why['kind']] += 1
    require(fourth_witnesses, 'R2 has no recorded fourth-indicator witnesses')
    return {'id': row['id'], 'low_count': len(low), 'checked_kinds': dict(checked),
            'fourth_witnesses': fourth_witnesses}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    root = args.archive/'supplementary'
    rows = list(map(json.loads, (root/'census/data/rings.jsonl').read_text().splitlines()))
    certs = list(map(json.loads, (root/'classification/results/certificates.jsonl').read_text().splitlines()))
    require(len(rows) == len(certs) and all(row['id'] == rec['id'] for row, rec in zip(rows, certs)),
            'certificate coverage/order differs')
    by_id = {c['id']: c for c in certs}
    require(len(by_id) == len(certs), 'certificate IDs are not bijective')
    require(all(c['stage'] != 'quadratic_boundary' for c in certs), 'obsolete separate R2 stage')
    family_keys = {canonical([A.subs(n, value).tolist() for A in R]): value
                   for value in range(2, 12)}
    matches = []
    r2 = []
    for row in rows:
        value = family_keys.get(canonical(row['tensor']))
        if value is None:
            continue
        certificate = by_id[row['id']]
        require(certificate['stage'] == 'central_induction', 'family assigned wrong filter')
        expected_kind = 'fourth_indicator_row' if value == 2 else 'third_indicator_row'
        require(contains_kind(certificate['certificate'], expected_kind), 'missing family witness')
        matches.append({'n': value, 'id': row['id'], 'stage': certificate['stage']})
        if value == 2:
            r2.append(check_r2_record(row, certificate))
    require(len(matches) == 10 and sorted(item['n'] for item in matches) == list(range(2, 12)),
            'quadratic family census coverage failed')
    require(len(r2) == 1 and 6+27*12**2 > 3600, 'wrong R2 coverage or family cutoff')
    result = {
        'passed': True,
        'laurent_coefficients': {'Pplus': plus_expected, 'Pminus': minus_expected},
        'spectral_integer_J': True,
        'symbolic_associativity': True,
        'character_and_codegree_field_identities': True,
        'uniform_third_indicator_gap_positive_for_all_n_at_least_3': True,
        'R2_low_weight_lower_bound': '7+30*delta',
        'R2_fourth_indicator_floor': 16,
        'R2_exact_positive_gap': 44,
        'R2_recorded_witnesses': r2[0],
        'R3_through_R11_have_third_indicator_certificates': True,
        'scope': ('No production imports. Exact polynomial, spectral and family identities; '
                  'direct R2 characters and full low-row boxes replay its recorded local '
                  'witnesses. Categorical indicator and positive central-moment theorems '
                  'are mathematical inputs.'),
        'cases': sorted(matches, key=lambda item: item['n']),
    }
    print(json.dumps(result, indent=2))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2)+'\n')


if __name__ == '__main__':
    main()

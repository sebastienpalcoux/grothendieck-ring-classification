#!/usr/bin/env python3
"""Exact seven-ring dimension-block screen and saturation constraints.

This checks arithmetic and source-ring hypotheses. The published modular
compression theorem and the already accepted Galois-PU gates are mathematical
dependencies; no new cone computation or category existence is claimed.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SOURCE = 'evidence/rank8_m3_20261021/pipeline/census_m3.json'
IDS = (928, 941, 982, 1154, 1768, 1795, 3472)


def need(ok, message):
    if not ok:
        raise ValueError(message)


class Field:
    def __init__(self, radicands):
        self.r = tuple(radicands)
        self.n = 1 << len(self.r)
        self.zero = (F(0),) * self.n
        self.one = (F(1),) + self.zero[1:]

    def vector(self, a):
        return tuple(map(F, a))

    def scalar(self, a):
        return (F(a),) + self.zero[1:]

    def add(self, a, b):
        return tuple(x + y for x, y in zip(a, b))

    def scale(self, k, a):
        return tuple(k * x for x in a)

    def mul(self, a, b):
        out = list(self.zero)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                factor = 1
                for k, r in enumerate(self.r):
                    if i & j & (1 << k):
                        factor *= r
                out[i ^ j] += factor * x * y
        return tuple(out)

    def sigma(self, a, mask):
        return tuple((-x if (i & mask).bit_count() % 2 else x)
                     for i, x in enumerate(a))

    def inv(self, a):
        need(a != self.zero, 'Division by zero')
        product = self.one
        for mask in range(1, self.n):
            product = self.mul(product, self.sigma(a, mask))
        norm = self.mul(a, product)
        need(norm[0] and norm[1:] == self.zero[1:], 'Nonrational field norm')
        return self.scale(1 / norm[0], product)

    def total(self, values):
        out = self.zero
        for value in values:
            out = self.add(out, value)
        return out

    def sqrt_basis(self, mask):
        value = 1
        for j, r in enumerate(self.r):
            if mask & (1 << j):
                value *= r
        return value


def encode(a):
    return [str(x) for x in a]


def null_vector(K, matrix, D):
    """Exact one-dimensional Casimir kernel, normalized at the unit."""
    size = matrix.rows
    rows = [[K.add(K.scalar(matrix[i, j]), K.scale(-int(i == j), D))
             for j in range(size)] for i in range(size)]
    pivots = []
    for col in range(size):
        candidates = [i for i in range(len(pivots), size) if rows[i][col] != K.zero]
        if not candidates:
            continue
        k = len(pivots)
        rows[k], rows[candidates[0]] = rows[candidates[0]], rows[k]
        inverse = K.inv(rows[k][col])
        rows[k] = [K.mul(x, inverse) for x in rows[k]]
        for i in range(size):
            if i == k:
                continue
            coefficient = rows[i][col]
            rows[i] = [K.add(a, K.scale(-1, K.mul(coefficient, b)))
                       for a, b in zip(rows[i], rows[k])]
        pivots.append(col)
    free = [j for j in range(size) if j not in pivots]
    need(len(free) == 1, 'The FP Casimir eigenspace must be one-dimensional')
    vector = [K.zero] * size
    vector[free[0]] = K.one
    for k, pivot in enumerate(pivots):
        vector[pivot] = K.scale(-1, rows[k][free[0]])
    inverse = K.inv(vector[0])
    return [K.mul(x, inverse) for x in vector]


def compute(record):
    rid = record['id']
    number = int(rid.split('_')[-1])
    if number in (928, 941, 982):
        K, D = Field((2, 3)), (144, 96, 80, 56)
    elif number in (1154, 1795):
        K, D = Field((5,)), (540, 240)
    elif number == 1768:
        K, D = Field((37,)), (444, 72)
    else:
        K, D = Field((2,)), (700, 490)
    D = K.vector(D)
    R = record['tensor']
    tensor_sha = hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest()
    need(tensor_sha == record['tensor_sha256'], rid + ': tensor binding')
    dual = []
    for i in range(8):
        choices = [j for j in range(8) if R[i][j][0]]
        need(len(choices) == 1 and R[i][choices[0]][0] == 1, 'Simple dual')
        dual.append(choices[0])
    matrices = [s.Matrix(row) for row in R]
    casimir = sum((matrices[i] * matrices[dual[i]] for i in range(8)), s.zeros(8))
    dims = null_vector(K, casimir, D)
    need(all(all(x >= 0 for x in d) and any(x > 0 for x in d) for d in dims),
         rid + ': the normalized dimension character must be positive')
    for i, j in itertools.product(range(8), repeat=2):
        need(K.mul(dims[i], dims[j]) ==
             K.total(K.scale(R[i][j][k], dims[k]) for k in range(8)),
             rid + ': dimension multiplication')
    need(K.total(K.mul(dims[i], dims[dual[i]]) for i in range(8)) == D,
         rid + ': exact global FP dimension')
    conjugates = [K.sigma(D, mask) for mask in range(K.n)]
    need(len(set(conjugates)) == K.n, rid + ': D generates the full dimension field')
    inverse = K.inv(D)
    characters = []
    for mask in range(K.n):
        total = K.total(K.scale(-1 if (mask & g).bit_count() % 2 else 1,
                                K.sigma(inverse, g)) for g in range(K.n))
        square = K.mul(total, total)
        need(square[1:] == K.zero[1:], 'Fourier-sum square is rational')
        squarefree = K.sqrt_basis(mask)
        conductor = 1 if mask == 0 else squarefree * (1 if squarefree % 4 == 1 else 4)
        value = conductor * square[0]
        need(value <= 1, rid + ': dimension-block inequality violated')
        characters.append({'mask': mask, 'quadratic_character_radicand': squarefree,
                           'conductor': conductor, 'twisted_sum': encode(total),
                           'absolute_square': str(square[0]),
                           'conductor_times_absolute_square': str(value),
                           'saturated': value == 1})
    saturated = [row['mask'] for row in characters if row['saturated']]
    polynomial = casimir.charpoly().as_poly()
    x = polynomial.gen
    orbit_polynomial = s.Poly(1, x)
    # Build the exact product in the multiquadratic field and verify rationality.
    coefficients = [K.one]
    for value in conjugates:
        new = [K.zero] * (len(coefficients) + 1)
        for i, a in enumerate(coefficients):
            new[i] = K.add(new[i], a)
            new[i + 1] = K.add(new[i + 1], K.scale(-1, K.mul(a, value)))
        coefficients = new
    need(all(c[1:] == K.zero[1:] for c in coefficients), 'Rational dimension polynomial')
    orbit_polynomial = s.Poly.from_list([s.Rational(c[0]) for c in coefficients], x)
    remainder, rem = s.div(polynomial, orbit_polynomial)
    need(rem.is_zero, 'Dimension orbit divides Casimir characteristic polynomial')
    commutative = all(R[i][j] == R[j][i] for i, j in itertools.product(range(8), repeat=2))
    forced = []
    if number in (928, 941):
        need(not commutative and remainder == s.Poly((x - 8) ** 4, x),
             'Four scalar dimension-orbit representations and one two-dimensional representation')
        forced = [(K.scalar(4), 1, 2)]
    elif number == 982:
        need(commutative and remainder == s.Poly((x * x - 32*x + 128)**2, x),
             'R982 outside-orbit scalar formal codegrees')
        forced = [(K.vector((16, sign*8, 0, 0)), 2, 1) for sign in (-1, 1)]
    elif number == 1768:
        need(commutative and remainder == s.Poly((x-6)**4*(x-12)**2, x),
             'R1768 outside-orbit scalar formal codegrees')
        forced = [(K.scalar(6), 4, 1), (K.scalar(12), 2, 1)]
    checked = []
    for f, count, representation_dimension in forced:
        ratio = K.inv(f)
        need(all(ratio[mask] == 0 for mask in saturated),
             'A forced twist-one I(1) summand violates saturation')
        checked.append({'formal_codegree': encode(f), 'distinct_representations': count,
                        'representation_dimension': representation_dimension,
                        'central_dimension_over_D': encode(ratio),
                        'saturation_conditions_satisfied': True})
    equations = []
    for mask in saturated:
        row = []
        for coordinate in range(K.n):
            unit = tuple(F(int(i == coordinate)) for i in range(K.n))
            row.append(K.mul(unit, inverse)[mask])
        denominator = s.ilcm(*[value.denominator for value in row])
        integers = [int(value * denominator) for value in row]
        divisor = s.igcd(*integers)
        integers = [value // abs(divisor) for value in integers]
        first = next(v for v in integers if v)
        if first < 0:
            integers = [-v for v in integers]
        equations.append(integers)
    return {'id': rid, 'tensor_sha256': tensor_sha,
            'field_radicands': list(K.r), 'basis': [K.sqrt_basis(i) for i in range(K.n)],
            'FP_dimensions': [encode(d) for d in dims], 'D': encode(D),
            'D_inverse': encode(inverse), 'D_minimal_polynomial': str(orbit_polynomial.as_expr()),
            'dimensional_grading_order_e': 1,
            'characters': characters, 'saturated_masks': saturated,
            'extra_twist_one_dimension_coefficient_equations': equations,
            'extra_twist_one_scope': 'Only central simples outside the dimension orbit; each listed linear form must vanish.',
            'outside_dimension_orbit_I1_codegree_checks': checked,
            'outside_dimension_orbit_I1_test': 'all pass' if saturated else 'not restricted by saturation',
            'scalar_obstruction': False, 'new_categorical_exclusion': False}


def run():
    raw = (ROOT / SOURCE).read_bytes()
    census = {row['id']: row for row in json.loads(raw)}
    rows = [compute(census[f'R8_3_{number}']) for number in IDS]
    need([row['id'] for row in rows if row['saturated_masks']] ==
         ['R8_3_928', 'R8_3_941', 'R8_3_982', 'R8_3_1768'], 'Saturated ring inventory')
    return {'schema': 'rank8-dimension-block-screen/v1',
            'primary_reference': {'author': 'Andrew Schopieray',
                                  'title': 'The dimension block of a spherical fusion category',
                                  'arxiv': '2609.35287v1', 'version_date': '2026-09-28',
                                  'url': 'https://arxiv.org/html/2609.35287v1',
                                  'locations': ['Lemma 2.1', 'Lemma 4.1', 'Theorem 5.1', 'Section 6, equation (30)']},
            'inputs_sha256': {SOURCE: hashlib.sha256(raw).hexdigest()},
            'scope': 'Exact FP-form arithmetic. General categorifications transfer via previously accepted sphericality/Galois-pseudo-unitary gates, which are not rerun here.',
            'all_seven_scalar_bounds_satisfied': True,
            'all_forced_I1_saturation_constraints_satisfied': True,
            'new_cone_search_performed': False, 'new_exclusion_or_model': False,
            'records': rows}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = run()
    path = HERE / 'verification.json'
    if args.write:
        path.write_text(json.dumps(result, indent=2) + '\n')
    else:
        need(result == json.loads(path.read_text()), 'Saved arithmetic receipt differs')
    print('PASS: all seven dimension-block bounds; four saturation restrictions; every forced I(1) summand passes; no exclusion or model')

#!/usr/bin/env python3
"""Exact C3+3 TPE reduction and the source hypotheses for R8_3_436.

The categorical implications, including the indispensable full-parameter
necessity theorem, are stated separately in R436_GENERAL_TPE.md.
Default invocation is read-only. No published evidence is modified.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import sympy as sp

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
IDENT = 'R8_3_436'
SHA = '0f6d68de67a7287db7dd32a786237f7af9f35ec7c26b3ada2ba50012ff5455c7'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def source_certificate():
    path = REPO / 'evidence/rank8_m3_20261021/pipeline/census_m3.json'
    row = next(r for r in json.loads(path.read_text()) if r['id'] == IDENT)
    R = row['tensor']
    require(row['tensor_sha256'] == SHA == digest(R), 'source hash mismatch')
    A = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for i, j in itertools.product(range(3), repeat=2):
        A[i][j][(i+j) % 3] = 1
    for i in range(3):
        A[i][3][3] = A[3][i][3] = 1
    A[3][3] = [1, 1, 1, 3]
    p = [0, 2, 1, 3]
    S = [[[0] * 8 for _ in range(8)] for _ in range(8)]
    for i, e, j, f, k in itertools.product(range(4), range(2), range(4), range(2), range(4)):
        S[2*i+e][2*j+f][2*k+(e+f) % 2] = A[i][p[j] if e else j][k]
    m = [0, 3, 1, 7, 2, 6, 5, 4]
    require(all(S[i][j][k] == R[m[i]][m[j]][m[k]]
                for i, j, k in itertools.product(range(8), repeat=3)),
            'crossed ring does not match all source coefficients')
    neutral = [0, 1, 2, 5]
    require([[[R[i][j][k] for k in neutral] for j in neutral] for i in neutral] == A,
            'wrong neutral subring')
    require(all(R[i][j][k] == 0 for i in neutral for j in neutral
                for k in range(8) if k not in neutral), 'neutral subring not closed')
    def product(i, j):
        require(sum(R[i][j]) == 1, 'product not simple')
        return R[i][j].index(1)
    require(product(3, 3) == 0, 'wrong odd invertible square')
    conjugation = [product(product(3, i), 3) for i in neutral]
    require(conjugation == [0, 2, 1, 5], 'wrong inversion action')
    require(R[5][5][5] == 3, 'FRS odd-multiplicity hypothesis fails')
    return {'id': IDENT, 'tensor_sha256': SHA, 'neutral_basis': neutral,
            'near_group_tensor': A, 'odd_invertible': 3,
            'conjugation_on_neutral_basis': conjugation,
            'basis_map_crossed_model_to_source': m, 'coefficients_checked': 512,
            'frobenius_schur_odd_multiplicity': 3}


def tpe_certificate():
    # Both primitive cube roots and both dimension roots are kept symbolic.
    x, y, d, w = sp.symbols('x y d w')
    variables = (x, y, d, w)
    t = (3-d) / 3
    a = [sp.Integer(1), w, w]
    beta = [t, x, y]
    base = [d*d-3*d-3, w*w+w+1]
    B = sp.groebner(base, *variables, order='lex', domain=sp.QQ)
    def base_reduce(expr):
        return B.reduce(sp.expand(expr))[1]
    cubic = []
    for g, h in itertools.product(range(3), repeat=2):
        # In Q[w]/Phi_3, inverse chi(h,k) = w^(2hk), inverse a = a^2.
        lhs = a[(h-g) % 3] * sum(w**((2*h*k) % 3)
                * beta[(g-k) % 3] * beta[k] * a[k]**2 for k in range(3)) / 3
        rhs = beta[-h % 3] * beta[g] * beta[(h-g) % 3]
        if g == h == 0:
            rhs += (d-3) / 3
        cubic.append(base_reduce(lhs-rhs))
    generated = sp.groebner(cubic + base, *variables, order='lex', domain=sp.QQ)
    expected = sp.groebner([x+y-(1+w)*t, x*y-w/3] + base,
                          *variables, order='lex', domain=sp.QQ)
    require(list(generated) == list(expected), 'exact TPE ideal reduction failed')
    def red(expr):
        return expected.reduce(sp.expand(expr))[1]
    require(all(red(e) == 0 for e in cubic), 'one of the nine cubic equations fails')
    # Derivation without elimination: x=y would contradict the dimension polynomial.
    require(base_reduce(6*t*t-6*t+1) == 3, 'equal-root contradiction failed')
    require(red((x-y)**2 + w*d/3) == 0, 'nonzero root discriminant identity failed')
    q_inverse = 1+w*w
    u, v = x*q_inverse, y*q_inverse
    require(red(u+v-t) == 0 and red(u*v-sp.Rational(1, 3)) == 0,
            'real quadratic normalization failed')
    require(base_reduce(t*t-sp.Rational(4, 3)+d/3) == 0,
            'negative discriminant identity failed')
    # The rotation scalar c=1/(2+w)=(1-w)/3; check the entire remaining TPE system.
    c = (1-w)/3
    require(red(c*(2+w)-1) == 0, 'wrong rotation scalar')
    require(red(c*(beta[0]+beta[1]+beta[2])-t) == 0, 'rotation normalization fails')
    require(red(3*c**3*sum(a)-1) == 0, 'Gauss normalization fails')
    for h in range(3):
        fourier = sum(a[g]**2*w**((h*g) % 3)*beta[g] for g in range(3))-3*c*beta[h]
        require(red(fourier) == 0, 'Fourier equation fails')
        quadratic = beta[h]*beta[-h % 3]-a[h]/3
        if h == 0:
            quadratic += (d-3)/3
        require(red(quadratic) == 0, 'product equation fails')
    # Primitive quadratic data are exhaustive on C3: even a and refinement
    # give a1=a2=w, since a2*w=a1^2 and a1 is nonzero.
    for g, h in itertools.product(range(3), repeat=2):
        require(base_reduce(a[(g+h) % 3]*w**((g*h) % 3)-a[g]*a[h]) == 0,
                'quadratic refinement fails')
    return {'variables': list(map(str, variables)),
            'dimension_polynomial': str(base[0]), 'bicharacter_polynomial': str(base[1]),
            'beta0': str(t), 'quadratic_refinement': ['1', 'w', 'w'],
            'cubic_equations_checked': 9,
            'reduced_groebner_basis': [str(p) for p in generated],
            'equivalent_scalar_relations': ['x+y=(1+w)*(3-d)/3', 'x*y=w/3'],
            'rotation_scalar': str(c), 'equal_root_contradiction': '3=0',
            'real_normalization': 'u=x/(1+w), v=y/(1+w)',
            'real_quadratic': 'z^2-((3-d)/3)*z+1/3',
            'real_quadratic_discriminant': '-d/3',
            'positive_dimension_branch': '(3+sqrt(21))/2',
            'positive_branch_hermitian_relation': 'conjugate(beta(g))=beta(-g)/a(g)',
            'full_tpe_checked_after_reduction': True,
            'all_primitive_bicharacters_included': True,
            'both_dimension_roots_included': True,
            'number_of_scalar_solutions_before_gauge': 8}


def record():
    return {'schema': 'rank8-frontier-c3-tpe-general-v1',
            'kind': 'c3_near_group_galois_unitarization_inversion_obstruction',
            'scope': 'general_complex', 'outcome': 'excluded',
            'source': source_certificate(), 'algebra': tpe_certificate(),
            'proof': 'evidence/rank8_frontier_20261021/structural_models/R436_GENERAL_TPE.md',
            'literature_hypotheses': [
                {'url': 'https://arxiv.org/pdf/1102.4640', 'locator': 'Theorem1.3',
                 'input': 'Every complex near-group category is spherical and Galois-pseudounitary.'},
                {'url': 'https://arxiv.org/pdf/2203.06522', 'locator': 'Theorem3.9, printedp11',
                 'input': 'Odd multiplicity in X* tensor X forces the second indicator to be +1.'},
                {'url': 'https://arxiv.org/pdf/2610.11652',
                 'locator': 'Theorem2.3; Proposition2.7; Theorem4.12; Corollary5.5',
                 'input': 'Full spherical C3+3 tetrahedral parametrization with indicator+1, and unitary reconstruction from Hermitian scalar data.'},
                {'url': 'https://arxiv.org/pdf/1512.04288', 'locator': 'Theorem9.1; Example9.4',
                 'input': 'Unitary C3+3 categories are the known Izumi-Xu categories up to complex conjugation.'},
                {'url': 'https://arxiv.org/pdf/1211.6414', 'locator': 'Section4.2, printedp10 afterRemark4.10',
                 'input': 'Either known Izumi-Xu category has no outer tensor autoequivalences.'}],
            'review_qualification': 'New proof using the October2026 TPE preprint; independent human mathematical review remains appropriate.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    actual = record()
    path = HERE / 'r436_general_tpe.json'
    if args.write:
        path.write_text(json.dumps(actual, indent=2) + '\n')
    else:
        require(actual == json.loads(path.read_text()), 'saved frontier certificate differs')
    print('PASS: R8_3_436 full512 source match; all9 C3 TPE cubics; exact all-branch reduction and positive-branch unitary identities.')


if __name__ == '__main__':
    main()

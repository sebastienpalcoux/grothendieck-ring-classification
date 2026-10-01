#!/usr/bin/env python3
"""Conditional rank-18 relative-center candidates for R6_9_3748.

This is isolated research, not a general exclusion for the rank-six tensor.
The proposed categorical reduction is a hypothesis, not certified here.
Run using the package's SymPy-enabled Python. Each case has a hard 55s
subprocess deadline; an unfinished case is never counted as an exclusion.
"""
import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'software'))
import sympy as s
import rings
from exact import pc, require, t

A = [
    [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    [[0, 1, 0], [1, 0, 1], [0, 1, 1]],
    [[0, 0, 1], [0, 1, 1], [1, 1, 1]],
]
PAIR = list(itertools.product(range(3), repeat=2))
LABELS = ['1', 'a', 'b']
TARGET = [2, 2, 1]
CASE_SECONDS = 55


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, value):
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_text(json.dumps(value, indent=2) + '\n')
    os.replace(tmp, path)


def forget(c):
    return [sum(c[q] * A[i][j][k] for q, (i, j) in enumerate(PAIR))
            for k in range(3)]


def lifts():
    # Every basis pair has at least one positive forgetful coefficient.
    # Bounding each coefficient by the relevant target coordinates makes
    # this a complete rectangular enumeration, independent of the count15.
    bounds = [min(TARGET[k] // A[i][j][k] for k in range(3) if A[i][j][k])
              for i, j in PAIR]
    out = [list(c) for c in itertools.product(*(range(b + 1) for b in bounds))
           if forget(c) == TARGET]
    require(len(out) == 15, 'unexpected nonnegative lift count')
    return out


def tensor_product():
    return [[[A[i][k][u] * A[j][l][v] for u, v in PAIR]
             for k, l in PAIR] for i, j in PAIR]


def multiply(R, u, v):
    n = len(R)
    result = [0] * n
    for i, x in enumerate(u):
        if not x:
            continue
        for j, y in enumerate(v):
            if y:
                for k, z in enumerate(R[i][j]):
                    result[k] += x * y * z
    return result


def extension(B, c):
    # Basis is B followed by Bt, with t at index9.
    n = len(B)
    R = [[[0] * (2*n) for _ in range(2*n)] for _ in range(2*n)]
    for i, j in itertools.product(range(n), repeat=2):
        R[i][j][:n] = B[i][j]
        R[i][n+j][n:] = B[i][j]
        R[n+i][j][n:] = B[i][j]
        R[n+i][n+j][:n] = B[i][j]
        R[n+i][n+j][n:] = multiply(B, B[i][j], c)
    return R


def validate_exact(R):
    """Integer-only full based-ring checks, including all associativity entries."""
    n = len(R)
    require(all(len(M) == n and all(len(row) == n for row in M) for M in R), 'shape')
    require(all(type(x) is int and x >= 0 for M in R for row in M for x in row), 'coefficients')
    for i, j in itertools.product(range(n), repeat=2):
        require(R[0][i][j] == R[i][0][j] == int(i == j), 'unit')
        require(R[i][j][0] == int(i == j), 'self-duality')
    for i, j, k in itertools.product(range(n), repeat=3):
        require(R[i][j][k] == R[j][i][k] == R[i][k][j], 'reciprocity')
    support = [[[(k, x) for k, x in enumerate(R[i][j]) if x]
                for j in range(n)] for i in range(n)]
    for i, j, k in itertools.product(range(n), repeat=3):
        left = [0] * n
        right = [0] * n
        for q, x in support[i][j]:
            for h, y in support[q][k]:
                left[h] += x * y
        for q, x in support[j][k]:
            for h, y in support[i][q]:
                right[h] += x * y
        require(left == right, 'associativity')


def source_row():
    rows = json.loads((ROOT / 'data/census.json').read_text())
    row = next(r for r in rows if r['id'] == 'R6_9_3748')
    R = row['N']
    require(row['m'] == 9 and max(rings.flat(R)) == 9, 'wrong source multiplicity')
    validate_exact(R)
    labels = [0, 1, 5]
    complement = [2, 3, 4]
    # Exact subring, regular module, and X^2 coefficient, from the full tensor.
    for i, j in itertools.product(range(3), repeat=2):
        expected = [0] * 6
        for k in range(3):
            expected[labels[k]] = A[i][j][k]
        require(R[labels[i]][labels[j]] == expected, 'wrong subring')
        expected = [0] * 6
        for k in range(3):
            expected[complement[k]] = A[i][j][k]
        require(R[labels[i]][complement[j]] == expected, 'wrong module action')
    require(R[2][2] == [1, 0, 2, 2, 1, 0], 'wrong quadratic relation')
    # Reconstructing the complete ambient ring rules out a local-profile match.
    ambient = extension(A, TARGET)
    original_order = [0, 1, 5, 2, 3, 4]
    require(rings.permute(R, original_order) == ambient, 'full ambient tensor mismatch')
    return row


def case(number):
    started = time.monotonic()
    c = lifts()[number - 1]
    B = tensor_product()
    R = extension(B, c)
    validate_exact(R)
    N = list(map(s.Matrix, B))
    K = sum((M * M for M in N), s.zeros(9))
    H = sum((x * M for x, M in zip(c, N)), s.zeros(9))
    require(K * H == H * K, 'commuting B operators')
    I = s.eye(9)
    formula_casimir = (2*K).row_join(K*H).col_join((K*H).row_join(K*(2*I + H*H)))
    direct_casimir = rings.casimir(R)
    require(direct_casimir == formula_casimir, 'Casimir block formula')
    p = direct_casimir.charpoly(t).as_poly()
    # For every B character, f_E has quadratic
    # z^2 - f_B(4+chi(C)^2)z + f_B^2(4+chi(C)^2).
    # Verify its determinant formula at19 exact rational points. Both sides
    # are degree18 polynomials, so this is an exact polynomial identity.
    Q = 4*I + H*H
    L = K*Q
    M = K*K*Q
    evaluation_checks = []
    for z in range(19):
        determinant = int((z*z*I - z*L + M).det(method='domain-ge'))
        value = int(p.eval(z))
        require(value == determinant, 'character-pair determinant identity')
        evaluation_checks.append([z, str(value)])
    fac = rings.codegree_factors(R)
    require(sum(q.degree()*m for q, m in fac) == 18, 'formal degree count')
    factor_rows = []
    for q, multiplicity in fac:
        co = list(map(int, q.all_coeffs()))
        require(q.is_irreducible and co[0] == 1 and co[-1] != 0, 'minimal polynomial')
        degree = q.degree()
        constant = abs(co[-1])
        failures = []
        for j, a in enumerate(co[1:], 1):
            remainder = pow(a, degree, constant**j)
            if remainder:
                failures.append(dict(j=j, coefficient=str(a), degree=degree,
                                     divisor=str(constant**j), remainder=str(remainder)))
        factor_rows.append(dict(polynomial=pc(q), multiplicity=multiplicity,
                                degree=degree, dnumber=not failures,
                                failed_divisibilities=failures))
    witness = rings.dnumber(R)
    if witness:
        rings.check_dnumber(R, witness)
    require(bool(witness) == any(not f['dnumber'] for f in factor_rows), 'dnumber consistency')
    return dict(case=number, C=c, C_matrix=[c[3*i:3*i+3] for i in range(3)],
                forgetful_image=forget(c), tensor_sha256=rings.fingerprint(R),
                tensor_rank=18, exact_based_ring_checked=True,
                casimir_block_formula_checked=True,
                paired_character_determinant_checked=True,
                character_formula_evaluations=evaluation_checks,
                formal_codegree_polynomial=pc(p), formal_codegree_factors=factor_rows,
                dnumber_certificate=witness, dnumber_certificate_exact_checked=bool(witness),
                status='excluded_as_rank18_fusion_ring' if witness else 'survives_dnumber',
                seconds=round(time.monotonic()-started, 6))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', type=int, choices=range(1, 16))
    parser.add_argument('--verify', action='store_true', help='replay existing artifacts without writing')
    args = parser.parse_args()
    if args.case:
        print(json.dumps(case(args.case), separators=(',', ':')))
        return
    row = source_row()
    source = dict(id=row['id'], tensor_sha256=rings.fingerprint(row['N']),
                  census_sha256=digest(ROOT/'data/census.json'),
                  scripts_sha256={str(p.relative_to(ROOT)): digest(p) for p in
                                  (Path(__file__), ROOT/'software/rings.py', ROOT/'software/exact.py')},
                  python=sys.version, sympy=s.__version__)
    results = []
    for number in range(1, 16):
        try:
            run = subprocess.run([sys.executable, '-O', str(Path(__file__)), '--case', str(number)],
                                 capture_output=True, text=True, timeout=CASE_SECONDS, check=True)
            result = json.loads(run.stdout)
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, ValueError) as error:
            result = dict(case=number, C=lifts()[number-1], status='unfinished', error=str(error))
        print('case', number, result['status'], 'seconds', result.get('seconds'), flush=True)
        results.append(result)
    complete = all(r['status'] != 'unfinished' for r in results)
    report = dict(
        schema='conditional_relative_psu2_5_dnumber_v1', source=source,
        scope='CONDITIONAL RESEARCH ONLY. This does not certify a general exclusion of R6_9_3748.',
        categorical_reduction_proved=False,
        proposed_categorical_hypotheses=[
            'A characteristic-zero fusion categorification C of the given full rank-six tensor exists.',
            'For its subcategory D on labels[0,1,5], K0(Z(D)) is the based ring A tensor A, with forgetful map multiplication A tensor A -> A.',
            'The complementary D-bimodule on labels[2,3,4] is equivalent to the regular D-bimodule, with X corresponding to the unit.',
            'Under these identifications, the relative center Z_D(C) has simples b and bt for b in the nine-simple basis of B=A tensor A, with F(t)=X and B central.',
        ],
        conditional_ring_consequences=[
            'The only B-simple whose forgetful image is the unit is(1,1); nonnegative sums introduce no other preimage of1.',
            'Duality and the exact regular module imply t*=t, and the B-part of t^2 is1.',
            'Therefore t^2=1+C t for C>=0 with F(C)=2+2a+b; there are exactly15 labelled C.',
            'For a B character chi and lambda^2-chi(C)lambda-1=0, the extension has formal codegree f_B(1+lambda^2).',
        ],
        A_tensor=A, B_basis=[[LABELS[i], LABELS[j]] for i,j in PAIR],
        extension_basis='B in the listed order, followed by Bt in the same order',
        lift_equations=['c00+c11+c22=2', 'c01+c10+c12+c21+c22=2',
                        'c02+c20+c11+c12+c21+c22=1'],
        lift_count=15, per_case_hard_timeout_seconds=CASE_SECONDS,
        complete=complete,
        excluded_conditional_rank18_count=sum(r['status']=='excluded_as_rank18_fusion_ring' for r in results),
        surviving_conditional_case_numbers=[r['case'] for r in results if r['status']=='survives_dnumber'],
        general_rank6_exclusion=False, cases=results)
    if args.verify:
        old = json.loads((HERE/'conditional_certificate.json').read_text())
        old_source = old['source']; new_source = report['source']
        for key in ('id', 'tensor_sha256', 'census_sha256', 'scripts_sha256'):
            require(old_source[key] == new_source[key], 'source/version drift: '+key)
        for a, b in zip(old['cases'], report['cases']):
            a.pop('seconds', None); b.pop('seconds', None)
        # Runtime descriptions and durations do not alter the exact artifact.
        old['source'] = report['source']
        require(old == report and complete, 'conditional replay mismatch/incomplete')
        require(json.loads((HERE/'input_tensor.json').read_text()) == row, 'input snapshot mismatch')
        print('VERIFIED: all15 conditional cases; general rank-six exclusion remains unproved.')
    else:
        write(HERE/'input_tensor.json', row)
        write(HERE/'conditional_certificate.json', report)
        print('COMPLETE', complete, 'CONDITIONAL EXCLUSIONS', report['excluded_conditional_rank18_count'],
              'SURVIVORS', report['surviving_conditional_case_numbers'])


if __name__ == '__main__':
    main()

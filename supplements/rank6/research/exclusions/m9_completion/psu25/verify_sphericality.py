#!/usr/bin/env python3
"""Exact exhaustive sphericalization certificate for R6_9_3748.

This proves forced sphericality, not existence or nonexistence.
All operations use integers or exact rational polynomial arithmetic.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent
SOURCE = HERE/'input_tensor.json'
SOURCE_SHA256 = '7d64ff2cd0dc0cb74c6faeb51bcb70d21d943834b5a0b1faf31828186b647b14'
A = [
    [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    [[0, 1, 0], [1, 0, 1], [0, 1, 1]],
    [[0, 0, 1], [0, 1, 1], [1, 1, 1]],
]
z = s.Symbol('z')


def require(condition, description):
    if not condition:
        raise ValueError(description)


def load_source():
    require(hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256,
            'frozen source fixture SHA256')
    row = json.loads(SOURCE.read_text())
    require(row['id'] == 'R6_9_3748', 'frozen source identifier')
    return row


def extension(c):
    R = [[[0]*6 for j in range(6)] for i in range(6)]
    for i, j, k in itertools.product(range(3), repeat=3):
        R[i][j][k] = R[i][j+3][k+3] = R[i+3][j][k+3] = R[i+3][j+3][k] = A[i][j][k]
        R[i+3][j+3][k+3] = sum(A[i][j][u]*c[v]*A[u][v][k] for u,v in itertools.product(range(3),repeat=2))
    return R


def doubled(R, S):
    T = [[[0]*12 for j in range(12)] for i in range(12)]
    for i,j,k in itertools.product(range(12),repeat=3):
        r,si = divmod(i,2)
        t,sj = divmod(j,2)
        u,sk = divmod(k,2)
        n = R[r][t][u]+(-1)**(si+sj+sk)*S[r][t][u]
        require(n % 2 == 0 and n >= 0, 'nonnegative integral sphericalization coefficients')
        T[i][j][k] = n//2
    return T


def based_checks(R):
    n = len(R)
    for i,j,k in itertools.product(range(n),repeat=3):
        require(R[i][j][k] == R[j][i][k] == R[i][k][j], 'self-dual Frobenius reciprocity')
    for i,j in itertools.product(range(n),repeat=2):
        require(R[0][i][j] == R[i][0][j] == R[i][j][0] == int(i == j), 'unit and duality')
    matrices = [s.Matrix(x) for x in R]
    for i,j in itertools.product(range(n),repeat=2):
        require(matrices[i]*matrices[j] == sum((R[i][j][k]*matrices[k] for k in range(n)),s.zeros(n)), 'associativity')
    return True


def casimir_polynomial(R):
    matrices = [s.Matrix(x) for x in R]
    K = sum((x*x for x in matrices),s.zeros(len(R)))
    return K.charpoly(z).as_poly()


def factors(p):
    out = []
    for f, multiplicity in s.factor_list(p)[1]:
        co = list(map(int,f.all_coeffs()))
        degree = f.degree()
        require(co[0] == 1 and co[-1] != 0 and f.is_irreducible, 'minimal polynomial')
        failures = []
        for j in range(1,degree+1):
            divisor = abs(co[-1])**j
            remainder = pow(co[j],degree,divisor)
            if remainder:
                failures.append(dict(j=j,divisor=str(divisor),remainder=str(remainder)))
        out.append(dict(coefficients=co,multiplicity=int(multiplicity),dnumber=not failures,failures=failures))
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',action='store_true')
    args = parser.parse_args()
    source = load_source()
    tensor = source.get('N',source.get('tensor'))
    require(tensor is not None,'source tensor field')
    R = extension([2,2,1])
    permutation = [0,1,5,2,3,4]
    require(R == [[[tensor[i][j][k] for k in permutation] for j in permutation] for i in permutation], 'exact source tensor')
    based_checks(R)
    pR = casimir_polynomial(R)
    records = []
    for p,q in itertools.product([-2,0,2],repeat=2):
        c = [p,q,1]
        S = extension(c)
        T = doubled(R,S)
        based_checks(T)
        pS = casimir_polynomial(S)
        pT = casimir_polynomial(T)
        require(s.Poly(2**12*pR.as_expr().subs(z,z/2)*pS.as_expr().subs(z,z/2),z) == pT, 'doubled Casimir decomposition')
        facS,facT = factors(pS),factors(pT)
        require(all(f['dnumber'] for f in facS) == all(f['dnumber'] for f in facT), 'rational scaling preserves dnumbers')
        records.append(dict(signed_coefficient=c,signed_formal_codegree_factors=facS,
                            sphericalization_formal_codegree_factors=facT,
                            rank12_based_ring_verified=True,
                            doubled_Casimir_factorization_verified=True,
                            survives=all(f['dnumber'] for f in facT)))
    require([r['signed_coefficient'] for r in records if r['survives']] == [[2,2,1]], 'unique spherical section')
    report = dict(ring='R6_9_3748',conclusion='Every characteristic-zero fusion categorification is spherical; the companion center proof then excludes all categorifications.',
                  source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                  verifier_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  sympy=s.__version__,exhaustive_gauge_reduced_domain=9,excluded=8,survivors=1,cases=records)
    target = HERE/'sphericality_certificate.json'
    if args.verify:
        require(json.loads(target.read_text()) == report,'saved certificate replay')
        print('Verified all 9 exact rank12 candidates; 8 excluded and the unique positive section survives.')
    else:
        target.write_text(json.dumps(report,indent=2)+'\n')
        print(target)


if __name__ == '__main__':
    main()

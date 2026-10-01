#!/usr/bin/env python3
"""Portable exact fifteen-case relative-center calculation for R6_9_3748.

The categorical applicability is proved in structural_reduction.tex.
This file imports only the accompanying verifier and SymPy.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

import sympy as s
from verify_sphericality import (
    A, SOURCE, based_checks, casimir_polynomial, extension as rank6_extension,
    factors, load_source, require,
)

HERE = Path(__file__).resolve().parent
PAIRS = list(itertools.product(range(3), repeat=2))
TARGET = [2,2,1]


def forget(c):
    return [sum(c[r]*A[i][j][k] for r,(i,j) in enumerate(PAIRS))
            for k in range(3)]


def lifts():
    bounds = [min(TARGET[k]//A[i][j][k] for k in range(3) if A[i][j][k])
              for i,j in PAIRS]
    candidates = [list(c) for c in itertools.product(*(range(b+1) for b in bounds))
                  if forget(c) == TARGET]
    require(len(candidates) == 15, 'complete rectangular domain has15 lifts')
    return bounds,candidates


def extension(B,c):
    n = len(B)
    R = [[[0]*(2*n) for _ in range(2*n)] for _ in range(2*n)]
    for i,j,k in itertools.product(range(n),repeat=3):
        R[i][j][k] = R[i][j+n][k+n] = R[i+n][j][k+n] = R[i+n][j+n][k] = B[i][j][k]
        R[i+n][j+n][k+n] = sum(B[i][j][u]*c[v]*B[u][v][k]
                                for u,v in itertools.product(range(n),repeat=2))
    return R


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',action='store_true')
    args = parser.parse_args()
    source = load_source()['N']
    perm = [0,1,5,2,3,4]
    require(rank6_extension(TARGET) == [[[source[i][j][k] for k in perm]
                for j in perm] for i in perm], 'exact frozen source tensor')
    B = [[[A[i][k][u]*A[j][l][v] for u,v in PAIRS]
           for k,l in PAIRS] for i,j in PAIRS]
    based_checks(B)
    bounds,candidates = lifts()
    rows=[]
    for number,c in enumerate(candidates,1):
        R = extension(B,c)
        based_checks(R)
        polynomial = casimir_polynomial(R)
        fac = factors(polynomial)
        survives = all(f['dnumber'] for f in fac)
        rows.append(dict(case=number,C=c,forgetful_image=forget(c),
                         rank18_based_ring_verified=True,
                         formal_codegree_polynomial=list(map(int,polynomial.all_coeffs())),
                         formal_codegree_factors=fac,survives=survives))
    survivors=[r['C'] for r in rows if r['survives']]
    require(sorted(survivors) == sorted([[2,2,1,0,0,0,0,0,0],[2,0,0,2,0,0,1,0,0]]),
            'only Q tensor1 and1 tensorQ survive')
    report=dict(ring='R6_9_3748',
                conclusion='Only the two one-sided lifts survive; the categorical proof applies this unconditionally.',
                source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                verifier_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                helper_sha256=hashlib.sha256((HERE/'verify_sphericality.py').read_bytes()).hexdigest(),
                sympy=s.__version__,rectangular_coefficient_bounds=bounds,
                exhaustive_domain=15,excluded=13,survivors=2,cases=rows)
    target=HERE/'relative_center_certificate.json'
    if args.verify:
        require(json.loads(target.read_text()) == report,'exact certificate replay')
        print('Verified all15 rank18 relative-center tensors;13 d-number exclusions and two one-sided survivors.')
    else:
        target.write_text(json.dumps(report,indent=2)+'\n')
        print(target)


if __name__ == '__main__':
    main()

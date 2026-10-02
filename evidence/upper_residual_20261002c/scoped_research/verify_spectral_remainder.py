#!/usr/bin/env python3
"""Finite exact necessary spectra; never a classification decision."""
import argparse
import itertools
import json
import math
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'evidence/upper_residual_20261002b/r7_nonintegral'))
from case_source import SOFTWARE, read_cases
sys.path.insert(0, str(SOFTWARE))
from rings import Characters, dual
from oriented_signed import validate_general


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def quotient_integral(u, v, a, b, norm):
    # (u+v sqrt5)/((a+b sqrt5)/2) = (c+d sqrt5)/(2 norm).
    c, d = u*a-5*v*b, v*a-u*b
    return c % norm == d % norm == 0 and (c//norm-d//norm) % 2 == 0


def divisors(u, v, bound):
    integers = [n for n in range(3, bound+1)
                if 2*u % n == 2*v % n == 0
                and ((2*u)//n-(2*v)//n) % 2 == 0]
    pairs = []
    for a in range(5, bound+1):
        for b in range(1, math.isqrt((a-4)**2//5)+1):
            if a % 2 != b % 2 or (a-4)**2 <= 5*b*b:
                continue  # both roots must be strictly greater than two
            norm = (a*a-5*b*b)//4
            if a*a % norm:
                continue  # exact quadratic d-number condition
            if quotient_integral(u,v,a,b,norm) and quotient_integral(u,v,a,-b,norm):
                pairs.append((a,b,norm))
    return integers, pairs


def spectra(u, v, bound):
    rest_bound = bound-2*u-2
    target = Q(1,2)-Q(2*u,u*u-5*v*v)
    integers, pairs = divisors(u,v,rest_bound)
    out = []
    for ns in itertools.combinations_with_replacement(integers,4):
        if sum(ns) <= rest_bound and sum((Q(1,n) for n in ns),Q(0)) == target:
            out.append((tuple(ns),()))
    for pair in pairs:
        a,b,norm = pair
        for ns in itertools.combinations_with_replacement(integers,2):
            if a+sum(ns) <= rest_bound and Q(a,norm)+sum((Q(1,n) for n in ns),Q(0)) == target:
                out.append((tuple(ns),(pair,)))
    by_reciprocal = {}
    for index,(a,b,norm) in enumerate(pairs):
        by_reciprocal.setdefault(Q(a,norm),[]).append(index)
    for i,(a,b,norm) in enumerate(pairs):
        for j in by_reciprocal.get(target-Q(a,norm),[]):
            if j >= i and a+pairs[j][0] <= rest_bound:
                out.append(((),((a,b,norm),pairs[j])))
    # Source characteristic polynomial is z^7 modulo two. Every monic
    # rational factor therefore has all its lower coefficients even.
    out = [(ns,ps) for ns,ps in out if all(n % 2 == 0 for n in ns)
           and all(a % 2 == norm % 2 == 0 for a,b,norm in ps)]
    return out, len(integers), len(pairs)


def verify():
    records = []
    for case, source in read_cases(['R7_4_1212','R7_4_1213']).items():
        R = source['tensor']; validate_general(R, nonnegative=True)
        require(dual(R) == list(range(7)), 'source is not all self-dual')
        require(all(R[i][j] == R[j][i] for i,j in itertools.product(range(7),repeat=2)), 'source not commutative')
        require(R[1][1][0] == 1 and all(R[1][i][i] == 1 and sum(R[1][i]) == 1 for i in range(2,7)), 'pointed fixing action')
        analysis = Characters(R); bound = int(analysis.C.trace())
        coefficients = [sum(R[i][i][j] for i in range(7)) for j in range(7)]
        require(sum(x*x for x in coefficients) == bound, 'Casimir coefficient trace identity')
        require(coefficients[:2] == [7,5], 'Casimir pointed coefficients')
        require([int(a)%2 for a in analysis.C.charpoly().all_coeffs()] == [1]+[0]*7, 'source Casimir mod2 polynomial')
        domains = []
        for j in range(2,7):
            sums = {0}
            for i in range(7):
                n = R[i][i][j]
                choices = [t for t in range(-n,n+1,2) if (n-t)%4 == 0]
                sums = {a+t for a in sums for t in choices}
            domains.append(sorted(sums))
        attainable = {}
        for xs in itertools.product(*domains):
            trace = 74+sum(x*x for x in xs)
            attainable[trace] = attainable.get(trace,0)+1
        branches = []
        for u,v in [(180,0),(270,90),(360,0),(450,90)]:
            raw, ni, nq = spectra(u,v,bound)
            surviving = []
            mod8_survivors = 0
            for ns,ps in raw:
                trace = 2*u+2+sum(ns)+sum(a for a,b,norm in ps)
                if (trace-bound)%8:
                    continue
                mod8_survivors += 1
                if trace not in attainable:
                    continue
                surviving.append({'integers':list(ns),'quadratics':[list(p) for p in ps],
                                  'total_trace':trace,'casimir_coefficient_vectors':attainable[trace]})
            branches.append({'delta':[u,v],'rational_divisors_checked':ni,'quadratic_pairs_checked':nq,
                             'spectra_after_mod2':len(raw),'spectra_after_mod8':mod8_survivors,
                             'residual_spectra':surviving})
        require([len(b['residual_spectra']) for b in branches] == [3,6,1,0], 'unexpected exact remainder')
        records.append({'id':case,'source_sha256':source['tensor_sha256'],'trace_bound':bound,
                        'casimir_coefficient_domains':domains,'branches':branches,'general_status':'unresolved'})
    return {'status':'PASS','scope':'conditional_necessary_reduction','classification_decisions':0,
            'remaining_global_dimensions':[[180,0],[270,90],[270,-90],[360,0]],'cases':records}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path); args=parser.parse_args()
    result=verify(); text=json.dumps(result,indent=2)
    if args.output: args.output.write_text(text+'\n')
    print(text)

#!/usr/bin/env python3
"""Independent exact audit of the saturated quadratic prime twist sign.

Work in Q[X]/Phi_p(X).  The canonical quadratic Gauss sum has positive
value sqrt(p) for p == 1 mod 4; the polynomial identities below do not
depend on floating point arithmetic.  This checks the finite Fourier
step of SATURATED_CONDUCTOR.md, not existence of a fusion category.
"""
from pathlib import Path
import argparse
import json


def need(value, message):
    if not value:
        raise ValueError(message)


def character(k, p):
    r = pow(k % p, (p - 1) // 2, p)
    return 0 if r == 0 else (1 if r == 1 else -1)


def reduce_coefficients(coefficients, p):
    cyclic = [0] * p
    for j, a in enumerate(coefficients):
        cyclic[j % p] += a
    return tuple(cyclic[j] - cyclic[p - 1] for j in range(p - 1))


def verify_prime(p):
    need(p % 4 == 1 and all(p % k for k in range(2, int(p ** .5) + 1)),
         'Expected a prime congruent to one modulo four')
    tau = [character(t, p) for t in range(p)]
    square = [0] * (2 * p - 1)
    for i, a in enumerate(tau):
        for j, b in enumerate(tau):
            square[i + j] += a * b
    need(reduce_coefficients(square, p) == (p,) + (0,) * (p - 2),
         'Exact Gauss-square identity failed')
    reduced_tau = reduce_coefficients(tau, p)
    supports = {}
    for sign in (-1, 1):
        # Equality eigenvector is F + sign*sqrt(p)*H.
        # For k != 0, its S-image Fourier coefficient is
        # sum_t chi(t)*zeta^(-kt) + sign*sqrt(p).
        support = []
        for k in range(1, p):
            fourier = [0] * p
            for t in range(p):
                fourier[(-k * t) % p] += character(t, p)
            lhs = reduce_coefficients(fourier, p)
            need(lhs == tuple(character(k, p) * a for a in reduced_tau),
                 'Exact Fourier/Gauss identity failed')
            coefficient = tuple(a + sign * b for a, b in zip(lhs, reduced_tau))
            if any(coefficient):
                support.append(k)
            need(bool(any(coefficient)) == (character(k, p) == sign),
                 'Incorrect quadratic class for saturated twist support')
        need(len(support) == (p - 1) // 2, 'Incorrect twist support size')
        supports[str(sign)] = support
    return {'prime': p, 'gauss_square': p, 'positive_gauss_root':
            'Classical quadratic Gauss identity for zeta_p=exp(2*pi*i/p)',
            'eigenvalue_sign_to_nontrivial_twist_exponents': supports}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    reports = [verify_prime(p) for p in (5, 13, 37)]
    report = {'status': 'PASS', 'arithmetic': 'exact integer polynomial identities',
              'scope': 'Quadratic-prime Fourier support in the saturated modular subrepresentation',
              'controls': reports,
              'R8_3_1768': {'conductor': 37, 'compression_eigenvalue': '-1/sqrt(37)',
                  'nontrivial_twist_exponents': reports[-1]['eigenvalue_sign_to_nontrivial_twist_exponents']['-1'],
                  'legendre_values_at_moments_1_to_4': [character(k, 37) for k in range(1, 5)],
                  'normalized_relative_trace': '(-1-chi_37(k)*sqrt(37))/36',
                  'application_scope': 'Nonrational dim(Z)/D; twist-one dimension-orbit objects are separate'}}
    path = Path(__file__).with_suffix('.json')
    if args.write:
        path.write_text(json.dumps(report, indent=2) + '\n')
    else:
        need(json.loads(path.read_text()) == report, 'Saved exact audit differs')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()

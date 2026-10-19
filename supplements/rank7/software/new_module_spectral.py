"""Exact spectral pruning of the anti-invariant involution-module system.

The input is a commutative fusion tensor. No pivotality is assumed. A
self-dual algebra generator with irreducible regular matrix is used; the
Perron factor cannot occur on a proper fixed-point principal block. Every
remaining integral symmetric matrix is enumerated by exact trace/norm and
modulo-two characteristic polynomial, then all ring relations are checked.
"""
import argparse
import itertools
import json
from pathlib import Path

import sympy as s

from involution_module import generated_basis, invs


def connected(M):
    seen = {0}
    while True:
        nxt = seen | {j for i in seen for j in range(M.rows) if M[i, j]}
        if nxt == seen:
            return len(seen) == M.rows
        seen = nxt


def mod2_coefficients(poly):
    return [int(c) % 2 for c in poly.all_coeffs()]


def perron_factor(factors):
    """Identify the largest root by disjoint exact rational intervals."""
    eps = s.Rational(1, 1024)
    while True:
        intervals = []
        for k, q in enumerate(factors):
            for (lo, hi), multiplicity in q.intervals(eps=eps):
                intervals.append((lo, hi, k))
        largest = max(intervals, key=lambda a: a[0])
        if all(largest == r or largest[0] > r[1] for r in intervals):
            return largest[2], [str(largest[0]), str(largest[1])]
        eps /= 2


def factor_multisets(factors, degree):
    def rec(k, remaining, selected):
        if k == len(factors):
            if remaining == 0:
                yield tuple(selected)
            return
        d = factors[k].degree()
        for a in range(remaining // d + 1):
            yield from rec(k + 1, remaining - a * d, selected + [a])
    yield from rec(0, degree, [])


def symmetric_candidates(B, trace, norm):
    """All parity-compatible symmetric matrices with given trace and norm."""
    f = B.rows
    entries = [(i, i) for i in range(f)]
    entries += [(i, j) for i in range(f) for j in range(i + 1, f)]
    choices = []
    for i, j in entries:
        weight = 1 if i == j else 2
        vals = [v for v in range(-int(B[i, j]), int(B[i, j]) + 1, 2)
                if weight * v * v <= norm]
        choices.append(vals)
    if any(not v for v in choices):
        return
    minimum = [0] * (len(entries) + 1)
    for k in range(len(entries) - 1, -1, -1):
        i, j = entries[k]
        minimum[k] = minimum[k + 1] + (1 if i == j else 2) * min(v*v for v in choices[k])
    M = s.zeros(f)
    def rec(k, remaining, diagonal_sum):
        if k == f and diagonal_sum != trace:
            return
        if k == len(entries):
            if remaining == 0:
                yield M.copy()
            return
        if remaining < minimum[k]:
            return
        i, j = entries[k]
        weight = 1 if i == j else 2
        for v in choices[k]:
            cost = weight*v*v
            if cost > remaining:
                continue
            M[i, j] = M[j, i] = v
            yield from rec(k + 1, remaining - cost, diagonal_sum + (v if i == j else 0))
    yield from rec(0, norm, 0)


def solve_generator(R, g, gen):
    n = len(R)
    if g not in invs(R) or any(R[i][j] != R[j][i] for i in range(n) for j in range(n)):
        return None
    fixed = [x for x in range(n) if R[g][x][x]]
    f = len(fixed)
    if not fixed or f == n:
        return None
    dual = [next(j for j in range(n) if R[i][j][0]) for i in range(n)]
    if dual[gen] != gen:
        return None
    regular = s.Matrix(R[gen])
    if not connected(regular):
        return None
    info = generated_basis(R, [gen])
    if info is None:
        return None
    words, inverse = info
    x = s.Symbol('x')
    polynomials = [s.Poly(sum(inverse[k, j]*x**len(word)
                             for j, word in enumerate(words)), x)
                   for k in range(n)]
    characteristic = regular.charpoly(x).as_poly()
    factors = [q for q, multiplicity in characteristic.factor_list()[1]]
    pf, pf_interval = perron_factor(factors)
    # A nonzero odd entry in a fixed object's action rules out a -1
    # diagonal entry of T_g, since T_i T_g = T_i for g i = i.
    force_g_identity = all(any(R[i][a][b] % 2 for i in fixed for b in fixed)
                           for a in fixed)
    allowed = [q for k, q in enumerate(factors) if k != pf and
               (not force_g_identity or (polynomials[g] - 1).rem(q).is_zero)]
    B = regular.extract(fixed, fixed)
    mod2 = mod2_coefficients(B.charpoly(x).as_poly())
    statistics = {'factor_multisets': 0, 'parity_spectra': 0,
                  'norm_matrices': 0, 'spectral_matrices': 0,
                  'full_representations': 0}
    spectra = []
    witness = None
    for mults in factor_multisets(allowed, f):
        statistics['factor_multisets'] += 1
        polynomial = s.Poly(1, x)
        minimal = s.Poly(1, x)
        for q, m in zip(allowed, mults):
            polynomial *= q**m
            if m:
                minimal *= q
        if mod2_coefficients(polynomial) != mod2:
            continue
        statistics['parity_spectra'] += 1
        coefficients = polynomial.all_coeffs()
        trace = -int(coefficients[1])
        norm = trace*trace - 2*int(coefficients[2]) if f >= 2 else trace*trace
        spectra.append({'coefficients': list(map(int, coefficients)),
                        'trace': trace, 'squared_norm': norm})
        for T in symmetric_candidates(B, trace, norm):
            statistics['norm_matrices'] += 1
            powers = [s.eye(f)]
            for j in range(1, n):
                powers.append(powers[-1]*T)
            value = sum((c*powers[j] for (j,), c in minimal.terms()), s.zeros(f))
            if value != s.zeros(f):
                continue
            statistics['spectral_matrices'] += 1
            mats = [sum((c*powers[j] for (j,), c in p.terms()), s.zeros(f))
                    for p in polynomials]
            if any(v.q != 1 for M in mats for v in M):
                continue
            if any(abs(mats[i][a, b]) > R[i][fixed[a]][fixed[b]] or
                   (mats[i][a, b] - R[i][fixed[a]][fixed[b]]) % 2
                   for i in range(n) for a in range(f) for b in range(f)):
                continue
            if any(mats[i].T != mats[dual[i]] for i in range(n)):
                continue
            if any(mats[i]*mats[j] != sum((R[i][j][k]*mats[k] for k in range(n)), s.zeros(f))
                   for i in range(n) for j in range(n)):
                continue
            statistics['full_representations'] += 1
            witness = [[[int(v) for v in row] for row in M.tolist()] for M in mats]
            break
        if witness is not None:
            break
    return {'kind': 'spectral_involution_module', 'involution': g,
            'generator': gen, 'fixed': fixed,
            'regular_characteristic_polynomial': list(map(int, characteristic.all_coeffs())),
            'perron_factor': list(map(int, factors[pf].all_coeffs())),
            'perron_isolating_interval': pf_interval,
            'forced_involution_identity': force_g_identity,
            'allowed_factors': [list(map(int, q.all_coeffs())) for q in allowed],
            'mod2_characteristic_polynomial': mod2,
            'spectra': spectra, 'search': statistics,
            'feasible': witness is not None, 'witness': witness}


def certificate(R):
    n = len(R)
    if any(R[i][j] != R[j][i] for i in range(n) for j in range(n)):
        return None
    for g in invs(R):
        if not any(R[g][a][a] for a in range(n)):
            continue
        for gen in range(1, n):
            result = solve_generator(R, g, gen)
            if result is not None and not result['feasible']:
                return result
    return None


def verify(R, record):
    result = solve_generator(R, record['involution'], record['generator'])
    if result != record or result['feasible']:
        raise ValueError('invalid spectral module exclusion')


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path)
    ap.add_argument('--verify', type=Path)
    ap.add_argument('--min-fixed', type=int, default=3)
    args = ap.parse_args()
    frozen = root/'verification/continuation/campaign_manifest.json'
    rows = (json.load(open(frozen))['inputs'] if frozen.exists()
            else json.load(open(root/'data/unresolved_tensors.json')))
    if args.verify:
        tensors = {r['id']: r['N'] for r in json.load(open(root/'data/census.json'))}
        records = json.load(open(args.verify))
        for record in records:
            verify(tensors[record['id']], record['certificate'])
        print('EXACT SPECTRAL MODULE CERTIFICATES VERIFIED', len(records))
    else:
        records = []
        for row in rows:
            R = row['N']
            if not any(sum(bool(R[g][a][a]) for a in range(len(R))) >= args.min_fixed for g in invs(R)):
                continue
            result = certificate(R)
            print(row['id'], 'excluded' if result else 'not excluded', flush=True)
            if result:
                records.append({'id': row['id'], 'status': 'excluded', 'certificate': result})
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(json.dumps(records, indent=2)+'\n')

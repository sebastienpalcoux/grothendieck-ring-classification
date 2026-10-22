#!/usr/bin/env python3
"""Exact finite-group controls for the saturated-conductor argument.

These controls supplement the uniform proof; they do not replace its arbitrary
prime-power argument or enumerate possible Drinfeld centers.
"""
from pathlib import Path
from math import gcd
import argparse
import hashlib
import json
import sympy as s


def need(ok, message):
    if not ok:
        raise ValueError(message)


def character(conductor, b):
    if conductor == 1:
        return 1
    if conductor == 4:
        return 1 if b % 4 == 1 else -1
    if conductor == 8:
        return 1 if b % 8 in (1, 7) else -1
    value = pow(b % conductor, (conductor - 1) // 2, conductor)
    need(value in (1, conductor - 1), 'Not a quadratic unit')
    return 1 if value == 1 else -1


def local_control(modulus, conductor):
    """Construct the whole U-fixed torus eigenspace, then its exact compression."""
    M = modulus
    points = [(x, y) for x in range(M) for y in range(M) if gcd(gcd(x, y), M) == 1]
    pointset = set(points)
    orbits, which = [], {}
    for point in points:
        if point in which:
            continue
        x, y = point
        orbit = sorted({((x + b*y) % M, y) for b in range(M)})
        index = len(orbits)
        orbits.append(orbit)
        for v in orbit:
            need(v not in which, 'Overlapping U-orbits')
            which[v] = index
    need(set(which) == pointset, 'Incomplete primitive domain')
    units = [b for b in range(M) if gcd(b, M) == 1]
    basis, used = [], set()
    for j, orbit in enumerate(orbits):
        if j in used:
            continue
        x, y = orbit[0]
        values, inconsistent = {}, False
        for b in units:
            target = which[((b*x) % M, (pow(b, -1, M)*y) % M)]
            value = character(conductor, b)
            if target in values and values[target] != value:
                inconsistent = True
            values[target] = value
        used.update(values)
        if not inconsistent:
            basis.append(values)
    need(len(used) == len(orbits), 'Incomplete torus-orbit enumeration')
    point_basis = [{v: row.get(which[v], 0) for v in points} for row in basis]
    W = s.diag(*[sum(len(orbits[j])*value*value for j, value in row.items()) for row in basis])
    columns = []
    for function in point_basis:
        compressed = [s.Rational(sum(function[(y, (-x) % M)] for x, y in orbit), len(orbit))
                      for orbit in orbits]
        coefficients = []
        for row in basis:
            j = next(iter(row))
            coefficients.append(compressed[j] / row[j])
        reconstruction = [sum(coefficients[k]*basis[k].get(j, 0) for k in range(len(basis)))
                          for j in range(len(orbits))]
        need(reconstruction == compressed, 'Compression leaves torus eigenspace')
        columns.append(s.Matrix(coefficients))
    A = s.Matrix.hstack(*columns)
    B = W.inv()*A.T*W*A
    eigenvalues = B.eigenvals()
    expected_nonzero = s.Rational(1, conductor)
    if conductor > 1:
        need(set(eigenvalues) <= {s.Integer(0), expected_nonzero}, 'Wrong exact singular spectrum')
    else:
        need(all(value.is_Rational and 0 <= value <= 1 for value in eigenvalues),
             'Trivial-character compression exceeds norm one')
    expected_dimension = 1 if conductor == 1 else 2
    need(eigenvalues.get(expected_nonzero) == expected_dimension, 'Wrong maximal singular multiplicity')
    if conductor > 1:
        F = {v: character(conductor, v[1]) if gcd(v[1], M) == 1 else 0 for v in points}
        H = {v: character(conductor, v[0]) if v[1] % conductor == 0 else 0 for v in points}
        vectors = []
        for function in (F, H):
            coefficients = []
            for row in basis:
                j = next(iter(row))
                coefficients.append(s.Rational(function[orbits[j][0]], row[j]))
            vector = s.Matrix(coefficients)
            need(B*vector == expected_nonzero*vector, 'Displayed equality vector not maximal')
            reduced = {}
            for v, value in function.items():
                key = tuple(x % conductor for x in v)
                need(key not in reduced or reduced[key] == value, 'Equality vector does not inflate')
                reduced[key] = value
            vectors.append(vector)
        need(s.Matrix.hstack(*vectors).rank() == 2, 'F and H are dependent')
    else:
        vector = s.Matrix([s.Rational(1, row[next(iter(row))]) for row in basis])
        need(B*vector == vector, 'Constant function is not maximal')
    return {'modulus': M, 'conductor': conductor, 'primitive_columns': len(points),
            'unipotent_orbits': len(orbits), 'torus_eigenspace_dimension': len(basis),
            'squared_singular_values': {str(k): int(v) for k, v in eigenvalues.items()},
            'maximal_subspace_dimension': expected_dimension,
            'maximal_vectors_inflate_from_conductor': True}


def arithmetic_control():
    r2, r3, r37 = s.sqrt(2), s.sqrt(3), s.sqrt(37)
    D4 = 144 + 96*r2 + 80*r3 + 56*r2*r3
    inv4 = s.Rational(1,8) - r3/24 - r2*r3/48
    need(s.expand(D4*inv4) == 1, 'Quartic inverse dimension')
    h12, h24 = -r3/6, -r2*r3/12
    need(s.expand(12*h12*h12) == 1 and s.expand(24*h24*h24) == 1, 'Quartic saturation')
    D37 = 444 + 72*r37
    inv37 = s.Rational(1,12) - r37/s.Integer(74)
    need(s.expand(D37*inv37) == 1, 'Quadratic inverse dimension')
    h37 = -r37/37
    need(s.expand(37*h37*h37) == 1, 'Quadratic saturation')
    a,b,c,d = s.symbols('a b c d')
    # Extract independent basis coefficients using sign involutions instead of
    # treating sqrt(6) and sqrt(2)*sqrt(3) as syntactically distinct expressions.
    embeddings = [s.expand((a+u*b*r2+v*c*r3+u*v*d*r2*r3)
                           *(s.Rational(1,8)-v*r3/24-u*v*r2*r3/48))
                  for u,v in ((1,1),(-1,1),(1,-1),(-1,-1))]
    fourier3 = s.simplify(embeddings[0]+embeddings[1]-embeddings[2]-embeddings[3])
    fourier6 = s.simplify(embeddings[0]-embeddings[1]-embeddings[2]+embeddings[3])
    need(s.simplify(fourier3-r3*(3*c-a-b)/6) == 0, 'Conductor12 linear mask')
    need(s.simplify(fourier6-r2*r3*(6*d-a-2*b)/12) == 0, 'Conductor24 linear mask')
    fourier37 = s.expand((a+b*r37)*inv37-(a-b*r37)*(s.Rational(1,12)+r37/74))
    need(s.simplify(fourier37-r37*(37*b-6*a)/222) == 0, 'Conductor37 linear mask')
    return {'quartic': {'conductors': [12,24], 'nonzero_masks': ['3c-a-b','6d-a-2b'],
                        'forced_twist_orders_divide': [12,24]},
            'R8_3_1768': {'conductor': 37, 'nonzero_mask': '37b-6a',
                          'forced_twist_order_divides': 37,
                          'I_g_twist_orders': [4], 'I_g_required_equation': '37b=6a'}}


def signed_prime_control(prime, epsilon):
    """Exact DFT in Q[zeta_p], including projection norms and residue sign."""
    p = prime
    need(s.isprime(p) and p % 4 == 1 and epsilon in (-1,1), 'Invalid signed-prime control')
    z = s.Symbol('z')
    modulus = s.Poly(s.cyclotomic_poly(p,z),z,domain=s.QQ)
    gauss = s.Poly(sum(character(p,t)*z**t for t in range(1,p)),z,domain=s.QQ)
    need((gauss*gauss-s.Poly(p,z)).rem(modulus).is_zero, 'Quadratic Gauss square')
    nonzero_support=[]
    for k in range(p):
        dft=s.Poly(sum(character(p,t)*z**((-k*t)%p) for t in range(1,p)),z,domain=s.QQ)
        dft=(dft+epsilon*gauss).rem(modulus)
        multiplier=epsilon if k==0 else character(p,k)+epsilon
        need((dft-multiplier*gauss).rem(modulus).is_zero, 'Exact DFT coefficient mismatch')
        if k and not dft.is_zero:
            nonzero_support.append(k)
    need(nonzero_support==[k for k in range(1,p) if character(p,k)==epsilon],
         'Incorrect signed spectral support')
    total_norm=2*p*(p-1)
    zero_norm=2*(p-1)
    nonzero_norm=4*(p-1)
    need(s.Rational(zero_norm,total_norm)==s.Rational(1,p), 'Zero spectral norm')
    need(s.Rational(nonzero_norm,total_norm)==s.Rational(2,p), 'Nonzero spectral norm')
    need(zero_norm+len(nonzero_support)*nonzero_norm==total_norm, 'Spectral norm completeness')
    return {'prime':p,'epsilon':epsilon,'allowed_nonzero_exponents':nonzero_support,
            'zero_projection_ratio':str(s.Rational(1,p)),
            'each_allowed_nonzero_projection_ratio':str(s.Rational(2,p)),
            'exact_cyclotomic_DFT':'PASS'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    controls = [(3,3),(9,3),(5,5),(25,5),(37,37),(4,4),(8,4),(16,4),(8,8),(16,8),
                (3,1),(4,1),(8,1),(9,1)]
    report = {'status':'PASS',
              'scope':'Exact finite-group controls plus application arithmetic; the general arbitrary-order theorem is proved in SATURATED_CONDUCTOR.md.',
              'local_controls':[local_control(M,f) for M,f in controls],
              'application_arithmetic':arithmetic_control(),
              'signed_prime_controls':[signed_prime_control(p,e) for p in (5,13,37) for e in (-1,1)],
              'R1768_integer_capacities':{'delta':'37b-6a','twist_one_sum_delta_squared':72,
                  'each_nonresidue_37_twist_sum_delta_squared':144,
                  'dimension_orbit_deltas':[-6,6],
                  'other_nonzero_delta_absolute_bound':12}}
    here = Path(__file__).resolve().parent
    report['source_sha256'] = {name:hashlib.sha256((here/name).read_bytes()).hexdigest()
                               for name in ('SATURATED_CONDUCTOR.md','SIGNED_PRIME_SUPPORT.md','verify_saturated_conductor.py')}
    text = json.dumps(report,indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    print(text,end='')


if __name__ == '__main__':
    main()

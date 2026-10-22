#!/usr/bin/env python3
"""Independent exact small-prime-power controls for conductor saturation.

The theorem is proved for arbitrary prime powers in the companion audit;
these controls check the equality-space assertion at excess prime powers,
including odd and nonreal local characters. They are not a proof by cutoff.
"""
from pathlib import Path
import argparse
import itertools
import json
import math
import sympy as s

HERE = Path(__file__).resolve().parent

def need(condition, message):
    if not condition:
        raise ValueError(message)

def audit(M, conductor, alpha):
    units = [b for b in range(M) if math.gcd(b, M) == 1]
    omega = [(x, y) for x in range(M) for y in range(M)
             if math.gcd(math.gcd(x, y), M) == 1]
    indices = {v: i for i, v in enumerate(omega)}
    orbit_id = {}
    orbits = []
    for x, y in omega:
        if (x, y) in orbit_id:
            continue
        orbit = sorted({((x + t*y) % M, y) for t in range(M)})
        number = len(orbits)
        orbits.append(orbit)
        orbit_id.update({v: number for v in orbit})
    need(all(s.simplify(alpha(b*c % M)-alpha(b)*alpha(c)) == 0
             for b, c in itertools.product(units, repeat=2)), 'character')
    columns = []
    done = set()
    for j, orbit in enumerate(orbits):
        if j in done:
            continue
        x, y = orbit[0]
        assignments = {}
        consistent = True
        for b in units:
            image = orbit_id[(b*x % M, pow(b, -1, M)*y % M)]
            value = s.conjugate(alpha(b))
            if image in assignments and s.simplify(assignments[image]-value) != 0:
                consistent = False
            assignments[image] = value
        done.update(assignments)
        if not consistent:
            continue
        columns.append(s.Matrix([assignments.get(orbit_id[v], 0) for v in omega]))
    F = s.Matrix.hstack(*columns)
    need(F.rank() == F.cols, 'independent U-fixed torus basis')
    images = []
    for column in columns:
        image = []
        for x, y in omega:
            image.append(s.simplify(sum(column[indices[(y, -(x+t*y) % M)]]
                                         for t in range(M))/M))
        images.append(s.Matrix(image))
    A = s.Matrix.hstack(*images)
    Q = s.simplify(F.conjugate().T*F/conductor-A.conjugate().T*A)
    need(Q == Q.conjugate().T, 'Hermitian norm defect')
    # All principal minors characterize positive semidefiniteness exactly.
    for n in range(1, Q.rows+1):
        for subset in itertools.combinations(range(Q.rows), n):
            need(s.simplify(Q.extract(subset, subset).det()) >= 0, 'norm bound')
    null = Q.nullspace()
    need(len(null) == (1 if conductor == 1 else 2), 'complete equality dimension')
    for coefficient in null:
        v = s.simplify(F*coefficient)
        reduced_values = {}
        for point, value in zip(omega, v):
            key = tuple(x % conductor for x in point)
            if key in reduced_values:
                need(s.simplify(reduced_values[key]-value) == 0, 'conductor descent')
            reduced_values[key] = value
        for x, y in omega:
            # T^c S v = S v, tested directly in the primitive-column model.
            need(s.simplify(v[indices[(y, -(x-conductor*y) % M)]]-
                            v[indices[(y, -x % M)]]) == 0, 'twist support')
    return {'modulus': M, 'conductor': conductor, 'primitive_columns': len(omega),
            'torus_unipotent_eigenspace_dimension': F.cols,
            'norm_defect_rank': Q.rank(), 'equality_dimension': len(null),
            'all_equality_vectors_descend_to_conductor': True,
            'T_power_S_identity': True}

def run():
    cases = [
        ('odd_mod4_at16', 16, 4, lambda b: s.Integer(1 if b % 4 == 1 else -1)),
        ('odd_mod3_at27', 27, 3, lambda b: s.Integer(1 if b % 3 == 1 else -1)),
        ('quadratic_mod8_at16', 16, 8, lambda b: s.Integer(1 if b % 8 in (1, 7) else -1)),
        ('quadratic_mod5_at25', 25, 5, lambda b: s.Integer(1 if b % 5 in (1, 4) else -1)),
        ('nonreal_mod5_at25', 25, 5, lambda b: {1:s.Integer(1),2:s.I,4:s.Integer(-1),3:-s.I}[b % 5]),
        ('trivial_at9', 9, 1, lambda b: s.Integer(1)),
    ]
    return {'kind': 'independent_exact_local_conductor_saturation_controls',
            'scope': 'Finite controls of the general equality-space proof, not a cutoff theorem or a categorification claim',
            'cases': [{'name': name, **audit(M, c, alpha)} for name, M, c, alpha in cases],
            'status': 'PASS'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = run()
    path = HERE/'conductor_local_audit.json'
    if args.write:
        path.write_text(json.dumps(result, indent=2)+'\n')
    else:
        need(result == json.loads(path.read_text()), 'frozen local controls')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()

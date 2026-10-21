"""Independent column-space check of all saved stable mod-two classes.

This imports no discovery code. It uses permutations for D8 and A6,
highest-bit column elimination, and tests every boundary by span membership.
"""
from pathlib import Path
from itertools import product, permutations
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'integral/a6_relative_cohomology.json'
E = tuple(range(6))

def check(v, message):
    if not v:
        raise ValueError(message)

def mul(p, q):
    return tuple(p[q[i]] for i in range(6))

def inv(p):
    return tuple(p.index(i) for i in range(6))

def power(p, n):
    a = E
    for _ in range(n):
        a = mul(a, p)
    return a

R = (1, 2, 3, 0, 5, 4)
S = (2, 1, 0, 3, 5, 4)
# Keep only the saved vector's declared coordinate order; all operations use
# permutations rather than the discovery program's semidirect-product law.
P = tuple(mul(power(R, i), power(S, j)) for i, j in product(range(4), range(2)))
H = tuple(g for g in P if g[5] == 5)
A6 = tuple(p for p in permutations(range(6))
           if sum(p[i] > p[j] for i in range(6) for j in range(i+1, 6)) % 2 == 0)
check(len(set(P)) == 8 and len(H) == 4 and len(A6) == 360, 'group orders')
check(all(mul(x, y) in P for x in P for y in P), 'D8 closure')

def basis(vectors):
    pivots = {}
    for v in vectors:
        while v:
            k = v.bit_length()-1
            if k in pivots:
                v ^= pivots[k]
            else:
                pivots[k] = v
                break
    return pivots

def contains(v, pivots):
    while v:
        k = v.bit_length()-1
        if k not in pivots:
            return False
        v ^= pivots[k]
    return True

def differential(group, n):
    nonunit = [g for g in group if g != E]
    domain = tuple(product(nonunit, repeat=n))
    codomain = tuple(product(nonunit, repeat=n+1))
    position = {t:i for i, t in enumerate(domain)}
    columns = [0]*len(domain)
    for row, t in enumerate(codomain):
        terms = [t[1:], t[:-1]]
        terms += [t[:i]+(mul(t[i], t[i+1]),)+t[i+2:] for i in range(n)]
        for u in terms:
            if E not in u:
                columns[position[u]] ^= 1 << row
    return domain, codomain, columns

def image(columns, v):
    w = 0
    while v:
        k = v.bit_length()-1
        w ^= columns[k]
        v ^= 1 << k
    return w

def main():
    raw = SOURCE.read_bytes()
    saved = json.loads(raw)
    output = {'source_sha256': hashlib.sha256(raw).hexdigest(), 'degrees': {}}
    for degree in (2, 3):
        coordinates, _, differential_columns = differential(P, degree)
        _, boundary_coordinates, boundaries = differential(P, degree-1)
        check(coordinates == boundary_coordinates, 'cochain order')
        boundary_basis = basis(boundaries)
        cocycle_dimension = len(coordinates)-len(basis(differential_columns))
        saved_vectors = [sum(bit << i for i, bit in enumerate(v))
                         for v in saved[str(degree)]['basis_normalized_cochain_bits']]
        check({tuple(r['basis_bits']) for r in saved[str(degree)]['all_classes']}
              == set(product((0, 1), repeat=len(saved_vectors))),
              'not every cohomology class is listed')
        check(all(image(differential_columns, v) == 0 for v in saved_vectors), 'saved representative not cocycle')
        check(len(basis(boundaries+saved_vectors)) == cocycle_dimension,
              'saved representatives do not span cohomology')
        check(len(boundary_basis)+len(saved_vectors) == cocycle_dimension,
              'saved representatives not independent modulo boundaries')
        position = {t:i for i, t in enumerate(coordinates)}
        tests = []
        for g in A6:
            gi = inv(g)
            K = tuple(x for x in P if mul(mul(gi, x), g) in P)
            theta = {x:mul(mul(gi, x), g) for x in K}
            _, local_coordinates, local_boundaries = differential(K, degree-1)
            tests.append((local_coordinates, theta, basis(local_boundaries)))
        _, h_coordinates, h_boundaries = differential(H, degree-1)
        h_basis = basis(h_boundaries)
        stable_count = relative_count = 0
        for record in saved[str(degree)]['all_classes']:
            v = 0
            for take, representative in zip(record['basis_bits'], saved_vectors):
                if take:
                    v ^= representative
            def value(t):
                return (v >> position[t]) & 1
            stable = True
            for local, theta, local_basis in tests:
                difference = sum((value(t)^value(tuple(theta[x] for x in t))) << i
                                 for i, t in enumerate(local))
                if not contains(difference, local_basis):
                    stable = False
                    break
            restriction = sum(value(t) << i for i, t in enumerate(h_coordinates))
            relative = contains(restriction, h_basis)
            check(stable == record['stable'], 'stable class disagreement')
            check(relative == record['restriction_to_point_V4_is_zero'], 'restriction disagreement')
            stable_count += stable
            relative_count += stable and relative
        check((stable_count, relative_count) == ((2, 1) if degree == 2 else (4, 2)), 'wrong stable counts')
        output['degrees'][str(degree)] = {
            'cocycle_dimension': cocycle_dimension,
            'boundary_dimension': len(boundary_basis),
            'cohomology_dimension': len(saved_vectors),
            'stable_classes': stable_count,
            'stable_restriction_kernel': relative_count,
            'conjugations_checked': len(A6),
        }
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()

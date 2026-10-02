#!/usr/bin/env python3
"""Exact premises of twelve theoretical general rank-seven exclusions.

Python 3 standard library only. All assertions that affect correctness are
explicit exceptions and survive python3 -O. This checks full census tensors,
ring axioms, positive dimensions, adjoint closure, invertible actions and the
small finite groups used in the written arguments. Category-theoretic inputs
are separately stated with their original hypotheses in STRUCTURAL_INPUTS.md.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROFILES = {
    'R7_2_50': ([1,1,3,6,6,3,2], 'D96_new', 'C2'),
    'R7_2_70': ([1,1,1,1,2,4,4], 'eight_p', 'V4'),
    'R7_2_113': ([1,1,3,3,6,6,2], 'D96_existing', 'C2'),
    'R7_2_213': ([1,1,1,2,4,4,1], 'eight_p', 'C4'),
    'R7_2_273': ([1,6,6,1,2,3,3], 'D96_existing', 'C2'),
    'R7_2_280': ([1,6,6,1,2,3,3], 'D96_new', 'C2'),
    'R7_3_386': ([1,1,7,7,2,2,2], 'D112', 'C2'),
    'R7_3_398': ([1,1,2,2,6,2,2], 'D54', 'C2'),
    'R7_3_478': ([1,1,2,2,6,2,2], 'D54', 'C2'),
    'R7_3_966': ([1,7,7,1,2,2,2], 'D112', 'C2'),
    'R7_4_358': ([1,1,1,1,2,8,8], 'eight_p', 'V4'),
    'R7_4_963': ([1,1,2,10,10,10,2], 'D310', 'C2'),
}
PROOFS = {
    'eight_p': 'EIGHT_P_GENERAL_PROOF.md',
    'D96_new': 'D96_NEW_BRANCH_PROOF.md',
    'D96_existing': 'D96_EXISTING_BRANCH_PROOF.md',
    'D112': 'D112_GENERAL_PROOF.md',
    'D54': 'D54_GENERAL_PROOF.md',
    'D310': 'D310_GENERAL_PROOF.md',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def file_digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def root_from_location():
    for p in (HERE, *HERE.parents):
        if (p/'supplements/rank7/data/rank7_tables.txt.gz').is_file():
            return p
    raise FileNotFoundError('Pass --repository /absolute/path/to/repository')


def closure(T, initial):
    out = set(initial)
    while True:
        before = set(out)
        for i, j in itertools.product(before, repeat=2):
            out.update(k for k, a in enumerate(T[i][j]) if a)
        if out == before:
            return sorted(out)


def ring_premises(rid, T):
    d, family, expected_group = PROFILES[rid]
    n = 7
    require(len(T) == n and all(len(A) == n and all(len(row) == n for row in A)
                                for A in T), rid+': shape')
    require(all(type(a) is int and a >= 0 for A in T for row in A for a in row),
            rid+': nonnegative integral entries')
    require(all(T[0][i][j] == T[i][0][j] == int(i == j)
                for i,j in itertools.product(range(n), repeat=2)), rid+': unit')
    require(all(sum(T[i][j][k]*d[k] for k in range(n)) == d[i]*d[j]
                for i,j in itertools.product(range(n), repeat=2)), rid+': FP character')
    require(all(T[i][j][k] == T[j][i][k]
                for i,j,k in itertools.product(range(n), repeat=3)), rid+': commutativity')
    dual = []
    for i in range(n):
        js = [j for j in range(n) if T[i][j][0]]
        require(len(js) == 1 and T[i][js[0]][0] == 1, rid+': duality')
        dual.append(js[0])
    require(all(dual[dual[i]] == i for i in range(n)), rid+': dual involution')
    require(all(T[i][j][k] == T[dual[i]][k][j]
                for i,j,k in itertools.product(range(n), repeat=3)), rid+': reciprocity')
    for i,j,k,l in itertools.product(range(n), repeat=4):
        require(sum(T[i][j][s]*T[s][k][l] for s in range(n)) ==
                sum(T[j][k][s]*T[i][s][l] for s in range(n)), rid+': associativity')
    inv = [i for i,a in enumerate(d) if a == 1]
    perms = {}
    orders = {}
    for g in inv:
        require(all(sum(T[g][i]) == 1 for i in range(n)), rid+': invertible action')
        p = [row.index(1) for row in T[g]]
        require(sorted(p) == list(range(n)), rid+': invertible permutation')
        perms[g] = p
        x, order = 0, 0
        while True:
            x = p[x]
            order += 1
            if x == 0:
                break
            require(order <= len(inv), rid+': invertible group')
        orders[g] = order
    actual_group = ('C2' if len(inv) == 2 else
                    'C4' if max(orders.values()) == 4 else 'V4')
    require(actual_group == expected_group, rid+': invertible group type')
    ad_seeds = {0}
    for i in range(n):
        ad_seeds.update(k for k,a in enumerate(T[i][dual[i]]) if a)
    ad = closure(T, ad_seeds)
    require(ad == list(range(n)), rid+': adjoint closure')
    result = {'id': rid, 'status': 'PASS', 'scope': 'general_complex',
              'family': family, 'proof': PROOFS[family], 'dimensions': d,
              'global_dimension': sum(a*a for a in d), 'duals': dual,
              'invertibles': inv, 'invertible_group': actual_group,
              'invertible_orders': orders, 'invertible_actions': perms,
              'adjoint_closure': ad, 'dimension_equations_checked': 49,
              'associativity_equations_checked': 2401}
    if family == 'eight_p':
        require(all(perms[g][i] == i for g in inv for i in range(n) if d[i] > 1),
                rid+': nonunit invertible stabilizers')
        h = next(g for g in inv if orders[g] == 2)
    else:
        h = inv[1]
    p = perms[h]
    fixed_by_dimension = {a: [i for i in range(n) if d[i] == a and p[i] == i]
                          for a in sorted(set(d))}
    if family == 'D96_new':
        require(len(fixed_by_dimension[2]) == 1 and
                not fixed_by_dimension[3] and not fixed_by_dimension[6],
                rid+': D96 new sign branch')
    elif family == 'D96_existing':
        require(len(fixed_by_dimension[2]) == 1 and
                not fixed_by_dimension[3] and len(fixed_by_dimension[6]) == 2,
                rid+': D96 existing sign branch')
    elif family == 'D112':
        require(len(fixed_by_dimension[2]) == 3 and not fixed_by_dimension[7],
                rid+': D112 sign branch')
    elif family in ('D54', 'D310'):
        require(all(p[i] == i for i in range(n) if d[i] > 1), rid+': sign action')
    deeq, visited = [], set()
    for i in range(n):
        if i in visited:
            continue
        if p[i] == i:
            require(d[i] % 2 == 0, rid+': orbit divisibility')
            deeq += [d[i]//2]*2
            visited.add(i)
        else:
            require(d[p[i]] == d[i], rid+': sign preserves dimensions')
            deeq.append(d[i])
            visited.update([i,p[i]])
    expected = {'D96_new': [1,1,1,3,6], 'D96_existing': [1,1,1,3,3,3,3,3],
                'D112': [1]*7+[7], 'D54': [1]*9+[3,3],
                'D310': [1,1,1,1,1,5,5,5,5,5,5]}
    if family == 'eight_p':
        expected_deeq = [1]*4+[max(d)//2]*4
    else:
        expected_deeq = expected[family]
    require(sorted(deeq) == sorted(expected_deeq), rid+': first descent type')
    require(sum(a*a for a in deeq)*2 == sum(a*a for a in d), rid+': descent dimension')
    result['sign_invertible'] = h
    result['sign_permutation'] = p
    result['first_deequivariantization_dimensions'] = sorted(deeq)
    if family == 'D310':
        subrings = []
        for mask in range(1 << 6):
            s = {0}|{i+1 for i in range(6) if mask >> i & 1}
            if all(dual[i] in s for i in s) and closure(T,s) == sorted(s):
                subrings.append({'indices': sorted(s), 'dimension':sum(d[i]**2 for i in s)})
        require(sorted({x['dimension'] for x in subrings}) == [1,2,10,310],
                rid+': complete fusion subring dimensions')
        result['all_fusion_subrings'] = subrings
    return result


def binary_linear_groups(n):
    """Enumerate matrices by their columns; retain their full permutations."""
    v = list(range(1 << n))
    for columns in itertools.product(range(1,1 << n), repeat=n):
        perm = []
        for x in v:
            y = 0
            for k in range(n):
                if x >> k & 1:
                    y ^= columns[k]
            perm.append(y)
        if len(set(perm)) == 1 << n:
            yield tuple(perm)


def compose(a,b):
    return tuple(a[b[x]] for x in range(len(a)))


def finite_groups():
    gl3 = list(binary_linear_groups(3))
    require(len(gl3) == 168, 'GL3(2) complete enumeration')
    one3 = tuple(range(8))
    singer = None
    for g in gl3:
        power = one3
        powers = []
        for _ in range(7):
            power = compose(g,power)
            powers.append(power)
        if powers[-1] == one3 and g != one3:
            singer = g
            break
    require(singer is not None, 'Singer exists')
    powers, power = {}, one3
    for k in range(1,7):
        power = compose(singer,power)
        powers[power] = k
    exponents = []
    for s in gl3:
        inverse = tuple(s.index(i) for i in range(8))
        conjugate = compose(compose(s,singer),inverse)
        if conjugate in powers:
            exponents.append(powers[conjugate])
    require(len(exponents) == 21 and sorted(set(exponents)) == [1,2,4],
            'Singer normalizer and conjugation exponents')
    require(6 not in exponents, 'No Singer inversion')
    gl4_count = 0
    inv4_count = 0
    minimum_fixed = 16
    orthogonal_v4 = 0
    q = lambda x: ((x & 1)*((x >> 2)&1) + ((x >> 1)&1)*((x >> 3)&1)) % 2
    for p in binary_linear_groups(4):
        gl4_count += 1
        if all(p[p[x]] == x for x in range(16)):
            inv4_count += 1
            minimum_fixed = min(minimum_fixed, sum(p[x] == x for x in range(16)))
        if all(q(x) == q(p[x]) for x in range(16)):
            orthogonal_v4 += 1
    require(gl4_count == 20160 and minimum_fixed == 4, 'C2^4 involution bound')
    require(orthogonal_v4 == 72, 'BrPic(VecV4) order')
    z4_gl_count, z4_involutions, z4_minimum, orthogonal_c4 = 0,0,16,0
    points = list(itertools.product(range(4), repeat=2))
    for a,b,c,d in itertools.product(range(4), repeat=4):
        if (a*d-b*c) % 2 != 1:
            continue
        z4_gl_count += 1
        p = tuple(points.index(((a*x+b*y)%4,(c*x+d*y)%4)) for x,y in points)
        if all(p[p[x]] == x for x in range(16)):
            z4_involutions += 1
            z4_minimum = min(z4_minimum, sum(p[x] == x for x in range(16)))
        if all((x*y)%4 == (points[p[k]][0]*points[p[k]][1])%4
               for k,(x,y) in enumerate(points)):
            orthogonal_c4 += 1
    require(z4_gl_count == 96 and z4_minimum == 4, 'C4^2 involution bound')
    require(orthogonal_c4 == 4, 'BrPic(VecC4) order')
    require(orthogonal_c4 % 5 and orthogonal_v4 % 5, 'No order5 BrPic element')
    # All possible p=5/17 second-descent partitions, before divisibility.
    partitions5 = [{'invertibles': 10-4*b, 'dimension2_objects': b} for b in range(3)]
    require(partitions5 == [{'invertibles':10,'dimension2_objects':0},
                           {'invertibles':6,'dimension2_objects':1},
                           {'invertibles':2,'dimension2_objects':2}], 'p5 partitions')
    partitions17 = [{'invertibles':2, 'dimension2_objects':8-4*b,
                     'dimension4_objects':b} for b in range(3)]
    require(all(2+4*x['dimension2_objects']+16*x['dimension4_objects'] == 34
                for x in partitions17), 'p17 partitions')
    require(34 % 4 != 0, 'p17 Frobenius exclusion')
    return {'GL3_2_order':168, 'Singer_normalizer_order':21,
            'Singer_conjugation_exponents':sorted(set(exponents)),
            'GL4_2_order':gl4_count, 'C2_4_involutions_including_identity':inv4_count,
            'C2_4_minimum_involution_fixed_points':minimum_fixed,
            'GL2_Z4_order':z4_gl_count, 'C4_2_involutions_including_identity':z4_involutions,
            'C4_2_minimum_involution_fixed_points':z4_minimum,
            'BrPic_Vec_C4_order':orthogonal_c4, 'BrPic_Vec_V4_order':orthogonal_v4,
            'second_descent_p5_partitions':partitions5,
            'second_descent_p17_partitions':partitions17}


def verify(repository):
    repository = Path(repository).resolve()
    recovery = repository/'evidence/upper_residual_20261002b_recovery'
    decisions = json.loads((recovery/'decisions.json').read_text())
    previous = json.loads((recovery/'previous_records.json').read_text())
    cert = json.loads((HERE/'approved_general_decisions.json').read_text())
    require(len(cert['records']) == 12 and {x['id'] for x in cert['records']} == set(PROFILES),
            'complete twelve-case inventory')
    raw = gzip.open(repository/'supplements/rank7/data/rank7_tables.txt.gz','rb').read()
    require(hashlib.sha256(raw).hexdigest() == cert['raw_census_sha256'], 'raw census hash')
    lines = raw.decode().splitlines()
    by_dec = {x['id']:x for x in decisions}
    by_previous = {x['id']:x for x in previous}
    results = []
    for binding in cert['records']:
        rid = binding['id']
        dec, old = by_dec[rid], by_previous[rid]
        require(dec['status'] == 'excluded' and dec['scope'] == 'general_complex', rid+': decision scope')
        require(old['source_line'] == binding['source_line'], rid+': source line metadata')
        source = json.loads(lines[binding['source_line']-1].replace('{','[').replace('}',']'))
        T = dec['census_tensor']
        require(source == T == old['tensor'], rid+': all343 source coefficients')
        require(digest(T) == binding['tensor_sha256'] == dec['census_tensor_sha256'],
                rid+': tensor fingerprint')
        r = ring_premises(rid,T)
        r.update({'source_line':binding['source_line'], 'tensor_sha256':digest(T)})
        results.append(r)
    # Negative controls must reject even under -O; they cannot be disabled by assertions.
    control = json.loads(json.dumps(by_dec['R7_2_70']['census_tensor']))
    control[0][0][0] = 2
    try:
        ring_premises('R7_2_70',control)
    except ValueError:
        pass
    else:
        raise ValueError('unit tamper not rejected')
    control = json.loads(json.dumps(by_dec['R7_2_50']['census_tensor']))
    control[1][3] = [0,0,0,1,0,0,0]
    try:
        ring_premises('R7_2_50',control)
    except ValueError:
        pass
    else:
        raise ValueError('sign-action tamper not rejected')
    groups = finite_groups()
    sources = {p.name:file_digest(p) for p in sorted(HERE.iterdir())
               if p.suffix in ('.py','.md') or p.name == 'approved_general_decisions.json'}
    return {'status':'PASS', 'scope':'general_complex', 'case_count':12,
            'records':results, 'finite_group_checks':groups,
            'negative_controls':['unit_tamper_rejected','sign_tamper_rejected'],
            'raw_census_sha256':cert['raw_census_sha256'], 'source_files_sha256':sources}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = verify(args.repository or root_from_location())
    payload = json.dumps(report,indent=2)+'\n'
    if args.output:
        args.output.write_text(payload)
    print(payload, end="")


if __name__ == '__main__':
    main()
